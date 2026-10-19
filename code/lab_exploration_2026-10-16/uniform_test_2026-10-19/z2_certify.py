"""Find and exactly check a Farkas certificate of the second-order count design (z2lib) for one gz template.
usage: python z2_certify.py <codex code dir> <catalogue.json.gz> <index> <out.json> [--corners] [--max-free=7]"""
import gzip
import hashlib
import json
import sys
import time
from pathlib import Path

CODEX, CAT, IDX, OUT = sys.argv[1], sys.argv[2], int(sys.argv[3]), Path(sys.argv[4])
CORNERS = '--corners' in sys.argv
MAXFREE = int(next((a.split('=')[1] for a in sys.argv if a.startswith('--max-free=')), 7))
if sys.flags.optimize:
    raise SystemExit('assertions required')
assert not OUT.exists()
sys.path.insert(0, CODEX)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_z_distribution import RECTANGLES, row_catalogue      # noqa: E402
import z2lib                                                              # noqa: E402

t0 = time.process_time()
raw = Path(CAT).read_bytes()
template = json.loads(gzip.decompress(raw))['open'][IDX]['template']
cat = row_catalogue(template, max_free=MAXFREE)
assert cat['status'] == 'ROW_CATALOGUE_COMPLETE', cat['status']
S = z2lib.build_system(template, [tuple(q) for q in RECTANGLES], cat, corners=CORNERS)
t1 = time.process_time()
cert = z2lib.find_certificate(S)
out = {'scope': 'second-order count design (z2lib), Farkas certificate checked exactly', 'template_index': IDX,
       'catalogue_sha256': hashlib.sha256(raw).hexdigest(), 'corners': CORNERS, 'types': len(S['types']),
       'pairs': len(S['pairs']), 'variables': len(S['names']), 'equalities': len(S['eq']), 'inequalities': len(S['ub']),
       'status': cert['status'], 'check': cert.get('check'), 'build_cpu': round(t1 - t0, 2),
       'certificate_cpu': round(time.process_time() - t1, 2), 'uses_E3': True,
       'state_counts': [r['state_count'] for r in cat['row_types']], 'free_dimension': cat['free_dimension']}
if cert['status'] == 'CERTIFICATE':
    out['certificate'] = {k: cert[k] for k in ('y_eq', 'y_ub', 'y_up')}
    # self-describing copy for the independent verifier: types written as rectangle:state (no internal indices)
    def tk(t):
        qi, z = S['types'][t]
        return '%d%d:%s' % (RECTANGLES[qi][0], RECTANGLES[qi][1], ''.join(map(str, z)))

    def key(name):
        p = name.split(':')
        if p[0] == 'n':
            return 'n|' + tk(int(p[1]))
        if p[0] == 'm':
            return 'm|' + tk(int(p[1])) + '|' + tk(int(p[2]))
        if p[0] == 'C0':
            return 'C0|%d%d' % RECTANGLES[int(p[1])]
        if p[0] in ('L1', 'L3'):
            return p[0] + '|' + tk(int(p[1])) + '|%d%d' % RECTANGLES[int(p[2])]
        if p[0] == 'E3n':
            return 'E3n|%d%d' % RECTANGLES[int(p[1])]
        raise ValueError(name)
    if not CORNERS:
        out['certificate_explicit'] = {k: {key(n): y for n, y in cert[k].items()} for k in ('y_eq', 'y_ub', 'y_up')}
OUT.write_text(json.dumps(out))
print(json.dumps({k: out[k] for k in ('template_index', 'status', 'check', 'types', 'variables', 'build_cpu', 'certificate_cpu')}))
