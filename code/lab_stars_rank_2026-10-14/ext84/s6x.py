"""Six-star extension test S6X (LAB 16/10/2026), built on Codex's column machinery (read-only copies).

A rank-30 germ S (lines l = {v,0,1}, m = {v,2,3}) and a third line n = {v,y,y^1} (y outer).  In a Conway graph the
60 labels meeting l u m u n carry T of rank 30 (it contains S), so the 16 new labels (those meeting n but not l, m)
have columns in their exact domains (range equations of T and U, Schur norm 20/8, U residual >= 0, caps), and every
new-new adjacency is forced by T.  We enumerate all such 16-label assemblies with:
  - T-forced edges binary, U residual 2x2 compatible, and a final exact U-residual PSD check of rank <= 40 - rank U_S;
  - partial graph checks (degree <= 12, common neighbours <= 2 - incidence).
Each assembly gives two four-star blocks (l,n) and (m,n), principal blocks of T, U on 60 labels (PSD, nullity >= 14).
Their star matchings on l (resp. m) are those of S, so the l-half of (H-MATCH) at (l,n) holds iff M_1 = s(n) M_0.
An assembly with a broken block that passes the full local checks would be an exact counterexample to (H-MATCH).
usage: python s6x.py <germ json> <out json> [seconds per column]"""
import json
import sys
import time
from itertools import combinations
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_star_completion_columns import prepare, inverse_on_range, enumerate_column
from hmatch_cycle_reflections import LABELS
from odd9_endpoint_mate_family import exact_psd

OUTSIDE = [p for p in combinations(range(4, 14), 2) if p[1] != (p[0] ^ 1)]


def matchings(gamma):
    M = {}
    for a in range(4):
        idx = [i for i, p in enumerate(LABELS) if a in p]
        other = {i: (p[0] if p[1] == a else p[1]) for i, p in enumerate(LABELS) if a in p}
        pairs = set()
        for i in idx:
            nb = [j for j in idx if gamma[i, j]]
            assert len(nb) == 1, (a, LABELS[i], nb)
            pairs.add(tuple(sorted((other[i], other[nb[0]]))))
        M[a] = pairs
    return M


def apply(perm, pairs):
    return set(tuple(sorted((perm.get(a, a), perm.get(b, b)))) for a, b in pairs)


def main():
    src, out = sys.argv[1], sys.argv[2]
    per = float(sys.argv[3]) if len(sys.argv) > 3 else 5.0
    t0 = time.monotonic()
    gamma, t8, u15, kt, ku = prepare(json.loads(Path(src).read_text(encoding='utf-8')))
    assert kt.shape[1] == 14, 'needs T rank 30'
    ti, ui = inverse_on_range(t8), inverse_on_range(u15)
    resid_target = 40 - len(ui[0])
    M = matchings(gamma)
    report = dict(source=src, U_rank=len(ui[0]), U_residual_rank_total=resid_target, lines={}, domains={})
    doms = {}
    for lab in OUTSIDE:
        col = enumerate_column(lab, gamma, kt, ku, ti, ui, per)
        doms[lab] = col
        report['domains'][str(lab)] = dict(size=len(col['domains']), complete=col['complete'], status=col['status'])
    print('domains:', {str(k): (len(v['domains']), v['complete']) for k, v in doms.items()}, flush=True)
    _, tn, td = ti
    _, un, ud = ui

    def offsets(p, q):
        inter = len(set(p) & set(q))
        mates = sum((r ^ 1) in q for r in p)
        return 3 * inter + mates - 2, 4 * inter - mates + 2

    for k in range(2, 7):
        n = (2 * k, 2 * k + 1)
        sn = {n[0]: n[1], n[1]: n[0]}
        sm = {2: 3, 3: 2}
        sl = {0: 1, 1: 0}
        pred = dict(l_half_at_ln=(apply(sn, M[0]) == M[1]), m_half_at_mn=(apply(sn, M[2]) == M[3]),
                    M0_pairs_n=(tuple(n) in M[0]), M2_pairs_n=(tuple(n) in M[2]))
        new = [p for p in OUTSIDE if n[0] in p or n[1] in p]
        assert len(new) == 16
        entry = dict(third_line=list(n), predicted=pred, new_labels=[list(p) for p in new])
        empty = [p for p in new if doms[p]['complete'] and not doms[p]['domains']]
        incomplete = [p for p in new if not doms[p]['complete']]
        if empty:
            entry.update(status='IMPOSSIBLE_EMPTY_DOMAIN', empty=[list(p) for p in empty])
            report['lines'][str(n)] = entry
            print(n, entry['status'], empty, pred, flush=True)
            continue
        if incomplete:
            entry.update(status='DOMAIN_INCOMPLETE', incomplete=[list(p) for p in incomplete])
            report['lines'][str(n)] = entry
            print(n, entry['status'], incomplete, flush=True)
            continue
        D = [doms[p]['domains'] for p in new]
        coords = [[(np.array(d['T_coordinates'], dtype=object), np.array(d['U_coordinates'], dtype=object),
                    int(d['U_residual_numerator'])) for d in dom] for dom in D]
        cache = {}

        def pair(i, ai, j, aj):
            key = (i, ai, j, aj) if i < j else (j, aj, i, ai)
            if key in cache:
                return cache[key]
            i2, ai2, j2, aj2 = key
            bt, bu, di = coords[i2][ai2]
            ct, cu, dj = coords[j2][aj2]
            kk, ll = offsets(new[i2], new[j2])
            num = -int(bt @ tn @ ct) - td * kk
            if num not in (0, 8 * td):
                cache[key] = None
                return None
            e = num // (8 * td)
            res = ud * (15 * e - ll) - int(bu @ un @ cu)
            ok = (res * res <= di * dj) if resid_target >= 2 else (res * res == di * dj)
            cache[key] = (e, res) if ok else None
            return cache[key]

        sols, nodes = [], [0]
        deadline = time.monotonic() + 120
        inc = [[] for _ in range(16)]  # chosen neighbours

        def graph_ok(sel):
            # degree <= 12 and pairwise common-neighbour caps inside the 44 + chosen labels
            order = sorted(sel)
            labs = list(LABELS) + [new[i] for i in order]
            nn = 44 + len(order)
            A = np.zeros((nn, nn), dtype=np.int64)
            A[:44, :44] = gamma
            for a, i in enumerate(order, 44):
                nb = D[i][sel[i]]['neighbours']
                A[a, nb] = A[nb, a] = 1
            for a, b in combinations(range(len(order)), 2):
                i, j = order[a], order[b]
                A[44 + a, 44 + b] = A[44 + b, 44 + a] = pair(i, sel[i], j, sel[j])[0]
            if np.any(A.sum(axis=1) > 12):
                return False
            inc_ = np.array([[int(r in p) for p in labs] for r in range(14)], dtype=np.int64)
            tot = A @ A + A + inc_.T @ inc_
            np.fill_diagonal(tot, 0)
            return not np.any(tot > 2)

        def visit(possible, sel):
            if time.monotonic() > deadline:
                return
            nodes[0] += 1
            if len(sel) == 16:
                order = sorted(sel)
                R = [[coords[i][sel[i]][2] if i == j else pair(i, sel[i], j, sel[j])[1] for j in order] for i in order]
                psd, rank, _ = exact_psd(R)
                if psd and rank <= resid_target:
                    sols.append(dict(sel))
                return
            v = min((i for i in range(16) if i not in sel), key=lambda i: len(possible[i]))
            for a in possible[v]:
                sel[v] = a
                if not graph_ok(sel):
                    del sel[v]
                    continue
                rem = [list(x) for x in possible]
                ok = True
                for j in range(16):
                    if j in sel:
                        continue
                    rem[j] = [b for b in possible[j] if pair(v, a, j, b) is not None]
                    if not rem[j]:
                        ok = False
                        break
                if ok:
                    visit(rem, sel)
                del sel[v]
                if len(sols) >= 50:
                    return

        visit([list(range(len(d))) for d in D], {})
        exhaustive = time.monotonic() <= deadline and len(sols) < 50
        entry.update(status=('ASSEMBLIES_FOUND' if sols else ('NO_ASSEMBLY' if exhaustive else 'TIME_LIMIT')),
                     exhaustive=exhaustive, nodes=nodes[0], domain_sizes=[len(d) for d in D], n_solutions=len(sols))
        built = []
        for s in sols[:20]:
            order = sorted(s)
            labs = list(LABELS) + [new[i] for i in order]
            nn = 60
            A = np.zeros((nn, nn), dtype=np.int64)
            A[:44, :44] = gamma
            for a, i in enumerate(order, 44):
                nb = D[i][s[i]]['neighbours']
                A[a, nb] = A[nb, a] = 1
            for a, b in combinations(range(16), 2):
                i, j = order[a], order[b]
                A[44 + a, 44 + b] = A[44 + b, 44 + a] = pair(i, s[i], j, s[j])[0]
            built.append(dict(labels=[list(p) for p in labs],
                              edges=[[i, j] for i in range(nn) for j in range(i + 1, nn) if A[i, j]]))
        entry['assemblies'] = built
        report['lines'][str(n)] = entry
        print(n, entry['status'], 'domains', entry['domain_sizes'], 'nodes', nodes[0], 'solutions', len(sols), pred,
              flush=True)
    report['seconds'] = time.monotonic() - t0
    Path(out).write_text(json.dumps(report, indent=1) + '\n', encoding='utf-8')
    print('done in %.1f s' % report['seconds'], flush=True)


if __name__ == '__main__':
    main()
