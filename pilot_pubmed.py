"""Record a transparent PubMed pilot search; do not label records as eligible."""
import csv
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

root=Path(__file__).parent
out=root/'validation_pilot';out.mkdir(exist_ok=True)
window='2019/01/01:2026/09/28[dp]'
queries={
 'emotion_regulation':f'("emotion regulation"[tiab] OR reappraisal[tiab] OR downregulation[tiab]) AND (fMRI[tiab] OR "functional magnetic resonance imaging"[tiab]) AND ({window})',
 'reward':f'(reward[tiab] OR "monetary incentive"[tiab] OR reinforcement[tiab]) AND (fMRI[tiab] OR "functional magnetic resonance imaging"[tiab]) AND ({window})',
}
base='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
def get(endpoint,params):
    return json.load(urlopen(base+endpoint+'?'+urlencode(params),timeout=30))
records=[];log={}
for domain,query in queries.items():
    data=get('esearch.fcgi',{'db':'pubmed','term':query,'retmode':'json','retmax':25,'sort':'relevance'})['esearchresult']
    ids=data['idlist']
    log[domain]={'query':query,'database':'PubMed','count':int(data['count']),
                 'returned_count':len(ids),'sort':'relevance','pmids':ids}
    details=get('esummary.fcgi',{'db':'pubmed','id':','.join(ids),'retmode':'json'})['result']
    for pmid in ids:
        item=details[pmid]
        records.append({'domain_search':domain,'pmid':pmid,'title':item.get('title',''),
                        'pubdate':item.get('pubdate',''),'journal':item.get('fulljournalname',''),
                        'article_ids':'; '.join(f"{x.get('idtype')}:{x.get('value')}" for x in item.get('articleids',[])),
                        'screening_status':'NOT SCREENED','decision_reason':'',
                        'pubmed_url':f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/'})
with (out/'candidate_queue.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=records[0].keys());w.writeheader();w.writerows(records)
(out/'search_log.json').write_text(json.dumps({'search_date':'2026-09-28','queries':log,
    'status':'Pilot feasibility search. First 25 relevance-sorted records per query, not a complete review.'},indent=2),encoding='utf-8')
print({name:info['count'] for name,info in log.items()},'queued:',len(records))
