r"""Finish line (C), C1 27/09: h-configurations up to the Weyl group, with the star-sum (L7) test.  PROVEN conditions (notes/140):
 (O) 7 pairwise orthogonal norm-4 h; (H2) |(h,beta)| <= 1 on new roots, w(beta) in {1,3}; (Z) sum h in 2U;
 (CELL) for each pair {c,d} and t = +-1 a norm-3 x with (x,h_c)(x,h_d) = t (both +-1), (x,h_e) = 0 for e not in {c,d};
 (STAR) for each block c: one x per cell of star(c) (12 cells: 6 partners d, 2 signs t) with sum_cells (x,h_c) x = 3 h_c
        (from 3h_c + sum_{o in c} C_co u_o = 0 and (u_o,h_c) = -C_co);  checked per block (necessary), exact, by CP-SAT <= 60 s.
Symmetry (complete): ordered sequences (h_1..h_7), h_{k+1} dominant (up to sign) for the root subsystem R_k = R cap {h_1..h_k}-perp
(pointwise stabilisers in W(R) are the reflection groups W(R_k), Steinberg); positive roots fixed by a generic vector.
Usage: python rigid_h.py <envelope.json> [--max-seconds S]  (run through run_capped.ps1 -LimitMB 2500)."""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from h_stage2 import setup
from frame_pipeline import y_stage
from u_stage import u_stage


def main():
    rec_ = json.load(open(sys.argv[1]))
    ms = float(sys.argv[sys.argv.index('--max-seconds') + 1]) if '--max-seconds' in sys.argv else 1200
    t0 = time.time()
    B, Bf, R, X3, X4c, X4, S = setup(rec_['gens'])
    HS = np.rint(X4 @ S.T).astype(np.int64)
    ok = np.abs(HS).max(axis=1) <= 1
    H, Hc, cov = X4[ok], X4c[ok], (HS[ok] != 0)
    M, NI = len(H), len(S)
    g = np.random.RandomState(11).randn(24)
    Rp = np.array([a if a @ g > 0 else -a for a in R]) if len(R) else np.zeros((0, 24))
    HR = H @ Rp.T                                                   # (h, alpha) for positive roots
    par = np.array([int(''.join(str(int(b) & 1) for b in row[::-1]), 2) for row in Hc], dtype=object)
    IP3 = np.rint(X3 @ H.T).astype(np.int8)
    X3c_int = np.rint(X3 @ np.linalg.inv(Bf)).astype(np.int64)      # integer coordinates of norm-3 vectors
    Hc_int = Hc.astype(np.int64)
    print({'roots': 2 * len(R), 'items': NI, 'h_cands': M, 'setup_s': round(time.time() - t0, 1)}, flush=True)
    Gi = [[int(round(v)) for v in row] for row in (Bf @ Bf.T)]
    m3 = (np.abs(np.abs(X3 @ S.T) - 1.5) < 1e-6).sum(axis=1)
    ctx = {'Bq': B, 'Gi': Gi, 'Bf': Bf, 'R': R, 'X3': X3, 'H': H, 'Hc': Hc, 'S': S, 'HS': HS[ok], 'm3': m3}
    stats = {'nodes': 0, 'full': 0, 'wZ_ok': 0, 'cells_ok': 0, 'star_ok': 0, 'y_ok': 0, 'timeout': False}
    survivors = []
    prev_free = [False]

    def dominant_ok(i, rootmask):
        """h_i (or -h_i) dominant for the positive roots selected by rootmask."""
        v = HR[i, rootmask]
        return bool((v >= -1e-9).all() or (v <= 1e-9).all())

    def cells(chosen):
        cols = IP3[:, chosen].astype(np.int16); nz = cols != 0; cnt = nz.sum(axis=1)
        out = {}
        for a in range(len(chosen)):
            for b in range(a + 1, len(chosen)):
                sel = (cnt == 2) & nz[:, a] & nz[:, b] & (np.abs(cols[:, a]) == 1) & (np.abs(cols[:, b]) == 1)
                idx = np.nonzero(sel)[0]
                prod = cols[idx, a] * cols[idx, b]
                pos, neg = idx[prod > 0], idx[prod < 0]
                if len(pos) == 0 or len(neg) == 0:
                    return None
                out[(a, b, 1)] = pos; out[(a, b, -1)] = neg
        return out

    def star_ok(chosen, cl):
        from ortools.sat.python import cp_model
        for c in range(7):
            m = cp_model.CpModel()
            vars_, terms = [], []
            for (a, b, t), idx in cl.items():
                if c not in (a, b):
                    continue
                vs = [m.NewBoolVar('') for _ in idx]
                m.AddExactlyOne(vs)
                col = IP3[idx, chosen[c]].astype(np.int64)          # (x, h_c) = +-1
                for v, x, s in zip(vs, idx, col):
                    terms.append((v, s * X3c_int[x]))
            target = 3 * Hc_int[chosen[c]]
            for k in range(24):
                m.Add(sum(v * int(vec[k]) for v, vec in terms if vec[k] != 0) == int(target[k]))
            sol = cp_model.CpSolver()
            sol.parameters.max_time_in_seconds = 60
            sol.parameters.num_workers = 1
            st = sol.Solve(m)
            if st == cp_model.INFEASIBLE:
                return False
            if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                return None                                           # unknown: keep as survivor
        return True

    def rec(chosen, cand, w, rootmask):
        stats['nodes'] += 1
        if time.time() - t0 > ms:
            stats['timeout'] = True
            return
        k = len(chosen)
        if k == 7:
            stats['full'] += 1
            if not np.all((w == 1) | (w == 3)):
                return
            p = 0
            for i in chosen:
                p ^= par[i]
            if p != 0:
                return
            stats['wZ_ok'] += 1
            cl = cells(chosen)
            if cl is None:
                return
            stats['cells_ok'] += 1
            so = star_ok(chosen, cl)
            if so is False:
                return
            stats['star_ok'] += 1
            yi = y_stage(ctx, list(chosen))
            if not yi.get('verdict', '').endswith('survive'):
                return
            stats['y_ok'] += 1
            X3c = np.rint(X3 @ np.linalg.inv(Bf)).astype(np.int64)
            ures = []
            for (a1, a2) in yi['pair_vecs']:
                st, det = u_stage(B, Gi, X3, X3c, [Hc[i] for i in chosen], [a1, a2], S, yi['B1_idx'], time_limit=60)
                ures.append(st)
                if st != 'INFEASIBLE':
                    break
            if all(st == 'INFEASIBLE' for st in ures) and len(ures) == len(yi['pair_vecs']) and yi.get('y_pairs', 0) <= 200:
                stats['u_dead'] = stats.get('u_dead', 0) + 1
                return
            survivors.append({'h': [int(i) for i in chosen], 'star': 'feasible' if so else 'unknown',
                              'y_pairs': yi.get('y_pairs'), 'u': ures[-1] if ures else None})
            print('SURVIVOR', survivors[-1], flush=True)
            return
        # every item with w = 0 must still be coverable: crude bound
        zero = np.nonzero(w == 0)[0]
        if len(zero):
            if len(cand) == 0:
                return
            if not cov[cand][:, zero].any(axis=0).all():
                return
        free_order = not rootmask.any()                 # no root orthogonal to the chosen h: no symmetry left,
        last = chosen[-1] if chosen else -1              # the remaining h form an unordered set: increasing indices
        for i in cand:
            if free_order and prev_free[0] and i <= last:
                continue
            if not dominant_ok(i, rootmask):
                continue
            nw = w + cov[i]
            if (nw > 3).any():
                continue
            ch = chosen + [int(i)]
            if k >= 1 and cells(ch) is None:
                continue
            nc = cand[(np.abs(H[cand] @ H[i]) < 1e-9)]
            nc = nc[nc != i]
            nrm = rootmask & (np.abs(HR[i]) < 1e-9)
            saved = prev_free[0]
            prev_free[0] = free_order
            rec(ch, nc, nw, nrm)
            prev_free[0] = saved
            if stats['timeout']:
                return

    rec([], np.arange(M), np.zeros(NI, dtype=np.int64), np.ones(len(Rp), dtype=bool))
    stats['survivors'] = len(survivors)
    stats['seconds'] = round(time.time() - t0, 1)
    stats['verdict'] = ('EXCLUDED (no h-configuration passes O + H2 + Z + CELL + STAR)' if not survivors and not stats['timeout']
                        else ('TIMEOUT' if stats['timeout'] else 'survivors'))
    print(json.dumps(stats), flush=True)


if __name__ == '__main__':
    main()
