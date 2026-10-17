"""CP-SAT model: choose candidate lines (plus fixed lines) so that the collinearity graph is srg(243,22,1,2).
All lines are affine lines of AG(5,3) so that two points lie on at most one candidate line."""
import itertools, time, numpy as np
from ortools.sat.python import cp_model
from lines_model import *

def build(fixed, cands, n=243, k_lines=11, forbid=()):
    m = cp_model.CpModel()
    fixed = set(map(tuple, fixed)); cands = [tuple(c) for c in cands if tuple(c) not in fixed]
    x = {c: m.NewBoolVar("") for c in cands}
    on = [[] for _ in range(n)]; fixed_on = [0] * n
    E = {}
    for c in cands:
        for p in c: on[p].append(x[c])
        for a, b in itertools.combinations(c, 2):
            assert (a, b) not in E, "two lines through a pair"
            E[(a, b)] = E[(b, a)] = x[c]
    for c in fixed:
        for p in c: fixed_on[p] += 1
        for a, b in itertools.combinations(c, 2):
            assert (a, b) not in E
            E[(a, b)] = E[(b, a)] = True
    for p in range(n):
        m.Add(sum(on[p]) == k_lines - fixed_on[p])
    nb = [[] for _ in range(n)]
    for (a, b) in E: nb[a].append(b)
    nbs = [set(l) for l in nb]
    third = {}
    for c in list(cands) + list(fixed):
        for a, b in itertools.permutations(c, 2):
            third[(a, b)] = [t for t in c if t != a and t != b][0]
    andcache = {}
    def AND(u, v):
        if u is True: return v
        if v is True: return u
        key = (min(id(u), id(v)), max(id(u), id(v)))
        if key in andcache: return andcache[key]
        y = m.NewBoolVar("")
        m.AddImplication(y, u); m.AddImplication(y, v); m.AddBoolOr([u.Not(), v.Not(), y])
        andcache[key] = y; return y
    npairs = 0
    for p in range(n):
        for q in range(p + 1, n):
            common = nbs[p] & nbs[q]
            if not common: 
                # must not be adjacent... and need 2 common: impossible unless adjacency; handle below
                pass
            epq = E.get((p, q), False)
            th = third.get((p, q))
            terms = []; const = 0
            for z in common:
                if z == th: continue
                u, v = E[(p, z)], E[(z, q)]
                if u is True and v is True: const += 1
                else: terms.append(AND(u, v))
            rhs_adj = 0; rhs_non = 2
            if epq is True:
                m.Add(sum(terms) + const == 0)
            elif epq is False:
                m.Add(sum(terms) + const == 2)
            else:
                m.Add(sum(terms) + const == 0).OnlyEnforceIf(epq)
                m.Add(sum(terms) + const == 2).OnlyEnforceIf(epq.Not())
            npairs += 1
    for sol in forbid:   # forbid an exact candidate selection
        sel = [x[c] for c in cands if c in sol]; uns = [x[c] for c in cands if c not in sol]
        m.AddBoolOr([v.Not() for v in sel] + uns)
    return m, x, cands

def solve_all(fixed, cands, limit=20, time_limit=600, workers=4, forbid=(), log=False):
    t0 = time.time()
    m, x, cands = build(fixed, cands, forbid=forbid)
    print(f"  model: {len(cands)} candidate lines, built in {time.time()-t0:.1f}s", flush=True)
    sols = []
    while len(sols) < limit:
        s = cp_model.CpSolver(); s.parameters.num_workers = workers; s.parameters.max_time_in_seconds = time_limit
        s.parameters.log_search_progress = log
        r = s.Solve(m)
        if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print("  status", s.StatusName(r), f"{time.time()-t0:.0f}s", flush=True)
            return sols, s.StatusName(r)
        sel = frozenset(c for c in cands if s.Value(x[c]))
        sols.append(sel)
        print(f"  solution {len(sols)} ({time.time()-t0:.0f}s)", flush=True)
        m.AddBoolOr([x[c].Not() for c in sel] + [x[c] for c in cands if c not in sel])
    return sols, "LIMIT"
