"""Sym x Alt identity for a sib column (C1, 26/09 night).  In the (Sym, Alt) basis of the 42 orbits,
Q = [[Q_S, K],[K^T, Q_A]] and Q^2 + Q = 12I + 4J - B^T B has no Sym-Alt part, hence  Q_S K + K Q_A + K = 0.
Pair-level entries: (Q_S)_{YX} = (phi_{Y0}(X) + phi_{Y1}(X))/2,  K_{YX} = (phi_{X0}(Y) - phi_{X1}(Y))/2.
For a sib pair P (Alt column), with the 4-state one-hot of alt_sib.py for every X disjoint from P:
  sum_{X disj P} [ (phi_{Y0}(X) + phi_{Y1}(X)) kappa_{PX} + (phi_{X0}(Y) - phi_{X1}(Y)) sigma_{PX} ] = phi_{P0}(Y) - phi_{P1}(Y)
for every pair Y (kappa = K-state sign, sigma = A-state sign).  Products integer x binary are linearised exactly."""
import itertools
import numpy as np
from general_model import N, PAIRS, pr
from alt_sib import STATES, PHIVAL, prod


def add_alt_sib_full(A, lo, hi, lb, ub, nvar, phi, orbs, symalt=True, altalt=True):
    sib = {}
    by_pair = {}
    for i, o in enumerate(orbs):
        by_pair.setdefault(o['pair'], []).append(i)
        if o['pivot'] == 'sib':
            sib.setdefault(o['pair'], []).append(i)
    rows, rlo, rhi = [], [], []
    extra = []
    cnt = [nvar]

    def new(l=0, u=1):
        extra.append((l, u))
        cnt[0] += 1
        return cnt[0] - 1

    def row(cs, l, h):
        rows.append(cs); rlo.append(l); rhi.append(h)
    w = {}
    for P, (i0, i1) in sib.items():
        for R in PAIRS:
            if set(R) & set(P):
                continue
            ws = {s: new() for s in STATES}
            w[(P, R)] = ws
            row([(v, 1) for v in ws.values()], 1, 1)
            row([(phi[(i0, R)], 1)] + [(ws[s], -PHIVAL[s]) for s in STATES], 0, 0)
    if altalt:
        for P, P2 in itertools.combinations(sorted(sib), 2):
            if not (set(P) & set(P2)):
                continue
            rest = set(range(N)) - set(P) - set(P2)
            terms = []
            for R in itertools.combinations(sorted(rest), 2):
                R = pr(*R)
                joint = {(s1, s2): new() for s1 in STATES for s2 in STATES}
                row([(v, 1) for v in joint.values()], 1, 1)
                for s1 in STATES:
                    row([(joint[(s1, s2)], 1) for s2 in STATES] + [(w[(P, R)][s1], -1)], 0, 0)
                for s2 in STATES:
                    row([(joint[(s1, s2)], 1) for s1 in STATES] + [(w[(P2, R)][s2], -1)], 0, 0)
                terms += [(joint[(s1, s2)], prod(s1, s2)) for s1 in STATES for s2 in STATES if prod(s1, s2)]
            row(terms, 0, 0)

    def times_binary(coefs, bvar, M):
        """new var p = (sum coefs) * b exactly, with |sum coefs| <= M (integers)."""
        p = new(-M, M)
        # p <= M b, p >= -M b, p - S <= M(1-b), p - S >= -M(1-b)
        row([(p, 1), (bvar, -M)], -np.inf, 0)
        row([(p, 1), (bvar, M)], 0, np.inf)
        row([(p, 1)] + [(v, -c) for v, c in coefs] + [(bvar, M)], -np.inf, M)
        row([(p, 1)] + [(v, -c) for v, c in coefs] + [(bvar, -M)], -M, np.inf)
        return p
    if symalt:
        for P, (i0, i1) in sib.items():
            disj = [X for X in PAIRS if not (set(X) & set(P))]
            for Y in PAIRS:
                Y0, Y1 = by_pair[Y]
                terms = []
                for X in disj:
                    X0, X1 = by_pair[X]
                    ws = w[(P, X)]
                    qs = [(phi[(Y0, X)], 1), (phi[(Y1, X)], 1)]              # 2 (Q_S)_{YX}, in [0,6]
                    kk = [(phi[(X0, Y)], 1), (phi[(X1, Y)], -1)]             # 2 K_{YX}, in [-3,3]
                    terms.append((times_binary(qs, ws['K+'], 6), 1))
                    terms.append((times_binary(qs, ws['K-'], 6), -1))
                    terms.append((times_binary(kk, ws['A+'], 3), 1))
                    terms.append((times_binary(kk, ws['A-'], 3), -1))
                row(terms + [(phi[(i0, Y)], -1), (phi[(i1, Y)], 1)], 0, 0)
    n2 = cnt[0]
    A2 = np.zeros((A.shape[0] + len(rows), n2))
    A2[:A.shape[0], :nvar] = A
    for r, cs in enumerate(rows):
        for j, c in cs:
            A2[A.shape[0] + r, j] += c
    lb2 = np.concatenate([lb, [e[0] for e in extra]])
    ub2 = np.concatenate([ub, [e[1] for e in extra]])
    integ = np.ones(n2)
    return A2, np.concatenate([lo, rlo]), np.concatenate([hi, rhi]), lb2, ub2, n2, integ
