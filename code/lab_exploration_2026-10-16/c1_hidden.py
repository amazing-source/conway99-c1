"""Where the 3-eigenvectors of A_H (H = N(l) u Y) come from, on positive c(l) = 1 sides.
dim E_3(A_H) = dim ker F - 1, and ker F contains 1_{Y2}, 1_{Y3} and the Y-parts of the component vectors of m:
known = 1 + c(m) (independent), hidden = dim ker F - 1 - c(m) = mult_3(A_H) - c(m).
Conway: mult_3(A_H) >= 11, i.e. hidden >= 11 - c(m) (c(m) <= 5 since Q_01 is not a grid when c(l) = 1).
usage: python c1_hidden.py <distinct_cache.jsonl> <max sides>"""
import itertools, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, XL, Y, k8, rank_mod, relabel, build_H, gl_connected

def comps_m(EE):
    """components of the cubic graph on N(m), m = {v,2,3}: letters {0,1,4..13} + labels touching 2 or 3."""
    letters = [0, 1] + list(range(4, 14))
    XM = [l for l in S if l & {2, 3}]
    V = [("L", a) for a in letters] + XM
    pos = {x: i for i, x in enumerate(V)}
    adj = [set() for _ in V]
    def e(x, y):
        adj[pos[x]].add(pos[y]); adj[pos[y]].add(pos[x])
    for a in letters:
        if a ^ 1 in letters and a < (a ^ 1):
            e(("L", a), ("L", a ^ 1))
        for r in (2, 3):
            lab = frozenset((r, a))
            if lab in pos:
                e(("L", a), lab)
    for x, y in itertools.combinations(XM, 2):
        if frozenset((x, y)) in EE:
            e(x, y)
    if any(len(a) != 3 for a in adj):
        return None, None
    seen, comps = set(), []
    for s in range(len(V)):
        if s in seen:
            continue
        st, cc = [s], {s}
        seen.add(s)
        while st:
            u = st.pop()
            for w in adj[u]:
                if w not in seen:
                    seen.add(w); cc.add(w); st.append(w)
        comps.append(sorted(len(cc) for _ in [0])[0])
    return len(comps), sorted(comps)

def main():
    mx = int(sys.argv[2])
    P1, P2 = 1000000007, 998244353
    tab = Counter()
    done = 0
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
            G = np.zeros((44, 44))
            for i, j in itertools.combinations(range(44), 2):
                if frozenset((S[i], S[j])) in EE:
                    G[i, j] = G[j, i] = 1
            K8 = np.array([[k8(a, b) for b in S] for a in S], float)
            T8 = 24 * np.eye(44) - 8 * G - K8
            if np.linalg.eigvalsh(T8 / 8)[0] < -1e-9:
                continue
            V, A = build_H(EE)
            M = (A - 3 * np.eye(len(V), dtype=np.int64)).tolist()
            m56 = len(V) - min(rank_mod(M, P1), rank_mod(M, P2))
            cm, sizes = comps_m(EE)
            if cm is None:
                continue
            tab[(cm, m56, m56 - cm)] += 1
            done += 1
            if done >= mx:
                break
        if done >= mx:
            break
    print("sides:", done)
    print("(c(m), mult_3(A_H), hidden = mult_3 - c(m)) : count    [Conway: hidden >= 11 - c(m)]")
    for k, v in sorted(tab.items()):
        print("   ", k, v, "   Conway needs hidden >=", 11 - k[0])

if __name__ == "__main__":
    main()
