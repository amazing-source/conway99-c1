r"""Finish line (C), C1 27/09: the PACKING criterion from the Niemeier neighbours (root data only).
Let nb_j (j = 1, 2) be the two even neighbours of U (Coxeter numbers h_j, 24 h_j roots, full rank), U0 = even part, r = #roots(U),
new roots of nb_j = roots of nb_j outside U (24 h_j - r of them, they lie in the shadow half S_j).
 * lattice identity: for every norm-3 x in U,  m_j(x) := #{new beta : |(beta,x)| = 3/2} = r/8 - E(x),  E(x) = sum_i h_i |P_i x|^2
   (sum over all roots of nb_j of (beta,x)^2 = 2 h_j |x|^2; old roots give 2E(x), new roots give 1/4 or 9/4).
 * frame identity (F) at a new root beta: sum_u (u,beta)^2 + sum_h (h,beta)^2 + sum_y (y,beta)^2 = 14 with (u,beta),(y,beta) in 1/2+Z
   and (h,beta) in Z gives: AT MOST ONE of the 44 odd frame vectors has |(.,beta)| = 3/2.
 => sum over the 42 u of m_j(u) <= #new_j, hence 42 (r/8 - E*) <= 24 h_j - r, where E* = max E over norm-3 profiles (minuscule weights,
    total norm <= 3, = 3 if the roots span). Violated for some j  =>  U carries no frame: EXCLUDED."""
import json, re
from fractions import Fraction as F
from itertools import product

COX = {'\Lambda': 0, 'A_1^{24}': 2, 'A_2^{12}': 3, 'A_3^8': 4, 'A_4^6': 5, 'A_5^4D_4': 6, 'D_4^6': 6, 'A_6^4': 7, 'A_7^2D_5^2': 8,
       'A_8^3': 9, 'A_9^2D_6': 10, 'D_6^4': 10, 'A_{11}D_7E_6': 12, 'E_6^4': 12, 'A_{12}^2': 13, 'D_8^3': 14, 'A_{15}D_9': 16,
       'A_{17}E_7': 18, 'D_{10}E_7^2': 18, 'D_{12}^2': 22, 'A_{24}': 25, 'D_{16}E_8': 30, 'E_8^3': 30, 'D_{24}': 46}


def comps(s):
    out = []
    for m in re.finditer(r'([ade])_(\{?\d+\}?)(\^(\{?\d+\}?))?', s):
        t = m.group(1); n = int(m.group(2).strip('{}')); k = int(m.group(4).strip('{}')) if m.group(4) else 1
        out += [(t, n)] * k
    return out


def cox(t, n):
    return {'a': n + 1, 'd': 2 * n - 2, 'e': {6: 12, 7: 18, 8: 30}.get(n)}[t]


def minuscule_norms(t, n):
    if t == 'a':
        return sorted({F(k * (n + 1 - k), n + 1) for k in range(1, n + 1)})
    if t == 'd':
        return sorted({F(1), F(n, 4)})
    return {6: [F(4, 3)], 7: [F(3, 2)], 8: []}[n]


def E_star(cs, full_rank):
    """max sum h_i n_i, n_i in {0} u minuscule norms, sum n_i <= 3 (== 3 if full rank). Knapsack over distinct norm values."""
    best = {F(0): 0}                      # total norm -> max E
    for (t, n) in cs:
        h = cox(t, n)
        new = dict(best)
        for tot, e in best.items():
            for nm in minuscule_norms(t, n):
                s = tot + nm
                if s <= 3 and new.get(s, -1) < e + h * nm:
                    new[s] = e + h * nm
        best = new
    if full_rank:
        return best.get(F(3))
    return max(best.values())


if __name__ == '__main__':
    d = json.load(open('data/borcherds_odd24.json'))
    out = []
    for L in d:
        if L['id'] == 0:
            continue
        cs = comps(L['roots'])
        r = L['nroots']
        h1, h2 = COX[L['nb1']], COX[L['nb2']]
        assert r == 8 * (h1 + h2 - 2), L['id']
        Es = E_star(cs, L['rank'] == 24)
        need = 42 * (F(r, 8) - Es) if Es is not None else None
        new = {1: 24 * h1 - r, 2: 24 * h2 - r}
        viol = [j for j in (1, 2) if Es is None or need > new[j]]
        out.append({'id': L['id'], 'roots': L['roots'], 'r8': r // 8, 'Estar': str(Es), 'need': str(need), 'new1': new[1], 'new2': new[2],
                    'excluded': bool(viol), 'status': L['status']})
    ex = [o for o in out if o['excluded']]
    print('excluded by packing:', len(ex))
    for o in out:
        print(o['id'], o['roots'], 'r/8', o['r8'], 'E*', o['Estar'], 'need', o['need'], 'new', o['new1'], o['new2'], 'EXCL' if o['excluded'] else '', o['status'][:25])
    json.dump(out, open('data/finishC/packing.json', 'w'), indent=1)
