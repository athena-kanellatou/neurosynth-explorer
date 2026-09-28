"""Transparent descriptive comparisons of aligned Neurosynth z maps."""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import numpy as np
import nibabel as nib


@dataclass(frozen=True)
class MapData:
    name: str
    array: np.ndarray
    affine: np.ndarray
    sha256: str


def load_map(path: str | Path, name: str | None = None) -> MapData:
    path = Path(path)
    image = nib.load(str(path))
    values = np.asarray(image.get_fdata(dtype=np.float32))
    if values.ndim != 3 or not np.isfinite(values).any():
        raise ValueError(f"{path.name}: expected a finite 3D statistical map")
    return MapData(name or path.name, values, image.affine.copy(), sha256(path.read_bytes()).hexdigest())


def validate_grid(maps: list[MapData]) -> None:
    if len(maps) < 2:
        raise ValueError("At least two maps are needed")
    reference = maps[0]
    for other in maps[1:]:
        if other.array.shape != reference.array.shape or not np.allclose(other.affine, reference.affine, atol=1e-4, rtol=0):
            raise ValueError(f"{other.name}: grid/affine differs from {reference.name}; resample deliberately before analysis")


def compare(a: MapData, b: MapData, thresholds: list[float]) -> list[dict]:
    validate_grid([a, b])
    finite = np.isfinite(a.array) & np.isfinite(b.array)
    results = []
    for threshold in thresholds:
        if threshold <= 0:
            raise ValueError("Positive thresholds required")
        left = finite & (a.array >= threshold)
        right = finite & (b.array >= threshold)
        n1, n2 = int(left.sum()), int(right.sum())
        both = int(np.count_nonzero(left & right))
        union = n1 + n2 - both
        results.append({
            "threshold_z": float(threshold), "finite_voxels": int(finite.sum()),
            "a_voxels": n1, "b_voxels": n2, "shared_voxels": both,
            "jaccard": both / union if union else None,
            "dice": 2 * both / (n1 + n2) if n1 + n2 else None,
        })
    return results
