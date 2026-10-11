"""BvLS in coordinates: vertices = F_3^5 (syndromes), S = {+-h_1..h_11}. Index map consistent with bvls243.edges."""
import itertools, numpy as np
from lib243 import load_edges

def golay_coords():
    import sys; sys.path.insert(0, '../omega')
    G = np.array([[1,0,0,0,0,0,1,1,1,1,1],[0,1,0,0,0,0,0,1,2,2,1],[0,0,1,0,0,0,1,0,1,2,2],
                  [0,0,0,1,0,0,2,1,0,1,2],[0,0,0,0,1,0,2,2,1,0,1],[0,0,0,0,0,1,1,2,2,1,0]])
    dual = []
    for w in itertools.product(range(3), repeat=11):
        if all(sum(a * b for a, b in zip(w, g)) % 3 == 0 for g in G) and any(w):
            dual.append(w)
            if len(dual) > 400: break
    H = []
    def span(M):
        S = set()
        for c in itertools.product(range(3), repeat=len(M)):
            S.add(tuple((np.array(c) @ np.array(M)) % 3))
        return S
    for w in dual:
        if len(span(H + [w])) == 3 ** (len(H) + 1): H.append(w)
        if len(H) == 5: break
    H = np.array(H)
    allsy = sorted(itertools.product(range(3), repeat=5))
    return G, H, allsy

if __name__ == "__main__":
    G, H, allsy = golay_coords()
    A = load_edges("bvls243.edges")
    idx = {s: i for i, s in enumerate(allsy)}
    hs = [tuple(H[:, p] % 3) for p in range(11)]
    # check adjacency = difference in +-h
    ok = all(A[idx[s], idx[tuple((np.array(s) + np.array(h) * e) % 3)]] for s in allsy for h in hs for e in (1, 2))
    print("coords consistent:", ok)
    np.save("golayH.npy", H)
