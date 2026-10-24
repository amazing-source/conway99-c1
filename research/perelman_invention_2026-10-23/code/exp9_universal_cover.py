"""Expérience 9 : construction du revêtement universel du 2-complexe X (triangles + quadrangles) par énumération de
classes (Todd-Coxeter, stratégie HLT) sur le groupoïde fondamental.

Un sommet du revêtement est au-dessus d'un sommet de base ; table[s][i] est le relevé de l'arête vers le i-ème voisin.
Chaque 2-cellule passant par v est un relateur lu depuis v (dans les deux sens). On n'identifie deux sommets que si un
relateur l'impose (coïncidence) : si l'énumération se termine, le revêtement obtenu est le revêtement universel et
|pi_1(X)| = (nombre de sommets) / |V|. Un plafond arrête les cas infinis ou trop gros.

Usage : python3 exp9_universal_cover.py [noms...]  (par défaut : tous les cas ci-dessous sauf BvLS, qui est lent)."""
import sys, json, time
from collections import deque
sys.path.insert(0, '.')
import srg_tools as T
from exp6_cover_homology import squares_general
from exp5_cover_invariants import cover, files
from exp3_growth_comparison import hamming


def relators(N, adj):
    nb = [sorted(adj[v]) for v in range(N)]
    cells = [list(c) for c in T.lines_of(N, adj)] + [list(q) for q in squares_general(N, adj)]
    rel = [[] for _ in range(N)]
    for c in cells:
        m = len(c)
        for r in range(m):
            cyc = c[r:] + c[:r]
            for w in (cyc, [cyc[0]] + cyc[1:][::-1]):
                rel[w[0]].append(w + [w[0]])
    return nb, rel


def universal_cover(N, adj, cap=400000):
    nb, rel = relators(N, adj)
    pos = [{w: i for i, w in enumerate(nb[v])} for v in range(N)]
    base, table, parent = [], [], []

    def new(v):
        base.append(v); table.append([-1] * len(nb[v])); parent.append(-1)
        return len(base) - 1

    def find(s):
        r = s
        while parent[r] >= 0:
            r = parent[r]
        while parent[s] >= 0:
            parent[s], s = r, parent[s]
        return r

    pending = deque()

    def link(s, i, t):
        # s et t vivants ; un conflit sur la flèche retour devient une coïncidence en attente
        if table[s][i] >= 0 and find(table[s][i]) != t:
            pending.append((find(table[s][i]), t))
        table[s][i] = t
        j = pos[base[t]][base[s]]
        if table[t][j] >= 0 and find(table[t][j]) != s:
            pending.append((find(table[t][j]), s))
        table[t][j] = s

    def coincidence(a, b):
        q = pending
        q.append((a, b))
        while q:
            a, b = q.popleft()
            a, b = find(a), find(b)
            if a == b:
                continue
            if a > b:
                a, b = b, a
            assert base[a] == base[b]
            parent[b] = a
            for i, t in enumerate(table[b]):
                if t < 0:
                    continue
                t = find(t)
                j = pos[base[t]][base[b]]
                if table[t][j] == b:
                    table[t][j] = -1
                if table[a][i] >= 0:
                    q.append((find(table[a][i]), t))
                else:
                    link(a, i, t)
            table[b] = []

    def step(s, v, w):
        t = table[s][pos[v][w]]
        return -1 if t < 0 else find(t)

    def scan(s, word):
        while True:
            s = find(s)
            f, j = s, 0
            m = len(word) - 1
            while j < m:
                t = step(f, word[j], word[j + 1])
                if t < 0:
                    break
                f, j = t, j + 1
            b, l = s, m
            while l > j:
                t = step(b, word[l], word[l - 1])
                if t < 0:
                    break
                b, l = t, l - 1
            if j >= l:
                if f != b:
                    coincidence(f, b)
                return
            if l == j + 1:
                link(f, pos[word[j]][word[j + 1]], b)
                if pending:
                    a0, b0 = pending.popleft()
                    coincidence(a0, b0)
                return
            t = new(word[j + 1])
            link(f, pos[word[j]][word[j + 1]], t)

    root = new(0)
    s = 0
    while s < len(base):
        if parent[s] < 0:
            v = base[s]
            for i in range(len(nb[v])):
                if parent[s] >= 0:
                    break
                if table[s][i] < 0:
                    link(s, i, new(nb[v][i]))
            for word in rel[v]:
                if parent[s] >= 0:
                    break
                scan(s, word)
        s += 1
        if len(base) > cap:
            return None
    live = [x for x in range(len(base)) if parent[x] < 0]
    return len(live)


if __name__ == '__main__':
    cases = {}
    for m in (2, 3):
        cases[f'H({m},3)'] = lambda m=m: hamming(m)
    cases['t2_twisted'] = lambda: T_from('t2_twisted')
    cases['t3_twisted'] = lambda: T_from('t3_twisted')

    def T_from(name):
        A = json.load(open(f'../../../data/{name}.json'))
        return len(A), [set(j for j in range(len(A)) if A[i][j]) for i in range(len(A))]

    for name, f in files.items():
        cases[name] = lambda f=f: (lambda r: (r[0], r[2]))(T.load_edges(f))
        cases[name + '_cover3'] = lambda f=f: cover(f)
    wanted = sys.argv[1:] or [c for c in cases if c != 'BvLS' and c != 'BvLS_cover3']
    out = {}
    for name in wanted:
        n, adj = cases[name]()
        t0 = time.time()
        U = universal_cover(n, adj)
        out[name] = dict(vertices=n, universal_cover_vertices=U,
                         pi1_order=(None if U is None else U // n), seconds=round(time.time() - t0, 1))
        print(name, out[name], flush=True)
    try:
        old = json.load(open('../data/exp9_universal_cover.json'))
    except FileNotFoundError:
        old = {}
    old.update(out)
    json.dump(old, open('../data/exp9_universal_cover.json', 'w'), indent=1)
