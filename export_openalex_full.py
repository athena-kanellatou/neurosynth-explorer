"""Complete, checkpointed export of the four documented OpenAlex searches.

Searches title, abstract and available full text. No article screening occurs.
"""
import csv
import hashlib
import json
import math
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
import requests

ROOT=Path(__file__).parent/'validation_pilot'
CACHE=ROOT/'openalex_pages'
CACHE.mkdir(exist_ok=True)
SEARCHES={'cognitive_reappraisal':'"cognitive reappraisal" fMRI',
          'emotion_reappraisal':'"emotion reappraisal" fMRI',
          'monetary_incentive_delay':'"monetary incentive delay" fMRI',
          'monetary_reward':'"monetary reward" fMRI'}
BASE='https://api.openalex.org/works'
DATE_FILTER='from_publication_date:2019-01-01,to_publication_date:2026-09-28'
SELECT='id,doi,display_name,publication_date,ids,type'
PAGE_SIZE=200

def fetch(arm,query,page):
    filename=CACHE/f'{arm}_{page:03}.json'
    if filename.exists():return json.loads(filename.read_text())
    params={'search':query,'filter':DATE_FILTER,'per_page':PAGE_SIZE,'page':page,'select':SELECT}
    for attempt in range(5):
        try:
            r=requests.get(BASE,params=params,timeout=55)
            if r.status_code in (429,500,502,503,504):
                time.sleep(2**attempt);continue
            r.raise_for_status(); data=r.json()
            assert 'results' in data and 'meta' in data
            snapshot={'request_url':r.url,'count':data['meta']['count'],'results':data['results']}
            filename.write_text(json.dumps(snapshot,ensure_ascii=False),encoding='utf-8')
            return snapshot
        except (requests.RequestException,ValueError,AssertionError):
            if attempt==4:raise
            time.sleep(2**attempt)
    raise RuntimeError(f'OpenAlex unavailable for {arm} page {page}')

def main():
    first={arm:fetch(arm,q,1) for arm,q in SEARCHES.items()}
    jobs=[(arm,q,p) for arm,q in SEARCHES.items() for p in range(2,math.ceil(first[arm]['count']/PAGE_SIZE)+1)]
    print('remaining pages',len(jobs),flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures=[pool.submit(fetch,*job) for job in jobs]
        for i,f in enumerate(as_completed(futures),1):
            f.result()
            if i%10==0:print('fetched',i,'/',len(jobs),flush=True)
    pubmed=list(csv.DictReader((ROOT/'narrow_full_queue.csv').open(newline='',encoding='utf-8')))
    pmids={r['pmid'] for r in pubmed if r['pmid']}
    dois={r['doi'].lower().removeprefix('https://doi.org/') for r in pubmed if r['doi']}
    records={};log={'retrieved_utc':datetime.now(timezone.utc).isoformat(),'database':'OpenAlex',
                    'scope':'Complete export of four fulltext-inclusive searches, not eligibility screening',
                    'filter':DATE_FILTER,'page_size':PAGE_SIZE,'select':SELECT,'arms':{}}
    for arm,q in SEARCHES.items():
        count=first[arm]['count'];pages=math.ceil(count/PAGE_SIZE);found=0;ids=set()
        for page in range(1,pages+1):
            snapshot=json.loads((CACHE/f'{arm}_{page:03}.json').read_text())
            if snapshot['count']!=count:raise RuntimeError(f'Count changed during export: {arm} page {page}')
            found+=len(snapshot['results'])
            for x in snapshot['results']:
                oid=x['id']
                if oid in ids:raise RuntimeError(f'Duplicate ID within arm {arm}: {oid}')
                ids.add(oid)
                if oid not in records:
                    i=x.get('ids') or {}
                    records[oid]={'openalex_id':oid,'doi':(x.get('doi') or '').removeprefix('https://doi.org/'),
                                  'pmid':(i.get('pmid') or '').removeprefix('https://pubmed.ncbi.nlm.nih.gov/').strip('/'),
                                  'title':x.get('display_name') or '', 'publication_date':x.get('publication_date') or '',
                                  'type':x.get('type') or '', 'search_arms':set()}
                records[oid]['search_arms'].add(arm)
        if found!=count:raise RuntimeError(f'Incomplete export for {arm}: {found}/{count}')
        log['arms'][arm]={'query':q,'count':count,'pages':pages,'exported':found,
                          'first_request_url':first[arm]['request_url'],'complete':True}
    rows=[]
    for x in records.values():
        x['search_arms']=';'.join(sorted(x['search_arms']))
        x['in_pubmed_pilot']=int((x['pmid'] in pmids if x['pmid'] else False) or (x['doi'].lower() in dois if x['doi'] else False))
        x['screening_status']='NOT SCREENED'
        rows.append(x)
    rows.sort(key=lambda x:x['openalex_id'])
    out=ROOT/'openalex_full_export.csv'
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    log['unique_openalex_ids']=len(rows)
    log['matched_to_pubmed_pilot_by_pmid_or_doi']=sum(x['in_pubmed_pilot'] for x in rows)
    log['sha256_csv']=hashlib.sha256(out.read_bytes()).hexdigest()
    log['warning']='Complete for these OpenAlex API queries only; full-text-inclusive scope differs from PubMed tiab, no screening, no final protocol freeze.'
    (ROOT/'openalex_full_log.json').write_text(json.dumps(log,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'arm_counts':{k:v['count'] for k,v in log['arms'].items()},
                      'unique':len(rows),'pubmed_pilot_matches':log['matched_to_pubmed_pilot_by_pmid_or_doi']}),flush=True)

if __name__=='__main__':main()
