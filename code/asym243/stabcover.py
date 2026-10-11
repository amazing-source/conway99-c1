"""Symmetry-steered re-voltaging: srg(243,22,1,2) that are 3-covers of BH along the h_0 spread of BvLS and are
invariant under K = Stab_{Aut BvLS}(h_0-spread, S) for a chosen substructure S (a set of fibres of BH).
Uses the affine line model (fixed h_0 lines, candidates of directions h_m + e h_0) with orbit-equalities.
Usage: python3 stabcover.py NAME 'fibre list' [limit]"""
import sys, time, pickle, numpy as np, subprocess, re
from ortools.sat.python import cp_model
from linesat import build
from lines_model import *
from lib243 import *
from cover import fibres_of, is_cover

A = load_edges("bvls243.edges")
fib = [list(f) for f in lines_of_direction(HS[0])]           # 81 spread lines
okc, Qadj = is_cover(A, fib)


def stabiliser_gens(S):
    """generators of Aut(BvLS) preserving the spread and the fibre set S (setwise), via a gadget graph."""
    n0 = 243; N = n0 + 81
    M = np.zeros((N, N), dtype=np.int64); M[:n0, :n0] = A
    for i, f in enumerate(fib):
        for p in f: M[p, n0 + i] = M[n0 + i, p] = 1
    Spts = sorted(p for i in S for p in fib[i])
    cells = [Spts, [p for p in range(n0) if p not in set(Spts)], [n0 + i for i in S],
             [n0 + i for i in range(81) if i not in set(S)]]
    cells = [c for c in cells if c]
    o, orb, gens = aut(M, partition=cells)
    return o, [g[:n0] for g in gens]


def run(name, S, limit=3, workers=4, tlimit=600):
    o, gens = stabiliser_gens(S)
    print(f"[{name}] |S| = {len(S)} fibres, |K| = {o}", flush=True)
    hd = HS[0]
    fixed = lines_of_direction(hd)
    cands = []
    for mm in range(1, 11):
        for e in (0, 1, 2):
            cands += lines_of_direction(add(HS[mm], hd, e))
    m, x, cl = build(fixed, cands)
    cs = set(cl)
    # orbit equalities
    for g in gens:
        for c in cl:
            im = tuple(sorted(g[p] for p in c))
            if im in cs and im != c: m.Add(x[c] == x[im])
            elif im not in cs: m.Add(x[c] == 0)
    known = {canon_g6(A): "BvLS", canon_g6(load_edges("twin243_switched.edges")): "twin",
             canon_g6(np.load("aff0_1.npy")): "Gamma3"}
    try: known.update(pickle.load(open("stab_classes.pkl", "rb")))
    except Exception: pass
    res = []
    for k in range(limit):
        s = cp_model.CpSolver(); s.parameters.num_workers = workers; s.parameters.max_time_in_seconds = tlimit
        t0 = time.time(); r = s.Solve(m)
        if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print(f"[{name}] {s.StatusName(r)} after {k} solutions ({time.time()-t0:.0f}s)", flush=True); break
        sel = [c for c in cl if s.Value(x[c])]
        G = graph_from_lines(list(fixed) + sel)
        cg = canon_g6(G)
        if cg not in known:
            ao = aut(G)[0]; known[cg] = f"S{len(known)}_{ao}"
            np.save(f"stab_{known[cg]}.npy", G); pickle.dump({k_: v for k_, v in known.items()
                                                              if k_ not in ()}, open("stab_classes.pkl", "wb"))
            tag = "NEW"
        else: tag = "seen"
        _, ng = grids_per_vertex(G)
        print(f"[{name}] sol {k+1}: srg={is_srg(G)} class={known[cg]} {tag} grids={ng} [{time.time()-t0:.0f}s]", flush=True)
        res.append(known[cg])
        m.AddBoolOr([x[c].Not() for c in sel])
    return res


if __name__ == "__main__":
    name = sys.argv[1]; S = [int(t) for t in sys.argv[2].split(",")] if sys.argv[2] else []
    run(name, S, int(sys.argv[3]) if len(sys.argv) > 3 else 3)
