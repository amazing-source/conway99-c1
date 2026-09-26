"""'All far rows rigid' regime (g = 18 with t = 0; g = 16 with t = 2): T_FF = Z (mod 7) on the 30 far orbits.
Propagation before any solver, on the options surviving the unary filters:
  (P1) arc consistency: option a of f needs, in every other orbit f', an alive option a' with Z(a, a') in {0, +-1};
  (P2) row counts: #{f' : T_ff' != 0} = 10 - |supp s_f|; for option a: (#orbits f' whose alive compatible options all
       have Z != 0) <= need <= (#orbits f' having an alive compatible option with Z != 0);
  (P3) (i) as a matching: every non-mu pair must still be coverable, and an orbit whose options all use a pair e removes e
       from the others (unit propagation on 'each non-mu pair used exactly once').
Then CP-SAT on what is left (optional).  python q7_rigid_ac.py START END [TCAP] (t = 0 split classes, g = 18)."""
import sys, json, time, itertools
import numpy as np
from q7_g16_test import classes_t_ge, ball_disc, split, unary_filter, ball, ginv_sym, L, P7, FAR


def prep(tau, eta, regime_t2=True):
    t, res, Pp = unary_filter(tau, eta, regime_t2=regime_t2)
    opts = [r[0] for r in res]
    X = [r[1] for r in res]
    n = len(res)
    comp, nzm = {}, {}
    for f in range(n):
        for g in range(n):
            if f == g or len(opts[f]) == 0 or len(opts[g]) == 0:
                continue
            Zm = (X[f].T @ ((Pp @ X[g]) % P7)) % P7
            comp[(f, g)] = (Zm == 0) | (Zm == 1) | (Zm == 6)
            nzm[(f, g)] = (Zm == 1) | (Zm == 6)
    need = [np.array([10 - len(set(e) ^ set(e2)) for (e, e2) in opts[f]], dtype=np.int64) for f in range(n)]
    return opts, comp, nzm, need


def propagate(opts, comp, nzm, need, tau, max_rounds=200):
    n = len(opts)
    alive = [np.ones(len(opts[f]), dtype=bool) for f in range(n)]
    if any(len(o) == 0 for o in opts):
        return alive, 'wipeout-unary'
    nonmu = [e for e in itertools.combinations(L, 2) if tau[e[0]] != e[1]]
    uses = {}
    for f in range(n):
        for j, (e, e2) in enumerate(opts[f]):
            uses.setdefault(e, []).append((f, j))
            uses.setdefault(e2, []).append((f, j))
    for rnd in range(max_rounds):
        changed = False
        for f in range(n):
            if not alive[f].any():
                return alive, 'wipeout'
            a = alive[f].copy()
            forced = np.zeros(len(a), dtype=np.int64)
            possible = np.zeros(len(a), dtype=np.int64)
            for g in range(n):
                if g == f:
                    continue
                C = comp[(f, g)][:, alive[g]]
                NZ = nzm[(f, g)][:, alive[g]]
                a &= C.any(axis=1)
                has_nz = NZ.any(axis=1)
                all_nz = (C == NZ).all(axis=1) & C.any(axis=1)       # every compatible alive option is nonzero
                possible += has_nz
                forced += all_nz
            a &= (forced <= need[f]) & (need[f] <= possible)
            if (a != alive[f]).any():
                alive[f] = a
                changed = True
            if not alive[f].any():
                return alive, 'wipeout'
        # (P3) matching unit propagation on non-mu pairs
        for e in nonmu:
            live = [(f, j) for (f, j) in uses.get(e, []) if alive[f][j]]
            if not live:
                return alive, 'wipeout-pair'
            owners = {f for f, _ in live}
            if len(owners) == 1:
                f0 = next(iter(owners))
                # orbit f0 is the only one that can cover e: it must use e
                mask = np.array([(e in (o[0], o[1])) for o in opts[f0]])
                a = alive[f0] & mask
                if (a != alive[f0]).any():
                    alive[f0] = a
                    changed = True
        for f in range(n):
            live_opts = np.nonzero(alive[f])[0]
            common = None
            for j in live_opts:
                s = {opts[f][j][0], opts[f][j][1]}
                common = s if common is None else common & s
            for e in (common or ()):
                for (g, j) in uses.get(e, []):
                    if g != f and alive[g][j]:
                        alive[g][j] = False
                        changed = True
        if not changed:
            break
    return alive, 'stable'


if __name__ == '__main__':
    start, end = int(sys.argv[1]), int(sys.argv[2])
    tcap = float(sys.argv[3]) if len(sys.argv) > 3 else 270
    t0 = time.time()
    cls = [c for c in classes_t_ge(0) if c[2] == 0]
    cls = [c for c in cls if split(*ball_disc(c[0], c[1]))]
    out = []
    for idx in range(start, min(end, len(cls))):
        if time.time() - t0 > tcap:
            print('TIME CAP at', idx, flush=True); break
        tau, eta, t, osz = cls[idx]
        opts, comp, nzm, need = prep(tau, eta)
        alive, st = propagate(opts, comp, nzm, need, tau)
        sizes = [int(a.sum()) for a in alive]
        print(idx, st, 'domain sizes after propagation:', sizes if st == 'stable' else '', '(%.0fs)' % (time.time() - t0),
              flush=True)
        out.append({'idx': idx, 'status': st, 'sizes': sizes})
    json.dump(out, open('g18_t0_ac_%d_%d.json' % (start, end), 'w'))
