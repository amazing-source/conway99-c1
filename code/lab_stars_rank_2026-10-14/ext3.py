"""Fourth-star column test for a three-star structure of rank 30 (LAB 15/10/2026), EXACT.

Setting: stars 0, 1 (line l) and 2 (mate 3); S3 = L_0 u L_1 u L_2 (34 labels).  If T_S3 has rank 30 (the label vectors
of S3 span the whole 30-space, as for the counterexamples to (A)), every label u = {3,y} (y outer) of the fourth star
has its vector fixed by its profile nb = N(u) n S3: (Tr) p = T(S3,u) is orthogonal to ker T_S3 and (Tn)
p^T T_S3^+ p = 5/2.  This is needed for ANY four-star structure (stars 0,1,2,3) containing S3 with rank T_S4 = 30
(and of course for a Conway graph); it is Codex's column filter in this setting.
Admissible profiles: exactly 2 labels in L_0 and in L_1 (mu with the letters 0, 1), exactly 1 in L_2 (2 is the mate of
3), at most one of {0,3}, {1,3} (the tau_3 partner), partial counts (C1') towards every other letter, caps (C2).
(B') link: a four-star structure with c(l) = 1 and rank <= 30 contains such an S3 of rank <= 30, so if every label of
L_3 \\ X_l passes, a rank-30 completion is not excluded by this test; if one label has no profile, no rank-30
four-star completion of S3 exists.
usage: python ext3.py <json: labels (34) + edges | structures[k].edges> [k] [first]"""
import itertools
import json
import sys
from fractions import Fraction as Fr

import numpy as np

from ext4 import kval, need, rref_kernel, exact_norm, int_rows, MATE


def main():
    d = json.load(open(sys.argv[1]))
    if "structures" in d:
        k = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        edges = d["structures"][k]["edges"]
    else:
        edges = d["edges"]
    S = [frozenset(l) for l in d["labels"]]
    n = len(S)
    assert set(S) == {frozenset((a, x)) for a in (0, 1, 2) for x in range(14) if x not in (a, MATE(a))}, "not S3"
    Gl = [[0] * n for _ in range(n)]
    for i, j in edges:
        Gl[i][j] = Gl[j][i] = 1
    G = np.array(Gl, dtype=np.int64)
    T = [[(3 if i == j else 0) - Gl[i][j] - kval(S[i], S[j]) for j in range(n)] for i in range(n)]
    rT, kT = rref_kernel(T)
    print("rank T_S3 = %d (nullity %d)" % (rT, n - rT))
    if rT != 30:
        print("rank != 30: the fourth-star vectors are not fixed by their profiles; stop")
        return
    KTi = int_rows(kT)
    # speed-up (15/10): for p in range(T), p^T T^+ p = p_I^T (T_II)^-1 p_I with I a set of 30 independent rows
    Ib, rI, Ainv = [], 0, None
    Mrows = [[Fr(x) for x in row] for row in T]
    basis = []
    for i in range(n):
        trial = basis + [i]
        Msub = [[Mrows[a][b] for b in trial] for a in trial]
        if rref_kernel(Msub)[0] == len(trial):
            basis = trial
        if len(basis) == rT:
            break
    TI = [[Mrows[a][b] for b in basis] for a in basis]
    m = len(basis)
    aug = [TI[r][:] + [Fr(1) if c == r else Fr(0) for c in range(m)] for r in range(m)]
    for c in range(m):
        piv = next(r for r in range(c, m) if aug[r][c] != 0)
        aug[c], aug[piv] = aug[piv], aug[c]
        pv = aug[c][c]
        aug[c] = [x / pv for x in aug[c]]
        for r in range(m):
            if r != c and aug[r][c] != 0:
                f = aug[r][c]
                aug[r] = [x - f * y for x, y in zip(aug[r], aug[c])]
    TIinv = [row[m:] for row in aug]

    def norm_fast(p):
        pI = [p[i] for i in basis]
        w = [sum(TIinv[r][c] * pI[c] for c in range(m)) for r in range(m)]
        return sum(a * b for a, b in zip(pI, w))
    star = {s: [i for i in range(n) if s in S[i]] for s in (0, 1, 2)}
    i30 = [i for i in range(n) if S[i] in (frozenset((0, 3)), frozenset((1, 3)))]
    Lmat = np.array([[1 if z in S[i] else 0 for z in range(14)] for i in range(n)], dtype=np.int64)
    summary = {}
    for y in range(4, 14):
        u = frozenset((3, y))
        K8 = np.array([int(8 * kval(S[i], u)) for i in range(n)], dtype=np.int64)
        shared = np.array([len(S[i] & u) for i in range(n)], dtype=np.int64)
        needv = np.array([need(u, z) for z in range(14)], dtype=np.int64)
        rows = []
        for A0 in itertools.combinations(star[0], 2):
            for A1 in itertools.combinations(star[1], 2):
                base = np.zeros(n, dtype=np.int64)
                base[list(A0)] = 1
                base[list(A1)] = 1
                c2 = int(sum(base[i] for i in star[2]))
                if c2 > 1:
                    continue
                rest2 = [i for i in star[2] if not (S[i] & {0, 1})]
                choices = [()] if c2 == 1 else [(i,) for i in rest2]
                for b2 in choices:
                    x = base.copy()
                    x[list(b2)] = 1
                    if int(sum(x[i] for i in i30)) > 1:
                        continue
                    cnt = x @ Lmat
                    if not (cnt[0] == 2 and cnt[1] == 2 and cnt[2] == 1):
                        continue
                    if not np.all(cnt[4:] <= needv[4:]):
                        continue
                    if cnt[3] > 1:
                        continue
                    common = G @ x + shared
                    if not np.all(common <= 2 - x):
                        continue
                    rows.append(x)
        X = np.array(rows, dtype=np.int64) if rows else np.zeros((0, n), dtype=np.int64)
        R = (8 * X + K8[None, :]) @ KTi.T
        tr = np.all(R == 0, axis=1)
        nTn = 0
        vals = set()
        for x in X[tr]:
            p = [-int(x[i]) - kval(S[i], u) for i in range(n)]
            nv = norm_fast(p)
            vals.add(str(nv - Fr(5, 2)))
            if nv == Fr(5, 2):
                nTn += 1
        summary["3,%d" % y] = [int(len(X)), int(tr.sum()), nTn]
        fv = sorted(Fr(v) for v in vals)
        print("label {3,%d}: %d admissible profiles; (Tr) %d; (Tr)+(Tn) %d; residues p^T T^+ p - 5/2 in [%s, %s]"
              % (y, len(X), int(tr.sum()), nTn, float(fv[0]) if fv else "-", float(fv[-1]) if fv else "-"), flush=True)
        if nTn == 0 and len(sys.argv) > 3 and sys.argv[3] == "first":
            print("first dead fourth-star label found: no four-star completion of rank 30")
            return
    dead = [k for k, v in summary.items() if v[2] == 0]
    print("fourth-star labels with NO profile: %d of 10 %s -> %s" % (len(dead), dead,
          "no four-star completion of rank 30" if dead else "column test passed"))


if __name__ == "__main__":
    main()
