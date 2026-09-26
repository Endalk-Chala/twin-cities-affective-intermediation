from __future__ import annotations

import glob
import os
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

CORPUS = Path('data/processed/full_corpus_coded_master_v1.csv')
MEDIA_GLOB = 'data/raw/news_media_uptake_batch_*.csv'
CORRECTIONS = Path('data/interim/media_multi_org_split_corrections_v1.csv')
TRANSFORM_AUDIT = Path('data/processed/media_frame_transformation_audit_v1.csv')
OUT = Path('analysis/generated/affective_circulation_network_v1')
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


def clean(x):
    return '' if pd.isna(x) else str(x).strip()


def norm_url(url):
    url = clean(url)
    if not url:
        return ''
    try:
        p = urlsplit(url)
        path = re.sub(r'/+$', '', p.path)
        return urlunsplit((p.scheme.lower(), p.netloc.lower(), path, p.query, ''))
    except Exception:
        return url.rstrip('/')


def story_key(row):
    u = norm_url(row.get('url', ''))
    if u:
        return u
    return '|'.join([clean(row.get('date','')), clean(row.get('outlet','')), clean(row.get('headline',''))])

corpus = pd.read_csv(CORPUS)
for c in emotion_cols:
    corpus[c] = pd.to_numeric(corpus[c], errors='coerce').fillna(0)

org_counts = corpus.groupby(['org_id','organization']).agg(observed_items=('item_id','nunique')).reset_index()

affect_rows = []
for (org_id, org), g in corpus.groupby(['org_id','organization'], dropna=False):
    n = g['item_id'].nunique()
    for col, affect in emotion_cols.items():
        vals = g[col]
        present = vals > 0
        raw_sum = float(vals.sum())
        present_count = int(present.sum())
        if raw_sum > 0:
            affect_rows.append({
                'org_id': clean(org_id), 'organization': clean(org), 'affect': affect,
                'observed_items': int(n), 'affect_item_count': present_count,
                'raw_intensity_sum': raw_sum,
                'normalized_intensity_per_item': raw_sum / n if n else 0,
                'prevalence_share': present_count / n if n else 0,
            })
org_affect = pd.DataFrame(affect_rows)
org_affect.to_csv(OUT / 'organization_affect_edges_all_v1.csv', index=False)

frames = []
for f in sorted(glob.glob(MEDIA_GLOB)):
    d = pd.read_csv(f, dtype=str, keep_default_na=False)
    d['source_batch'] = os.path.basename(f)
    frames.append(d)
media = pd.concat(frames, ignore_index=True, sort=False) if frames else pd.DataFrame()

if not media.empty:
    if 'collection_status' in media.columns:
        status = media['collection_status'].map(clean).str.lower()
        reject = status.str.contains('candidate|unverified|exclude|rejected', regex=True)
        media = media.loc[~reject].copy()
    media['multi_org'] = media.get('org_id', '').map(lambda x: ';' in clean(x))
    media_single = media.loc[~media['multi_org']].copy()
    if CORRECTIONS.exists():
        corr = pd.read_csv(CORRECTIONS, dtype=str, keep_default_na=False)
        corrected_pairs = set(zip(corr['source_batch'], corr['legacy_news_item_id']))
        if 'news_item_id' in media_single.columns:
            mask_corr = media_single.apply(lambda r: (clean(r.get('source_batch','')), clean(r.get('news_item_id',''))) in corrected_pairs, axis=1)
            media_single = media_single.loc[~mask_corr].copy()
        corr2 = pd.DataFrame({
            'source_batch': corr['source_batch'], 'news_item_id': corr['legacy_news_item_id'],
            'date': corr['date'], 'outlet': corr['outlet'], 'headline': corr['headline'],
            'url': corr['url'], 'org_id': corr['org_id'], 'organization': corr['organization'],
            'organization_visibility': corr['organization_visibility'],
            'organization_quoted': corr['organization_quoted'], 'spokesperson': corr['spokesperson'],
            'source_function': corr['source_function'], 'matched_org_item_id': corr['matched_org_item_id'],
            'match_confidence': corr['match_confidence'],
        })
        media_single = pd.concat([media_single, corr2], ignore_index=True, sort=False)
    media_single['story_key'] = media_single.apply(story_key, axis=1)
    media_single['organization'] = media_single.get('organization','').map(clean)
    media_single['org_id'] = media_single.get('org_id','').map(clean)
    media_single['outlet'] = media_single.get('outlet','').map(clean)
    media_single = media_single[(media_single['organization'] != '') & (media_single['outlet'] != '')]
    media_rel = media_single.drop_duplicates(subset=['org_id','organization','outlet','story_key']).copy()
    org_media = (media_rel.groupby(['org_id','organization','outlet'])
                 .agg(verified_relations=('story_key','nunique')).reset_index())
else:
    media_rel = pd.DataFrame(columns=['org_id','organization','outlet','story_key'])
    org_media = pd.DataFrame(columns=['org_id','organization','outlet','verified_relations'])

org_media.to_csv(OUT / 'organization_media_edges_all_v1.csv', index=False)
media_rel.to_csv(OUT / 'media_relations_deduplicated_all_v1.csv', index=False)

if TRANSFORM_AUDIT.exists():
    transform = pd.read_csv(TRANSFORM_AUDIT, dtype=str, keep_default_na=False)
    transform.to_csv(OUT / 'linked_frame_transformation_layer_v1.csv', index=False)
else:
    transform = pd.DataFrame()

G = nx.Graph()
for affect in sorted(set(org_affect['affect'])):
    G.add_node('AFF::'+affect, label=affect, layer='affect', node_type='affect')
for _, r in org_counts.iterrows():
    oid = clean(r['org_id']); org = clean(r['organization'])
    G.add_node('ORG::'+oid, label=org, layer='organization', node_type='organization', observed_items=int(r['observed_items']))
for outlet in sorted(set(org_media['outlet'])):
    G.add_node('MED::'+outlet, label=outlet, layer='media', node_type='media')

for _, r in org_affect.iterrows():
    G.add_edge('AFF::'+r['affect'], 'ORG::'+r['org_id'], edge_type='affect_org',
               raw_weight=float(r['raw_intensity_sum']), normalized_weight=float(r['normalized_intensity_per_item']),
               count=int(r['affect_item_count']))
for _, r in org_media.iterrows():
    G.add_edge('ORG::'+r['org_id'], 'MED::'+r['outlet'], edge_type='org_media',
               raw_weight=float(r['verified_relations']), normalized_weight=float(r['verified_relations']),
               count=int(r['verified_relations']))

nx.write_graphml(G, OUT / 'affective_circulation_network_all_v1.graphml')

affects = sorted([n for n,d in G.nodes(data=True) if d['layer']=='affect'], key=lambda n: G.degree(n, weight='raw_weight'), reverse=True)
org_nodes = sorted([n for n,d in G.nodes(data=True) if d['layer']=='organization'], key=lambda n: G.degree(n, weight='raw_weight'), reverse=True)
media_nodes = sorted([n for n,d in G.nodes(data=True) if d['layer']=='media'], key=lambda n: G.degree(n, weight='raw_weight'), reverse=True)

def layer_pos(nodes, x, span):
    if not nodes: return {}
    ys = np.linspace(span/2, -span/2, len(nodes))
    return {n:(x,float(y)) for n,y in zip(nodes,ys)}

span = max(14, len(org_nodes) * 0.56)
pos = {}
pos.update(layer_pos(affects, -2.5, min(span, 16)))
pos.update(layer_pos(org_nodes, 0.0, span))
pos.update(layer_pos(media_nodes, 2.5, max(span, len(media_nodes)*0.46)))
fig_h = max(12, len(org_nodes)*0.29)

def rescale(vals, low, high):
    if not vals: return {}
    mn, mx = min(vals.values()), max(vals.values())
    if mx == mn: return {k:(low+high)/2 for k in vals}
    return {k: low + (v-mn)/(mx-mn)*(high-low) for k,v in vals.items()}

affect_strength = {n: sum(d['normalized_weight'] for _,_,d in G.edges(n,data=True) if d['edge_type']=='affect_org') for n in affects}
org_aff_strength = {n: sum(d['normalized_weight'] for _,_,d in G.edges(n,data=True) if d['edge_type']=='affect_org') for n in org_nodes}
org_med_strength = {n: sum(d['raw_weight'] for _,_,d in G.edges(n,data=True) if d['edge_type']=='org_media') for n in org_nodes}
media_strength = {n: sum(d['raw_weight'] for _,_,d in G.edges(n,data=True) if d['edge_type']=='org_media') for n in media_nodes}
aff_sizes = rescale(affect_strength, 350, 1050)
org_combined = {n: org_aff_strength.get(n,0) + 0.35*org_med_strength.get(n,0) for n in org_nodes}
org_sizes = rescale(org_combined, 90, 520)
med_sizes = rescale(media_strength, 100, 620)

aff_weights = [d['normalized_weight'] for _,_,d in G.edges(data=True) if d['edge_type']=='affect_org']
med_weights = [d['raw_weight'] for _,_,d in G.edges(data=True) if d['edge_type']=='org_media']
max_aff = max(aff_weights) if aff_weights else 1
max_med = max(med_weights) if med_weights else 1
upper = span/2 + 1.8

def draw_base(ax, presentation=False):
    threshold = org_affect['normalized_intensity_per_item'].quantile(.50) if len(org_affect) else 0
    for u,v,d in G.edges(data=True):
        if d['edge_type']=='affect_org':
            if presentation:
                ax.plot([pos[u][0],pos[v][0]],[pos[u][1],pos[v][1]], linewidth=.25, alpha=.055, zorder=1)
            else:
                w=d['normalized_weight']
                ax.plot([pos[u][0],pos[v][0]],[pos[u][1],pos[v][1]], linewidth=.18+2.0*(w/max_aff), alpha=.10+.18*(w/max_aff), zorder=1)
        else:
            w=d['raw_weight']
            ax.plot([pos[u][0],pos[v][0]],[pos[u][1],pos[v][1]], linewidth=.35+2.8*(w/max_med), alpha=.18+.32*(w/max_med), zorder=1)
    if presentation:
        for u,v,d in G.edges(data=True):
            if d['edge_type']=='affect_org' and d['normalized_weight']>=threshold:
                w=d['normalized_weight']
                ax.plot([pos[u][0],pos[v][0]],[pos[u][1],pos[v][1]], linewidth=.35+2.3*(w/max_aff), alpha=.20+.25*(w/max_aff), zorder=2)
    nx.draw_networkx_nodes(G,pos,nodelist=affects,node_shape='D',node_size=[aff_sizes[n] for n in affects],linewidths=.8,edgecolors='black',ax=ax)
    nx.draw_networkx_nodes(G,pos,nodelist=org_nodes,node_shape='o',node_size=[org_sizes[n] for n in org_nodes],linewidths=.6,edgecolors='black',ax=ax)
    nx.draw_networkx_nodes(G,pos,nodelist=media_nodes,node_shape='s',node_size=[med_sizes[n] for n in media_nodes],linewidths=.7,edgecolors='black',ax=ax)
    for n in affects:
        x,y=pos[n]; ax.text(x-.10,y,G.nodes[n]['label'],ha='right',va='center',fontsize=9,fontweight='bold')
    for n in media_nodes:
        x,y=pos[n]; ax.text(x+.10,y,G.nodes[n]['label'],ha='left',va='center',fontsize=8.5)
    for n in org_nodes:
        x,y=pos[n]
        ax.text(x,y,G.nodes[n]['label'],ha='center',va='center',fontsize=7.4 if org_med_strength.get(n,0)>0 else 6.2,
                fontweight='bold' if org_med_strength.get(n,0)>=4 else 'normal',
                bbox=dict(boxstyle='round,pad=0.12',facecolor='white',edgecolor='none',alpha=.78),zorder=4)
    ax.text(-2.5,upper,'AFFECT',ha='center',fontsize=13,fontweight='bold')
    ax.text(0,upper,'ORGANIZATIONS',ha='center',fontsize=13,fontweight='bold')
    ax.text(2.5,upper,'NEWS MEDIA',ha='center',fontsize=13,fontweight='bold')
    ax.set_xlim(-4.3,4.3); ax.set_ylim(-span/2-1.2,span/2+2.3); ax.axis('off')

fig,ax=plt.subplots(figsize=(18,fig_h)); draw_base(ax,False)
ax.set_title('Affective Circulation Network',fontsize=20,fontweight='bold',pad=18)
ax.text(.5,1.005,f'All coded nonprofit communication (N={len(corpus)}) linked to all verified media-uptake relations in the repository',transform=ax.transAxes,ha='center',fontsize=10)
ax.text(.5,-.012,'Affect–organization edge width uses organization-normalized affect intensity; organization–media edge width uses verified story relations. The linked frame-transformation audit is retained separately.',transform=ax.transAxes,ha='center',fontsize=8.5)
fig.tight_layout(); fig.savefig(OUT/'affective_circulation_network_all_v1.png',dpi=400,bbox_inches='tight'); fig.savefig(OUT/'affective_circulation_network_all_v1.pdf',bbox_inches='tight'); fig.savefig(OUT/'affective_circulation_network_all_v1.svg',bbox_inches='tight'); plt.close(fig)

fig,ax=plt.subplots(figsize=(18,fig_h)); draw_base(ax,True)
ax.set_title('Affective Circulation Network — Presentation View',fontsize=20,fontweight='bold',pad=18)
ax.text(.5,1.005,'All nodes and all media ties retained; weaker affect ties remain visible in the background.',transform=ax.transAxes,ha='center',fontsize=10)
fig.tight_layout(); fig.savefig(OUT/'affective_circulation_network_presentation_v1.png',dpi=400,bbox_inches='tight'); fig.savefig(OUT/'affective_circulation_network_presentation_v1.pdf',bbox_inches='tight'); fig.savefig(OUT/'affective_circulation_network_presentation_v1.svg',bbox_inches='tight'); plt.close(fig)

summary = pd.DataFrame([
    ['coded_communication_items', len(corpus)],
    ['organizations_in_coded_corpus', corpus['org_id'].nunique()],
    ['organization_affect_edges', len(org_affect)],
    ['deduplicated_verified_media_relations', len(media_rel)],
    ['organization_media_edges', len(org_media)],
    ['media_outlets', org_media['outlet'].nunique() if len(org_media) else 0],
    ['affect_nodes', len(affects)],
    ['transformation_audit_rows', len(transform)],
], columns=['metric','value'])
summary.to_csv(OUT/'affective_circulation_summary_v1.csv',index=False)
print(summary.to_string(index=False))
