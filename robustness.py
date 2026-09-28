"""Track reference overlap components under increasingly strict z cutoffs."""
import csv
from pathlib import Path
import numpy as np
from scipy import ndimage
from analysis import load_map

root = Path(__file__).parent
out = root / 'results'
a = load_map(root/'data/emotion_regulation.nii.gz')
b = load_map(root/'data/reward.nii.gz')
finite = np.isfinite(a.array) & np.isfinite(b.array)
def mask(z): return finite & (a.array >= z) & (b.array >= z)
reference = mask(3)
labels, _ = ndimage.label(reference, structure=ndimage.generate_binary_structure(3, 1))
components = [(i,int((labels==i).sum())) for i in range(1, labels.max()+1)]
components.sort(key=lambda x:x[1],reverse=True)
rows=[]
for rank,(identifier,size) in enumerate(components[:2],1):
    ref = labels == identifier
    for z in [2,3,4,5]:
        surviving = ref & mask(z)
        # z=2 supersets the z=3 component, so this captures reference retention, not growth.
        fraction = surviving.sum()/size
        cc,n = ndimage.label(surviving,structure=ndimage.generate_binary_structure(3,1))
        largest = max((int((cc==i).sum()) for i in range(1,n+1)),default=0)
        rows.append({'z3_component_rank':rank,'z3_voxels':size,'threshold_z':z,
                     'reference_voxels_retained':int(surviving.sum()),
                     'retained_fraction':round(float(fraction),3),
                     'largest_connected_remnant':largest})
with (out/'cluster_stability.csv').open('w',newline='',encoding='utf-8') as f:
    writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
for row in rows: print(row)
