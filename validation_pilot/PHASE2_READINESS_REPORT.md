# Independent-validation readiness report

**28 September 2026. No independent meta-analysis result.** The sequence below distinguishes completed source preparation from scientific steps that require article-level judgments and extracted coordinates.

| Stage | Completed now | Remaining before an independent result |
|---|---|---|
| 1. Search and deduplication | Complete pilot PubMed 507, OpenAlex title/abstract 640; PMID/DOI merge gives 731 unscreened groups (414 in both, 93 PubMed only, 224 OpenAlex only). Exact requests and hashes saved. | Validate recall with a prespecified known-paper set, review titles/DOIs for residual duplicates, rerun final searches at a frozen date. |
| 2. Source independence | Compared 731 records with all 14,371 Neurosynth v0.7 IDs and 13,459 NeuroQuery model PMIDs. One confirmed Neurosynth ID match, zero NeuroQuery PMID matches; five further records without PMID have exact title matches with at least one source corpus. | Resolve those five title matches, 213 records without PMID and any repeated participant cohorts using DOI, full text and source data. |
| 3. Protocol and analysis | Draft contrast and ALE choices are in `NARROW_PROTOCOL_DRAFT.md` and `ANALYSIS_SPEC_DRAFT.md`; minimum 17 independent experiments per arm proposed. | Confirm source recall, exact contrast tie-breaks, coordinate conversion, atlas/mask hash, NiMARE environment/seed and review staffing; then date and freeze the protocol. |
| 4. Screening and extraction | An auditable 731-record queue with source and overlap flags exists. **No records screened.** | Review titles/abstracts and full texts, document inclusion/exclusion and cohort identity, extract whole-brain MNI/Talairach foci with source-table citations. |
| 5. ALE and report | `validation_gate.py` produces `VALIDATION_READINESS.json` with `BLOCKED` and 0 extracted experiments in each arm. **No ALE run.** | Only after stage 4 and >=17 independent experiments per arm: run corrected maps, bilateral conjunction, sensitivity analyses and complete PRISMA-style reporting. |

The one direct Neurosynth match is PMID **29428771**, listed under emotion regulation despite the PubMed pilot's 2020 publication-date entry. The source DOI contains 2018; publication dates alone cannot establish independence. The five additional exact title matches are **flags**, not confirmed identical papers or exclusions. Absence of a PMID match is not proof of an independent participant cohort.

The proposed ALE minimum follows [Eickhoff et al. 2016](https://pubmed.ncbi.nlm.nih.gov/27179606/) under cluster-level FWE simulation conditions; NiMARE's [ALE documentation](https://nimare.readthedocs.io/en/stable/generated/nimare.meta.cbma.ale.ALE.html) describes Monte Carlo correction. Neither supplies missing coordinates or converts this search queue into a meta-analysis. The [PRISMA 2020 checklist](https://www.prisma-statement.org/prisma-2020-checklist) is a reporting guide for the eventual study, not evidence that screening has occurred.

**Current conclusion:** The exploratory Neurosynth overlap result remains the only brain-map finding. A confirmatory bilateral-amygdala claim is blocked by unscreened records, unverified cohort independence and zero extracted experiments. Do not infer either success or failure of that endpoint.
