"""Programme linéaire EXACT (fractions) : genre 1 + forme de Jacobi d'indice 2 des 462 vecteurs-triangles.

Paramètres u = (b_1..b_7, w_1..w_f, P) ; toutes les quantités sont des formes affines exactes en u.
1. Les équations (holomorphie ; sum_r c(n,r) = 462 b_n ; sum_r r^2 c(n,r) = 84 n b_n) sont résolues exactement :
   x = x(b, w), w = paramètres libres restants de l'espace de Jacobi.
2. Inégalités : c(n,r) >= 0 (0 <= r <= sqrt(8n), n <= N) ; c(2,2) >= 4P ; c(2,1) >= 4(7854 - 4P) ;
   c(2,0) >= 8(18711 + 3P) ; 0 <= P <= Pmax ; contraintes de genre 1 « ext » de l'équipe.
3. Réalisabilité décidée par le simplexe exact de lab_theta_lp_2026-10-08/theta_lp_exact.py (dual, Bland), généralisé
   à D inconnues ; un certificat de Farkas est revérifié en cas d'irréalisabilité.
Mode « sanity » : on remplace Conway par un vrai réseau ((sqrt7 E8)^5 + A + A, un vecteur y de norme 4) et on vérifie que
le programme analogue est réalisable.  Usage : python3 jacobi_exact_lp.py N [sanity | d1 d2 ...] [Pmax=...]"""
import sys, math, importlib
from fractions import Fraction as Fr
N = int(sys.argv[1]); args = sys.argv[2:]
Pmax = 1386
ONLY_TRIANGLES = False
for a in list(args):
    if a.startswith('Pmax='): Pmax = int(a[5:]); args.remove(a)
    if a == 'only_triangles': ONLY_TRIANGLES = True; args.remove(a)
sys.argv = ['x', str(N)]
sys.path.insert(0, '/home/user/conway99-c1/research/jacobi_genre2_2026-11-20')
sys.path.insert(0, '/home/user/conway99-c1/code/lab_theta_lp_2026-10-08')
JS = importlib.import_module('jacobi_space')
TL = importlib.import_module('theta_lp')
TX = importlib.import_module('theta_lp_exact')
G = JS.gensJ; R = JS.R; nJ = len(G)
def gc(i, n, r): return Fr(G[i][n].get(r, 0))

def affine_solve(E, RHS, D):
    """E : lignes (listes de nJ fractions) ; RHS : formes affines de longueur 1 + D (constante, puis u).
    Résout E x = RHS exactement. Renvoie (X, free) : x_i = forme affine en (1, u, w) ; free = nb de paramètres w."""
    rows = [list(e) + list(rh) for e, rh in zip(E, RHS)]
    piv = []; r0 = 0
    for c in range(nJ):
        p = next((i for i in range(r0, len(rows)) if rows[i][c] != 0), None)
        if p is None: continue
        rows[r0], rows[p] = rows[p], rows[r0]
        q = rows[r0][c]; rows[r0] = [v / q for v in rows[r0]]
        for i in range(len(rows)):
            if i != r0 and rows[i][c] != 0:
                f = rows[i][c]; rows[i] = [v - f * w for v, w in zip(rows[i], rows[r0])]
        piv.append(c); r0 += 1
    for i in range(r0, len(rows)):                      # lignes nulles en x : contraintes sur u seules
        assert all(v == 0 for v in rows[i][nJ:]), "système incompatible : contrainte sur u"
    freecols = [c for c in range(nJ) if c not in piv]; nf = len(freecols)
    X = [None] * nJ
    for k, c in enumerate(freecols):
        v = [Fr(0)] * (1 + D + nf); v[1 + D + k] = Fr(1); X[c] = v
    for i, c in enumerate(piv):
        v = [Fr(0)] * (1 + D + nf)
        for j in range(1 + D): v[j] = rows[i][nJ + j]
        for k, fc in enumerate(freecols): v[1 + D + k] = -rows[i][fc]
        X[c] = v
    return X, nf

def cform(X, n, r, L):
    v = [Fr(0)] * L
    for i in range(nJ):
        g = gc(i, n, r)
        if g:
            for j, x in enumerate(X[i]):
                if x: v[j] += g * x
    return v

def run(theta_aff, D, extra, label):
    """theta_aff[n] : forme affine (1 + D) de b_n ; extra(L, cf) -> liste de (nom, forme affine longueur L) >= 0."""
    E, RHS = [], []
    for n in range(N + 1):
        for r in range(-R, R + 1):
            if r * r > 8 * n:
                row = [gc(i, n, r) for i in range(nJ)]
                if any(row): E.append(row); RHS.append([Fr(0)] * (1 + D))
        E.append([sum(gc(i, n, r) for r in range(-R, R + 1)) for i in range(nJ)]); RHS.append([462 * t for t in theta_aff[n]] if label != 'sanity' else list(theta_aff[n]))
        if label != 'sanity':
            E.append([sum(r * r * gc(i, n, r) for r in range(-R, R + 1)) for i in range(nJ)]); RHS.append([84 * n * t for t in theta_aff[n]])
    X, nf = affine_solve(E, RHS, D)
    L = 1 + D + nf
    C = []
    for n in range(N + 1):
        for r in range(0, math.isqrt(8 * n) + 1): C.append((f"c({n},{r}) >= 0", cform(X, n, r, L)))
    C += extra(L, lambda n, r: cform(X, n, r, L))
    print(f'[{label}] paramètres libres de Jacobi : {nf} ; inconnues : {L - 1} ; contraintes : {len(C)}', flush=True)
    st = feasible_D(C, L - 1)
    if st[0] != "réalisable" or label == 'sanity': return st
    rng = []
    for sgn in (1, -1):
        form = [Fr(0)] * L; form[8] = Fr(sgn)                       # u = (b_1..b_7, P, w...) : P = inconnue n° 8
        res = TX.simplex([f[1:] for _, f in C], [-f[0] for _, f in C], form[1:])
        rng.append(sgn * res[1] if res[0] == "optimal" else None)
    return (f"réalisable ; P exact dans [{rng[0]}, {rng[1]}]", None)

def feasible_D(C, D):
    res = TX.simplex([f[1:] for _, f in C], [-f[0] for _, f in C], [Fr(0)] * D)
    if res[0] == "unbounded":
        lam = res[1]; assert all(x >= 0 for x in lam)
        assert all(sum(l * f[k] for l, (_, f) in zip(lam, C)) == 0 for k in range(1, D + 1))
        assert sum(l * f[0] for l, (_, f) in zip(lam, C)) < 0
        return ("IRRÉALISABLE (certificat de Farkas vérifié)", [(C[i][0], lam[i]) for i in range(len(C)) if lam[i]])
    assert res[0] == "optimal" and res[1] == 0
    return ("réalisable", None)

if __name__ == '__main__':
    if args and args[0] == 'sanity':
        f = JS.jfromq(JS.TA)
        for _ in range(5): f = JS.jmul(f, JS.jfromq(JS.sub7(JS.E4)))
        truth = JS.jmul(JS.TAy, f)
        theta = [[Fr(sum(truth[n].values()))] for n in range(N + 1)]      # D = 0 : pas d'inconnue de genre 1
        print(run(theta, 0, lambda L, cf: [], 'sanity')[0])
    else:
        ds = [int(a) for a in args] or [36, 38, 40, 42]
        for d in ds:
            A, B = TL.family(d)                                         # affines (1, b_1..b_7)
            D = 8                                                       # b_1..b_7, P
            th = [list(B[n]) + [Fr(0)] for n in range(N + 1)]
            def extra(L, cf, A=A, B=B):
                def lift(f):                                            # forme genre 1 (1 + 7) -> longueur L
                    v = [Fr(0)] * L; v[:8] = f[:8]; return v
                Pv = [Fr(0)] * L; Pv[8] = Fr(1)
                out = []
                out.append(("c(2,2) >= 4P", [a - 4 * p for a, p in zip(cf(2, 2), Pv)]))
                out.append(("c(2,1) >= 4(7854-4P)", [a + 16 * p for a, p in zip(cf(2, 1), Pv)])); out[-1][1][0] -= 4 * 7854
                out.append(("c(2,0) >= 8(18711+3P)", [a - 24 * p for a, p in zip(cf(2, 0), Pv)])); out[-1][1][0] -= 8 * 18711
                out.append(("P >= 0", Pv)); m = [-x for x in Pv]; m[0] += Pmax; out.append((f"P <= {Pmax}", m))
                if ONLY_TRIANGLES:                                      # hypothèse : les seuls vecteurs de norme 4 sont les +-y_T
                    v = lift(B[2]); v[0] -= 462; out.append(("b_2 <= 462", [-x for x in v]))
                    for (nm, f) in list(out[:3]):
                        out.append((nm.replace(">=", "<="), [-x for x in f]))
                    out.append(("c(2,3) <= 0", [-x for x in cf(2, 3)]))
                for n in range(7, N + 1): out.append((f"a_{n} >= 0", lift(A[n])))
                for n in range(1, N + 1): out.append((f"b_{n} >= 0", lift(B[n])))
                for n, lo in ((2, 462), (3, 24948), (4, 388080), (5, 196812)):
                    v = lift(B[n]); v[0] -= lo; out.append((f"b_{n} >= {lo}", v))
                for k in range(1, N // 7 + 1):
                    out.append((f"a_{7*k} >= b_{k}", [x - y for x, y in zip(lift(A[7 * k]), lift(B[k]))]))
                return out
            st, cert = run(th, D, extra, f'd={d}, r={d+1}')
            print(f'd = {d} (r = {d + 1}) : {st}', flush=True)
            if cert: print('   support :', ', '.join(nm for nm, _ in cert[:40]), flush=True)
