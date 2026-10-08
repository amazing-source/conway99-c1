"""C1, lab session, 2026-10-09. Bounded PILOT: forced closure of the 14-vertex cores (division of work agreed with Codex).
  python twisted_core_closure.py <twisted_core_check.json> <out json> <first> <step> <max cores> <node cap per core>
What is added to a core H = S + 8 doubles: only vertices that are FORCED and UNIQUELY IDENTIFIED, namely the third point
w(s, d) of the line through an edge (s, d), s in S, d a double containing s, when that edge has no common neighbour in H.
They are pairwise distinct and outside H: a vertex adjacent to two points of S is a double, hence in H; and w(s, d) =
w(s, d') would put d and d' on one line through s. Each w(s, d) is a "single" at s: its neighbours in S are exactly {s}.
Unknown and enumerated exhaustively: the edges between the new vertices and the doubles, and among the new vertices.
Necessary conditions used (valid at every rank): every pair of H' = H + new vertices has at most 2 - A common neighbours
inside H' (monotone, used for pruning); the two projector blocks 27I - 9A + J and 44I + 11A - 2J of every vertex subset
are positive semidefinite (tested when all pairs of H + the first j new vertices are decided; screened in floating point,
and a rejection is counted only with an EXACT certificate: an integer vector z with z^T Q z < 0 obtained by rounding the
floating eigenvector and checked in integers, or else the exact rational test of twisted_core_check.py).
Optional 7th argument: a json list of "bits" restricting the cores (e.g. those left unresolved by Codex's mask LP).
Per core: node cap and an 18 s time cap; "survivors per level" = partial configurations passing both tests after j new vertices.
Outcome per core: DEAD (exhaustive search, no completion of H'), ALIVE (exhaustive, number of completions), or CAP (node
cap reached: unknown, never counted as an exclusion). This measures whether cores die at small depth; it is not a
classification of completions. One process, below 1 GB."""
import sys, json, time, importlib.util, os
import numpy as np
spec = importlib.util.spec_from_file_location("tcc", os.path.join(os.path.dirname(os.path.abspath(__file__)), "twisted_core_check.py"))
src = open(spec.origin, encoding="utf-8").read().split("def psd_or_vector")[1].split("\nout = ")[0]; ns = {"Fr": __import__("fractions").Fraction}
exec("def psd_or_vector" + src, ns); psd_or_vector = ns["psd_or_vector"]
D = json.load(open(sys.argv[1])); first, step, maxc, cap = (int(x) for x in sys.argv[3:7]); t00 = time.time()
SUP = {6: (0, 3), 7: (1, 4), 8: (2, 3), 9: (2, 4), 10: (0, 5), 11: (1, 5), 12: (2, 5), 13: (2, 5)}
def exact_fail(a):
    n = len(a); Qm = [[27 * int(i == j) - 9 * int(a[i][j]) + 1 for j in range(n)] for i in range(n)]; Qp = [[44 * int(i == j) + 11 * int(a[i][j]) - 2 for j in range(n)] for i in range(n)]
    return psd_or_vector(Qm) is not None or psd_or_vector(Qp) is not None
def psd_ok(a):
    """True unless an EXACT integer certificate z^T Q z < 0 exists for one of the two blocks."""
    n = len(a); A = a.astype(float); I = np.eye(n)
    for Qf, Qi in ((27 * I - 9 * A + 1, 27 * np.eye(n, dtype=object) - 9 * a.astype(object) + 1), (44 * I + 11 * A - 2, 44 * np.eye(n, dtype=object) + 11 * a.astype(object) - 2)):
        w, v = np.linalg.eigh(Qf)
        if w[0] > -1e-7: continue
        for scale in (10 ** 3, 10 ** 5, 10 ** 7):                     # fast exact certificate from the floating eigenvector
            z = np.array([int(round(x)) for x in v[:, 0] / np.abs(v[:, 0]).max() * scale], dtype=object)
            if int(z @ Qi @ z) < 0: return False
        if exact_fail(a.tolist()): return False                       # fallback: exact rational elimination
    return True
passing = [c for c in D["cores"] if not c["excluded"]]; out = {"cores_total_passing": len(passing), "results": []}
if len(sys.argv) > 7:                                                   # optional: restrict to the cores listed in a json file (list of "bits" of twisted_core_check.json)
    keepbits = set(json.load(open(sys.argv[7]))); passing = [c for c in passing if c["bits"] in keepbits]; out["restricted_to"] = len(passing)
for ci in range(first, len(passing), step)[:maxc]:
    c = passing[ci]; t0 = time.time(); a = np.zeros((14, 14), dtype=np.int64)
    for u, v in [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 3), (1, 4)] + [(d, s) for d, sp in SUP.items() for s in sp] + [tuple(e) for e in c["edges_among_doubles"]]: a[u, v] = a[v, u] = 1
    new = [(s, d) for d, sp in SUP.items() for s in sp if (a[s] & a[d]).sum() == 0]; n = 14 + len(new); A = np.zeros((n, n), dtype=np.int64); A[:14, :14] = a
    for j, (s, d) in enumerate(new): A[14 + j, s] = A[s, 14 + j] = 1; A[14 + j, d] = A[d, 14 + j] = 1
    def viol(M): cn = M @ M; np.fill_diagonal(cn, 0); return bool((cn > 2 - M).any())
    assert not viol(A), "base with forced vertices already violates"
    groups = []                                                        # per new vertex: its free pairs with doubles and earlier new vertices
    for j in range(len(new)):
        g = []
        for x in list(range(6, 14)) + list(range(14, 14 + j)):
            if A[14 + j, x]: continue
            A[14 + j, x] = A[x, 14 + j] = 1; bad = viol(A); A[14 + j, x] = A[x, 14 + j] = 0
            if not bad: g.append((14 + j, x))
        groups.append(g)
    nodes = [0]; sols = [0]; capped = [False]; kill = {"common_neighbours": 0, "positivity": 0}; level = [0] * (len(new) + 1); tcore = time.time()
    def rec(j, k):
        if capped[0]: return
        nodes[0] += 1
        if nodes[0] > cap or (nodes[0] % 2000 == 0 and time.time() - tcore > 18): capped[0] = True; return
        if j == len(groups): sols[0] += 1; return
        if k == len(groups[j]):
            m = 15 + j
            if psd_ok(A[:m, :m]): level[j + 1] += 1; rec(j + 1, 0)
            else: kill["positivity"] += 1
            return
        u, v = groups[j][k]; rec(j, k + 1)
        A[u, v] = A[v, u] = 1
        if not viol(A[:15 + j, :15 + j]): rec(j, k + 1)
        else: kill["common_neighbours"] += 1
        A[u, v] = A[v, u] = 0
    rec(0, 0); status = "CAP" if capped[0] else ("DEAD" if sols[0] == 0 else "ALIVE")
    out["results"].append({"core_index": ci, "bits": c["bits"], "edges_among_doubles": len(c["edges_among_doubles"]), "forced_new_vertices": len(new), "free_pairs": sum(len(g) for g in groups),
                           "status": status, "completions": None if capped[0] else sols[0], "nodes": nodes[0], "pruned": kill, "survivors_after_j_new_vertices": level[1:], "seconds": round(time.time() - t0, 2)})
    if time.time() - t00 > 250: break
json.dump(out, open(sys.argv[2], "w"), indent=0); R = out["results"]
print("cores tested %d of %d passing (first %d, step %d, node cap %d): DEAD %d, ALIVE %d, CAP %d   [%.0f s]" % (len(R), len(passing), first, step, cap, sum(r["status"] == "DEAD" for r in R), sum(r["status"] == "ALIVE" for r in R), sum(r["status"] == "CAP" for r in R), time.time() - t00))
print("forced new vertices per core: min %d max %d; free pairs: min %d max %d" % (min(r["forced_new_vertices"] for r in R), max(r["forced_new_vertices"] for r in R), min(r["free_pairs"] for r in R), max(r["free_pairs"] for r in R)))
al = [r for r in R if r["status"] == "ALIVE"]
if al: print("ALIVE cores: completions min %d median %d max %d" % (min(r["completions"] for r in al), sorted(r["completions"] for r in al)[len(al) // 2], max(r["completions"] for r in al)))
print("pruning events: common neighbours %d, positivity %d" % (sum(r["pruned"]["common_neighbours"] for r in R), sum(r["pruned"]["positivity"] for r in R)))
for r in R: print("   core", r["core_index"], "e(D)", r["edges_among_doubles"], "new", r["forced_new_vertices"], "free", r["free_pairs"], r["status"], r["completions"], "nodes", r["nodes"], "survivors per level", r["survivors_after_j_new_vertices"], r["seconds"], "s")
