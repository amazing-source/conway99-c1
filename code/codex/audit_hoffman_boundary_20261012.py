"""Audit one published BvLS Hoffman boundary, without a 198-row repeat.

The source row enumerator is reviewed and reused. Enumerate one row per
orbit of a verified boundary stabilizer, transport by explicit permutations,
then independently assemble ALL labelled completions (no symmetry quotient).
"""
from pathlib import Path
from collections import Counter, deque
import argparse
import json
import hashlib
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--deps', required=True)
    ap.add_argument('--coclique', required=True)
    ap.add_argument('--row-timeout', type=float, default=45)
    args = ap.parse_args()
    sys.path.insert(0, args.deps)
    import igraph as ig
    import numpy as np
    from sympy.combinatorics import Permutation, PermutationGroup
    from audit_asymmetry_20261012 import read_graph
    a, edges = read_graph(ROOT / 'data/srg243/bvls243.edges')
    c = sorted(map(int, Path(args.coclique).read_text().split()))
    assert len(c) == len(set(c)) == 45 and not a[np.ix_(c, c)].any()
    f = sorted(set(range(243)) - set(c))
    y = a[np.ix_(c, f)]
    assert (y.sum(axis=0) == 5).all()
    assert np.array_equal(y @ y.T, 20 * np.eye(45, dtype=int) + 2)
    blocks = [sum(1 << j for j in range(45) if y[j, i]) for i in range(198)]
    boundary = '198 45 17\n' + ''.join('5 ' + ' '.join(str(j) for j in range(45)
                 if (b >> j) & 1) + '\n' for b in blocks)
    output = ROOT / 'data/codex_hoffman_boundary_audit_20261012'
    output.mkdir(exist_ok=True)
    (output / 'boundary.txt').write_text(boundary, encoding='ascii')
    colors = [int(i in set(c)) for i in range(243)]
    generators = ig.Graph(243, edges).automorphism_group(color=colors)
    fi = {u: i for i, u in enumerate(f)}
    for p in generators:
        assert {p[i] for i in c} == set(c) and np.array_equal(a[np.ix_(p, p)], a)
    pg = PermutationGroup([Permutation(p) for p in generators])
    fperms = [[fi[p[u]] for u in f] for p in generators]
    domains = [None] * 198
    row_runs = []
    start = time.monotonic()
    for rep in range(198):
        if domains[rep] is not None:
            continue
        target = output / f'row_{rep}.txt'
        t0 = time.monotonic()
        try:
            proc = subprocess.run([str(Path(args.deps) / 'hoffman_rowdom.exe'), str(rep),
                                   '1000000', str(target)], input=boundary, text=True,
                                  capture_output=True, timeout=args.row_timeout, check=True)
        except subprocess.TimeoutExpired:
            report = dict(status='INCOMPLETE', completed_row_orbits=row_runs,
                          timed_out_representative=rep, row_timeout=args.row_timeout,
                          coclique=c, boundary_sha256=hashlib.sha256(boundary.encode()).hexdigest(),
                          conclusion='No independent completion count established by this bounded run.')
            (output / 'report.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
            print(json.dumps(report), flush=True)
            return
        ds = [tuple(sorted(map(int, line.split()))) for line in target.read_text().splitlines()]
        assert len(ds) == len(set(ds)) == int(proc.stdout.strip())
        assert len(ds) < 1000000
        for d in ds:
            assert len(d) == 17 and rep not in d
            assert all(sum((blocks[u] >> j) & 1 for u in d) == (1 if (blocks[rep] >> j) & 1 else 2)
                       for j in range(45))
            assert all((blocks[u] & blocks[v]).bit_count() <= 1
                       for i, u in enumerate(d) for v in d[i+1:])
            assert all((blocks[rep] & blocks[u]).bit_count() <= 1 for u in d)
        domains[rep] = ds
        queue = deque([rep])
        orbit = [rep]
        while queue:
            w = queue.popleft()
            for p in fperms:
                v = p[w]
                if domains[v] is None:
                    domains[v] = [tuple(sorted(p[u] for u in d)) for d in domains[w]]
                    orbit.append(v)
                    queue.append(v)
        info = dict(representative=rep, orbit_size=len(orbit), domain=len(ds),
                    seconds=time.monotonic()-t0, enumerator_stderr=proc.stderr.strip())
        row_runs.append(info)
        print(json.dumps(info), flush=True)
    mask_domains = [[sum(1 << u for u in d) for d in ds] for ds in domains]
    truth = [sum(1 << j for j, v in enumerate(f) if a[u, v]) for u in f]
    assert all(truth[w] in mask_domains[w] for w in range(198))
    inter = [[(b & c0).bit_count() for c0 in blocks] for b in blocks]
    nodes = 0
    solutions = []

    def dfs(assigned, remaining):
        nonlocal nodes
        nodes += 1
        if not remaining:
            solutions.append([assigned[i] for i in range(198)])
            return
        w = min(remaining, key=lambda u: len(remaining[u]))
        for row in remaining[w]:
            next_domains = {}
            for u, ds in remaining.items():
                if u == w:
                    continue
                e = (row >> u) & 1
                target = 2-e-inter[w][u]
                nd = [b for b in ds if ((b >> w) & 1) == e and (row & b).bit_count() == target]
                if not nd:
                    break
                next_domains[u] = nd
            else:
                assigned[w] = row
                dfs(assigned, next_domains)
                del assigned[w]

    dfs({}, dict(enumerate(mask_domains)))
    assert len(solutions) == 1 and solutions[0] == truth
    report = dict(coclique=c, boundary_sha256=hashlib.sha256(boundary.encode()).hexdigest(),
                  stabilizer_order=int(pg.order()), row_orbit_runs=row_runs,
                  domain_histogram=dict(Counter(map(len, domains))),
                  total_domains=sum(map(len, domains)), complete_labelled_solutions=len(solutions),
                  solution_is_input_bvls=True, assembly_nodes=nodes,
                  total_seconds=time.monotonic()-start,
                  method='Reviewed source rowdom.cpp on orbit representatives; verified graph automorphisms '
                         'transport all domains; independent exhaustive Python bitset assembly without symmetry reduction.')
    (output / 'report.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
