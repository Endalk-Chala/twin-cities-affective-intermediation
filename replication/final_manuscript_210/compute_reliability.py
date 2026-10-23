#!/usr/bin/env python3
"""Reproduce Krippendorff alpha point estimates on de-textualized coder score matrices.

Usage: python compute_reliability.py [coder1.csv coder2.csv]

Both coder matrices must have matched item_id keys, coding_status, and categorical
coding fields. Only rows coded complete/partial by both coders enter alpha.
The 'present' outputs are derived from nonzero emotion intensity scores.
The script reads historical_agreement_by_variable.csv as a variable schema only,
and does NOT rely on its numerical outputs for the new calculations.
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent

def alpha(data, level):
    data=np.asarray(data,dtype=float)
    cats=np.unique(data[~np.isnan(data)])
    if len(cats)<2: return float('nan')
    ix={v:i for i,v in enumerate(cats)}
    o=np.zeros((len(cats),len(cats)))
    for row in data:
        v=[ix[x] for x in row if not np.isnan(x)]
        if len(v)<2: continue
        for ai in range(len(v)):
            for bi in range(len(v)):
                if ai!=bi: o[v[ai],v[bi]]+=1/(len(v)-1)
    nc=o.sum(axis=1); n=nc.sum()
    if n<=1: return float('nan')
    if level=='nominal': delta=1.0-np.eye(len(cats))
    elif level=='ordinal':
        delta=np.zeros((len(cats),len(cats)))
        for i in range(len(cats)):
            for j in range(len(cats)):
                lo,hi=min(i,j),max(i,j)
                delta[i,j]=(nc[lo:hi+1].sum()-(nc[i]+nc[j])/2.)**2
    else: raise ValueError(level)
    do=(o*delta).sum()/n
    de=(np.outer(nc,nc)*delta).sum()/(n*(n-1))
    return 1-do/de if de>0 else float('nan')

def main():
    paths=sys.argv[1:]
    if not paths:
        paths=[HERE/'Full_Coder_1_de_textualized_214.csv',HERE/'Full_Coder_2_de_textualized_214.csv']
    A=pd.read_csv(paths[0],dtype=str,keep_default_na=False).set_index('item_id')
    B=pd.read_csv(paths[1],dtype=str,keep_default_na=False).set_index('item_id')
    assert len(A)==len(B)==214 and A.index.is_unique and B.index.is_unique
    assert set(A.index)==set(B.index)
    A=A.sort_index();B=B.loc[A.index]
    included=A.coding_status.isin(('complete','partial')) & B.coding_status.isin(('complete','partial'))
    assert included.sum()==210
    print('Matched:',len(A),'codable by both:',int(included.sum()))
    print('Status disagreements:',[(i,a,b) for i,a,b in zip(A.index,A.coding_status,B.coding_status) if a!=b])
    schema=pd.read_csv(HERE/'historical_agreement_by_variable.csv')
    rows=[]
    for _,r in schema.iterrows():
        col=r.variable
        if col.endswith('_present') and col not in A.columns:
            root=col[:-8]+'_intensity'
            if root not in A.columns: raise ValueError(root)
            aa=A.loc[included,root].map(lambda x:'' if x=='' else str(int(float(x)>0)))
            bb=B.loc[included,root].map(lambda x:'' if x=='' else str(int(float(x)>0)))
        else:
            aa=A.loc[included,col];bb=B.loc[included,col]
        aa=aa.tolist();bb=bb.tolist()
        if r.level=='ordinal':
            xa=pd.to_numeric(pd.Series(aa).replace('',np.nan),errors='coerce').values
            xb=pd.to_numeric(pd.Series(bb).replace('',np.nan),errors='coerce').values
        else:
            levels=sorted((set(aa)|set(bb))-{''});mapping={v:i for i,v in enumerate(levels)}
            xa=np.array([mapping.get(v,np.nan) for v in aa],dtype=float)
            xb=np.array([mapping.get(v,np.nan) for v in bb],dtype=float)
        stacked=np.column_stack((xa,xb)); valid=~np.isnan(stacked).any(axis=1)
        point=alpha(stacked,r.level)
        raw=float(np.mean(xa[valid]==xb[valid])) if valid.any() else float('nan')
        rows.append(dict(variable=col,family=r.family,level=r.level,n_valid=int(valid.sum()),alpha=point,raw_agreement=raw,historical_alpha=r.alpha,difference_from_historical=point-r.alpha))
    T=pd.DataFrame(rows)
    T.to_csv(HERE/'recomputed_reliability_summary.csv',index=False)
    emotions=T[(T.family=='emotion_intensity') & ~T.variable.str.contains('other_emotion')]
    apps=T[T.variable.isin(['threat_appraisal','injustice_appraisal','harm_loss_appraisal','opportunity_hope_appraisal','collective_efficacy_appraisal'])]
    functions=T[T.variable.str.startswith('function_')]
    tags=T[T.variable.str.startswith('emotion_source_')]
    for name,s in [('14 emotions',emotions),('5 appraisals',apps),('functions',functions),('attribution tags',tags)]:
        print(name,'n=',len(s),'median alpha=',round(s.alpha.median(),3),'range=',round(s.alpha.min(),3),round(s.alpha.max(),3))
    print('max abs departure from historical 3-decimal estimates:',round(T.difference_from_historical.abs().max(),7))
    assert len(emotions)==14 and abs(emotions.alpha.median()-.864)<.002
    assert (T.difference_from_historical.abs()<.001).all(), 'Historical values not reproduced: review variable coding'
    print('REPRODUCED: all',len(T),'historical point estimates to rounding precision')
if __name__=='__main__':main()
