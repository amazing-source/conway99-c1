"""BvLS: candidate far-neighbourhoods of every far vertex from the integer equations only; then count the symmetric
graphs obtainable by picking one candidate per row (exact propagation)."""
import numpy as np, time
from ortools.sat.python import cp_model
from graphs_test import bvls243
A = bvls243(); n = 243
v = 0; a = int(np.nonzero(A[v])[0][0]); ap = [c for c in np.nonzero(A[v])[0] if A[a, c]][0]
ball = sorted(set([v, a, ap]) | set(np.nonzero(A[v])[0]) | set(np.nonzero(A[a])[0]) | set(np.nonzero(A[ap])[0]))
tri = [v, a, ap]; C = [u for u in ball if u not in tri]; far = [u for u in range(n) if u not in ball]
Af = A[np.ix_(far, far)]; deg = int(Af[0].sum()); F = len(far)
cands = []
t = time.time()
for wi, w in enumerate(far):
    m = cp_model.CpModel(); x = [m.NewBoolVar("") for _ in range(F)]
    m.Add(x[wi] == 0); m.Add(sum(x) == deg)
    for u in C:
        tgt = (2 - A[u, w]) - len(set(np.nonzero(A[u])[0]) & set(np.nonzero(A[w])[0]) & set(C))
        m.Add(sum(x[j] for j in range(F) if A[u, far[j]]) == tgt)
    sols = []
    class CB(cp_model.CpSolverSolutionCallback):
        def on_solution_callback(s_): sols.append(frozenset(j for j in range(F) if s_.Value(x[j])))
    s = cp_model.CpSolver(); s.parameters.enumerate_all_solutions = True; s.parameters.num_workers = 1
    s.Solve(m, CB()); cands.append(sols)
print("candidates per row: distribution", {c: sum(1 for L in cands if len(L) == c) for c in set(len(L) for L in cands)},
      round(time.time() - t, 1), "s")
# propagation: a candidate S for row w is viable only if every w' in S has a viable candidate containing w,
# and every w' not in S has a viable candidate not containing w
changed = True
while changed:
    changed = False
    for wi in range(F):
        keep = []
        for S in cands[wi]:
            ok = all(any((wi in T) == (wj in S) for T in cands[wj]) for wj in range(F) if wj != wi)
            if ok: keep.append(S)
        if len(keep) < len(cands[wi]): cands[wi] = keep; changed = True
print("after symmetric propagation:", {c: sum(1 for L in cands if len(L) == c) for c in set(len(L) for L in cands)})
true_ok = all(frozenset(np.nonzero(Af[wi])[0].tolist()) in cands[wi] for wi in range(F))
print("true graph still among candidates:", true_ok)

# the alternative candidate of each row
alt = []
for wi in range(F):
    tr = frozenset(np.nonzero(Af[wi])[0].tolist())
    alt.append([S for S in cands[wi] if S != tr][0])
sym = all((wj in alt[wi]) == (wi in alt[wj]) for wi in range(F) for wj in range(F) if wi != wj)
sizes = sorted(set(len(alt[wi] ^ frozenset(np.nonzero(Af[wi])[0].tolist())) for wi in range(F)))
print("alternative rows form a symmetric graph:", sym, "; |alt xor true| per row:", sizes)
if sym:
    B2 = A.copy()
    for wi in range(F):
        for wj in range(F):
            B2[far[wi], far[wj]] = 1 if wj in alt[wi] else 0
    from graphs_test import is_srg
    import networkx as nx
    print("twin graph is srg(243,22,1,2):", is_srg(B2, 243, 22, 1, 2))
    if is_srg(B2, 243, 22, 1, 2):
        print("twin isomorphic to BvLS:", nx.is_isomorphic(nx.from_numpy_array(A), nx.from_numpy_array(B2)))
