"""C1, lab session, 2026-10-09. Formula check for NOTE 17.80 (discriminant of the near Gram matrix M0 = 3J - H mod 7).
  python disc_tau_check.py <folder with the laptop session's multi.py, sweep48.py and type files> <number of random graphs> <seed>
Claims checked, on graphs only (no rank hypothesis enters here):
 (a) G connected cubic on 36 vertices, tau = number of spanning trees: det(3J - H) = -3888 tau exactly, so = 4 tau mod 7.
 (b) G = C1 + C2 (balls (s, b) of the (4,8) profile, 7 not dividing tau1 tau2): the Gram matrix M0 has a radical of
     dimension 1 and the discriminant of the quotient of dimension 35 is 3 tau1 tau2 modulo squares.
One process, a few seconds, below 200 MB."""
import sys, os, random
from fractions import Fraction
folder = os.path.abspath(sys.argv[1]); nrand = int(sys.argv[2]); random.seed(int(sys.argv[3])); here = os.getcwd(); os.chdir(folder); sys.path.insert(0, folder)
from multi import make_ball, build
from sweep48 import SMALL, REPS, big_key
QR = {1, 2, 4}
def det_int(M):                                    # exact determinant, fraction-free (Bareiss)
    M = [r[:] for r in M]; n = len(M); sign = 1; prev = 1
    for k in range(n - 1):
        if M[k][k] == 0:
            p = next((i for i in range(k + 1, n) if M[i][k]), None)
            if p is None: return 0
            M[k], M[p] = M[p], M[k]; sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n): M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return sign * M[n - 1][n - 1]
def lap(adj, vs):
    idx = {v: i for i, v in enumerate(vs)}; H = [[0] * len(vs) for _ in vs]
    for v in vs:
        H[idx[v]][idx[v]] = 3
        for w in adj[v]: H[idx[v]][idx[w]] -= 1
    return H
tau = lambda H: det_int([r[1:] for r in H[1:]])
def disc_mod7(M):                                  # (rank, determinant of the non-degenerate quotient mod 7) of a symmetric matrix mod 7
    n = len(M); M = [[x % 7 for x in r] for r in M]; d = 1; rank = 0; live = list(range(n))
    while live:                                    # symmetric elimination: diagonal pivots, or a hyperbolic pair when all diagonals vanish
        p = next((i for i in live if M[i][i]), None)
        if p is None:
            pr = next(((i, j) for i in live for j in live if i < j and M[i][j]), None)
            if pr is None: break
            i, j = pr
            for k in range(n): M[i][k] = (M[i][k] + M[j][k]) % 7
            for k in range(n): M[k][i] = (M[k][i] + M[k][j]) % 7
            p = i
        a = M[p][p]; ia = pow(a, -1, 7); d = d * a % 7; rank += 1; live.remove(p)
        for i in live:
            f = M[i][p] * ia % 7
            if f:
                for k in range(n): M[i][k] = (M[i][k] - f * M[p][k]) % 7
                for k in range(n): M[k][i] = (M[k][i] - f * M[k][p]) % 7
    return rank, d
# (a) random connected cubic layered graphs with twelve points per layer (no further condition: the identity is general)
ok = 0; n = 12; iota = tuple(i ^ 1 for i in range(n))
def rmatch():
    p = list(range(n)); random.shuffle(p); t = [0] * n
    for i in range(0, n, 2): t[p[i]] = p[i + 1]; t[p[i + 1]] = p[i]
    return tuple(t)
done = 0; cls = {0: 0, "QR": 0, "non-QR": 0}
while done < nrand:
    pi = list(range(n)); random.shuffle(pi); adj = build((iota, rmatch(), rmatch(), tuple(pi)))
    if any(len(a) != 3 for a in adj): continue
    seen = {0}; st = [0]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen: seen.add(y); st.append(y)
    if len(seen) != 36: continue
    H = lap(adj, list(range(36))); t = tau(H); M0 = [[3 - H[i][j] for j in range(36)] for i in range(36)]; D = det_int(M0)
    assert D == -3888 * t, (D, t); done += 1
    r, d = disc_mod7(M0)
    if t % 7: assert r == 36 and (d in QR) == ((4 * t) % 7 in QR) and (d in QR) == (t % 7 in QR); cls["QR" if t % 7 in QR else "non-QR"] += 1
    else: assert r < 36; cls[0] += 1
print("(a) %d random connected cubic graphs on 36 vertices: det(3J - H) = -3888 tau in all; tau mod 7: zero %d, quadratic residue %d, non-residue %d" % (done, cls[0], cls["QR"], cls["non-QR"]))
# (b) two components: balls of the (4,8) profile
lines = [l for l in open("types_m4_p0.txt").read().split(chr(10)) if l.strip()]; done = 0; skipped = 0
while done < nrand:
    s = random.choice(REPS); b = random.randrange(len(lines)); adj, lay, comp = make_ball([SMALL[s], big_key(lines[b])], [(0, 1, 2)] * 2)
    c1 = [v for v in range(36) if comp[v] == 0]; c2 = [v for v in range(36) if comp[v] == 1]
    t1 = tau(lap(adj, c1)); t2 = tau(lap(adj, c2))
    if (t1 * t2) % 7 == 0: skipped += 1; continue
    H = lap(adj, list(range(36))); r, d = disc_mod7([[3 - H[i][j] for j in range(36)] for i in range(36)])
    assert r == 35 and (d in QR) == ((3 * t1 * t2) % 7 in QR), (s, b, r, d, t1, t2); done += 1
print("(b) %d torsion-free balls of the (4,8) profile: radical of dimension 1 and discriminant of the quotient = 3 tau1 tau2 modulo squares in all (%d torsion balls skipped)" % (done, skipped))
