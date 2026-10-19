"""Line-local (near-far) system of a line in a srg(v,k,1,2) (LAB 19/10/2026).

For a line T = {p, q, s}, n = k - 2: the classes C_0 = N(p)-T, C_1 = N(q)-T, C_2 = N(s)-T (n vertices each, relabelled so
that the partner of i is i^1: the pair {2j, 2j+1} is a line through the T-point), the cubic graph G_T (partner edges and
three bijections s01, s12, s20 between the classes), the far set F (vertices with no neighbour in T).  Every far vertex
has exactly two neighbours, non-partners, in each class (mu = 2 with each point of T), so F is in bijection with the
n(n-2)/2 non-partner pairs of C_0 ("p-names"), and E (near-far incidence) is two more bijections: far vertex -> q-pair,
far vertex -> s-pair.  Necessary conditions on E given G_T (proofs in NOTE_REDUCTION_2026-10-19.md, section 3):
  (L1) E E^T = K := (k-2) I - G - G^2 + 2J - J_cl          (pair multiplicities; the same-class blocks are automatic)
  (L2) for x in N(T), w in F:  |N_G(x) cap names(w)| <= 2 - [x in names(w)]       (mu / lambda between x and w)
  (L3) a transversal 3-set (one vertex per class) lies in the names of at most one far vertex     (mu between far ones)
  (L4) Conway only (k = 14): every far vertex has exactly |K|/6 names in each component K of G_T     (equitable lemma)
Modes (one process, CP-SAT with ONE worker: the lab PC is in low-performance mode):
  check <edges> [line#]                      extract (G_T, E) from a real graph, verify L1-L3 exactly (no solver)
  solve-real <edges> <line#> <sec> [L..]     rebuild E from scratch for the real G_T (positive control: FEASIBLE expected)
  random <seed> <sec> [L1|L12|L123|L1234]    random G_T with c = 1 for Conway (n = 12), solve
  randomc <seed> <c> <sec> [L..]             random G_T with exactly c components (Conway), solve
  blocks <seed> <k1,k2,..> <sec> [L..]       random G_T with components of 6*k_i vertices (Conway), solve
  planted <seed> <sec> [n]                   random 3D matching (n = 12 default), its own margins, solve L1 (capability)
  option --workers=W (default 1)
Output: one JSON line per run (status, wall, model size, independent re-check of any solution found)."""
import json
import random
import sys
import time
from itertools import combinations

import numpy as np
from ortools.sat.python import cp_model


# ----------------------------------------------------------------------------------------------- structure helpers
def pairs_of(n):
    return [(i, j) for i, j in combinations(range(n), 2) if i // 2 != j // 2]


def gt_matrix(n, s01, s12, s20):
    """adjacency of G_T on 3n vertices (class c, index i) -> c*n + i"""
    G = np.zeros((3 * n, 3 * n), dtype=np.int64)
    for c in range(3):
        for i in range(n):
            G[c * n + i, c * n + (i ^ 1)] = 1
    for i in range(n):
        for (ca, cb, s) in ((0, 1, s01), (1, 2, s12), (2, 0, s20)):
            a, b = ca * n + i, cb * n + s[i]
            G[a, b] = G[b, a] = 1
    return G


def k_matrix(n, G):
    N = 3 * n
    Jcl = np.zeros((N, N), dtype=np.int64)
    for c in range(3):
        Jcl[c * n:(c + 1) * n, c * n:(c + 1) * n] = 1
    return n * np.eye(N, dtype=np.int64) - G - G @ G + 2 * np.ones((N, N), dtype=np.int64) - Jcl


def components(G):
    N = G.shape[0]
    comp = [-1] * N
    c = 0
    for x in range(N):
        if comp[x] >= 0:
            continue
        stack = [x]
        comp[x] = c
        while stack:
            y = stack.pop()
            for z in np.nonzero(G[y])[0]:
                if comp[z] < 0:
                    comp[z] = c
                    stack.append(int(z))
        c += 1
    return c, comp


def inv(s):
    r = [0] * len(s)
    for i, j in enumerate(s):
        r[j] = i
    return r


# ----------------------------------------------------------------------------------------------- exact verifier
def verify(n, s01, s12, s20, names, conway):
    """names[f] = (p-pair, q-pair, s-pair); returns dict of violations of L1..L4 (independent of the model)."""
    G = gt_matrix(n, s01, s12, s20)
    K = k_matrix(n, G)
    m = len(names)
    E = np.zeros((3 * n, m), dtype=np.int64)
    for f, (pp, qq, ss) in enumerate(names):
        for c, pr in enumerate((pp, qq, ss)):
            assert pr[0] // 2 != pr[1] // 2
            for i in pr:
                E[c * n + i, f] = 1
    out = {}
    out["L1_bad_entries"] = int((E @ E.T != K).sum())
    GE = G @ E
    out["L2_bad"] = int((GE > 2 - E).sum())
    trip = {}
    bad3 = 0
    for f, (pp, qq, ss) in enumerate(names):
        for u in pp:
            for v in qq:
                for w in ss:
                    trip[(u, v, w)] = trip.get((u, v, w), 0) + 1
    bad3 = sum(1 for t in trip.values() if t > 1)
    out["L3_bad"] = bad3
    # bijectivity of the three name maps
    out["bijective"] = all(len({names[f][c] for f in range(m)}) == m for c in range(3))
    if conway:
        nc, comp = components(G)
        badeq = 0
        sizes = {}
        for x in range(3 * n):
            sizes[comp[x]] = sizes.get(comp[x], 0) + 1
        for f in range(m):
            cnt = {}
            for x in np.nonzero(E[:, f])[0]:
                cnt[comp[x]] = cnt.get(comp[x], 0) + 1
            for cc, sz in sizes.items():
                if cnt.get(cc, 0) * 6 != sz:
                    badeq += 1
        out["L4_bad"] = badeq
    return out


# ----------------------------------------------------------------------------------------------- real graph extraction
def extract(edges_path, line_no):
    edges = [tuple(map(int, l.split())) for l in open(edges_path) if l.strip()]
    v = 1 + max(max(e) for e in edges)
    adj = [set() for _ in range(v)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    k = len(adj[0])
    lines = sorted({tuple(sorted((a, b, c))) for a in range(v) for b in adj[a] for c in adj[a] & adj[b]})
    T = lines[line_no]
    Ts = set(T)
    n = k - 2
    cls = []
    for t in T:
        raw = [u for u in sorted(adj[t]) if u not in Ts]
        order, seen = [], set()
        for u in raw:                                   # partners adjacent: put them in consecutive positions
            if u in seen:
                continue
            mate = [w for w in raw if w in adj[u]]
            assert len(mate) == 1
            order += [u, mate[0]]
            seen |= {u, mate[0]}
        cls.append(order)
    pos = [{u: i for i, u in enumerate(c)} for c in cls]

    def bij(a, b):
        return [pos[b][[w for w in adj[cls[a][i]] if w in pos[b]][0]] for i in range(n)]
    s01, s12, s20 = bij(0, 1), bij(1, 2), bij(2, 0)
    near = set(cls[0]) | set(cls[1]) | set(cls[2])
    far = [w for w in range(v) if w not in Ts and w not in near]
    names = []
    for w in far:
        nm = []
        for c in range(3):
            pr = tuple(sorted(pos[c][u] for u in adj[w] if u in pos[c]))
            assert len(pr) == 2
            nm.append(pr)
        names.append(tuple(nm))
    names.sort()
    return k, n, T, s01, s12, s20, names


# ----------------------------------------------------------------------------------------------- the model
def build_model(n, s01, s12, s20, use, conway, margins=None):
    """use: set of 'L1','L2','L3','L4'.  margins: optional dict of explicit K blocks (planted mode)."""
    G = gt_matrix(n, s01, s12, s20) if s01 is not None else None
    if margins is None:
        K = k_matrix(n, G)
        K01, K02, K12 = K[0:n, n:2 * n], K[0:n, 2 * n:3 * n], K[n:2 * n, 2 * n:3 * n]
    else:
        K01, K02, K12 = margins
    P = pairs_of(n)
    m = len(P)
    md = cp_model.CpModel()
    X = [[md.NewBoolVar("") for _ in range(m)] for _ in range(m)]
    Y = [[md.NewBoolVar("") for _ in range(m)] for _ in range(m)]
    for f in range(m):
        md.AddExactlyOne(X[f])
        md.AddExactlyOne(Y[f])
    for e in range(m):
        md.AddExactlyOne([X[f][e] for f in range(m)])
        md.AddExactlyOne([Y[f][e] for f in range(m)])
    inc = [[e for e, pr in enumerate(P) if v in pr] for v in range(n)]
    a = [[md.NewBoolVar("") for _ in range(n)] for _ in range(m)]
    b = [[md.NewBoolVar("") for _ in range(n)] for _ in range(m)]
    for f in range(m):
        for v in range(n):
            md.Add(a[f][v] == sum(X[f][e] for e in inc[v]))
            md.Add(b[f][v] == sum(Y[f][e] for e in inc[v]))
    pin = [[f for f, pr in enumerate(P) if u in pr] for u in range(n)]     # far vertices whose p-name contains u
    z = [[[None] * n for _ in range(n)] for _ in range(m)]
    for f in range(m):
        for v in range(n):
            for w in range(n):
                t = md.NewBoolVar("")
                md.AddImplication(t, a[f][v])
                md.AddImplication(t, b[f][w])
                md.AddBoolOr([a[f][v].Not(), b[f][w].Not(), t])
                z[f][v][w] = t
    if "L1" in use:
        for u in range(n):
            for v in range(n):
                md.Add(sum(a[f][v] for f in pin[u]) == int(K01[u][v]))
                md.Add(sum(b[f][v] for f in pin[u]) == int(K02[u][v]))
        for v in range(n):
            for w in range(n):
                md.Add(sum(z[f][v][w] for f in range(m)) == int(K12[v][w]))
    if "L2" in use:
        i01, i12, i20 = inv(s01), inv(s12), inv(s20)
        for f, (x, y) in enumerate(P):
            pset = {x, y}
            for u in range(n):                                   # x = (0,u)
                fixed = int((u ^ 1) in pset)
                md.Add(fixed + a[f][s01[u]] + b[f][i20[u]] <= 2 - int(u in pset))
            for v in range(n):                                   # x = (1,v)
                md.Add(a[f][v ^ 1] + int(i01[v] in pset) + b[f][s12[v]] + a[f][v] <= 2)
            for w in range(n):                                   # x = (2,w)
                md.Add(b[f][w ^ 1] + a[f][i12[w]] + int(s20[w] in pset) + b[f][w] <= 2)
    if "L3" in use:
        for u in range(n):
            for v in range(n):
                for w in range(n):
                    md.Add(sum(z[f][v][w] for f in pin[u]) <= 1)
    if "L4" in use and conway:
        nc, comp = components(G)
        if nc > 1:
            sizes = {}
            for x in range(3 * n):
                sizes[comp[x]] = sizes.get(comp[x], 0) + 1
            for f, (x0, y0) in enumerate(P):
                for cc, sz in sizes.items():
                    fixed = int(comp[x0] == cc) + int(comp[y0] == cc)
                    md.Add(fixed + sum(a[f][v] for v in range(n) if comp[n + v] == cc)
                           + sum(b[f][w] for w in range(n) if comp[2 * n + w] == cc) == sz // 6)
    return md, P, X, Y


WORKERS = 1


def solve(md, P, X, Y, sec, n):
    sv = cp_model.CpSolver()
    sv.parameters.num_workers = WORKERS
    sv.parameters.max_time_in_seconds = sec
    t0 = time.time()
    st = sv.Solve(md)
    wall = round(time.time() - t0, 1)
    names = None
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        m = len(P)
        names = []
        for f in range(m):
            e1 = [e for e in range(m) if sv.Value(X[f][e])][0]
            e2 = [e for e in range(m) if sv.Value(Y[f][e])][0]
            names.append((P[f], P[e1], P[e2]))
    return sv.StatusName(st), wall, names, sv.ResponseStats().splitlines()[:0]


def random_gt(n, rng, want_c):
    tries = 0
    while True:
        tries += 1
        s01, s12, s20 = (rng.sample(range(n), n) for _ in range(3))
        G = gt_matrix(n, s01, s12, s20)
        K = k_matrix(n, G)
        if (K < 0).any():
            continue
        nc, _ = components(G)
        if nc == want_c:
            return s01, s12, s20, tries


def block_gt(n, rng, sizes):
    """random G_T whose components have 6k vertices for k in sizes (sum 6 = n/2): lines 0..5 of each class are cut
    into consecutive blocks; inside a block, random bijections until the block is connected; K >= 0 checked globally."""
    assert sum(sizes) == n // 2
    tries = 0
    while True:
        tries += 1
        s01, s12, s20 = [0] * n, [0] * n, [0] * n
        start = 0
        okb = True
        for k in sizes:
            idx = list(range(2 * start, 2 * (start + k)))
            for s in (s01, s12, s20):
                img = idx[:]
                rng.shuffle(img)
                for i, j in zip(idx, img):
                    s[i] = j
            start += k
        G = gt_matrix(n, s01, s12, s20)
        K = k_matrix(n, G)
        if (K < 0).any():
            continue
        nc, _ = components(G)
        if nc == len(sizes):
            return s01, s12, s20, tries


def uses(tag):
    return {"L1": {"L1"}, "L12": {"L1", "L2"}, "L123": {"L1", "L2", "L3"}, "L1234": {"L1", "L2", "L3", "L4"}}[tag]


def main():
    global WORKERS
    args = [a for a in sys.argv[1:] if not a.startswith("--workers=")]
    for a in sys.argv[1:]:
        if a.startswith("--workers="):
            WORKERS = int(a.split("=")[1])
    sys.argv = [sys.argv[0]] + args
    mode = sys.argv[1]
    rec = {"mode": mode, "argv": sys.argv[2:], "workers": WORKERS}
    if mode == "check":
        k, n, T, s01, s12, s20, names = extract(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 0)
        G = gt_matrix(n, s01, s12, s20)
        rec.update(k=k, n=n, line=T, c=components(G)[0], far=len(names),
                   violations=verify(n, s01, s12, s20, names, conway=(k == 14)))
    elif mode == "solve-real":
        k, n, T, s01, s12, s20, names = extract(sys.argv[2], int(sys.argv[3]))
        sec = float(sys.argv[4])
        use = uses(sys.argv[5]) if len(sys.argv) > 5 else {"L1", "L2", "L3"}
        md, P, X, Y = build_model(n, s01, s12, s20, use, conway=(k == 14))
        st, wall, sol, _ = solve(md, P, X, Y, sec, n)
        rec.update(k=k, n=n, line=T, c=components(gt_matrix(n, s01, s12, s20))[0], use=sorted(use), status=st, wall=wall,
                   recheck=verify(n, s01, s12, s20, sol, conway=(k == 14)) if sol else None,
                   real_recheck=verify(n, s01, s12, s20, names, conway=(k == 14)))
    elif mode in ("random", "randomc"):
        seed = int(sys.argv[2])
        if mode == "random":
            want_c, sec, tag = 1, float(sys.argv[3]), (sys.argv[4] if len(sys.argv) > 4 else "L123")
        else:
            want_c, sec, tag = int(sys.argv[3]), float(sys.argv[4]), (sys.argv[5] if len(sys.argv) > 5 else "L1234")
        rng = random.Random(seed)
        n = 12
        s01, s12, s20, tries = random_gt(n, rng, want_c)
        use = uses(tag)
        md, P, X, Y = build_model(n, s01, s12, s20, use, conway=True)
        st, wall, sol, _ = solve(md, P, X, Y, sec, n)
        G = gt_matrix(n, s01, s12, s20)
        t = int(np.trace(G @ G @ G)) // 6
        rec.update(n=n, c=components(G)[0], transversal_triangles=t, gen_tries=tries, use=sorted(use), status=st,
                   wall=wall, recheck=verify(n, s01, s12, s20, sol, conway=True) if sol else None,
                   gt=[s01, s12, s20])
    elif mode == "blocks":
        seed, sizes, sec = int(sys.argv[2]), [int(x) for x in sys.argv[3].split(",")], float(sys.argv[4])
        tag = sys.argv[5] if len(sys.argv) > 5 else "L1234"
        rng = random.Random(seed)
        n = 12
        s01, s12, s20, tries = block_gt(n, rng, sizes)
        use = uses(tag)
        md, P, X, Y = build_model(n, s01, s12, s20, use, conway=True)
        st, wall, sol, _ = solve(md, P, X, Y, sec, n)
        G = gt_matrix(n, s01, s12, s20)
        rec.update(n=n, sizes=sizes, c=components(G)[0], transversal_triangles=int(np.trace(G @ G @ G)) // 6,
                   gen_tries=tries, use=sorted(use), status=st, wall=wall,
                   recheck=verify(n, s01, s12, s20, sol, conway=True) if sol else None, gt=[s01, s12, s20])
    elif mode == "planted":
        seed, sec = int(sys.argv[2]), float(sys.argv[3])
        n = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        rng = random.Random(seed)
        P = pairs_of(n)
        m = len(P)
        q = rng.sample(range(m), m)
        s = rng.sample(range(m), m)
        names = [(P[f], P[q[f]], P[s[f]]) for f in range(m)]
        E = np.zeros((3 * n, m), dtype=np.int64)
        for f, nm in enumerate(names):
            for c, pr in enumerate(nm):
                for i in pr:
                    E[c * n + i, f] = 1
        K = E @ E.T
        margins = (K[0:n, n:2 * n], K[0:n, 2 * n:3 * n], K[n:2 * n, 2 * n:3 * n])
        md, P2, X, Y = build_model(n, None, None, None, {"L1"}, conway=False, margins=margins)
        st, wall, sol, _ = solve(md, P2, X, Y, sec, n)
        ok = None
        if sol:
            E2 = np.zeros_like(E)
            for f, nm in enumerate(sol):
                for c, pr in enumerate(nm):
                    for i in pr:
                        E2[c * n + i, f] = 1
            ok = bool(((E2 @ E2.T) == K).all())
        rec.update(n=n, status=st, wall=wall, recheck_margins_equal=ok)
    print(json.dumps(rec), flush=True)


if __name__ == "__main__":
    main()
