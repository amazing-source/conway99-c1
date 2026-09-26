r"""X27 -- Fano-tight model with the DERIVED exact block counts c(z) (notes/115-116): the cell-level identities of
X19i restricted to ONE block R decouple (all but cellbal).  For each block R, a tiny LP in the split variables
s[z,k] (z free for R, k = (k_A, k_B), k_A + k_B = c_R(z), sum_k s = 1):
  cellcross (21 rows):  sum_z (k_A - k_B) c_R'(z)  = - sum_{y in R} eps(y) c_R'(y) - (special z)
  cellsame  (3 rows):   sum_z c_z(C) c_z(C')       = 12|C cap C'| + 8 - e(C,C') - L(C,C')      (C, C' cells of R)
  celllab   (20 rows):  sum_{y containing u} c_y(C) = 4                                        (u outside R's classes)
Then, optionally, all blocks together with cellbal e(C,C') = e(C',C) (couples the blocks).
usage: python x27_fano_block_cells.py <config.pkl> [joint]"""
import sys, pickle, itertools
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, 'scripts')
from x15_fano_tight import config_data, BLOCKS, PAIRS, blk, LAB
from x25_fano_cellcross_blocks import counts

cell_of = lambda y: (blk(y), 'A' if len({l[1] for l in y}) == 1 else 'B')
SPL = lambda m: [(a, m - a) for a in range(m + 1)]

def setup(tau, sigma):
    D = config_data(tau, sigma)
    assert D['ok'] and D['imbalance'] == 0 and D['lab_bad'] == 0 and D['neg'] == 0
    c = counts(D)
    spec_cell = {z: {} for z in PAIRS}
    for z in PAIRS:
        for w in D['spec'][z]:
            spec_cell[z][cell_of(w)] = spec_cell[z].get(cell_of(w), 0) + 1
    return D, c, spec_cell

def block_rows(R, c, spec_cell, VI, add_row):
    """append the per-block rows for R; VI[(z,k)] -> column index."""
    A_, B_ = (R, 'A'), (R, 'B')
    members = {h: [y for y in PAIRS if cell_of(y) == (R, h)] for h in 'AB'}
    free = [z for z in PAIRS if not (blk(z) & R) and c[z][R] > 0]
    def cz(z, h):     # count of z's neighbours in cell (R,h): linear form (dict) + const
        if blk(z) & R:
            return {}, spec_cell[z].get((R, h), 0)
        if c[z][R] == 0:
            return {}, 0
        return {VI[(z, k)]: (k[0] if h == 'A' else k[1]) for k in SPL(c[z][R])}, 0
    eps = {y: (1 if cell_of(y)[1] == 'A' else -1) for y in PAIRS if blk(y) == R}
    for Rp in BLOCKS:                                   # cellcross
        F = {}; c0 = 0
        for z in PAIRS:
            if not c[z][Rp]: continue
            for h, sg in (('A', 1), ('B', -1)):
                G, k0 = cz(z, h)
                for j, v in G.items(): F[j] = F.get(j, 0) + sg * v * c[z][Rp]
                c0 += sg * k0 * c[z][Rp]
        r = -sum(eps[y] * c[y][Rp] for y in eps)
        add_row(F, r - c0, f'cellcross|{R}|{Rp}')
    L = lambda S1, S2: sum(len(a & b) for a in S1 for b in S2)
    for h1, h2 in (('A', 'A'), ('A', 'B'), ('B', 'B')):   # cellsame (products: per split, exact)
        F = {}; c0 = 0
        for z in PAIRS:
            if blk(z) & R:
                c0 += spec_cell[z].get((R, h1), 0) * spec_cell[z].get((R, h2), 0); continue
            if c[z][R] == 0: continue
            for k in SPL(c[z][R]):
                v1 = k[0] if h1 == 'A' else k[1]; v2 = k[0] if h2 == 'A' else k[1]
                if v1 * v2: F[VI[(z, k)]] = F.get(VI[(z, k)], 0) + v1 * v2
        C1, C2 = members[h1], members[h2]
        r = 12 * len(set(C1) & set(C2)) + 2 * len(C1) * len(C2) - L(C1, C2)
        for w in C1:                                     # - e(C1, C2): w's neighbours in C2 (w in R: specials only)
            r -= spec_cell[w].get((R, h2), 0)
        add_row(F, r - c0, f'cellsame|{R}|{h1}{h2}')
    for u in LAB:                                        # celllab
        if u[0] in R: continue
        for h in 'AB':
            F = {}; c0 = 0
            for y in PAIRS:
                if u in y:
                    G, k0 = cz(y, h)
                    for j, v in G.items(): F[j] = F.get(j, 0) + v
                    c0 += k0
            add_row(F, 4 - c0, f'celllab|{u}|{R}{h}')
    return free

def solve_block(R, c, spec_cell):
    free = [z for z in PAIRS if not (blk(z) & R) and c[z][R] > 0]
    var = [(z, k) for z in free for k in SPL(c[z][R])]
    VI = {v: i for i, v in enumerate(var)}
    rows, rhs = [], []
    def add_row(F, r, name): rows.append(F); rhs.append(r)
    for z in free:
        add_row({VI[(z, k)]: 1 for k in SPL(c[z][R])}, 1, 'conv')
    block_rows(R, c, spec_cell, VI, add_row)
    A = np.zeros((len(rows), len(var)))
    for i, F in enumerate(rows):
        for j, v in F.items(): A[i, j] = v
    res = linprog(np.zeros(len(var)), A_eq=A, b_eq=np.array(rhs, float), bounds=(0, None), method='highs')
    return res.status

if __name__ == '__main__':
    W = pickle.load(open(sys.argv[1], 'rb'))
    D, c, spec_cell = setup(W['tau'], W['sigma'])
    bad = []
    for R in BLOCKS:
        st = solve_block(R, c, spec_cell)
        if st == 2: bad.append(''.join(map(str, sorted(R))))
    print(f'{sys.argv[1]}: per-block cell systems infeasible in {len(bad)} blocks: {bad}', flush=True)
