import sys, numpy as np
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))))
from lib243 import load_edges
path, cpath, out = sys.argv[1], sys.argv[2], sys.argv[3]
G = np.load(path) if path.endswith(".npy") else load_edges(path)
C = [int(x) for x in np.load(cpath)]; Cs = set(C); F = [w for w in range(len(G)) if w not in Cs]
ci = {s: i for i, s in enumerate(C)}
k = int(G[0].sum()); t = int(G[F[0]][C].sum())
with open(out, "w") as f:
    f.write(f"{len(F)} {len(C)} {k - t}\n")
    for w in F:
        bl = [ci[s] for s in C if G[w, s]]; f.write(f"{len(bl)} " + " ".join(map(str, bl)) + "\n")
np.save(out + ".F.npy", np.array(F))
# truth rows (indices into F) for checking
Fi = {u: i for i, u in enumerate(F)}
with open(out + ".truth", "w") as f:
    for w in F: f.write(" ".join(str(Fi[u]) for u in F if G[w, u]) + "\n")
