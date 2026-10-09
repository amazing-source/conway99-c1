"""C1, lab session, 2026-10-09. Second-level mask filter for a support H of an srg(99,14,1,2).
First level (support_masks / certify_supports): masks b of one outside vertex filtered by the local axioms and the two
exact Schur complements, then the multiplicity system. Second level: a mask b is kept only if the support H + z_b
(z_b adjacent to b) itself passes the first level; the multiplicity system of H is then solved again with the masks
that are left. Masks are tested once per orbit of Aut(H). Float LP indications; `exact` adds Farkas certificates
for the removed masks and for the final system.
  python second_level.py ribbon6tri <cylinder|moebius>        the 6-ribbon whose chords are the triangle c0 c2 c4
  python second_level.py ribbon5 <cylinder|moebius>           the clean 5-ribbon
As a module: second_level(n, edges) -> dict."""
import sys, time, collections
import numpy as np
from scipy.optimize import linprog
import support_masks as S
import certify_supports as C


def automorphisms(n, edges):
    adj = [set() for _ in range(n)]
    for x, y in edges: adj[x].add(y); adj[y].add(x)
    auts = []
    def ext(p):
        k = len(p)
        if k == n: auts.append(tuple(p)); return
        for v in range(n):
            if v in p or len(adj[v]) != len(adj[k]): continue
            if all((p[u] in adj[v]) == (u in adj[k]) for u in range(k)): ext(p + [v])
    ext([]); return auts


def second_level(n, edges, verbose=True):
    t0 = time.time(); masks, rows, rhs, lab = C.system(n, edges); auts = automorphisms(n, edges)
    orb = {}
    for j, s in enumerate(masks):
        key = min(tuple(sorted(p[v] for v in s)) for p in auts); orb.setdefault(key, []).append(j)
    keep = np.ones(len(masks), dtype=bool); removed = []
    for key, members in sorted(orb.items(), key=lambda t: (len(t[0]), t[0])):
        if len(key) == 0: continue
        r = S.verdict(n + 1, list(edges) + [(n, v) for v in key])
        if not r["status"].startswith("feasible"):
            for j in members: keep[j] = False
            removed.append((key, len(members), r["status"].split(" (")[0]))
    A = np.array(rows, dtype=float)[:, keep]; res = {"masks": len(masks), "orbits": len(orb), "automorphisms": len(auts), "removed": removed, "left": int(keep.sum())}
    if keep.sum() == 0: res["status"] = "INFEASIBLE (no mask left)"
    else:
        fl = linprog(np.zeros(A.shape[1]), A_eq=A, b_eq=np.array(rhs, dtype=float), bounds=[(0, None)] * A.shape[1], method="highs")
        res["status"] = "feasible (float LP)" if fl.status == 0 else "INFEASIBLE (float LP, status %d)" % fl.status
    res["seconds"] = round(time.time() - t0, 1)
    if verbose:
        print("   first level: %d masks in %d orbits (|Aut| = %d); second level removes %d orbits (%d masks), %d masks left -> %s  [%.0f s]"
              % (res["masks"], res["orbits"], res["automorphisms"], len(removed), sum(c for _, c, _ in removed), res["left"], res["status"], res["seconds"]), flush=True)
        by = collections.Counter((len(k), st) for k, c, st in removed)
        if removed: print("   removed orbits by (mask size, reason):", dict(sorted(by.items())))
    return res


def ribbon(m, MO, chords=()):
    names = ["a%d" % i for i in range(m)] + ["b%d" % i for i in range(m)] + ["c%d" % i for i in range(m)]; ix = {s: i for i, s in enumerate(names)}; E0 = []
    for i in range(m):
        if i < m - 1 or not MO: an, bn = "a%d" % ((i + 1) % m), "b%d" % ((i + 1) % m)
        else: an, bn = "b0", "a0"
        for x, y in (("c%d" % i, "a%d" % i), ("c%d" % i, an), ("a%d" % i, an), ("c%d" % i, "b%d" % i), ("c%d" % i, bn), ("b%d" % i, bn)): E0.append((ix[x], ix[y]))
    return names, E0 + [(ix[u], ix[v]) for u, v in chords]


if __name__ == "__main__":
    what = sys.argv[1]; MO = sys.argv[2] == "moebius"
    if what == "ribbon6tri": names, E = ribbon(6, MO, (("c0", "c2"), ("c2", "c4"), ("c0", "c4")))
    elif what == "ribbon5": names, E = ribbon(5, MO)
    print("%s %s: %d points, first level: %s" % (what, sys.argv[2], len(names), S.verdict(len(names), E)["status"]), flush=True)
    second_level(len(names), E)
