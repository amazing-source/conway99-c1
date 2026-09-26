"""C2's general equilibrium (star), 26/09 night, in the valid linear form (structures):
for a block k and a set S of blocks (k not in S, s = |S|), Lab = the 2s orbits of pairs {k,m}, m in S;
g_o = sum_{m in S} phi_o(km) (own pair included), delta_W = |P_W cap S| + sum_{m in S} phi_W(km) - s for W avoiding k,
eps_W = sum_{m in S} phi_W(km) for W through k, W not in Lab.  Exact:
  sum_{W avoiding k} delta_W^2 + sum_{W through k, not in Lab} eps_W^2 = sum_{o in Lab} (2 - g_o)(g_o + 5).
Valid linear consequence (|x| <= x^2 on integers, (2-g)(g+5) <= 10 - 4g on g >= 0 integers):
  sum |delta_W| + sum eps_W <= sum_{o in Lab} (10 - 4 g_o)."""
import itertools
import numpy as np
from general_model import N, PAIRS, pr


def add_star_budget(A, lo, hi, lb, ub, nvar, phi, orbs, sets=None):
    rows, rlo, rhi, extra = [], [], [], []
    cnt = [nvar]

    def new(l, u):
        extra.append((l, u))
        cnt[0] += 1
        return cnt[0] - 1

    def row(cs, l, h):
        rows.append(cs)
        rlo.append(l)
        rhi.append(h)
    n_orb = len(orbs)
    for k in range(N):
        others = [m for m in range(N) if m != k]
        for r in range(1, len(others)):                  # proper nonempty subsets (S = all is the plain F1 count)
            for S in itertools.combinations(others, r):
                if sets is not None and (k, S) not in sets:
                    continue
                s = len(S)
                Lab = [i for i in range(n_orb) if k in orbs[i]['pair'] and (set(orbs[i]['pair']) - {k}) <= set(S)]
                terms = []
                for i in range(n_orb):
                    P = orbs[i]['pair']
                    if i in Lab:
                        continue
                    a = new(0, 3 * s + 2)
                    if k not in P:
                        const = len(set(P) & set(S)) - s
                        lin = [(phi[(i, pr(k, m))], 1) for m in S]
                        # a >= delta, a >= -delta
                        row([(a, 1)] + [(v, -c) for v, c in lin], const, np.inf)
                        row([(a, 1)] + [(v, c) for v, c in lin], -const, np.inf)
                    else:
                        lin = [(phi[(i, pr(k, m))], 1) for m in S]
                        row([(a, 1)] + [(v, -c) for v, c in lin], 0, np.inf)
                    terms.append((a, 1))
                # sum a <= sum_{o in Lab} (10 - 4 g_o) = 10|Lab| - 4 sum_o g_o
                g_terms = [(phi[(o, pr(k, m))], 4) for o in Lab for m in S]
                row(terms + g_terms, -np.inf, 10 * len(Lab))
    n2 = cnt[0]
    A2 = np.zeros((A.shape[0] + len(rows), n2))
    A2[:A.shape[0], :nvar] = A
    for rr, cs in enumerate(rows):
        for j, c in cs:
            A2[A.shape[0] + rr, j] += c
    lb2 = np.concatenate([lb, [e[0] for e in extra]])
    ub2 = np.concatenate([ub, [e[1] for e in extra]])
    return A2, np.concatenate([lo, rlo]), np.concatenate([hi, rhi]), lb2, ub2, n2
