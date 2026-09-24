"""Incremental frontier: ONE exact rooted model with every transition tau_a free (rooted_family.build with all labels
as sources, 'at least one twist' clause included), then each class-level twist pattern W is tested as a set of
ASSUMPTIONS on the 84 'mate' literals m(a,j) = t[a, {(j,0),(j,1)}]  (m true <=> a does not twist class j).
Learned clauses about the disjoint-edge structure are shared between patterns.
Usage: python frontier_incremental.py PATTERN_FILE OUT_FILE [conflict_budget_per_pattern]
Pattern file: one spec per line, 'ab:classes,...' (twisting labels and the classes they twist); every label not
listed twists nothing.
"""
import sys, time
from pysat.solvers import Cadical153, Glucose4
import rooted_family as rf

LABELS = [(c, s) for c in range(7) for s in (0, 1)]


def parse(spec):
    per = {}
    for item in spec.split(','):
        lab, cls = item.split(':')
        per[(int(lab[0]), int(lab[1]))] = set(int(ch) for ch in cls)
    return per


def main():
    pfile, ofile = sys.argv[1], sys.argv[2]
    budget = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    t0 = time.time()
    cnf, pool, T = rf.build([], sources=LABELS)
    print(f'model: {len(T)} tau vars, {pool.top} vars, {len(cnf.clauses)} clauses ({time.time()-t0:.0f}s)', flush=True)
    m = {}
    for a in LABELS:
        for j in range(7):
            if j != a[0]:
                m[(a, j)] = T[(a, ((j, 0), (j, 1)))]
    done = set()
    try:
        for line in open(ofile):
            done.add(line.split(' ')[0])
    except FileNotFoundError:
        pass
    S = Glucose4(bootstrap_with=cnf.clauses) if budget else Cadical153(bootstrap_with=cnf.clauses)
    out = open(ofile, 'a')
    for spec in (l.strip() for l in open(pfile)):
        if not spec or spec in done:
            continue
        per = parse(spec)
        assum = []
        for (a, j), v in m.items():
            assum.append(-v if j in per.get(a, ()) else v)
        t1 = time.time()
        if budget:
            S.conf_budget(budget)
            r = S.solve_limited(assumptions=assum)
        else:
            r = S.solve(assumptions=assum)
        res = {False: 'UNSAT', True: 'SAT!!', None: 'UNKNOWN'}[r]
        out.write(f'{spec} result: {res} ({time.time()-t1:.1f}s)\n')
        out.flush()
        print(spec, res, f'{time.time()-t1:.1f}s', flush=True)
        if r:
            break


if __name__ == '__main__':
    main()
