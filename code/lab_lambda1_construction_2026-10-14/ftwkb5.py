"""The generalized quadrangle FTWKB(5) of order (25,5) by the Knarr model, and its hemisystems of lines (14/10/2026).

Source of the construction: Bamberg, Giudici, Royle, "Hemisystems of small flock generalized quadrangles" (arXiv
1012.3819), section 2.2 (Knarr model, Table 2) and Lemma 5.1 / Table 4 (BLT-set of FTWKB(q): f_t = (3/2) t^2,
g_t = 3 t^3, q = 2 mod 3). Their Theorem 1.1 classifies the hemisystems of FTWKB(5): three complementary pairs with
stabilisers of orders 600, 120 and 6 (S3). A hemisystem H (each point on exactly (s+1)/2 = 3 of its 6 lines) gives
a partial quadrangle PQ(2,25,8): vertices = lines of H, adjacent = concurrent, a srg(378,52,1,8) (Cameron, Delsarte,
Goethals).
This script: builds points and lines over GF(5) exactly, checks the GQ axioms (order, two lines meet in at most one
point), writes the hemisystem CNF (exactly 3 of the 6 lines at each point) for cadical, and decodes a solution into
the srg with a check of its parameters.
usage: python ftwkb5.py build <out dir>                             -> gq.json (incidence), hemi.cnf
       python ftwkb5.py decode <out dir> <cadical output> <name>    -> <name>.edges (the srg), <name>.hemi.json
"""
import itertools
import json
import os
import sys

q = 5
INV = {1: 1, 2: 3, 3: 2, 4: 4}
E6 = [tuple(int(i == j) for i in range(6)) for j in range(6)]


def rref(rows):
    """reduced row echelon form over GF(q); a tuple of tuples, canonical key of the row space"""
    M = [list(r) for r in rows]
    piv = 0
    for c in range(len(M[0])):
        p = next((i for i in range(piv, len(M)) if M[i][c] % q), None)
        if p is None:
            continue
        M[piv], M[p] = M[p], M[piv]
        iv = INV[M[piv][c] % q]
        M[piv] = [(x * iv) % q for x in M[piv]]
        for i in range(len(M)):
            if i != piv and M[i][c] % q:
                fac = M[i][c]
                M[i] = [(a - fac * b) % q for a, b in zip(M[i], M[piv])]
        piv += 1
    return tuple(tuple(r) for r in M[:piv])


def beta(x, y):
    """alternating form x1y6 - x6y1 + x2y5 - x5y2 + x3y4 - x4y3"""
    return (x[0] * y[5] - x[5] * y[0] + x[1] * y[4] - x[4] * y[1] + x[2] * y[3] - x[3] * y[2]) % q


def span_points(basis):
    """all projective points (normalised vectors) of the subspace spanned by basis"""
    pts = set()
    for coeffs in itertools.product(range(q), repeat=len(basis)):
        if not any(coeffs):
            continue
        v = [sum(c * b[i] for c, b in zip(coeffs, basis)) % q for i in range(6)]
        pts.add(rref([v])[0])
    return pts


def build(outdir):
    os.makedirs(outdir, exist_ok=True)
    P = (1, 0, 0, 0, 0, 0)
    f = {t: (4 * t * t) % q for t in range(q)}          # (3/2) t^2 with 3/2 = 4 in GF(5)
    g = {t: (3 * t ** 3) % q for t in range(q)}

    def lift(x):
        return (0, x[0], x[1], x[2], x[3], 0)
    blt = [((0, 0, 1, 0), (0, 0, 0, 1))] + [((1, 0, f[t], t), (0, 1, g[t], f[t])) for t in range(q)]
    O = [rref([P, lift(a), lift(b)]) for a, b in blt]
    for pi in O:
        assert all(beta(u, v) == 0 for u in pi for v in pi), "plane not totally isotropic"
    allpts = span_points(E6)
    assert len(allpts) == (q ** 6 - 1) // (q - 1)
    pts_i = sorted(p for p in allpts if p[5] != 0)
    assert len(pts_i) == q ** 5
    pts_ii = []
    for pi in O:
        P_pi = span_points(list(pi))
        found = set()
        for a, b in itertools.combinations(sorted(P_pi), 2):
            m = rref([a, b])
            if P not in span_points(list(m)):
                found.add(m)
        pts_ii += sorted(found)
    assert len(pts_ii) == (q + 1) * q * q, len(pts_ii)
    points = [("i", p) for p in pts_i] + [("ii", m) for m in pts_ii] + [("iii", P)]
    pindex = {p: i for i, p in enumerate(points)}
    lines = []
    for m in pts_ii:
        Pm = span_points(list(m))
        perp = [v for v in allpts if all(beta(v, u) == 0 for u in m)]
        planes = set()
        for v in perp:
            if v in Pm:
                continue
            s = rref(list(m) + [v])
            if any(x[5] != 0 for x in span_points(list(s))):
                planes.add(s)
        assert len(planes) == q, len(planes)
        for s in sorted(planes):
            on = [pindex[("i", p)] for p in span_points(list(s)) if p[5] != 0] + [pindex[("ii", m)]]
            lines.append(sorted(on))
    for pi in O:
        P_pi = span_points(list(pi))
        on = [pindex[("ii", m)] for m in pts_ii if span_points(list(m)) <= P_pi]
        on.append(pindex[("iii", P)])
        lines.append(sorted(on))
    npts, nlines = len(points), len(lines)
    assert npts == (q * q + 1) * (q ** 3 + 1) and nlines == (q + 1) * (q ** 3 + 1), (npts, nlines)
    assert all(len(l) == q * q + 1 for l in lines)
    meet = {}
    for li, l in enumerate(lines):
        for p in l:
            meet.setdefault(p, []).append(li)
    assert {len(v) for v in meet.values()} == {q + 1}
    seen = set()
    for p, ls in meet.items():
        for a, b in itertools.combinations(ls, 2):
            assert (a, b) not in seen, "two lines share two points"
            seen.add((a, b))
    # GQ axiom: a point off a line is collinear with exactly one point of it (check on a sample of 300 pairs)
    collin = {}
    for l in lines:
        for a in l:
            collin.setdefault(a, set()).update(l)
    import random
    rng = random.Random(1)
    for _ in range(300):
        li = rng.randrange(nlines)
        p = rng.randrange(npts)
        if p in lines[li]:
            continue
        assert sum(1 for x in lines[li] if x in collin[p]) == 1, "GQ axiom fails"
    print("FTWKB(5): %d points, %d lines, %d points per line, %d lines per point; lines meet in <= 1 point; GQ axiom "
          "checked on a sample" % (npts, nlines, q * q + 1, q + 1), flush=True)
    json.dump({"lines": lines, "npoints": npts}, open(os.path.join(outdir, "gq.json"), "w"))
    cls = []
    for p, ls in meet.items():
        for sub in itertools.combinations(ls, 4):
            cls.append([-(x + 1) for x in sub])
            cls.append([x + 1 for x in sub])
    with open(os.path.join(outdir, "hemi.cnf"), "w") as fh:
        fh.write("p cnf %d %d\n" % (nlines, len(cls)))
        for c in cls:
            fh.write(" ".join(map(str, c)) + " 0\n")
    print("hemisystem CNF: %d variables, %d clauses" % (nlines, len(cls)), flush=True)


def decode(outdir, solfile, name):
    G = json.load(open(os.path.join(outdir, "gq.json")))
    lines = G["lines"]
    val = {}
    for line in open(solfile):
        if line.startswith("v"):
            for x in line.split()[1:]:
                x = int(x)
                if x:
                    val[abs(x)] = x > 0
    H = [i for i in range(len(lines)) if val.get(i + 1)]
    deg = {}
    for i in H:
        for p in lines[i]:
            deg[p] = deg.get(p, 0) + 1
    assert len(H) == len(lines) // 2 and set(deg.values()) == {3} and len(deg) == G["npoints"]
    idx = {li: k for k, li in enumerate(H)}
    on = {}
    for i in H:
        for p in lines[i]:
            on.setdefault(p, []).append(idx[i])
    edges = set()
    for p, ls in on.items():
        for a, b in itertools.combinations(sorted(ls), 2):
            edges.add((a, b))
    n = len(H)
    nb = [set() for _ in range(n)]
    for a, b in edges:
        nb[a].add(b)
        nb[b].add(a)
    ks = {len(x) for x in nb}
    lam, mu = set(), set()
    for a in range(n):
        for b in range(a + 1, n):
            c = len(nb[a] & nb[b])
            (lam if b in nb[a] else mu).add(c)
    print("hemisystem of %d lines; graph on %d vertices: degrees %s, lambda %s, mu %s" % (len(H), n, ks, lam, mu),
          flush=True)
    with open(os.path.join(outdir, name + ".edges"), "w") as fh:
        for a, b in sorted(edges):
            fh.write("%d %d\n" % (a, b))
    json.dump(H, open(os.path.join(outdir, name + ".hemi.json"), "w"))


if __name__ == "__main__":
    if sys.argv[1] == "build":
        build(sys.argv[2])
    else:
        decode(sys.argv[2], sys.argv[3], sys.argv[4])
