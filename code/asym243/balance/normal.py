"""Conjecture: alpha = Pi_R N_+ Pi_R is normal on R, spectrum on the boundary of the triangle
T = conv{-2/3, (2/3)e^{+-i pi/3}} (edges: Re(w^k z) = 1/3, k = 0,1,2)."""
import sys, pickle, numpy as np
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))))
from lib243 import load_edges
def from_graph(path, pidx):
    G = np.load(path) if path.endswith(".npy") else load_edges(path)
    part = pickle.load(open(path + ".gridparts.pkl", "rb"))[pidx]; n = len(part)
    B = []
    for c in part:
        w, V = np.linalg.eigh(G[np.ix_(c, c)].astype(float))
        B.append(np.hstack([V[:, np.abs(w - 1) < 1e-8], V[:, np.abs(w + 2) < 1e-8]]))
    U = np.zeros((8 * n, 8 * n))
    for i in range(n):
        U[8*i:8*i+8, 8*i:8*i+8] = np.diag([1.] * 4 + [-1.] * 4) / 3
        for j in range(n):
            if i != j and G[np.ix_(part[i], part[j])].sum():
                U[8*i:8*i+8, 8*j:8*j+8] = (2 / 9) * B[i].T @ G[np.ix_(part[i], part[j])].astype(float) @ B[j]
    return U
def analyse(U, name):
    n = U.shape[0] // 8; blk = lambda i: slice(8 * i, 8 * i + 8)
    adj = np.array([[i != j and np.abs(U[blk(i), blk(j)]).max() > 1e-9 for j in range(n)] for i in range(n)])
    part = [-1] * n; p = 0
    for i in range(n):
        if part[i] < 0:
            for j in range(n):
                if not adj[i, j]: part[j] = p
            p += 1
    K = np.kron(np.eye(n), np.diag([1.] * 4 + [-1.] * 4)); N = U - K / 3
    Npl = N.copy()
    for i in range(n):
        for j in range(n):
            if adj[i, j] and (part[j] - part[i]) % 3 != 1: Npl[blk(i), blk(j)] = 0
    out = []
    for lab, idx in (("R", np.concatenate([np.arange(8*i, 8*i+4) for i in range(n)])), ("S", np.concatenate([np.arange(8*i+4, 8*i+8) for i in range(n)]))):
        a = Npl[np.ix_(idx, idx)]
        z = np.linalg.eigvals(a)
        w = np.exp(2j * np.pi / 3)
        target = 1 / 3 if lab == "R" else -1 / 3
        # distance to the three lines Re(w^k z) = target, then min over k
        dist = np.min(np.abs(np.array([np.real(w ** k * z) - target for k in range(3)])), axis=0)
        out.append(f"{lab}: |[a,a^T]| = {np.linalg.norm(a @ a.T - a.T @ a):.2e}, max dist of eigenvalues to lines Re(w^k z) = {target:+.3f}: {dist.max():.2e}, |z| in [{np.abs(z).min():.4f}, {np.abs(z).max():.4f}]")
    print(name); [print("   ", o) for o in out]
if __name__ == "__main__":
  for a in sys.argv[1:]:
    if a.endswith(".npy") and "Ucurve" in a: analyse(np.load(a), a)
    else:
        path, pidx = a.split(":"); analyse(from_graph(path, int(pidx)), a)
