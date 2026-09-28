"""Verify the bundled research snapshot against source hashes and recomputation."""
import csv
import json
from pathlib import Path
import numpy as np
from analysis import load_map, compare

root=Path(__file__).parent
results=root/'results'
provenance=json.loads((results/'provenance.json').read_text(encoding='utf-8'))
neuroquery=json.loads((results/'neuroquery_provenance.json').read_text(encoding='utf-8'))
checks=[]

def check(name,condition,detail=''):
    checks.append({'check':name,'status':'PASS' if condition else 'FAIL','detail':detail})

maps={}
for term,meta in provenance['inputs'].items():
    item=load_map(root/'data'/f'{term}.nii.gz')
    maps[term]=item
    check(f'Neurosynth {term} SHA-256',item.sha256==meta['sha256'])
    check(f'Neurosynth {term} geometry',list(item.array.shape)==meta['shape'] and
          np.allclose(item.affine,meta['affine'],atol=1e-4,rtol=0))

for term,meta in neuroquery['maps'].items():
    key=term.replace(' ','_')
    item=load_map(root/meta['path'])
    check(f'NeuroQuery {key} SHA-256',item.sha256==meta['sha256'])
    check(f'NeuroQuery {key} geometry',list(item.array.shape)==meta['shape'] and
          np.allclose(item.affine,meta['affine'],atol=1e-4,rtol=0))

with (results/'overlap.csv').open(encoding='utf-8') as f:
    rows=list(csv.DictReader(f))
for row in rows:
    actual=compare(maps[row['term_a']],maps[row['term_b']],[float(row['threshold_z'])])[0]
    for field in ('a_voxels','b_voxels','shared_voxels'):
        check(f"{row['term_a']} x {row['term_b']} z={row['threshold_z']} {field}",
              actual[field]==int(row[field]))
    for field in ('jaccard','dice'):
        check(f"{row['term_a']} x {row['term_b']} z={row['threshold_z']} {field}",
              abs(actual[field]-float(row[field]))<1e-12)

study_sets=json.loads((results/'study_id_sets.json').read_text(encoding='utf-8'))['study_ids']
with (results/'study_overlap.csv').open(encoding='utf-8') as f:
    for row in csv.DictReader(f):
        a,b=set(study_sets[row['term_a']]),set(study_sets[row['term_b']])
        check(f"{row['term_a']} x {row['term_b']} shared study IDs",
              len(a&b)==int(row['shared_studies']) and len(a)==int(row['a_studies']) and len(b)==int(row['b_studies']))

report={'checks':checks,'passed':sum(c['status']=='PASS' for c in checks),
        'failed':sum(c['status']=='FAIL' for c in checks),
        'scope':'Offline integrity and numerical checks. Atlas labels need the AAL source; NeuroQuery maps need the pretrained model to regenerate from text.'}
(results/'REPRODUCTION_AUDIT.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(f"{report['passed']} passed, {report['failed']} failed")
if report['failed']:
    for item in checks:
        if item['status']=='FAIL': print(item)
    raise SystemExit(1)
