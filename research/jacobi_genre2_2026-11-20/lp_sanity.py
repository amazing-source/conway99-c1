import sys, math, importlib
import numpy as np
from scipy.optimize import linprog
N = int(sys.argv[1]) if len(sys.argv) > 1 else 24
sys.argv = ['x', str(N)]
sys.path.insert(0, '/home/user/conway99-c1/research/jacobi_genre2_2026-11-20')
JS = importlib.import_module('jacobi_space')
G = JS.gensJ; R = JS.R; nJ = len(G)
# vrai réseau : L = (sqrt7 E8)^5 + A + A, y dans A de norme 4 ; Phi = theta_{L,y}, theta = theta_L
f = JS.jfromq(JS.TA)
for _ in range(5): f = JS.jmul(f, JS.jfromq(JS.sub7(JS.E4)))
truth = JS.jmul(JS.TAy, f)
theta = [sum(truth[n].values()) for n in range(N + 1)]      # = theta_L (un seul y)
def cform(n, r): return np.array([float(g[n].get(r, 0)) for g in G])
for scaled in (False, True):
    Aeq, beq, Aub, bub = [], [], [], []
    for n in range(N + 1):
        for r in range(-R, R + 1):
            if r * r > 8 * n:
                v = cform(n, r)
                if np.any(v): Aeq.append(v); beq.append(0.0)
        Aeq.append(sum(cform(n, r) for r in range(-R, R + 1))); beq.append(float(theta[n]))
        for r in range(0, math.isqrt(8 * n) + 1): Aub.append(-cform(n, r)); bub.append(0.0)
    Aeq = np.array(Aeq); beq = np.array(beq); Aub = np.array(Aub); bub = np.array(bub)
    if scaled:
        colsc = np.maximum(np.max(np.abs(np.vstack([Aeq, Aub])), axis=0), 1e-300); Aeq = Aeq / colsc; Aub = Aub / colsc
        re = np.maximum(np.max(np.abs(Aeq), axis=1), 1e-300); Aeq = Aeq / re[:, None]; beq = beq / re
        ru = np.maximum(np.max(np.abs(Aub), axis=1), 1e-300); Aub = Aub / ru[:, None]; bub = bub / ru
    res = linprog(np.zeros(nJ), A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq, bounds=[(None, None)] * nJ, method='highs')
    print('mise à l\'échelle' if scaled else 'brut', ': statut', res.status, '(0 = réalisable)', res.message[:80])
    mx = max(abs(float(g[n].get(r, 0))) for g in G for n in range(N + 1) for r in g[n])
    print('   plus grand coefficient des générateurs :', f'{mx:.3e}')
