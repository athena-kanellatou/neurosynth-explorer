"""Reproduce the three-term descriptive analysis and a figure."""
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from analysis import load_map, compare

root = Path(__file__).parent
out = root / 'results'
out.mkdir(exist_ok=True)
terms = ['emotion_regulation', 'reward', 'depression']
maps = {name: load_map(root / 'data' / f'{name}.nii.gz', name) for name in terms}
urls = {
    'emotion_regulation': 'https://neurosynth.org/api/analyses/498/images/association?unthresholded',
    'reward': 'https://neurosynth.org/api/analyses/46/images/association?unthresholded',
    'depression': 'https://neurosynth.org/api/analyses/772/images/association?unthresholded',
}
counts = {'emotion_regulation': 247, 'reward': 922, 'depression': 502}
rows = []
for a, b in [('emotion_regulation', 'reward'), ('emotion_regulation', 'depression'), ('reward', 'depression')]:
    for row in compare(maps[a], maps[b], [2, 3, 4, 5]):
        rows.append({'term_a': a, 'term_b': b, **row})
with (out / 'overlap.csv').open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader(); writer.writerows(rows)
metadata = {
    'retrieved_utc': '2026-09-28',
    'analysis_utc': datetime.now(timezone.utc).isoformat(),
    'source': 'Neurosynth association-test z maps via ?unthresholded endpoint',
    'inputs': {name: {'url': urls[name], 'sha256': maps[name].sha256,
                      'shape': maps[name].array.shape, 'affine': maps[name].affine.tolist(),
                      'studies_on_term_page': counts[name]} for name in terms},
    'thresholds': [2, 3, 4, 5],
    'mask': 'pairwise finite voxels, positive z only',
    'resampling': 'none',
    'caveat': 'Descriptive overlap; z cutoff is not a claim of corrected inference.'
}
(out / 'provenance.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
fig, ax = plt.subplots(figsize=(7, 4.5))
for a, b in [('emotion_regulation','reward'),('emotion_regulation','depression'),('reward','depression')]:
    points = [r for r in rows if r['term_a'] == a and r['term_b'] == b]
    ax.plot([r['threshold_z'] for r in points], [r['jaccard'] for r in points], marker='o', label=f'{a.replace("_", " ")} × {b}')
ax.set(xlabel='Positive z threshold', ylabel='Jaccard overlap', title='Term-map overlap across thresholds')
ax.set_xticks([2, 3, 4, 5]); ax.set_ylim(bottom=0)
ax.legend(fontsize=8); fig.tight_layout(); fig.savefig(out / 'overlap.png', dpi=180); plt.close(fig)
print('Wrote results/overlap.csv, provenance.json, overlap.png')
