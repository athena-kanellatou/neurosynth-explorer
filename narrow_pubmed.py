"""Export the complete narrow PubMed search records for future screening."""
import csv
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

root=Path(__file__).parent
out=root/'validation_pilot';out.mkdir(exist_ok=True)
period='2019/01/01:2026/09/28[dp]'
queries={
 'cognitive_reappraisal':f'("cognitive reappraisal"[tiab] OR "emotion reappraisal"[tiab]) AND (fMRI[tiab] OR "functional magnetic resonance imaging"[tiab]) AND ({period})',
 'monetary_reward':f'("monetary incentive delay"[tiab] OR "monetary reward"[tiab]) AND (fMRI[tiab] OR "functional magnetic resonance imaging"[tiab]) AND ({period})',
}
base='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
def get(endpoint,params):
    return json.load(urlopen(base+endpoint+'?'+urlencode(params),timeout=40))
log={};ids_by_arm={}
for arm,query in queries.items():
    result=get('esearch.fcgi',{'db':'pubmed','term':query,'retmode':'json','retmax':1000,'sort':'relevance'})['esearchresult']
    ids=result['idlist'];count=int(result['count'])
    if len(ids)!=count: raise RuntimeError(f'Incomplete retrieval for {arm}: {len(ids)}/{count}')
    ids_by_arm[arm]=ids
    log[arm]={'query':query,'count':count,'retrieved':len(ids),'sort':'relevance'}
unique=list(dict.fromkeys(pmid for ids in ids_by_arm.values() for pmid in ids))
records={}
for offset in range(0,len(unique),150):
    ids=unique[offset:offset+150]
    data=get('esummary.fcgi',{'db':'pubmed','id':','.join(ids),'retmode':'json'})['result']
    for pmid in ids:
        item=data[pmid]
        doi=next((x.get('value','') for x in item.get('articleids',[]) if x.get('idtype')=='doi'),'')
        records[pmid]={'pmid':pmid,'doi':doi,'title':item.get('title',''),
                       'pubdate':item.get('pubdate',''),'journal':item.get('fulljournalname',''),
                       'in_reappraisal':int(pmid in ids_by_arm['cognitive_reappraisal']),
                       'in_monetary_reward':int(pmid in ids_by_arm['monetary_reward']),
                       'screening_status':'NOT SCREENED','decision_reason':'',
                       'pubmed_url':f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/'}
with (out/'narrow_full_queue.csv').open('w',newline='',encoding='utf-8') as f:
    writer=csv.DictWriter(f,fieldnames=next(iter(records.values())).keys())
    writer.writeheader();writer.writerows(records.values())
(out/'narrow_search_log.json').write_text(json.dumps({'date':'2026-09-28',
    'status':'Pilot export; no eligibility screening or independent validation yet',
    'queries':log,'unique_pmids':len(unique),
    'overlap_between_search_arms':len(set(ids_by_arm['cognitive_reappraisal'])&set(ids_by_arm['monetary_reward']))},indent=2),encoding='utf-8')
print('Arm counts:',{a:len(ids) for a,ids in ids_by_arm.items()},'unique:',len(unique))
