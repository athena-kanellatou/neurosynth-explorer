# Complete export of the four OpenAlex pilot queries

**28 September 2026 | Complete for these exact queries; no eligibility screening.** `export_openalex_full.py` retrieved every page of four documented OpenAlex searches with publication dates from 1 January 2019 through 28 September 2026. The machine-readable `openalex_full_log.json` stores exact queries, first request URLs, page counts, export counts and the SHA-256 hash of `openalex_full_export.csv`. The CSV carries OpenAlex IDs, titles, dates, DOI/PMID where available, query-arm membership and `NOT SCREENED` for every record. The per-page consistency check required all returned arm counts to match the opening count. Source query behavior is described in the [OpenAlex search documentation](https://help.openalex.org/api/searching/).

| Search phrase plus `fMRI` | Records exported |
|---|---:|
| `"cognitive reappraisal"` | 4,016 |
| `"emotion reappraisal"` | 182 |
| `"monetary incentive delay"` | 1,700 |
| `"monetary reward"` | 3,498 |

The sum of arm counts is 9,396; the union has **8,354 distinct OpenAlex IDs**. Of these, 424 link to **422 distinct** records among the 507 PubMed pilot records by PMID or normalized DOI; two PubMed records each link to two OpenAlex IDs. The other 7,930 are unmatched *OpenAlex records under this search*, not eligible new experiments. The 85 unmatched PubMed records are recorded in `pubmed_unmatched_openalex.csv`; they should not be described as absent from the entire OpenAlex database. There are 8,035 OpenAlex records with DOI, 5,186 with PMID, and 318 with neither. Fifteen DOI values occur on two OpenAlex IDs each, so an OpenAlex ID union does not complete bibliographic deduplication. These collisions need review by title/metadata, and repeated cohorts require a later independent check. See `cross_source_linkage.json` and `audit_cross_source.py`.

The broad OpenAlex `search` parameter can index available full text as well as titles and abstracts; it is **not equivalent** to the PubMed Title/Abstract queries. Its corpus includes articles, preprints, reviews, dissertations and other source types. Raw counts do not measure eligibility. The linkage counts for these two pilot strategies do not estimate sensitivity or recall of OpenAlex. The PubMed export itself must be rerun at a defined final date.

**Decision:** This is a complete *supplementary broad-source export*, not the final second-source search for the proposed systematic review. Screening all 8,354 IDs under the present strategy would be a separate substantial workload. A narrower, field-defined and recall-checked search strategy, preferably using a bibliographic database with accessible title/abstract field queries, should be set before the protocol freeze. Preserve this export as an audit trail; do not silently replace it or select records based on reported brain locations.
