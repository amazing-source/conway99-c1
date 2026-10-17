"""Re-gluing grids: a graph with an equitable partition into 3x3 grids is a 'grid cover' of its quotient; the 9x9
matchings between adjacent grids are the voltages.  Keep everything fixed except the matchings of a chosen set of grid
pairs, and solve the srg(v,k,1,2) conditions exactly (CP-SAT).  Any other solution is a re-glued srg with the same grid
partition.  Library + CLI:
  python3 regluing.py GRAPH PARTITION_INDEX 'free grid indices' [limit]
(the free set = all matchings between the listed grids and every other grid)"""
import sys, itertools, time, pickle, numpy as np
from ortools.sat.python import cp_model
from lib243 import *


def block_model(G, part, free_pairs, k=22, lam=1, mu=2, forbid_original=True):
    n = len(G); m = cp_model.CpModel()
    var = {}
    for (i, j) in free_pairs:
        gi, gj = part[i], part[j]
        X = [[m.NewBoolVar("") for _ in gj] for _ in gi]
        for a in range(9): m.AddExactlyOne(X[a])
        for b in range(9): m.AddExactlyOne([X[a][b] for a in range(9)])
        for a, x in enumerate(gi):
            for b, y in enumerate(gj):
                var[(x, y)] = var[(y, x)] = X[a][b]
    def adj(x, y):
        return var.get((x, y), bool(G[x, y]))
    freev = set(p for pr in var for p in pr)
    nb_pot = [set(np.nonzero(G[x])[0].tolist()) for x in range(n)]
    for (x, y) in var: nb_pot[x].add(y)
    AND = {}
    def land(u, v):
        if u is True: return v
        if v is True: return u
        key = (min(u.Index(), v.Index()), max(u.Index(), v.Index()))
        if key not in AND:
            w = m.NewBoolVar(""); m.AddImplication(w, u); m.AddImplication(w, v); m.AddBoolOr([u.Not(), v.Not(), w])
            AND[key] = w
        return AND[key]
    ncons = 0
    for x in range(n):
        for y in range(x + 1, n):
            axy = adj(x, y)
            common = nb_pot[x] & nb_pot[y]
            involved = not isinstance(axy, bool) or any(not isinstance(adj(x, z), bool) or not isinstance(adj(z, y), bool) for z in common)
            if not involved: continue
            terms, const = [], 0
            for z in common:
                u, v = adj(x, z), adj(z, y)
                if u is False or v is False: continue
                if u is True and v is True: const += 1
                else: terms.append(land(u, v))
            if axy is True: m.Add(sum(terms) + const == lam)
            elif axy is False: m.Add(sum(terms) + const == mu)
            else:
                m.Add(sum(terms) + const == lam).OnlyEnforceIf(axy)
                m.Add(sum(terms) + const == mu).OnlyEnforceIf(axy.Not())
            ncons += 1
    if forbid_original:
        m.AddBoolOr([v.Not() for (x, y), v in var.items() if x < y and G[x, y]])
    m._and = AND
    return m, var, ncons


def solve(G, part, free_pairs, limit=5, workers=4, tlimit=600, known=None, tag="rg"):
    m, var, ncons = block_model(G, part, free_pairs)
    out = []
    for it in range(limit):
        s = cp_model.CpSolver(); s.parameters.num_workers = workers; s.parameters.max_time_in_seconds = tlimit
        t0 = time.time(); r = s.Solve(m)
        if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            out.append(("STATUS", s.StatusName(r), round(time.time() - t0))); break
        H = G.copy()
        for (x, y), v in var.items(): H[x, y] = int(s.Value(v))
        assert is_srg(H)
        c = canon_g6(H)
        name = None
        if known is not None:
            if c not in known:
                o = aut(H)[0]; known[c] = f"{tag}{len(known)}_{o}"; np.save(f"{known[c]}.npy", H)
            name = known[c]
        out.append(("SOL", name, round(time.time() - t0)))
        m.AddBoolOr([v.Not() for (x, y), v in var.items() if x < y and s.Value(v)])
    return out


if __name__ == "__main__":
    from gridcover_anatomy import grid_partitions
    path, pidx, fl = sys.argv[1], int(sys.argv[2]), [int(t) for t in sys.argv[3].split(",")]
    limit = int(sys.argv[4]) if len(sys.argv) > 4 else 5
    G = np.load(path) if path.endswith(".npy") else load_edges(path)
    import os
    parts = pickle.load(open(path + ".gridparts.pkl", "rb")) if os.path.exists(path + ".gridparts.pkl") else grid_partitions(G)
    part = parts[pidx]
    Qd = [[bool(G[np.ix_(part[i], part[j])].sum()) for j in range(len(part))] for i in range(len(part))]
    free = sorted({(min(i, j), max(i, j)) for i in fl for j in range(len(part)) if j != i and Qd[i][j]})
    # gauge fixing: relabelling the points of a free grid is an isomorphism; keep, for each free grid, its matching
    # to one non-free neighbour grid fixed (this kills the relabelling freedom)
    for i in fl:
        j0 = next(j for j in range(len(part)) if Qd[i][j] and j not in fl)
        free.remove((min(i, j0), max(i, j0)))
    print(f"{path} partition {pidx}: free grids {fl}, free matchings {len(free)}", flush=True)
    known = {canon_g6(G): "self"}
    for f in ["bvls243.edges", "twin243_switched.edges", "aff0_1.npy", "stab_S3_3888.npy"]:
        H = np.load(f) if f.endswith(".npy") else load_edges(f); known.setdefault(canon_g6(H), f.split(".")[0])
    for r in solve(G, part, free, limit, known=known): print("  ", r, flush=True)
