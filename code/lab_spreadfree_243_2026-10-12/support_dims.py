"""Lab session, 2026-10-12. SCREENING of regions by linear algebra: for a set F of vertices, the dimensions of the
spaces of eigenvectors of A (eigenvalues 4 and -5) supported in F. A trade inside F needs both to be non-zero
(support criterion, NOTE_SPREADFREE.md section 3); the completions are the integral points of a Grassmannian of
subspaces of dimension w4 in a space of dimension w4 + w5.
python -I support_dims.py <edge file> <region> [<region> ...]     region: a-b[,c-d...] (inclusive ranges of vertices)"""
import sys
import numpy as np
def load(path):
    E = [tuple(map(int, l.split())) for l in open(path) if l.strip()]
    A = np.zeros((243, 243))
    for a, b in E: A[a, b] = A[b, a] = 1
    return A
def dims(A, F):
    R = [v for v in range(243) if v not in set(F)]; w, U = np.linalg.eigh(A); out = []
    for ev in (4, -5):
        Bm = U[:, np.abs(w - ev) < 1e-6]; s = np.linalg.svd(Bm[R, :], compute_uv=False); out.append(Bm.shape[1] - int((s > 1e-8).sum()))
    return out
if __name__ == "__main__":
    A = load(sys.argv[1])
    for spec in sys.argv[2:]:
        F = [v for part in spec.split(",") for v in range(int(part.split("-")[0]), int(part.split("-")[1]) + 1)]
        w4, w5 = dims(A, F); print("%s, region %s (%d vertices): eigenvectors supported inside: eigenvalue 4: %d, eigenvalue -5: %d" % (sys.argv[1].split("/")[-1], spec, len(F), w4, w5))
