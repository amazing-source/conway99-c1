"""Pilot: signed U on a fixed-D skeleton (3K2_or14 by default), D imposed at the PAIR level (canonical parities WLOG).
Usage (from C2's repo root, so that scripts/ and logs/ resolve):
    python <path>/run_signedU_fixed.py <ptype json> <assign json> <tag> [--test] [--nosign]
env TL (time limit, s), LOWMEM (C2's chunked pricing).
--test: build, apply the layer, unit-test entries() against score_parts(), print sizes, no solve.
--nosign: same pipeline without the signed layer (control: U with pair-level D)."""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from signed_layer import apply_signed_layer, forbid_pairlevel, check_scores, C2_SCRIPTS
sys.path.insert(0, C2_SCRIPTS)
import orbit_colmodel as OM
import orbit_colmodel_U as OU

ptf, asgf, tag = sys.argv[1], sys.argv[2], sys.argv[3]
test = '--test' in sys.argv
nosign = '--nosign' in sys.argv
items = {it['tag']: it for it in json.load(open(ptf))}
pt = {tuple(int(c) for c in k.split(',')): tuple(v) for k, v in items[tag]['ptype'].items()}
for j, a in enumerate(json.load(open(asgf))[tag]):
    assign = {int(c): [tuple(e) for e in edges] for c, edges in a.items()}
    t0 = time.time()
    g = OU.OrbitModelU(pt)
    fb = forbid_pairlevel(g, assign)
    g = OU.OrbitModelU(pt, forbid=fb)
    print('%s a%d: U (pair-level D) columns %d rows %d, empty orbits %s (%.0fs)'
          % (tag, j, sum(len(M) for M in g.cols), len(g.rname), g.empty_orbits, time.time() - t0), flush=True)
    if g.empty_orbits:
        continue
    if not nosign:
        apply_signed_layer(g)
        print('  rows after signed layer: %d (%.0fs)' % (len(g.rname), time.time() - t0), flush=True)
        if g.empty_orbits_signed:
            print('  DEAD (combinatorial): an orbit has no signed column', flush=True)
            continue
        bad = check_scores(g, trials=300)
        print('  unit test entries vs score_parts: %d mismatches of 300' % bad, flush=True)
    if test:
        continue
    obj, y = g.solve(tlimit=float(os.environ.get('TL', 3000)), verbose=os.environ.get('V') is not None)
    if g.done and obj > 1e-6:
        ok, b = g.verify(y)
        print('  %s: INFEASIBLE slack %.4f, exact check %s %s (%.0fs)' % (tag, obj, 'VALID' if ok else 'FAILED', b,
                                                                        time.time() - t0), flush=True)
        if ok:
            OM.save_cert(g, y, 'logs/orbit_certs/signedU_%s_a%d.json.gz' % (tag, j), 'signedU',
                         {'ptype': items[tag]['ptype'], 'assign': a, 'D': 'pair-level', 'parity': 'canonical'}, b)
    else:
        print('  %s: %s obj %.5f (%.0fs)' % (tag, 'FEASIBLE' if g.done else 'TIME CAP', obj, time.time() - t0), flush=True)
