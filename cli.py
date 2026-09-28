"""Generate a reproducible local analysis report from two NIfTI maps."""
import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from analysis import load_map, compare


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("map_a", type=Path)
    p.add_argument("map_b", type=Path)
    p.add_argument("--output", type=Path, default=Path("results"))
    p.add_argument("--thresholds", type=float, nargs="+", default=[2.0, 3.0, 4.0, 5.0])
    args = p.parse_args()
    a, b = load_map(args.map_a), load_map(args.map_b)
    rows = compare(a, b, args.thresholds)
    args.output.mkdir(parents=True, exist_ok=True)
    with (args.output / "overlap.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    provenance = {
        "analysis": "positive association-test z-map overlap; descriptive only",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": [{"name": x.name, "sha256": x.sha256, "shape": x.array.shape,
                    "affine": x.affine.tolist()} for x in (a, b)],
        "thresholds_z": args.thresholds,
        "mask": "pairwise finite voxels",
        "software": "Neurosynth Map Explorer 0.2.0",
    }
    (args.output / "provenance.json").write_text(json.dumps(provenance, indent=2), encoding="utf-8")
    print(f"Saved {args.output / 'overlap.csv'} and {args.output / 'provenance.json'}")


if __name__ == "__main__":
    main()
