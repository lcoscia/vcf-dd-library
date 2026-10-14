#!/usr/bin/env python3
"""Splice / maintain the datasets embedded in index.html (idempotent).

Usage:
  python3 -I -B tools/update_index.py index.html --v911 vcf911.json \
      [--v91-excel "VCF91 - Design Library.xlsx" --web-ids tools/data/web_ids_91x.txt] \
      [--web-only-91 tools/data/web_only_91.json] [--drop-parasites] \
      [--vdefend-blueprint tools/data/vdefend_blueprint_ids.txt] [--out out.html]

Steps (in this order):
 1. --drop-parasites : remove "Web Doc" rows whose id is not a real DD id (scrape artifacts such as
                       "Design Choice", "Requirements ID", or sentences) from 9.0, 9.1 and 9.1.1.
 2. --v91-excel      : 9.1 reimport. The embedded 9.1 Excel rows are a prefix of the Excel (the original
                       import stopped at Excel row 1184). The missing tail is parsed with the tools/ rules
                       (component, type, cleaned section, source Both/Excel against --web-ids) and inserted
                       after the existing Excel rows; "Web Doc" rows with the same id are superseded.
 3. 9.1 type rule    : `type` recomputed with dd_type(); vDefend / License Hub prefixes re-mapped.
 4. --web-only-91    : web-only 9.1 DDs appended as "Web Doc" (deduplicated by id).
 5. --v911           : `VCF_VERSIONS['9.1.1']` replaced by the given dataset.
 6. --vdefend-blueprint : BLUEPRINT_DATA["Lateral Security with vDefend Blueprint"] filled with the 9.1.1
                       records of the listed ids (TechDocs blueprint order, first occurrence of each id).
 `_uid` is renumbered sequentially in every array that was touched.
"""
import sys, os, json, argparse, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vcf_dd_lib import dd_component, dd_type, parse_excel, KEYS  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('index'); ap.add_argument('--v911', required=True)
ap.add_argument('--v91-excel'); ap.add_argument('--web-ids')
ap.add_argument('--web-only-91'); ap.add_argument('--drop-parasites', action='store_true')
ap.add_argument('--vdefend-blueprint'); ap.add_argument('--out')
a = ap.parse_args()

lines = open(a.index, encoding='utf-8').read().split('\n')
dump = lambda d: json.dumps(d, ensure_ascii=False, separators=(',', ':'))
REAL_ID = re.compile(r'^[A-Z][A-Z0-9]*(-[A-Za-z0-9_]+)+$')
REMAP = re.compile(r'^(SEC|MDS|SSP|WDS|DVP|LH)-')
report = {}


def find(prefix):
    idx = [n for n, l in enumerate(lines) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx)
    return idx[0]


def load(n, cut):
    l = lines[n]
    return json.loads(l[l.index(cut) + len(cut) - 1:].rstrip().rstrip(',;'))


def renum(arr):
    for i, d in enumerate(arr):
        d['_uid'] = i
    return arr


def drop_parasites(arr, name):
    keep = [d for d in arr if d.get('source') != 'Web Doc' or REAL_ID.match(d['id'])]
    gone = [d['id'] for d in arr if d not in keep]
    if gone:
        report.setdefault('parasites_removed', {})[name] = gone
    return keep


def web_row(w):
    return dict(id=w['id'], decision=w['decision'], justification=w.get('justification', ''),
                implication=w.get('implication', ''), compliant_status='Compliant', criticality='No Risk',
                notes='', subsection=w.get('subsection', ''), component=dd_component(w['id']),
                type=dd_type(w['id']), source='Web Doc')


# ---- 9.0 (only parasite cleanup) ----
i90 = find('const EMBEDDED_DATA = [')
if a.drop_parasites:
    d90 = drop_parasites(load(i90, '= ['), '9.0')
    lines[i90] = 'const EMBEDDED_DATA = ' + dump(renum(d90)) + ';'

# ---- 9.1 ----
i91 = find("  '9.1': [")
tail = ',' if lines[i91].rstrip().endswith(',') else ''
d91 = load(i91, ': [')
if a.drop_parasites:
    d91 = drop_parasites(d91, '9.1')
if a.v91_excel:
    web_ids = {l.strip() for l in open(a.web_ids, encoding='utf-8') if l.strip() and not l.startswith('#')}
    xl = parse_excel(a.v91_excel)
    excel_rows = [d for d in d91 if d.get('source') != 'Web Doc']
    web_rows = [d for d in d91 if d.get('source') == 'Web Doc']
    assert [d['id'] for d in excel_rows] == [r['id'] for r in xl[:len(excel_rows)]], \
        'embedded 9.1 Excel rows are not a prefix of the 9.1 Excel'
    missing = xl[len(excel_rows):]
    for r in missing:
        r.update(component=dd_component(r['id']), type=dd_type(r['id']),
                 source='Both' if r['id'] in web_ids else 'Excel')
    miss_ids = {r['id'] for r in missing}
    superseded = [d['id'] for d in web_rows if d['id'] in miss_ids]
    web_rows = [d for d in web_rows if d['id'] not in miss_ids]
    d91 = excel_rows + missing + web_rows
    report['9.1_reimported'] = len(missing)
    report['9.1_webdoc_superseded_by_excel'] = len(superseded)
for d in d91:
    d['type'] = dd_type(d['id'])
    if REMAP.match(d['id']):
        d['component'] = dd_component(d['id'])
if a.web_only_91:
    have = {d['id'] for d in d91}
    n = 0
    for w in json.load(open(a.web_only_91, encoding='utf-8')):
        if w['id'] not in have:
            d91.append(web_row(w)); have.add(w['id']); n += 1
    report['9.1_web_added'] = n
d91 = [{k: d.get(k, '') for k in KEYS} for d in d91]
lines[i91] = "  '9.1': " + dump(renum(d91)) + tail

# ---- 9.1.1 ----
d911 = json.load(open(a.v911, encoding='utf-8'))
if a.drop_parasites:
    d911 = drop_parasites(d911, '9.1.1')
renum(d911)
i11 = find("VCF_VERSIONS['9.1.1'] = ")
lines[i11] = "VCF_VERSIONS['9.1.1'] = " + dump(d911) + ';'
c = i11 - 2
if lines[c].startswith('// VCF 9.1.1 is a maintenance release'):
    lines[c:c + 2] = ["// VCF 9.1.1 — own dataset built from 'VCF911 - Design Library.xlsx' with tools/build_vcf911.py",
                      "// (delta/prev_id = changes vs VCF 9.1). Blueprints are shared with 9.1."]

# ---- vDefend blueprint ----
if a.vdefend_blueprint:
    ids = [l.strip() for l in open(a.vdefend_blueprint, encoding='utf-8') if l.strip() and not l.startswith('#')]
    first = {}
    for d in d911:
        first.setdefault(d['id'], d)
    bp = []
    for i in ids:
        if i in first:
            rec = {k: v for k, v in first[i].items() if k not in ('delta', 'prev_id')}
            bp.append({k: rec.get(k, '') for k in KEYS})
    ib = find('  "Lateral Security with vDefend Blueprint": [')
    lines[ib] = '  "Lateral Security with vDefend Blueprint": ' + dump(renum(bp)) + ','
    report['vdefend_blueprint'] = len(bp)
    report['vdefend_blueprint_missing_ids'] = [i for i in ids if i not in first]

open(a.out or a.index, 'w', encoding='utf-8').write('\n'.join(lines))
report.update({'9.0': None if not a.drop_parasites else len(d90), '9.1': len(d91), '9.1.1': len(d911)})
print(json.dumps(report, ensure_ascii=False, indent=1))
