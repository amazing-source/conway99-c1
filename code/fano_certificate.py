"""notes/104 §8: explicit inconsistency certificate of the kappa system for the surviving configuration
(Fano plane {0,1,3}+d, C = {01, 02, 15, 25}): a set of equations whose left sides cancel and whose
constants sum to 1.  Found by Gaussian elimination with provenance, then shrunk greedily."""
import pickle, itertools
from kappa_linear_system import system, pairs, disjoint

surv = pickle.load(open('../data/fano_bc_survivors.pkl', 'rb'))
import sys
WHICH = int(sys.argv[1]) if len(sys.argv) > 1 else 0
C, st = surv[WHICH]
print('survivor', WHICH, 'C =', C)
nu = {e for e, s in st.items() if s == 1}
eqs, var = system(nu)

# label equations
labels = []
for P in pairs:
    for m in range(7):
        if m not in P:
            labels.append(('Z_A', P, m))
nZ = len(labels)
from kappa_linear_system import triangles
for t in triangles:
    for R in t:
        P, P2 = [Q for Q in t if Q != R]
        if frozenset((P, P2)) not in nu and frozenset((P, R)) in nu and frozenset((P2, R)) in nu:
            labels.append(('(i)', P, P2, R))
for i in range(7):
    for j, k in itertools.combinations([c for c in range(7) if c != i], 2):
        labels.append(("(C')", i, j, k))
assert len(labels) == len(eqs)

def rowbits(vs, c):
    r = c
    for v in vs:
        r |= 1 << (v + 1)
    return r

def find_cert(idx):
    basis = {}
    for n in idx:
        r = rowbits(*eqs[n])
        prov = 1 << n
        while r >> 1:
            top = r.bit_length() - 1
            if top in basis:
                r ^= basis[top][0]
                prov ^= basis[top][1]
            else:
                basis[top] = (r, prov)
                break
        else:
            if r & 1:
                return [m for m in range(len(eqs)) if prov >> m & 1]
    return None

cert = find_cert(range(len(eqs)))
# greedy shrink: try removing equations not in the certificate span
cur = list(cert)
changed = True
while changed:
    changed = False
    for n in list(cur):
        trial = [m for m in cur if m != n]
        c2 = find_cert(trial)
        if c2 is not None:
            cur = c2
            changed = True
            break
# verify
tot_vars, tot_c = set(), 0
for n in cur:
    vs, c = eqs[n]
    tot_vars ^= vs
    tot_c ^= c
print('certificate size', len(cur), ' variables left', len(tot_vars), ' constant', tot_c)
from collections import Counter
print(Counter(labels[n][0] for n in cur))
for n in sorted(cur, key=lambda m: labels[m]):
    print('  ', labels[n])
