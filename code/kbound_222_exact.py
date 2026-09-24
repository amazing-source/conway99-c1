"""k = 8 with a (2,2,2) star: exact check of the candidate annihilators A found by kbound_star (32 subspaces).

Unknowns: for each column z outside star(a):
  generic z = {l,q} (a, abar not in z): its two star neighbours {a,b1},{a,b2} (pair, not tau_a-partners);
  z = {abar,q}: its unique star neighbour {a,b1}.
Constraints (all consequences of lambda = 1, mu = 2 at x):
  (deg)   each star vertex {a,b} has exactly 10 neighbours among the 60 generic z and exactly 1 in star(abar);
  (label) for each star label l: {a,l} ~ {l,q} iff tau_l(a) = q, so exactly one column containing l (generic, or
          {abar,l}) lists l among its star neighbours;
  (lin)   the functional of the chosen neighbours (kbound_star) lies in A.
If every A is UNSAT, k = 8 is impossible (with L20: k >= 10).
"""
import itertools, pickle, sys
import numpy as np
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153
import kbound_star as ks

p = 7


def in_span(R, piv, v):
    v = v.copy() % p
    for i, c in enumerate(piv):
        v = (v - v[c] * R[i]) % p
    return not v.any()


def main():
    tau = ks.type_reps()['(0;2,2,2)']
    others, oi, mate, abar = ks.others, ks.oi, ks.mate, ks.abar
    Kb, found = pickle.load(open('../data/kbound_A222.pkl', 'rb'))
    d = Kb.shape[0]
    cval = {b: Kb[:, oi[b]] for b in others}
    ssum = Kb.sum(axis=1) % p
    generic = [(l, q) for l, q in itertools.combinations(others, 2) if l[0] != q[0]]
    results = []
    for n_A, key in enumerate(sorted(found)):
        A = np.array(key, dtype=np.int64)
        R, piv = ks.rref(A)
        pool = IDPool(); cnf = CNF()
        inc = {b: [] for b in others}          # generic incidences of b
        lab = {l: [] for l in others}          # incidences where a label of z is listed
        for (l, q) in generic:
            base = (3 * (cval[l] + cval[q]) + cval[mate(l)] + cval[mate(q)] + 5 * ssum) % p
            opts = []
            for b1, b2 in itertools.combinations(others, 2):
                if tau[b1] == b2:
                    continue
                if in_span(R, piv, (base + cval[b1] + cval[b2]) % p):
                    v = pool.id(('g', l, q, b1, b2)); opts.append(v)
                    inc[b1].append(v); inc[b2].append(v)
                    for bb in (b1, b2):
                        if bb in (l, q):
                            lab[bb].append(v)
            if not opts:
                cnf.append([]); break
            cnf.extend(CardEnc.equals(opts, 1, vpool=pool, encoding=EncType.seqcounter).clauses)
        match = {b: [] for b in others}
        for q in others:
            base = (3 * cval[q] + cval[mate(q)] + 6 * ssum) % p
            opts = []
            for b in others:
                if in_span(R, piv, (base + cval[b]) % p):
                    v = pool.id(('s', q, b)); opts.append(v); match[b].append(v)
                    if b == q:
                        lab[q].append(v)
            if not opts:
                cnf.append([]); break
            cnf.extend(CardEnc.equals(opts, 1, vpool=pool, encoding=EncType.seqcounter).clauses)
        for b in others:
            cnf.extend(CardEnc.equals(inc[b], 10, vpool=pool, encoding=EncType.seqcounter).clauses if inc[b] else [[]])
            cnf.extend(CardEnc.equals(match[b], 1, vpool=pool, encoding=EncType.seqcounter).clauses if match[b] else [[]])
            cnf.extend(CardEnc.equals(lab[b], 1, vpool=pool, encoding=EncType.seqcounter).clauses if lab[b] else [[]])
        with Cadical153(bootstrap_with=cnf.clauses) as s:
            r = s.solve()
        results.append(r)
        print(f'A #{n_A}: {"SAT" if r else "UNSAT"}', flush=True)
    print('summary:', 'ALL UNSAT -> k = 8 impossible' if not any(results) else f'{sum(results)} of {len(results)} SAT')


if __name__ == '__main__':
    main()
