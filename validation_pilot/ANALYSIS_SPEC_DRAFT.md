# Coordinate meta-analysis specification, draft 0.1

**28 September 2026. Not frozen or registered; no eligible experiments extracted.** This specifies proposed decisions before outcome maps exist. The protocol still needs a final search review, exact contrast-selection hierarchy, access to full texts, reviewers and a tested software environment. Do not call an empty or simulated analysis an independent validation.

## Unit and feasibility

Use one independent participant cohort per domain in the primary analysis; a cohort reported twice cannot be counted twice. Select an explicit whole-brain positive task contrast for cognitive reappraisal and monetary reward anticipation, keeping separate negative contrasts out of the primary sets. Require at least **17 independent experiments in each domain** before fitting ALE. Eickhoff et al. (2016) found that, under their simulations, cluster-level FWE inference with 17 or more experiments controlled excessive contribution from one experiment; 17 is a pragmatic feasibility floor, **not** a guarantee of power for bilateral amygdala overlap. Report the number of subjects, experiments and foci per arm before running anything.

## Proposed locked parameters

| Parameter | Proposed value / rule |
|---|---|
| Software | NiMARE 0.21.0, exact installed build to be recorded after environment validation |
| Estimator | ALE, with NiMARE's ALEKernel and experiment-level `n_subjects` |
| Space | MNI; preserve source Talairach coordinates and one documented conversion if needed |
| Mask | One documented common whole-brain MNI mask for both arms, saved with SHA-256 |
| Null correction | Monte Carlo cluster-size FWE, 5,000 iterations, cluster-defining uncorrected p < 0.001 |
| Corrected map | Cluster-size FWE p < 0.05, positive contrasts, each arm separately |
| Anatomical endpoint | Intersection of the two corrected binary maps within each left and right AAL SPM12 amygdala label; at least one voxel in **each** label |
| Randomness | Record and set a seed using the tested NiMARE implementation before freeze |
| Grid | Resample atlas labels to the analysis grid with nearest-neighbor interpolation only; save original and target geometry |
| Sensitivity | One experiment per cohort, leave-one-out if feasible, and alternate atlas/broader medial temporal mask, all clearly exploratory |

The software documentation describes ALE and Monte Carlo FWE options, including 5,000 iterations and the default p = 0.001 cluster-defining threshold: [NiMARE ALE](https://nimare.readthedocs.io/en/stable/generated/nimare.meta.cbma.ale.ALE.html). The feasibility rationale comes from [Eickhoff et al. 2016](https://pubmed.ncbi.nlm.nih.gov/27179606/). The chosen mask, atlas file hash, coordinate conversion, software build and seed remain **unresolved** and must be filled before protocol freeze. This file is a draft specification rather than a tested analysis pipeline.

## Decision rule

If fewer than 17 independent eligible experiments remain in either arm, or any required source-independence status remains uncertain, report **primary analysis infeasible** and stop. If both corrected maps exist, report each arm's map, cluster sizes, left/right intersection counts and the binary endpoint, including zeros. The endpoint's failure is not proof that the processes lack a common neural substrate. No post-hoc threshold relaxation is permitted to rescue the endpoint.
