# Sources and reuse notes

## Neurosynth maps and study identifiers

The three `data/*.nii.gz` files and term-associated study identifiers were retrieved from Neurosynth on 28 September 2026. The exact map URLs, file hashes, geometry, source study counts, and study listing endpoints are in `results/provenance.json` and `results/study_id_sets.json`. The Neurosynth data repository describes its data as Open Database License (ODbL); public reuse should attribute Neurosynth, keep applicable derived databases open, and check the full current licence terms: https://github.com/neurosynth/neurosynth-data . The original method is Yarkoni et al., Nature Methods 2011, DOI 10.1038/nmeth.1635.

## NeuroQuery maps

The three `neuroquery_maps/*.nii.gz` files were generated locally from the public pretrained `neuroquery_model` using NeuroQuery 1.1.0 and the exact phrases in `results/neuroquery_provenance.json`. The model source is https://osf.io/598tj/download and method is Dockes et al., eLife 2020, DOI 10.7554/eLife.53385. The model archive is not included. Before republishing generated maps, review the current model and data reuse terms at https://github.com/neuroquery/neuroquery and https://github.com/neuroquery/neuroquery_data .

The validation pilot includes the NeuroQuery model's `corpus_metadata.csv` and Neurosynth v0.7 `metadata.tsv.gz` solely to audit source-study identity. Exact source URLs and SHA-256 values are recorded in `validation_pilot/corpus_independence_log.json`. Preserve upstream attribution and applicable licences when redistributing these metadata files.

## AAL SPM12 atlas

The AAL atlas image is not included. `atlas_labels.py` retrieves the archive linked in Nilearn's AAL documentation, checks its geometry, and uses its label XML to generate the supplied annotation table. Attribution and any atlas reuse terms remain with the atlas authors and distributors.

## Project status

The code and report are an exploratory educational analysis. No patient-level data are included. This document does not grant a new licence to upstream datasets or models.
