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
    psd = ev[0] > -1e-9
    nu = int(np.sum(np.abs(ev) < 1e-7))
    idx = {l: i for i, l in enumerate(S)}
    hp = [idx[frozenset(hm.get(y, y) for y in l)] for l in S]
    sp = [(i, j) for i in range(n) for j in range(i + 1, n) if S[i] & S[j] & {0, 1, 2, 3}]
    masym = sum(1 for (i, j) in sp if G[i, j] != G[hp[i], hp[j]])
    for side in (0, 1):
        L, EE = orient(S, d["edges"], side)
        V, pos, A = line_graph(L, EE)
        if not all(sum(r) == 3 for r in A) or components(A) != 1:
            continue
        gap = float(np.sort(np.linalg.eigvalsh(3 * np.eye(36) - np.array(A, dtype=float)))[1])
        out, _ = tests(L, EE)
        killed = bool(out)
        if not killed:
            o = RL.analyse(L, EE)
            killed = any(k.startswith("killed") for k in o)
        rows.append((psd, gap, killed, nu, masym, d["src"]))
for lo, hi in ((0, 0.14), (0.14, 0.2), (0.2, 0.3), (0.3, 1.0)):
    sel = [r for r in rows if lo <= r[1] < hi]
    c = Counter((r[0], r[2]) for r in sel)
    nus = Counter(r[3] for r in sel if r[0] and not r[2])
    print("gap in [%.2f, %.2f): %4d sides ; (PSD, killed by integer lemmas): %s ; nu of PSD survivors %s" % (lo, hi, len(sel), dict(c), dict(nus)))
big = [r for r in rows if r[1] >= 0.2 and r[0]]
for r in big[:8]:
    print("   PSD, gap %.3f, killed %s, nu %d, h-asym %d, %s" % (r[1], r[2], r[3], r[4], r[5]))
