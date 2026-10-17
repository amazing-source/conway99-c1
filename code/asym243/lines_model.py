"""Affine line systems of AG(5,3) whose collinearity graph is srg(243,22,1,2).
Vertices = F_3^5 (index = position in sorted list, as in bvls243.edges). A line = coset of <v>, v a direction."""
import itertools, numpy as np
from golay import golay_coords
G, H, PTS = golay_coords()
IDX = {s: i for i, s in enumerate(PTS)}
HS = [tuple(int(x) for x in H[:, p] % 3) for p in range(11)]

def add(a, b, s=1):
    return tuple((x + s * y) % 3 for x, y in zip(a, b))

def norm_dir(v):
    """canonical representative of <v>: first nonzero coordinate = 1."""
    for x in v:
        if x:
            return v if x == 1 else tuple((2 * y) % 3 for y in v)
    raise ValueError

def line(p, v):
    return tuple(sorted((IDX[p], IDX[add(p, v)], IDX[add(p, v, 2)])))

def lines_of_direction(v):
    out = set()
    for p in PTS:
        out.add(line(p, v))
    return sorted(out)

def graph_from_lines(Ls, n=243):
    A = np.zeros((n, n), dtype=np.int64)
    for a, b, c in Ls:
        A[a, b] = A[b, a] = A[a, c] = A[c, a] = A[b, c] = A[c, b] = 1
    return A

def lines_of_graph(A):
    from lib243 import triangles
    return triangles(A)

def affine_line_of(i, j):
    p, q = PTS[i], PTS[j]
    v = add(q, p, 2)
    return line(p, v)

def is_affine_triple(t):
    a, b, c = (PTS[x] for x in t)
    return add(add(a, b), c) == (0,) * 5
