"""Build the guided analysis notebook."""
from pathlib import Path
import nbformat as nbf

root=Path(__file__).parent
cells=[]
def md(s): cells.append(nbf.v4.new_markdown_cell(s))
def code(s): cells.append(nbf.v4.new_code_cell(s))

md('''# Neurosynth Map Explorer: guided research notebook

**Question:** How much do term-associated maps for emotion regulation and reward overlap, and how sensitive is the answer to analysis choices?

This notebook uses public aggregate neuroimaging maps, **not individual patient data**. It is an exploratory exercise, not a diagnostic tool or a significance test. Run cells in order from the project folder. The full protocol is in `PROTOCOL.md`; exact source URLs and hashes are in `results/provenance.json`.''')
md('''## 1. Load and check the maps

Each NIfTI file holds a three-dimensional statistical map. Matching array shapes alone are insufficient: the affine matrices must also match so voxel indices refer to the same MNI coordinates.''')
code('''from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from analysis import load_map, validate_grid, compare
root = Path.cwd()
a = load_map(root / "data/emotion_regulation.nii.gz", "emotion regulation")
b = load_map(root / "data/reward.nii.gz", "reward")
validate_grid([a, b])
print("Shape:", a.array.shape)
print("Voxel dimensions (mm):", np.linalg.norm(a.affine[:3, :3], axis=0))
print("Matching affine:", np.allclose(a.affine, b.affine))''')
md('''## 2. Calculate overlap across thresholds

For each positive z threshold, mark voxels present in both maps. Jaccard is the number of shared selected voxels divided by the number selected by either map. The thresholds below describe the supplied maps; they do not constitute multiple-comparison correction.''')
code('''rows = compare(a, b, [2, 3, 4, 5])
for row in rows:
    print(f"z >= {row['threshold_z']:.0f}: shared={row['shared_voxels']:,}, "
          f"Jaccard={row['jaccard']:.3f}, Dice={row['dice']:.3f}")
assert rows[1]['shared_voxels'] == 1296''')
code('''fig, ax = plt.subplots(figsize=(6, 3.5))
ax.plot([r['threshold_z'] for r in rows], [r['jaccard'] for r in rows], marker='o')
ax.set(xlabel='Positive z threshold', ylabel='Jaccard',
       title='Emotion regulation x reward: descriptive overlap')
ax.set_xticks([2, 3, 4, 5]); ax.set_ylim(bottom=0)
plt.show()''')
md('''**Interpretation prompt:** The Jaccard value falls with stricter thresholds. Does this alone prove that the two processes have separate neural circuits? Write one alternative explanation before reading the report.''')
md('''## 3. Locate overlap components

We define connected components using six-neighbor connectivity. At z >= 3, only components with at least ten voxels are listed. The peak is selected by maximizing the smaller z value of the two maps at each voxel.''')
code('''from spatial import overlap_clusters
common, clusters = overlap_clusters(a, b, threshold=3, min_voxels=10)
print("Total shared voxels:", int(common.sum()))
for row in clusters[:3]:
    print(row['voxels'], "voxels; peak MNI:",
          (row['peak_mni_x'], row['peak_mni_y'], row['peak_mni_z']))''')
md('''## 4. Read atlas annotations cautiously

The AAL source image was checked against the map geometry. The table contains both peak labels and labels covering each entire component. A peak can lie outside a labeled atlas region even when much of its component lies within one.''')
code('''import csv
with (root / "results/atlas_labels_z3.csv").open(encoding="utf-8") as f:
    atlas_rows = list(csv.DictReader(f))
for row in atlas_rows[:3]:
    print(row['peak_mni'], 'peak:', row['peak_aal_label'],
          '| component:', row['top_aal_labels_counts'])''')
md('''## 5. Audit the shared literature

The maps are not statistically independent when some articles are assigned to both terms. Count shared study identifiers without assuming that specific shared voxels came from those articles.''')
code('''import json
study_sets = json.loads((root / "results/study_id_sets.json").read_text())['study_ids']
shared = set(study_sets['emotion_regulation']) & set(study_sets['reward'])
print(f"Shared studies: {len(shared)} / {len(study_sets['emotion_regulation'])} emotion-regulation studies")
assert len(shared) == 20''')
md('''## 6. Compare another synthesis method

NeuroQuery predicts a spatial map from text. Neurosynth association maps answer a different statistical question. The project compares **ranks** after spatial resampling, without treating their values as interchangeable p values or z scores.''')
code('''with (root / "results/cross_method_sensitivity.csv").open(encoding="utf-8") as f:
    comparison = list(csv.DictReader(f))
for row in comparison:
    if row['top_percent'] == '5':
        print(row['term'], 'Spearman:', row['spearman_rho'],
              'top-5% Jaccard:', row['jaccard'])''')
md('''## 7. State a bounded conclusion

Complete the following sentences in your own words:

1. **Observation:** At z >= 3, the two Neurosynth maps share ___ voxels, with Jaccard ___.
2. **Sensitivity:** When the cutoff changes from z >= 2 to z >= 5, the overlap ___.
3. **Anatomy:** The largest component's peak receives the AAL label ___, but its full extent ___.
4. **Limitation:** The two methods use related literature, so their agreement is ___ rather than fully independent replication.
5. **Next test:** A manually curated study set and a prespecified spatial null model could test ___.

Check your wording against `results/REPORT.md` and `results/RESEARCH_NOTE.pdf`.''')
nb=nbf.v4.new_notebook(cells=cells,metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}})
nbf.write(nb,root/'GUIDED_ANALYSIS.ipynb')
print(root/'GUIDED_ANALYSIS.ipynb')
