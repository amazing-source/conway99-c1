"""For an affine line system containing the h_d spread: per grid coset Pi = p + <h_d,h_m>, which direction class
h_m + e h_d is used (uniform e, or 'mixed').  Reduce by the transvection gauge x -> x + f(x) h_d."""
import sys, itertools, collections, numpy as np
from lines_model import *
from lib243 import *

def e_table(G, d=0):
    tri = set(triangles(G)); hd = HS[d]
    tab = {}
    for mm in range(11):
        if mm == d: continue
        seen = set()
        for p in PTS:
            # coset key: p mod <h_d,h_m>
            key = min(add(add(p, hd, a), HS[mm], b) for a in range(3) for b in range(3))
            if (mm, key) in seen: continue
            seen.add((mm, key))
            es = []
            for a in range(3):
                q = add(p, hd, a)
                lst = [e for e in range(3) if line(q, add(HS[mm], hd, e)) in tri]
                es.append(tuple(lst))
            tab[(mm, key)] = es
    return tab

def summarise(G, d=0):
    tab = e_table(G, d)
    uni = {k: v[0][0] for k, v in tab.items() if all(len(x) == 1 for x in v) and len({x[0] for x in v}) == 1}
    mixed = {k: v for k, v in tab.items() if k not in uni}
    # gauge: e'(m,coset) = e - f(h_m) for f in F_3^{10} restricted to linear functionals: f(h_m) determined by f on basis
    # brute force over linear f with f(h_d)=0 : 3^4 choices
    H = np.load("golayH.npy") % 3
    best = None
    for fv in itertools.product(range(3), repeat=5):
        if (np.array(fv) @ np.array(HS[d])) % 3: continue
        fm = {mm: int(np.array(fv) @ np.array(HS[mm])) % 3 for mm in range(11)}
        nz = sum(1 for (mm, key), e in uni.items() if (e - fm[mm]) % 3)
        if best is None or nz < best[0]: best = (nz, fm)
    return len(tab), len(uni), len(mixed), best

if __name__ == "__main__":
    for f in sys.argv[1:]:
        G = np.load(f) if f.endswith(".npy") else load_edges(f)
        n, u, mx, best = summarise(G)
        print(f, "cosets", n, "uniform", u, "mixed", mx, "min #re-ruled cosets over gauge:", best[0])
