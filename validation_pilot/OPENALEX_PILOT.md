# Second-source search feasibility pilot: OpenAlex

**Retrieved 28 September 2026. No title/abstract or full-text eligibility screening.**

The script `pilot_openalex.py` searched OpenAlex works published from 1 January 2019 through 28 September 2026. It retrieved **only the first relevance-ranked page of at most 200 records per query**. The exact requests, returned page sizes and count metadata are in `openalex_pilot_log.json`; `openalex_first_page.csv` preserves the exported records and search-arm membership. Query and publication-date filters follow the [OpenAlex API](https://help.openalex.org/api/) and its [search guidance](https://help.openalex.org/api/searching/).

| Phrase plus `fMRI` | OpenAlex reported hits | Exported first page |
|---|---:|---:|
| `"cognitive reappraisal"` | 4,016 | 200 |
| `"emotion reappraisal"` | 182 | 182 |
| `"monetary incentive delay"` | 1,700 | 200 |
| `"monetary reward"` | 3,498 | 200 |

The four pages yielded **715 distinct OpenAlex IDs**; 243 matched a record in the 507-record PubMed pilot by PMID or normalized DOI. The remaining 472 are *not* 472 eligible or unique new studies. They may include off-topic records, duplicate reports, incomplete metadata, or works outside the eventual inclusion rules. This match count applies only to the exported pages; it cannot be extrapolated to all hits.

**Critical search difference:** OpenAlex's general `search` also searches full-text content when available, whereas the PubMed queries searched Title/Abstract fields. This explains why the raw hit counts cannot be compared as if the strategies were identical. The pages are incomplete in three of the four arms, and date/index changes can alter counts. This pilot is therefore a feasibility and query-design audit, **not a completed second database search or a PRISMA record flow**.

Before screening, design and document a defensible final second-source strategy, retrieve all records under that strategy, inspect its coverage and metadata, deduplicate against the final PubMed export, and freeze both searches. The proposed endpoint and other unresolved decisions remain in `NARROW_PROTOCOL_DRAFT.md`.
