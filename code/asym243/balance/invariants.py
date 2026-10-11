import sys, pickle, numpy as np, itertools
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))))
from lib243 import load_edges
path, pidx = sys.argv[1], int(sys.argv[2]); files = sys.argv[3:]
G = np.load(path) if path.endswith(".npy") else load_edges(path); part = pickle.load(open(path + ".gridparts.pkl", "rb"))[pidx]; n = len(part)
Q = [[i != j and bool(G[np.ix_(part[i], part[j])].sum()) for j in range(n)] for i in range(n)]
B = []
for c in part:
    w, V = np.linalg.eigh(G[np.ix_(c, c)].astype(float))
    B.append(np.hstack([V[:, np.abs(w - 1) < 1e-8], V[:, np.abs(w + 2) < 1e-8]]))
blk = lambda i: slice(8 * i, 8 * i + 8)
U0 = np.zeros((8 * n, 8 * n))
for i in range(n):
    U0[blk(i), blk(i)] = np.diag([1.] * 4 + [-1.] * 4) / 3
    for j in range(n):
        if Q[i][j]: U0[blk(i), blk(j)] = (2 / 9) * B[i].T @ G[np.ix_(part[i], part[j])].astype(float) @ B[j]
tris = [t for t in itertools.combinations(range(n), 3) if Q[t[0]][t[1]] and Q[t[1]][t[2]] and Q[t[0]][t[2]]][:400]
quads = [(a, b, c, d) for (a, b, c, d) in itertools.product(range(9), range(9, 18), range(9), range(18, 27)) if a < c][:400]
PR = np.diag([1.] * 4 + [0.] * 4)
def inv(U):
    h = lambda cyc, P: np.trace(P @ np.linalg.multi_dot([U[blk(cyc[k]), blk(cyc[(k + 1) % len(cyc)])] for k in range(len(cyc))]))
    t3 = np.array([h(t, PR) for t in tris] + [h(t, np.eye(8)) for t in tris])
    t4 = np.array([h(q, PR) for q in quads])
    ev = np.linalg.eigvalsh(U[np.ix_(np.concatenate([np.arange(8*i, 8*i+4) for i in range(n)]), np.concatenate([np.arange(8*i, 8*i+4) for i in range(n)]))])
    return t3, t4, ev
a3, a4, ae = inv(U0)
for f in files:
    U = np.load(f); b3, b4, be = inv(U)
    print(f, " max change: triangle holonomy traces %.3e, 4-cycle traces %.3e, spectrum of Pi_R U Pi_R %.3e" % (np.abs(a3 - b3).max(), np.abs(a4 - b4).max(), np.abs(ae - be).max()))
