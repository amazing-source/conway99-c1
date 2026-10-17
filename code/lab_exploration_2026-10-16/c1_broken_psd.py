import json, sys, itertools
from collections import Counter
import numpy as np
sys.path.insert(0, r"C:\Users\RESEARCHER\Downloads\conway_c2_researcher2_start_2026_09_30\conway_c2_researcher2_start_2026_09_30\work\stars_rank_2026-10-14")
sys.path.insert(0, r"C:\Users\RESEARCHER\Downloads\conway_c2_researcher2_start_2026_09_30\conway_c2_researcher2_start_2026_09_30\work\exploration_2026-10-16")
from stars_rank import kval
from gg_test import orient, line_graph, components
from c1_cutfilter import tests
import c1_rlattice as RL
hm = {0: 1, 1: 0, 2: 3, 3: 2}
rows = []
for line in open("distinct_cache.jsonl"):
    d = json.loads(line)
    if len(d["labels"]) != 44:
        continue
    S = [frozenset(x) for x in d["labels"]]
    E = set(frozenset((frozenset(a), frozenset(b))) for a, b in d["edges"])
    n = 44
    G = np.zeros((n, n))
    for i, j in itertools.combinations(range(n), 2):
        if frozenset((S[i], S[j])) in E:
            G[i, j] = G[j, i] = 1
    T = 3 * np.eye(n) - G - np.array([[kval(a, b) for b in S] for a in S])
    ev = np.linalg.eigvalsh(T)
    if ev[0] < -1e-9:
        continue
    idx = {l: i for i, l in enumerate(S)}
    hp = [idx[frozenset(hm.get(y, y) for y in l)] for l in S]
    sp = [(i, j) for i in range(n) for j in range(i + 1, n) if S[i] & S[j] & {0, 1, 2, 3}]
    masym = sum(1 for (i, j) in sp if G[i, j] != G[hp[i], hp[j]])
    if masym == 0:
        continue
    nu = int(np.sum(np.abs(ev) < 1e-7))
    for side in (0, 1):
        L, EE = orient(S, d["edges"], side)
        V, pos, A = line_graph(L, EE)
        if not all(sum(r) == 3 for r in A) or components(A) != 1:
            continue
        gap = np.sort(np.linalg.eigvalsh(3 * np.eye(36) - np.array(A, dtype=float)))[1]
        out, _ = tests(L, EE)
        o = RL.analyse(L, EE)
        killed_rl = any(k.startswith("killed") for k in o)
        rows.append((d["src"], side, masym, nu, round(float(gap), 3), sorted(out), killed_rl))
print("broken (not h-related) PSD blocks with a c = 1 side:", len(rows))
c = Counter((tuple(r[5]), r[6]) for r in rows)
print("filters (cut lemma / E3, R-lattice norm 14) on these sides:", dict(c))
print("gap of G_l: min %.3f median %.3f max %.3f" % (min(r[4] for r in rows), float(np.median([r[4] for r in rows])), max(r[4] for r in rows)))
print("nullity nu(T_S):", dict(Counter(r[3] for r in rows)))
for r in rows[:12]:
    print("  ", r)
