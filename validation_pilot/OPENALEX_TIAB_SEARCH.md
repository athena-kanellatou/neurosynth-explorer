# Complete OpenAlex title/abstract search pilot

**28 September 2026 | Not screened; protocol not frozen.** A second-source search can use OpenAlex's `title_and_abstract.search` field through its OQO query API. The [OpenAlex property registry](https://api.openalex.org/properties/works) exposes that field, and the [OQL/OQO documentation](https://help.openalex.org/api/oql/) describes nested queries and paging. `export_openalex_tiab.py` stores the complete first-page request body, echoed server query, per-arm page counts, export counts and CSV SHA-256 in `openalex_tiab_log.json`. The actual exported records are in `openalex_tiab_export.csv`; each is marked `NOT SCREENED`.

Both arms used publication dates 1 January 2019 to 28 September 2026 and searched only OpenAlex's title/abstract field:

| Arm | Search expression | Complete export |
|---|---|---:|
| Reappraisal | `(“cognitive reappraisal” OR “emotion reappraisal”) AND (fMRI OR “functional magnetic resonance imaging”)` | 183 |
| Monetary reward | `(“monetary incentive delay” OR “monetary reward”) AND (fMRI OR “functional magnetic resonance imaging”)` | 457 |

The union is **640 OpenAlex IDs** (no cross-arm ID overlap in this retrieval). **416 OpenAlex IDs** link by PMID or DOI to **414 distinct PubMed pilot records**. Thus 93 of the 507 PubMed pilot records have no identifier link *under these two OpenAlex queries*, and 224 OpenAlex IDs do not link to the PubMed pilot. Two PubMed records have two linked OpenAlex IDs each; two DOI values also appear on two OpenAlex IDs each. A bibliographic and cohort-level deduplication still remains. Eighteen exported OpenAlex records have neither DOI nor PMID. These are search-linkage and metadata observations, not judgments of relevance, eligibility, or source recall.

This search is more manageable and field-aligned with PubMed than the earlier full-text-inclusive 8,354-ID export. It is still not an identical query: the OpenAlex search was expressed as two combined arms with an `fMRI OR full phrase` clause, while the PubMed pilot used two separate phrase queries per arm and its own indexing. Fifty-six IDs in this export were not in the earlier broad OpenAlex export, consistent with those search-expression differences. Neither set should be silently substituted for the other.

## Remaining search gate

Review search recall against a prespecified known-paper set *without choosing studies by brain result*, decide whether synonyms and date/end-date rules should change, and document the final query translations for each source. Then rerun both complete source exports at a final recorded date, reconcile DOI/PMID and bibliographic duplicates, and freeze the protocol before any eligibility decision. A 640-ID candidate source export is still a substantial screening task and may require a second reviewer or a recorded single-reviewer limitation.
