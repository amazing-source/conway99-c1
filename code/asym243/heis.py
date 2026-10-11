"""Cayley covers of BH = Cay(F_3^4, Sbar) by central extensions E_B = Z_3 x_B F_3^4.
Vertex (t,x); (t,x) ~ (t+a(s)+B(x,s), x+s) for s in Sbar, and (t,x) ~ (t+-1, x).
srg(243,22,1,2)  <=>  for every delta not in Sbar u {0}, the 6 values a(s1)+a(s2)+B(s1,s2) (s1+s2=delta, s_i in Sbar)
are equidistributed in Z_3; and a(-s) = -a(s) + B(s,s)."""
import itertools, numpy as np, sys
from ortools.sat.python import cp_model
from golay import golay_coords
from lines_model import HS
# quotient by h_0: coordinates. choose basis of F_3^5 with h_0 as last vector; project.
G, H, PTS = golay_coords()
h = [np.array(v) for v in HS]
# find complement basis: 4 vectors among h_1..h_10 spanning F_3^5/<h_0>
def rank3(M):
    M = [list(r) for r in M]; r = 0; cols = len(M[0]) if M else 0
    for c in range(cols):
        piv = next((i for i in range(r, len(M)) if M[i][c] % 3), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]; inv = 1 if M[r][c] % 3 == 1 else 2
        M[r] = [(x * inv) % 3 for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] % 3:
                f = M[i][c]; M[i] = [(x - f * y) % 3 for x, y in zip(M[i], M[r])]
        r += 1
    return r
basis = None
for comb in itertools.combinations(range(1, 11), 4):
    if rank3([h[0]] + [h[i] for i in comb]) == 5: basis = comb; break
Bm = np.array([h[i] for i in basis] + [h[0]]).T % 3          # columns: w1..w4, h0
# coordinates of v in this basis: solve Bm c = v mod 3 by brute force table
coord = {}
for c in itertools.product(range(3), repeat=5):
    coord[tuple((Bm @ np.array(c)) % 3)] = c
Sbar = []; aval = {}
for m in range(1, 11):
    for e in (1, 2):
        c = coord[tuple((e * h[m]) % 3)]
        s = tuple(c[:4]); Sbar.append(s); aval[s] = c[4]
Sset = set(Sbar)
def addv(x, y): return tuple((a + b) % 3 for a, b in zip(x, y))
reps = {}
for s1 in Sbar:
    for s2 in Sbar:
        d = addv(s1, s2)
        if d == (0,) * 4 or d in Sset: continue
        reps.setdefault(d, []).append((s1, s2))
assert all(len(v) == 6 for v in reps.values()) and len(reps) == 60

def bil(Bmat, x, y): return int(np.array(x) @ Bmat @ np.array(y)) % 3

def check(avals, Bmat):
    for d, L in reps.items():
        vals = [(avals[s1] + avals[s2] + bil(Bmat, s1, s2)) % 3 for s1, s2 in L]
        if sorted(vals) != [0, 0, 1, 1, 2, 2]: return False
    return all((avals[tuple((-np.array(s)) % 3)] + avals[s] - bil(Bmat, s, s)) % 3 == 0 for s in Sbar)

if __name__ == "__main__":
    print("BvLS (B=0, a from Golay):", check(aval, np.zeros((4, 4), dtype=int)))
    # CP-SAT over a in Z3^Sbar, B in Z3^{4x4}
    m = cp_model.CpModel()
    a = {s: m.NewIntVar(0, 2, "") for s in Sbar}
    Bv = [[m.NewIntVar(0, 2, "") for _ in range(4)] for _ in range(4)]
    # one-hot booleans for B entries and a values to linearise B(s1,s2) mod 3
    def mod3_expr(expr, tag):
        q = m.NewIntVar(-40, 40, ""); r = m.NewIntVar(0, 2, ""); m.Add(expr == 3 * q + r); return r
    for s in Sbar:
        ms = tuple((-np.array(s)) % 3)
        bss = sum(s[i] * s[j] * Bv[i][j] for i in range(4) for j in range(4))
        r = mod3_expr(a[ms] + a[s] - bss, "")
        m.Add(r == 0)
    for d, L in reps.items():
        cnt = {0: [], 1: [], 2: []}
        for s1, s2 in L:
            e = a[s1] + a[s2] + sum(s1[i] * s2[j] * Bv[i][j] for i in range(4) for j in range(4))
            r = mod3_expr(e, "")
            for v in range(3):
                b = m.NewBoolVar(""); m.Add(r == v).OnlyEnforceIf(b); m.Add(r != v).OnlyEnforceIf(b.Not()); cnt[v].append(b)
        for v in range(3): m.Add(sum(cnt[v]) == 2)
    # require B non-symmetric?
    mode = sys.argv[1] if len(sys.argv) > 1 else "nonsym"
    if mode == "nonsym":
        diffs = []
        for i in range(4):
            for j in range(i + 1, 4):
                b = m.NewBoolVar(""); m.Add(Bv[i][j] != Bv[j][i]).OnlyEnforceIf(b); m.Add(Bv[i][j] == Bv[j][i]).OnlyEnforceIf(b.Not()); diffs.append(b)
        m.AddBoolOr(diffs)
    s = cp_model.CpSolver(); s.parameters.num_workers = 1; s.parameters.max_time_in_seconds = 1200
    sols = []
    class CB(cp_model.CpSolverSolutionCallback):
        def on_solution_callback(self):
            av = {x: self.Value(a[x]) for x in Sbar}; Bmat = np.array([[self.Value(Bv[i][j]) for j in range(4)] for i in range(4)])
            sols.append((av, Bmat))
            if len(sols) >= 2000: self.StopSearch()
    s.parameters.enumerate_all_solutions = True
    r = s.Solve(m, CB())
    print(mode, "status", s.StatusName(r), "solutions", len(sols))
    import pickle; pickle.dump((Sbar, sols), open(f"heis_{mode}.pkl", "wb"))
    if sols:
        av, Bmat = sols[0]; print("check", check(av, Bmat)); print(Bmat); print("antisym part rank:", rank3(((Bmat - Bmat.T) % 3).tolist()))
