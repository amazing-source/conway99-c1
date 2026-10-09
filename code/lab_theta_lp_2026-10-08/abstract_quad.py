"""C1, lab session, 2026-10-09, mandate B. Is  c(Q) = c_va + c_aw + c_wb + c_bv (mod 2)  a purely combinatorial identity?
Abstract model of the four walls of a quadrangle Q = (v, a, w, b): four 14-sets with their mate pairs and the four
cross matchings, with ONLY the constraints forced at the corners (pi_va(b) = w, pi_aw(v) = b, pi_wb(a) = v,
pi_bv(w) = a; the ears a', p, q, b' belong to two walls). Everything else random.
  python abstract_quad.py [trials]      One process, seconds."""
import random, sys, collections
random.seed(11); TR = int(sys.argv[1]) if len(sys.argv) > 1 else 20000


def trial():
    # wall of u: centre u, points: the two neighbours of u on Q with their mates (ears), and 10 others in 5 pairs
    walls = {}
    names = {"v": ("a", "a'", "b", "b'"), "a": ("v", "a'", "w", "p"), "w": ("a", "p", "b", "q"), "b": ("w", "q", "v", "b'")}
    for u, sp in names.items():
        pts = list(sp) + ["%s%d" % (u, i) for i in range(10)]
        mate = {sp[0]: sp[1], sp[1]: sp[0], sp[2]: sp[3], sp[3]: sp[2]}
        for i in range(0, 10, 2): mate["%s%d" % (u, i)] = "%s%d" % (u, i + 1); mate["%s%d" % (u, i + 1)] = "%s%d" % (u, i)
        walls[u] = (pts, mate)

    def matching(u, w_, forced):
        """random bijection N(u) minus line(u, w_) -> N(w_) minus line(u, w_), with forced values"""
        third = walls[u][1][w_]
        src = [x for x in walls[u][0] if x not in (w_, third)]; dst = [y for y in walls[w_][0] if y not in (u, third)]
        d = dict(forced); rs = [x for x in src if x not in d]; rd = [y for y in dst if y not in d.values()]
        random.shuffle(rd); d.update(zip(rs, rd)); return d
    P = {("v", "a"): matching("v", "a", {"b": "w"}), ("a", "w"): matching("a", "w", {"v": "b"}),
         ("w", "b"): matching("w", "b", {"a": "v"}), ("b", "v"): matching("b", "v", {"w": "a"})}

    def two_layer(u, w_):
        d = P[(u, w_)]; inv = {y: x for x, y in d.items()}; mu, mw = walls[u][1], walls[w_][1]; seen = set(); c = 0
        for x in d:
            if x in seen: continue
            c += 1; z = x
            while z not in seen:
                seen.add(z); z1 = mu[z]; seen.add(z1); y = d[z1]; y1 = mw[y]; z = inv[y1]
        return c
    cs = [two_layer(*e) for e in P]
    # holonomy on N[v] with PHI' (identity on the line of each edge)
    def phi(u, w_, x):
        third = walls[u][1][w_]
        return x if x in (u, w_, third) else P[(u, w_)][x]
    dom = [x for x in walls["v"][0] if x not in ("a", "b")]; hol = {}
    for x in dom:
        y = x
        for e in (("v", "a"), ("a", "w"), ("w", "b"), ("b", "v")): y = phi(e[0], e[1], y)
        hol[x] = y
    if set(hol.values()) != set(dom): return None
    seen = set(); cq = 0
    for x in dom:
        if x in seen: continue
        cq += 1; z = x
        while z not in seen: seen.add(z); z = hol[z]
    return (cq + sum(cs)) % 2


res = collections.Counter(trial() for _ in range(TR))
print("abstract four-wall model, %d trials: c(Q) + sum of the four c_e mod 2 ->" % TR, dict(res))
