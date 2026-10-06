"""Lemma: for srg(n,k,1,2) with N(v) = (k/2)K2 and k/2 >= 3 matched pairs, no eigenvector of the positive
eigenvalue r is supported on N[v].  Exact check on controls (rank of rows of A - rI indexed by N[v])."""
import numpy as np, sympy as sp
from graphs_test import paley9, bvls243
for name, A, r in (("paley9", paley9(), 1), ("bvls243", bvls243(), 4)):
    v = 0; U = [v] + list(np.nonzero(A[v])[0])
    M = sp.Matrix(A[U, :] - r * np.eye(A.shape[0], dtype=int)[U, :])
    print(name, "|N[v]| =", len(U), "rank of rows (A - rI)[N[v]] =", M.rank(), "(independent iff = |N[v]|)")
