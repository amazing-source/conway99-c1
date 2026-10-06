"""Sample admissible configurations of O_x (the 10 outside neighbours of x: 6 Bx, 4 Zx) for a fixed core and hole set,
then apply the class-minimum test to the 37-vertex seed core + O_x (adjacency fully known: core, columns, matching).

O_x constraints used (all necessary):
  * columns: grid neighbour x, local rules, hole rule (positive degree), q-label by slot;
  * x-fiber pair counts exact: sum_{u in O_x} [l in b_u] = M[x,l] for every core label l;
  * label pair caps: sum_{u in O_x} [l,l' in b_u] <= M[l,l'];
  * N(x) is a perfect matching: O_x carries 5 matched pairs (4 Zx-Bx, 1 Bx-Bx); matched pairs have b_u cap b_u' = {x};
    unmatched pairs share at most one core label;
  * for l in core, u in O_x: common neighbours of (l,u) inside the seed <= lambda/mu.
"""
import json, sys, random, itertools, time
import numpy as np
from ortools.sat.python import cp_model
from bstage import gen_columns, target_matrix, pdeg, QCORE, P13, T
from seedcvp import class_min_violation

LAB = T + P13


def sample(core, holes, nsamp, seed=0, tl=60):
    A = np.array(core["adj"]); M = target_matrix(A)
    cols = gen_columns(A, set(tuple(p) for p in core["defect"]))
    cand = {1: [], 0: []}
    for b, q in cols:
        if b[0] != 0:
            continue
        p13 = [v for v in b if v in P13]
        if sum(1 for v in p13 if v not in holes) > pdeg(0, q):
            continue
        cand[q].append(b)
    slots = [1] * 6 + [0] * 4
    rng = random.Random(seed)
    out = []
    nb = [set(np.nonzero(A[i])[0]) for i in range(27)]
    for it in range(nsamp):
        m = cp_model.CpModel()
        X = [[m.NewBoolVar(f"x{s}_{c}") for c in range(len(cand[slots[s]]))] for s in range(10)]
        for s in range(10):
            m.AddExactlyOne(X[s])
        inl = lambda s, l: sum(X[s][c] for c, b in enumerate(cand[slots[s]]) if l in b)
        # matching variables
        Mt = {}
        for s, t in itertools.combinations(range(10), 2):
            if slots[s] == 0 and slots[t] == 0:
                continue
            Mt[(s, t)] = m.NewBoolVar(f"m{s}_{t}")
        for s in range(10):
            m.AddExactlyOne([v for (a, b), v in Mt.items() if s in (a, b)])
        m.Add(sum(v for (a, b), v in Mt.items() if slots[a] == 1 and slots[b] == 1) == 1)
        # symmetry: order slots within groups by chosen column index
        ci = [m.NewIntVar(0, len(cand[slots[s]]) - 1, f"ci{s}") for s in range(10)]
        for s in range(10):
            m.Add(ci[s] == sum(c * X[s][c] for c in range(len(cand[slots[s]]))))
        for s in range(5):
            m.Add(ci[s] <= ci[s + 1])
        for s in range(6, 9):
            m.Add(ci[s] <= ci[s + 1])
        for l in LAB:
            m.Add(sum(inl(s, l) for s in range(10)) == int(M[0, l]))
        for l, l2 in itertools.combinations(LAB, 2):
            terms = []
            for s in range(10):
                cs = [c for c, b in enumerate(cand[slots[s]]) if l in b and l2 in b]
                if cs:
                    terms.append(sum(X[s][c] for c in cs))
            if terms:
                m.Add(sum(terms) <= int(M[l, l2]))
        # pair rules between slots: shared labels
        for s, t in itertools.combinations(range(10), 2):
            for l in LAB:
                pass
            sh = {}
            for l in LAB:
                a = m.NewBoolVar(""); m.AddMultiplicationEquality(a, [inl(s, l), inl(t, l)]) if False else None
            # shared label count via pairwise column compatibility (cheap enough: forbid incompatible column pairs)
        # forbid incompatible column pairs with table constraints
        for s, t in itertools.combinations(range(10), 2):
            Cs, Ct = cand[slots[s]], cand[slots[t]]
            mv = Mt.get((s, t))
            # unmatched: share <= 1 label ; matched: share 0 labels
            for c1, b1 in enumerate(Cs):
                s1 = set(b1[1:])
                for c2, b2 in enumerate(Ct):
                    sh = len(s1 & set(b2[1:]))
                    if sh >= 2:
                        m.AddBoolOr([X[s][c1].Not(), X[t][c2].Not()])
                    elif sh == 1 and mv is not None:
                        m.AddBoolOr([X[s][c1].Not(), X[t][c2].Not(), mv.Not()])
            if len(Cs) * len(Ct) > 3_000_000:
                raise RuntimeError("too many pairs")
        m.Maximize(sum(rng.randint(0, 1000) * X[s][c] for s in range(10) for c in range(len(cand[slots[s]]))))
        sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tl; sol.parameters.num_workers = 2
        sol.parameters.random_seed = rng.randint(0, 10**6)
        st = sol.Solve(m)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            out.append(None); continue
        bs = [cand[slots[s]][next(c for c in range(len(cand[slots[s]])) if sol.Value(X[s][c]))] for s in range(10)]
        match = [k for k, v in Mt.items() if sol.Value(v)]
        out.append((bs, match))
    return out


def seed_matrix(core, holes, bs, match):
    A = np.array(core["adj"])
    n = 37
    S = np.zeros((n, n), dtype=np.int64); S[:27, :27] = A
    for s, b in enumerate(bs):
        for v in b:
            S[27 + s, v] = S[v, 27 + s] = 1
    for a, b in match:
        S[27 + a, 27 + b] = S[27 + b, 27 + a] = 1
    q = [-1, -1, 1, 1, 1, 1, 1, 1] + [0] * 6 + [0 if v in holes else 1 for v in P13] + [1] * 6 + [0] * 4
    return S, q


def lam_mu_ok(S):
    C2 = S @ S
    n = S.shape[0]
    for i in range(n):
        for j in range(i + 1, n):
            if C2[i, j] > (1 if S[i, j] else 2):
                return False
    return True


if __name__ == "__main__":
    cores = json.load(open("cores27.json"))
    k = int(sys.argv[1]); holes = [int(v) for v in sys.argv[2].split(",")]; ns = int(sys.argv[3])
    t = time.time()
    res = sample(cores[k], holes, ns, seed=int(sys.argv[4]) if len(sys.argv) > 4 else 0)
    stats = {"none": 0, "lammu_bad": 0, "killed": 0, "alive": 0}
    for r in res:
        if r is None:
            stats["none"] += 1; continue
        S, q = seed_matrix(cores[k], holes, *r)
        if not lam_mu_ok(S):
            stats["lammu_bad"] += 1; continue
        bad = class_min_violation(S, q)
        if bad:
            stats["killed"] += 1
        else:
            stats["alive"] += 1
        print(r[1], bad, flush=True)
    print(stats, round(time.time() - t, 1))
