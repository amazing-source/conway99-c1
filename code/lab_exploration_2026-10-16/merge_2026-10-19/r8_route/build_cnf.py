"""Write a CNF of the R8 family with my independent encoder (LAB 20/10/2026).

usage: python build_cnf.py <out.cnf> [--K 14] [--nx N] [--implied L4B,XPAIR] [--five]
                           [--units structure.json] [--m0case k] [--lex all|none|N] [--lexlen T] [--sbseed s]
  --units F    fix every edge variable to the adjacency of the structure in F ({"labels", "edges"}), as unit clauses
               (planted-solution control: the CNF must then be SAT by unit propagation alone).
  --m0case k   fix the matching M_0 of L_0 to the representative of the k-th orbit (my own enumeration, m0_orbits()),
               and add lex-leader clauses for every non-trivial element of its stabiliser in G_0 (K = 14 only).
  --lex all    lex-leader clauses x <= x o g for every non-identity g of the letter group G (order 3072, K = 14);
  --lex N      for N random elements of G (seed --sbseed).  --lexlen T truncates every chain after T positions.
Soundness of the symmetry breaking: see NOTE_R8_ROUTE.md section 3."""
import itertools
import json
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r8lib  # noqa: E402


def opt(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def matchings(points):
    if not points:
        yield []
        return
    a = points[0]
    for i in range(1, len(points)):
        for m in matchings(points[1:i] + points[i + 1:]):
            yield [(a, points[i])] + m


def g0_group(K=14):
    """G_0 = stabiliser of the letter 0 in the R8 group (it also fixes 1, 4, 5)."""
    return [g for g in r8lib.r8_group(K) if g[0] == 0]


def m0_orbits(K=14):
    """Orbits of the perfect matchings of the 12 letters s (labels {0,s} of L_0) under G_0.  Returns a sorted list of
    (canonical representative, orbit size); the representative is the lexicographically least image."""
    G0 = g0_group(K)
    pts = [s for s in range(K) if s not in (0, 1)]
    seen = {}
    for m in matchings(pts):
        key = tuple(sorted(tuple(sorted(p)) for p in m))
        if key in seen:
            continue
        orbit = set()
        for g in G0:
            orbit.add(tuple(sorted(tuple(sorted((g[a], g[b]))) for a, b in key)))
        rep = min(orbit)
        for o in orbit:
            seen[o] = rep
    reps = {}
    for k, r in seen.items():
        reps[r] = reps.get(r, 0) + 1
    return sorted(reps.items())


def lex_clauses(F, sig, order, maxlen=None):
    """x <= x o sigma (lexicographic, positions in 'order'); x_v = variable v, (x o sigma)_v = variable sig[v]."""
    prev = None
    used = 0
    for v in order:
        w = sig[v]
        if w == v:
            continue
        if maxlen is not None and used >= maxlen:
            break
        used += 1
        a = F.new()
        pre = [] if prev is None else [-prev]
        F.add(pre + [-v, w])          # prefix equal  =>  x_v <= y_v
        F.add(pre + [v, w, a])        # prefix equal and x_v = y_v = 0  =>  still equal
        F.add(pre + [-v, -w, a])      # prefix equal and x_v = y_v = 1  =>  still equal
        prev = a
    return used


def main():
    out = sys.argv[1]
    K = int(opt("--K", "14"))
    nx = opt("--nx")
    M = r8lib.Model(K, nx=int(nx) if nx else None)
    implied = [t for t in opt("--implied", "").split(",") if t]
    five = "--five" in sys.argv
    t0 = time.time()
    F, info = r8lib.encode(M, implied=implied, five=five, stream=out)
    extra = {"K": K, "labels": M.n, "implied": implied, "five": five}
    if opt("--units"):
        d = json.load(open(opt("--units")))
        labs = [frozenset(x) for x in d["labels"]]
        E = set()
        for i, j in d["edges"]:
            if labs[i] in M.idx and labs[j] in M.idx:
                a, b = M.idx[labs[i]], M.idx[labs[j]]
                E.add((min(a, b), max(a, b)))
        for p in M.pairs:
            F.add([M.var(*p)] if p in E else [-M.var(*p)])
        extra["units"] = len(M.pairs)
    order = list(range(1, len(M.pairs) + 1))
    maxlen = int(opt("--lexlen")) if opt("--lexlen") else None
    if opt("--m0case") is not None:
        assert K == 14
        k = int(opt("--m0case"))
        reps = m0_orbits(K)
        rep, size = reps[k]
        pairs = set(frozenset(p) for p in rep)
        L0 = [i for i, l in enumerate(M.S) if 0 in l]
        for a, b in itertools.combinations(L0, 2):
            s, t = list(M.S[a] - {0})[0], list(M.S[b] - {0})[0]
            F.add([M.var(a, b)] if frozenset((s, t)) in pairs else [-M.var(a, b)])
        stab = [g for g in g0_group(K)
                if set(frozenset((g[a], g[b])) for a, b in rep) == pairs and any(g[y] != y for y in range(K))]
        nl = 0
        for g in stab:
            nl += lex_clauses(F, r8lib.var_perm(M, g), order, maxlen)
        extra.update({"m0case": k, "m0rep": rep, "orbit": size, "stabiliser_nontrivial": len(stab), "lexpos": nl})
    lex = opt("--lex", "none")
    if lex != "none":
        assert K == 14
        # never combine with --m0case: the canonical M_0 choice and the lex-leader of G are two different normal forms
        assert opt("--m0case") is None, "--lex and --m0case together would not be sound"
        G = [g for g in r8lib.r8_group(K) if any(g[y] != y for y in range(K))]
        if lex != "all":
            G = random.Random(int(opt("--sbseed", "1"))).sample(G, int(lex))
        nl = 0
        for g in G:
            nl += lex_clauses(F, r8lib.var_perm(M, g), order, maxlen)
        extra.update({"lex_elements": len(G), "lexpos": extra.get("lexpos", 0) + nl})
    F.close()
    extra.update({"vars": F.n, "clauses": F.len_clauses(), "seconds": round(time.time() - t0, 1)})
    print(json.dumps(extra), flush=True)


if __name__ == "__main__":
    main()
