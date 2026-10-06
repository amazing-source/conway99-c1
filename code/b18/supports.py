"""Branch 18, level 0: the supports.
z integer, Az = -4z, ||z||^2 = 18: P (9 vertices, +1), N (9, -1), both independent; D = P x N biadjacency is
4-regular, two rows share <= 2 columns and two columns share <= 2 rows (mu = 2 for non-adjacent same-sign pairs).
Enumerate D up to row/column permutations and transposition (z -> -z)."""
import itertools, json, sys, time
import networkx as nx

ROWS = [frozenset(c) for c in itertools.combinations(range(9), 4)]

def gen():
    out = []
    first = frozenset(range(4))
    colsum = [0] * 9
    chosen = [first]
    for c in first: colsum[c] += 1
    colpair = {}
    def addpairs(r, s):
        for a, b in itertools.combinations(sorted(r), 2):
            colpair[(a, b)] = colpair.get((a, b), 0) + s
    addpairs(first, 1)
    order = sorted(ROWS, key=lambda r: tuple(sorted(r)))
    idx = {r: i for i, r in enumerate(order)}
    def rec(start):
        if len(chosen) == 9:
            if all(c == 4 for c in colsum):
                out.append(list(chosen))
            return
        # columns must reach 4: remaining rows*4 must fill deficits
        for i in range(start, len(order)):
            r = order[i]
            if any(colsum[c] >= 4 for c in r): continue
            if any(len(r & s) > 2 for s in chosen): continue
            if any(colpair.get((a, b), 0) >= 2 for a, b in itertools.combinations(sorted(r), 2)): continue
            chosen.append(r)
            for c in r: colsum[c] += 1
            addpairs(r, 1)
            rec(i + 1)
            addpairs(r, -1)
            for c in r: colsum[c] -= 1
            chosen.pop()
    rec(idx[first] + 1)
    return out

def graph(rows, transpose=False):
    G = nx.Graph()
    for i in range(9):
        G.add_node(("P", i), side=0); G.add_node(("N", i), side=1)
    for i, r in enumerate(rows):
        for c in r:
            G.add_edge(("P", i), ("N", c))
    return G

if __name__ == "__main__":
    t = time.time()
    sols = gen()
    print("lex-ordered labelled solutions (first row fixed):", len(sols), round(time.time() - t, 1), flush=True)
    reps = []
    buckets = {}
    nm = lambda a, b: a["side"] == b["side"]
    for rows in sols:
        G = graph(rows)
        h = nx.weisfeiler_lehman_graph_hash(G, node_attr=None, iterations=4)
        lst = buckets.setdefault(h, [])
        if any(nx.is_isomorphic(G, H) for H, _ in lst):  # iso as uncoloured graph = up to transpose too
            continue
        lst.append((G, rows))
        reps.append(rows)
    print("supports up to row/col perms and transposition:", len(reps), round(time.time() - t, 1))
    json.dump([[sorted(r) for r in rows] for rows in reps], open("supports18.json", "w"))
