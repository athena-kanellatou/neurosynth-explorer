"""Check candidate PMIDs against exact source-corpus metadata without screening."""
import csv,gzip,hashlib,json,re,unicodedata
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).parent;OUT=ROOT/'validation_pilot'
NS_URL='https://raw.githubusercontent.com/neurosynth/neurosynth-data/master/data-neurosynth_version-7_metadata.tsv.gz'
NQ_URL='https://osf.io/598tj/download'

def main():
 nsfile=OUT/'neurosynth_v7_metadata.tsv.gz'
 with gzip.open(nsfile,'rt',encoding='utf-8') as f:nsrows=list(csv.DictReader(f,delimiter='\t'))
 ns={r['id'] for r in nsrows}
 nqfile=OUT/'neuroquery_corpus_metadata.csv'
 with nqfile.open(encoding='utf-8',newline='') as f:nqrows=list(csv.DictReader(f))
 nq={r['pmid'] for r in nqrows}
 def title_key(t):return re.sub(r'[^a-z0-9]+',' ',unicodedata.normalize('NFKD',t).casefold()).strip()
 nsdoi={r['doi'].lower().strip() for r in nsrows if r['doi']}
 nstitles={title_key(r['title']) for r in nsrows if r['title']}
 nqtitles={title_key(r['title']) for r in nqrows if r['title']}
 assert len(ns)==14371 and len(nq)==13459
 with (OUT/'merged_unscreened_queue.csv').open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
 for x in rows:
  x['neurosynth_full_corpus_match']=int((bool(x['pmid']) and x['pmid'] in ns) or (bool(x['doi']) and x['doi'].lower() in nsdoi))
  x['neuroquery_model_corpus_match']=int(bool(x['pmid']) and x['pmid'] in nq)
  key=title_key(x['title'])
  x['possible_source_title_match']=int(bool(key) and (key in nstitles or key in nqtitles))
  x['corpus_independence_status']='SOURCE OVERLAP BY ID' if x['neurosynth_full_corpus_match'] or x['neuroquery_model_corpus_match'] else ('POSSIBLE SOURCE TITLE MATCH' if x['possible_source_title_match'] else ('NO PMID/DOI MATCH; COHORT UNVERIFIED' if x['pmid'] else 'UNVERIFIED: NO PMID'))
 out=OUT/'merged_corpus_audit.csv'
 with out.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 log={'checked_utc':datetime.now(timezone.utc).isoformat(),
  'neurosynth_release':'v0.7 (July 2018)','neurosynth_metadata_url':NS_URL,
  'neurosynth_metadata_sha256':hashlib.sha256(nsfile.read_bytes()).hexdigest(),
  'neurosynth_corpus_pmids':len(ns),'neuroquery_model_source':NQ_URL,
  'neuroquery_corpus_metadata_sha256':hashlib.sha256(nqfile.read_bytes()).hexdigest(),
  'neuroquery_model_corpus_pmids':len(nq),'candidate_records':len(rows),
  'with_pmid':sum(bool(x['pmid']) for x in rows),
  'neurosynth_matches':sum(x['neurosynth_full_corpus_match'] for x in rows),
  'neuroquery_matches':sum(x['neuroquery_model_corpus_match'] for x in rows),
  'without_pmid':sum(not x['pmid'] for x in rows),
  'possible_source_title_matches':sum(x['possible_source_title_match'] for x in rows),
  'source_overlaps':[{k:x[k] for k in ['record_key','pmid','doi','title','neurosynth_full_corpus_match','neuroquery_model_corpus_match']} for x in rows if x['neurosynth_full_corpus_match'] or x['neuroquery_model_corpus_match']],
  'sha256_csv':hashlib.sha256(out.read_bytes()).hexdigest(),
  'caveat':'PMID absence does not rule out duplicate cohort or metadata mismatch; no article eligibility screening.'}
 (OUT/'corpus_independence_log.json').write_text(json.dumps(log,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 print(json.dumps({k:log[k] for k in ['candidate_records','with_pmid','neurosynth_matches','neuroquery_matches','without_pmid','possible_source_title_matches']}))
if __name__=='__main__':main()
