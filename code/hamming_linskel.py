"""Hamming point, general case (L8): is the contradiction already visible on the LINEAR PARTS of the bijections?

Every bijection phi_{PR}: Q_P -> Q_R (Q = F_2^2) is affine; its linear part L_{PR} permutes the 3 directions
{flip p, flip q, diag}.  Necessary conditions on linear parts only:
 (C-lin) for P = ij, P' = ik: the multiset of composite linear parts L_{P'R}^{-1} L_{PR} (R in [7]-{i,j,k}, 6 of
         them) must be the linear-part multiset of one of the 58 six-tuples allowed by fact C (computed here);
 (E-lin) for P and a class m not in P: for each direction d of Q_P, #{l : L_{P,ml}^{-1}(flip l) = d} is even
         (fact E: the m-coordinate functionals come in balanced pairs of equal linear type).
Usage: hamming_linskel.py [C|E|CE]
"""
import itertools, sys
from collections import Counter
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153

# ---- local data: the 58 allowed six-tuples for fact C, in coordinates (s_i, s_other) -> (s_i, s_other')
pts = [(0, 0), (0, 1), (1, 0), (1, 1)]
ix = {p: t for t, p in enumerate(pts)}
perms = list(itertools.permutations(range(4)))
M = [[1 if pts[u][0] == pts[w][0] else 2 for w in range(4)] for u in range(4)]
sols = []
def rec(start, left, acc, cnt):
    if left == 0:
        if all(acc[u][w] == M[u][w] for u in range(4) for w in range(4)):
            sols.append(tuple(cnt))
        return
    for t in range(start, len(perms)):
        p = perms[t]
        if all(acc[u][p[u]] + 1 <= M[u][p[u]] for u in range(4)):
            for u in range(4): acc[u][p[u]] += 1
            cnt.append(t); rec(t, left - 1, acc, cnt); cnt.pop()
            for u in range(4): acc[u][p[u]] -= 1
rec(0, 6, [[0] * 4 for _ in range(4)], [])
# directions as vectors: 0 = flip first coord (e1), 1 = flip second (e2), 2 = diag (e1+e2)
DV = [(1, 0), (0, 1), (1, 1)]
def linpart(p):
    t = pts[p[0]]
    img = []
    for v in DV:
        w = pts[p[ix[v]]]
        img.append(DV.index(tuple((a - b) % 2 for a, b in zip(w, t))))
    return tuple(img)          # image of direction 0,1,2
S3 = list(itertools.permutations(range(3)))
allowed = set()
for s in sols:
    c = Counter(linpart(perms[t]) for t in s)
    allowed.add(tuple(c.get(g, 0) for g in S3))
allowed = sorted(allowed)

# ---- global model
pool = IDPool()
pairs = [tuple(p) for p in itertools.combinations(range(7), 2)]
def dirs(P):   # direction names of Q_P: ('f', p), ('f', q), ('d',)
    return [('f', P[0]), ('f', P[1]), ('d',)]
def X(P, R, a, b):
    """literal: L_{PR} maps direction a of Q_P to direction b of Q_R (unordered edge stored with P < R)."""
    if P < R:
        return pool.id(('X', P, R, a, b))
    return pool.id(('X', R, P, b, a))
cnf = CNF()
for P in pairs:
    for R in pairs:
        if P < R and not set(P) & set(R):
            dP, dR = dirs(P), dirs(R)
            for a in dP:
                cnf.extend(CardEnc.equals([X(P, R, a, b) for b in dR], 1, vpool=pool, encoding=EncType.pairwise).clauses)
            for b in dR:
                cnf.extend(CardEnc.equals([X(P, R, a, b) for a in dP], 1, vpool=pool, encoding=EncType.pairwise).clauses)

def xor_even(lits):
    """CNF: XOR of lits = 0 (chain with auxiliaries)."""
    if not lits:
        return
    acc = lits[0]
    for l in lits[1:]:
        y = pool.id(('xor', len(cnf.clauses), acc, l))
        cnf.extend([[-y, acc, l], [-y, -acc, -l], [y, -acc, l], [y, acc, -l]])
        acc = y
    cnf.append([-acc])

mode = sys.argv[1] if len(sys.argv) > 1 else 'CE'
if 'E' in mode:
    for P in pairs:
        for m in range(7):
            if m in P:
                continue
            ls = [l for l in range(7) if l not in P and l != m]
            for d in dirs(P):
                lits = []
                for l in ls:
                    R = tuple(sorted((m, l)))
                    lits.append(X(P, R, d, ('f', l)))    # L_{PR}(d) = flip l
                xor_even(lits)
if 'C' in mode:
    for i in range(7):
        for j, k in itertools.combinations([c for c in range(7) if c != i], 2):
            P, Pp = tuple(sorted((i, j))), tuple(sorted((i, k)))
            # local coordinates: Q_P dirs -> (0: flip i, 1: flip j, 2: diag); Q_P' -> (0: flip i, 1: flip k, 2: diag)
            locP = [('f', i), ('f', j), ('d',)]
            locPp = [('f', i), ('f', k), ('d',)]
            rest = [c for c in range(7) if c not in (i, j, k)]
            gvars = {g: [] for g in S3}
            for m, n in itertools.combinations(rest, 2):
                R = (m, n)
                dR = dirs(R)
                for g in S3:
                    # composite maps local dir a of P to local dir g[a] of P':  exists b: L_PR(a)=b and L_P'R(g[a])=b
                    y = pool.id(('comp', P, Pp, R, g))
                    # y <-> AND_a OR_b (X(P,R,a,b) & X(Pp,R,g[a],b))
                    conj = []
                    for a in range(3):
                        ors = []
                        for b in dR:
                            z = pool.id(('and', P, Pp, R, a, g[a], b))
                            x1, x2 = X(P, R, locP[a], b), X(Pp, R, locPp[g[a]], b)
                            cnf.extend([[-z, x1], [-z, x2], [z, -x1, -x2]])
                            ors.append(z)
                        o = pool.id(('or', P, Pp, R, a, g[a]))
                        cnf.append([-o] + ors)
                        for z in ors:
                            cnf.append([o, -z])
                        conj.append(o)
                    cnf.append([y] + [-o for o in conj])
                    for o in conj:
                        cnf.append([-y, o])
                    gvars[g].append(y)
            sel = []
            for pat in allowed:
                s = pool.id(('sel', i, j, k, pat))
                sel.append(s)
                for g, cnt in zip(S3, pat):
                    for cl in CardEnc.equals(gvars[g], cnt, vpool=pool, encoding=EncType.seqcounter).clauses:
                        cnf.append([-s] + cl)
            cnf.append(sel)

print('allowed linear-part multisets for fact C:', len(allowed))
with Cadical153(bootstrap_with=cnf.clauses) as s:
    r = s.solve()
    print(mode, 'vars', pool.top, 'clauses', len(cnf.clauses), '->', 'SAT' if r else 'UNSAT')
