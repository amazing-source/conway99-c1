"""notes/104 §7: the single surviving configuration (up to the Fano group): C = {01, 02, 15, 25} for the
cyclic Fano plane {0,1,3}+d.  Test the linear kappa system (Z_A, (i), (C')) plus the X-parallel constraint
(for P in C, kappa(Q->P) is the same for its 8 non-pencil neighbours Q)."""
import itertools, pickle
from kappa_linear_system import system, consistent, pairs, disjoint

survivors = pickle.load(open('../data/fano_bc_survivors.pkl', 'rb'))
lines = [tuple(sorted(((0 + d) % 7, (1 + d) % 7, (3 + d) % 7))) for d in range(7)]
def vpt(P):
    L = next(L for L in lines if set(P) <= set(L))
    return next(c for c in L if c not in P)
def pencil_edge(P, Q): return disjoint(P, Q) and vpt(P) == vpt(Q)

for C, st in survivors[:3]:
    nu = {e for e, s in st.items() if s == 1}
    eqs, var = system(nu)
    ok0, rk0 = consistent(eqs)
    extra = []
    for P in C:
        nb = [Q for Q in pairs if disjoint(P, Q) and not pencil_edge(P, Q)]
        for Q1, Q2 in zip(nb, nb[1:]):
            extra.append(({var[(Q1, P)], var[(Q2, P)]} if var[(Q1, P)] != var[(Q2, P)] else set(), 0))
    ok1, rk1 = consistent(eqs + extra)
    print(C, ' linear system:', 'consistent' if ok0 else 'INCONSISTENT', rk0,
          '| + X-parallel:', 'consistent' if ok1 else 'INCONSISTENT', rk1, ' unknowns', len(var))
