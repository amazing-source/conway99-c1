"""Expérience 7 : contrôle indépendant (programme linéaire de transport) des formules de courbure d'Ollivier :
arêtes : kappa_0 = 1/k, kappa_alpha = 3(1-alpha)/k pour alpha >= 1/(k+1) (donc LLY = 3/k) ;
non-arêtes : kappa_0 = (k+2)/(2k) si le graphe de transport admet un couplage parfait (eps = 0), (k+1)/(2k) sinon."""
import sys, random
import numpy as np
from scipy.optimize import linprog
from collections import deque
sys.path.insert(0, '.')
import srg_tools as T

def dist_matrix(n, adj):
    D = np.full((n, n), 99, dtype=int)
    for s in range(n):
        D[s, s] = 0; dq = deque([s])
        while dq:
            u = dq.popleft()
            for w in adj[u]:
                if D[s, w] == 99: D[s, w] = D[s, u] + 1; dq.append(w)
    return D

def W1(mu, nu, D):
    P = [i for i in range(len(mu)) if mu[i] > 0]; Qn = [j for j in range(len(nu)) if nu[j] > 0]
    c = np.array([D[i, j] for i in P for j in Qn], dtype=float)
    A_eq, b_eq = [], []
    for a, i in enumerate(P):
        row = np.zeros(len(P) * len(Qn)); row[a * len(Qn):(a + 1) * len(Qn)] = 1; A_eq.append(row); b_eq.append(mu[i])
    for b, j in enumerate(Qn):
        row = np.zeros(len(P) * len(Qn)); row[b::len(Qn)] = 1; A_eq.append(row); b_eq.append(nu[j])
    r = linprog(c, A_eq=np.array(A_eq), b_eq=np.array(b_eq), bounds=(0, None), method='highs')
    return r.fun

def measure(n, adj, x, alpha):
    m = np.zeros(n); m[x] = alpha
    for u in adj[x]: m[u] += (1 - alpha) / len(adj[x])
    return m

ROOT = '/home/user/conway99-c1/data/srg243/'
if __name__ == '__main__':
    import json
    rows = []
    for name, f in [('BvLS', ROOT + 'bvls243.edges'), ('twin', ROOT + 'twin243_switched.edges')]:
        n, edges, adj = T.load_edges(f); k = len(adj[0]); D = dist_matrix(n, adj)
        par = T.nonedge_transport_parity(n, adj)
        random.seed(1)
        for (x, y) in random.sample(edges, 3):
            k0 = 1 - W1(measure(n, adj, x, 0), measure(n, adj, y, 0), D)
            a = 0.5; ka = (1 - W1(measure(n, adj, x, a), measure(n, adj, y, a), D)) / (1 - a)
            print(f'{name} arête {(x, y)} : kappa_0={k0:.6f} (1/k={1 / k:.6f}) ; kappa_0.5/(0.5)={ka:.6f} (3/k={3 / k:.6f})')
            rows.append(dict(graph=name, pair=[x, y], kind='edge', kappa0=k0, kappa_half_over_half=ka,
                             predicted=[1 / k, 3 / k]))
        ne = list(par.items())
        random.shuffle(ne)
        shown = {0: 0, 1: 0}
        for (x, y), (eps, paths, cyc) in ne:
            if shown[eps] >= 2: continue
            shown[eps] += 1
            k0 = 1 - W1(measure(n, adj, x, 0), measure(n, adj, y, 0), D) / 2
            pred = (k + 2) / (2 * k) if eps == 0 else (k + 1) / (2 * k)
            print(f'{name} non-arête {(x, y)} eps={eps} : kappa_0={k0:.6f} prédit={pred:.6f}')
            rows.append(dict(graph=name, pair=[x, y], kind='non-edge', eps=eps, kappa0=k0, predicted=pred))
            if all(v >= 2 for v in shown.values()): break
    json.dump(rows, open('../data/exp7_ollivier_check.json', 'w'), indent=1)
