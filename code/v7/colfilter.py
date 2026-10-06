"""Residual column filter: an outside column (b, q_u) is impossible if the class of q contains, among
   z = q + eps*q_u + sum_{v in core} c_v q_v + j*1   (eps = +-1),
a level-0 vector of norm <= 26 or a level-+-1 vector of norm <= 21 (integer 26 / affine 21 are excluded in the
residual; norms < 14 at level 0 are impossible outright).

w = q + Q_c + j*1 is enumerated once (core-supported class elements, any level, norm <= NMAX);
for a column, ||w + eps q_u||^2 = N(w) + 23 + 2 eps <w, q_u>,
  <w, q_u> = (6 - 7 q_u) + sum_v c_v (2 - 7[v in b]) + 11 j,     level(w + eps q_u) = level(w) + eps.
"""
import json, sys, itertools, time
import numpy as np
from coset_cvp import gram_and_lin, enumerate_short
from bstage import gen_columns

P13 = list(range(14, 27))
NMAX = 77


def class_elements(core, holes, nmax=NMAX):
    A = np.array(core["adj"], dtype=np.int64)
    qcore = [-1, -1, 1, 1, 1, 1, 1, 1] + [0] * 6 + [0 if v in holes else 1 for v in P13]
    G, lin = gram_and_lin(A, qcore)
    keep = list(range(26)) + [27]
    G = G[np.ix_(keep, keep)]; lin = lin[keep]
    import subprocess, os
    inp = f"{len(keep)}\n" + " ".join(map(str, G.flatten())) + "\n" + " ".join(map(str, lin)) + f"\n37 {nmax}\n"
    out = subprocess.run([os.path.join(os.path.dirname(os.path.abspath(__file__)), "fp_enum")], input=inp.encode(),
                         capture_output=True, check=True)
    arr = np.frombuffer(out.stdout, dtype=np.int32).reshape(-1, len(keep) + 1).astype(np.int64)
    N = arr[:, 0]; X = arr[:, 1:]
    C = np.zeros((len(arr), 27), dtype=np.int64); C[:, :26] = X[:, :26]
    J = X[:, 26]
    L = 3 + X[:, :26].sum(1) + 9 * J
    return C, J, N, L


def filter_columns(core, holes, cols, nmax=NMAX, chunk=20000):
    """column (b,q_u) dead iff some class element w (core-supported) and eps=+-1 give
       level 0 & norm<=26  :  level(w) = -eps  and  eps*w(u) >= (N-7)/14
       level +-1 & norm<=21:  level(w)+eps = +-1 and 14*eps*w(u) >= N + 2 + 4*eps*level(w)
       where w(u) = q_u + sum_{v in b} c_v + j  (value of the affine function w at the outside vertex u)."""
    C, J, N, L = class_elements(core, holes, nmax)
    Bm = np.zeros((len(cols), 27), dtype=np.int16)
    qu = np.zeros(len(cols), dtype=np.int64)
    for i, (b, q) in enumerate(cols):
        Bm[i, list(b)] = 1; qu[i] = q
    dead = np.zeros(len(cols), dtype=bool)
    nused = 0
    for eps in (1, -1):
        for target in ("lev0", "lev1"):
            if target == "lev0":
                sel = (L == -eps)
                thr = np.ceil((N - 7) / 14.0)                       # eps*w(u) >= thr
            else:
                sel = (np.abs(L + eps) == 1)
                thr = np.ceil((N + 2 + 4 * eps * L) / 14.0)
            # eps*w(u) = eps*q_u + eps*j + eps*sum_b c ;  need eps*sum_b c >= thr - eps*j - eps*q_u
            need = thr - eps * J                                   # minus eps*q_u per column (q_u in {0,1})
            # prefilter: max of eps*sum_b c over |b|<=7 is the sum of the 7 largest eps*c_v (positive part)
            ec = np.sort(np.maximum(eps * C, 0), axis=1)[:, ::-1][:, :7].sum(1)
            sel = sel & (ec + 1 >= need)
            idx = np.nonzero(sel)[0]
            nused += len(idx)
            for s0 in range(0, len(idx), chunk):
                ii = idx[s0:s0 + chunk]
                Cc = (eps * C[ii]).astype(np.int16)
                val = Bm @ Cc.T                                    # cols x chunk
                val = val.astype(np.int32) + (eps * qu)[:, None]
                dead |= (val >= need[ii][None, :]).any(1)
    return dead, nused


if __name__ == "__main__":
    cores = json.load(open("cores27.json"))
    k = int(sys.argv[1]); holes = [int(v) for v in sys.argv[2].split(",")]
    core = cores[k]
    cols = gen_columns(np.array(core["adj"]), set(tuple(p) for p in core["defect"]))
    t = time.time()
    dead, nw = filter_columns(core, holes, cols)
    print("core", k, "holes", holes, "class elements <=", NMAX, ":", nw, "columns", len(cols), "killed", int(dead.sum()),
          "time", round(time.time() - t, 1))
