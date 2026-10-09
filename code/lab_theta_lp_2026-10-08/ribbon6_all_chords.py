"""C1, lab session, 2026-10-09. Injective closed transport ribbon of length 6 (18 distinct roles): ALL sets of extra
edges (chords). Step 1 (this script, mode count): enumerate the chord sets allowed by the local axioms (an edge has at
most one common neighbour, a non-edge at most two; every point has degree at most 14), up to the symmetries of the
ribbon, and keep those whose two projector blocks are positive semidefinite (float). Step 2 (mode test): run the
one-vertex multiplicity system on the survivors.
  python ribbon6_all_chords.py <cylinder|moebius> count <max chords>
  python ribbon6_all_chords.py <cylinder|moebius> test <max chords> <time budget s>"""
import sys, itertools, collections, time, json
import numpy as np
m = 6; MO = sys.argv[1] == "moebius"; MODE = sys.argv[2]; KMAX = int(sys.argv[3])
names = ["a%d" % i for i in range(m)] + ["b%d" % i for i in range(m)] + ["c%d" % i for i in range(m)]; ix = {s: i for i, s in enumerate(names)}; E0 = []
for i in range(m):
    if i < m - 1 or not MO: an, bn = "a%d" % ((i + 1) % m), "b%d" % ((i + 1) % m)
    else: an, bn = "b0", "a0"
    for x, y in (("c%d" % i, "a%d" % i), ("c%d" % i, an), ("a%d" % i, an), ("c%d" % i, "b%d" % i), ("c%d" % i, bn), ("b%d" % i, bn)): E0.append((ix[x], ix[y]))
n = len(names); A0 = np.zeros((n, n), dtype=np.int64)
for x, y in E0: A0[x, y] = A0[y, x] = 1
adj0 = [set(np.nonzero(A0[i])[0].tolist()) for i in range(n)]
# automorphisms of the ribbon graph (backtracking)
auts = []
def ext(p):
    k = len(p)
    if k == n: auts.append(tuple(p)); return
    for v in range(n):
        if v in p: continue
        if all((p[u] in adj0[v]) == (u in adj0[k]) for u in range(k)): ext(p + [v])
ext([])
A2 = A0 @ A0
cand = [(x, y) for x in range(n) for y in range(x + 1, n) if not A0[x, y] and A2[x, y] == 0]
J = np.ones((n, n)); I = np.eye(n)


def local_ok(A):
    B = A @ A
    return bool(((B * A) <= 1).all() and ((B * (1 - A - np.eye(n, dtype=np.int64))) <= 2).all())


def canon(S):
    return min(tuple(sorted(tuple(sorted((p[x], p[y]))) for x, y in S)) for p in auts)


seen = set(); by = collections.Counter(); psd = []
def rec(start, S, A):
    key = canon(S)
    if key in seen: return
    seen.add(key); by[(len(S), "local")] += 1
    if S:
        Af = A.astype(float)
        if np.linalg.eigvalsh(3 * I - Af + J / 9).min() > -1e-9 and np.linalg.eigvalsh(Af + 4 * I - 2 * J / 11).min() > -1e-9:
            by[(len(S), "PSD")] += 1; psd.append(key)
    if len(S) == KMAX: return
    for t in range(start, len(cand)):
        x, y = cand[t]; A[x, y] = A[y, x] = 1
        if local_ok(A): rec(t + 1, S + [cand[t]], A)
        A[x, y] = A[y, x] = 0
t0 = time.time(); rec(0, [], A0.copy())
print("%s: |Aut| = %d, %d candidate chords; classes of chord sets by size (local / PSD): %s  [%.0f s]"
      % (sys.argv[1], len(auts), len(cand), {k: (by[(k, "local")], by[(k, "PSD")]) for k in range(KMAX + 1)}, time.time() - t0), flush=True)
json.dump([[list(e) for e in key] for key in psd], open("ribbon6_%s_psd_chordsets_k%d.json" % (sys.argv[1], KMAX), "w"))
if MODE == "test":
    import support_masks as S_
    BUD = float(sys.argv[4]); tally = collections.Counter(); passing = []
    for key in sorted(psd, key=lambda k_: (len(k_), k_)):
        if time.time() - t0 > BUD: tally[(len(key), "not tested")] += 1; continue
        r = S_.verdict(n, E0 + [tuple(e) for e in key]); st = r["status"].split(" (")[0]; tally[(len(key), st)] += 1
        if st == "feasible": passing.append([[names[x], names[y]] for x, y in key])
    print("multiplicity system on the PSD classes (size, verdict) -> count:", dict(sorted(tally.items())), " [%.0f s]" % (time.time() - t0))
    json.dump(passing, open("ribbon6_%s_passing_k%d.json" % (sys.argv[1], KMAX), "w"))
    for p in passing[:40]: print("   passes:", ", ".join("%s-%s" % tuple(e) for e in p))
