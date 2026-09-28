"""Descriptive connected components and orthogonal overlays for two z maps."""
from pathlib import Path
import numpy as np
import nibabel as nib
from scipy import ndimage
import matplotlib.pyplot as plt
from analysis import load_map, validate_grid


def overlap_clusters(a, b, threshold=3., min_voxels=10):
    validate_grid([a, b])
    common = np.isfinite(a.array) & np.isfinite(b.array) & (a.array >= threshold) & (b.array >= threshold)
    labels, number = ndimage.label(common, structure=ndimage.generate_binary_structure(3, 1))
    rows = []
    minimum = np.minimum(a.array, b.array)
    volume_mm3 = abs(np.linalg.det(a.affine[:3, :3]))
    for idx in range(1, number + 1):
        voxels = np.argwhere(labels == idx)
        if len(voxels) < min_voxels:
            continue
        scores = minimum[labels == idx]
        peak_ijk = voxels[np.argmax(scores)]
        xyz = nib.affines.apply_affine(a.affine, peak_ijk)
        centroid_xyz = nib.affines.apply_affine(a.affine, voxels.mean(axis=0))
        rows.append({'voxels': len(voxels), 'volume_mm3': round(len(voxels)*volume_mm3),
                     'peak_mni_x': round(float(xyz[0]), 1), 'peak_mni_y': round(float(xyz[1]), 1),
                     'peak_mni_z': round(float(xyz[2]), 1),
                     'centroid_mni_x': round(float(centroid_xyz[0]), 1),
                     'centroid_mni_y': round(float(centroid_xyz[1]), 1),
                     'centroid_mni_z': round(float(centroid_xyz[2]), 1),
                     'peak_min_z': round(float(np.max(scores)), 3),
                     'peak_ijk': peak_ijk.tolist()})
    rows.sort(key=lambda row: row['voxels'], reverse=True)
    return common, rows


def plot_orthogonal(a, b, threshold, center, output):
    """Use a common nonzero map footprint as neutral background, not an atlas."""
    shared = np.isfinite(a.array) & np.isfinite(b.array) & (a.array >= threshold) & (b.array >= threshold)
    only_a = np.isfinite(a.array) & (a.array >= threshold) & ~shared
    only_b = np.isfinite(b.array) & (b.array >= threshold) & ~shared
    footprint = (a.array != 0) | (b.array != 0)
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for axis, ax, label in zip(range(3), axes, ('sagittal', 'coronal', 'axial')):
        index = int(center[axis])
        slice_at = lambda image: np.rot90(np.take(image, index, axis=axis))
        ax.imshow(slice_at(footprint), cmap='Greys', vmin=-0.5, vmax=2.0)
        rgb = np.zeros((*slice_at(shared).shape, 4), dtype=float)
        rgb[slice_at(only_a)] = [0.2, 0.4, 0.95, .75]
        rgb[slice_at(only_b)] = [0.95, 0.45, 0.1, .75]
        rgb[slice_at(shared)] = [0.65, 0.1, 0.7, 1]
        ax.imshow(rgb)
        ax.set(title=f'{label} (voxel {index})', xticks=[], yticks=[])
    fig.suptitle(f'z ≥ {threshold}: blue={a.name}, orange={b.name}, purple=overlap', fontsize=10)
    fig.tight_layout(); fig.savefig(output, dpi=180); plt.close(fig)


def main():
    root = Path(__file__).parent
    a = load_map(root/'data/emotion_regulation.nii.gz', 'emotion regulation')
    b = load_map(root/'data/reward.nii.gz', 'reward')
    common, clusters = overlap_clusters(a, b)
    import csv
    out = root/'results'
    with (out/'overlap_clusters_z3.csv').open('w', newline='', encoding='utf-8') as f:
        columns = ['rank','voxels','volume_mm3','peak_mni_x','peak_mni_y','peak_mni_z',
                   'centroid_mni_x','centroid_mni_y','centroid_mni_z','peak_min_z']
        writer = csv.DictWriter(f, fieldnames=columns); writer.writeheader()
        for rank, row in enumerate(clusters, 1):
            writer.writerow({key: rank if key == 'rank' else row[key] for key in columns})
    center = clusters[0]['peak_ijk'] if clusters else [n//2 for n in a.array.shape]
    plot_orthogonal(a, b, 3., center, out/'orthogonal_overlap_z3.png')
    print('Shared voxels:', int(common.sum()), 'clusters ≥10 voxels:', len(clusters))
    print('Largest clusters:', clusters[:5])

if __name__ == '__main__': main()
