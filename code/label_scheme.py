"""Local Delsarte bound on the label scheme at a vertex x (pure linear algebra, instantaneous).

X = Gamma_2(x) = the 84 non-mate pairs of the 14 labels (7 classes).  The hyperoctahedral group B_7 acts on X with
6 orbitals: R0 (equal), Ra (share a label, other two mates; valency 2), Rsig (w = sigma_x z; 1),
Rsh (share a label, others in different classes; 20), Rcl (disjoint labels, one class shared; 20),
Rdj (disjoint labels and classes; 40).
Edge counts of H = Gamma[X] per relation (derived in notes/91):  Ra: 84 - W, Rsh: W, Rsig: s/2, Rcl: W - s,
Rdj: 420 - W + s/2   (W = |W(x)|, s = s(x) = #{E : E ~ sigma_x E}).
H has eigenvalues 3 (x40) and -4 (x30) on K = ker B^T (70-dim) and acts as Phi on K^perp.
For each irreducible B_7-module V_i in K:  tr(H E_i) = 3 d_i - 7 c_i with c_i = tr(E_i P_{-4}) in [0, min(d_i, 30)].
"""
import itertools
import numpy as np
from fractions import Fraction

labels = list(range(14))
mate = {a: a ^ 1 for a in labels}
cls = {a: a // 2 for a in labels}
X = [frozenset(p) for p in itertools.combinations(labels, 2) if mate[p[0]] != p[1]]
assert len(X) == 84


def rel(z, w):
    if z == w:
        return 'R0'
    inter = z & w
    if len(inter) == 1:
        (u,) = z - w
        (v,) = w - z
        return 'Ra' if mate[u] == v else 'Rsh'
    cz = {cls[a] for a in z}
    cw = {cls[a] for a in w}
    k = len(cz & cw)
    return {2: 'Rsig', 1: 'Rcl', 0: 'Rdj'}[k]


names = ['R0', 'Ra', 'Rsig', 'Rsh', 'Rcl', 'Rdj']
Amat = {r: np.zeros((84, 84)) for r in names}
for i, z in enumerate(X):
    for j, w in enumerate(X):
        Amat[rel(z, w)][i, j] = 1
val = {r: int(Amat[r][0].sum()) for r in names}
print('valencies', val)

# primitive idempotents via a generic element of the Bose-Mesner algebra
rng = np.random.default_rng(1)
G = sum(rng.normal() * Amat[r] for r in names)
ev, U = np.linalg.eigh(G)
groups = []
for e, u in zip(ev, U.T):
    for g in groups:
        if abs(g[0] - e) < 1e-6:
            g[1].append(u)
            break
    else:
        groups.append([e, [u]])
idem = []
for e, vs in groups:
    V = np.array(vs).T
    idem.append(V @ V.T)
# label space K^perp
B = np.array([[1 if a in z else 0 for a in labels] for z in X], dtype=float)
PKp = B @ np.linalg.pinv(B)
for E in idem:
    d = round(np.trace(E))
    inKp = np.allclose(PKp @ E, E, atol=1e-8)
    inK = np.allclose(PKp @ E, 0, atol=1e-8)
    vals = {r: E[np.nonzero(Amat[r])][0] for r in names}
    # tr(H E) as a function of W, s: sum_r 2*count_r * value_r  (+ diagonal 0)
    # counts: Ra 84-W, Rsh W, Rsig s/2, Rcl W-s, Rdj 420-W+s/2
    c0 = 2 * (84 * vals['Ra'] + 420 * vals['Rdj'])
    cW = 2 * (-vals['Ra'] + vals['Rsh'] + vals['Rcl'] - vals['Rdj'])
    cs = 2 * (0.5 * vals['Rsig'] - vals['Rcl'] + 0.5 * vals['Rdj'])
    tag = 'K^perp' if inKp else ('K' if inK else '??')
    print(f'dim {d:2d} [{tag}]  tr(H E) = {c0:+.6f} {cW:+.6f}*W {cs:+.6f}*s   values:',
          {r: round(v * 84, 6) for r, v in vals.items()})
