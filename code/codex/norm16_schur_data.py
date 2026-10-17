"""Exact Schur data for 3I-A+J/9 on core+D+Z.

After eliminating the core, the Z block is Q=3I-A_Z-J/7 and the D-Z
block is (3J-7X)/7. Export H and Q^-1/49 with a common integer scale.
"""
import argparse
import json
from functools import lru_cache
from math import lcm
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]


@lru_cache(None)
def source_data():
    cores = [c for c in json.loads((ROOT/'data/codex_norm16_cores.json').read_text())['cases']
             if c['representatives']]
    attachments = json.loads((ROOT/'data/codex_norm16_attachments_rank.json').read_text())['cases']
    forests = json.loads((ROOT/'data/codex_norm16_far_forest_refined.json').read_text())['forests']
    return cores, attachments, forests


@lru_cache(None)
def core_data(case):
    cores, _, _ = source_data()
    b = sp.Matrix(cores[case]['representatives'][0])
    ac = sp.zeros(16)
    ac[:8, 8:16] = b
    ac[8:16, :8] = b.T
    m = 3*sp.eye(16)-ac+sp.ones(16)/9
    assert all(m[:i, :i].det() > 0 for i in range(1, 17))
    return m.inv()


@lru_cache(None)
def h_matrix(case, orbit):
    _, attachments, _ = source_data()
    rows = attachments[case]['orbits'][orbit]['representative']
    v = sp.zeros(16, 8)
    for d, row in enumerate(rows):
        for i in row[:2]+[8+q for q in row[2:]]:
            v[i, d] = 1
    cd = sp.ones(16, 8)/9-v
    return 3*sp.eye(8)+sp.ones(8)/9-cd.T*core_data(case)*cd


@lru_cache(None)
def w_matrix(forest):
    _, _, forests = source_data()
    f = next(f for f in forests if f['id'] == forest)
    q = 3*sp.eye(11)-sp.Matrix(f['adjacency_Z'])-sp.ones(11)/7
    # These two eliminated blocks must be positive definite.
    assert all(q[:i, :i].det() > 0 for i in range(1, 12))
    return q.inv()/49


def matrices(case, orbit, forest, edge=None):
    h = h_matrix(case, orbit).copy()
    if edge is not None:
        d, e = edge
        h[d, e] -= 1
        h[e, d] -= 1
    w = w_matrix(forest)
    scale = lcm(*[int(x.q) for x in list(h)+list(w)])
    return scale, [[int(x) for x in row] for row in (scale*h).tolist()], [[int(x) for x in row] for row in (scale*w).tolist()]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', type=int, default=0)
    parser.add_argument('--orbit', type=int, default=0)
    parser.add_argument('--forest', type=int, default=2)
    parser.add_argument('--output', default='data/codex_norm16_schur_0_0_2.txt')
    args = parser.parse_args()
    scale, h, w = matrices(args.case, args.orbit, args.forest)
    lines = [str(scale)]+[' '.join(map(str, row)) for row in h+w]
    (ROOT/args.output).write_text('\n'.join(lines)+'\n', encoding='ascii')
    print(json.dumps({'scale': scale, 'file': args.output}))
