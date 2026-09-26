# Emotion co-occurrence network analysis
# Twin Cities Affective Intermediation project
# Reads the frozen/validated coded master corpus and produces:
#   1) weighted emotion co-occurrence edge list
#   2) node-level prominence/centrality table
#   3) publication-ready R network graph
#
# Required packages:
# install.packages(c("tidyverse", "igraph", "tidygraph", "ggraph", "ggrepel"))

library(tidyverse)
library(igraph)
library(tidygraph)
library(ggraph)
library(ggrepel)

input_file <- "data/processed/full_corpus_coded_master_v1.csv"
output_edge_file <- "analysis/tables/emotion_cooccurrence_edges_v1.csv"
output_node_file <- "analysis/tables/emotion_network_centrality_v1.csv"
output_figure_png <- "analysis/figures/emotion_cooccurrence_network_v1.png"
output_figure_pdf <- "analysis/figures/emotion_cooccurrence_network_v1.pdf"

dir.create("analysis/tables", recursive = TRUE, showWarnings = FALSE)
dir.create("analysis/figures", recursive = TRUE, showWarnings = FALSE)

# ------------------------------------------------------------
# 1. Load corpus
# ------------------------------------------------------------

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

missing_cols <- setdiff(emotion_cols, names(dat))
if (length(missing_cols) > 0) {
  stop("Missing required emotion columns: ", paste(missing_cols, collapse = ", "))
}

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

# Treat any intensity > 0 as presence for the main co-occurrence network.
# Preserve intensity values separately for weighted robustness analysis.
presence <- dat %>%
  select(item_id, all_of(emotion_cols)) %>%
  mutate(across(all_of(emotion_cols), ~ replace_na(as.numeric(.x), 0))) %>%
  mutate(across(all_of(emotion_cols), ~ as.integer(.x > 0)))

intensity <- dat %>%
  select(item_id, all_of(emotion_cols)) %>%
  mutate(across(all_of(emotion_cols), ~ replace_na(as.numeric(.x), 0)))

# ------------------------------------------------------------
# 2. Build undirected weighted emotion co-occurrence edges
# ------------------------------------------------------------

pairs <- combn(emotion_cols, 2, simplify = FALSE)

edges <- purrr::map_dfr(pairs, function(pair) {
  a <- pair[[1]]
  b <- pair[[2]]

  present_both <- presence[[a]] == 1 & presence[[b]] == 1

  tibble(
    from = unname(emotion_labels[a]),
    to = unname(emotion_labels[b]),
    cooccurrence_count = sum(present_both, na.rm = TRUE),
    intensity_product_sum = sum(intensity[[a]] * intensity[[b]], na.rm = TRUE),
    mean_joint_intensity = ifelse(
      sum(present_both, na.rm = TRUE) > 0,
      mean((intensity[[a]] + intensity[[b]]) / 2, na.rm = TRUE, subset = present_both),
      0
    )
  )
}) %>%
  filter(cooccurrence_count > 0) %>%
  arrange(desc(cooccurrence_count), desc(intensity_product_sum))

# Base figure uses co-occurrence count as the edge weight.
# intensity_product_sum is retained for robustness/sensitivity analysis.
readr::write_csv(edges, output_edge_file)

# ------------------------------------------------------------
# 3. Construct graph and calculate prominence
# ------------------------------------------------------------

g <- graph_from_data_frame(
  d = edges %>% select(from, to, cooccurrence_count, intensity_product_sum),
  directed = FALSE
)

E(g)$weight <- E(g)$cooccurrence_count

# Similarity weights are converted to distances for shortest-path measures.
E(g)$distance <- 1 / E(g)$weight

# Node prevalence in the underlying corpus.
node_prevalence <- tibble(
  emotion = unname(emotion_labels),
  item_prevalence = purrr::map_int(emotion_cols, ~ sum(presence[[.x]] == 1, na.rm = TRUE)),
  intensity_sum = purrr::map_dbl(emotion_cols, ~ sum(intensity[[.x]], na.rm = TRUE))
)

# Weighted degree/strength and centralities.
centrality <- tibble(
  emotion = V(g)$name,
  degree = degree(g, mode = "all"),
  weighted_degree = strength(g, mode = "all", weights = E(g)$weight),
  betweenness = betweenness(g, directed = FALSE, weights = E(g)$distance, normalized = TRUE),
  closeness = closeness(g, weights = E(g)$distance, normalized = TRUE),
  eigenvector = eigen_centrality(g, directed = FALSE, weights = E(g)$weight, scale = TRUE)$vector
)

# Community detection is exploratory and descriptive. It does not define theory a priori.
set.seed(20260926)
community_fit <- cluster_louvain(g, weights = E(g)$weight)
community_tbl <- tibble(
  emotion = names(membership(community_fit)),
  community = as.integer(membership(community_fit))
)

nodes <- centrality %>%
  left_join(node_prevalence, by = "emotion") %>%
  left_join(community_tbl, by = "emotion") %>%
  arrange(desc(weighted_degree))

readr::write_csv(nodes, output_node_file)

# ------------------------------------------------------------
# 4. Publication-ready node-and-edge graph
# ------------------------------------------------------------

network_tbl <- as_tbl_graph(g) %>%
  activate(nodes) %>%
  left_join(nodes, by = c("name" = "emotion")) %>%
  activate(edges) %>%
  mutate(
    edge_weight = cooccurrence_count,
    edge_alpha = scales::rescale(cooccurrence_count, to = c(0.20, 0.85))
  )

set.seed(20260926)

p <- ggraph(network_tbl, layout = "fr", weights = edge_weight) +
  geom_edge_link(
    aes(width = edge_weight, alpha = edge_alpha),
    show.legend = FALSE,
    lineend = "round"
  ) +
  geom_node_point(
    aes(size = weighted_degree, shape = factor(community)),
    stroke = 0.4
  ) +
  geom_node_text(
    aes(label = name),
    repel = TRUE,
    size = 3.8,
    max.overlaps = Inf
  ) +
  scale_edge_width(range = c(0.25, 3.2)) +
  scale_size_continuous(range = c(4.5, 12)) +
  guides(shape = "none", size = "none") +
  labs(
    title = "Emotion Co-occurrence Network in Twin Cities Nonprofit Communication",
    subtitle = "Edges represent emotions appearing together within the same coded communication item",
    caption = paste0(
      "Study period: Nov. 1, 2025–Mar. 31, 2026. ",
      "Node size = weighted degree; edge width = co-occurrence count. ",
      "Layout = Fruchterman–Reingold. Community shapes are descriptive Louvain clusters."
    )
  ) +
  theme_graph(base_family = "sans") +
  theme(
    plot.title = element_text(face = "bold", size = 15),
    plot.subtitle = element_text(size = 10),
    plot.caption = element_text(size = 8, hjust = 0),
    plot.margin = margin(18, 24, 18, 24)
  )

ggsave(output_figure_png, p, width = 11, height = 8.5, dpi = 320, bg = "white")
ggsave(output_figure_pdf, p, width = 11, height = 8.5, device = cairo_pdf)

# ------------------------------------------------------------
# 5. Console summary
# ------------------------------------------------------------

cat("\nEmotion network complete.\n")
cat("Items in corpus:", nrow(dat), "\n")
cat("Emotion nodes:", vcount(g), "\n")
cat("Observed co-occurrence edges:", ecount(g), "\n\n")
cat("Top emotions by weighted degree:\n")
print(nodes %>% select(emotion, item_prevalence, weighted_degree, betweenness, community) %>% head(10))
