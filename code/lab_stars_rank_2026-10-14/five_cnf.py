"""CNF of the k-star admissibility problem with an exact product encoding (LAB 16/10/2026).
Same constraints as stars_rank.build (C1 exact for the stars, C1' bounds for the other letters, C2 caps by a sequential
counter on the products), for a root with K letters.  Difference: with --reify each product variable p_ijt is tied to
both factors (p -> e_it, p -> e_jt), so that p = e_it AND e_jt exactly; in stars_rank.build p is only bounded below and a
decision on p is meaningless.  Optional --m4 "a-b,c-d,...": fix the matching M_4 of L_4 (pairs of outer letters a, b of
the labels {4,a}, {4,b}) as unit clauses, as in five_split_par.py.  Optional --cadical EXE --seconds T: run cadical.
usage: python five_cnf.py <K> <stars> <out cnf> [--reify] [--m4 ...] [--cadical exe --seconds T]"""
import itertools
import subprocess
import sys
import time


def opt(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


K = int(sys.argv[1])
stars = [int(t) for t in sys.argv[2].split(",")]
out = sys.argv[3]
reify = "--reify" in sys.argv
MATE = lambda i: i ^ 1
LABELS = [frozenset((u, w)) for u, w in itertools.combinations(range(K), 2) if w != MATE(u)]


def count_needed(l, y):
    return 1 if (y in l or MATE(y) in l) else 2


S = [l for l in LABELS if any(y in l for y in stars)]
if opt("--xk"):
    # partial fifth star: the given stars exact, plus the first xk labels {4,6}, {4,7}, ... (letter 4 only bounded)
    S = S + [frozenset((4, t)) for t in range(6, K) if frozenset((4, t)) not in S][:int(opt("--xk"))]
idx = {l: i for i, l in enumerate(S)}
n = len(S)
nv = [0]
clauses = []


def var():
    nv[0] += 1
    return nv[0]


e = {}
for i, j in itertools.combinations(range(n), 2):
    e[(i, j)] = e[(j, i)] = var()
for l in S:
    i = idx[l]
    for y in range(K):
        lits = [e[(i, idx[t])] for t in S if y in t and t != l]
        if not lits:
            continue
        c = count_needed(l, y)
        for sub in itertools.combinations(lits, c + 1):                    # at most c
            clauses.append([-x for x in sub])
        if y in stars:                                                     # at least c
            if c == 1:
                clauses.append(list(lits))
            else:
                for x in lits:
                    clauses.append([z for z in lits if z != x])
for i, j in itertools.combinations(range(n), 2):
    s = len(S[i] & S[j])
    prods = []
    for t in range(n):
        if t in (i, j):
            continue
        p = var()
        clauses.append([-e[(i, t)], -e[(j, t)], p])
        if reify:
            clauses.append([-p, e[(i, t)]])
            clauses.append([-p, e[(j, t)]])
        prods.append(p)
    prev = {}
    for p in prods:
        cur = {}
        for mm in (1, 2, 3):
            r = var()
            if mm == 1:
                clauses.append([-p, r])
            elif mm - 1 in prev:
                clauses.append([-p, -prev[mm - 1], r])
            if mm in prev:
                clauses.append([-prev[mm], r])
            cur[mm] = r
        prev = cur
    eij = e[(i, j)]
    if s == 1:
        clauses.append([-eij, -prev[1]])
        clauses.append([eij, -prev[2]])
    else:
        clauses.append([-eij, -prev[2]])
        clauses.append([eij, -prev[3]])
m0 = opt("--m0")
m0pairs = None
if m0:
    # fix the matching M_0 of L_0: pairs "a-b" mean {0,a} ~ {0,b}; every other pair inside L_0 is a non-edge
    m0pairs = set(frozenset(int(t) for t in pq.split("-")) for pq in m0.split(","))
    L0 = [l for l in S if 0 in l]
    for x, y in itertools.combinations(L0, 2):
        a, b = list(x - {0})[0], list(y - {0})[0]
        v = e[(idx[x], idx[y])]
        clauses.append([v] if frozenset((a, b)) in m0pairs else [-v])
m4 = opt("--m4")
if m4:
    pairs = set(frozenset(int(t) for t in pq.split("-")) for pq in m4.split(","))
    L4 = [l for l in S if 4 in l]
    for x, y in itertools.combinations(L4, 2):
        a, b = list(x - {4})[0], list(y - {4})[0]
        v = e[(idx[x], idx[y])]
        clauses.append([v] if frozenset((a, b)) in pairs else [-v])
if opt("--base"):
    # fix the adjacency among the labels of a given structure; --base-stars restricts it to the labels meeting those
    # stars (e.g. 0,1,2,3: keep the four-star block of an R7 solution, release its labels {4,t})
    import json as _json
    bd = _json.load(open(opt("--base")))
    bl = [frozenset(x) for x in bd["labels"]]
    keep = [int(t) for t in opt("--base-stars", "").split(",") if t]
    bE = set(tuple(sorted(x)) for x in bd["edges"])
    nfix = 0
    for a, b in itertools.combinations(range(len(bl)), 2):
        if keep and not (any(y in bl[a] for y in keep) and any(y in bl[b] for y in keep)):
            continue
        if bl[a] in idx and bl[b] in idx:
            v = e[(idx[bl[a]], idx[bl[b]])]
            clauses.append([v] if (a, b) in bE else [-v])
            nfix += 1
    print("base %s: %d fixed pairs" % (opt("--base"), nfix), flush=True)
if opt("--symbreak"):
    # lex-leader symmetry breaking (K = 14, label set invariant under the letter group G of order 3072: D4 on the lines
    # {0,1}, {2,3}, letters 4 and 5 fixed, hyperoctahedral group on the outer lines {6,7}, ..., {12,13}).  Every
    # constraint (C1, C1', C2) is defined combinatorially and is G-invariant, so g maps solutions (edge assignments) to
    # solutions; the lexicographically least image x* satisfies x* <= x* o g for every g, hence adding x <= x o g for
    # any set of g loses no solution orbit.  Encoding as in five_symbreak.py.
    import random as _random
    assert K == 14
    star_maps = []
    for sl in (False, True):
        for s0 in (False, True):
            for s1 in (False, True):
                g = {0: 0, 1: 1, 2: 2, 3: 3}
                if s0:
                    g[0], g[1] = 1, 0
                if s1:
                    g[2], g[3] = 3, 2
                if sl:
                    g = {k2: {0: 2, 1: 3, 2: 0, 3: 1}[v2] for k2, v2 in g.items()}
                star_maps.append(g)
    outer = [(6, 7), (8, 9), (10, 11), (12, 13)]
    outer_maps = []
    for perm in itertools.permutations(range(4)):
        for flips in itertools.product((0, 1), repeat=4):
            g = {}
            for q, (a, b) in enumerate(outer):
                c, d = outer[perm[q]]
                if flips[q]:
                    c, d = d, c
                g[a], g[b] = c, d
            outer_maps.append(g)
    group = []
    for s_ in star_maps:
        for o_ in outer_maps:
            g = dict(s_)
            g.update(o_)
            g[4], g[5] = 4, 5
            if any(g[y] != y for y in range(14)):
                if m0pairs is not None:
                    # with M_0 fixed, only the elements that fix letter 0 and map M_0 onto itself are symmetries
                    if g[0] != 0 or set(frozenset((g[a], g[b])) for a, b in (tuple(q) for q in m0pairs)) != m0pairs:
                        continue
                group.append(g)
    nsb = int(opt("--symbreak"))
    if nsb < len(group):
        group = _random.Random(int(opt("--sbseed", "1"))).sample(group, nsb)
    pairs_all = list(itertools.combinations(range(n), 2))
    nlex = 0
    for g in group:
        prev = None
        for (i, j) in pairs_all:
            gi = idx[frozenset(g[y] for y in S[i])]
            gj = idx[frozenset(g[y] for y in S[j])]
            x_, y_ = e[(i, j)], e[(gi, gj)]
            if x_ == y_:
                continue
            a_ = var()
            if prev is None:
                clauses.extend([[-x_, y_], [x_, y_, a_], [-x_, -y_, a_]])
            else:
                clauses.extend([[-prev, -x_, y_], [-prev, x_, y_, a_], [-prev, -x_, -y_, a_]])
            prev = a_
            nlex += 3
    print("symmetry breaking: %d group elements, %d lex clauses" % (len(group), nlex), flush=True)
with open(out, "w") as fh:
    fh.write("p cnf %d %d\n" % (nv[0], len(clauses)))
    for c in clauses:
        fh.write(" ".join(map(str, c)) + " 0\n")
print("K=%d stars=%s labels=%d reify=%s m4=%s: %d vars, %d clauses" % (K, stars, n, reify, m4, nv[0], len(clauses)),
      flush=True)
cad = opt("--cadical")
if cad:
    T = float(opt("--seconds", "300"))
    t0 = time.time()
    model_path = out + ".model"
    with open(model_path, "w") as mf:
        p = subprocess.Popen([cad, "-q", out], stdout=mf, stderr=subprocess.DEVNULL)
        try:
            p.wait(timeout=T)
            st = {10: "SAT", 20: "UNSAT"}.get(p.returncode, "UNKNOWN(%d)" % p.returncode)
        except subprocess.TimeoutExpired:
            p.kill()
            p.wait()
            st = "TIMEOUT"
    print("cadical: %s in %.1f s" % (st, time.time() - t0), flush=True)
    if st == "SAT":
        import json
        vals = set()
        for line in open(model_path):
            if line.startswith("v "):
                vals.update(int(t) for t in line.split()[1:] if t != "0")
        edges = [[i, j] for i, j in itertools.combinations(range(n), 2) if e[(i, j)] in vals]
        json.dump({"K": K, "stars": stars, "xk": opt("--xk"), "labels": [sorted(l) for l in S], "edges": edges},
                  open(out + ".json", "w"))
        print("structure saved: %s.json (%d edges)" % (out, len(edges)), flush=True)
