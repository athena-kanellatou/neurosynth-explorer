"""Merge two unscreened source exports by PMID/DOI; flag known term-map IDs."""
import csv,json,hashlib
from pathlib import Path
ROOT=Path(__file__).parent
P=ROOT/'validation_pilot'
pr=list(csv.DictReader((P/'narrow_full_queue.csv').open(encoding='utf-8',newline='')))
orows=list(csv.DictReader((P/'openalex_tiab_export.csv').open(encoding='utf-8',newline='')))
terms=json.loads((ROOT/'results/study_id_sets.json').read_text())['study_ids']
by_pmid={r['pmid']:r for r in pr}
by_doi={r['doi'].lower():r for r in pr if r['doi']}
groups={r['pmid']:{'pmid':r['pmid'],'doi':r['doi'],'title':r['title'],'publication_date':r['pubdate'],
 'pubmed':1,'openalex_ids':[],'pubmed_arm_reappraisal':r['in_reappraisal'],
 'pubmed_arm_reward':r['in_monetary_reward'],'openalex_arms':set(),
 'neurosynth_term_map_ids':set(k for k,v in terms.items() if r['pmid'] in v),
 'screening_status':'NOT SCREENED','independence_status':'UNVERIFIED'} for r in pr}
new_by_doi={}
for x in orows:
 pmid=x['pmid'];doi=x['doi'].lower()
 match=by_pmid.get(pmid) if pmid else None
 if match is None and doi: match=by_doi.get(doi)
 if match is not None:key=match['pmid']
 elif doi and doi in new_by_doi:key=new_by_doi[doi]
 else:
  key=x['openalex_id']
  groups[key]={'pmid':pmid,'doi':x['doi'],'title':x['title'],'publication_date':x['publication_date'],
   'pubmed':0,'openalex_ids':[],'pubmed_arm_reappraisal':'','pubmed_arm_reward':'',
   'openalex_arms':set(),'neurosynth_term_map_ids':set(k for k,v in terms.items() if pmid and pmid in v),
   'screening_status':'NOT SCREENED','independence_status':'UNVERIFIED'}
  if doi:new_by_doi[doi]=key
 groups[key]['openalex_ids'].append(x['openalex_id'])
 groups[key]['openalex_arms'].update(x['search_arms'].split(';'))
rows=[]
for key,g in groups.items():
 g['record_key']=key
 g['openalex_ids']=';'.join(sorted(g['openalex_ids']))
 g['openalex_arms']=';'.join(sorted(g['openalex_arms']))
 g['neurosynth_term_map_ids']=';'.join(sorted(g['neurosynth_term_map_ids']))
 rows.append(g)
rows.sort(key=lambda r:(not bool(r['pubmed']),r['record_key']))
assert len(rows)==731
assert sum(bool(r['neurosynth_term_map_ids']) for r in rows)==1
assert all(r['screening_status']=='NOT SCREENED' for r in rows)
out=P/'merged_unscreened_queue.csv'
with out.open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
log={'source_pubmed_records':len(pr),'source_openalex_ids':len(orows),
 'merged_identifier_groups':len(rows),'both_sources':sum(r['pubmed'] and bool(r['openalex_ids']) for r in rows),
 'pubmed_only':sum(r['pubmed'] and not r['openalex_ids'] for r in rows),
 'openalex_only':sum(not r['pubmed'] for r in rows),
 'neurosynth_three_term_map_matches':[{k:r[k] for k in ['record_key','pmid','doi','title','neurosynth_term_map_ids']} for r in rows if r['neurosynth_term_map_ids']],
 'full_neurosynth_corpus_membership':'UNVERIFIED','neuroquery_corpus_membership':'UNVERIFIED',
 'bibliographic_duplicate_review':'PENDING','cohort_duplicate_review':'PENDING',
 'screening':'NOT STARTED','sha256_csv':hashlib.sha256(out.read_bytes()).hexdigest()}
(P/'merged_queue_log.json').write_text(json.dumps(log,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({k:log[k] for k in ['merged_identifier_groups','both_sources','pubmed_only','openalex_only','neurosynth_three_term_map_matches']}))
