"""C1, lab session, 2026-10-09. Clean closed transport ribbon of length 5 (15 points): second level.
Counting gives n1 + 2 n2 + 3 n3 + 4 n4 + 5 n5 = 150 and n2 + 3 n3 + 6 n4 + 10 n5 = 90 for the numbers n_t of outside
vertices with t neighbours in H, hence n1 = 3 n3 + 8 n4 + 15 n5 - 30: at least one outside vertex has three or more
neighbours in H. For every admissible mask S of size >= 3 (one per orbit of the automorphism group of H) the support
H + z, z adjacent to S, is tested with support_masks.verdict. If every such support fails, the clean 5-ribbon is excluded.
  python ribbon5_second_level.py <cylinder|moebius>"""
import sys, itertools, collections, time
import numpy as np
import support_masks as S
m = 5; MO = sys.argv[1] == "moebius"; n = 3 * m
names = ["a%d" % i for i in range(m)] + ["b%d" % i for i in range(m)] + ["c%d" % i for i in range(m)]; ix = {s: i for i, s in enumerate(names)}; E0 = []
for i in range(m):
    if i < m - 1 or not MO: an, bn = "a%d" % ((i + 1) % m), "b%d" % ((i + 1) % m)
    else: an, bn = "b0", "a0"
    for x, y in (("c%d" % i, "a%d" % i), ("c%d" % i, an), ("a%d" % i, an), ("c%d" % i, "b%d" % i), ("c%d" % i, bn), ("b%d" % i, bn)): E0.append((ix[x], ix[y]))
adj = [set() for _ in range(n)]
for x, y in E0: adj[x].add(y); adj[y].add(x)
# automorphisms of H by backtracking (15 vertices)
auts = []
def ext(p):
    k = len(p)
    if k == n: auts.append(tuple(p)); return
    for v in range(n):
        if v in p: continue
        if all((p[u] in adj[v]) == (u in adj[k]) for u in range(k)): ext(p + [v])
ext([])
A2 = [[len(adj[i] & adj[j]) for j in range(n)] for i in range(n)]
cocl = []
def rec(start, cur):
    if len(cur) >= 3 and all(len(adj[u] & set(cur)) <= 2 for u in range(n) if u not in cur): cocl.append(tuple(cur))
    for h in range(start, n):
        if all(h not in adj[g] and 2 - A2[g][h] > 0 for g in cur): rec(h + 1, cur + [h])
rec(0, [])
orb = {}
for s in cocl:
    key = min(tuple(sorted(p[v] for v in s)) for p in auts); orb.setdefault(key, []).append(s)
print("m = 5, %s: |Aut(H)| = %d; candidate masks of size >= 3: %d in %d orbits" % (sys.argv[1], len(auts), len(cocl), len(orb)), flush=True)
t0 = time.time(); tally = collections.Counter()
for key in sorted(orb, key=lambda t: (len(t), t)):
    r = S.verdict(n + 1, E0 + [(n, v) for v in key]); st = r["status"].split(" (")[0]; tally[(len(key), st)] += 1
    print("   mask %s (orbit of %d): %s%s  [%.0f s]" % ([names[v] for v in key], len(orb[key]), r["status"], " masks %d" % r["masks"] if "masks" in r else "", time.time() - t0), flush=True)
print("summary (mask size, verdict) -> orbits:", dict(sorted(tally.items())))
