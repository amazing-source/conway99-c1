"""Combinatorial consequences of the hand-proved lemmas L12 and L13a (valid in every local-axiom graph):
  W(a, j) : label a twists class j (tau_a is not the mate matching on the labels of class j).
  (R0) W(a, j) depends only on the class j; a label twists 0 or >= 2 classes; never its own class.
  (L12) if W(a, j), then for EACH label c of class j:  W(c, [a])  or  exists y, [y] not in {[a], j}, with W(y, j).
Question: which twist patterns (at one vertex, t + 1 = 7 classes) survive?  We minimise
  (i) the number of twisting labels, (ii) the number of classes involved (as source or target),
over patterns with at least one twist.  Pure SAT on 14 x 7 booleans (tiny).
"""
import itertools
from pysat.formula import IDPool, CNF, WCNF
from pysat.card import CardEnc, EncType
from pysat.examples.rc2 import RC2

CL = range(7)
LABELS = [(c, s) for c in CL for s in (0, 1)]


def base():
    pool = IDPool()
    cnf = []
    W = lambda a, j: pool.id(('W', a, j))
    for a in LABELS:
        cnf.append([-W(a, a[0])])
        lits = [W(a, j) for j in CL if j != a[0]]
        # not exactly one: each true literal forces another
        for i, l in enumerate(lits):
            cnf.append([-l] + lits[:i] + lits[i + 1:])
    for a in LABELS:
        for j in CL:
            if j == a[0]:
                continue
            third = [W(y, j) for y in LABELS if y[0] not in (a[0], j)]
            for c in [(j, 0), (j, 1)]:
                cnf.append([-W(a, j), W(c, a[0])] + third)
    # (L13a) holonomy/derangement rule: each class is twisted by 0 or >= 2 labels
    for j in CL:
        lits = [W(a, j) for a in LABELS if a[0] != j]
        for i, l in enumerate(lits):
            cnf.append([-l] + lits[:i] + lits[i + 1:])
    anyt = [W(a, j) for a in LABELS for j in CL if j != a[0]]
    cnf.append(anyt)
    return pool, cnf, W


def minimise(objective):
    pool, hard, W = base()
    wcnf = WCNF()
    for cl in hard:
        wcnf.append(cl)
    if objective == 'labels':
        for a in LABELS:
            t = pool.id(('T', a))
            for j in CL:
                if j != a[0]:
                    wcnf.append([-W(a, j), t])
            wcnf.append([-t], weight=1)
    else:
        for i in CL:
            inv = pool.id(('C', i))
            for a in LABELS:
                for j in CL:
                    if j != a[0] and (a[0] == i or j == i):
                        wcnf.append([-W(a, j), inv])
            wcnf.append([-inv], weight=1)
    with RC2(wcnf) as rc2:
        m = rc2.compute()
        cost = rc2.cost
    s = set(l for l in m if l > 0)
    pattern = {a: [j for j in CL if j != a[0] and W(a, j) in s] for a in LABELS}
    return cost, {a: v for a, v in pattern.items() if v}


if __name__ == '__main__':
    for obj in ('labels', 'classes'):
        cost, pat = minimise(obj)
        print(f'minimum number of {"twisting labels" if obj == "labels" else "classes involved"} allowed by L12: {cost}')
        print('   example pattern (label -> twisted classes):', pat)
