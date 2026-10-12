"""Lab session, 2026-10-12. The S3 question, LOCAL problem at one vertex (own derivation of 12/10, afternoon).

BH: V = F_3^4, x ~ y iff q(y - x) = 0, q = x0^2 + x1^2 + x2 x3. A parity skeleton is eps on the edges, even on the
lines, with the six path parities of every non-adjacent pair of weight 0, 3 or 6.
Gauge at the vertex P = 0: all 20 edges at P are positive, so the ten lines through P are positive; every far vertex R
(60 of them) is switched so that its first edge to N(P) is positive. Then:
  * pair (P, R): the labelling l_R of the six common neighbours C(P,R) by eps(Z R) has weight 0 or 3
    ("R flat" or "R split"; weight 6 is switched to 0);
  * a non-adjacent pair {Z, Z'} inside N(P) has the common neighbour P (even path) and exactly five others, all far:
    the R with Z, Z' in C(P,R). Its path parities are l_R(Z) + l_R(Z'), so the number of R separating Z from Z' is 0 or 3.
These conditions involve only the 360 edges between N(P) and the far vertices: a design problem on the 20 points of
N(P) with 60 blocks of size 6. If its only solution were "every R flat", every pair at every vertex would be flat and
every parity skeleton would be trivial (all squares even).

This script writes that local problem as a CNF, with the extra clause "some R is split" (mode nontrivial) or with a
given far vertex forced to be split (mode first), and can check a model.
python local_vertex.py <nontrivial | first | free> <out.cnf>"""
import sys, itertools

V = list(itertools.product(range(3), repeat=4)); I = {v: i for i, v in enumerate(V)}; n = 81
q = lambda x: (x[0] * x[0] + x[1] * x[1] + x[2] * x[3]) % 3
add = lambda a, b: tuple((x + y) % 3 for x, y in zip(a, b))
S = [v for v in V if any(v) and q(v) == 0]
nbs = [set(I[add(V[i], s)] for s in S) for i in range(n)]
P = 0; NP = sorted(nbs[P]); far = [r for r in range(n) if r != P and r not in nbs[P]]
C = {r: sorted(nbs[P] & nbs[r]) for r in far}
assert len(NP) == 20 and len(far) == 60 and all(len(C[r]) == 6 for r in far)
var = {}; nv = 0
for r in far:
    for z in C[r][1:]:
        nv += 1; var[(z, r)] = nv                    # l_R(Z); the first one is 0 (gauge at R)
lit = lambda z, r: var.get((z, r))                   # None = constant 0


def build(mode):
    global nv
    cl = []
    def new():
        global nv; nv += 1; return nv
    for r in far:                                    # weight 0 or 3 (the first label is 0)
        vs = [var[(z, r)] for z in C[r][1:]]
        for bits in itertools.product((0, 1), repeat=5):
            if sum(bits) not in (0, 3): cl.append([vs[i] * (-1 if bits[i] else 1) for i in range(5)])
    npairs = 0
    for a, b in itertools.combinations(NP, 2):
        if b in nbs[a]: continue
        R5 = [r for r in far if a in C[r] and b in C[r]]; assert len(R5) == 5
        npairs += 1; ws = []
        for r in R5:
            x, y = lit(a, r), lit(b, r)
            if x is None and y is None: ws.append(None)
            elif x is None: ws.append(y)
            elif y is None: ws.append(x)
            else:
                t = new(); ws.append(t)
                cl += [[-t, x, y], [-t, -x, -y], [t, -x, y], [t, x, -y]]
        vs = [w for w in ws if w is not None]
        for bits in itertools.product((0, 1), repeat=len(vs)):
            if sum(bits) not in (0, 3): cl.append([vs[i] * (-1 if bits[i] else 1) for i in range(len(vs))])
    assert npairs == 180
    if mode == "nontrivial": cl.append([var[(z, r)] for r in far for z in C[r][1:]])
    if mode == "first": cl.append([var[(z, far[0])] for z in C[far[0]][1:]])
    return cl


if __name__ == "__main__":
    mode = sys.argv[1]; cl = build(mode)
    with open(sys.argv[2], "w", newline="\n") as f:
        f.write("p cnf %d %d\n" % (nv, len(cl)))
        for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
    print("local problem at P = 0, mode %s: %d variables (300 labels), %d clauses" % (mode, nv, len(cl)))
