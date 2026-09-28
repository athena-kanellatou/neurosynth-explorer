# PubMed feasibility pilot - 28 September 2026

The prospective protocol remains a **draft**, not a registered or frozen confirmatory protocol. This pilot assessed search volume before any title/abstract or full-text eligibility decisions. No records in `candidate_queue.csv` have been screened or included.

| Search arm | PubMed matches | Records queued for inspection |
|---|---:|---:|
| Emotion regulation | 1,024 | 25 |
| Reward | 2,590 | 25 |

The exact Title/Abstract queries, date range (1 January 2019 to 28 September 2026), relevance sort, returned PMIDs and API metadata are in `search_log.json`. The queue is an inspection sample, **not** a random sample and **not** the complete set of eligible studies. Search counts can change as PubMed indexing changes. Some records may appear in both arms; no deduplication has been performed on the complete result sets.

## Design implication before screening

The broad search has 3,614 arm-level hits before deduplication. A credible systematic review needs a planned screening workload, access to full texts and coordinate tables, and ideally a second independent screener. Before screening, narrow the operational research question to explicitly defined task contrasts or resource a full review; pilot revised queries and log all changes. Freeze the final protocol and exact search strings before assigning eligibility decisions. Do not call this pilot an independent replication.

## Provenance

The script `pilot_pubmed.py` uses NCBI ESearch and ESummary. See [NCBI E-utilities documentation](https://www.ncbi.nlm.nih.gov/books/NBK25499/) and the [PubMed search field guide](https://pubmed.ncbi.nlm.nih.gov/help/). No article full text is stored here.
