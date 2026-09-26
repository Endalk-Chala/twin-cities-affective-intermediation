# Organization-emotion bipartite network analysis
# Twin Cities Affective Intermediation project
# Produces both raw and organization-normalized network graphs.
#
# Required packages:
# install.packages(c("tidyverse", "igraph", "tidygraph", "ggraph", "ggrepel"))

library(tidyverse)
library(igraph)
library(tidygraph)
library(ggraph)
library(ggrepel)

input_file <- "data/processed/full_corpus_coded_master_v1.csv"
output_edge_file <- "analysis/tables/org_emotion_edges_v1.csv"
output_node_file <- "analysis/tables/org_emotion_node_metrics_v1.csv"
output_raw_png <- "analysis/figures/org_emotion_bipartite_raw_v1.png"
output_raw_pdf <- "analysis/figures/org_emotion_bipartite_raw_v1.pdf"
output_norm_png <- "analysis/figures/org_emotion_bipartite_normalized_v1.png"
output_norm_pdf <- "analysis/figures/org_emotion_bipartite_normalized_v1.pdf"

dir.create("analysis/tables", recursive = TRUE, showWarnings = FALSE)
dir.create("analysis/figures", recursive = TRUE, showWarnings = FALSE)

dat <- readr::read_csv(input_file, show_col_types = FALSE)

emotion_cols <- c(
  "fear_intensity",
  "anxiety_uncertainty_intensity",
  "anger_intensity",
  "moral_outrage_intensity",
  "grief_sadness_intensity",
  "solidarity_intensity",
  "care_compassion_intensity",
  "empathy_intensity",
  "hope_intensity",
  "gratitude_intensity",
  "pride_intensity",
  "reassurance_intensity",
  "defiance_intensity",
  "urgency_emotion_intensity"
)

emotion_labels <- c(
  fear_intensity = "Fear",
  anxiety_uncertainty_intensity = "Anxiety / uncertainty",
  anger_intensity = "Anger",
  moral_outrage_intensity = "Moral outrage",
  grief_sadness_intensity = "Grief / sadness",
  solidarity_intensity = "Solidarity",
  care_compassion_intensity = "Care / compassion",
  empathy_intensity = "Empathy",
  hope_intensity = "Hope",
  gratitude_intensity = "Gratitude",
  pride_intensity = "Pride",
  reassurance_intensity = "Reassurance",
  defiance_intensity = "Defiance",
  urgency_emotion_intensity = "Urgency"
)

missing_cols <- setdiff(c("org_id", "organization", "item_id", emotion_cols), names(dat))
if (length(missing_cols) > 0) {
  stop("Missing required columns: ", paste(missing_cols, collapse = ", "))
}

# ------------------------------------------------------------
# 1. Organization-level denominators
# ------------------------------------------------------------

org_counts <- dat %>%
  distinct(item_id, org_id, organization) %>%
  count(org_id, organization, name = "observed_items")

# ------------------------------------------------------------
# 2. Long-form organization-emotion data
# ------------------------------------------------------------

long <- dat %>%
  select(item_id, org_id, organization, all_of(emotion_cols)) %>%
  mutate(across(all_of(emotion_cols), ~ replace_na(as.numeric(.x), 0))) %>%
  pivot_longer(
    cols = all_of(emotion_cols),
    names_to = "emotion_var",
    values_to = "intensity"
  ) %>%
  mutate(
    emotion = unname(emotion_labels[emotion_var]),
    present = intensity > 0
  )

edges <- long %>%
  group_by(org_id, organization, emotion) %>%
  summarise(
    emotion_item_count = sum(present, na.rm = TRUE),
    raw_intensity_sum = sum(intensity, na.rm = TRUE),
    mean_intensity_all_items = mean(intensity, na.rm = TRUE),
    mean_intensity_when_present = ifelse(
      sum(present, na.rm = TRUE) > 0,
      mean(intensity[present], na.rm = TRUE),
      0
    ),
    .groups = "drop"
  ) %>%
  left_join(org_counts, by = c("org_id", "organization")) %>%
  mutate(
    normalized_intensity_per_item = ifelse(observed_items > 0, raw_intensity_sum / observed_items, 0),
    prevalence_share = ifelse(observed_items > 0, emotion_item_count / observed_items, 0)
  ) %>%
  filter(raw_intensity_sum > 0)

readr::write_csv(edges, output_edge_file)

# ------------------------------------------------------------
# 3. Helper to construct graph and metrics
# ------------------------------------------------------------

build_bipartite <- function(edge_df, weight_col) {
  d <- edge_df %>%
    transmute(
      from = paste0("ORG::", org_id),
      to = paste0("EMO::", emotion),
      weight = .data[[weight_col]],
      org_id = org_id,
      organization = organization,
      emotion = emotion,
      observed_items = observed_items,
      raw_intensity_sum = raw_intensity_sum,
      normalized_intensity_per_item = normalized_intensity_per_item,
      prevalence_share = prevalence_share
    )

  g <- graph_from_data_frame(d %>% select(from, to, weight), directed = FALSE)
  E(g)$weight <- E(g)$weight
  E(g)$distance <- 1 / pmax(E(g)$weight, 1e-8)

  org_lookup <- edge_df %>%
    distinct(org_id, organization, observed_items) %>%
    mutate(name = paste0("ORG::", org_id), type = "organization", label = organization)

  emo_lookup <- tibble(
    emotion = unique(edge_df$emotion)
  ) %>%
    mutate(name = paste0("EMO::", emotion), type = "emotion", label = emotion)

  lookup <- bind_rows(
    org_lookup %>% select(name, type, label, observed_items),
    emo_lookup %>% mutate(observed_items = NA_integer_) %>% select(name, type, label, observed_items)
  )

  metrics <- tibble(
    name = V(g)$name,
    degree = degree(g),
    weighted_degree = strength(g, weights = E(g)$weight),
    betweenness = betweenness(g, weights = E(g)$distance, normalized = TRUE)
  ) %>%
    left_join(lookup, by = "name")

  list(graph = g, metrics = metrics)
}

raw_net <- build_bipartite(edges, "raw_intensity_sum")
norm_net <- build_bipartite(edges, "normalized_intensity_per_item")

raw_metrics <- raw_net$metrics %>% mutate(network = "raw")
norm_metrics <- norm_net$metrics %>% mutate(network = "normalized")
readr::write_csv(bind_rows(raw_metrics, norm_metrics), output_node_file)

# ------------------------------------------------------------
# 4. Plotting helper
# ------------------------------------------------------------

plot_bipartite <- function(net_obj, title, subtitle, output_png, output_pdf) {
  g <- net_obj$graph
  metrics <- net_obj$metrics

  graph_tbl <- as_tbl_graph(g) %>%
    activate(nodes) %>%
    left_join(metrics, by = "name") %>%
    mutate(
      node_type = factor(type, levels = c("organization", "emotion")),
      label_show = ifelse(
        type == "emotion" | weighted_degree >= quantile(weighted_degree[type == "organization"], 0.75, na.rm = TRUE),
        label,
        NA_character_
      )
    )

  set.seed(20260926)

  p <- ggraph(graph_tbl, layout = "fr", weights = weight) +
    geom_edge_link(
      aes(width = weight),
      alpha = 0.28,
      show.legend = FALSE,
      lineend = "round"
    ) +
    geom_node_point(
      aes(size = weighted_degree, shape = node_type),
      stroke = 0.45
    ) +
    geom_node_text(
      aes(label = label_show),
      repel = TRUE,
      size = 3.1,
      max.overlaps = Inf
    ) +
    scale_edge_width(range = c(0.15, 3.4)) +
    scale_size_continuous(range = c(3.2, 11)) +
    guides(size = "none", shape = guide_legend(title = NULL)) +
    labs(
      title = title,
      subtitle = subtitle,
      caption = paste0(
        "Bipartite network: organization nodes connect only to emotion nodes. ",
        "Node size = weighted degree; edge width = organization-emotion tie strength. ",
        "Organization labels shown for the upper quartile of weighted degree; all emotion labels shown. ",
        "Layout = Fruchterman–Reingold."
      )
    ) +
    theme_graph(base_family = "sans") +
    theme(
      plot.title = element_text(face = "bold", size = 15),
      plot.subtitle = element_text(size = 10),
      plot.caption = element_text(size = 8, hjust = 0),
      legend.position = "bottom",
      plot.margin = margin(18, 24, 18, 24)
    )

  ggsave(output_png, p, width = 12, height = 9, dpi = 320, bg = "white")
  ggsave(output_pdf, p, width = 12, height = 9, device = cairo_pdf)

  invisible(p)
}

# ------------------------------------------------------------
# 5. Raw graph
# ------------------------------------------------------------

plot_bipartite(
  raw_net,
  title = "Organization–Emotion Network: Raw Affective Strength",
  subtitle = "Edge weight = summed 0–3 emotion intensity across all observed communication items",
  output_png = output_raw_png,
  output_pdf = output_raw_pdf
)

# ------------------------------------------------------------
# 6. Normalized graph
# ------------------------------------------------------------

plot_bipartite(
  norm_net,
  title = "Organization–Emotion Network: Normalized Affective Profile",
  subtitle = "Edge weight = summed emotion intensity divided by each organization’s observed item count",
  output_png = output_norm_png,
  output_pdf = output_norm_pdf
)

# ------------------------------------------------------------
# 7. Console summaries
# ------------------------------------------------------------

cat("\nOrganization-emotion bipartite analysis complete.\n")
cat("Organizations observed:", n_distinct(edges$org_id), "\n")
cat("Emotion nodes:", n_distinct(edges$emotion), "\n")
cat("Observed organization-emotion ties:", nrow(edges), "\n\n")

cat("Top organization nodes by RAW weighted degree:\n")
print(
  raw_metrics %>%
    filter(type == "organization") %>%
    arrange(desc(weighted_degree)) %>%
    select(label, observed_items, weighted_degree, betweenness) %>%
    head(10)
)

cat("\nTop organization nodes by NORMALIZED weighted degree:\n")
print(
  norm_metrics %>%
    filter(type == "organization") %>%
    arrange(desc(weighted_degree)) %>%
    select(label, observed_items, weighted_degree, betweenness) %>%
    head(10)
)
