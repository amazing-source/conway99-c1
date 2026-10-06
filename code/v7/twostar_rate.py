"""Kill rate of the class-minimum test on the universal 37-branch seed  {x, y} u N(x) u N(y)  (28 vertices).

Residual 37 (no integer 26, hence no affine 21), a = 2, no NZZ triangle.  Seed structure (all forced):
  x, y non adjacent (q = -1), common neighbours c, d (q = +1, non adjacent);
  N(x) = c, d, 8 Bx (q=1), 4 Zx (q=0); N(y) likewise; N(x) and N(y) are perfect matchings (7K2);
  no Zx-Zx and no Zy-Zy matching pair (no NZZ), the c,d mates are arbitrary (m counts Zx/Zy mates);
  every w in N(x)\\{c,d} has exactly two neighbours in N(y) (its common neighbours with y), c being one of them for
  the mate of c; symmetric for N(y).
Random sampling (not uniform) of such seeds satisfying lambda/mu inside the seed; then seedcvp test.
"""
import sys, random, time, itertools
import numpy as np
from seedcvp import class_min_violation


def sample(rng, max_tries=2000):
    # vertices: 0=x 1=y 2=c 3=d ; X: 4..15 (N(x)\C), Y: 16..27 (N(y)\C)
    X = list(range(4, 16)); Y = list(range(16, 28))
    qX = [1] * 8 + [0] * 4; rng.shuffle(qX)
    qY = [1] * 8 + [0] * 4; rng.shuffle(qY)
    q = [-1, -1, 1, 1] + qX + qY
    def matching(Vs, qs):
        # mates of c and d chosen first, then perfect matching of the remaining 10 with no zero-zero pair
        for _ in range(1000):
            vs = Vs[:]; rng.shuffle(vs)
            mc, md = vs[0], vs[1]; rest = vs[2:]
            pairs = [(rest[i], rest[i + 1]) for i in range(0, 10, 2)]
            if all(not (q[a] == 0 and q[b] == 0) for a, b in pairs):
                return mc, md, pairs
        return None
    mx = matching(X, qX); my = matching(Y, qY)
    if mx is None or my is None:
        return None
    A = np.zeros((28, 28), dtype=np.int64)
    def e(a, b):
        A[a, b] = A[b, a] = 1
    for v in [2, 3] + X:
        e(0, v)
    for v in [2, 3] + Y:
        e(1, v)
    e(2, mx[0]); e(3, mx[1]); e(2, my[0]); e(3, my[1])
    for a, b in mx[2] + my[2]:
        e(a, b)
    # bipartite X-Y: degree 2 except the c,d mates (degree 1)
    degX = {v: 2 for v in X}; degX[mx[0]] = 1; degX[mx[1]] = 1
    degY = {v: 2 for v in Y}; degY[my[0]] = 1; degY[my[1]] = 1
    for _ in range(max_tries):
        B = A.copy()
        stubsX = [v for v in X for _ in range(degX[v])]
        stubsY = [v for v in Y for _ in range(degY[v])]
        rng.shuffle(stubsY)
        ok = True
        for a, b in zip(stubsX, stubsY):
            if B[a, b]:
                ok = False; break
            B[a, b] = B[b, a] = 1
        if not ok:
            continue
        C = B @ B
        lim = np.where(B == 1, 1, 2); np.fill_diagonal(lim, 99)
        if (C <= lim).all():
            # exact lambda/mu where all common neighbours lie in the seed: x,y pairs
            if C[0, 1] != 2:
                continue
            return B, q
    return None


if __name__ == "__main__":
    n = int(sys.argv[1]); rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 0)
    st = {}; t = time.time(); got = 0; fails = 0
    while got < n:
        s = sample(rng)
        if s is None:
            fails += 1; continue
        B, q = s
        bad = class_min_violation(B, q)
        key = str(bad[0]) if bad else "alive"
        st[key] = st.get(key, 0) + 1; got += 1
    print(st, "sampling failures", fails, round(time.time() - t, 1))
