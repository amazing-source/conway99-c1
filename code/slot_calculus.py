"""notes/108-109: the slot calculus at a vertex x, for a given twisting configuration (tau, rho).
Only necessary conditions proved in notes/108 are used:
  specials: for y = {a,b}, the neighbours containing a, b, abar, bbar are exactly
            T_a(y) = {a, tau_a(b)}, T_b(y) = {b, tau_b(a)}, S_alpha(y) = {abar, rho(b)}, S_beta(y) = {bbar, rho(a)};
  (F) for each class m outside P(y): sum_{R ni m, R disjoint from P(y)} n_R(y) = 4 - s_m(y);
  (Q) n_R(y) <= 1 whenever the pair R is complete (its quadrangle has label apexes);
  (C) sum_{y in Q_P} n_R(y) = sum_{w in Q_R} n_P(w) for every Kneser pair {P, R};
  n >= 0 integer.
Exact interval propagation; returns the propagation log on contradiction (a human-readable argument)."""
import itertools
from fractions import Fraction

CL = range(7)
LAB = [(c, s) for c in CL for s in (0, 1)]
def mate(l): return (l[0], 1 - l[1])
PAIRS = [frozenset(p) for p in itertools.combinations(CL, 2)]
VERT = [frozenset((a, b)) for a, b in itertools.combinations(LAB, 2) if a[0] != b[0]]   # 84
def cls(v): return frozenset(l[0] for l in v)

class Config:
    """tau[l]: dict label->label (perfect matching on labels outside class(l));
       rho[c]: dict label->label, the shadow map star(c,0) -> star(c,1): {(c,0), z} ~ {(c,1), rho[c][z]}."""
    def __init__(self, tau, rho):
        self.tau, self.rho = tau, rho
    def twists(self, l, c):
        return self.tau[l][(c, 0)] != (c, 1)
    def incomplete(self):
        out = set()
        for P in PAIRS:
            a, b = sorted(P)
            if any(self.twists(l, b) for l in LAB if l[0] == a) or any(self.twists(l, a) for l in LAB if l[0] == b):
                out.add(P)
        return out
    def specials(self, y):
        a, b = sorted(y)
        sp = set()
        sp.add(frozenset((a, self.tau[a][b])))
        sp.add(frozenset((b, self.tau[b][a])))
        for (u, v) in ((a, b), (b, a)):          # shadow of y via class(u): the neighbour containing mate(u)
            c = u[0]
            if u[1] == 0:
                sp.add(frozenset((mate(u), self.rho[c][v])))
            else:
                inv = {w: z for z, w in self.rho[c].items()}
                sp.add(frozenset((mate(u), inv[v])))
        return sp

def build(cfg):
    inc = cfg.incomplete()
    var = {}
    lo, hi = [], []
    for y in VERT:
        P = cls(y)
        for R in PAIRS:
            if not (R & P):
                var[(y, R)] = len(lo)
                lo.append(0)
                hi.append(1 if R not in inc else 4)
    eqs = []   # (coef dict, rhs, label)
    for y in VERT:
        P = cls(y)
        sp = cfg.specials(y)
        for m in CL:
            if m in P:
                continue
            s_m = sum(1 for z in sp for l in z if l[0] == m)
            coef = {var[(y, R)]: 1 for R in PAIRS if m in R and not (R & P)}
            eqs.append((coef, 4 - s_m, ('F', tuple(sorted(y)), m)))
    for P, R in itertools.combinations(PAIRS, 2):
        if P & R:
            continue
        coef = {}
        for y in VERT:
            if cls(y) == P:
                coef[var[(y, R)]] = coef.get(var[(y, R)], 0) + 1
            if cls(y) == R:
                coef[var[(y, P)]] = coef.get(var[(y, P)], 0) - 1
        eqs.append((coef, 0, ('C', tuple(sorted(P)), tuple(sorted(R)))))
    return var, lo, hi, eqs, inc

def propagate(lo, hi, eqs, max_rounds=200):
    lo, hi = list(lo), list(hi)
    log = []
    for _ in range(max_rounds):
        changed = False
        for coef, rhs, lab in eqs:
            for j, a in coef.items():
                rest_lo = sum((c * lo[k] if c > 0 else c * hi[k]) for k, c in coef.items() if k != j)
                rest_hi = sum((c * hi[k] if c > 0 else c * lo[k]) for k, c in coef.items() if k != j)
                # a*x_j = rhs - rest, rest in [rest_lo, rest_hi]
                if a > 0:
                    nlo = -(-(rhs - rest_hi) // a)
                    nhi = (rhs - rest_lo) // a
                else:
                    nlo = -(-(rhs - rest_lo) // a) if False else -((rhs - rest_lo) // (-a)) * 1
                    # a<0: x_j = (rest - rhs)/(-a)
                    nlo = -(-(rest_lo - rhs) // (-a))
                    nhi = (rest_hi - rhs) // (-a)
                if nlo > lo[j]:
                    lo[j] = nlo; changed = True; log.append((lab, j, 'lo', nlo))
                if nhi < hi[j]:
                    hi[j] = nhi; changed = True; log.append((lab, j, 'hi', nhi))
                if lo[j] > hi[j]:
                    log.append((lab, j, 'EMPTY', (lo[j], hi[j])))
                    return False, lo, hi, log
        if not changed:
            return True, lo, hi, log
    return True, lo, hi, log
