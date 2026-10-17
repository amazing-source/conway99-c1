"""Summary table of the srg(243,22,1,2) family: for each .edges file in data/srg243/family (plus BvLS and the twin),
independent srg check (pure Python), nauty |Aut| with generators verified as automorphisms and the generated group's
order recomputed by Schreier-Sims (sympy), grids, flat BH-grids (= (grids-270)/3), twisted pairs, prisms, hexagons,
number of regular spreads, pairwise non-isomorphism (nauty canonical forms)."""
import glob, os, sys, numpy as np
from sympy.combinatorics import Permutation, PermutationGroup
from lib243 import *
from certify import load as pload, check_srg
from spreads import regular_spreads

H0, PMAX = 4980690, 8910
files = ["bvls243.edges", "twin243_switched.edges"] + sorted(glob.glob("../../data/srg243/family/*.edges"))
rows, canons = [], {}
for f in files:
    n, nb = pload(f); bad = check_srg(n, nb)
    G = load_edges(f); o, orb, gens = aut(G)
    okg = all((G[np.ix_(g, g)] == G).all() for g in gens)
    so = PermutationGroup([Permutation(g) for g in gens]).order() if gens else 1
    _, ng = grids_per_vertex(G); tw, pr = twisted_pairs(G)
    sp, st = regular_spreads(G, 100)
    c = canon_g6(G); dup = canons.get(c); canons.setdefault(c, os.path.basename(f))
    rows.append((os.path.basename(f), bad, o, so, okg, sorted(len(x) for x in orb), ng, (ng - 270) // 3, tw, pr,
                 H0 + 3 * (PMAX - pr), len(sp), dup))
print("| graph | srg violations | \\|Aut\\| (nauty) | Schreier-Sims | gens ok | orbits | grids | flat BH-grids | twisted | prisms | hexagons | regular spreads | isomorphic to |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    orbs = r[5] if len(r[5]) <= 6 else f"{len(r[5])} orbits"
    print(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {orbs} | {r[6]} | {r[7]} | {r[8]} | {r[9]} | {r[10]} | {r[11]} | {r[12] or '—'} |")
