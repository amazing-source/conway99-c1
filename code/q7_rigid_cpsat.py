"""CP-SAT model of the 'all far rows rigid' regime (g = 18, t = 0 split blocks): one option (Phi(z), Phi(sigma z)) per far
orbit among those with Z_ff = 0; (i) each non-mu pair once; (ii), (iii); pairwise: x_{f,a} => OR of the options a' of f'
with Z(a, a') in {0, +-1} (for every f' != f); row counts: x_{f,a} => sum_{f'} [Z(a, chosen a') = +-1] = 10 - |supp s_f|.
python q7_rigid_cpsat.py IDX [TIME_LIMIT] [WORKERS]"""
import sys, time, itertools
import numpy as np
from ortools.sat.python import cp_model
from q7_g16_test import classes_t_ge, ball_disc, split, K2, K3, L, FAR, P7
from q7_rigid_ac import prep


def solve_class(tau, eta, tl=240, workers=1, pairwise=True, rowcount=True):
    opts, comp, nzm, need = prep(tau, eta)
    n = len(opts)
    if any(len(o) == 0 for o in opts):
        return 'dead-unary', 0.0
    k2, k3 = K2(tau, eta), K3(tau, eta)
    m = cp_model.CpModel()
    x = [[m.NewBoolVar('x%d_%d' % (f, j)) for j in range(len(opts[f]))] for f in range(n)]
    for f in range(n):
        m.AddExactlyOne(x[f])
    nonmu = [e for e in itertools.combinations(L, 2) if tau[e[0]] != e[1]]
    use = {e: [] for e in nonmu}
    acc2, acc3 = {}, {}
    for f in range(n):
        z, sz = FAR[f]
        for j, (e, e2) in enumerate(opts[f]):
            v = x[f][j]
            use[e].append(v); use[e2].append(v)
            for a in z:
                for b in e:
                    acc2.setdefault((a, b), []).append(v)
            for a in sz:
                for b in e2:
                    acc2.setdefault((a, b), []).append(v)
            for b in e:
                for d in e2:
                    acc3.setdefault((b, d), []).append(v)
            for b in e2:
                for d in e:
                    acc3.setdefault((b, d), []).append(v)
    for e in nonmu:
        m.AddExactlyOne(use[e])
    for a in L:
        for b in L:
            m.Add(sum(acc2.get((a, b), [])) == int(k2[a, b]))
            m.Add(sum(acc3.get((a, b), [])) == int(k3[a, b]))
    if pairwise:
        for f in range(n):
            for g in range(n):
                if g <= f:
                    continue
                C = comp[(f, g)]
                # forbidden pairs as binary clauses would be too many; use support clauses both ways
                for j in range(len(opts[f])):
                    sup = [x[g][k] for k in np.nonzero(C[j])[0]]
                    m.AddBoolOr(sup + [x[f][j].Not()])
                for k in range(len(opts[g])):
                    sup = [x[f][j] for j in np.nonzero(C[:, k])[0]]
                    m.AddBoolOr(sup + [x[g][k].Not()])
    if rowcount:
        # t_{f,g} = 1 iff the chosen options of f and g have Z = +-1
        tv = {}
        for f in range(n):
            for g in range(f + 1, n):
                NZ = nzm[(f, g)]
                t = m.NewBoolVar('t%d_%d' % (f, g))
                # t >= x_fj + x_gk - 1 for NZ pairs; t <= sum over NZ pairs of ... (use: t == OR over chosen) via
                # t = sum_j x_fj * [any chosen g-option nonzero with j]: linearize with y_{f,j,g} = x_fj AND (sum_k NZ x_gk)
                sj = []
                for j in range(len(opts[f])):
                    ks = np.nonzero(NZ[j])[0]
                    if len(ks) == 0:
                        continue
                    y = m.NewBoolVar('')
                    m.AddImplication(y, x[f][j])
                    m.Add(sum(x[g][k] for k in ks) >= 1).OnlyEnforceIf(y)
                    m.Add(sum(x[g][k] for k in ks) == 0).OnlyEnforceIf([x[f][j], y.Not()])
                    sj.append(y)
                m.Add(t == sum(sj))
                tv[(f, g)] = tv[(g, f)] = t
        for f in range(n):
            row = [tv[(f, g)] for g in range(n) if g != f]
            for j in range(len(opts[f])):
                m.Add(sum(row) == int(need[f][j])).OnlyEnforceIf(x[f][j])
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tl
    s.parameters.num_workers = workers
    t0 = time.time()
    st = s.Solve(m)
    return s.StatusName(st), time.time() - t0


if __name__ == '__main__':
    idx = int(sys.argv[1])
    tl = float(sys.argv[2]) if len(sys.argv) > 2 else 240
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    cls = [c for c in classes_t_ge(0) if c[2] == 0]
    cls = [c for c in cls if split(*ball_disc(c[0], c[1]))]
    tau, eta, t, osz = cls[idx]
    print('class', idx, tau, eta, flush=True)
    rc = '--rowcount' in sys.argv
    print(solve_class(tau, eta, tl=tl, workers=workers, pairwise=True, rowcount=rc), flush=True)
