import glob, os, re, shutil
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

CORPUS=Path('data/processed/full_corpus_coded_master_v1.csv')
CORR=Path('data/interim/media_multi_org_split_corrections_v1.csv')
TRANS=Path('data/processed/media_frame_transformation_audit_v1.csv')
OUT=Path('analysis/generated/affective_circulation_network_v1'); OUT.mkdir(parents=True,exist_ok=True)
AFFECT={
'fear_intensity':'Fear','anxiety_uncertainty_intensity':'Anxiety / uncertainty','anger_intensity':'Anger',
'moral_outrage_intensity':'Moral outrage','grief_sadness_intensity':'Grief / sadness','solidarity_intensity':'Solidarity',
'care_compassion_intensity':'Care / compassion','empathy_intensity':'Empathy','hope_intensity':'Hope',
'gratitude_intensity':'Gratitude','pride_intensity':'Pride','reassurance_intensity':'Reassurance',
'defiance_intensity':'Defiance','urgency_emotion_intensity':'Urgency'}

def s(x): return '' if pd.isna(x) else str(x).strip()
def canon_url(x):
    x=s(x)
    if not x:return ''
    try:
        p=urlsplit(x); return urlunsplit((p.scheme.lower(),p.netloc.lower(),re.sub(r'/+$','',p.path),p.query,''))
    except:return x.rstrip('/')
def skey(r): return canon_url(r.get('url','')) or '|'.join([s(r.get('date','')),s(r.get('outlet','')),s(r.get('headline',''))])

# Full coded corpus -> organization-affect edges
c=pd.read_csv(CORPUS)
for col in AFFECT:c[col]=pd.to_numeric(c[col],errors='coerce').fillna(0)
org_counts=c.groupby(['org_id','organization']).agg(observed_items=('item_id','nunique')).reset_index()
rows=[]
for (oid,org),g in c.groupby(['org_id','organization']):
    n=g['item_id'].nunique()
    for col,label in AFFECT.items():
        vals=g[col]; total=float(vals.sum()); cnt=int((vals>0).sum())
        if total>0: rows.append([s(oid),s(org),label,n,cnt,total,total/n,cnt/n])
oa=pd.DataFrame(rows,columns=['org_id','organization','affect','observed_items','affect_item_count','raw_intensity_sum','normalized_intensity_per_item','prevalence_share'])
oa.to_csv(OUT/'organization_affect_edges_all_v1.csv',index=False)

# All existing media uptake batches -> deduplicated organization-story relations
parts=[]
for f in sorted(glob.glob('data/raw/news_media_uptake_batch_*.csv')):
    d=pd.read_csv(f,dtype=str,keep_default_na=False); d['source_batch']=os.path.basename(f); parts.append(d)
m=pd.concat(parts,ignore_index=True,sort=False) if parts else pd.DataFrame()
if len(m):
    if 'collection_status' in m:
        st=m['collection_status'].map(s).str.lower(); m=m.loc[~st.str.contains('candidate|unverified|exclude|rejected',regex=True)].copy()
    # unresolved bundled multi-org relations are replaced only where explicit corrections exist
    multi=m['org_id'].map(lambda x:';' in s(x)) if 'org_id' in m else pd.Series(False,index=m.index)
    single=m.loc[~multi].copy()
    if CORR.exists():
        q=pd.read_csv(CORR,dtype=str,keep_default_na=False)
        pairs=set(zip(q['source_batch'],q['legacy_news_item_id']))
        if 'news_item_id' in single:
            drop=single.apply(lambda r:(s(r.get('source_batch','')),s(r.get('news_item_id',''))) in pairs,axis=1); single=single.loc[~drop]
        q2=pd.DataFrame({
          'source_batch':q['source_batch'],'news_item_id':q['legacy_news_item_id'],'date':q['date'],'outlet':q['outlet'],
          'headline':q['headline'],'url':q['url'],'org_id':q['org_id'],'organization':q['organization'],
          'organization_visibility':q['organization_visibility'],'organization_quoted':q['organization_quoted'],
          'spokesperson':q['spokesperson'],'source_function':q['source_function'],'matched_org_item_id':q['matched_org_item_id'],
          'match_confidence':q['match_confidence']})
        single=pd.concat([single,q2],ignore_index=True,sort=False)
    single['story_key']=single.apply(skey,axis=1)
    for col in ['org_id','organization','outlet']: single[col]=single[col].map(s)
    single=single[(single.organization!='')&(single.outlet!='')]
    mr=single.drop_duplicates(['org_id','organization','outlet','story_key']).copy()
    om=mr.groupby(['org_id','organization','outlet']).agg(verified_relations=('story_key','nunique')).reset_index()
else:
    mr=pd.DataFrame(columns=['org_id','organization','outlet','story_key']); om=pd.DataFrame(columns=['org_id','organization','outlet','verified_relations'])
mr.to_csv(OUT/'media_relations_deduplicated_all_v1.csv',index=False); om.to_csv(OUT/'organization_media_edges_all_v1.csv',index=False)

# Preserve transformation audit exactly as a linked layer; it is not required for graph construction.
trans_rows=0
if TRANS.exists():
    shutil.copyfile(TRANS,OUT/'linked_frame_transformation_layer_v1.csv')
    with open(TRANS,encoding='utf-8',errors='replace') as fh: trans_rows=max(0,sum(1 for _ in fh)-1)

# Three-layer graph
G=nx.Graph()
for a in sorted(oa.affect.unique()):G.add_node('A::'+a,label=a,layer='affect')
for _,r in org_counts.iterrows():G.add_node('O::'+s(r.org_id),label=s(r.organization),layer='organization',observed_items=int(r.observed_items))
for x in sorted(om.outlet.unique()):G.add_node('M::'+x,label=x,layer='media')
for _,r in oa.iterrows():G.add_edge('A::'+r.affect,'O::'+r.org_id,edge_type='affect_org',raw_weight=float(r.raw_intensity_sum),normalized_weight=float(r.normalized_intensity_per_item),count=int(r.affect_item_count))
for _,r in om.iterrows():G.add_edge('O::'+r.org_id,'M::'+r.outlet,edge_type='org_media',raw_weight=float(r.verified_relations),normalized_weight=float(r.verified_relations),count=int(r.verified_relations))
nx.write_graphml(G,OUT/'affective_circulation_network_all_v1.graphml')

# Layout
an=sorted([n for n,d in G.nodes(data=True) if d['layer']=='affect'],key=lambda n:G.degree(n,weight='raw_weight'),reverse=True)
on=sorted([n for n,d in G.nodes(data=True) if d['layer']=='organization'],key=lambda n:G.degree(n,weight='raw_weight'),reverse=True)
mn=sorted([n for n,d in G.nodes(data=True) if d['layer']=='media'],key=lambda n:G.degree(n,weight='raw_weight'),reverse=True)
span=max(14,len(on)*.56)
def lay(nodes,x,sp):
    ys=np.linspace(sp/2,-sp/2,len(nodes)) if nodes else []
    return {n:(x,float(y)) for n,y in zip(nodes,ys)}
pos={**lay(an,-2.5,min(span,16)),**lay(on,0,span),**lay(mn,2.5,max(span,len(mn)*.46))}

def strength(nodes,etype,key):return {n:sum(d[key] for _,_,d in G.edges(n,data=True) if d['edge_type']==etype) for n in nodes}
astr=strength(an,'affect_org','normalized_weight'); ostr=strength(on,'affect_org','normalized_weight'); omstr=strength(on,'org_media','raw_weight'); mstr=strength(mn,'org_media','raw_weight')
def scale(v,lo,hi):
    if not v:return {}
    a,b=min(v.values()),max(v.values()); return {k:(lo+hi)/2 if a==b else lo+(x-a)/(b-a)*(hi-lo) for k,x in v.items()}
asz=scale(astr,350,1050); osz=scale({n:ostr.get(n,0)+.35*omstr.get(n,0) for n in on},90,520); msz=scale(mstr,100,620)
ma=max([d['normalized_weight'] for _,_,d in G.edges(data=True) if d['edge_type']=='affect_org'] or [1]); mm=max([d['raw_weight'] for _,_,d in G.edges(data=True) if d['edge_type']=='org_media'] or [1]); upper=span/2+1.8

def draw(presentation=False):
    fig,ax=plt.subplots(figsize=(18,max(12,len(on)*.29)))
    cut=oa.normalized_intensity_per_item.quantile(.5)
    for u,v,d in G.edges(data=True):
        if d['edge_type']=='affect_org':
            w=d['normalized_weight']; lw=.25 if presentation else .18+2*(w/ma); al=.055 if presentation else .10+.18*(w/ma)
        else:
            w=d['raw_weight']; lw=.35+2.8*(w/mm); al=.18+.32*(w/mm)
        ax.plot([pos[u][0],pos[v][0]],[pos[u][1],pos[v][1]],linewidth=lw,alpha=al,zorder=1)
    if presentation:
        for u,v,d in G.edges(data=True):
            if d['edge_type']=='affect_org' and d['normalized_weight']>=cut:
                w=d['normalized_weight']; ax.plot([pos[u][0],pos[v][0]],[pos[u][1],pos[v][1]],linewidth=.35+2.3*(w/ma),alpha=.20+.25*(w/ma),zorder=2)
    nx.draw_networkx_nodes(G,pos,nodelist=an,node_shape='D',node_size=[asz[n] for n in an],linewidths=.8,edgecolors='black',ax=ax)
    nx.draw_networkx_nodes(G,pos,nodelist=on,node_shape='o',node_size=[osz[n] for n in on],linewidths=.6,edgecolors='black',ax=ax)
    nx.draw_networkx_nodes(G,pos,nodelist=mn,node_shape='s',node_size=[msz[n] for n in mn],linewidths=.7,edgecolors='black',ax=ax)
    for n in an:
        x,y=pos[n];ax.text(x-.10,y,G.nodes[n]['label'],ha='right',va='center',fontsize=9,fontweight='bold')
    for n in mn:
        x,y=pos[n];ax.text(x+.10,y,G.nodes[n]['label'],ha='left',va='center',fontsize=8.5)
    for n in on:
        x,y=pos[n];ax.text(x,y,G.nodes[n]['label'],ha='center',va='center',fontsize=7.4 if omstr.get(n,0)>0 else 6.2,fontweight='bold' if omstr.get(n,0)>=4 else 'normal',bbox=dict(boxstyle='round,pad=.12',facecolor='white',edgecolor='none',alpha=.78),zorder=4)
    ax.text(-2.5,upper,'AFFECT',ha='center',fontsize=13,fontweight='bold');ax.text(0,upper,'ORGANIZATIONS',ha='center',fontsize=13,fontweight='bold');ax.text(2.5,upper,'NEWS MEDIA',ha='center',fontsize=13,fontweight='bold')
    ax.set_xlim(-4.3,4.3);ax.set_ylim(-span/2-1.2,span/2+2.3);ax.axis('off')
    title='Affective Circulation Network — Presentation View' if presentation else 'Affective Circulation Network';ax.set_title(title,fontsize=20,fontweight='bold',pad=18)
    if presentation:ax.text(.5,1.005,'All nodes and all media ties retained; weaker affect ties remain visible in the background.',transform=ax.transAxes,ha='center',fontsize=10)
    else:
        ax.text(.5,1.005,f'All coded nonprofit communication (N={len(c)}) linked to all verified media-uptake relations in the repository',transform=ax.transAxes,ha='center',fontsize=10)
        ax.text(.5,-.012,'Affect–organization edge width uses organization-normalized affect intensity; organization–media edge width uses verified story relations. Frame transformation remains a separate linked layer.',transform=ax.transAxes,ha='center',fontsize=8.5)
    fig.tight_layout(); stem='affective_circulation_network_presentation_v1' if presentation else 'affective_circulation_network_all_v1'
    fig.savefig(OUT/(stem+'.png'),dpi=400,bbox_inches='tight');fig.savefig(OUT/(stem+'.pdf'),bbox_inches='tight');fig.savefig(OUT/(stem+'.svg'),bbox_inches='tight');plt.close(fig)
draw(False);draw(True)

summary=pd.DataFrame([
['coded_communication_items',len(c)],['organizations_in_coded_corpus',c.org_id.nunique()],['organization_affect_edges',len(oa)],
['deduplicated_verified_media_relations',len(mr)],['organization_media_edges',len(om)],['media_outlets',om.outlet.nunique() if len(om) else 0],
['affect_nodes',len(an)],['transformation_audit_physical_rows',trans_rows]],columns=['metric','value'])
summary.to_csv(OUT/'affective_circulation_summary_v1.csv',index=False);print(summary.to_string(index=False))
