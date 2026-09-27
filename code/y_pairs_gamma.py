r"""Finish line (C), C1 27/09: y-pair enumeration reduced by Gamma = Aut(U)/W(R) (full-rank lattices, gamma_fullrank.py).
y1: W-dominant (y_pairs.dominant_y1), then one representative per Gamma-orbit (Gamma preserves the fundamental chamber).
y2: W(R cap y1-perp)-dominant candidates (y2_engine), then one representative per orbit of Stab_Gamma(y1) x {+-1}
(Stab_Gamma(y1) preserves R cap y1-perp and its positive system, hence the candidate set; -y2 is merged when it is a candidate).
Complete up to Aut(U) x {signs}: every frame pair is Aut(U)-equivalent to a listed one (up to the order of y1, y2).
Usage: python y_pairs_gamma.py <envelope.json> <gamma.json> <out.json> [--max-seconds S]"""
import json, os, sys, time
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from y_pairs import setup, dominant_y1
from y2_engine import Y2Engine


def orbit_reps(vectors, mats, sign=False):
    """vectors: int array (n x 24) of coefficient rows; mats: list of int matrices (a -> a @ M). Returns (rep indices, orbit sizes)."""
    key = {tuple(v): k for k, v in enumerate(vectors)}
    parent = list(range(len(vectors)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for k, v in enumerate(vectors):
        imgs = [v @ M for M in mats]
        if sign:
            imgs += [-w for w in imgs]
        for w in imgs:
            j = key.get(tuple(int(x) for x in w))
            if j is not None:
                ra, rb = find(k), find(j)
                if ra != rb:
                    parent[ra] = rb
    groups = {}
    for k in range(len(vectors)):
        groups.setdefault(find(k), []).append(k)
    reps = [min(g) for g in groups.values()]
    sizes = [len(g) for g in groups.values()]
    return reps, sizes


def main():
    rec_ = json.load(open(sys.argv[1]))
    gam = json.load(open(sys.argv[2]))
    outp = sys.argv[3]
    ms = float(sys.argv[sys.argv.index('--max-seconds') + 1]) if '--max-seconds' in sys.argv else 3600
    assert gam['id'] == rec_['id']
    mats = [np.array(M, dtype=np.int64) for M in gam['matrices']]
    t0 = time.time()
    B, Gi, Bf, R, X3, Snew = setup(rec_['gens'])
    Y, Yf, info = dominant_y1(B, Gi, Bf, R, X3, Snew)
    reps1, sizes1 = orbit_reps(Y, mats)
    info.update(id=rec_['id'], roots=rec_['roots'], gamma=len(mats), y1_orbits=len(reps1))
    print(json.dumps(info), flush=True)
    eng = Y2Engine(B, Gi, Bf, R, X3, Snew)
    pairs = []
    tot = {'y2_candidates': 0, 'y2_orbits': 0, 'truncated': 0}
    for r in reps1:
        if time.time() - t0 > ms:
            info['timeout'] = True
            break
        y1c = Y[r]
        stab = [M for M in mats if np.array_equal(y1c @ M, y1c)]
        Y2, st = eng.pairs_for(Yf[r], t0=time.time(), max_seconds=ms)
        tot['truncated'] += int(st.get('truncated', False))
        tot['y2_candidates'] += len(Y2)
        if len(Y2) == 0:
            continue
        reps2, _ = orbit_reps(Y2, stab, sign=True)
        tot['y2_orbits'] += len(reps2)
        for k in reps2:
            pairs.append((y1c, Y2[k]))
    info.update(tot)
    info['pairs'] = len(pairs)
    info['complete'] = not info.get('timeout') and tot['truncated'] == 0
    info['seconds'] = round(time.time() - t0, 1)
    print(json.dumps(info), flush=True)

    def q24(a):
        return [str(sum(F(int(a[i])) * B[i][k] for i in range(24))) for k in range(24)]
    json.dump({'id': rec_['id'], 'pairs': [[q24(a), q24(b)] for a, b in pairs], 'stats': info,
               'note': 'complete up to Aut(U) x signs (Gamma from gamma_fullrank.py, |Gamma| checked against the table)'},
              open(outp, 'w'))


if __name__ == '__main__':
    main()
