# Exploratory result: three Neurosynth association maps

Data retrieved 28 September 2026. The source files, exact API URLs, SHA-256 hashes, image geometry, and counts reported on the term pages are recorded in `provenance.json`. The three NIfTI maps are included under `data/`. No resampling was performed; all have shape 91 × 109 × 91 and matching affine.

## Primary pair: emotion regulation × reward

| Positive z threshold | Emotion regulation voxels | Reward voxels | Shared voxels | Jaccard | Dice |
|---:|---:|---:|---:|---:|---:|
| 2 | 18,354 | 25,801 | 4,725 | 0.120 | 0.214 |
| 3 | 5,517 | 15,112 | 1,296 | 0.067 | 0.126 |
| 4 | 1,685 | 9,120 | 420 | 0.040 | 0.078 |
| 5 | 586 | 5,722 | 169 | 0.028 | 0.054 |

The primary pair overlaps less at higher positive z thresholds. The `reward` map has many more supra-threshold voxels at high thresholds, which affects Jaccard's denominator. This observation is descriptive; it does not establish that emotion regulation and reward rely on separate brain systems.

At z ≥ 3, the secondary Jaccard values are 0.060 for `emotion regulation` × `depression` and 0.034 for `reward` × `depression`. Across all three terms, differences in article keywords, study counts (247, 922, 502), reported activation coordinates, and research practices can contribute to these patterns.

The unthresholded maps were retrieved from endpoints used by the Neurosynth viewer. Our threshold choices are illustrative and do not establish FDR or family-wise error control. No clinical diagnosis, subject-level data, or causal inference is involved. Before making anatomical claims, examine maps in multiple planes and validate peaks against an atlas. A significance claim about overlap would need a justified spatial null model and study-dependence analysis.

Reproduce tables and figure with `python make_report.py`. The figure `overlap.png` is descriptive. Source: [Neurosynth](https://neurosynth.org/) and [FAQ](https://neurosynth.org/faq/). Data attributed to Neurosynth; see its [data repository and Open Database License](https://github.com/neurosynth/neurosynth-data).

## Step 2: Where does the primary overlap occur?

At z ≥ 3, `emotion regulation` × `reward` has 1,296 shared positive voxels. A six-neighbor connected-component analysis found 10 components of at least 10 voxels. The largest two contain 395 and 296 voxels; their peaks (chosen by the highest minimum z across both maps) are at MNI **(24, 2, −16)** and **(−18, 2, −14)**. Three orthogonal views through the first peak are in `orthogonal_overlap_z3.png`: blue indicates emotion regulation only, orange reward only, and purple overlap. The dark outline shows a shared map footprint and **is not an anatomical MRI or atlas**. Full peak and centroid coordinates are in `overlap_clusters_z3.csv`.

These components are summaries of thresholded spatial patterns. Their sizes and boundaries depend on the threshold and six-neighbor definition. Region names have deliberately not been assigned without an independently checked atlas. The coordinates are candidate locations for follow-up, not precise localization or evidence of a unique psychological mechanism.

Reproduce this stage with `python spatial.py`. Unit checks: `python -m unittest discover -p 'test*.py'`.

## Step 3: Atlas check

We checked the components against **AAL SPM12**, whose label image has the exact same 91 × 109 × 91 grid and affine as these Neurosynth maps. `atlas_labels_z3.csv` reports the AAL label *at each component peak* and the three most frequent labels across that component. The largest component's peak **(24, 2, −16)** is labeled `Amygdala_R`; of its 395 voxels, 159 are assigned `Amygdala_R`, 71 `Hippocampus_R`, and 109 are outside the AAL parcellation. The second component's peak **(−18, 2, −14)** falls outside an AAL label, though 127 of its 296 voxels are assigned `Amygdala_L` and 32 `Hippocampus_L`. This demonstrates why a single peak label must not stand in for an entire component.

AAL labels are atlas-defined spatial annotations, not evidence that the associated mental processes localize uniquely to those structures. The atlas can leave voxels unlabeled and its boundaries are template dependent. The script `python atlas_labels.py` verifies matching image geometry and retrieves the official AAL SPM12 archive if needed. The atlas itself is not redistributed in this project. Source: [Nilearn AAL documentation](https://nilearn.github.io/stable/modules/generated/nilearn.datasets.fetch_atlas_aal.html) and its linked [AAL SPM12 archive](https://osf.io/s94qg/).

## Step 4: Threshold robustness of the two largest components

We anchored the components at z ≥ 3 and measured what fraction of *those same voxels* remains in the intersection when both maps must exceed higher cutoffs. This is a nested descriptive check, not a new statistical test.

| z ≥ | First component retained / 395 | Second component retained / 296 |
|---:|---:|---:|
| 3 | 395 (100%) | 296 (100%) |
| 4 | 190 (48.1%) | 151 (51.0%) |
| 5 | 88 (22.3%) | 76 (25.7%) |

At z ≥ 5, the largest connected remnants contain 87 and 75 voxels respectively. Thus both broad z ≥ 3 patterns contain smaller contiguous high-z cores. This does **not** validate anatomical specificity or statistical significance of the overlap: thresholds are arbitrary and the underlying Neurosynth maps are derived from partly overlapping literature. The z ≥ 2 reference retention is necessarily 100%, because lowering a threshold retains every voxel selected at z ≥ 3; it says nothing about the growth or shape of the full z ≥ 2 components. Full values are in `cluster_stability.csv` and can be regenerated with `python robustness.py`.

## Step 5: Shared studies behind the term maps

We retrieved the study IDs listed for each Neurosynth term and compared the sets. Counts match those displayed on the term pages. Full ID sets, source endpoints, and reproducible code are in `study_id_sets.json` and `study_overlap.py`.

| Term pair | Shared studies | Share of first term | Share of second term | Study-set Jaccard |
|---|---:|---:|---:|---:|
| Emotion regulation × reward | 20 | 8.1% | 2.2% | 0.017 |
| Emotion regulation × depression | 31 | 12.6% | 6.2% | 0.043 |
| Reward × depression | 58 | 6.3% | 11.6% | 0.043 |

For the primary comparison, 20 of the 247 emotion-regulation studies also appear in the reward set. That is a measurable source of non-independence. The 1,296 shared voxels at z ≥ 3 must **not** be attributed to those 20 studies: the published aggregate maps do not provide a per-study decomposition of that overlap. Even distinct studies can share paradigms, conventions, subjects, or reporting biases. This audit limits interpretation; it cannot remove those dependencies or establish that the remaining overlap is statistically surprising.

## Step 7: Cross-method check with NeuroQuery

We used the published pretrained NeuroQuery model (`neuroquery` 1.1.0) to generate *predicted* `brain_map` images for the exact phrases `emotion regulation`, `reward`, and `depression`. These are different statistical objects from Neurosynth association-test maps: NeuroQuery predicts where a study about a phrase may report activations, while Neurosynth tests associations between a term's use and reported coordinates. We therefore do **not** compare their z thresholds or p values.

To compare broad spatial patterns, Neurosynth's 2 mm maps were linearly resampled to NeuroQuery's 4 mm grid. Analysis was confined to 28,542 voxels that were finite and nonzero in both maps. We calculated Spearman rank correlation and Jaccard overlap of the top 5% highest-valued voxels **within each map**. This 5% is a descriptive rank cutoff, not a significance threshold.

| Phrase | Spearman ρ | Shared top-5% voxels | Top-5% Jaccard |
|---|---:|---:|---:|
| Emotion regulation | 0.272 | 319 | 0.126 |
| Reward | 0.502 | 802 | 0.391 |
| Depression | 0.399 | 295 | 0.115 |

On these choices, the `reward` pattern agrees more strongly across methods than `emotion regulation`. Differences in corpora, text representations, model objectives, resolution, smoothing, and selected maps may explain differences. NeuroQuery and Neurosynth draw on related published neuroimaging literature, so this is **methodological triangulation, not an independent replication**. No clinical inference follows. Map hashes, phrases, geometry, package and model source are in `neuroquery_provenance.json`; outputs are in `cross_method.csv`.

Sources: [NeuroQuery model and code](https://github.com/neuroquery/neuroquery), [NeuroQuery methodology](https://neuroquery.org/about), and [Neurosynth FAQ](https://neurosynth.org/faq/). Reproduce with `python generate_neuroquery.py` followed by `python cross_method.py` (requires `requirements-replication.txt`).

## Step 8: Sensitivity of cross-method ranking to the selected fraction

We repeated the top-ranked voxel comparison at 1%, 5%, and 10% within the same 28,542-voxel common mask. This checks whether the earlier 5% choice drove the qualitative comparison; it does not create independent tests.

| Phrase | Top 1% Jaccard | Top 5% Jaccard | Top 10% Jaccard |
|---|---:|---:|---:|
| Emotion regulation | 0.244 | 0.126 | 0.156 |
| Reward | 0.546 | 0.391 | 0.399 |
| Depression | 0.034 | 0.115 | 0.146 |

`Reward` has the highest top-ranked spatial overlap at all three fractions. `Emotion regulation` exceeds `depression` at 1% and 5%, while their overlap is similar at 10%. Whole-mask Spearman ranks tell a different detail: `depression` (ρ = 0.399) exceeds `emotion regulation` (ρ = 0.272). The choice between global rank correlation and focal high-value overlap changes what “agreement” means. These cutoffs are exploratory, the voxels are spatially dependent, and the methods share some underlying literature. Reproduce with `python cross_method_sensitivity.py`; results are in `cross_method_sensitivity.csv`.

## Step 10: Reproduction audit

The bundled offline audit (`python verify_reproduction.py`) checked the SHA-256 hashes and geometry of all six map files, recomputed every threshold row for all three Neurosynth term pairs, and recomputed the shared-study counts from the saved study ID sets. On 28 September 2026 it returned **75 checks passed, 0 failed**; individual results are in `REPRODUCTION_AUDIT.json`. This does not independently verify the upstream publications, the AAL labeling without its source atlas, or the NeuroQuery pretrained model without downloading it again. Those dependencies and URLs are recorded in the provenance files.
