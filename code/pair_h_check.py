r"""Finish line (C), C1 27/09: for each (y1, y2) pair of a pairs_NNN.json file, the exact h-stage with PRESCRIBED coverage.
RIGID lattices (no norm-3 vector hits a new root at 3/2): w(beta) = 1 exactly on hits(y1) u hits(y2), w = 3 elsewhere.
General lattices: w = 1 on the y-hits; w in {1,3} on the new roots hit at 3/2 by some norm-3 vector orthogonal to y1, y2;
w = 3 on all other new roots.  Plus: h orthogonal to y1, y2 and pairwise, |(h,beta)| <= 1,
Lemma Z (sum h in 2U), cells with norm-3 x orthogonal to y1, y2 (both signs for every pair of blocks).
A pair with no h-configuration is EXCLUDED (all conditions proven, notes/140-141).
Usage: python pair_h_check.py <envelope.json> <pairs_NNN.json> <out.jsonl> [--from K] [--to K] [--max-seconds S] [--lemma-u | --lemma-u-strong]"""
import json, os, sys, time
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from h_stage2 import setup
from y_first import h_exact


def main():
    rec_ = json.load(open(sys.argv[1]))
    pairs = json.load(open(sys.argv[2]))['pairs']
    outp = sys.argv[3]
    k0 = int(sys.argv[sys.argv.index('--from') + 1]) if '--from' in sys.argv else 0
    k1 = int(sys.argv[sys.argv.index('--to') + 1]) if '--to' in sys.argv else len(pairs)
    ms = float(sys.argv[sys.argv.index('--max-seconds') + 1]) if '--max-seconds' in sys.argv else 60
    lemma_u = 2 if '--lemma-u-strong' in sys.argv else ('--lemma-u' in sys.argv)   # notes/145 Lemma U / U+ (general lattices)
    B, Bf, R, X3, X4c, X4, S = setup(rec_['gens'])
    HS = np.rint(X4 @ S.T).astype(np.int64)
    ok = np.abs(HS).max(axis=1) <= 1
    H, Hc, HSb = X4[ok], X4c[ok], (HS[ok] != 0)
    par = [int(''.join(str(int(b) & 1) for b in row[::-1]), 2) for row in Hc]
    rigid = bool((np.abs(np.abs(X3 @ S.T) - 1.5) < 1e-6).sum(axis=1).max() == 0)
    done = set()
    if os.path.exists(outp):
        for line in open(outp):
            done.add(json.loads(line)['k'])
    for k in range(k0, min(k1, len(pairs))):
        if k in done:
            continue
        y1 = np.array([float(F(x)) for x in pairs[k][0]])
        y2 = np.array([float(F(x)) for x in pairs[k][1]])
        yh = ((np.abs(np.abs(S @ y1) - 1.5) < 1e-6) | (np.abs(np.abs(S @ y2) - 1.5) < 1e-6))
        t0 = time.time()
        hittable = None
        if not rigid:
            perp = (np.abs(X3 @ y1) < 1e-9) & (np.abs(X3 @ y2) < 1e-9)
            hittable = (np.abs(np.abs(X3[perp] @ S.T) - 1.5) < 1e-6).any(axis=0)
        res = h_exact(y1, y2, yh, rigid, H, Hc, HSb, par, X3, S, t0, ms, hittable=hittable, lemma_u=lemma_u)
        sec = time.time() - t0
        row = {'k': k, 'rigid': rigid, 'h_found': res is not None, 'timeout': (res is None and sec >= ms - 0.5),
               'seconds': round(sec, 2), 'lemma_u': lemma_u}
        if res is not None:
            row['h'] = [int(i) for i in res]
        with open(outp, 'a') as f:
            f.write(json.dumps(row) + '\n')
        print(json.dumps(row), flush=True)


if __name__ == '__main__':
    main()
