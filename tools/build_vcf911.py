#!/usr/bin/env python3
"""Build the VCF 9.1.1 Design Decisions dataset from 'VCF911 - Design Library.xlsx'.

Usage:
  python3 -I tools/build_vcf911.py <project_dir> <out.json> [--web-ids ids.txt] [--web-only web_only.json]

  --web-ids   text file of DD ids seen on the VCF 9.1.1 TechDocs pages -> source Both/Excel.
              Without it, the May 2026 VCF 9.1 TechDocs scrape (commit ce60acf) is used.
  --web-only  JSON list of web-only DDs ({id, decision, justification, implication, subsection, url, ...})
              appended with source "Web Doc".

delta (new|changed|renumbered, + prev_id) is computed against 'VCF91 - Design Library.xlsx'.
"""
import sys, os, json, argparse, subprocess, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vcf_dd_lib import parse_excel, dd_component, dd_type, compute_delta, finalize  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('project'); ap.add_argument('out')
ap.add_argument('--web-ids'); ap.add_argument('--web-only')
a = ap.parse_args()
P = a.project.rstrip('/') + '/'

if a.web_ids:
    web_ids = {l.strip() for l in open(a.web_ids, encoding='utf-8') if l.strip()}
    web_src = a.web_ids
else:
    old = subprocess.run(['git', '-C', P, 'show', 'ce60acf:index.html'],
                         capture_output=True, text=True, check=True).stdout
    line = next(l for l in old.split('\n') if l.lstrip().startswith("'9.1': ["))
    web_ids = {d['id'] for d in json.loads(line[line.index(': [') + 2:].rstrip().rstrip(',;'))}
    web_src = 'git ce60acf (VCF 9.1 TechDocs scrape)'

rows91 = parse_excel(P + 'VCF91 - Design Library.xlsx')
rows = parse_excel(P + 'VCF911 - Design Library.xlsx')
counts, removed = compute_delta(rows91, rows)
for r in rows:
    r.update(component=dd_component(r['id']), type=dd_type(r['id']),
             source='Both' if r['id'] in web_ids else 'Excel')

n_web = 0
if a.web_only:
    have = {r['id'] for r in rows}
    for w in json.load(open(a.web_only, encoding='utf-8')):
        if w['id'] in have:
            continue
        rows.append(dict(id=w['id'], decision=w['decision'], justification=w.get('justification', ''),
                         implication=w.get('implication', ''), compliant_status='Compliant',
                         criticality='No Risk', notes='', subsection=w.get('subsection', ''),
                         component=dd_component(w['id']), type=dd_type(w['id']), source='Web Doc',
                         delta=w.get('delta', '')))
        have.add(w['id']); n_web += 1

data = finalize(rows)
C = collections.Counter
report = dict(total=len(data), unique_ids=len({d['id'] for d in data}), web_only_added=n_web,
              source_basis=web_src, delta=counts,
              removed_vs_91=[{'id': r['id'], 'decision': r['decision'][:120]} for r in removed],
              type=C(d['type'] for d in data), source=C(d['source'] for d in data),
              component=C(d['component'] for d in data), sections=len({d['subsection'] for d in data}),
              dup_ids=sorted(i for i, c in C(d['id'] for d in data).items() if c > 1))
with open(a.out, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
with open(os.path.splitext(a.out)[0] + '_report.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in report.items() if k != 'removed_vs_91'}, ensure_ascii=False, indent=1))
print('removed vs 9.1:', len(removed))
