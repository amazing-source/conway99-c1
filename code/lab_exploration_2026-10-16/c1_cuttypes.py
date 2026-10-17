import itertools, json, sys
from collections import Counter
sys.path.insert(0, r"C:\Users\RESEARCHER\Downloads\conway_c2_researcher2_start_2026_09_30\conway_c2_researcher2_start_2026_09_30\work\exploration_2026-10-16")
from gg_test import orient, line_graph, components
agg = Counter(); n = 0
for line in open("distinct_cache.jsonl"):
    d = json.loads(line)
    if len(d["labels"]) != 44: continue
    for side in (0, 1):
        L, E = orient([frozenset(x) for x in d["labels"]], d["edges"], side)
        V, pos, A = line_graph(L, E)
        if any(sum(r) != 3 for r in A): continue
        c = components(A)
        roots = [(2*j, 2*j+1) for j in range(1, 7)]
        Q = [[frozenset((r, x)) for r in (0, 1) for x in rt] for rt in roots]
        for s in range(1, 4):
            for S in itertools.combinations(range(6), s):
                if s == 3 and 0 not in S: continue
                QS = set(w for j in S for w in Q[j])
                out = [w for k in range(6) if k not in S for w in Q[k]]
                cut = [(a, b) for a in QS for b in out if frozenset((a, b)) in E]
                if len(cut) != 2: continue
                typ = []
                for a, b in cut:
                    ra, rb = (0 if 0 in a else 1), (0 if 0 in b else 1)
                    typ.append("mu%d" % ra if ra == rb else "sig")
                t = tuple(sorted(typ))
                if t == ("sig", "sig"):
                    (a1, b1), (a2, b2) = cut
                    shared = bool(a1 & a2) or bool(b1 & b2)
                    t = t + ("shared" if shared else "DISTINCT",)
                agg[(c, t)] += 1
print(dict(sorted(agg.items())))
