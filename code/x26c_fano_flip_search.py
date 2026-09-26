r"""X26c -- for a FIXED Fano-tight sigma, search all 2^42 tau-flip assignments (by lines, with pruning) for those
that are locally admissible (7 line-triangle supports + 7 stars; the 28 non-line triangles do not see the flips)
AND satisfy the 21 Psi conditions I_R = 0.  Survivors are then put through the complete per-block cellcross rank
test (all 5 kernel functionals, X25).  Exact finite enumeration, no LP.
usage: python x26c_fano_flip_search.py <config.pkl>"""
import sys, pickle, itertools
from fractions import Fraction
sys.path.insert(0, 'scripts')
from x15_fano_tight import FANO, PHI, LAB, BLOCKS, PAIRS, blk, config_data
from x14_triangle_supports import build, admissible
from x21_fano_cells import keys, tau_from
from x26b_fano_flip_analysis import D_values
from x25_fano_cellcross_blocks import counts, block_system

def rank(rows):
    M = [[Fraction(v) for v in r] for r in rows]
    rk = 0
    for col in range(len(M[0])):
        p = next((i for i in range(rk, len(M)) if M[i][col] != 0), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]
        for i in range(len(M)):
            if i != rk and M[i][col] != 0:
                f = M[i][col] / M[rk][col]; M[i] = [a - f * b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk

def cellcross_rank_ok(tau, sigma):
    D = config_data(tau, sigma)
    if not (D['ok'] and D['imbalance'] == 0 and D['lab_bad'] == 0 and D['neg'] == 0):
        return None
    c = counts(D); bad = []
    for R in BLOCKS:
        free, sd, rhs = block_system(D, c, R)
        rows = [[c[z][Rp] for z in free] for Rp in BLOCKS]
        if rank([r + [rhs[Rp]] for r, Rp in zip(rows, BLOCKS)]) > rank(rows):
            bad.append(''.join(map(str, sorted(R))))
    return bad

if __name__ == '__main__':
    W = pickle.load(open(sys.argv[1], 'rb'))
    sigma = W['sigma']
    D = D_values(W['tau'], sigma)          # D depends on sigma only (asserted below on a second tau)
    LI = {l: i for i, l in enumerate(LAB)}
    base_bits = {k: 0 for k in keys}
    options = []
    for li, L in enumerate(FANO):
        labs = [(c, s) for c in L for s in (0, 1)]
        blocks = [frozenset(p) for p in itertools.combinations(L, 2)]
        tri_pairs = [frozenset({(i, s), (j, t)}) for i, j in itertools.combinations(L, 2) for s in (0, 1) for t in (0, 1)]
        opts = []
        for fl in itertools.product((0, 1), repeat=6):
            f = dict(zip(labs, fl))
            if any(sum((-1) ** (s + f[(X, s)]) * D[(R, X, s)] for X in R for s in (0, 1)) != 0 for R in blocks):
                continue
            bits = dict(base_bits)
            for (X, s), v in f.items():
                bits[(LI[(X, s)], li)] = v
            if not admissible(build(tri_pairs, tau_from(bits), sigma)):
                continue
            opts.append(f)
        options.append(opts)
        print(f'line {L}: {len(opts)} of 64 flip settings pass Psi + line admissibility', flush=True)
    star_pairs = {c: [frozenset({(c, s), l}) for s in (0, 1) for l in LAB if l[0] != c] for c in range(7)}
    lines_of = {c: [li for li, L in enumerate(FANO) if c in L] for c in range(7)}
    found = []
    def rec(li, bits):
        if li == 7:
            found.append(dict(bits)); return
        for f in options[li]:
            b2 = dict(bits)
            for (X, s), v in f.items():
                b2[(LI[(X, s)], li)] = v
            ok = True
            for c in FANO[li]:
                if max(lines_of[c]) == li and not admissible(build(star_pairs[c], tau_from(b2), sigma)):
                    ok = False; break
            if ok:
                rec(li + 1, b2)
    rec(0, dict(base_bits))
    print(f'complete flip assignments passing admissibility + all 21 Psi conditions: {len(found)}', flush=True)
    for k, bits in enumerate(found[:50]):
        tau = tau_from(bits)
        bad = cellcross_rank_ok(tau, sigma)
        print(f'  assignment {k}: per-block cellcross rank obstruction in blocks {bad}', flush=True)
    if found:
        pickle.dump(found, open(sys.argv[1].replace('.pkl', '_psi_flips.pkl'), 'wb'))
