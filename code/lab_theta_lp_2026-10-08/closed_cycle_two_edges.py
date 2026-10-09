"""C1, lab session, 2026-10-09. Closed transport cycle of length m (distinct roles) with TWO extra edges: which pairs
pass the local axioms, positivity and the one-vertex multiplicity system (float LP indication)?
  python closed_cycle_two_edges.py <m> <cylinder|moebius> <time budget s>"""
import sys, itertools, collections, time
import numpy as np
import support_masks as S
m = int(sys.argv[1]); MO = sys.argv[2] == "moebius"; BUD = float(sys.argv[3])
names = ["a%d" % i for i in range(m)] + ["b%d" % i for i in range(m)] + ["c%d" % i for i in range(m)]; ix = {s: i for i, s in enumerate(names)}
E0 = []
for i in range(m):
    if i < m - 1 or not MO: an, bn = "a%d" % ((i + 1) % m), "b%d" % ((i + 1) % m)
    else: an, bn = "b0", "a0"
    for x, y in (("c%d" % i, "a%d" % i), ("c%d" % i, an), ("a%d" % i, an), ("c%d" % i, "b%d" % i), ("c%d" % i, bn), ("b%d" % i, bn)): E0.append((ix[x], ix[y]))
n = len(names); base = set(tuple(sorted(e)) for e in E0)
A0 = np.zeros((n, n))
for x, y in E0: A0[x, y] = A0[y, x] = 1
# automorphism group of the ribbon graph by brute force on generators found among simple maps
def shift(s):
    t, i = s[0], int(s[1:])
    if MO and t in "ab" and i == m - 1: return ("b" if t == "a" else "a") + "0"
    return "%s%d" % (t, (i + 1) % m)
def swap(s): return (("b" if s[0] == "a" else "a") if s[0] in "ab" else "c") + s[1:]
def refl(s):
    t, i = s[0], int(s[1:])
    if t == "c": return "c%d" % ((-i - 1) % m)
    if MO and i != 0: t = "b" if t == "a" else "a"
    return "%s%d" % (t, (-i) % m)
gens = [g for g in (shift, swap, refl) if all(tuple(sorted((ix[g(names[p])], ix[g(names[q])]))) in base for p, q in E0)]
perms = {tuple(range(n))}; st = [tuple(range(n))]
while st:
    p = st.pop()
    for g in gens:
        q = tuple(ix[g(names[p[i]])] for i in range(n))
        if q not in perms: perms.add(q); st.append(q)
# candidate extra edges: pairs with no common neighbour in the ribbon (otherwise an edge of the ribbon would get a second triangle)
A2 = A0 @ A0
cand = [(x, y) for x in range(n) for y in range(x + 1, n) if not A0[x, y] and A2[x, y] == 0]
print("m = %d, %s: group of order %d, %d candidate extra edges" % (m, sys.argv[2], len(perms), len(cand)), flush=True)
J = np.ones((n, n)); done = set(); tally = collections.Counter(); t0 = time.time()
for e1, e2 in itertools.combinations(cand, 2):
    key = min(tuple(sorted((tuple(sorted((p[e1[0]], p[e1[1]]))), tuple(sorted((p[e2[0]], p[e2[1]])))))) for p in perms)
    if key in done: continue
    done.add(key)
    A = A0.copy()
    for x, y in (e1, e2): A[x, y] = A[y, x] = 1
    if np.linalg.eigvalsh(3 * np.eye(n) - A + J / 9).min() < -1e-7: tally["NOT PSD"] += 1; continue
    if time.time() - t0 > BUD: tally["not tested (budget)"] += 1; continue
    r = S.verdict(n, E0 + [e1, e2]); tally[r["status"].split(" (")[0]] += 1
    if r["status"].startswith("feasible"): print("   %s-%s, %s-%s : %s (masks %d)  [%.0f s]" % (names[e1[0]], names[e1[1]], names[e2[0]], names[e2[1]], r["status"], r["masks"], time.time() - t0), flush=True)
print("summary over %d classes of pairs of extra edges:" % len(done), dict(tally))
