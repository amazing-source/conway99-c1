"""Expérience 2 : la classe de H^1(X;F_3) des srg(243,22,1,2) tordus vient-elle de l'étalement régulier ?
Étalement régulier = partition des sommets en droites, deux droites de l'étalement reliées par 0 ou 3 arêtes.
Cocycle d'étalement : orienter chaque droite de l'étalement, f = +-1 sur ses arêtes, 0 ailleurs ;
c'est un cocycle si les orientations sont compatibles avec les couplages des prismes.
On teste : existence d'orientations compatibles (2-coloration d'un graphe signé), condition de cocycle,
et non-trivialité (f n'est pas un cobord mod 3)."""
import sys, itertools
sys.path.insert(0, '.')
from srg_tools import *
import flint

ROOT = '/home/user/conway99-c1/data/srg243/'
files = {'BvLS': ROOT + 'bvls243.edges', 'twin': ROOT + 'twin243_switched.edges',
         'Gamma3': ROOT + 'family/gamma3_aut864.edges', 'Gamma4': ROOT + 'family/gamma4_aut3888.edges'}

def regular_spreads(n, adj, lines):
    """Énumère les étalements réguliers par recherche exacte (droites deux à deux à 0 ou 3 arêtes)."""
    line_of_edge = {}
    for L in lines:
        for u, v in itertools.combinations(L, 2):
            line_of_edge[(u, v)] = L; line_of_edge[(v, u)] = L
    def nedges(L, M):
        return sum(1 for u in L for v in M if v in adj[u])
    lines_at = defaultdict(list)
    for L in lines:
        for v in L: lines_at[v].append(L)
    # compatibilité : deux droites disjointes avec 1 ou 2 arêtes ne peuvent pas être toutes deux dans l'étalement
    res = []
    # choisir la droite par le sommet 0, puis propager : dans un étalement régulier, si L est dedans et M est
    # une droite disjointe reliée par 3 arêtes ... on fait une recherche avec propagation simple
    sys.setrecursionlimit(10000)
    def search(chosen, covered):
        if len(covered) == n:
            res.append(list(chosen)); return
        v = min(set(range(n)) - covered)
        for L in lines_at[v]:
            if set(L) & covered: continue
            if any(nedges(L, M) in (1, 2) for M in chosen): continue
            chosen.append(L)
            search(chosen, covered | set(L))
            chosen.pop()
            if len(res) > 20: return
    search([], set())
    return res

def spread_cocycle(n, edges, adj, spread):
    # graphe des droites de l'étalement reliées par 3 arêtes ; chaque telle paire donne une bijection
    pos = {}
    for i, L in enumerate(spread):
        for v in L: pos[v] = i
    # orientation : o[i] = cycle (a,b,c) ; on cherche un signe s_i in {+1,-1} (ordre cyclique fixé ou inversé)
    base = [tuple(L) for L in spread]
    def cyc_sign(L, perm_img):
        # perm_img : images (dans M) des points de L dans l'ordre base(L) ; renvoie +1 si l'ordre cyclique
        # de base(M) est conservé, -1 sinon
        M = base[pos[perm_img[0]]]
        idx = [M.index(x) for x in perm_img]
        d = (idx[1] - idx[0]) % 3
        return 1 if d == 1 else -1
    nb = defaultdict(list)
    for i, L in enumerate(base):
        for j, M in enumerate(base):
            if i < j:
                match = [[y for y in M if y in adj[x]] for x in L]
                if all(len(m) == 1 for m in match):
                    img = [m[0] for m in match]
                    s = cyc_sign(L, img)
                    nb[i].append((j, s)); nb[j].append((i, s))
    sgn = [0] * len(base)
    ok = True
    for r in range(len(base)):
        if sgn[r]: continue
        sgn[r] = 1; stack = [r]
        while stack:
            i = stack.pop()
            for j, s in nb[i]:
                want = sgn[i] * s
                if sgn[j] == 0:
                    sgn[j] = want; stack.append(j)
                elif sgn[j] != want:
                    ok = False
    if not ok:
        return None
    # cochaîne : f(u->v) = +1 si u->v suit l'orientation de la droite d'étalement
    eidx = edge_index(edges)
    f = [0] * len(edges)
    for i, L in enumerate(base):
        a, b, c = L if sgn[i] == 1 else (L[0], L[2], L[1])
        for (u, v) in [(a, b), (b, c), (c, a)]:
            if u < v: f[eidx[(u, v)]] = 1
            else: f[eidx[(v, u)]] = -1
    return f

if __name__ == '__main__':
    import json
    summary = {}
    for name, fpath in files.items():
        n, edges, adj = load_edges(fpath)
        L = lines_of(n, adj); Q = squares_of(n, adj)
        spreads = regular_spreads(n, adj, L)
        rows = boundary_2_rows(edges, L, Q)
        out = []
        cocycles = []
        for S in spreads:
            f = spread_cocycle(n, edges, adj, S)
            if f is None:
                out.append('orientations incompatibles'); continue
            bad = sum(1 for idx, sg in rows if sum(s * f[c] for c, s in zip(idx, sg)) % 3 != 0)
            cocycles.append(f)
            out.append(f'cocycle: {bad == 0}')
        # rang des classes : cobords (n-1) + cocycles d'étalement
        if cocycles:
            M = flint.nmod_mat(n + len(cocycles), len(edges), 3)
            for (u, v), e in edge_index(edges).items():
                M[u, e] = (int(M[u, e]) - 1) % 3; M[v, e] = (int(M[v, e]) + 1) % 3
            for t, f in enumerate(cocycles):
                for e, val in enumerate(f):
                    M[n + t, e] = val % 3
            rk = M.rank()
            print(name, 'étalements réguliers:', len(spreads), out[:12], ' dim des classes engendrées:', rk - (n - 1))
            summary[name] = dict(regular_spreads=len(spreads), cocycle_checks=out, span_dim_mod3=rk - (n - 1))
        else:
            print(name, 'étalements réguliers:', len(spreads), out)
            summary[name] = dict(regular_spreads=len(spreads), cocycle_checks=out, span_dim_mod3=0)
    json.dump(summary, open('../data/exp2_spread_cocycle.json', 'w'), indent=1)
