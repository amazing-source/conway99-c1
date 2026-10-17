"""F_Y = 3I - A_YY + J/12 - B_Y^T L^+ B_Y (l-view Schur form, c(l) = 1) and the attachment bound
   Conway:  B_Y B_Y^T <= Lambda(L) := 7L - L^2 + 2J - sum_p 1_{X_p} 1_{X_p}^T   (B_D B_D^T = Lambda(L) exactly; Y subset D).
usage: python c1_fy_look.py walks f1.json ... | cache file max"""
import itertools, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, build_H, relabel, gl_connected


def fy(EE):
    V, A = build_H(EE)            # 56 vertices: 12 letters, 24 X_l labels, 20 Y labels
    n36 = 36
    AG = A[:n36, :n36].astype(float)
    L = 3 * np.eye(n36) - AG
    BY = A[:n36, n36:].astype(float)
    AYY = A[n36:, n36:].astype(float)
    Lp = np.linalg.pinv(L)
    G = BY.T @ Lp @ BY
    F = 3 * np.eye(20) - AYY + np.ones((20, 20)) / 12 - G
    grp = np.zeros((n36, 3))
    grp[:12, 0] = 1; grp[12:24, 1] = 1; grp[24:, 2] = 1   # X_v letters, L_0, L_1 (build_H order: letters, XL, Y)
    # check XL order: XL = labels touching 0 or 1, in S order: first 12 contain 0, next 12 contain 1
    Lam = 7 * L - L @ L + 2 * np.ones((n36, n36)) - grp @ grp.T
    Mgap = Lam - BY @ BY.T
    ev_gap = np.linalg.eigvalsh(Mgap)
    lamL = np.linalg.eigvalsh(L)
    return np.linalg.eigvalsh(F)[::-1], ev_gap[0], lamL[1], G, F


def main():
    rows = []
    if sys.argv[1] == "walks":
        for f in sys.argv[2:]:
            d = json.load(open(f))
            lab = [frozenset(x) for x in d["labels"]]
            EE = {frozenset((lab[i], lab[j])) for i, j in d["edges"]}
            evF, gap, a2, G, F = fy(EE)
            print(f.split("/")[-1].split("\\")[-1])
            print("   F_Y eigenvalues:", np.round(evF, 3))
            print("   min eig of Lambda(L) - B_Y B_Y^T (Conway >= 0): %.4f ; algebraic connectivity %.4f" % (gap, a2))
            off = F[~np.eye(20, dtype=bool)]
            print("   F diag mean %.3f, offdiag mean %.3f, offdiag |.| mean %.3f; G diag mean %.3f" % (
                np.diag(F).mean(), off.mean(), np.abs(off).mean(), np.diag(G).mean()))
    else:
        mx = int(sys.argv[3]); tab = Counter(); done = 0
        for line in open(sys.argv[2]):
            d = json.loads(line)
            if len(d["labels"]) != 44:
                continue
            S0 = [frozenset(x) for x in d["labels"]]
            E0 = [(frozenset(a), frozenset(b)) for a, b in d["edges"]]
            for side in (0, 1):
                L_, EE = relabel(S0, E0, side)
                conn, degok = gl_connected(EE)
                if not (conn and degok):
                    continue
                evF, gap, a2, G, F = fy(EE)
                psd = evF[-1] > -1e-9
                tab[(bool(psd), bool(gap > -1e-9))] += 1
                rows.append((gap, a2, psd))
                done += 1
            if done >= mx:
                break
        print("(F_Y >= 0 i.e. T_S >= 0, attachment bound Lambda(L) - B_Y B_Y^T >= 0) : count")
        for k, v in sorted(tab.items()):
            print("   ", k, v)
        g = np.array([r[0] for r in rows])
        print("min eig gap: min %.4f median %.4f max %.4f" % (g.min(), np.median(g), g.max()))


if __name__ == "__main__":
    main()
