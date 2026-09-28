# Prospective validation protocol (draft, not registered)

**Status:** Planned research only. No studies have been screened or analyzed under this protocol. Freeze and date this document before the first new screening decision; record any amendment separately. The current Neurosynth findings generated the hypothesis and must not be counted as independent confirmation.

## Question and target

Do independent post-2018 task-fMRI studies of emotion regulation and reward show spatial convergence in bilateral medial temporal regions under a prespecified coordinate-based meta-analysis? The existing project found bilateral overlap in automated term maps; that observation is the hypothesis source, not validation evidence.

## Search and eligibility

- Search PubMed/MEDLINE and a second bibliographic database from 1 January 2019 through the actual search date. Record exact query strings, database export dates, and deduplication counts. Candidate concept blocks: `(emotion regulation OR reappraisal OR downregulation)` and `(reward OR monetary incentive OR reinforcement)`, each combined with `(fMRI OR functional magnetic resonance imaging)`.
- Include original human task-fMRI studies with whole-brain coordinates for an explicitly defined emotion-regulation or reward contrast, sample size, coordinate space, and sufficient methods to map a unique participant cohort.
- Exclude reviews, purely resting-state studies, ROI-only coordinate reporting, animal studies, unavailable coordinate tables, and repeated reports of the same participants for the same contrast. Record one primary exclusion reason per full-text record.
- Keep clinical populations and medication manipulations in a separate exploratory stratum; the primary stratum is adults without a clinical diagnosis reported for the analyzed group. If a study includes several independent groups, record them separately and avoid counting a participant twice.
- Exclude any study present in the saved Neurosynth term-ID lists and any study identified as part of the NeuroQuery training corpus, where that can be verified. If corpus membership cannot be established, mark independence as **uncertain** and keep it out of the primary validation set. Match by DOI, PMID and cohort details, not title alone.
- Do not select papers by whether their reported peaks are in the amygdala. Screening uses design and reporting criteria only. Two independent screeners and adjudication are preferred; if unavailable, state that limitation rather than claiming dual screening.

## Extraction

For each independent experiment record DOI/PMID, cohort ID, domain, contrast, direction, N, age summary, clinical status, task, scanner/analysis summary, whole-brain threshold, coordinate space, all eligible peak coordinates, and any coordinate conversion. Keep a link to the exact table and a decision log. Convert Talairach coordinates to MNI using one prespecified transform and retain originals. Do not mix positive and negative contrasts without distinct analyses.

Use `validation_screening_template.csv` for the screening log. For each included experiment, create a separate coordinate table with `experiment_id, x, y, z, space, contrast_direction, source_table` and preserve the original source extract. The supplied template contains headers only.

## Analysis plan (freeze before extraction)

1. Define the primary comparison as one emotion-regulation experiment set and one reward experiment set, with independent participant cohorts. Record the number of studies, experiments, subjects and foci in each.
2. Run a current, documented NiMARE coordinate-based ALE pipeline separately per domain, using experiment-level modeling, a common MNI mask, permutation-based correction with family-wise error control at 0.05, and a fixed software version and random seed. Write down all kernel, correction, and permutation parameters before execution. Review whether the available number of independent experiments supports a stable analysis; if not, report the project as infeasible rather than relaxing thresholds after seeing results.
3. The primary endpoint is whether the intersection of the two corrected maps contains at least one connected voxel within **each** of the left and right AAL SPM12 amygdala regions. Report the full corrected maps, overlap volume, and cluster coordinates, including zeros. This is a stringent anatomical hypothesis derived from the exploratory analysis, not a proof of shared mechanism.
4. Sensitivity analyses: (a) one experiment per cohort, (b) task-subtype strata if enough studies, (c) leave-one-study-out influence, (d) an alternate atlas or broader medial temporal mask, and (e) matched experiment-count subsampling if domain sizes differ markedly. Label all secondary analyses as exploratory and report every attempt.
5. Do not interpret a failed endpoint as evidence that the processes have no shared substrate: insufficient power, task heterogeneity, and coordinate-reporting limitations remain plausible.

## Reporting and decision log

Report the search strategy and flow counts with PRISMA 2020 items adapted to a neuroimaging review; PRISMA is a reporting guide, not a guarantee of methodological validity. Deposit the dated protocol, inclusion decisions, anonymized extraction table, code, software versions, atlas and correction parameters, and all outputs subject to source licences. A separate `AMENDMENTS.md` should record deviations before reruns.

## Sources

- [PRISMA 2020 official checklist](https://www.prisma-statement.org/prisma-2020-checklist)
- [NiMARE coordinate-based meta-analysis documentation](https://nimare.readthedocs.io/en/stable/api.html)
- Eickhoff et al., random-effects ALE and empirical spatial uncertainty: [PMCID PMC2872071](https://pmc.ncbi.nlm.nih.gov/articles/PMC2872071/)
- Exploratory hypothesis source: `results/RESEARCH_NOTE.pdf` and this project's provenance files.
