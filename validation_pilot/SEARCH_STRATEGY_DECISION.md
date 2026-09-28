# Search-strategy decision memo 0.1

**28 September 2026 | Pre-screening methodological audit; no article-level eligibility decisions.**

## What the bounded OpenAlex export shows

The 715 unique records exported in the previous pilot have 711 DOI values, 608 PMID values, and four with neither. There are 590 records tagged `article`, 51 `preprint`, 48 `review`, and other OpenAlex types. These are **source metadata labels**, not our inclusion decisions. `openalex_metadata_audit.json` gives the exact counts and per-query checks; `audit_openalex_pilot.py` reproduces them.

| Query arm | Exported | Exact phrase appears in title | Title mentions fMRI or full name | Matched PubMed pilot by PMID/DOI |
|---|---:|---:|---:|---:|
| Cognitive reappraisal | 200 | 85 | 55 | 62 |
| Emotion reappraisal | 182 | 3 | 13 | 17 |
| Monetary incentive delay | 200 | 23 | 48 | 121 |
| Monetary reward | 200 | 39 | 68 | 76 |

The title checks inspect only the title string. An article can be relevant when the phrase appears in its abstract or full text instead. Conversely, matching a phrase in a title does not prove eligibility. Arms overlap, so column counts cannot be summed as unique studies. Three arms were truncated at 200 and the relevance-ranked first pages are a biased subset; none of these fractions estimates precision, recall, or the eventual number of studies.

## Decision

Do **not** treat the current OpenAlex query as the final second-database strategy. OpenAlex's general search can match full text, while the PubMed pilot searches title/abstract. Its very large raw counts and the title audit make a full export under the present terms a sizable, methodologically different task. Both differences must be addressed in the search design before final deduplication and screening. See [OpenAlex search documentation](https://help.openalex.org/api/searching/).

Candidate path: test a second bibliographic source that supports documented title/abstract field searches and complete export through institutional access; or define a separate, explicitly broader OpenAlex supplementary search, retrieve every result and report its distinct scope. A title-only OpenAlex filter would silently lose abstract-only hits and should not be presented as equivalent to PubMed Title/Abstract. The preferred final source, access route and exact syntax remain **unresolved**. No protocol freeze or screening is justified yet.

## Subsequent export and remaining gate

The four broad OpenAlex queries were subsequently exported in full; see `OPENALEX_FULL_EXPORT.md` for 8,354 unique IDs and the hashed export. This addresses completeness **for those broad queries**, but not the field-scope and workload concern above. Establish a defensible field-defined final second-source strategy, reconcile it with a freshly run final PubMed search by DOI, PMID and bibliographic identity, and resolve cohort-independence and ALE configuration gates in `NARROW_PROTOCOL_DRAFT.md`. Freeze the protocol before any eligibility decision.
