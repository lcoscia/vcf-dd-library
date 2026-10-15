"""Shared helpers for building the VCF Design Decision datasets embedded in index.html.

The rules here mirror the JS helpers ddComponent()/ddType() used by the in-app Excel import.
Requires openpyxl (pip install openpyxl).
"""
import re, sys, site, difflib

# User site-packages is skipped under `python3 -I`; add it back so a user-installed openpyxl is found
_p = site.getusersitepackages()
if _p not in sys.path:
    sys.path.append(_p)
import openpyxl  # noqa: E402

# ID token -> component (VCF 9.1 taxonomy + 9.1.1 additions)
COMP = {
    'CLS': 'vSphere Cluster', 'ESX': 'ESX', 'VCS': 'vCenter', 'WLD': 'Workload Domain',
    'VSAN': 'Storage', 'FC': 'Storage', 'NFS': 'Storage',
    'NET': 'vSphere Networking', 'VDS': 'vSphere Networking',
    'WLDCON': 'Workload Connectivity', 'VNI': 'Workload Connectivity', 'VN': 'Workload Connectivity',
    'NSX': 'NSX', 'EDGE': 'NSX Edge', 'VNA': 'NSX VNA',
    'AVI': 'Load Balancing', 'FLB': 'Load Balancing',
    'OPS': 'Operations', 'LOGS': 'Operations', 'SDDCM': 'Operations',
    'MGMT': 'Management Services', 'MS': 'Management Services',
    'AUTO': 'Automation', 'SUP': 'IaaS', 'PC': 'Data Services Manager',
    'SSO': 'SSO', 'SEC': 'Security', 'LIC': 'Licensing',
    'BCK': 'Backup', 'PB': 'Live Recovery',
    'MDS': 'vDefend', 'SSP': 'vDefend', 'WDS': 'vDefend', 'DVP': 'vDefend',
    'LH': 'License Hub', 'PAIF': 'Private AI',
    'NECE': 'Operations',   # VCF Operations for Networks
}

KEYS = ['_uid', 'id', 'decision', 'justification', 'implication', 'compliant_status',
        'criticality', 'notes', 'subsection', 'component', 'type', 'source']


def comp_key(i):
    p = i.split('-')
    return p[1] if p[0] == 'VCF' and len(p) > 1 else p[0]


def dd_component(i):
    if i.split('-')[0] == 'SEC':      # non-VCF SEC-* rows are vDefend; VCF-SEC-* stays "Security"
        return 'vDefend'
    k = comp_key(i)
    return COMP.get(k, k)


def dd_type(i):
    toks = [t for part in i.split('-') for t in part.split('_')]
    if 'REQD' in toks:
        return 'Requirement'
    if 'RECD' in toks or 'RCMD' in toks:
        return 'Recommendation'
    return 'Choice'


def clean_section(s):
    s = re.sub(r'\s+', ' ', s).strip()
    s = s.replace('Requierements', 'Requirements')
    s = re.sub(r'(9\.1\.\d)(?=[A-Za-z])', r'\1 ', s)                 # "9.1.1with" -> "9.1.1 with"
    s = re.sub(r'\s*-?\s*Create new table for Tep Less', ' (TEP-less)', s, flags=re.I)
    s = re.sub(r'\s+NEW 9\.1\.1\b', '', s)
    return s.strip()


def parse_excel(path):
    """Read sheet 'VCF Design Library' to the end. Rows with only column A are section headers."""
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True)['VCF Design Library']
    out, sub, hdr = [], '', False
    s = lambda v: '' if v is None else str(v).strip()
    for r in ws.iter_rows(values_only=True):
        r = list(r) + [None] * 7
        if all(c is None for c in r[:7]):
            continue
        if r[0] == 'Design Decision ID':
            hdr = True
            continue
        if not hdr or r[0] == 'Design Library':
            continue
        if r[1] is None:
            if r[0] is not None:
                sub = clean_section(str(r[0]))
            continue
        out.append(dict(id=s(r[0]), decision=s(r[1]), justification=s(r[2]), implication=s(r[3]),
                        compliant_status=s(r[4]) or 'Compliant', criticality=s(r[5]) or 'No Risk',
                        notes=s(r[6]), subsection=sub))
    return out


def _norm(t):
    t = t.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    return re.sub(r'\s+', ' ', t).strip().casefold()


def _sig(r):
    return '\x1f'.join(_norm(r.get(k, '')) for k in
                       ('decision', 'justification', 'implication', 'compliant_status', 'criticality'))


def _ratio(a, b):
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


def compute_delta(old, new):
    """Annotate `new` rows (in place) with delta = new|changed|renumbered (+prev_id).
    Case/whitespace/quote-only edits count as unchanged. Returns (counts, removed_old_rows)."""
    used, idx_by_sig, idx_by_id = set(), {}, {}
    for j, r in enumerate(old):
        idx_by_sig.setdefault(_sig(r), []).append(j)
        idx_by_id.setdefault(r['id'], []).append(j)
    match = [None] * len(new)
    # pass 1: identical content, same id
    for i, r in enumerate(new):
        for j in idx_by_sig.get(_sig(r), []):
            if j not in used and old[j]['id'] == r['id']:
                match[i] = j; used.add(j); break
    # pass 2: identical content, different id (renumbered)
    for i, r in enumerate(new):
        if match[i] is None:
            for j in idx_by_sig.get(_sig(r), []):
                if j not in used:
                    match[i] = j; used.add(j); break
    # pass 3: same id, similar content (changed)
    for i, r in enumerate(new):
        if match[i] is None:
            for j in idx_by_id.get(r['id'], []):
                if j not in used and _ratio(_sig(r), _sig(old[j])) >= 0.5:
                    match[i] = j; used.add(j); break
    # pass 4: global greedy fuzzy match of remaining rows (renumbered, maybe edited);
    # score = mean(similarity of decision, similarity of full text), threshold 0.55
    rest_old = [j for j in range(len(old)) if j not in used]
    rest_new = [i for i in range(len(new)) if match[i] is None]
    cand = []
    for i in rest_new:
        for j in rest_old:
            sc = 0.5 * _ratio(_norm(new[i]['decision']), _norm(old[j]['decision'])) \
                + 0.5 * _ratio(_sig(new[i]), _sig(old[j]))
            if sc >= 0.55:
                cand.append((sc, i, j))
    for sc, i, j in sorted(cand, reverse=True):
        if match[i] is None and j not in used:
            match[i] = j; used.add(j)
    counts = {'unchanged': 0, 'changed': 0, 'renumbered': 0, 'new': 0}
    for i, r in enumerate(new):
        j = match[i]
        r.pop('delta', None); r.pop('prev_id', None)
        if j is None:
            r['delta'] = 'new'
        elif old[j]['id'] != r['id']:
            r['delta'] = 'renumbered'; r['prev_id'] = old[j]['id']
        elif _sig(old[j]) != _sig(r):
            r['delta'] = 'changed'
        counts[r.get('delta', 'unchanged')] += 1
    removed = [old[j] for j in range(len(old)) if j not in used]
    return counts, removed


def finalize(rows, extra_keys=('delta', 'prev_id')):
    out = []
    for n, d in enumerate(rows):
        rec = {k: (n if k == '_uid' else d.get(k, '')) for k in KEYS}
        for k in extra_keys:
            if d.get(k):
                rec[k] = d[k]
        out.append(rec)
    return out
