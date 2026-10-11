"""3-covers of the Brouwer-Haemers graph Q = srg(81,20,1,6) with triangle fibres.
A cover = for every edge PQ of Q a bijection (perfect matching) between the fibres P and Q.
Gamma (243 vertices) is srg(243,22,1,2) iff
  (T) every triangle of Q lifts to three triangles (holonomy around each line of Q is trivial), and
  (L) for non-adjacent P,Q of Q and p in P, q in Q: exactly 2 of the 6 two-paths through common neighbours of P,Q
      carry p to q.
We use the labelling of BvLS: fibres = lines of direction h_d."""
import itertools, numpy as np
from lib243 import *
from lines_model import *

def fibres_of(A, d=0):
    hd = HS[d]
    F = lines_of_direction(hd)
    return [list(f) for f in F]

def quotient(A, fib):
    n = len(fib); where = {}
    for i, f in enumerate(fib):
        for p in f: where[p] = i
    Q = np.zeros((n, n), dtype=np.int64)
    for i, f in enumerate(fib):
        for p in f:
            for q in np.nonzero(A[p])[0]:
                if where[q] != i: Q[i, where[q]] += 1
    return Q, where

def is_cover(A, fib):
    """every pair of distinct fibres joined by 0 edges or a perfect matching; fibres are triangles."""
    Q, where = quotient(A, fib)
    tri = all(A[f[0], f[1]] and A[f[0], f[2]] and A[f[1], f[2]] for f in fib)
    ok = tri and set(np.unique(Q)) <= {0, 3}
    if ok:
        for i in range(len(fib)):
            for j in np.nonzero(Q[i])[0]:
                sub = A[np.ix_(fib[i], fib[j])]
                if not ((sub.sum(0) == 1).all() and (sub.sum(1) == 1).all()): return False, Q
    return ok, (Q > 0).astype(np.int64)

from ortools.sat.python import cp_model

def cover_model(A0, fib, Qadj, fix_edges=None, free_edges=None):
    """CP-SAT model for the S3-covers. Variables x[(p,q)] for p,q in BH-adjacent fibres.
    fix_edges: dict {(P,Q): 3x3 matrix} forcing some matchings (default: none fixed)."""
    m = cp_model.CpModel(); nQ = len(fib)
    X = {}
    edgesQ = [(P, R) for P in range(nQ) for R in range(P + 1, nQ) if Qadj[P, R]]
    for P, R in edgesQ:
        for p in fib[P]:
            for r in fib[R]:
                v = m.NewBoolVar(""); X[(p, r)] = X[(r, p)] = v
        for p in fib[P]:
            m.AddExactlyOne([X[(p, r)] for r in fib[R]])
        for r in fib[R]:
            m.AddExactlyOne([X[(p, r)] for p in fib[P]])
        if fix_edges is not None and (P, R) in fix_edges:
            Mx = fix_edges[(P, R)]
            for a, p in enumerate(fib[P]):
                for b, r in enumerate(fib[R]):
                    m.Add(X[(p, r)] == int(Mx[a][b]))
    # triangles of Q
    nb = [set(np.nonzero(Qadj[P])[0]) for P in range(nQ)]
    ntri = 0
    for P in range(nQ):
        for R in nb[P]:
            if R <= P: continue
            for S in nb[P] & nb[R]:
                if S <= R: continue
                ntri += 1
                for (U, V, W) in ((P, R, S), (R, S, P), (S, P, R), (P, S, R), (R, P, S), (S, R, P)):
                    for u in fib[U]:
                        for v in fib[V]:
                            for w in fib[W]:
                                m.AddBoolOr([X[(u, v)].Not(), X[(v, w)].Not(), X[(u, w)]])
    # Latin condition on non-adjacent fibre pairs
    nL = 0
    for P in range(nQ):
        for R in range(P + 1, nQ):
            if Qadj[P, R]: continue
            CN = sorted(nb[P] & nb[R]); assert len(CN) == 6
            for p in fib[P]:
                for r in fib[R]:
                    terms = []
                    for Z in CN:
                        for z in fib[Z]:
                            y = m.NewBoolVar("")
                            m.AddImplication(y, X[(p, z)]); m.AddImplication(y, X[(z, r)])
                            m.AddBoolOr([X[(p, z)].Not(), X[(z, r)].Not(), y])
                            terms.append(y)
                    m.Add(sum(terms) == 2); nL += 1
    return m, X, edgesQ

def graph_from_X(solver, X, fib, n=243):
    A = np.zeros((n, n), dtype=np.int64)
    for f in fib:
        for a, b in itertools.combinations(f, 2): A[a, b] = A[b, a] = 1
    for (p, q), v in X.items():
        if solver.Value(v): A[p, q] = 1
    return A

def parity_cocycle(A, fib, Qadj):
    """relative parity of matchings: orient each fibre by its stored order; eps(PQ)=parity of the matching."""
    eps = {}
    nQ = len(fib)
    for P in range(nQ):
        for R in range(P + 1, nQ):
            if Qadj[P, R]:
                perm = [int(np.nonzero(A[fib[P][a], fib[R]])[0][0]) for a in range(3)]
                inv = sum(1 for i in range(3) for j in range(i + 1, 3) if perm[i] > perm[j])
                eps[(P, R)] = inv % 2
    return eps

def is_coboundary(eps, nQ):
    """solve eps(PR) = f(P)+f(R) over GF(2) by BFS on the graph; return True/False."""
    import collections
    adj = collections.defaultdict(list)
    for (P, R), e in eps.items():
        adj[P].append((R, e)); adj[R].append((P, e))
    f = {}
    for s in range(nQ):
        if s in f: continue
        f[s] = 0; dq = collections.deque([s])
        while dq:
            u = dq.popleft()
            for v, e in adj[u]:
                if v not in f: f[v] = f[u] ^ e; dq.append(v)
                elif f[v] != f[u] ^ e: return False
    return True
