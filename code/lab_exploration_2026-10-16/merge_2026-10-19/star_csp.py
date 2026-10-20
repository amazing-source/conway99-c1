"""The complete star of a near vertex at rank 37 (LAB 20/10/2026): why does it die?

For a generic line T (G = G_T connected, 7 not dividing tau) and a near vertex x in C0, the star of x is the set of the 10
far vertices adjacent to x: W_y = {x, y} u q_y u s_y for y in C0 - {x, xbar}.  Exact conditions (srg + rank 37):
  L2 for every W_y;  Green diagonal e_W^T Omega e_W = 0;  R(W, W') = 4 - e_W^T Omega e_W' in {0, 1}  (rank 37);
  q_y distinct, s_y distinct (bijections);
  MATCH: N(x) induces a perfect matching (lambda = 1), so W has exactly 1 - |N_G(x) n W| star neighbours, and two star
         neighbours share only x;
  MARG:  #{y : u in W_y} = K(x, u) for every u in C1 u C2 (L1: these are all the far vertices containing x and u);
  NF:    if W ~ W' in the star, every name z of W' other than x has at most one G-neighbour in W (mu(z, W) = 2);
  L3:    |W n W'| <= 2.
Flags switch families off (ablation): g = Green values (keep only the diagonal), m = MATCH, k = MARG, n = NF.
On a sub-star (cores), MATCH and MARG are used as upper bounds only (full = False, as in Codex's note 207).
usage: python star_csp.py <seed> [x] [flags] [--cores] [--tau any] [--limit seconds]"""
import ctypes
import itertools
import json
import os
import random
import sys
import time

import numpy as np

if sys.platform == "win32":
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x40)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "reduction_2026-10-19"))
from ll_test import gt_matrix, k_matrix, components, pairs_of, random_gt  # noqa: E402

P = 7
n, N = 12, 36


def inv_mod(M):
    k = M.shape[0]
    A = np.concatenate([M % P, np.eye(k, dtype=np.int64)], axis=1)
    for c in range(k):
        piv = [r for r in range(c, k) if A[r, c] % P]
        if not piv:
            return None
        r = piv[0]
        A[[c, r]] = A[[r, c]]
        A[c] = A[c] * pow(int(A[c, c]), P - 2, P) % P
        for r2 in range(k):
            if r2 != c and A[r2, c]:
                A[r2] = (A[r2] - A[r2, c] * A[c]) % P
    return A[:, k:]


def det_mod(M):
    M = M.copy() % P
    k, d = M.shape[0], 1
    for c in range(k):
        piv = [r for r in range(c, k) if M[r, c]]
        if not piv:
            return 0
        r = piv[0]
        if r != c:
            M[[c, r]] = M[[r, c]]
            d = -d
        d = d * int(M[c, c]) % P
        iv = pow(int(M[c, c]), P - 2, P)
        for r2 in range(c + 1, k):
            if M[r2, c]:
                M[r2] = (M[r2] - M[r2, c] * iv * M[c]) % P
    return d % P


def line_graph(seed, need_tau=-1):
    """the first connected admissible G with d = 1 (and (tau|7) = need_tau unless 0) from the seeded stream"""
    rng = random.Random(seed)
    while True:
        s01, s12, s20, _ = random_gt(n, rng, 1)
        G = gt_matrix(n, s01, s12, s20)
        L = (3 * np.eye(N, dtype=np.int64) - G + 1) % P
        Om = inv_mod(L)
        if Om is None:
            continue
        t = det_mod((3 * np.eye(N, dtype=np.int64) - G)[1:, 1:])
        leg = 1 if pow(t, 3, P) == 1 else -1
        if need_tau and leg != need_tau:
            continue
        return (s01, s12, s20), G, Om, k_matrix(n, G), leg


class Star:
    def __init__(self, G, Om, K, x, flags=""):
        self.G, self.Om, self.K, self.x = G, Om, K, x
        self.flags = flags
        self.nb = [set(int(z) for z in np.nonzero(G[v])[0]) for v in range(N)]
        xb = x ^ 1
        self.ys = [y for y in range(n) if y not in (x, xb)]
        P1 = [(n + a, n + b) for a, b in pairs_of(n)]
        P2 = [(2 * n + a, 2 * n + b) for a, b in pairs_of(n)]
        self.dom = {}
        for y in self.ys:
            cands = []
            for qi, q in enumerate(P1):
                if "k" not in flags and (K[x, q[0]] == 0 or K[x, q[1]] == 0):
                    continue
                for si, s in enumerate(P2):
                    if "k" not in flags and (K[x, s[0]] == 0 or K[x, s[1]] == 0):
                        continue
                    W = (x, y) + q + s
                    Ws = set(W)
                    if any(len(self.nb[v] & Ws) > 1 for v in W):
                        continue
                    cnt = {}
                    for v in W:
                        for z in self.nb[v]:
                            if z not in Ws:
                                cnt[z] = cnt.get(z, 0) + 1
                    if any(c > 2 for c in cnt.values()):
                        continue
                    e = np.zeros(N, dtype=np.int64)
                    e[list(W)] = 1
                    if int(e @ Om @ e) % P:
                        continue
                    cands.append((W, qi, si))
            self.dom[y] = cands
        # arrays for vectorised pair tests
        self.arr = {}
        for y, cands in self.dom.items():
            if not cands:
                continue
            names = np.array([c[0] for c in cands], dtype=np.int64)          # (m, 6)
            E = np.zeros((len(cands), N), dtype=np.int64)
            np.put_along_axis(E, names, 1, axis=1)
            Y = (E @ Om) % P                                                  # rows Omega e_W
            capx = np.array([1 - len(self.nb[x] & set(c[0])) for c in cands], dtype=np.int64)
            self.arr[y] = dict(names=names, E=E, Y=Y, qi=np.array([c[1] for c in cands]),
                               si=np.array([c[2] for c in cands]), cap=capx)

    def pair_ok(self, ya, ia, yb_arr):
        """vector of booleans: candidates of yb compatible with candidate ia of ya; and their R values"""
        A = self.arr[ya]
        B = yb_arr
        ok = (B["qi"] != A["qi"][ia]) & (B["si"] != A["si"][ia])
        share = B["E"][:, A["names"][ia]].sum(axis=1)                         # |W_a n W_b|
        ok &= share <= 2
        if "g" in self.flags:
            R = np.zeros(len(B["qi"]), dtype=np.int64)                         # Green off: no adjacency information
            return ok, R, share
        g = A["Y"][ia][B["names"]].sum(axis=1) % P
        R = (4 - g) % P
        ok &= R <= 1
        if "m" not in self.flags:
            ok &= ~((R == 1) & (share > 1))
            ok &= ~((R == 1) & ((B["cap"] == 0) | (A["cap"][ia] == 0)))
        if "n" not in self.flags:
            # W_a ~ W_b: names of W_b (other than x) have <= 1 G-neighbour in W_a, and vice versa
            Ga = self.G[:, A["names"][ia]].sum(axis=1)                         # |N_G(z) n W_a| for every z
            bad_b = (Ga[B["names"]] > 1) & (B["names"] != self.x)
            cnt_a = np.stack([self.G[B["names"][:, k]][:, A["names"][ia]] for k in range(6)], axis=1).sum(axis=1)
            bad_a = (cnt_a > 1) & (A["names"][ia] != self.x)[None, :]
            ok &= ~((R == 1) & (bad_b.any(axis=1) | bad_a.any(axis=1)))
        return ok, R, share

    def solve(self, subset=None, full=True, limit=60.0):
        ys = list(subset) if subset is not None else list(self.ys)
        if any(not self.dom[y] for y in ys):
            return "UNSAT", 0
        x = self.x
        doms = {y: np.arange(len(self.dom[y])) for y in ys}
        state = dict(chosen={}, deg={}, marg={})
        nodes = [0]
        t0 = time.time()

        def marg_ok(names, marg):
            if "k" in self.flags:
                return True
            for u in names[2:]:
                if marg.get(u, 0) + 1 > self.K[x, u]:
                    return False
            return True

        def rec(doms, chosen, deg, marg, adj):
            nodes[0] += 1
            if time.time() - t0 > limit:
                raise TimeoutError
            if len(chosen) == len(ys):
                if full and "m" not in self.flags and "g" not in self.flags:
                    for y in ys:
                        if deg[y] != self.arr[y]["cap"][chosen[y]]:
                            return False
                return True
            y = min((v for v in ys if v not in chosen), key=lambda v: len(doms[v]))
            for i in doms[y]:
                names = self.arr[y]["names"][i]
                if not marg_ok(names, marg):
                    continue
                # adjacency to the chosen ones (already pairwise-filtered); matching capacity
                newdeg = dict(deg)
                okc = True
                Ri = {}
                for v, j in chosen.items():
                    g = int(self.arr[y]["Y"][i][self.arr[v]["names"][j]].sum()) % P if "g" not in self.flags else 4
                    R = (4 - g) % P
                    Ri[v] = R
                    if R == 1:
                        newdeg[v] = newdeg.get(v, 0) + 1
                        newdeg[y] = newdeg.get(y, 0) + 1
                if "m" not in self.flags and "g" not in self.flags:
                    for v in list(chosen) + [y]:
                        idx = chosen[v] if v != y else i
                        if newdeg.get(v, 0) > self.arr[v]["cap"][idx]:
                            okc = False
                if not okc:
                    continue
                newmarg = dict(marg)
                for u in names[2:]:
                    newmarg[u] = newmarg.get(u, 0) + 1
                newchosen = dict(chosen)
                newchosen[y] = i
                full_cap = [v for v in chosen if Ri.get(v) == 1 and newdeg.get(v, 0) >= self.arr[v]["cap"][chosen[v]]]
                nd = {}
                dead = False
                for v in ys:
                    if v in newchosen:
                        continue
                    ok, R, share = self.pair_ok(y, i, self.arr[v])
                    cand = doms[v][ok[doms[v]]]
                    if "m" not in self.flags and "g" not in self.flags:
                        # every chosen W at full matching capacity forbids new star neighbours
                        if newdeg.get(y, 0) >= self.arr[y]["cap"][i]:
                            cand = cand[R[cand] == 0]
                        for u in full_cap:
                            if len(cand):
                                _, Ru, _ = self.pair_ok(u, newchosen[u], self.arr[v])
                                cand = cand[Ru[cand] == 0]
                    if "k" not in self.flags and len(cand):
                        full_u = [u for u, c in newmarg.items() if c >= self.K[x, u]]
                        if full_u:
                            hit = np.isin(self.arr[v]["names"][cand][:, 2:], full_u).any(axis=1)
                            cand = cand[~hit]
                    if len(cand) == 0:
                        dead = True
                        break
                    nd[v] = cand
                if dead:
                    continue
                nd.update({v: doms[v] for v in newchosen if v in doms})
                if rec(nd, newchosen, newdeg, newmarg, adj):
                    state["chosen"] = newchosen
                    return True
            return False

        try:
            res = rec(doms, {}, {}, {}, {})
        except TimeoutError:
            return "TIMEOUT", nodes[0]
        return ("SAT" if res else "UNSAT"), nodes[0]


def main():
    seed = int(sys.argv[1])
    x = int(sys.argv[2]) if len(sys.argv) > 2 and not sys.argv[2].startswith("-") else 0
    flags = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith("-") else ""
    need = 0 if "--tau" in sys.argv and sys.argv[sys.argv.index("--tau") + 1] == "any" else -1
    gt, G, Om, K, leg = line_graph(seed, need)
    t = time.time()
    st = Star(G, Om, K, x, flags)
    sizes = [len(st.dom[y]) for y in st.ys]
    lim = float(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 60.0
    res, nodes = st.solve(limit=lim)
    out = {"seed": seed, "x": x, "flags": flags, "tau_leg": leg, "dom_sizes": sizes, "status": res, "nodes": nodes,
           "seconds": round(time.time() - t, 2)}
    if "--cores" in sys.argv and res == "UNSAT":
        core = list(st.ys)
        for y in list(st.ys):
            trial = [v for v in core if v != y]
            r2, _ = st.solve(trial, full=False, limit=60.0)
            if r2 == "UNSAT":
                core = trial
        out["core"] = core
        out["core_size"] = len(core)
    print(json.dumps(out), flush=True)


if __name__ == "__main__":
    main()
