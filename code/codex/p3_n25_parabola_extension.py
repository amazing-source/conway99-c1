"""Exact column filter from LAP's integer parabola, after adjoining one vertex.

One small pilot, no support enumeration or LP. Optimize the coefficient of
the new vertex analytically over every integer, for a fixed small weight pool.
"""
from itertools import combinations
import json

import numpy as np

from p3_n25_saturated import ROOT, adjacency


def phi(a, w, level):
    aw = a @ w
    first = int(14*w.sum()-aw.sum())
    second = int(12*(w @ w)+2*int(w.sum())**2-w @ aw-aw @ aw)
    return second-(2*level+1)*first+(99-len(a))*level*(level+1)


def columns(a):
    deficit = 2-a-a @ a
    forbidden = [sum(1 << j for j in range(28) if i != j and deficit[i, j] == 0)
                 for i in range(28)]
    out = []
    for k in range(4):
        for pp in combinations(range(3), k):
            if any(deficit[p, q] == 0 for p, q in combinations(pp, 2)):
                continue
            available = [q for q in range(3, 28) if all(deficit[p, q] > 0 for p in pp)]
            for nn in combinations(available, 4+k):
                bits = 0
                for q in nn:
                    if bits & forbidden[q]:
                        break
                    bits |= 1 << q
                else:
                    b = np.zeros(28, dtype=np.int64)
                    b[list(pp)+list(nn)] = 1
                    out.append(b)
    b = np.array(out, dtype=np.int64)
    b = b[np.all(b @ a <= 2-b, axis=1)]
    # The separate seven-pair capacity theorem, note248.
    return b[np.sum((b @ a)*b, axis=1) >= 2*(b.sum(axis=1)-7)]


def weight_pool(a):
    seen = set()
    out = []

    def add(w):
        w = np.array(w, dtype=np.int64)
        nz = np.flatnonzero(w)
        if not len(nz):
            return
        if w[nz[0]] < 0:
            w = -w
        key = tuple(map(int, w))
        if key not in seen:
            seen.add(key)
            out.append(w)

    identity = np.eye(28, dtype=np.int64)
    for i in range(28):
        add(identity[i])
        add(a[i])
        add(a[i]+identity[i])
    q = [a[p]+identity[p] for p in range(3)]
    for p, r in combinations(range(3), 2):
        add(q[p]+q[r])
        add(q[p]-q[r])
    return out


def pilot(row):
    a = np.array(adjacency(row), dtype=np.int64)
    b = columns(a)
    d = 14-b.sum(axis=1)
    assert np.all(d > 0)
    removed = np.zeros(len(b), dtype=bool)
    witnesses = []
    pool = weight_pool(a)
    for w in pool:
        first = int(14*w.sum()-(a @ w).sum())
        centre = first//71
        t = b @ w
        s = 2*int(w.sum())-b @ (w+a @ w)
        for level in (centre-1, centre, centre+1):
            budget = phi(a, w, level)
            assert budget >= 0, 'This pilot must begin with a support not excluded by its weights.'
            constant = budget-(t-level)*(t-level-1)
            linear = 2*s-(2*level+1)*d
            h = (-linear)//(2*d)
            value = constant+linear*h+d*h*h
            other = constant+linear*(h+1)+d*(h+1)*(h+1)
            take_other = other < value
            h = h+take_other.astype(np.int64)
            value = np.minimum(value, other)
            newly = np.flatnonzero((value < 0) & ~removed)
            if len(newly):
                # One direct enlarged-graph evaluation for each new certificate family.
                j = int(newly[0])
                extended = np.zeros((29, 29), dtype=np.int64)
                extended[:28, :28] = a
                extended[28, :28] = extended[:28, 28] = b[j]
                assert phi(extended, np.r_[w, h[j]], level) == int(value[j])
                witnesses.append({'w': w.tolist(), 'a': level, 'parent_phi': budget,
                                  'newly_removed': len(newly),
                                  'example': {'B': np.flatnonzero(b[j]).tolist(),
                                              'h': int(h[j]), 'phi': int(value[j])}})
                removed[newly] = True
    return {'id': row['id'], 'scope': __doc__, 'weight_count': len(pool),
            'before': len(b), 'removed': int(removed.sum()),
            'remaining': int((~removed).sum()), 'certificate_families': witnesses,
            'excluded_blocks': [np.flatnonzero(mask).tolist() for mask in b[removed]]}


if __name__ == '__main__':
    source = json.loads((ROOT/'data/codex_p3_n25_open_triangles.json').read_text())
    row = next(r for r in source['supports'] if r['id'] == 4)
    result = pilot(row)
    (ROOT/'data/codex_p3_n25_parabola_extension.json').write_text(
        json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'excluded_blocks'}, indent=2))
