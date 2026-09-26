import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
from pathlib import Path

INPUT = Path('data/processed/full_corpus_coded_master_v1.csv')
OUT = Path('analysis/generated/emotion_network_v1')
OUT.mkdir(parents=True, exist_ok=True)

emotion_cols = {
    'fear_intensity': 'Fear',
    'anxiety_uncertainty_intensity': 'Anxiety / uncertainty',
    'anger_intensity': 'Anger',
    'moral_outrage_intensity': 'Moral outrage',
    'grief_sadness_intensity': 'Grief / sadness',
    'solidarity_intensity': 'Solidarity',
    'care_compassion_intensity': 'Care / compassion',
    'empathy_intensity': 'Empathy',
    'hope_intensity': 'Hope',
    'gratitude_intensity': 'Gratitude',
    'pride_intensity': 'Pride',
    'reassurance_intensity': 'Reassurance',
    'defiance_intensity': 'Defiance',
    'urgency_emotion_intensity': 'Urgency',
}

df = pd.read_csv(INPUT)
for c in emotion_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

presence = (df[list(emotion_cols)] > 0).astype(int)
prevalence = presence.sum().rename(index=emotion_cols)

rows = []
for a, b in combinations(emotion_cols, 2):
    both = (presence[a] == 1) & (presence[b] == 1)
    count = int(both.sum())
    if count:
        rows.append({
            'from': emotion_cols[a],
            'to': emotion_cols[b],
            'cooccurrence_count': count,
            'intensity_product_sum': float((df[a] * df[b]).sum()),
        })

edges = pd.DataFrame(rows).sort_values(['cooccurrence_count','intensity_product_sum'], ascending=False)
edges.to_csv(OUT / 'emotion_cooccurrence_edges_v1.csv', index=False)

G = nx.Graph()
for emotion, count in prevalence.items():
    G.add_node(emotion, prevalence=int(count))
for _, r in edges.iterrows():
    G.add_edge(r['from'], r['to'], weight=int(r['cooccurrence_count']))

strength = dict(G.degree(weight='weight'))
degree = dict(G.degree())
# Convert similarity to distance for path-based centrality.
distance_graph = G.copy()
for u, v, d in distance_graph.edges(data=True):
    d['distance'] = 1.0 / max(d['weight'], 1)
bet = nx.betweenness_centrality(distance_graph, weight='distance', normalized=True)

nodes = pd.DataFrame([
    {'emotion': n, 'item_prevalence': G.nodes[n]['prevalence'], 'degree': degree[n],
     'weighted_degree': strength[n], 'betweenness': bet[n]}
    for n in G.nodes
]).sort_values('weighted_degree', ascending=False)
nodes.to_csv(OUT / 'emotion_network_centrality_v1.csv', index=False)

# Publication-oriented network: show all emotion nodes but suppress weak edges visually.
# Edges below the 35th percentile remain in tables but are not drawn in the main figure.
cutoff = max(1, edges['cooccurrence_count'].quantile(.35))
Gdraw = nx.Graph()
Gdraw.add_nodes_from(G.nodes(data=True))
for u, v, d in G.edges(data=True):
    if d['weight'] >= cutoff:
        Gdraw.add_edge(u, v, **d)

pos = nx.spring_layout(Gdraw, seed=20260926, weight='weight', k=0.95, iterations=800)

fig, ax = plt.subplots(figsize=(13, 10))
weights = [Gdraw[u][v]['weight'] for u, v in Gdraw.edges]
maxw = max(weights) if weights else 1
widths = [0.6 + 5.2*(w/maxw) for w in weights]

nx.draw_networkx_edges(Gdraw, pos, width=widths, alpha=0.30, ax=ax)
node_sizes = [650 + 18*G.nodes[n]['prevalence'] for n in Gdraw.nodes]
nx.draw_networkx_nodes(Gdraw, pos, node_size=node_sizes, linewidths=1.1, edgecolors='black', ax=ax)
nx.draw_networkx_labels(Gdraw, pos, font_size=10, font_weight='bold', ax=ax)

ax.set_title('Emotion Co-occurrence Network', fontsize=18, fontweight='bold', pad=20)
ax.text(.5, 1.01,
        f'Full coded corpus (N={len(df)}). Node size = item prevalence; edge width = within-item co-occurrence.',
        transform=ax.transAxes, ha='center', fontsize=10)
ax.text(.5, -.035,
        'Main figure suppresses the weakest 35% of observed edges for legibility; all observed edges are retained in the edge table.',
        transform=ax.transAxes, ha='center', fontsize=9)
ax.axis('off')
fig.tight_layout()
fig.savefig(OUT / 'emotion_cooccurrence_network_v1.png', dpi=400, bbox_inches='tight')
fig.savefig(OUT / 'emotion_cooccurrence_network_v1.pdf', bbox_inches='tight')
fig.savefig(OUT / 'emotion_cooccurrence_network_v1.svg', bbox_inches='tight')
plt.close(fig)

# Also create a readable ranked prevalence figure to accompany the network.
ranked = nodes.sort_values('item_prevalence', ascending=True)
fig, ax = plt.subplots(figsize=(10, 7.5))
ax.barh(ranked['emotion'], ranked['item_prevalence'])
ax.set_xlabel('Number of coded communication items')
ax.set_title('Emotion Prevalence in the Full Coded Corpus', fontweight='bold')
ax.spines[['top','right']].set_visible(False)
fig.tight_layout()
fig.savefig(OUT / 'emotion_prevalence_v1.png', dpi=400, bbox_inches='tight')
fig.savefig(OUT / 'emotion_prevalence_v1.pdf', bbox_inches='tight')
plt.close(fig)

print('N', len(df))
print(nodes.to_string(index=False))
print('edges', len(edges), 'draw_cutoff', cutoff)
