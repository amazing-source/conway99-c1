"""Godsil-McKay switching graph of a Spence list (asymmetry campaign, 14/10/2026).

A GM switching set is D (|D| = 2m) inducing a regular graph such that every vertex outside D has 0, m or 2m neighbours
in D. Switching: every outside vertex with exactly m neighbours in D exchanges its neighbours and non-neighbours in D.
The result is cospectral with the input, hence a srg with the same parameters. For each graph of the list and each
switching set of size 4 (and 6 if asked) we identify the switched graph in the list (canonical forms).
usage: python gm_switch.py <spence file> [sizes, default 4]
"""
import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import srglib as L


def gm_sets(nb, size):
    n = len(nb)
    m = size // 2
    out = []
    for D in itertools.combinations(range(n), size):
        Ds = set(D)
        degs = {len(nb[v] & Ds) for v in D}
        if len(degs) != 1:
            continue
        ok = True
        for y in range(n):
            if y in Ds:
                continue
            c = len(nb[y] & Ds)
            if c not in (0, m, size):
                ok = False
                break
        if ok:
            out.append(D)
    return out


def switch(nb, D):
    n = len(nb)
    Ds = set(D)
    m = len(D) // 2
    new = [set(x) for x in nb]
    for y in range(n):
        if y in Ds or len(nb[y] & Ds) != m:
            continue
        for d in D:
            if d in nb[y]:
                new[y].discard(d)
                new[d].discard(y)
            else:
                new[y].add(d)
                new[d].add(y)
    return new


if __name__ == "__main__":
    header, gs = L.read_spence(sys.argv[1])
    sizes = [int(s) for s in sys.argv[2].split(",")] if len(sys.argv) > 2 else [4]
    canon = [L.canonical_form(g) for g in gs]
    index = {c: i + 1 for i, c in enumerate(canon)}
    orders = [L.group_order(g)[0] for g in gs]
    for size in sizes:
        print("switching sets of size", size, flush=True)
        for gi, nb in enumerate(gs):
            sets = gm_sets(nb, size)
            targets = {}
            for D in sets:
                h = switch(nb, D)
                assert L.srg_params(h) == L.srg_params(nb)
                t = index.get(L.canonical_form(h), "new")
                targets[t] = targets.get(t, 0) + 1
            print("  #%2d (|Aut| %d): %d switching sets -> %s" % (gi + 1, orders[gi], len(sets),
                  dict(sorted(targets.items(), key=lambda t: str(t[0])))), flush=True)
