# Narrow independent-validation protocol: operational draft 0.1

**Prepared 28 September 2026. Not registered, frozen, screened, or analyzed.** This document proposes a narrower question than `INDEPENDENT_VALIDATION_PROTOCOL.md`. It does not supersede that draft until the unresolved decisions below are completed, dated, and frozen. The exploratory Neurosynth/NeuroQuery findings generated the anatomical hypothesis and cannot count as independent evidence.

## Question and primary endpoint

Among independent adult, nonclinical, task-fMRI experiments published from 1 January 2019 onward, do whole-brain coordinate-based meta-analyses of **cognitive reappraisal** and **monetary reward/incentive** each yield corrected positive-contrast maps whose intersection has at least one voxel in *each* left and right AAL SPM12 amygdala region? Report the intersection count separately for left and right and the full maps, including an empty intersection. This stringent conjunction is an operational test of a hypothesis from the earlier project; it does not identify a unique mechanism.

**Unit of analysis:** independent experiment/participant cohort, with prespecified contrast selection. A paper can contribute more than one independent cohort; multiple contrasts from one cohort must not create pseudo-independent experiments in a primary domain analysis.

## Candidate identification

The PubMed feasibility export in `narrow_search_log.json` used the following Title/Abstract searches through 28 September 2026, restricted to publication dates from 1 January 2019:

- Reappraisal: `("cognitive reappraisal"[tiab] OR "emotion reappraisal"[tiab]) AND (fMRI[tiab] OR "functional magnetic resonance imaging"[tiab]) AND (2019/01/01:2026/09/28[dp])` (135 records).
- Monetary reward: `("monetary incentive delay"[tiab] OR "monetary reward"[tiab]) AND (fMRI[tiab] OR "functional magnetic resonance imaging"[tiab]) AND (2019/01/01:2026/09/28[dp])` (372 records).

These 507 unique PubMed records are an **unscreened pilot queue**, not the final search. The presence of clearly irrelevant titles in the export is a reminder that keyword hits are not eligibility decisions. Before screening, add a second named bibliographic database, run date-stamped final searches in both, export complete records, deduplicate by PMID/DOI and then bibliographic identity, and preserve counts by source and stage. Search terms may be revised for recall during a documented search-design exercise, without selecting on observed brain locations. Freeze the final strings and end date before eligibility decisions.

## Eligibility decision sequence

1. **Title/abstract:** retain potential original human task-fMRI experiments involving deliberate cognitive reappraisal or monetary reward/incentive. Exclude clearly irrelevant modalities, reviews, editorials and unrelated tasks; use `UNCLEAR` if the abstract cannot establish exclusion.
2. **Full text:** require an adult cohort without reported clinical diagnosis in the analyzed group, an explicit task contrast, whole-brain peak coordinates (not solely ROI or small-volume-corrected peaks), a coordinate space, sample size and enough information to identify the participant cohort. Record one main exclusion reason, retaining all secondary reasons in notes. A reported brain location must never drive eligibility.
3. **Contrast rule to freeze:** reappraisal should compare instructed downregulation/reinterpretation with a specified control condition; reward should compare monetary reward anticipation with a specified neutral/no-reward condition. If multiple eligible contrasts exist, prioritize the paper's prespecified primary whole-brain contrast; unresolved ties require a written selection hierarchy before extraction. Analyze positive and negative directions separately.
4. **Independence:** match PMID/DOI to the saved Neurosynth study IDs and seek verifiable NeuroQuery training-corpus membership. Check repeated cohorts across papers using recruitment site, sample size, dates and author descriptions. Exclude overlaps from primary validation; if corpus membership is unverifiable, mark `UNCERTAIN` and exclude from the primary independent set. This may make the primary analysis infeasible and must be reported as such.
5. Two screeners should independently record decisions with adjudication. If only one screener is available, report that fact and keep a traceable decision log; do not label the review dual screened.

## Extraction and analysis lock

Record PMID, DOI, source table and page, cohort identifier, domain, task, exact contrast and direction, N, age, clinical status, whole-brain threshold, coordinate system and every eligible peak. Preserve original coordinates and any predeclared Talairach-to-MNI conversion. Store per-experiment foci separately from the screening table.

Before extraction or map inspection, freeze a runnable analysis specification with the exact NiMARE version, ALE estimator/kernel choices, common MNI mask and grid, permutation count, seed, voxel/cluster correction method and family-wise error threshold of 0.05. Define the minimum number of independent experiments per arm using a justified methodological source or simulation before knowing the included set. If either arm falls below that rule, stop the primary analysis as infeasible; do not loosen the rule after viewing maps. Define atlas version, resampling/intersection rules, connected-component connectivity and the treatment of empty maps. Run one domain map per arm and apply the prespecified bilateral intersection endpoint once. Log all exploratory subgroup and sensitivity results separately.

## Decision gates before any eligibility screening

| Gate | Current status | Required record |
|---|---|---|
| Final question and contrast hierarchy | Proposed | Dated, unambiguous contrast-selection rule |
| Second database and searches | Missing | Complete export, queries, dates and deduplication flow |
| Full texts and reviewer staffing | Unconfirmed | Access plan, reviewers and adjudication procedure |
| Independence against source corpora | Unresolved | Verifiable matching rules and uncertain-case handling |
| Minimum experiment count and exact ALE settings | Unspecified | Justification, environment lock and executable configuration |
| Protocol freeze | Not done | Dated version plus subsequent amendment log |

**Next action:** resolve the gates, then freeze a numbered protocol. Only then begin title/abstract screening of the final deduplicated search set. The current queue remains `NOT SCREENED`; no claims about eligible studies or independent validation follow from its size.
