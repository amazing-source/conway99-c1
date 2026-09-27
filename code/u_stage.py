r"""Finish line (C), C1 27/09: u-stage given (h_1..h_7, y_1, y_2) on an explicit envelope U.  Exact CP-SAT (PROVEN conditions):
  cells: for each pair {c,d} (c < d) and t = +-1, exactly one u with (u,h_c)(u,h_d) = t, |(u,h_c)| = |(u,h_d)| = 1,
         (u,h_e) = 0 for e not in {c,d}, (u,y_1) = (u,y_2) = 0;
  frame identity in integer coordinates (basis B, Gram G, U unimodular so G^-1 integral):
         sum_u a_u^T a_u = 7 G^-1 - sum_h a_h^T a_h - sum_y a_y^T a_y          (300 equations; implies the star sums L7);
  conflicts: two chosen u have |(u,u')| <= 1;
  degree: every chosen u has exactly 10 chosen neighbours with |(u,u')| = 1  (T has 10 nonzeros per row);
  new roots: a u hits beta at 3/2 only if beta in B1 minus hits(y1, y2), and each such beta is hit by exactly one u.
Returns 'INFEASIBLE' / 'FEASIBLE' / 'UNKNOWN'."""
import numpy as np


def u_stage(Bq, Gi, X3, X3c, hs_c, ys_c, S, B1_idx, time_limit=60):
    from ortools.sat.python import cp_model
    Bf = np.array([[float(v) for v in row] for row in Bq])
    Gz = np.array(Gi, dtype=np.int64)
    Ginv = np.rint(np.linalg.inv(Gz.astype(float))).astype(np.int64)
    assert np.array_equal(Gz @ Ginv, np.eye(24, dtype=np.int64))
    H = np.array(hs_c, dtype=np.int64); Y = np.array(ys_c, dtype=np.int64)
    Hf = H.astype(float) @ Bf; Yf = Y.astype(float) @ Bf
    IPh = np.rint(X3 @ Hf.T).astype(np.int64)
    IPy = np.rint(X3 @ Yf.T).astype(np.int64)
    perp = (IPy == 0).all(axis=1)
    hitS = np.abs(np.abs(X3 @ S.T) - 1.5) < 1e-6
    yhit = (np.abs(np.abs(Yf @ S.T) - 1.5) < 1e-6).any(axis=0)
    allowed_hit = np.zeros(S.shape[0], bool); allowed_hit[list(B1_idx)] = True; allowed_hit &= ~yhit
    okhit = ~(hitS & ~allowed_hit).any(axis=1)
    nz = IPh != 0
    cells = {}
    for c in range(7):
        for d in range(c + 1, 7):
            base = perp & okhit & (nz.sum(axis=1) == 2) & nz[:, c] & nz[:, d] & (np.abs(IPh[:, c]) == 1) & (np.abs(IPh[:, d]) == 1)
            prod = IPh[:, c] * IPh[:, d]
            for t in (1, -1):
                idx = np.nonzero(base & (prod == t))[0]
                if len(idx) == 0:
                    return 'INFEASIBLE', {'empty_cell': (c, d, t)}
                cells[(c, d, t)] = idx
    m = cp_model.CpModel()
    var = {}
    for key, idx in cells.items():
        vs = []
        for x in idx:
            v = m.NewBoolVar('')
            var[(key, int(x))] = v
            vs.append(v)
        m.AddExactlyOne(vs)
    items = list(var.items())
    # frame identity
    RHS = 7 * Ginv - H.T @ H - Y.T @ Y
    for i in range(24):
        for j in range(i, 24):
            terms = []
            for (key, x), v in items:
                coef = int(X3c[x, i] * X3c[x, j])
                if coef:
                    terms.append(coef * v)
            m.Add(sum(terms) == int(RHS[i, j]))
    # conflicts and degree
    xs = np.array([x for (key, x), v in items])
    vv = [v for (key, x), v in items]
    Pm = np.rint(X3[xs] @ X3[xs].T).astype(np.int64)
    n = len(xs)
    for a in range(n):
        nb = []
        for b in range(n):
            if a == b:
                continue
            p = abs(Pm[a, b])
            if p >= 2:
                if a < b:
                    m.AddBoolOr([vv[a].Not(), vv[b].Not()])
            elif p == 1:
                nb.append(vv[b])
        m.Add(sum(nb) == 10).OnlyEnforceIf(vv[a])
    # each allowed new root (B1 minus y-hits) hit by exactly one u
    for bidx in np.nonzero(allowed_hit)[0]:
        hv = [v for (key, x), v in items if hitS[x, bidx]]
        m.Add(sum(hv) == 1)
    sol = cp_model.CpSolver()
    sol.parameters.max_time_in_seconds = time_limit
    sol.parameters.num_workers = 1
    st = sol.Solve(m)
    name = {cp_model.INFEASIBLE: 'INFEASIBLE', cp_model.FEASIBLE: 'FEASIBLE', cp_model.OPTIMAL: 'FEASIBLE'}.get(st, 'UNKNOWN')
    return name, {'cells_min': min(len(v) for v in cells.values()), 'vars': n}
