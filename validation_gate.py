"""Refuse to claim independent validation without verified experiment-level data."""
import csv
import json
from pathlib import Path

ROOT=Path(__file__).parent
P=ROOT/'validation_pilot'
queue=list(csv.DictReader((P/'merged_corpus_audit.csv').open(encoding='utf-8',newline='')))
coordinate_file=P/'validation_coordinates.csv'
experiments=[]
if coordinate_file.exists():
    experiments=list(csv.DictReader(coordinate_file.open(encoding='utf-8',newline='')))
required={'experiment_id','domain','cohort_id','n_subjects','x','y','z','space','source_table'}
errors=[]
if not coordinate_file.exists():errors.append('No verified coordinate extraction file exists')
elif not required.issubset(experiments[0].keys() if experiments else set()):errors.append('Coordinate file lacks required columns')
if any(r['screening_status']=='NOT SCREENED' for r in queue):errors.append('Candidate queue still contains unscreened records')
if any(r['corpus_independence_status'] in ('POSSIBLE SOURCE TITLE MATCH','UNVERIFIED: NO PMID') for r in queue):
    errors.append('Some candidate records have unresolved source-corpus identity')
counts={}
for domain in ('reappraisal','monetary_reward'):
    counts[domain]=len({r['experiment_id'] for r in experiments if r.get('domain')==domain})
    if counts[domain]<17:errors.append(f'{domain}: {counts[domain]} extracted experiments, minimum 17')
report={'status':'BLOCKED' if errors else 'REQUIRES MANUAL AUDIT BEFORE RUN',
        'candidate_records':len(queue),'unscreened':sum(r['screening_status']=='NOT SCREENED' for r in queue),
        'corpus_matches_by_id':sum(r['corpus_independence_status']=='SOURCE OVERLAP BY ID' for r in queue),
        'possible_source_title_matches':sum(r['corpus_independence_status']=='POSSIBLE SOURCE TITLE MATCH' for r in queue),
        'without_pmid':sum(not r['pmid'] for r in queue),
        'experiment_counts':counts,'blocking_reasons':errors,
        'statement':'No ALE or independent validation result has been produced.'}
(P/'VALIDATION_READINESS.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
if errors:raise SystemExit(2)
