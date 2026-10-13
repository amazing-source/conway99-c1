"""Lab session, 2026-10-13. Check, on the pentagonal prism (the standard example of a non-zero mixed defect with both
diagonal blocks exact; k = 3, mu = 1), of the matrix form of Codex's column identity (his note, section 59):
    T = A^2 + A - (k-mu) I - mu J = [[0, G], [G^t, 0]],  M = D^t G.
    (i)   M is symmetric;                 (ii)  G^t G = M + E M + M E;
    (iii) G^t G commutes with E;          (iv)  M^2 = G^t G ((k-mu) I - E^2 - E);
    (v)   the diagonal of (ii) is the column identity ||G_u||^2 = D_u^t (2B + I) G_u;
    (vi)  on a common eigenvector of E (value t) and G^t G (value s^2 > 0): (k-mu) - t^2 - t > 0 and
          s <= |2t+1| sqrt((k-mu) - t^2 - t).
Exact integers except (vi) (floating point, printed).   python check_defect_matrix_identity.py     Memory: negligible."""
import numpy as np
C5 = np.zeros((5, 5), dtype=np.int64)
for i in range(5): C5[i, (i + 1) % 5] = C5[(i + 1) % 5, i] = 1
I5 = np.eye(5, dtype=np.int64); B, D, E = C5, I5, C5; k, mu = 3, 1
A = np.block([[B, D], [D.T, E]]); n = 10
T = A @ A + A - (k - mu) * np.eye(n, dtype=np.int64) - mu
assert not T[:5, :5].any() and not T[5:, 5:].any()
G = T[:5, 5:]; M = D.T @ G; GG = G.T @ G
print("defect G non-zero:", bool(G.any()), " squared norm", int((G * G).sum()))
print("(i)   M symmetric:", bool((M == M.T).all()))
print("(ii)  G^tG = M + EM + ME:", bool((GG == M + E @ M + M @ E).all()))
print("(iii) G^tG E = E G^tG:", bool((GG @ E == E @ GG).all()))
print("(iv)  M^2 = G^tG((k-mu) - E^2 - E):", bool((M @ M == GG @ ((k - mu) * I5 - E @ E - E)).all()))
print("(v)   column identity:", all(int(G[:, u] @ G[:, u]) == int(D[:, u] @ (2 * B + I5) @ G[:, u]) for u in range(5)))
w, V = np.linalg.eigh(E.astype(float))
for t in sorted(set(np.round(w, 9))):
    X = V[:, np.abs(w - t) < 1e-7]; s2 = np.linalg.eigvalsh(X.T @ GG @ X)
    pt = (k - mu) - t * t - t
    print("(vi)  E-eigenvalue %+.4f: singular values of G there %s ; (k-mu)-t^2-t = %+.4f ; bound %s" % (t, np.round(np.sqrt(np.abs(s2)), 4), pt, ("%.4f" % (abs(2 * t + 1) * np.sqrt(pt))) if pt > 0 else "G must vanish"))
