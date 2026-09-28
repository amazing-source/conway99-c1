r"""Rank-17 switch: global star-1 search (C1, 28/09 night; route (b) agreed with C2). Skips the skeleton enumeration.
Star 1 = the 6 cells (1,d), d = 2..7, i.e. 12 norm-10 vectors w+-_1d of K with (orienting (u, h_1) = +1):
  in-cell (w+, w-) in {0, +-4}, w- != +-w+, w+ = w- mod 2K; cross-cell (w, w') in {-5, -1, 3} (= 4(u,u') - 1);
  star 1: the sum of the 12 vectors is 0 (sum_d a_1d = 0, a = (w+ + w-)/2).
The classes g_d = [w_1d] of a star-1 configuration ARE the skeleton; class-level filters (independence, usable sums, kappa
parity energy, unit rule, M1) are checked on it, then structures' solver runs the remaining cells with star 1 fixed.
Symmetry: cell (1,2) up to W(R_K) (reflections in the roots of K fix y1, y2) and the h-flips a -> -a (h_1) and b -> -b
(h_2); cells (1,3..7) unordered (increasing candidate index, the last one forced by the star equation and required to
come last) with b_1d normalised by h_d (first non-zero K-coordinate positive).
Verdicts: EXCLUDED-STAR1 (no star-1 configuration survives: exhaustive), EXCLUDED (all extend-searches excluded), FOUND,
LIMIT. Pass-1 tool; exact integer tests except the solver's PSD pruning.
Usage: python rank17_star1.py <K tag> <pair id> [node cap]"""
import json, os, sys, time, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rank17_engine as eng
import rank17_skeleton as sk
from rank17_ypairs import short_vectors_chunked
from y_pairs import root_system
from rank17_vsearch import CELLS

CROSS = np.array([-5, -1, 3])
INCELL = np.array([0, 4, -4])


def first_pos_rows(X):
    nz = X != 0
    has = nz.any(axis=1)
    first = X[np.arange(len(X)), nz.argmax(axis=1)]
    return ~has | (first > 0)


class Star1:
    def __init__(self, tag, pid):
        self.case = c = eng.Case(tag, pid)
        GK = c.GK
        self.GK = GK
        W = c.W                                                             # int16, up to sign
        us = np.zeros(1 << 15, dtype=bool)
        us[list(c.usable.keys())] = True
        # cheap L1 (w = r mod 4V; sign-invariant since the root set is symmetric) and usable class, on the unsigned shell
        keep = us[c.cls].copy()
        sh = 2 * np.arange(c.Kv.shape[1])
        for s0 in range(0, len(W), 100000):
            k = (((W[s0:s0 + 100000].astype(np.int64) @ c.Kv) % 4) << sh).sum(axis=1)
            keep[s0:s0 + 100000] &= ~np.isin(k, c.rootkeys4)
        Wk, ck = W[keep], c.cls[keep]
        self.S = np.vstack([Wk, -Wk]).astype(np.int16)                      # signed norm-10 shell, K coordinates
        self.cls = np.concatenate([ck, ck])
        self.SG = (self.S.astype(np.int32) @ GK.astype(np.int32))
        self.umask = us
        # roots of K and simple roots (orthonormal frame via Cholesky) for W(R_K)-canonical forms
        X, nrm = short_vectors_chunked(GK.tolist(), 2)
        R = X[nrm == 2].astype(np.int64)
        self.nroots = 2 * len(R)
        if len(R):
            L = np.linalg.cholesky(GK.astype(float))
            Rf = R.astype(float) @ L
            Sr, comp, marks, A, P = root_system(Rf)
            Linv = np.linalg.inv(L)
            self.SR = np.rint(Sr @ Linv).astype(np.int64)                    # simple roots, K coordinates
            assert np.allclose(self.SR.astype(float) @ L, Sr, atol=1e-6)
        else:
            self.SR = np.zeros((0, 15), dtype=np.int64)
        self.SRG = self.SR @ GK

    def canon_pair(self, a, b):
        """W(R_K)-canonical form of the ordered pair (a, b): a dominant, then b dominant for Stab_W(a)"""
        a = a.copy(); b = b.copy()
        for _ in range(100000):
            ip = self.SRG @ a
            neg = np.flatnonzero(ip < 0)
            if len(neg) == 0:
                break
            j = neg[0]
            b = b - (self.SRG[j] @ b) * self.SR[j]
            a = a - ip[j] * self.SR[j]
        for _ in range(100000):
            ipa = self.SRG @ a; ipb = self.SRG @ b
            neg = np.flatnonzero((ipa == 0) & (ipb < 0))
            if len(neg) == 0:
                break
            j = neg[0]
            b = b - ipb[j] * self.SR[j]
        return a, b

    def first_cells(self):
        """canonical (w+, w-) for cell (1,2): up to W(R_K) and the flips a -> -a, b -> -b"""
        if len(self.SR):
            keep = np.zeros(len(self.S), dtype=bool)
            for s0 in range(0, len(self.S), 100000):                       # chunks (memory)
                keep[s0:s0 + 100000] = ((self.S[s0:s0 + 100000].astype(np.int64) @ self.SRG.T) >= 0).all(axis=1)
            dom = self.S[keep].astype(np.int64)
        else:
            dom = self.S.astype(np.int64)
        seen, out = set(), []
        for wp in dom:
            same = self.S[(self.cls == int(((wp & 1) << np.arange(15)).sum()))].astype(np.int64)
            ip = same @ self.GK @ wp
            cand = same[np.isin(ip, INCELL) & ~(same == wp).all(axis=1) & ~(same == -wp).all(axis=1)]
            for wm in cand:
                a, b = (wp + wm) // 2, (wp - wm) // 2
                best = None
                for sa in (1, -1):
                    for sb in (1, -1):
                        ca, cb = self.canon_pair(sa * a, sb * b)
                        key = ca.tobytes() + cb.tobytes()
                        if best is None or key < best[0]:
                            best = (key, ca, cb)
                if best[0] not in seen:
                    seen.add(best[0])
                    out.append((best[1] + best[2], best[1] - best[2]))
        return out

    def search(self, cap=10 ** 7, max_configs=10 ** 5):
        GK = self.GK
        firsts = self.first_cells()
        configs, nodes = [], [0]
        for (wp, wm) in firsts:
            g2 = int(((wp & 1) << np.arange(15)).sum())
            # vectors compatible with both w+-_12
            ok = np.isin(self.SG @ wp, CROSS) & np.isin(self.SG @ wm, CROSS)
            V1, c1 = self.S[ok].astype(np.int64), self.cls[ok]
            # cell candidates among V1 (vectorised, index arrays only): pairs in one class, (w, w') in {0, +-4},
            # w' != -w, b = (w - w')/2 normalised (first non-zero coordinate > 0), class != g2, class ^ g2 usable
            order = np.argsort(c1, kind='stable')
            V1, c1 = V1[order], c1[order]
            if len(c1) == 0:
                continue
            bnd = np.flatnonzero(np.diff(c1)) + 1
            st = np.concatenate([[0], bnd]); en = np.concatenate([bnd, [len(c1)]])
            V1G = V1 @ GK
            II, JJ = [], []
            for a0, e0 in zip(st.tolist(), en.tolist()):
                C = int(c1[a0])
                if e0 - a0 < 2 or C == g2 or not self.umask[C ^ g2]:
                    continue
                ip = V1G[a0:e0] @ V1[a0:e0].T
                I, J = np.nonzero(np.isin(ip, INCELL))
                keep = I != J
                I, J = I[keep] + a0, J[keep] + a0
                if len(I):
                    notneg = ~(V1[I] == -V1[J]).all(axis=1)
                    b = (V1[I] - V1[J]) // 2
                    keep = notneg & first_pos_rows(b)
                    II.append(I[keep]); JJ.append(J[keep])
            if not II:
                continue
            II = np.concatenate(II); JJ = np.concatenate(JJ)
            if len(II) < 5:
                continue
            P, Mn, Cc = V1[II], V1[JJ], c1[II]
            PG, MG = P @ GK, Mn @ GK
            A2 = P + Mn                                                       # 2a
            A2v = np.ascontiguousarray(A2).view(np.dtype((np.void, A2.dtype.itemsize * A2.shape[1]))).ravel()
            a2order = np.argsort(A2v, kind='stable')
            A2sorted = A2v[a2order]

            def lookup_a2(need):
                nv = np.ascontiguousarray(need.astype(A2.dtype)).view(A2v.dtype).ravel()
                lo = np.searchsorted(A2sorted, nv[0], side='left'); hi = np.searchsorted(A2sorted, nv[0], side='right')
                return a2order[lo:hi]
            base = wp + wm
            n = len(P)

            def compat(idx, i):
                """candidates in idx compatible with candidate i (all 4 cross products in CROSS)"""
                p, m = P[i], Mn[i]
                ok = (np.isin(PG[idx] @ p, CROSS) & np.isin(PG[idx] @ m, CROSS) &
                      np.isin(MG[idx] @ p, CROSS) & np.isin(MG[idx] @ m, CROSS))
                return idx[ok & (Cc[idx] != Cc[i]) & self.umask[Cc[idx] ^ Cc[i]]]    # distinct classes, usable sums

            def rec(chosen, live, tot):
                nodes[0] += 1
                if nodes[0] > cap:
                    raise TimeoutError
                if len(chosen) == 4:
                    need = -(tot).astype(np.int64)                             # 2 a_17 = -(sum of the 10 others)
                    liveset = set(live.tolist())
                    for j in lookup_a2(need).tolist():
                        if j > chosen[-1] and j in liveset:
                            idx5 = [chosen[k] for k in range(4)] + [j]
                            configs.append([(wp.copy(), wm.copy())] + [(P[t].copy(), Mn[t].copy()) for t in idx5])
                            if len(configs) >= max_configs:
                                raise TimeoutError
                    return
                for i in live.tolist():
                    nl = compat(live[live > i], i)
                    if len(nl) < 4 - len(chosen):
                        continue
                    rec(chosen + [i], nl, tot + P[i] + Mn[i])
            rec([], np.arange(n), base.copy())
        return firsts, configs, nodes[0]


def main(tag, pid, cap=10 ** 7):
    t0 = time.time()
    s1 = Star1(tag, pid)
    try:
        firsts, configs, nodes = s1.search(cap=cap)
        exhaustive = True
    except TimeoutError:
        exhaustive = False
        firsts, configs, nodes = [], [], cap
    out = {'V': s1.case.V, 'pair': pid, 'roots_K': s1.nroots, 'shell': int(len(s1.S)), 'first_cells': len(firsts),
           'star1_configs': len(configs), 'nodes': nodes, 'exhaustive': exhaustive, 's': round(time.time() - t0, 1)}
    print(json.dumps(out), flush=True)
    return s1, configs, out


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 7)
