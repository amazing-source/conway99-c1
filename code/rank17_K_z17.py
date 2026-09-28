r"""K = Z^17 cap {y1, y2}-perp for structures' 8 Z^17 y-pair representatives (conway99-rank17/z17_y_pair_representatives.json),
in the data/rank17/K_<tag>.json format of rank17_K.py (tag Z17), so that rank17_z4export / rank17_z4 / rank17_pass2 run on them.
Exact: integer kernel by HNF of [M | I], LLL, det K = 49 checked (handoff Prop. 4.1), ambient = standard coordinates.
Usage: python rank17_K_z17.py"""
import json, os, sys
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from envelope_trap import hnf_rows, lll

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'rank17')
SRC = 'C:/home/researcher/Desktop/conway99-rank17/z17_y_pair_representatives.json'


def det_int(M):
    M = [[F(x) for x in r] for r in M]
    n = len(M); d = F(1)
    for c in range(n):
        p = next((i for i in range(c, n) if M[i][c] != 0), None)
        if p is None:
            return 0
        if p != c:
            M[c], M[p] = M[p], M[c]; d = -d
        d *= M[c][c]
        for i in range(c + 1, n):
            f = M[i][c] / M[c][c]
            M[i] = [a - f * b for a, b in zip(M[i], M[c])]
    return d


def main():
    Z = json.load(open(SRC))
    out = {'V': 'Z^17', 'core': 'Z17', 'units': 17, 'n': len(Z['pairs']),
           'note': 'structures z17_y_pair_representatives.json; ' + str(Z['status']), 'K': []}
    for p in Z['pairs']:
        y1, y2 = p['y1'], p['y2']
        assert sum(t * t for t in y1) == 7 and sum(t * t for t in y2) == 7 and sum(a * b for a, b in zip(y1, y2)) == 0
        # kernel of x -> (x.y1, x.y2): HNF of [M | I] with M = [y1 y2] columns
        rows = [[y1[i], y2[i]] + [int(i == j) for j in range(17)] for i in range(17)]
        H = hnf_rows(rows)
        ker = [r[2:] for r in H if r[0] == 0 and r[1] == 0 and any(r[2:])]
        assert len(ker) == 15, len(ker)
        Bk = lll([[int(x) for x in r] for r in ker])
        G = [[sum(a * b for a, b in zip(u, v)) for v in Bk] for u in Bk]
        d = det_int(G)
        assert d == 49, 'det K = %s' % d
        X = np.array(Bk, dtype=np.int64)
        nrm = (X * X).sum(axis=1)
        out['K'].append({'id': p['id'], 'K_basis': [[str(x) for x in r] for r in Bk], 'K_gram': G,
                         'counts_norm_1_2_3': None, 'rootless_U_allowed': p.get('rootless_U_allowed'),
                         'y1': y1, 'y2': y2, 'profiles': p.get('profiles')})
        print('pair', p['id'], 'det 49 ok, basis norms', sorted(int(t) for t in nrm)[:6], flush=True)
    json.dump(out, open(os.path.join(DATA, 'K_Z17.json'), 'w'))
    print('wrote K_Z17.json', flush=True)


if __name__ == '__main__':
    main()
