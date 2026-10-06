import numpy as np, pickle, subprocess, networkx as nx
from graphs_test import bvls243, is_srg
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
assert is_srg(B2, 243, 22, 1, 2)
g1 = nx.to_graph6_bytes(nx.from_numpy_array(A), header=False); g2 = nx.to_graph6_bytes(nx.from_numpy_array(B2), header=False)
open("pair.g6", "wb").write(g1 + g2)
out = subprocess.run(["/tmp/solvers/nauty_src/nauty2_8_8/labelg", "-q", "pair.g6"], capture_output=True).stdout.split()
print("canonical forms equal (isomorphic):", out[0] == out[1])
# how the twin relates: is the far-block change a Seidel/Godsil-McKay-type switching?
D = (B2 - A)[np.ix_(far, far)]
print("changed far edges:", int((D == 1).sum() // 2), "added,", int((D == -1).sum() // 2), "removed")
