suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(tibble)
  library(igraph)
  library(tidygraph)
  library(ggraph)
  library(graphlayouts)
  library(ggplot2)
  library(scales)
})

set.seed(20260926)

BASE <- "analysis/generated/affective_circulation_network_v1"
OUT  <- file.path(BASE, "r_force_directed")
dir.create(OUT, recursive = TRUE, showWarnings = FALSE)

aff <- read_csv(file.path(BASE, "organization_affect_edges_all_v1.csv"), show_col_types = FALSE)
med <- read_csv(file.path(BASE, "organization_media_edges_all_v1.csv"), show_col_types = FALSE)

# -----------------------------------------------------------------------------
# Nodes
# -----------------------------------------------------------------------------
affect_nodes <- aff %>%
  distinct(affect) %>%
  transmute(name = paste0("AFF::", affect), label = affect, node_type = "Affect")

org_nodes <- bind_rows(
  aff %>% distinct(org_id, organization),
  med %>% distinct(org_id, organization)
) %>%
  distinct(org_id, .keep_all = TRUE) %>%
  transmute(name = paste0("ORG::", org_id), label = organization, node_type = "Organization")

media_nodes <- med %>%
  distinct(outlet) %>%
  transmute(name = paste0("MED::", outlet), label = outlet, node_type = "Media")

nodes <- bind_rows(affect_nodes, org_nodes, media_nodes)

# -----------------------------------------------------------------------------
# Edges
# Affect edges use organization-normalized intensity so high-volume orgs do not
# dominate solely because they published more often. Media edges use verified
# unique story relations.
# -----------------------------------------------------------------------------
affect_edges <- aff %>%
  transmute(
    from = paste0("AFF::", affect),
    to = paste0("ORG::", org_id),
    edge_type = "Affect–organization",
    raw_weight = raw_intensity_sum,
    weight = normalized_intensity_per_item,
    count = affect_item_count
  )

media_edges <- med %>%
  transmute(
    from = paste0("ORG::", org_id),
    to = paste0("MED::", outlet),
    edge_type = "Organization–media",
    raw_weight = verified_relations,
    weight = verified_relations,
    count = verified_relations
  )

edges <- bind_rows(affect_edges, media_edges)

# Build graph and compute prominence measures.
g <- tbl_graph(nodes = nodes, edges = edges, directed = FALSE) %>%
  activate(nodes) %>%
  mutate(
    degree = centrality_degree(),
    strength = centrality_degree(weights = .E()$weight),
    label_priority = case_when(
      node_type == "Affect" ~ 3L,
      node_type == "Media" ~ 2L,
      strength >= quantile(strength[node_type == "Organization"], .70, na.rm = TRUE) ~ 2L,
      TRUE ~ 1L
    )
  )

# Stress layout generally produces a cleaner organic configuration than default
# FR for this mixed weighted network.
ig <- as.igraph(g)
lay <- graphlayouts::layout_with_stress(ig, weights = 1 / pmax(E(ig)$weight, 0.001))
layout_df <- as_tibble(g, active = "nodes") %>%
  mutate(x = lay[,1], y = lay[,2])
write_csv(layout_df, file.path(OUT, "affective_circulation_r_layout_nodes_v1.csv"))
write_csv(edges, file.path(OUT, "affective_circulation_r_edges_v1.csv"))

# Node scales are type-specific to prevent organizations overwhelming affect/media.
node_sizes <- layout_df %>%
  group_by(node_type) %>%
  mutate(
    size_scaled = case_when(
      node_type == "Affect" ~ rescale(strength, to = c(6.5, 12)),
      node_type == "Media" ~ rescale(strength, to = c(4.5, 9.5)),
      TRUE ~ rescale(strength, to = c(2.4, 7.2))
    )
  ) %>% ungroup()

# Rebuild graph with final size/label fields.
g2 <- tbl_graph(nodes = node_sizes, edges = edges, directed = FALSE)

# Edge width is scaled within edge type, not globally, because the two weights
# are on substantively different scales.
edge_df <- as_tibble(g2, active = "edges") %>%
  group_by(edge_type) %>%
  mutate(edge_width = rescale(weight, to = ifelse(first(edge_type)=="Affect–organization", c(.15, 2.2), c(.3, 3.2)))) %>%
  ungroup()

g2 <- tbl_graph(nodes = as_tibble(g2, active = "nodes"), edges = edge_df, directed = FALSE)

# Label organizations selectively for readability, while keeping every node and
# every edge in the figure. Full labels remain in the exported node table.
label_data <- node_sizes %>%
  mutate(plot_label = case_when(
    node_type == "Affect" ~ label,
    node_type == "Media" ~ label,
    label_priority >= 2 ~ label,
    TRUE ~ ""
  ))

g2 <- tbl_graph(nodes = label_data, edges = edge_df, directed = FALSE)

p <- ggraph(g2, layout = "manual", x = x, y = y) +
  geom_edge_link(aes(width = edge_width, alpha = edge_type, linetype = edge_type),
                 lineend = "round", show.legend = TRUE) +
  scale_edge_width_identity() +
  scale_edge_alpha_manual(values = c("Affect–organization" = .16,
                                     "Organization–media" = .38)) +
  scale_edge_linetype_manual(values = c("Affect–organization" = "solid",
                                        "Organization–media" = "solid")) +
  geom_node_point(aes(size = size_scaled, shape = node_type), stroke = .5) +
  scale_size_identity() +
  scale_shape_manual(values = c("Affect" = 23, "Organization" = 21, "Media" = 22)) +
  geom_node_text(aes(label = plot_label, fontface = ifelse(node_type == "Affect", "bold", "plain")),
                 repel = TRUE, box.padding = .35, point.padding = .18,
                 max.overlaps = Inf, size = 3.15, lineheight = .9) +
  labs(
    title = "Affective Circulation Network",
    subtitle = "Organic force-directed rendering of affect, nonprofit organizations, and verified news-media uptake",
    caption = paste0(
      "All affect–organization and organization–media ties are retained. ",
      "Affect edges use organization-normalized affect intensity; media edges use verified unique story relations. ",
      "Frame transformation remains a separate linked layer."
    ),
    shape = NULL,
    edge_alpha = "Relation",
    edge_linetype = "Relation"
  ) +
  theme_graph(base_family = "sans") +
  theme(
    plot.title = element_text(face = "bold", size = 18, hjust = .5),
    plot.subtitle = element_text(size = 10.5, hjust = .5),
    plot.caption = element_text(size = 8.5, hjust = 0),
    legend.position = "bottom",
    legend.box = "vertical",
    plot.margin = margin(18, 18, 18, 18)
  )

ggsave(file.path(OUT, "affective_circulation_network_r_force_v1.png"), p,
       width = 15, height = 12, dpi = 500, bg = "white")
ggsave(file.path(OUT, "affective_circulation_network_r_force_v1.pdf"), p,
       width = 15, height = 12, device = cairo_pdf, bg = "white")
ggsave(file.path(OUT, "affective_circulation_network_r_force_v1.svg"), p,
       width = 15, height = 12, bg = "white")

# A publication view that keeps all nodes/edges but further mutes low-strength
# affect ties. Nothing is removed from the analytical edge table.
aff_cut <- median(affect_edges$weight, na.rm = TRUE)
edge_df2 <- edge_df %>%
  mutate(display_alpha = case_when(
    edge_type == "Organization–media" ~ .42,
    edge_type == "Affect–organization" & weight >= aff_cut ~ .22,
    TRUE ~ .055
  ))
g3 <- tbl_graph(nodes = label_data, edges = edge_df2, directed = FALSE)

p2 <- ggraph(g3, layout = "manual", x = x, y = y) +
  geom_edge_link(aes(width = edge_width, alpha = display_alpha),
                 lineend = "round", show.legend = FALSE) +
  scale_edge_width_identity() +
  scale_edge_alpha_identity() +
  geom_node_point(aes(size = size_scaled, shape = node_type), stroke = .5) +
  scale_size_identity() +
  scale_shape_manual(values = c("Affect" = 23, "Organization" = 21, "Media" = 22)) +
  geom_node_text(aes(label = plot_label, fontface = ifelse(node_type == "Affect", "bold", "plain")),
                 repel = TRUE, box.padding = .35, point.padding = .18,
                 max.overlaps = Inf, size = 3.15, lineheight = .9) +
  labs(
    title = "Affective Circulation Network",
    subtitle = "Publication view: all nodes and media ties retained; weaker affect ties visually muted",
    caption = "Organic stress layout. The complete edge tables and GraphML preserve every observed relation.",
    shape = NULL
  ) +
  theme_graph(base_family = "sans") +
  theme(
    plot.title = element_text(face = "bold", size = 18, hjust = .5),
    plot.subtitle = element_text(size = 10.5, hjust = .5),
    plot.caption = element_text(size = 8.5, hjust = 0),
    legend.position = "bottom",
    plot.margin = margin(18,18,18,18)
  )

ggsave(file.path(OUT, "affective_circulation_network_r_force_publication_v1.png"), p2,
       width = 15, height = 12, dpi = 500, bg = "white")
ggsave(file.path(OUT, "affective_circulation_network_r_force_publication_v1.pdf"), p2,
       width = 15, height = 12, device = cairo_pdf, bg = "white")
ggsave(file.path(OUT, "affective_circulation_network_r_force_publication_v1.svg"), p2,
       width = 15, height = 12, bg = "white")

message("R force-directed affective circulation network rendered successfully.")
