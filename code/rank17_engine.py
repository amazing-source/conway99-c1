r"""Rank-17 pass-1 engine for the non-Z17 V (C1, 28/09 night): skeleton enumeration (rank17_skeleton filters) + vector level
through structures' compiled general-V solver (conway99-rank17 z17/sbdfs_g.exe, spec SPEC_ENGINE.md).
Per (V, y-pair): norm-10 vectors of K -> usable classes -> skeletons (all of them, one by one) -> per skeleton the 21 cell
domains per SPEC section 1 (w+ != +-w-, (w+, w-) in {0, +-4}, M1 orientation p((w+ + w-)/2) = eps_c, refined L1, sign
normalisation of a_12, b_12, b_1d) in V coordinates -> sbdfs_g.exe (pairwise rule, star closure, PSD, exact leaf).
Verdicts per y-pair: EXCLUDED (every skeleton excluded; 'no skeleton' included), FOUND, LIMIT (skeleton or node cap).
Pass-1 label: COMPUTED if exhaustive over the skeletons, else PATTERN. Refined L1 is structures' lemma (not re-derived here).
Usage: python rank17_engine.py <K tag> <pair ids comma-separated|all> [max_skeletons] [solver node cap]"""
import json, os, sys, time, itertools
from fractions import Fraction as Fr
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rank17_skeleton as sk
from rank17_ypairs import short_vectors_chunked
from rank17_K import v_basis, solve_coeffs
from rank17_vsearch import CELLS, pat
sys.path.insert(0, 'C:/home/researcher/Desktop/conway99-rank17/z17')
import stageB

DATA = sk.DATA
WORK = 'C:/home/researcher/AppData/Local/Temp/claude/runs/r17eng'


def canon_mod1(p):
    """p = (p_2..p_7) with p_1 = 0 implicit: already canonical (bit 1 clear)"""
    return tuple(int(x) for x in p)


def eps(c):
    return tuple([1] * 6) if c == 1 else tuple(int(k == c) for k in range(2, 8))


def first_pos(v):
    nz = np.flatnonzero(v)
    return len(nz) == 0 or v[nz[0]] > 0


class Case:
    def __init__(self, tag, pid):
        K = json.load(open(os.path.join(DATA, 'K_%s.json' % tag)))
        self.V = K['V']
        rec_ = [r for r in K['K'] if r['id'] == pid][0]
        self.pid = pid
        B, dim, m = v_basis(K['core'])
        self.m = m
        self.Gv = np.array([[int(sum(a * b for a, b in zip(u, v))) for v in B] for u in B], dtype=np.int64)
        self.GK = np.array(rec_['K_gram'], dtype=np.int64)
        self.Kv = np.array([solve_coeffs(B, [Fr(x) for x in row]) for row in rec_['K_basis']], dtype=np.int64)
        assert np.array_equal(self.Kv @ self.Gv @ self.Kv.T, self.GK)
        self.nB = len(B)
        # M = G Bw, Bw = G-orthonormal basis of W in V coordinates
        L = np.linalg.cholesky(self.GK.astype(float))
        O = np.linalg.solve(L, self.Kv.astype(float))                     # rows orthonormal for G
        self.M = self.Gv.astype(float) @ O.T                              # 17 x 15
        # roots of V (V coordinates, both signs) for refined L1
        X, nrm = short_vectors_chunked(self.Gv.tolist(), 2)
        R = X[nrm == 2].astype(np.int64)
        self.roots = np.vstack([R, -R])
        self.rootkeys4 = sk.root_keys_mod4(self.Gv)
        rk2 = {}
        for r in self.roots:
            rk2.setdefault(((r % 2) << np.arange(self.nB)).sum(), []).append(r)
        self.roots_mod2 = rk2
        # skeleton-level data (the norm-10 shell is enumerated once; int16 storage)
        Xk, nk = short_vectors_chunked(self.GK.tolist(), 10)
        W = Xk[nk == 10].astype(np.int16)
        del Xk, nk
        self.usable, self.info, self.masks = sk.usable_classes(self.GK, self.Kv, self.rootkeys4, W10=W)
        self.duals = sk.short_duals(self.GK)
        KG = self.Kv @ self.Gv
        self.units = [KG[:, self.nB - m + j].copy() for j in range(m)]
        self.W = W
        self.cls = ((W.astype(np.int64) & 1) << np.arange(15)).sum(axis=1)

    def pvec(self, x_v, gvecs):
        """p(x) = ((x, g_e))_e mod 2 for x in V coordinates, g_e class representatives in V coordinates"""
        return tuple(int(v) for v in ((x_v @ self.Gv @ gvecs.T) % 2))

    def class_data(self, C):
        """cached per class: oriented signed records (w+, w-) with w+ != +-w-, (w+, w-) in {0, +-4} (all 8 sign/order
        variants of each unordered pair), a = (w+ + w-)/2, b = (w+ - w-)/2, the index of the unsigned w behind w+ / w-,
        and for refined L1 the vectors v = (r - w)/2 (r a root of V, r = w mod 2V) with their owner index"""
        if not hasattr(self, '_cd'):
            self._cd = {}
        if C in self._cd:
            d = self._cd.pop(C); self._cd[C] = d                            # LRU order
            return d
        while len(self._cd) >= 64:                                          # memory: keep at most 64 classes
            self._cd.pop(next(iter(self._cd)))
        Wc = self.W[self.cls == C].astype(np.int64) @ self.Kv               # V coordinates, up to sign
        n = len(Wc)
        ip = Wc @ self.Gv @ Wc.T
        iu = np.triu_indices(n, 1)
        sel = np.isin(ip[iu], (0, 4, -4))
        I, J = iu[0][sel], iu[1][sel]
        Ps, Ms, iP, iM = [], [], [], []
        for sp in (1, -1):
            for sm in (1, -1):
                Ps.append(sp * Wc[I]); Ms.append(sm * Wc[J]); iP.append(I); iM.append(J)
                Ps.append(sm * Wc[J]); Ms.append(sp * Wc[I]); iP.append(J); iM.append(I)
        P = np.vstack(Ps) if len(I) else np.zeros((0, self.nB), dtype=np.int64)
        Mn = np.vstack(Ms) if len(I) else np.zeros((0, self.nB), dtype=np.int64)
        iP = np.concatenate(iP) if len(I) else np.zeros(0, dtype=np.int64)
        iM = np.concatenate(iM) if len(I) else np.zeros(0, dtype=np.int64)
        A = (P + Mn) // 2; Bv = (P - Mn) // 2
        vs, owner = [], []
        pw = 1 << np.arange(self.nB)
        for k, w in enumerate(Wc):
            key = int(((w % 2) * pw).sum())
            for r in self.roots_mod2.get(key, []):
                vs.append((r - w) // 2); owner.append(k)
        Vv = np.array(vs, dtype=np.int64).reshape(-1, self.nB)
        d = {'n': n, 'P': P, 'Mn': Mn, 'A': A, 'B': Bv, 'iP': iP, 'iM': iM, 'V': Vv,
             'owner': np.array(owner, dtype=np.int64)}
        self._cd[C] = d
        return d

    def domains(self, skel):
        """the 21 domains per SPEC section 1, in V coordinates (P = w+, Mn = w-), vectorised on cached class data"""
        gv = np.array([((np.array([(g >> i) & 1 for i in range(15)], dtype=np.int64)) @ self.Kv) for g in skel])
        GG = self.Gv @ gv.T                                                  # 17 x 6
        doms = []
        for (c, d) in CELLS:
            C = skel[d - 2] if c == 1 else skel[c - 2] ^ skel[d - 2]
            cd = self.class_data(C)
            if len(cd['P']) == 0:
                doms.append((cd['P'], cd['Mn'])); continue
            pa = (cd['A'] @ GG) % 2
            keep = (pa == np.array(eps(c))).all(axis=1)                        # M1
            # refined L1: w bad if some v = (r - w)/2 has p(v) in {0, eps_c, eps_d, eps_c + eps_d} (mod complement)
            bad_w = np.zeros(cd['n'], dtype=bool)
            if len(cd['V']):
                pv = (cd['V'] @ GG) % 2
                ec, ed = np.array(eps(c)), np.array(eps(d))
                allowed = [np.zeros(6, dtype=np.int64), ec, ed, (ec + ed) % 2]
                hit = np.zeros(len(pv), dtype=bool)
                for q in allowed:
                    hit |= (pv == q).all(axis=1) | (pv == (1 - q)).all(axis=1)
                bad_w[cd['owner'][hit]] = True
            keep &= ~bad_w[cd['iP']] & ~bad_w[cd['iM']]
            # sign normalisation: a_12, b_12, b_1d (d >= 3) with a positive first non-zero coordinate
            def fp(X):
                nz = X != 0
                has = nz.any(axis=1)
                first = X[np.arange(len(X)), nz.argmax(axis=1)]
                return ~has | (first > 0)
            if (c, d) == (1, 2):
                keep &= fp(cd['A']) & fp(cd['B'])
            elif c == 1:
                keep &= fp(cd['B'])
            P, Mn = cd['P'][keep], cd['Mn'][keep]
            if len(P):
                _, first = np.unique(np.hstack([P, Mn]), axis=0, return_index=True)
                P, Mn = P[np.sort(first)], Mn[np.sort(first)]
            doms.append((P, Mn))
        return doms


def run_case(tag, pid, max_skel=200, cap=10 ** 7, sample=0):
    """sample = 0: skeletons enumerated exhaustively (H-reduced) up to max_skel; sample = N > 0: N random skeletons
    (randomised DFS order, one per seed), PATTERN mode"""
    os.makedirs(WORK, exist_ok=True)
    t0 = time.time()
    case = Case(tag, pid)
    out = {'V': case.V, 'pair': pid, 'usable': len(case.usable), 'mode': 'sample %d' % sample if sample else 'exhaustive'}
    if sample:
        lst, none_exhaustive = [], False
        for seed in range(sample):
            try:
                r, nodes, rej = sk.skeleton_exists(case.usable, case.GK, limit=2 * 10 ** 6, duals=case.duals,
                                                   units=case.units, masks=case.masks, perm_seed=seed)
            except TimeoutError:
                continue                                                    # this random order hit the node cap
            if r is None:
                none_exhaustive = True                                      # a complete search found no skeleton
                break
            if r not in lst:
                lst.append(r)
        sks = {'list': lst, 'exhaustive': none_exhaustive}
    else:
        orbits = sk.root_orbits(case.GK, list(case.usable.keys()))
        out['class_orbits'] = len(set(orbits.values()))
        sks = sk.all_skeletons(case.usable, case.GK, duals=case.duals, units=case.units, masks=case.masks,
                               max_count=max_skel, orbits=orbits)
    out['skeletons'] = len(sks['list']); out['skeleton_search_exhaustive'] = sks['exhaustive']
    verdicts = {}
    for n, S in enumerate(sks['list']):
        doms = case.domains(S)
        empty = [str(CELLS[i]) for i, (P, _) in enumerate(doms) if len(P) == 0]
        if empty:
            verdicts[n] = 'EXCLUDED empty-cell ' + empty[0]
            continue
        path = os.path.join(WORK, '%s_%d_%d.bin' % (tag, pid, n))
        stageB.export_g(path, cap, case.Gv, case.M, doms)
        r = stageB.solve_g(path)
        os.remove(path)
        verdicts[n] = '%s %d' % (r['verdict'], r['nodes'])
        if r['verdict'] in ('FOUND', 'LIMIT'):
            out['stop'] = {'skeleton': S, 'verdict': r['verdict'], 'solver': r}
            break
    out['verdicts'] = verdicts
    kinds = {}
    for v in verdicts.values():
        k = v.split()[0] + (' empty' if 'empty' in v else '')
        kinds[k] = kinds.get(k, 0) + 1
    out['summary'] = kinds
    if 'stop' in out:
        out['verdict'] = out['stop']['verdict']
    elif sks['exhaustive']:
        out['verdict'] = 'EXCLUDED'
        out['label'] = 'COMPUTED (pass 1: all skeletons excluded)' if sks['list'] else 'COMPUTED (pass 1: no skeleton)'
    elif sample and not sks['list']:
        out['verdict'] = 'UNDECIDED'
        out['label'] = 'every random skeleton search hit the node cap'
    elif not sks['list']:
        out['verdict'] = 'UNDECIDED'
        out['label'] = 'skeleton search hit the node cap before finding any skeleton (not exhaustive)'
    else:
        out['verdict'] = 'PARTIAL'
        out['label'] = ('PATTERN (%d random skeletons, all excluded)' % len(sks['list']) if sample else
                        'PATTERN (skeleton cap %d or node cap reached, all tried excluded)' % max_skel)
    out['s'] = round(time.time() - t0, 1)
    return out


if __name__ == '__main__':
    tag = sys.argv[1]
    ids = sys.argv[2]
    ms = int(sys.argv[3]) if len(sys.argv) > 3 else 200
    cap = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 7
    smp = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    Y = json.load(open(os.path.join(DATA, 'ypairs_%s.json' % tag)))
    pids = [p['id'] for p in Y['pairs']] if ids == 'all' else [int(x) for x in ids.split(',')]
    outf = os.path.join(DATA, 'engine_%s.jsonl' % tag)
    for pid in pids:
        o = run_case(tag, pid, ms, cap, smp)
        print(json.dumps({k: v for k, v in o.items() if k != 'verdicts'}), flush=True)
        with open(outf, 'a') as f:
            f.write(json.dumps(o) + chr(10))
