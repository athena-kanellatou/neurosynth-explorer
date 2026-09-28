"""Assign descriptive AAL SPM12 labels to overlap components on matching grids."""
import csv
from pathlib import Path
import xml.etree.ElementTree as ET
import nibabel as nib
import numpy as np
from scipy import ndimage
from analysis import load_map
from spatial import overlap_clusters

root = Path(__file__).parent
atlas_root = root / 'atlas_cache' / 'aal' / 'atlas'
image_path, xml_path = atlas_root / 'AAL.nii', atlas_root / 'AAL.xml'
if not image_path.exists() or not xml_path.exists():
    import tarfile
    from urllib.request import urlopen
    import io
    source = 'https://osf.io/s94qg/download'  # Official AAL SPM12 archive linked by Nilearn.
    archive = tarfile.open(fileobj=io.BytesIO(urlopen(source, timeout=45).read()), mode='r:gz')
    atlas_root.mkdir(parents=True, exist_ok=True)
    for member, destination in [('aal/atlas/AAL.nii', image_path), ('aal/atlas/AAL.xml', xml_path)]:
        with archive.extractfile(member) as stream:
            destination.write_bytes(stream.read())
atlas = nib.load(str(image_path))
labels = {int(x.findtext('index')): x.findtext('name') for x in ET.parse(xml_path).findall('.//label')}
a = load_map(root/'data/emotion_regulation.nii.gz')
b = load_map(root/'data/reward.nii.gz')
if atlas.shape != a.array.shape or not np.allclose(atlas.affine, a.affine, atol=1e-4, rtol=0):
    raise ValueError('AAL grid/affine differs; aborting rather than assigning wrong labels')
values = np.asarray(atlas.dataobj)
mask, components = overlap_clusters(a, b, threshold=3, min_voxels=10)
component_ids, _ = ndimage.label(mask, structure=ndimage.generate_binary_structure(3, 1))
rows = []
for rank, component in enumerate(components, 1):
    peak = tuple(component['peak_ijk'])
    atlas_codes = values[component_ids[peak] == component_ids]
    codes, counts = np.unique(atlas_codes, return_counts=True)
    order = np.argsort(counts)[::-1]
    top = [(labels.get(int(codes[i]), 'outside AAL' if codes[i] == 0 else 'unknown'), int(counts[i])) for i in order[:3]]
    rows.append({'rank':rank, 'voxels':component['voxels'],
                 'peak_mni':f"({component['peak_mni_x']}, {component['peak_mni_y']}, {component['peak_mni_z']})",
                 'peak_aal_label':labels.get(int(values[peak]), 'outside AAL'),
                 'top_aal_labels_counts':'; '.join(f'{name}: {n}' for name,n in top)})
with (root/'results/atlas_labels_z3.csv').open('w', newline='', encoding='utf-8') as f:
    writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
print('AAL SPM12 atlas labels; first five components:')
for row in rows[:5]: print(row)
