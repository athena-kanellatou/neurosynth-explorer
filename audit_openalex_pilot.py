"""Descriptive metadata audit of the bounded OpenAlex export; never screens studies."""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).parent/'validation_pilot'
rows=list(csv.DictReader((ROOT/'openalex_first_page.csv').open(encoding='utf-8',newline='')))
terms={'cognitive_reappraisal':'cognitive reappraisal','emotion_reappraisal':'emotion reappraisal',
       'monetary_incentive_delay':'monetary incentive delay','monetary_reward':'monetary reward'}
report={'scope':'First page per OpenAlex query only; title string audit is not eligibility screening',
        'unique_records':len(rows),'with_doi':sum(bool(r['doi']) for r in rows),
        'with_pmid':sum(bool(r['pmid']) for r in rows),
        'without_doi_or_pmid':sum(not r['doi'] and not r['pmid'] for r in rows),
        'matched_to_pubmed_pilot':sum(int(r['in_pubmed_pilot']) for r in rows),
        'openalex_types':dict(sorted(Counter(r['type'] for r in rows).items())),
        'arms':{}}
for arm, phrase in terms.items():
    subset=[r for r in rows if arm in r['search_arms'].split(';')]
    report['arms'][arm]={'exported_records':len(subset),
        'title_contains_exact_phrase':sum(phrase in r['title'].casefold() for r in subset),
        'title_mentions_fmri_or_full_name':sum('fmri' in r['title'].casefold() or 'functional magnetic resonance imaging' in r['title'].casefold() for r in subset),
        'matched_to_pubmed_pilot':sum(int(r['in_pubmed_pilot']) for r in subset)}
assert report['unique_records']==715
assert report['matched_to_pubmed_pilot']==243
(ROOT/'openalex_metadata_audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
