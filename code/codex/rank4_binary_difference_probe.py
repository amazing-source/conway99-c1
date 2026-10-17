"""Bounded exact finite-field probe; no enumeration of Conway graphs.

Question: does every spanning isotropic {0,+1,-1} Gram configuration
in dimension four over F7 have a hyperplane missing at most two of its
unsigned directions? If yes, multiplicity <=2 and shadow distance >=6
would exclude a rank-four difference. A survivor only refutes this test.
"""
import itertools as it
import json
from pathlib import Path
import time

import networkx as nx

P = 7
PAIRS = list(it.combinations(range(4), 2))


def matrix(t):
    a = [[0] * 4 for _ in range(4)]
    for (i, j), x in zip(PAIRS, t):
        a[i][j] = a[j][i] = x % P
    return a


def inverse(a):
    b = [row[:] + [int(i == j) for j in range(4)] for i, row in enumerate(a)]
    for j in range(4):
        pivot = next((i for i in range(j, 4) if b[i][j]), None)
        if pivot is None:
            return None
        b[j], b[pivot] = b[pivot], b[j]
        scale = pow(b[j][j], -1, P)
        b[j] = [x * scale % P for x in b[j]]
        for i in range(4):
            if i != j:
                scale = b[i][j]
                b[i] = [(x - scale * y) % P for x, y in zip(b[i], b[j])]
    return [row[4:] for row in b]


def bilinear(v, h, w):
    return sum(v[i] * h[i][j] * w[j] for i in range(4) for j in range(4)) % P


def unsigned(v):
    v = tuple(x % P for x in v)
    first = next(x for x in v if x)
    return tuple((-x) % P for x in v) if first == 6 else v


def orbit(t):
    a = matrix(t)
    for perm in it.permutations(range(4)):
        for signs in it.product((-1, 1), repeat=4):
            for global_sign in (-1, 1):
                z = tuple(global_sign * signs[i] * signs[j] * a[perm[i]][perm[j]] % P
                          for i, j in PAIRS)
                yield tuple(-1 if x == 6 else x for x in z)


def main():
    started = time.monotonic()
    seen = set()
    representatives = []
    for t in it.product((-1, 0, 1), repeat=6):
        if t in seen:
            continue
        seen.update(orbit(t))
        h = matrix(t)
        inv = inverse(h)
        if inv is not None:
            representatives.append((t, h, inv))

    functionals = [v for v in it.product(range(P), repeat=4)
                   if any(v) and next(x for x in v if x) == 1]
    records = []
    complete = True
    for t, h, inv in representatives:
        vectors = sorted({unsigned(v) for v in it.product((-1, 0, 1), repeat=4)
                          if any(v) and bilinear(v, inv, v) == 0})
        basis = {vectors.index(unsigned([h[i][j] for i in range(4)])) for j in range(4)}
        g = nx.Graph()
        g.add_nodes_from(i for i in range(len(vectors)) if i not in basis)
        for i, j in it.combinations(g.nodes, 2):
            if bilinear(vectors[i], inv, vectors[j]) in (0, 1, 6):
                g.add_edge(i, j)
        for i in g:
            assert all(bilinear(vectors[i], inv, vectors[j]) in (0, 1, 6) for j in basis)

        hist = {}
        survivors = []
        certificates = []
        for rest in (nx.find_cliques(g) if len(g) else [[]]):
            clique = sorted(basis | set(rest))
            points = [vectors[i] for i in clique]
            weight, witness = min((sum(sum(a*b for a, b in zip(f, v)) % P != 0 for v in points), f)
                                  for f in functionals)
            key = f'{len(points)}:{weight}'
            hist[key] = hist.get(key, 0) + 1
            cert = {'vectors': points, 'minimum_unsigned_weight': weight, 'functional': witness}
            if weight > 2:
                survivors.append(cert)
            else:
                certificates.append(cert)
            if time.monotonic() - started > 45:
                complete = False
                break
        records.append({'basis_upper_triangle': t, 'candidate_directions': len(vectors),
                        'histogram_size_minweight': hist, 'survivors': survivors,
                        'small_weight_certificates': certificates})
        print(json.dumps({'basis': t, 'histogram': hist, 'survivors': len(survivors)}), flush=True)
        if not complete:
            break

    out = {'question': __doc__, 'complete': complete, 'basis_classes': len(representatives),
           'seconds': time.monotonic() - started, 'records': records}
    dest = Path(__file__).resolve().parents[2] / 'data' / 'codex_rank4_binary_difference_probe.json'
    dest.write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(json.dumps({'complete': complete, 'basis_classes': len(representatives),
                      'seconds': out['seconds'], 'file': str(dest)}))


if __name__ == '__main__':
    main()
