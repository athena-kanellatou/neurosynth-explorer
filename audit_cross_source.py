"""Cross-source identifier linkage; no article eligibility assessment."""
import csv
import json
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).parent/'validation_pilot'
pubmed=list(csv.DictReader((ROOT/'narrow_full_queue.csv').open(encoding='utf-8',newline='')))
openalex=list(csv.DictReader((ROOT/'openalex_full_export.csv').open(encoding='utf-8',newline='')))
by_pmid=defaultdict(set);by_doi=defaultdict(set)
for x in openalex:
    if x['pmid']:by_pmid[x['pmid']].add(x['openalex_id'])
    if x['doi']:by_doi[x['doi'].lower()].add(x['openalex_id'])
links={x['pmid']:by_pmid[x['pmid']]|by_doi[x['doi'].lower()] for x in pubmed}
unmatched=[{**x,'cross_source_status':'NO IDENTIFIER MATCH IN FOUR OPENALEX QUERIES'}
           for x in pubmed if not links[x['pmid']]]
with (ROOT/'pubmed_unmatched_openalex.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(unmatched[0]));w.writeheader();w.writerows(unmatched)
summary={'scope':'Identifier linkage between two pilot search exports, not eligibility or database recall',
         'pubmed_pilot_records':len(pubmed),'openalex_unique_ids':len(openalex),
         'pubmed_records_with_at_least_one_openalex_id':sum(bool(v) for v in links.values()),
         'pubmed_records_without_identifier_match':len(unmatched),
         'openalex_ids_linked_to_pubmed':len(set().union(*links.values())),
         'pubmed_pmids_with_multiple_openalex_ids':{k:sorted(v) for k,v in links.items() if len(v)>1},
         'unmatched_pubmed_reappraisal':sum(x['in_reappraisal']=='1' for x in unmatched),
         'unmatched_pubmed_monetary_reward':sum(x['in_monetary_reward']=='1' for x in unmatched),
         'warning':'No match under these exact queries does not mean absent from OpenAlex; identifiers or indexing may differ.'}
assert summary['pubmed_records_with_at_least_one_openalex_id']==422
assert summary['pubmed_records_without_identifier_match']==85
assert summary['openalex_ids_linked_to_pubmed']==424
assert all(x['screening_status']=='NOT SCREENED' for x in unmatched)
(ROOT/'cross_source_linkage.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
