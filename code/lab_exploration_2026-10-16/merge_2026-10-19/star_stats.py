"""Is the death of the star structural or statistical?  (LAB 20/10/2026)

For the star of x (rank 37, Green form), build the pairwise compatibility relation between the candidate triples of
two far vertices W_y, W_y' of the star: distinct q, distinct s, |W n W'| <= 2, g = e_W^T Omega e_W' in {3, 4}, and if
g = 3 (adjacent) then W n W' = {x}, both caps 1 and the NF condition.  Then count EXACTLY the compatible 3-tuples and
4-tuples (cliques in the k-partite compatibility graph) for random choices of y's, and compare with the count predicted
if the pair events were independent: prod |D_y| * prod over pairs of (density of compatible pairs).
A ratio near 1 for k = 3, 4 says the Green values behave like independent random residues on the star (the
refutation is then a counting phenomenon); a large deviation would point to hidden structure (a lemma to find).
Also reports the distribution of g over all candidate pairs (uniform would be 1/7 per residue).
usage: python star_stats.py <seed> <x> <trials>"""
import ctypes
import json
import os
import random
import sys
import time

import numpy as np

if sys.platform == "win32":
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x40)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from star_csp import Star, line_graph  # noqa: E402

P = 7


def compat(st, ya, yb):
    A, B = st.arr[ya], st.arr[yb]
    g = (A["Y"] @ B["E"].T) % P                                   # g[a, b] = e_Wa^T Omega e_Wb
    share = A["E"] @ B["E"].T                                     # |Wa n Wb|
    ok = (A["qi"][:, None] != B["qi"][None, :]) & (A["si"][:, None] != B["si"][None, :]) & (share <= 2)
    ok &= (g == 3) | (g == 4)
    adj = g == 3
    capok = (A["cap"][:, None] == 1) & (B["cap"][None, :] == 1)
    ok &= ~adj | ((share == 1) & capok)
    # NF for adjacent pairs: every name z (other than x) of one has <= 1 G-neighbour in the other
    GA = A["E"] @ st.G                                            # GA[a, z] = |N_G(z) n Wa|
    GB = B["E"] @ st.G
    xa = np.zeros(A["E"].shape[1], dtype=np.int64)
    xa[st.x] = 1
    badA = ((GA > 1) & (xa[None, :] == 0)).astype(np.int64)      # names z with >= 2 neighbours in Wa
    badB = ((GB > 1) & (xa[None, :] == 0)).astype(np.int64)
    nf_bad = (badA @ B["E"].T > 0) | (A["E"] @ badB.T > 0)
    ok &= ~(adj & nf_bad)
    return ok, g


def main():
    seed, x, trials = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    gt, G, Om, K, leg = line_graph(seed, -1)
    st = Star(G, Om, K, x, "")
    rng = random.Random(77 + seed)
    t0 = time.time()
    # distribution of g over all candidate pairs of two random far vertices of the star
    hist = np.zeros(P, dtype=np.int64)
    for _ in range(6):
        ya, yb = rng.sample(st.ys, 2)
        _, g = compat(st, ya, yb)
        hist += np.bincount(g.ravel(), minlength=P)
    out = {"seed": seed, "x": x, "tau_leg": leg, "g_hist_frac": [round(v / hist.sum(), 4) for v in hist.tolist()]}
    res = []
    for _ in range(trials):
        ys = rng.sample(st.ys, 4)
        C = {}
        dens = {}
        for i in range(4):
            for j in range(i + 1, 4):
                c, _ = compat(st, ys[i], ys[j])
                C[(i, j)] = c.astype(np.int64)
                dens[(i, j)] = float(c.mean())
        sizes = [len(st.dom[y]) for y in ys]
        # exact 3-cliques on (0, 1, 2) and 4-cliques on (0, 1, 2, 3)
        n3 = int((C[(0, 1)] * (C[(0, 2)] @ C[(1, 2)].T)).sum())
        pred3 = sizes[0] * sizes[1] * sizes[2] * dens[(0, 1)] * dens[(0, 2)] * dens[(1, 2)]
        # degree-corrected null model: given a, its partners in D1 and D2 are compatible with density dens(1, 2)
        pred3d = float((C[(0, 1)].sum(axis=1) * C[(0, 2)].sum(axis=1)).sum()) * dens[(1, 2)]
        n4 = 0
        for a in range(sizes[0]):
            bs = np.nonzero(C[(0, 1)][a])[0]
            if len(bs) == 0:
                continue
            V = C[(0, 2)][a][None, :] * C[(1, 2)][bs]              # (b, c)
            Wm = C[(0, 3)][a][None, :] * C[(1, 3)][bs]             # (b, d)
            n4 += int(((V @ C[(2, 3)]) * Wm).sum())
        pred4 = float(np.prod(sizes)) * float(np.prod(list(dens.values())))
        res.append({"ys": ys, "dens": [round(d, 4) for d in dens.values()], "n3": n3, "pred3": round(pred3, 1),
                    "ratio3": round(n3 / pred3, 3) if pred3 else None,
                    "ratio3_deg": round(n3 / pred3d, 3) if pred3d else None, "n4": n4, "pred4": round(pred4, 1),
                    "ratio4": round(n4 / pred4, 3) if pred4 else None})
    out["trials"] = res
    out["seconds"] = round(time.time() - t0, 1)
    print(json.dumps(out), flush=True)


if __name__ == "__main__":
    main()
