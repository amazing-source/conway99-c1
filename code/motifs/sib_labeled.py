"""Labeled copy of structures' build_sib (ad/sib_model.py, written by C1) for proof extraction: every row carries a group
label; bounds are kept as facts.  Same constraints, same variables."""
import itertools, sys
import numpy as np
sys.path.insert(0, r"C:/home/researcher/Desktop/c99_structures_lab/ad")
from general_model import N, PAIRS, pr
from sib_model import check_skeleton_sib, sib_pairs, components_sib


def build_sib_labeled(orbs, dichotomy=True, balance=True):
    check_skeleton_sib(orbs)
    sibs = sib_pairs(orbs)
    n_orb = len(orbs)
    by_pair = {P: [i for i, o in enumerate(orbs) if o['pair'] == P] for P in PAIRS}
    both_dis = {P: all(orbs[i]['pivot'] is None for i in by_pair[P]) for P in PAIRS}
    cnt = [0]

    def new(n=1):
        a = cnt[0]
        cnt[0] += n
        return a
    phi = {(i, P): new() for i in range(n_orb) for P in PAIRS}
    ns = {P: new() for P in PAIRS if both_dis[P]}
    y = {}
    if dichotomy:
        for i in range(n_orb):
            for P in PAIRS:
                if P != orbs[i]['pair']:
                    y[(i, P)] = new(4)
    xv = {}
    freeorb = [i for i, o in enumerate(orbs) if o['partner'] is None]
    for i, j in itertools.combinations(freeorb, 2):
        if orbs[i]['pivot'] == orbs[j]['pivot'] and orbs[i]['pair'] != orbs[j]['pair']:
            xv[(i, j)] = new()
    nvar = cnt[0]
    lb = np.zeros(nvar)
    ub = np.full(nvar, 3.0)
    for key in xv.values():
        ub[key] = 1
    rows, lo, hi, lab = [], [], [], []

    def add(coefs, l, h, g):
        rows.append(coefs)
        lo.append(l)
        hi.append(h)
        lab.append(g)
    comps = {k: components_sib(orbs, k, sibs) for k in range(N)}
    for i, o in enumerate(orbs):
        P = o['pair']
        a, b = P
        if o['pivot'] == 'sib':
            lb[phi[(i, P)]] = ub[phi[(i, P)]] = 2
        elif P in ns:
            add([(phi[(i, P)], 1), (ns[P], -1)], 0, 0, ('ns', i))
        else:
            ub[phi[(i, P)]] = 0
        for t in (a, b):
            add([(phi[(i, pr(t, m))], 1) for m in range(N) if m != t], 2, 2, ('F1', i, t))
            if o['pivot'] == 'sib':
                for m in range(N):
                    if m != t and pr(t, m) != P:
                        ub[phi[(i, pr(t, m))]] = 0
                continue
            for m in range(N):
                if m != t and pr(t, m) in sibs and pr(t, m) != P:
                    ub[phi[(i, pr(t, m))]] = 0
            if o['pivot'] == t and o['partner'] is None:
                raise NotImplementedError
            elif o['pivot'] == t:
                q = orbs[o['partner']]['pair']
                for m in range(N):
                    if m == t:
                        continue
                    j = phi[(i, pr(t, m))]
                    if pr(t, m) == q:
                        lb[j] = ub[j] = 2
                    else:
                        ub[j] = 0
            else:
                for m in range(N):
                    if m == t or pr(t, m) == P or pr(t, m) in sibs:
                        continue
                    cap = sum(1 for j2 in by_pair[pr(t, m)] if orbs[j2]['pivot'] != t)
                    ub[phi[(i, pr(t, m))]] = min(ub[phi[(i, pr(t, m))]], cap)
        if balance:
            for k in range(N):
                if k in P:
                    continue
                closed, rest = comps[k]
                for S in closed + ([rest] if rest else []):
                    add([(phi[(i, pr(k, m))], 1) for m in S], len(S - {a, b}), len(S - {a, b}),
                        ('bal', i, k, tuple(sorted(S))))
        if o['pivot'] is None:
            j = phi[(i, orbs[o['partner']]['pair'])]
            lb[j] = max(lb[j], 2)
    for P, P2 in itertools.combinations(PAIRS, 2):
        add([(phi[(i, P2)], 1) for i in by_pair[P]] + [(phi[(i, P)], -1) for i in by_pair[P2]], 0, 0, ('sym', P, P2))
    for P in ns:
        ub[ns[P]] = 1
    if dichotomy:
        for (i, P), yy in y.items():
            for f in range(4):
                ub[yy + f] = 1
            add([(yy + f, 1) for f in range(4)], 1, 1, ('ydef', i, P))
            add([(phi[(i, P)], 1)] + [(yy + f, -f) for f in range(4)], 0, 0, ('ydef', i, P))
            if orbs[i]['partner'] is None:
                ub[yy + 3] = 0
                continue
            is_partner = orbs[orbs[i]['partner']]['pair'] == P
            if not (is_partner and orbs[i]['pivot'] is None):
                ub[yy + 3] = 0
        for P in PAIRS:
            coefs = []
            partners = {orbs[j]['partner'] for j in by_pair[P] if orbs[j]['partner'] is not None}
            for i in range(n_orb):
                if orbs[i]['pair'] == P:
                    continue
                yy = y[(i, P)]
                if orbs[i]['partner'] is None:
                    coefs.append((yy + 2, 1))
                    for j in by_pair[P]:
                        if pr(i, j) in xv:
                            coefs.append((xv[pr(i, j)], -1))
                    continue
                if i not in partners:
                    coefs.append((yy + 2, 1))
                coefs.append((yy + 3, 2))
            if P in sibs:
                add(coefs, 0, 0, ('dich', P))
                continue
            if P in ns:
                coefs.append((ns[P], 1))
            add(coefs, 2, 2, ('dich', P))
    A = np.zeros((len(rows), nvar))
    for r, cs in enumerate(rows):
        for j, c in cs:
            A[r, j] += c
    return A, np.array(lo, float), np.array(hi, float), lb, ub, nvar, phi, ns, y, lab
