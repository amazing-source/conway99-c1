"""X14d -- per vertex configuration: dead if some triangle/star support is locally inadmissible (lambda/mu inside W)
or violates Rayleigh (lambda_min < -4 or lambda_max(A_W - 11J/99) > 3).  Random max twist vs Fano model.
For Fano survivors: does some sigma_i respect the Fano pairing P_i (then Lemma E kills it)?"""
import sys, random, itertools
import numpy as np
sys.path.insert(0, 'scripts')
from x14_triangle_supports import LAB, mate, random_tau, random_sigma, build, admissible
from x14c_fano import FANO, fano_tau

def supports():
    out = []
    for tri in itertools.combinations(range(7), 3):
        out.append(('tri', tri, [frozenset({(i, s), (j, t)}) for i, j in itertools.combinations(tri, 2) for s in (0, 1) for t in (0, 1)]))
    for c in range(7):
        out.append(('star', c, [frozenset({(c, s), l}) for s in (0, 1) for l in LAB if l[0] != c]))
    return out
SUP = supports()

def verdict(tau, sigma):
    inadm = viol = 0
    for kind, key, pairs in SUP:
        A = build(pairs, tau, sigma)
        if not admissible(A):
            inadm += 1; continue
        n = len(A)
        lmax = np.linalg.eigvalsh(A.astype(float) - (11 / 99) * np.ones((n, n))).max()
        lmin = np.linalg.eigvalsh(A.astype(float)).min()
        viol += (lmax > 3 + 1e-9) or (lmin < -4 - 1e-9)
    return inadm, viol

def respects(sigma, i):
    blocks = {}
    for L in FANO:
        if i in L:
            j, k = [c for c in L if c != i]; blocks[j] = blocks[k] = frozenset({j, k})
    return all(sigma[i][b][0] in blocks[b[0]] for b in LAB if b[0] != i)

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 2)
n = int(sys.argv[2]) if len(sys.argv) > 2 else 400
for name, gen in (('random max twist', lambda u: random_tau(u, rng)), ('Fano', lambda u: fano_tau(u, rng))):
    alive = dead_adm = dead_ray = 0; alive_resp = 0
    for _ in range(n):
        tau = {u: gen(u) for u in LAB}; sigma = {c: random_sigma(c, rng) for c in range(7)}
        inadm, viol = verdict(tau, sigma)
        if inadm:
            dead_adm += 1
        elif viol:
            dead_ray += 1
        else:
            alive += 1
            if name == 'Fano':
                alive_resp += any(respects(sigma, i) for i in range(7))
    extra = f', of which some sigma_i respects P_i (Lemma E): {alive_resp}' if name == 'Fano' else ''
    print(f'{name}: {n} configs -> locally inadmissible {dead_adm}, killed by Rayleigh only {dead_ray}, survive {alive}{extra}')
