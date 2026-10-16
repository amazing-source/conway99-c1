"""Five-star cases with symmetry breaking (LAB 16/10/2026).

For an M_4 orbit case (five_split_par_core), the stabiliser H of M_4 in the letter group of order 3072 still acts on the
model.  Every solution has a lexicographically least image under H, which satisfies x <= sigma(x) for every sigma in H.
We add these lex-leader constraints for up to MAXEL elements of H (all of H when it is small), over the edge variables in
a fixed order.  Encoding: a_0 true; for each position i, (not a_{i-1} or not x_i or y_i), and a_i is forced true when
the prefix is equal: (not a_{i-1} or x_i or y_i or a_i), (not a_{i-1} or not x_i or not y_i or a_i), with y = x o sigma.
Sound: adding constraints satisfied by the lex-least image cannot lose satisfiability.
usage: python five_symbreak.py <case> <out.cnf> [max elements]"""
import itertools
import random
import sys

import five_split_par_core as core

k = int(sys.argv[1])
out = sys.argv[2]
maxel = int(sys.argv[3]) if len(sys.argv) > 3 else 200
rep, size = core.reps[k]
M4 = set(frozenset(p) for p in rep)
H = [g for g in core.group if set(frozenset((g[a], g[b])) for a, b in M4) == M4]
H = [g for g in H if any(g[x] != x for x in g)]           # drop the identity
rng = random.Random(k)
if len(H) > maxel:
    H = rng.sample(H, maxel)
S, idx, e = core.S, core.idx, core.e
pairs = sorted(itertools.combinations(range(len(S)), 2))
order = [e[p] for p in pairs]                              # variable order for lex
pos_of = {e[p]: n for n, p in enumerate(pairs)}


def img_var(g, i, j):
    a = idx[frozenset(g.get(y, y) for y in S[i])]
    b = idx[frozenset(g.get(y, y) for y in S[j])]
    return e[(a, b)]


clauses = []
nv = core.F.n
for g in H:
    # sigma maps the variable of pair (i,j) to the variable of the image pair; y_n = x_{sigma(n)}
    ys = [img_var(g, i, j) for (i, j) in pairs]
    prev = None
    for n, (x, y) in enumerate(zip(order, ys)):
        if x == y:
            continue
        nv += 1
        a = nv
        if prev is None:
            clauses.append([-x, y])
            clauses.append([x, y, a])
            clauses.append([-x, -y, a])
        else:
            clauses.append([-prev, -x, y])
            clauses.append([-prev, x, y, a])
            clauses.append([-prev, -x, -y, a])
        prev = a
core.write_case(k, out)
lines = open(out).read().split("\n")
head = lines[0].split()
nvar, ncl = int(head[2]), int(head[3])
with open(out, "w") as fh:
    fh.write("p cnf %d %d\n" % (nv, ncl + len(clauses)))
    fh.write("\n".join(lines[1:]).rstrip("\n") + "\n")
    for c in clauses:
        fh.write(" ".join(map(str, c)) + " 0\n")
print("case %d: |orbit| %d, stabiliser used %d elements, %d lex clauses, %d vars" % (k, size, len(H), len(clauses), nv))
