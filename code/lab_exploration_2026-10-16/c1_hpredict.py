"""What predicts the number h of hidden 3-eigenvectors (c(l) = c(m) = 1, positive blocks)?  h = mult_3(A_H56) - c(m).
Statistics: e-profiles of the 6 l-rectangles and 6 m-rectangles, cycles of the 2-regular graphs on X_l and X_m,
rainbow triangles of G_l and G_m (sigma fixed points), edges between Y and Y' (the two far sets), edges inside Y, Y'."""
import itertools, json, sys
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, XL, Y, k8, rank_mod, relabel, build_H, gl_connected
from c1_hidden import comps_m

def cycles_2reg(labels, EE):
    adj = defaultdict(list)
    for a, b in itertools.combinations(labels, 2):
        if frozenset((a, b)) in EE:
            adj[a].append(b); adj[b].append(a)
    seen, cyc = set(), []
    for s in labels:
        if s in seen:
            continue
        st, n = [s], 0
        seen.add(s)
        while st:
            u = st.pop(); n += 1
            for w in adj[u]:
                if w not in seen:
                    seen.add(w); st.append(w)
        cyc.append(n)
    return sorted(cyc)

def eprof(EE, r0, r1):
    out = []
    for j in range(7):
        if j * 2 in (r0, r1):
            continue
        Q = [frozenset((r, s)) for r in (r0, r1) for s in (2 * j, 2 * j + 1)]
        out.append(sum(1 for a, b in itertools.combinations(Q, 2) if frozenset((a, b)) in EE))
    return tuple(sorted(out))

def main():
    mx = int(sys.argv[2])
    rows = []
    for line in open(sys.argv[1]):
        d = json.loads(line)
        if len(d["labels"]) != 44:
            continue
        S0 = [frozenset(x) for x in d["labels"]]
        E0 = [(frozenset(a), frozenset(b)) for a, b in d["edges"]]
        for side in (0, 1):
            L, EE = relabel(S0, E0, side)
            conn, degok = gl_connected(EE)
            if not (conn and degok):
                continue
            cm, _ = comps_m(EE)
            if cm != 1:
                continue
            n = 44
            G = np.zeros((n, n))
            for i, j in itertools.combinations(range(n), 2):
                if frozenset((S[i], S[j])) in EE:
                    G[i, j] = G[j, i] = 1
            K8 = np.array([[k8(a, b) for b in S] for a in S], float)
            if np.linalg.eigvalsh((24 * np.eye(n) - 8 * G - K8) / 8)[0] < -1e-9:
                continue
            V, A = build_H(EE)
            h = len(V) - rank_mod((A - 3 * np.eye(len(V), dtype=np.int64)).tolist(), 1000000007) - cm
            XM = [l for l in S if l & {2, 3}]
            Yp = [l for l in XL if not (l & {2, 3})]
            cyl = cycles_2reg(XL, EE)
            cym = cycles_2reg(XM, EE)
            fixl = sum(1 for t in range(2, 14) if frozenset((frozenset((0, t)), frozenset((1, t)))) in EE)
            fixm = sum(1 for t in [0, 1] + list(range(4, 14)) if frozenset((frozenset((2, t)), frozenset((3, t)))) in EE)
            eYYp = sum(1 for a in Y for b in Yp if frozenset((a, b)) in EE)
            eYY = sum(1 for a, b in itertools.combinations(Y, 2) if frozenset((a, b)) in EE)
            eYpYp = sum(1 for a, b in itertools.combinations(Yp, 2) if frozenset((a, b)) in EE)
            rows.append((h, eprof(EE, 0, 1), eprof(EE, 2, 3), len(cyl), len(cym), fixl, fixm, eYYp, eYY, eYpYp))
        if len(rows) >= mx:
            break
    print("c(l) = c(m) = 1 positive sides:", len(rows))
    hs = Counter(r[0] for r in rows)
    print("h histogram:", dict(sorted(hs.items())), "  (Conway needs h >= 10)")
    names = ["e-prof l", "e-prof m", "#cycles X_l", "#cycles X_m", "rainbow l", "rainbow m", "|E(Y,Y')|", "|E(Y)|", "|E(Y')|"]
    for k, nm in enumerate(names, start=1):
        by = defaultdict(Counter)
        for r in rows:
            by[r[k]][r[0]] += 1
        items = sorted(by.items(), key=lambda t: -sum(t[1].values()))[:8]
        print("  %-12s:" % nm, "; ".join("%s -> %s" % (key, dict(sorted(c.items()))) for key, c in items))

main()
