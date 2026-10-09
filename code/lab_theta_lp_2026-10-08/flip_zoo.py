"""C1, lab session, 2026-10-09, mandate B. Goal: srg(243,22,1,2) graphs with LESS symmetry than BvLS and its twin, to test
the sub-lemma "every quadrangle has even holonomy in diameter two". Tool: the flip BvLS -> twin (Codex note 159, decoded
by the laptop session: re-ruling of 80 far grids of a line T). Questions decided here:
  1. the rule of the flip in coordinates; 2. are partial or mixed flips still srg? 3. do flips at two parallel lines
  combine (D D' + D' D = 0 and 0/1 entries)?
  python flip_zoo.py <folder with bvls243.edges and twin243_switched.edges>      One process, seconds."""
import sys, itertools, collections
import numpy as np
R = sys.argv[1]; n = 243


def load(p):
    M = np.zeros((n, n), dtype=np.int64)
    for l in open(p):
        if l.strip():
            i, j = map(int, l.split()); M[i, j] = M[j, i] = 1
    return M


vec = lambda i: tuple((i // 3 ** k) % 3 for k in range(5))
idx = lambda v: sum((v[k] % 3) * 3 ** k for k in range(5))
add = lambda u, v: tuple((a + b) % 3 for a, b in zip(u, v))
sub = lambda u, v: tuple((a - b) % 3 for a, b in zip(u, v))
I = np.eye(n, dtype=np.int64); J = np.ones((n, n), dtype=np.int64)
is_srg = lambda X: bool(((X == 0) | (X == 1)).all() and (X.diagonal() == 0).all() and (X @ X + X == 20 * I + 2 * J).all())
A = load(R + "/bvls243.edges"); B = load(R + "/twin243_switched.edges"); D = B - A
assert is_srg(A) and is_srg(B)
S = [vec(j) for j in range(n) if A[0, j]]
assert all(A[i, idx(add(vec(i), s))] for i in range(n) for s in S)
changed = [i for i in range(n) if (D[i] != 0).any()]
cls = {}                                                   # the two classes of far vertices: components of the changed pairs
for i in changed:
    if i in cls: continue
    cls[i] = len(set(cls.values())); st = [i]
    while st:
        x = st.pop()
        for y in np.nonzero(D[x])[0]:
            if int(y) not in cls: cls[int(y)] = cls[x]; st.append(int(y))
print("classes of changed vertices:", collections.Counter(cls.values()))
c0 = [i for i in changed if cls[i] == 0]; c1 = [i for i in changed if cls[i] == 1]
D0 = np.zeros_like(D); D0[np.ix_(c0, c0)] = D[np.ix_(c0, c0)]; D1 = D - D0
print("D = D0 + D1 with D0 inside one class:", bool((D0 + D1 == D).all()), "; entries between classes:", int((D[np.ix_(c0, c1)] != 0).sum()))
print("2. partial flips: A + D0 srg: %s ; A + D1 srg: %s" % (is_srg(A + D0), is_srg(A + D1)))
# mirror flip: x0 -> -x0 is an automorphism of BvLS (the connection set is symmetric under it?) -> test
neg = [idx((-vec(i)[0] % 3,) + vec(i)[1:]) for i in range(n)]
print("   x0 -> -x0 is an automorphism of BvLS:", bool((A[np.ix_(neg, neg)] == A).all()))
Dm = D[np.ix_(neg, neg)]
print("   mirror flip A + Dm srg: %s ; equal to the flip: %s ; mixed A + D0 + Dm1 srg: %s"
      % (is_srg(A + Dm), bool((Dm == D).all()), is_srg(A + D0 + (Dm - Dm * 0 - np.where(np.isin(np.arange(n), c0)[:, None] & np.isin(np.arange(n), c0)[None, :], Dm, 0)))))
# 3. flips at translates of T: D_t = translate of D by t
def translate(M, t):
    p = [idx(add(vec(i), t)) for i in range(n)]; X = np.zeros_like(M); X[np.ix_(p, p)] = M; return X
res = collections.Counter(); good = []
for t in range(1, n):
    tv = vec(t)
    if not any(tv[1:]): continue                           # the same line T
    Dt = translate(D, tv)
    anti = bool((D @ Dt + Dt @ D == 0).all()); binary = bool(((A + D + Dt == 0) | (A + D + Dt == 1)).all())
    ok = anti and binary and is_srg(A + D + Dt)
    res[(anti, binary, ok)] += 1
    if ok: good.append(t)
print("3. second flip at a translate of T (242 - 2 translates): (anticommute, binary, srg) ->", dict(res))
print("   translates giving an srg:", len(good), good[:12])
np.save("flip_good_translates.npy", np.array(good))
