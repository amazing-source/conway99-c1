"""Flag-algebra (Razborov) PSD constraints on the EXACT census of a srg(99,14,1,2) (LAB 19/10/2026).

Census (census2.py, LAB 08/10, re-generated 18/10): for every admissible type H on n <= 9 (or 10) vertices, the number
x_H of induced EMBEDDINGS of H is an explicit affine form in the parameters (unlabelled counts of the types of minimum
degree >= 3; parameter 1 = P = number of induced prisms).  The archive used only x_H >= 0 (an LP).

Flag constraint (exact for one finite graph, no limit): fix a labelled admissible type sigma on k vertices and a set of
flags F (admissible labelled graphs on m vertices whose vertices 0..k-1 induce sigma, up to isomorphism fixing 0..k-1).
For an induced embedding theta of sigma, v_theta(F) = number of induced embeddings of F extending theta.  Then
    M_sigma = sum_theta v_theta v_theta^T  is positive semidefinite,
and M_sigma[F1,F2] = number of triples (theta, phi1, phi2) = sum over AMALGAM patterns (identification of some extra
vertices of F1 with extra vertices of F2, free adjacencies between the non-identified ones) of x_H, H = the amalgam.
Every entry is therefore an affine form in the census parameters; amalgams have at most k + 2(m - k) vertices.
Non-admissible amalgams have x_H = 0 (not in the census).

usage: python flag_sdp.py <census json> <k> <m> [max_sigmas] [--objective=min|max] [--solver=CLARABEL|SCS] [--dump=f]
   tries every admissible sigma of order k (or the first max_sigmas), flags of order m, solves min (and max) P
   subject to x_H >= 0 for all census types and M_sigma >= 0 for the chosen sigmas.  Floating point (exploration)."""
import itertools
import json
import os
import sys
import time
from fractions import Fraction as Fr

import numpy as np

sys.path.insert(0, r"C:\Users\RESEARCHER\Downloads\conway_c2_researcher2_start_2026_09_30\conway_c2_researcher2_start_2026_09_30\work\c1_theta_lp_2026-10-07")
import census2 as C2  # noqa: E402


def canon_rooted(n, rows, k):
    """canonical form of a graph whose vertices 0..k-1 are individually labelled (fixed)."""
    best = [None, None]

    def rec(colour):
        colour = C2.refine(n, rows, colour)
        cnt = {}
        for c in colour:
            cnt[c] = cnt.get(c, 0) + 1
        if len(cnt) == n:
            perm = sorted(range(n), key=lambda v: colour[v])
            code = 0
            for i in range(n):
                ri = rows[perm[i]]
                for j in range(i + 1, n):
                    code = code << 1 | (ri >> perm[j] & 1)
            if best[0] is None or code < best[0]:
                best[0], best[1] = code, perm
            return
        target = min(c for c, mlt in cnt.items() if mlt > 1)
        cell = [v for v in range(n) if colour[v] == target]
        seen = []
        for v in cell:
            if any((rows[v] & ~(1 << w)) == (rows[w] & ~(1 << v)) for w in seen):
                continue
            seen.append(v)
            rec([2 * colour[u] + (0 if u == v else 1) for u in range(n)])
    rec([u + 1 if u < k else 0 for u in range(n)])
    return best[0], best[1]


def admissible(n, rows):
    for i in range(n):
        for j in range(i + 1, n):
            c = bin(rows[i] & rows[j]).count("1")
            if c > (1 if rows[i] >> j & 1 else 2):
                return False
    return True


class Census:
    def __init__(self, path):
        d = json.load(open(path))
        self.params = d["params"]
        self.NP = len(self.params)
        self.maxn = max(int(n) for n in d["types"])
        self.form = {}                      # (n, code) -> dict param -> float  (x_H, embeddings)
        self.aut = {}
        for n, lst in d["types"].items():
            for key, rows, aut, form in lst:
                self.form[(int(n), key)] = {int(p): float(Fr(v)) for p, v in form.items()}
                self.aut[(int(n), key)] = aut
        assert self.params[0][0] == 6

    def x_of(self, n, rows):
        """affine form of x_H for an arbitrary labelled graph (0 if not admissible)"""
        if not admissible(n, rows):
            return None
        code, _ = C2.canon(n, list(rows))
        return self.form.get((n, code))


def flags_of(sigma, k, m):
    """admissible labelled extensions of sigma (k vertices) to m vertices, up to iso fixing 0..k-1"""
    level = {canon_rooted(k, list(sigma), k)[0]: list(sigma)}
    for n in range(k, m):
        nxt = {}
        for rows in level.values():
            for S in C2.admissible_sets(n, rows):
                new = C2.extend(n, rows, S)
                code, perm = canon_rooted(n + 1, new, k)
                if code not in nxt:
                    nxt[code] = new          # keep THIS labelling: sigma stays on 0..k-1, new vertices appended
        level = nxt
    out = [list(rows) for rows in level.values()]
    assert all(sigma_part(r, k) == tuple(sigma) for r in out)
    return out


def sigma_part(rows, k):
    return tuple(r & ((1 << k) - 1) for r in rows[:k])


def amalgams(F1, F2, k, m):
    """yield labelled amalgam graphs (n, rows) of F1 and F2 over the common labelled part 0..k-1"""
    e = m - k
    X1 = list(range(k, m))
    X2 = list(range(k, m))
    low = (1 << k) - 1
    for d in range(0, e + 1):
        for D1 in itertools.combinations(X1, d):
            for D2 in itertools.permutations(X2, d):
                pairs = list(zip(D1, D2))
                ok = all((F1[a] & low) == (F2[b] & low) for a, b in pairs)
                if ok:
                    for (a1, b1), (a2, b2) in itertools.combinations(pairs, 2):
                        if (F1[a1] >> a2 & 1) != (F2[b1] >> b2 & 1):
                            ok = False
                            break
                if not ok:
                    continue
                free1 = [x for x in X1 if x not in D1]
                free2 = [y for y in X2 if y not in D2]
                # vertex numbering of the amalgam: 0..m-1 = F1, then free2 at m.. ; identified y = D2[i] -> D1[i]
                n = m + len(free2)
                idx2 = {y: m + i for i, y in enumerate(free2)}
                for a, b in pairs:
                    idx2[b] = a
                for v in range(k):
                    idx2[v] = v
                base = [0] * n
                for i in range(m):
                    base[i] = F1[i]
                # edges of F2 involving free2 vertices
                for y in free2:
                    for z in range(m):
                        if F2[y] >> z & 1:
                            u, w = idx2[y], idx2[z]
                            base[u] |= 1 << w
                            base[w] |= 1 << u
                slots = [(a, idx2[y]) for a in free1 for y in free2]
                for bits in range(1 << len(slots)):
                    rows = base[:]
                    for t, (u, w) in enumerate(slots):
                        if bits >> t & 1:
                            rows[u] |= 1 << w
                            rows[w] |= 1 << u
                    yield n, rows


def build_matrix(cen, flags, k, m, cache):
    """M[F1,F2] as affine forms: returns (M0, {p: Mp}) numpy arrays"""
    nf = len(flags)
    terms = {}
    for i in range(nf):
        for j in range(i, nf):
            acc = {}
            for n, rows in amalgams(flags[i], flags[j], k, m):
                if n > cen.maxn:
                    raise SystemExit("amalgam of order %d exceeds the census order %d" % (n, cen.maxn))
                key = (n, tuple(rows))
                f = cache.get(key)
                if f is None and key not in cache:
                    f = cen.x_of(n, rows)
                    cache[key] = f
                if f:
                    for p, val in f.items():
                        acc[p] = acc.get(p, 0.0) + val
            terms[(i, j)] = acc
    ps = sorted({p for acc in terms.values() for p in acc})
    mats = {p: np.zeros((nf, nf)) for p in ps}
    for (i, j), acc in terms.items():
        for p, val in acc.items():
            mats[p][i, j] = val
            mats[p][j, i] = val
    return mats


def main():
    path, k, m = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    maxs = int(sys.argv[4]) if len(sys.argv) > 4 and not sys.argv[4].startswith("--") else None
    opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
    t0 = time.time()
    cen = Census(path)
    print("census: order %d, %d parameters, %d types  [%.0f s]" % (cen.maxn, cen.NP, len(cen.form), time.time() - t0),
          flush=True)
    # sigmas: all admissible types of order k (canonical rows from the census types list)
    d = json.load(open(path))
    sigmas = [rows for key, rows, aut, form in d["types"][str(k)]]
    if maxs:
        sigmas = sigmas[:maxs]
    cache = {}
    blocks = []
    for si, sigma in enumerate(sigmas):
        fl = flags_of(sigma, k, m)
        mats = build_matrix(cen, fl, k, m, cache)
        blocks.append((si, sigma, fl, mats))
        print("sigma %d (edges %d): %d flags  [%.0f s]" % (si, sum(bin(r).count('1') for r in sigma) // 2, len(fl),
                                                         time.time() - t0), flush=True)
    # SDP (variables rescaled by an LP reference point; blocks rescaled by a diagonal congruence)
    import cvxpy as cp
    from scipy.optimize import linprog
    NP = cen.NP
    rows_lp = []
    for (n, key), f in cen.form.items():
        c0 = f.get(0, 0.0)
        coef = np.zeros(NP)
        for p, val in f.items():
            if p:
                coef[p - 1] = val
        sc = max(abs(c0), np.abs(coef).max(), 1.0)
        rows_lp.append((coef / sc, c0 / sc))
    A = np.array([r[0] for r in rows_lp])
    b = np.array([r[1] for r in rows_lp])
    ref = linprog(np.ones(NP) * 0.0, A_ub=-A, b_ub=b, bounds=[(0, None)] * NP, method="highs")
    xr = ref.x
    svar = np.maximum(np.abs(xr), 1.0)
    y = cp.Variable(NP)
    xexpr = cp.multiply(svar, y)
    cons = [A @ xexpr + b >= 0, y >= 0]
    for si, sigma, fl, mats in blocks:
        nf0 = len(fl)
        M0 = mats.get(0, np.zeros((nf0, nf0)))
        # facial reduction: restrict to the joint range of all coefficient matrices
        stack = np.hstack([M0] + [Mp for p, Mp in mats.items() if p])
        U, sv, _ = np.linalg.svd(stack, full_matrices=False)
        rk = int((sv > sv.max() * 1e-10).sum()) if sv.size and sv.max() > 0 else 0
        Q = U[:, :rk]
        mats = {p: Q.T @ Mp @ Q for p, Mp in mats.items()}
        nf = rk
        M0 = mats.get(0, np.zeros((nf, nf)))
        print("  block sigma %d: %d flags -> joint range %d" % (si, nf0, nf), flush=True)
        Mref = M0 + sum(xr[p - 1] * Mp for p, Mp in mats.items() if p)
        dg = np.diag(Mref).copy()
        dsc = 1.0 / np.sqrt(np.where(dg > 1e-9, dg, max(dg.max(), 1.0)))
        Dm = np.outer(dsc, dsc)
        B = np.zeros((nf * nf, NP))
        for p, Mp in mats.items():
            if p:
                B[:, p - 1] = (Mp * Dm).reshape(-1) * svar[p - 1]
        c = (M0 * Dm).reshape(-1)
        Mexpr = cp.reshape(B @ y + c, (nf, nf), order="C")
        cons.append((Mexpr + Mexpr.T) / 2 >> 0)
    solver = opts.get("solver", "CLARABEL")
    res = {}
    for sense in (opts.get("objective", "min,max")).split(","):
        obj = cp.Minimize(y[0]) if sense == "min" else cp.Maximize(y[0])
        pr = cp.Problem(obj, cons)
        try:
            pr.solve(solver=solver, verbose=False)
            res[sense] = (pr.status, None if y.value is None else float(y.value[0] * svar[0]))
        except Exception as ex:
            res[sense] = ("ERROR", str(ex)[:200])
        print("P %s: status %s, value %s  [%.0f s]" % (sense, res[sense][0], res[sense][1], time.time() - t0), flush=True)
    for sense in ("min", "max"):
        r = linprog(np.eye(NP)[0] * (1 if sense == "min" else -1), A_ub=-A, b_ub=b, bounds=[(0, None)] * NP,
                    method="highs")
        print("LP only, P %s: %s %s" % (sense, r.status, r.x[0] if r.status == 0 else None), flush=True)
    if "dump" in opts:
        json.dump({"k": k, "m": m, "sigmas": len(blocks), "result": res}, open(opts["dump"], "w"))


if __name__ == "__main__":
    main()
