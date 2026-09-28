# Final synthesis of the exploratory phase

**28 September 2026 | Status: exploratory, descriptive, not peer reviewed**

## Research question and answer

How stable is spatial overlap between Neurosynth association-test maps for `emotion regulation`, `reward`, and `depression` as the positive z threshold changes? The emotion-regulation/reward overlap persists at every examined threshold, but its *extent* contracts sharply: Jaccard falls from 0.120 at z >= 2 to 0.028 at z >= 5. The other pairs also depend on threshold, and their ordering changes. These are properties of automated literature maps, not evidence that any individual has a shared neural mechanism.

| Pair | z >= 2: shared / Jaccard | z >= 3 | z >= 4 | z >= 5 |
|---|---:|---:|---:|---:|
| Emotion regulation × reward | 4,725 / 0.120 | 1,296 / 0.067 | 420 / 0.040 | 169 / 0.028 |
| Emotion regulation × depression | 1,665 / 0.074 | 391 / 0.060 | 127 / 0.069 | 16 / 0.026 |
| Reward × depression | 2,441 / 0.084 | 536 / 0.034 | 108 / 0.012 | 7 / 0.001 |

The complete table, including separate active-voxel counts, finite-voxel counts and Dice, is in `results/overlap.csv`. The sweep is a sensitivity analysis, not four independent hypothesis tests. No statistical test of spatial overlap was performed.

## What the follow-ups add

- The two largest emotion-regulation/reward overlap components at z >= 3 comprise 395 and 296 voxels. At z >= 5, 88 (22.3%) and 76 (25.7%) of their original voxels remain. The first peak is labeled right amygdala in AAL SPM12; the second peak is unlabeled, although part of that component lies in the atlas's left amygdala. Peak labels do not describe every voxel in a component.
- The term lists share 20 studies between emotion regulation (247) and reward (922). This is 8.1% of the emotion-regulation set. Shared studies are one possible contribution to map similarity; these summary maps cannot attribute specific voxels to particular papers.
- NeuroQuery produces related but distinct predictions from overlapping literature. After resampling Neurosynth maps to its 4 mm grid, Spearman rank correlations are 0.272 for emotion regulation, 0.502 for reward and 0.399 for depression. At the top 5% of ranks, same-term Jaccard is 0.126, 0.391 and 0.115, respectively. This is a method comparison, not independent replication.

## Boundaries of the claim

Abstract terms are imperfect proxies for tasks and populations. In particular, `depression` need not mean a diagnosed patient sample. Study dependence, differing term-study counts, selective coordinate reporting, publication bias, threshold choice, atlas boundaries and spatial autocorrelation limit interpretation. A voxel count is neither a participant count nor an effect size. The comparison does not predict individual brains, symptoms or treatment. The separate cross-method results have resampling and model differences; their numerical z values are not directly exchanged with Neurosynth z thresholds.

The supplied 2019–2026 PubMed pilots address *feasibility only*: the broad search yielded 3,614 arm-level hits before complete deduplication; a proposed narrower cognitive-reappraisal/monetary-reward search yielded 507 unique PMID. All records remain unscreened. No prospective validation, coordinate extraction, corrected ALE, or confirmatory test has been completed.

## Next falsifiable question

After a dated protocol is frozen, do independent post-2018, whole-brain task-fMRI experiment sets for prespecified emotion-regulation and reward contrasts each produce family-wise-error-corrected coordinate-based maps whose intersection includes at least one voxel in **each** left and right AAL SPM12 amygdala region? A zero intersection in either region fails this prespecified endpoint. It would not establish an absence of shared neural processing. The current broad protocol is a draft; narrowing to cognitive reappraisal versus monetary reward is a documented proposal, requiring a second database, eligibility rules, corpus-independence audit and resource assessment before screening.

## Audit trail and use

Source URLs, retrieval date, hashes and geometry: `results/provenance.json`; computed results: `results/overlap.csv`, `results/cluster_stability.csv`, `results/study_overlap.csv`, `results/cross_method_sensitivity.csv`; figures: `results/overlap.png`, `results/orthogonal_overlap_z3.png`; study-design boundary: `INDEPENDENT_VALIDATION_PROTOCOL.md`, `validation_pilot/REVISION_PROPOSAL.md`. Run `python verify_reproduction.py` to check the bundled snapshot. The dashboard, notebook, two-page note and poster offer different ways to inspect these same exploratory findings.
