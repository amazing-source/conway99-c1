import numpy as np, pickle, subprocess, itertools, networkx as nx
from graphs_test import bvls243
A = bvls243(); n = 243
v = 0; a = int(np.nonzero(A[v])[0][0]); ap = [c for c in np.nonzero(A[v])[0] if A[a, c]][0]
ball = sorted(set([v, a, ap]) | set(np.nonzero(A[v])[0]) | set(np.nonzero(A[a])[0]) | set(np.nonzero(A[ap])[0]))
far = [u for u in range(n) if u not in ball]; F = len(far)
Af = A[np.ix_(far, far)]
cands = pickle.load(open("far_cands.pkl", "rb"))
alt = [[S for S in cands[wi] if S != frozenset(np.nonzero(Af[wi])[0].tolist())][0] for wi in range(F)]
B2 = A.copy()
for wi in range(F):
    for wj in range(F):
        B2[far[wi], far[wj]] = 1 if wj in alt[wi] else 0
np.save("twin243.npy", B2)
for name, M in (("BvLS", A), ("twin", B2)):
    ev = np.round(np.linalg.eigvalsh(M.astype(float)), 6)
    vals, cnt = np.unique(ev, return_counts=True)
    deg = set(M.sum(1)); sym = (M == M.T).all(); diag = M.diagonal().any()
    A2 = M @ M
    lam = set(A2[M == 1]); mu = set(A2[(M == 0) & ~np.eye(n, dtype=bool)])
    # induced 3x3 grids (Paley9): count via each vertex's two triangles and grid closure
    # grid = 9 vertices, 18 edges, each vertex degree 4 inside, two disjoint triangle partitions
    tri = set()
    for i in range(n):
        for j in np.nonzero(M[i])[0]:
            if j > i:
                for k in np.nonzero(M[i] & M[j])[0]:
                    if k > j: tri.add((i, j, k))
    print(name, "spectrum", dict(zip(vals.tolist(), cnt.tolist())), "degrees", deg, "symmetric", sym, "loops", diag,
          "lambda", lam, "mu", mu, "triangles", len(tri), flush=True)
    # dreadnaut group order
    lines = [f"n={n} g"]
    for i in range(n):
        lines.append(" ".join(str(j) for j in np.nonzero(M[i])[0] if j > i) + ";")
    cmd = "\n".join(lines) + "\nx\nq\n"
    out = subprocess.run(["/tmp/solvers/nauty_src/nauty2_8_8/dreadnaut"], input=cmd, capture_output=True, text=True).stdout
    grp = [l for l in out.split("\n") if "grpsize" in l]
    print(name, "automorphism group:", grp[0].strip() if grp else out[-300:], flush=True)
