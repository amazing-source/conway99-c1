"""Alt identity between two sib pairs sharing a block (C1, 26/09 night; generalises the step of C2's Theorem D).

On Alt (a_P = (e_P0 - e_P1)/sqrt2) the orbit matrix satisfies Q_A^2 + Q_A + K^T K = 12 I (C2 carnet sec. 8), with
(Q_A)_{PR} = (q00 + q11 - q01 - q10)/2 and K_{RP} = (phi_{P0}(R) - phi_{P1}(R))/2.
For a sib pair P (8.1: every root disjoint from P has exactly one neighbour in P, roots meeting P have none):
  (Q_A)_{PR} = K_{RP} = 0 if R meets P (R != P);  (Q_A)_{PP} = -2;  for R disjoint: exactly one of
  (Q_A)_{PR} = +-1 ("perm") or K_{RP} = phi_{P0}(R) - 1 = +-1 ("(2,0)").
For sib P = ta, P' = tb (P, P' share t): (Q_A)_{PP'} = 0 and the (P,P') entry gives
  sum_{R inside [7] - {t,a,b}} [ (Q_A)_{PR}(Q_A)_{P'R} + K_{RP} K_{RP'} ] = 0      (6 pairs R).
This module adds it to the labeled sib model: per (sib P, disjoint R) a 4-state one-hot {A+, A-, K+, K-} tied to
phi_{P0}(R) (K+ <=> phi = 2, K- <=> phi = 0, A+- <=> phi = 1, sign free), and per (P, P', R) a joint one-hot."""
import itertools
import numpy as np
from general_model import N, PAIRS, pr

STATES = ['A+', 'A-', 'K+', 'K-']
PHIVAL = {'A+': 1, 'A-': 1, 'K+': 2, 'K-': 0}


def prod(s1, s2):
    if s1[0] != s2[0]:
        return 0
    return 1 if s1[1] == s2[1] else -1


def add_alt_sib(A, lo, hi, lb, ub, nvar, phi, orbs):
    """returns enlarged (A, lo, hi, lb, ub, nvar) with the Alt identity for every two sib pairs sharing a block."""
    sib = {}
    for i, o in enumerate(orbs):
        if o['pivot'] == 'sib':
            sib.setdefault(o['pair'], []).append(i)
    rows, rlo, rhi = [], [], []
    extra = []                                   # (lb, ub) of new variables
    cnt = [nvar]

    def new():
        extra.append((0, 1))
        cnt[0] += 1
        return cnt[0] - 1
    w = {}
    for P, (i0, i1) in sib.items():
        for R in PAIRS:
            if set(R) & set(P):
                continue
            ws = {s: new() for s in STATES}
            w[(P, R)] = ws
            rows.append([(v, 1) for v in ws.values()]); rlo.append(1); rhi.append(1)
            rows.append([(phi[(i0, R)], 1)] + [(ws[s], -PHIVAL[s]) for s in STATES]); rlo.append(0); rhi.append(0)
    npairs = 0
    for P, P2 in itertools.combinations(sorted(sib), 2):
        if not (set(P) & set(P2)):
            continue
        npairs += 1
        rest = set(range(N)) - set(P) - set(P2)
        terms = []
        for R in itertools.combinations(sorted(rest), 2):
            R = pr(*R)
            joint = {}
            for s1 in STATES:
                for s2 in STATES:
                    joint[(s1, s2)] = new()
            rows.append([(v, 1) for v in joint.values()]); rlo.append(1); rhi.append(1)
            for s1 in STATES:
                rows.append([(joint[(s1, s2)], 1) for s2 in STATES] + [(w[(P, R)][s1], -1)]); rlo.append(0); rhi.append(0)
            for s2 in STATES:
                rows.append([(joint[(s1, s2)], 1) for s1 in STATES] + [(w[(P2, R)][s2], -1)]); rlo.append(0); rhi.append(0)
            terms += [(joint[(s1, s2)], prod(s1, s2)) for s1 in STATES for s2 in STATES if prod(s1, s2)]
        rows.append(terms); rlo.append(0); rhi.append(0)
    n2 = cnt[0]
    A2 = np.zeros((A.shape[0] + len(rows), n2))
    A2[:A.shape[0], :nvar] = A
    for r, cs in enumerate(rows):
        for j, c in cs:
            A2[A.shape[0] + r, j] += c
    lb2 = np.concatenate([lb, [e[0] for e in extra]])
    ub2 = np.concatenate([ub, [e[1] for e in extra]])
    return A2, np.concatenate([lo, rlo]), np.concatenate([hi, rhi]), lb2, ub2, n2, npairs
