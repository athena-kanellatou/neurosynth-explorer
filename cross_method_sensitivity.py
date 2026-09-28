"""Rank-cutoff sensitivity for Neurosynth–NeuroQuery spatial agreement."""
import csv
from pathlib import Path
import numpy as np
import nibabel as nib
from scipy.stats import spearmanr
from nilearn.image import resample_to_img
from analysis import load_map

root=Path(__file__).parent
rows=[]
for term in ('emotion_regulation','reward','depression'):
    ns=load_map(root/'data'/f'{term}.nii.gz')
    nq=nib.load(str(root/'neuroquery_maps'/f'{term}.nii.gz'))
    resampled=resample_to_img(nib.Nifti1Image(ns.array,ns.affine),nq,
                              interpolation='continuous',force_resample=True,copy_header=True)
    x,y=resampled.get_fdata(),nq.get_fdata()
    common=np.isfinite(x)&np.isfinite(y)&(x!=0)&(y!=0)
    x,y=x[common],y[common]
    rho=float(spearmanr(x,y).statistic)
    for pct in (1,5,10):
        top_x=x>=np.quantile(x,1-pct/100)
        top_y=y>=np.quantile(y,1-pct/100)
        shared=int(np.count_nonzero(top_x&top_y))
        union=int(np.count_nonzero(top_x|top_y))
        rows.append({'term':term,'top_percent':pct,'common_voxels':len(x),
                     'shared_top_voxels':shared,'jaccard':round(shared/union,4),
                     'spearman_rho':round(rho,4)})
with (root/'results/cross_method_sensitivity.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
for row in rows:print(row)
