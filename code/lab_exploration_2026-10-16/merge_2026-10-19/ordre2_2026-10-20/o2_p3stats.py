"""Conway (k = 14) far projectors on a synthetic generic line: closed forms and the strength of the 3-eigenspace block
(LAB, NOTE_ORDRE2, 20/10/2026).
  H  = 7 Pi^(-4) = 3I - R + J/9  - E^T (3I - G + J)^{-1} E      (archive)
  H3 = 7 Pi^(3)  = 4I + R - 2J/35 - E^T (4I + G)^{-1} E          (this note; diagonal = TL 17.57 formula 138/35)
  H + H3 = 7 (I - E^T K^+ E)                                      (identity check, K = 12I - G - G^2 + 2J - J_cl)
Star of x (as star39_prep: L2, K(x, .) >= 1 on C1 u C2 names): unary 0 <= H_aa (engine) vs H3_aa >= 0 (new);
random blocks of k candidates (distinct y, q, s; overlap <= 2; R = 0 on all pairs, or a random matching):
fraction PSD for H alone, H and 7I - H (engine), H and H3 (new).
usage: python o2_p3stats.py <seed> [x] [samples]"""
import json
import os
import random
import sys

import numpy as np

MERGE = r"C:\Users\RESEARCHER\Downloads\conway_c2_researcher2_start_2026_09_30\conway_c2_researcher2_start_2026_09_30\work\exploration_2026-10-16\merge_2026-10-19"
sys.path.insert(0, MERGE)
sys.path.insert(0, os.path.join(MERGE, "..", "reduction_2026-10-19"))
from star_csp import line_graph, n, N  # noqa: E402
from ll_test import pairs_of  # noqa: E402


def psd(M, tol=1e-9):
    return np.linalg.eigvalsh(M).min() >= -tol


def main():
    seed = int(sys.argv[1])
    x = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    samples = int(sys.argv[3]) if len(sys.argv) > 3 else 4000
    rng = random.Random(1000 + seed)
    gt, G, Om, K, leg = line_graph(seed, -1)
    G = G.astype(float)
    I36, J36 = np.eye(N), np.ones((N, N))
    Z = np.linalg.inv(3 * I36 - G + J36)
    Z3 = np.linalg.inv(4 * I36 + G)
    Kp = np.linalg.pinv(K.astype(float), rcond=1e-10, hermitian=True)
    nb = [set(int(z) for z in np.nonzero(G[v])[0]) for v in range(N)]
    # identity check on random 2-per-class name sets
    P0 = [(a, b) for a, b in pairs_of(n)]
    maxerr = 0.0
    for _ in range(300):
        W = [list(rng.choice(P0)), [n + t for t in rng.choice(P0)], [2 * n + t for t in rng.choice(P0)]]
        W2 = [list(rng.choice(P0)), [n + t for t in rng.choice(P0)], [2 * n + t for t in rng.choice(P0)]]
        e = np.zeros(N); e[sum(W, [])] = 1
        e2 = np.zeros(N); e2[sum(W2, [])] = 1
        Rv = rng.randint(0, 1)
        h = -Rv + 1 / 9 - e @ Z @ e2
        h3 = Rv - 2 / 35 - e @ Z3 @ e2
        maxerr = max(maxerr, abs(h + h3 + 7 * (e @ Kp @ e2)))
        hd = 3 + 1 / 9 - e @ Z @ e
        h3d = 4 - 2 / 35 - e @ Z3 @ e
        maxerr = max(maxerr, abs(hd + h3d - 7 + 7 * (e @ Kp @ e)))
    # star candidates
    xb = x ^ 1
    ys = [y for y in range(n) if y not in (x, xb)]
    P1 = [(n + a, n + b) for a, b in pairs_of(n)]
    P2 = [(2 * n + a, 2 * n + b) for a, b in pairs_of(n)]
    cands = {}
    tot = cut_h = cut_h3 = cut_both = cut_7 = 0
    gzero = gzero_h3cut = 0
    for y in ys:
        lst = []
        for qi, q in enumerate(P1):
            if K[x, q[0]] == 0 or K[x, q[1]] == 0:
                continue
            for si, s_ in enumerate(P2):
                if K[x, s_[0]] == 0 or K[x, s_[1]] == 0:
                    continue
                W = (x, y) + q + s_
                Ws = set(W)
                if any(len(nb[v] & Ws) > 1 for v in W):
                    continue
                cnt = {}
                for v in W:
                    for z in nb[v]:
                        if z not in Ws:
                            cnt[z] = cnt.get(z, 0) + 1
                if any(c > 2 for c in cnt.values()):
                    continue
                e = np.zeros(N); e[list(W)] = 1
                dd = 3 + 1 / 9 - e @ Z @ e
                dd3 = 4 - 2 / 35 - e @ Z3 @ e
                tot += 1
                bad_h, bad_h3, bad_7 = dd < -1e-9, dd3 < -1e-9, dd > 7 + 1e-9
                cut_h += bad_h; cut_h3 += bad_h3; cut_7 += bad_7; cut_both += (bad_h or bad_h3)
                ei = np.zeros(N, dtype=np.int64); ei[list(W)] = 1
                g = int(ei @ ((Om @ ei) % 7)) % 7
                if g == 0 and not bad_h:
                    gzero += 1
                    gzero_h3cut += bad_h3
                if not bad_h and not bad_h3:
                    lst.append((W, qi, si, e))
                elif not bad_h:
                    lst.append((W, qi, si, e, "h3bad"))
        cands[y] = lst

    # random blocks
    def block(sel, Rm):
        k = len(sel)
        Hb = np.zeros((k, k)); H3b = np.zeros((k, k))
        for i in range(k):
            for j in range(k):
                ei, ej = sel[i][3], sel[j][3]
                if i == j:
                    Hb[i, i] = 3 + 1 / 9 - ei @ Z @ ei
                    H3b[i, i] = 4 - 2 / 35 - ei @ Z3 @ ei
                else:
                    Hb[i, j] = -Rm[i][j] + 1 / 9 - ei @ Z @ ej
                    H3b[i, j] = Rm[i][j] - 2 / 35 - ei @ Z3 @ ej
        return Hb, H3b

    res = {}
    for k in (2, 3, 4, 5, 6, 7, 8):
        stats = {"H": 0, "H_7mH": 0, "H_H3": 0, "n": 0}
        tries = 0
        while stats["n"] < samples and tries < 50 * samples:
            tries += 1
            yy = rng.sample(ys, k)
            sel = []
            okk = True
            for y in yy:
                pool = [c for c in cands[y] if len(c) == 4]  # candidates passing both unary tests
                if not pool:
                    okk = False
                    break
                sel.append(rng.choice(pool))
            if not okk:
                continue
            if len({c[1] for c in sel}) < k or len({c[2] for c in sel}) < k:
                continue
            if any(len(set(sel[i][0]) & set(sel[j][0])) > 2 for i in range(k) for j in range(i)):
                continue
            Rm = [[0] * k for _ in range(k)]
            if rng.random() < 0.5:  # random partial matching among the block (star edges)
                idx = list(range(k)); rng.shuffle(idx)
                for t in range(0, k - 1, 2):
                    if rng.random() < 0.5:
                        a, b = idx[t], idx[t + 1]
                        if len(set(sel[a][0]) & set(sel[b][0])) == 1:
                            Rm[a][b] = Rm[b][a] = 1
            Hb, H3b = block(sel, Rm)
            stats["n"] += 1
            okH = psd(Hb)
            stats["H"] += okH
            stats["H_7mH"] += okH and psd(7 * np.eye(k) - Hb)
            stats["H_H3"] += okH and psd(H3b)
        res[k] = {kk: (vv / stats["n"] if kk != "n" else vv) for kk, vv in stats.items()}
    print(json.dumps({"seed": seed, "x": x, "tau_leg": leg, "identity_maxerr": maxerr, "unary_candidates": tot,
                      "unary_cut_by_H<0": cut_h, "unary_cut_by_H>7": cut_7, "unary_cut_by_H3<0": cut_h3,
                      "unary_cut_by_H_or_H3": cut_both,
                      "rank37_level(g=0,H>=0)": gzero, "rank37_level_cut_by_H3": gzero_h3cut,
                      "blocks(PSD fraction; H3 sampled only among unary-H3-passing candidates)": res}, default=lambda o: o.item() if hasattr(o, "item") else str(o)))


if __name__ == "__main__":
    main()
