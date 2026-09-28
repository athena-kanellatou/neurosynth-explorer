"""Full OpenAlex title/abstract pilot export, with PubMed identifier linkage.

No eligibility decisions. Date and query strings are deliberately frozen for this export.
"""
import csv
import hashlib
import json
import math
import time
from datetime import datetime,timezone
from pathlib import Path
import requests

ROOT=Path(__file__).parent/'validation_pilot'
QUERIES={
 'reappraisal':'("cognitive reappraisal" OR "emotion reappraisal") AND (fMRI OR "functional magnetic resonance imaging")',
 'monetary_reward':'("monetary incentive delay" OR "monetary reward") AND (fMRI OR "functional magnetic resonance imaging")',
}
FIELDS='id,doi,display_name,publication_date,ids,type'
DATE_START='2019-01-01';DATE_END='2026-09-28';SIZE=200

def retrieve(arm,query,page):
 body={'oqo':{'get_rows':'works','filter_rows':[
      {'column_id':'title_and_abstract.search','operator':'has','value':query},
      {'column_id':'from_publication_date','value':DATE_START},
      {'column_id':'to_publication_date','value':DATE_END}]},
      'per_page':SIZE,'page':page,'select':FIELDS}
 for attempt in range(4):
  try:
   r=requests.post('https://api.openalex.org/',json=body,timeout=45)
   if r.status_code in (429,500,502,503,504):time.sleep(2**attempt);continue
   r.raise_for_status();j=r.json();assert 'meta' in j and 'results' in j
   return j,body
  except (requests.RequestException,ValueError,AssertionError):
   if attempt==3:raise
   time.sleep(2**attempt)
 raise RuntimeError(f'Failed {arm} page {page}')

def main():
 pubmed=list(csv.DictReader((ROOT/'narrow_full_queue.csv').open(encoding='utf-8',newline='')))
 by_pmid={r['pmid'] for r in pubmed};by_doi={r['doi'].lower() for r in pubmed if r['doi']}
 records={};log={'retrieved_utc':datetime.now(timezone.utc).isoformat(),
  'database':'OpenAlex','status':'Complete for these title/abstract queries; not screened or protocol-frozen',
  'date_start':DATE_START,'date_end':DATE_END,'search_field':'title_and_abstract.search',
  'query_interface':'OpenAlex OQO POST /','page_size':SIZE,'arms':{}}
 for arm,q in QUERIES.items():
  first,body=retrieve(arm,q,1);count=first['meta']['count'];pages=math.ceil(count/SIZE)
  results=list(first['results'])
  for page in range(2,pages+1):
   j,_=retrieve(arm,q,page)
   if j['meta']['count']!=count:raise RuntimeError(f'Count changed for {arm}')
   results.extend(j['results'])
  if len(results)!=count or len({x['id'] for x in results})!=count:raise RuntimeError(f'Incomplete {arm}')
  log['arms'][arm]={'query':q,'count':count,'pages':pages,'exported':len(results),'body_page_1':body,
                    'server_query_1':first['meta'].get('x_query')}
  for x in results:
   oid=x['id']; ids=x.get('ids') or {}
   if oid not in records:
    records[oid]={'openalex_id':oid,'doi':(x.get('doi') or '').removeprefix('https://doi.org/'),
      'pmid':(ids.get('pmid') or '').removeprefix('https://pubmed.ncbi.nlm.nih.gov/').strip('/'),
      'title':x.get('display_name') or '', 'publication_date':x.get('publication_date') or '',
      'type':x.get('type') or '', 'search_arms':set()}
   records[oid]['search_arms'].add(arm)
  print(arm,count,flush=True)
 rows=[]
 for x in records.values():
  x['search_arms']=';'.join(sorted(x['search_arms']))
  x['in_pubmed_pilot']=int((x['pmid'] in by_pmid if x['pmid'] else False) or (x['doi'].lower() in by_doi if x['doi'] else False))
  x['screening_status']='NOT SCREENED';rows.append(x)
 rows.sort(key=lambda x:x['openalex_id'])
 path=ROOT/'openalex_tiab_export.csv'
 with path.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 log['unique_openalex_ids']=len(rows)
 log['openalex_ids_linked_to_pubmed']=sum(x['in_pubmed_pilot'] for x in rows)
 log['sha256_csv']=hashlib.sha256(path.read_bytes()).hexdigest()
 log['caveat']='Search indexing, field contents and document sets differ from PubMed; title/abstract field restriction does not guarantee identical retrieval.'
 (ROOT/'openalex_tiab_log.json').write_text(json.dumps(log,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 print(json.dumps({'unique':len(rows),'linked_openalex_ids':log['openalex_ids_linked_to_pubmed']}),flush=True)
if __name__=='__main__':main()
