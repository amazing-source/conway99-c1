"""(tau(G_T) | 7) for the G_T of the rank-37 runs (LAB 20/10/2026).  tau = number of spanning trees = any cofactor of
the Laplacian 3I - G_T (exact integer, sympy).  Codex's L23 (archive: c1_index_2026-10-09/NOTE_RESEAUX_DE_DROITE.md
section 3): at rank 37 a connected line has (tau | 7) = -1.  usage: python tau_legendre.py"""
import os
import random
import sys

import numpy as np
import sympy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from oblr_prep import make_gt  # noqa: E402


def tau(G):
    L = 3 * np.eye(G.shape[0], dtype=np.int64) - G
    return int(sympy.Matrix(L[1:, 1:].tolist()).det(method="bareiss"))


for spec, seeds in (("c1", range(1, 6)), ("c1t", range(1, 5))):
    for sd in seeds:
        s01, s12, s20, G, nc, comp, d = make_gt(spec, random.Random(sd), 0)
        t = tau(G)
        leg = sympy.legendre_symbol(t % 7, 7) if t % 7 else 0
        print("%s seed %d: c=%d d=%d tau=%d, tau mod 7 = %d, (tau|7) = %d" % (spec, sd, nc, d, t, t % 7, leg), flush=True)
