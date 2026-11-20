"""Formes de Jacobi de poids 22, indice 2, niveau Gamma_0(7) : construction et validation.

Structure (Eichler-Zagier, étendue aux sous-groupes de congruence ; vérifiée ici sur des exemples) :
    J^weak_{22,2}(Gamma_0(7)) = M_22 phi_{0,1}^2 + M_24 phi_{-2,1} phi_{0,1} + M_26 phi_{-2,1}^2.
Une forme holomorphe vérifie de plus c(n, r) = 0 pour r^2 > 8n.
Validation : pour L = E8^a + (sqrt7 E8)^b + A + A (a + b = 5, A = réseau binaire de forme 2(x^2+xy+2y^2), rang 44,
niveau 7) et y un vecteur de norme 4 de A, la série thêta de Jacobi theta_{L,y}(tau, z) = sum_x q^{Q(x)/2} zeta^{B(x,y)}
doit appartenir à l'espace holomorphe ; on le vérifie jusqu'à q^N.
Arithmétique exacte (entiers et fractions)."""
import sys, math
from fractions import Fraction as Fr
N = int(sys.argv[1]) if len(sys.argv) > 1 else 30
R_FIN = math.isqrt(8 * N) + 6                      # plage finale des r : -R_FIN..R_FIN
R = N + 6                                          # plage interne (les termes de wp(tau,z) vont jusqu'à |r| = n)

# ---------- séries en q (listes de longueur N+1)
def mul(a, b):
    c = [0] * (N + 1)
    for i, x in enumerate(a):
        if x:
            for j in range(N + 1 - i):
                if b[j]: c[i + j] += x * b[j]
    return c
def sub7(a):
    b = [0] * (N + 1)
    for i in range(N // 7 + 1): b[7 * i] = a[i]
    return b
def sigma(n, k): return sum(d ** k for d in range(1, n + 1) if n % d == 0)
E2 = [1] + [-24 * sigma(n, 1) for n in range(1, N + 1)]
E4 = [1] + [240 * sigma(n, 3) for n in range(1, N + 1)]
E6 = [1] + [-504 * sigma(n, 5) for n in range(1, N + 1)]
e2 = [Fr(7 * x - y, 6) for x, y in zip(sub7(E2), E2)]         # (7 E2(7t) - E2(t))/6, dans M_2(Gamma_0(7))
gens = {'e2': (2, e2), 'E4': (4, E4), 'E4_7': (4, sub7(E4)), 'E6': (6, E6), 'E6_7': (6, sub7(E6))}

def monomials(k):
    out = []
    def rec(names, w, acc):
        if w == k: out.append(acc); return
        if not names: return
        nm = names[0]; wt, f = gens[nm]
        p = [Fr(1)] + [Fr(0)] * N; e = 0
        while w + e * wt <= k:
            rec(names[1:], w + e * wt, mul(acc, p) if e else acc)
            p = mul(p, f); e += 1
    rec(list(gens), 0, [Fr(1)] + [Fr(0)] * N)
    return out

def rowreduce(vecs):
    basis = []; pivots = []
    for v in vecs:
        v = list(v)
        for b, p in zip(basis, pivots):
            if v[p]: c = v[p] / b[p]; v = [x - c * y for x, y in zip(v, b)]
        nz = next((i for i, x in enumerate(v) if x), None)
        if nz is not None: basis.append(v); pivots.append(nz)
    return basis

def Mbasis(k):
    B = rowreduce(monomials(k)); dim = 1 + 2 * (k // 3)
    assert len(B) == dim, (k, len(B), dim)
    return B

# ---------- séries de Jacobi : dict n -> dict r -> coeff
def jmul(f, g):
    h = [dict() for _ in range(N + 1)]
    for n1 in range(N + 1):
        for r1, c1 in f[n1].items():
            for n2 in range(N + 1 - n1):
                for r2, c2 in g[n2].items():
                    r = r1 + r2
                    if abs(r) <= R: h[n1 + n2][r] = h[n1 + n2].get(r, 0) + c1 * c2
    return h
def jscal(f, s): return [{r: c * s for r, c in d.items()} for d in f]
def jadd(f, g):
    h = [dict(d) for d in f]
    for n in range(N + 1):
        for r, c in g[n].items(): h[n][r] = h[n].get(r, 0) + c
    return h
def jfromq(a): return [({0: a[n]} if a[n] else {}) for n in range(N + 1)]   # forme modulaire vue comme série de Jacobi

# phi_{-2,1} = (zeta - 2 + zeta^-1) prod_{n>=1} (1 - q^n zeta)^2 (1 - q^n zeta^-1)^2 / (1 - q^n)^4
def prodPi():
    P = [dict() for _ in range(N + 1)]; P[0] = {0: 1}
    for n in range(1, N + 1):
        for fac in ([(n, 1)] * 2 + [(n, -1)] * 2):     # (1 - q^n zeta^{s})
            nn, s = fac
            Q = [dict(d) for d in P]
            for m in range(N + 1 - nn):
                for r, c in P[m].items():
                    rr = r + s
                    if abs(rr) <= R: Q[m + nn][rr] = Q[m + nn].get(rr, 0) - c
            P = Q
        inv = [0] * (N + 1); inv[0] = 1                  # 1/(1 - q^n)^4 = sum C(k+3,3) q^{nk}
        for k in range(1, N // n + 1): inv[n * k] = math.comb(k + 3, 3)
        P = jmul(P, jfromq(inv))
    return P
Pi = prodPi()
phim2 = jmul([{1: 1, 0: -2, -1: 1}] + [dict() for _ in range(N)], Pi)
# phi_{0,1} = 12 [ phi_{-2,1}/12 + Pi + phi_{-2,1} * sum_n sum_{d|n} d (zeta^d - 2 + zeta^-d) q^n ]
W = [dict() for _ in range(N + 1)]
for n in range(1, N + 1):
    for d in range(1, n + 1):
        if n % d == 0:
            W[n][d] = W[n].get(d, 0) + d; W[n][-d] = W[n].get(-d, 0) + d; W[n][0] = W[n].get(0, 0) - 2 * d
phi01 = jadd(jadd(phim2, jscal(Pi, 12)), jscal(jmul(phim2, W), 12))
def jtrunc(f, RF): return [{r: c for r, c in d.items() if abs(r) <= RF and c} for d in f]
phi01 = jtrunc(phi01, R_FIN); phim2 = jtrunc(phim2, R_FIN)
assert all(r * r <= 4 * n + 1 for n in range(N + 1) for r in phi01[n]), 'phi01 non faible'
assert all(r * r <= 4 * n + 1 for n in range(N + 1) for r in phim2[n]), 'phim2 non faible'
R = R_FIN
assert phi01[0] == {1: 1, 0: 10, -1: 1}, phi01[0]
assert phi01[1] == {2: 10, 1: -64, 0: 108, -1: -64, -2: 10}, phi01[1]
assert phim2[1] == {2: -2, 1: 8, 0: -12, -1: 8, -2: -2}, phim2[1]

# ---------- espace faible : 49 générateurs
B22, B24, B26 = Mbasis(22), Mbasis(24), Mbasis(26)
P00 = jmul(phi01, phi01); P10 = jmul(phim2, phi01); P20 = jmul(phim2, phim2)
gensJ = [jmul(jfromq(f), P00) for f in B22] + [jmul(jfromq(f), P10) for f in B24] + [jmul(jfromq(f), P20) for f in B26]
print('dimension faible :', len(gensJ), flush=True)

def coeffvec(f, keys): return [Fr(f[n].get(r, 0)) for (n, r) in keys]
keys = [(n, r) for n in range(N + 1) for r in range(-R, R + 1)]
holo_keys = [(n, r) for (n, r) in keys if r * r > 8 * n]

def solve_in_span(target, gens_list, keyset):
    """Résout target = sum x_i gens_i sur keyset (exact). Renvoie x ou None."""
    cols = [coeffvec(g, keyset) for g in gens_list]; t = coeffvec(target, keyset)
    m = len(keyset); k = len(cols)
    Mx = [[cols[j][i] for j in range(k)] + [t[i]] for i in range(m)]
    piv = []; row = 0
    for c in range(k):
        p = next((i for i in range(row, m) if Mx[i][c]), None)
        if p is None: continue
        Mx[row], Mx[p] = Mx[p], Mx[row]
        inv = 1 / Mx[row][c]; Mx[row] = [x * inv for x in Mx[row]]
        for i in range(m):
            if i != row and Mx[i][c]:
                f = Mx[i][c]; Mx[i] = [x - f * y for x, y in zip(Mx[i], Mx[row])]
        piv.append(c); row += 1
    if any(Mx[i][k] for i in range(row, m)): return None
    x = [Fr(0)] * k
    for i, c in enumerate(piv): x[c] = Mx[i][k]
    return x

# ---------- validation sur L = E8^a + (sqrt7 E8)^b + A + A, y dans A de norme 4
TA = [0] * (N + 1); TAy = [dict() for _ in range(N + 1)]
RR = math.isqrt(8 * N) + 3
for x in range(-RR, RR + 1):
    for yv in range(-RR, RR + 1):
        v = x * x + x * yv + 2 * yv * yv
        if v <= N:
            TA[v] += 1
            # B((x,yv),(0,1)) pour la forme 2(x^2 + x y + 2 y^2) : B = x*0... gram [[2,1],[1,4]] ; (x,yv).G.(0,1) = x + 4 yv
            r = x + 4 * yv
            TAy[v][r] = TAy[v].get(r, 0) + 1
assert sum(TAy[2].values()) == 4 and TAy[2].get(4) == 1      # y = (0,1) a norme 2*2 = 4, B(y,y) = 4
if __name__ == '__main__':
    ok = 0
    for a in range(6):
        b = 5 - a; f = jfromq(TA)
        for _ in range(a): f = jmul(f, jfromq(E4))
        for _ in range(b): f = jmul(f, jfromq(sub7(E4)))
        test = jmul(TAy, f)
        assert all(test[n].get(r, 0) == 0 for (n, r) in holo_keys)
        x = solve_in_span(test, gensJ, keys)
        print(f'a={a}, b={b} : theta de Jacobi dans J_(22,2)(Gamma_0(7)) jusqu\'à q^{N} :', x is not None, flush=True)
        ok += x is not None
    # dimension de l'espace holomorphe
    cols = [coeffvec(g, holo_keys) for g in gensJ]
    import sympy
    Mh = sympy.Matrix([[cols[j][i] for j in range(len(cols))] for i in range(len(holo_keys))])
    rk = Mh.rank()
    print('contraintes d\'holomorphie : rang', rk, '; dimension holomorphe = 49 -', rk, '=', 49 - rk)
