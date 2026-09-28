"""Descriptive spatial agreement between Neurosynth and NeuroQuery term maps."""
import csv
from pathlib import Path
import numpy as np
import nibabel as nib
from scipy.stats import spearmanr
from nilearn.image import resample_to_img
from analysis import load_map

root=Path(__file__).parent
out=root/'results'
rows=[]
for term in ('emotion_regulation','reward','depression'):
    ns=load_map(root/'data'/f'{term}.nii.gz')
    nq=nib.load(str(root/'neuroquery_maps'/f'{term}.nii.gz'))
    # Resample the 2 mm source once to NeuroQuery's 4 mm grid for descriptive comparison.
    ns_on_nq=resample_to_img(nib.Nifti1Image(ns.array,ns.affine),nq,interpolation='continuous',force_resample=True,copy_header=True)
    x=ns_on_nq.get_fdata(); y=nq.get_fdata()
    common=np.isfinite(x)&np.isfinite(y)&(x!=0)&(y!=0)
    vx,vy=x[common],y[common]
    if len(vx)<1000: raise ValueError('Insufficient common brain voxels')
    cut_x,cut_y=np.quantile(vx,.95),np.quantile(vy,.95)
    top_x,top_y=vx>=cut_x,vy>=cut_y
    shared=int((top_x&top_y).sum())
    denom=int((top_x|top_y).sum())
    rows.append({'term':term,'common_nonzero_voxels':len(vx),
                 'spearman_rho':round(float(spearmanr(vx,vy).statistic),4),
                 'top_5pct_shared_voxels':shared,
                 'top_5pct_jaccard':round(shared/denom,4),
                 'ns_cutoff':round(float(cut_x),3),'nq_cutoff':round(float(cut_y),3)})
with (out/'cross_method.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
for row in rows:print(row)
