"""Alt identities between sib pairs (C1, 26/09 night), both cases, added to the labeled sib pair model.

For sib P and R disjoint from P, the 2x2 block between P and R is 'perm' ((Q_A)_PR = +-1, K_RP = 0) or '(2,0)'
(K_RP = phi_P0(R) - 1 = +-1, (Q_A)_PR = 0).  One-hot per (P, R): {A+, A-, K+, K-}.  If R is sib too the block is a perfect
matching (A-type) and (Q_A)_PR = (Q_A)_RP: the A-signs of (P,R) and (R,P) are tied.
Entry (P, P') of Q_A^2 + Q_A + K^T K = 12 I:
  * P, P' share a block t (P = ta, P' = tb):  sum_{R inside [7]-{t,a,b}} <v_PR, v_P'R> = 0               (6 pairs R)
  * P, P' disjoint:                            sum_{Y inside [7]-P-P'} <v_PY, v_P'Y> = 3 (Q_A)_PP'  (3 pairs Y)
    [(Q_A^2)_PP' = -4 (Q_A)_PP' + sum_Y ..., (Q_A)_PP' = +-1, K_P'P = 0].
<v, v'> = product of signs if same axis, 0 otherwise."""
import itertools
import numpy as np
from general_model import N, PAIRS, pr

STATES = ['A+', 'A-', 'K+', 'K-']
PHIVAL = {'A+': 1, 'A-': 1, 'K+': 2, 'K-': 0}


def prod(s1, s2):
    if s1[0] != s2[0]:
        return 0
    return 1 if s1[1] == s2[1] else -1


def add_alt_sib_all(A, lo, hi, lb, ub, nvar, phi, orbs, shared=True, disjoint=True):
    sib = {}
    for i, o in enumerate(orbs):
        if o['pivot'] == 'sib':
            sib.setdefault(o['pair'], []).append(i)
    rows, rlo, rhi, extra = [], [], [], []
    cnt = [nvar]

    def new():
        extra.append((0, 1))
        cnt[0] += 1
        return cnt[0] - 1

    def row(cs, l, h):
        rows.append(cs)
        rlo.append(l)
        rhi.append(h)
    w = {}
    for P, (i0, i1) in sib.items():
        for R in PAIRS:
            if set(R) & set(P):
                continue
            ws = {s: new() for s in STATES}
            w[(P, R)] = ws
            row([(v, 1) for v in ws.values()], 1, 1)
            row([(phi[(i0, R)], 1)] + [(ws[s], -PHIVAL[s]) for s in STATES], 0, 0)
    for P, P2 in itertools.combinations(sorted(sib), 2):
        if not (set(P) & set(P2)):
            row([(w[(P, P2)]['A+'], 1), (w[(P2, P)]['A+'], -1)], 0, 0)
            row([(w[(P, P2)]['A-'], 1), (w[(P2, P)]['A-'], -1)], 0, 0)
    nid = 0
    for P, P2 in itertools.combinations(sorted(sib), 2):
        share = bool(set(P) & set(P2))
        if (share and not shared) or (not share and not disjoint):
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
        if not share:
            terms += [(w[(P, P2)]['A+'], -3), (w[(P, P2)]['A-'], 3)]
        row(terms, 0, 0)
        nid += 1
    n2 = cnt[0]
    A2 = np.zeros((A.shape[0] + len(rows), n2))
    A2[:A.shape[0], :nvar] = A
    for r, cs in enumerate(rows):
        for j, c in cs:
            A2[A.shape[0] + r, j] += c
    lb2 = np.concatenate([lb, [e[0] for e in extra]])
    ub2 = np.concatenate([ub, [e[1] for e in extra]])
    return A2, np.concatenate([lo, rlo]), np.concatenate([hi, rhi]), lb2, ub2, n2, nid
