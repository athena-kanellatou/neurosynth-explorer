"""Audit overlap of study identifiers assigned to Neurosynth terms."""
import csv
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import urlopen

TERMS = {'emotion_regulation': 498, 'reward': 46, 'depression': 772}
root = Path(__file__).parent
out = root/'results'

def fetch(item):
    name, number = item
    url = f'https://neurosynth.org/api/analyses/{number}/studies?dt=1&start=0&length=2000&draw=1'
    raw = json.load(urlopen(url, timeout=40))['data']
    studies = {}
    for row in raw:
        match = re.search(r'/studies/(\d+)/', row[0])
        if not match:
            raise ValueError('Unexpected study link format')
        studies[match.group(1)] = re.sub(r'<[^>]*>', '', row[0])
    if len(studies) != len(raw):
        raise ValueError('Duplicate study identifiers')
    return name, studies, url

def main():
    with ThreadPoolExecutor(max_workers=3) as pool:
        items = list(pool.map(fetch, TERMS.items()))
    data = {name: studies for name, studies, _ in items}
    rows = []
    names = list(TERMS)
    for i, a in enumerate(names):
        for b in names[i+1:]:
            left, right = set(data[a]), set(data[b])
            shared = left & right
            rows.append({'term_a':a,'term_b':b,'a_studies':len(left),'b_studies':len(right),
                         'shared_studies':len(shared),'shared_fraction_of_a':round(len(shared)/len(left),4),
                         'shared_fraction_of_b':round(len(shared)/len(right),4),
                         'jaccard_study_ids':round(len(shared)/len(left|right),4)})
    with (out/'study_overlap.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    (out/'study_id_sets.json').write_text(json.dumps({'sources':{name:url for name,_,url in items},
        'study_ids':{name:sorted(studies) for name,studies,_ in items}},indent=2),encoding='utf-8')
    for row in rows: print(row)

if __name__ == '__main__': main()
