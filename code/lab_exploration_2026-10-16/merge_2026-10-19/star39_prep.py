"""Input of star39.cpp: the complete star of a near vertex x, at rank 37 (rho = 0) or 39 (rho = 2) (LAB 20/10/2026).

For a generic line T (G connected, 7 not dividing tau) and x in C0 not in a transversal triangle of G, the star of x
is the set of the 10 far vertices adjacent to x: W_y = {x, y} u q_y u s_y, y in C0 - {x, xbar}.  A candidate is
(triple, u), u in F_7^rho:
  - L2, K(x, n) >= 1 for its names n in C1 u C2, real unary 0 <= H(W, W) <= 7 with H = 3I - R - E^T Z E + J/9 = 7 Pi_T
    (Z = (3I - G + J)^-1 over the reals; valid at every rank);
  - diagonal of the rank condition: u^T D u = g(W, W) mod 7, g = e^T Omega e, Omega = (3I - G + J)^-1 mod 7
    (rho = 0: g(W, W) = 0).
Pairs (checked in star39.cpp): R = 4 - g(W, W') + u^T D u' mod 7 must be 0 or 1.
The residual form at rank 39 is fixed by Codex/LAB (NOTE_RESEAUX_DE_DROITE §2, 09/10): anisotropic plane (delta = 1)
if (tau|7) = +1, hyperbolic (delta = 3) if (tau|7) = -1.  Both can be run; the script prints the allowed one.
usage: python star39_prep.py <seed> <x> <rho 0|2> <delta 1|3> <out.bin> [--tau any|-1|+1]"""
import itertools
import json
import os
import struct
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from star_csp import line_graph, n, N  # noqa: E402
from oblr_prep import orbit_reps  # noqa: E402
from ll_test import pairs_of  # noqa: E402

P = 7


def main():
    seed, x, rho, delta, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    need = 0
    if "--tau" in sys.argv:
        t = sys.argv[sys.argv.index("--tau") + 1]
        need = 0 if t == "any" else int(t)
    gt, G, Om, K, leg = line_graph(seed, need)
    nb = [set(int(z) for z in np.nonzero(G[v])[0]) for v in range(N)]
    xb = x ^ 1
    b1 = [z for z in nb[x] if n <= z < 2 * n][0]
    b2 = [z for z in nb[x] if z >= 2 * n][0]
    if b2 in nb[b1]:
        raise SystemExit("x lies in a transversal triangle of G: choose another x")
    Lr = 3 * np.eye(N) - G + 1.0
    Z = np.linalg.inv(Lr)
    D = [1, delta] if rho == 2 else []
    if rho == 2:
        rep, gorder = orbit_reps(2, D)
        level = {t: [] for t in range(P)}
        for u in itertools.product(range(P), repeat=2):
            level[(u[0] * u[0] + delta * u[1] * u[1]) % P].append(u)
    else:
        rep, gorder = {(): ()}, 1
    ys = [y for y in range(n) if y not in (x, xb)]
    P1 = [(n + a, n + b) for a, b in pairs_of(n)]
    P2 = [(2 * n + a, 2 * n + b) for a, b in pairs_of(n)]
    stats = []
    with open(out, "wb") as f:
        f.write(struct.pack("<6i", rho, delta, x, b1, b2, len(ys)))
        f.write(struct.pack("<%di" % (N * 3), *[z for v in range(N) for z in sorted(nb[v])]))
        f.write(struct.pack("<%di" % N, *[int(K[x, v]) for v in range(N)]))
        f.write(struct.pack("<2i", *(D if rho == 2 else [0, 0])))
        for y in ys:
            tris, cands = [], []
            for qi, q in enumerate(P1):
                if K[x, q[0]] == 0 or K[x, q[1]] == 0:
                    continue
                for si, s in enumerate(P2):
                    if K[x, s[0]] == 0 or K[x, s[1]] == 0:
                        continue
                    W = (x, y) + q + s
                    Ws = set(W)
                    if any(len(nb[v] & Ws) > 1 for v in W):
                        continue
                    cnt = {}
                    for v in W:
                        for z in nb[v]:
                            if z not in Ws:
                                cnt[z] = cnt.get(z, 0) + 1
                    if any(c > 2 for c in cnt.values()):
                        continue
                    e = np.zeros(N)
                    e[list(W)] = 1
                    zq = Z @ e
                    dd = 3.0 + 1.0 / 9.0 - float(e @ zq)
                    if dd < -1e-9 or dd > 7 + 1e-9:
                        continue
                    ei = np.zeros(N, dtype=np.int64)
                    ei[list(W)] = 1
                    Y = (Om @ ei) % P
                    g = int(ei @ Y) % P
                    if rho == 0:
                        us = [()] if g == 0 else []
                    else:
                        us = level[g]
                    if not us:
                        continue
                    ti = len(tris)
                    cap = 1 - len(nb[x] & Ws)
                    nbc = [len(nb[z] & Ws) for z in range(N)]
                    tris.append((W, qi, si, cap, int(b1 in Ws), int(b2 in Ws), Y, zq, dd, nbc))
                    for u in us:
                        canon = 1 if (rho == 0 or tuple(u) == tuple(rep[tuple(u)])) else 0
                        cands.append((ti, canon, u))
            f.write(struct.pack("<3i", y, len(tris), len(cands)))
            for (W, qi, si, cap, h1, h2, Y, zq, dd, nbc) in tris:
                f.write(struct.pack("<6i", *W))
                f.write(struct.pack("<5i", qi, si, cap, h1, h2))
                f.write(struct.pack("<%dB" % N, *[int(v) for v in Y]))
                f.write(struct.pack("<%dB" % N, *nbc))
                f.write(struct.pack("<%dd" % N, *[float(v) for v in zq]))
                f.write(struct.pack("<d", dd))
            for (ti, canon, u) in cands:
                uu = list(u) + [0] * (2 - len(u))
                f.write(struct.pack("<4i", ti, canon, uu[0], uu[1]))
            stats.append((len(tris), len(cands)))
    allowed = None
    if rho == 2:
        allowed = 1 if leg == 1 else 3
    print(json.dumps({"seed": seed, "x": x, "b1": b1, "b2": b2, "rho": rho, "delta": delta, "tau_leg": leg,
                      "delta_allowed_by_rule": allowed, "O(D)": gorder, "triples": [s[0] for s in stats],
                      "candidates": [s[1] for s in stats]}))


if __name__ == "__main__":
    main()
