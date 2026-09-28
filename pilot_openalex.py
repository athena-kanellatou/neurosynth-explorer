"""Bounded OpenAlex retrieval pilot; not a complete systematic search."""
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
import requests

ROOT = Path(__file__).parent
OUT = ROOT / 'validation_pilot'
SEARCHES = {
    'cognitive_reappraisal': '"cognitive reappraisal" fMRI',
    'emotion_reappraisal': '"emotion reappraisal" fMRI',
    'monetary_incentive_delay': '"monetary incentive delay" fMRI',
    'monetary_reward': '"monetary reward" fMRI',
}
BASE = 'https://api.openalex.org/works'
FILTER = 'from_publication_date:2019-01-01,to_publication_date:2026-09-28'
FIELDS = 'id,doi,display_name,publication_date,ids,type'


def main():
    pubmed = list(csv.DictReader((OUT/'narrow_full_queue.csv').open(newline='', encoding='utf-8')))
    pmids = {r['pmid'] for r in pubmed if r['pmid']}
    dois = {r['doi'].lower().removeprefix('https://doi.org/') for r in pubmed if r['doi']}
    records = {}
    log = {'retrieved_utc': datetime.now(timezone.utc).isoformat(), 'database': 'OpenAlex',
           'status': 'One relevance-ranked page per query only; incomplete feasibility pilot, not screening',
           'search_scope': 'OpenAlex search may search full text in addition to title and abstract',
           'filter': FILTER, 'page_size': 200, 'searches': {}}
    for arm, query in SEARCHES.items():
        params = {'search':query,'filter':FILTER,'per_page':200,'page':1,'select':FIELDS}
        response = requests.get(BASE,params=params,timeout=45)
        response.raise_for_status()
        data=response.json()
        hits=data['results']; count=data['meta']['count']
        log['searches'][arm]={'query':query,'request_url':response.url,'reported_count':count,
                              'retrieved_count':len(hits),'complete':len(hits)==count}
        for item in hits:
            identifier=item['id']
            if identifier not in records:
                ids=item.get('ids') or {}
                records[identifier]={'openalex_id':identifier,'doi':(item.get('doi') or '').removeprefix('https://doi.org/'),
                                     'pmid':(ids.get('pmid') or '').removeprefix('https://pubmed.ncbi.nlm.nih.gov/').strip('/'),
                                     'title':item.get('display_name') or '', 'publication_date':item.get('publication_date') or '',
                                     'type':item.get('type') or '', 'search_arms':set()}
            records[identifier]['search_arms'].add(arm)
    rows=[]
    for item in records.values():
        item['search_arms']=';'.join(sorted(item['search_arms']))
        item['in_pubmed_pilot']=int(bool((item['pmid'] and item['pmid'] in pmids) or (item['doi'] and item['doi'].lower() in dois)))
        item['screening_status']='NOT SCREENED'
        rows.append(item)
    rows.sort(key=lambda x:x['openalex_id'])
    log['unique_exported_records']=len(rows)
    log['matched_to_pubmed_pilot_by_pmid_or_doi']=sum(r['in_pubmed_pilot'] for r in rows)
    log['warning']='These are only first-page results, with search semantics different from PubMed. Counts and matches do not support a PRISMA flow or eligibility claims.'
    with (OUT/'openalex_first_page.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (OUT/'openalex_pilot_log.json').write_text(json.dumps(log,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'counts':{k:v['reported_count'] for k,v in log['searches'].items()},
                      'unique_exported':len(rows),'matched_pubmed':log['matched_to_pubmed_pilot_by_pmid_or_doi']}))

if __name__=='__main__':main()
