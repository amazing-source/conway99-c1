"""(SV1) by adaptive exact cuts (exploration, LAB 17/10/2026).
(SV1): every four-star block (stars 0,1 = line l, 2,3 = line m) with c(l) = 1 and T_S, U_S >= 0 contains a configuration
excluded by an exact lemma.  If the model below becomes INFEASIBLE, (SV1) holds for the encoded lemmas (every cut is a
valid consequence of positivity or of a proved lemma), hence no line of a Conway graph has c = 1.
Model (CP-SAT), all constraints NECESSARY in a Conway graph:
  (A)  local axioms of the 44 labels (exact counts for the four star letters, caps otherwise, pair caps);
  (B)  c(l) = 1: the cubic graph on the 36 neighbours of l is connected (flow on the 12 letters);
  (E3) no rectangle with exactly 3 internal edges at the roots l and m (Codex's lemma);
  (C2a) 2-cut lemma at both roots: a 2-cut of the rectangle multigraph has no mu-crossing, and its sigma ends carry four
       distinct letters;
lazy cuts, each valid:
  (P)  positivity: x^t T_S x >= 0 and x^t U_S x >= 0 for integer x (linear in Gamma; 8 T_S is integral);
  (R)  co-Heawood for a norm-14 lattice direction c (c^t R c = 2 => h = T_S P c in {0,+-1}, same-sign labels neither
       adjacent nor sharing a letter);
  (B2) balanced 2-cut whose two fixed mate crossings lie in the letter group: its variable crossings are >= 1.
Cuts are stored in a JSON file and reloaded, so the search proceeds in rounds of bounded time (adaptive, like Codex).
usage: python c1_sv1_cuts.py <cuts.json> <seconds> [seed]"""
import itertools
import json
import os
import random
import sys
import time
from fractions import Fraction

import numpy as np
from ortools.sat.python import cp_model

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "stars_rank_2026-10-14"))
from stars_rank import kval, LABELS  # noqa: E402
from gg_test import orient, line_graph, components, group  # noqa: E402
from c1_balcut import min_bal_cut  # noqa: E402

MATE = lambda i: i ^ 1
STARS = [0, 1, 2, 3]
S = [l for l in LABELS if l & set(STARS)]
n = len(S)
IDX = {l: i for i, l in enumerate(S)}
PAIRS = list(itertools.combinations(range(n), 2))
PID = {p: k for k, p in enumerate(PAIRS)}
K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)
D = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for t in l:
        D[t, j] = 1
Pi84 = np.eye(84) - D.T @ np.linalg.inv(D @ D.T) @ D
posL = {l: i for i, l in enumerate(LABELS)}
PiS = Pi84[np.ix_([posL[l] for l in S], [posL[l] for l in S])]
Zst = np.array([[1.0 if y in l else 0.0 for l in S] for y in STARS]).T
Qz, _ = np.linalg.qr(Zst)
Pp = np.eye(n) - Qz @ Qz.T
RECTS = [[IDX[frozenset((r, x))] for r in (0, 1) for x in (2 * j, 2 * j + 1)] for j in range(1, 7)] + \
        [[IDX[frozenset((r, x))] for r in (2, 3) for x in (2 * j, 2 * j + 1)] for j in range(2, 7)]
PR = np.zeros((n, len(RECTS)), dtype=np.int64)
for k, q in enumerate(RECTS):
    for w in q:
        PR[w, k] = 1


def pid(i, j):
    return PID[(i, j) if i < j else (j, i)]


OUTER_ROOTS = [(4, 5), (6, 7), (8, 9), (10, 11), (12, 13)]


def random_image(x, rng):
    """image of a label vector under a random symmetry of the model: permutation of the five outer root lines,
    mate flips inside them, swap 0 <-> 1, swap 2 <-> 3 (all constraints of the model are invariant)."""
    perm = list(range(5))
    rng.shuffle(perm)
    f = {}
    for k, (a, b) in enumerate(OUTER_ROOTS):
        (c, d) = OUTER_ROOTS[perm[k]]
        if rng.random() < 0.5:
            c, d = d, c
        f[a], f[b] = c, d
    if rng.random() < 0.5:
        f[0], f[1] = 1, 0
    else:
        f[0], f[1] = 0, 1
    if rng.random() < 0.5:
        f[2], f[3] = 3, 2
    else:
        f[2], f[3] = 2, 3
    y = [0] * n
    for i, l in enumerate(S):
        j = IDX[frozenset(f[t] for t in l)]
        y[j] = int(x[i])
    return y


def build_model(cuts, rng):
    m = cp_model.CpModel()
    e = [m.NewBoolVar("e%d" % k) for k in range(len(PAIRS))]
    E = lambda i, j: e[pid(i, j)]
    # (A) local axioms
    for i, l in enumerate(S):
        for y in range(14):
            lits = [E(i, t) for t, w in enumerate(S) if y in w and t != i]
            if not lits:
                continue
            c = 1 if (y in l or MATE(y) in l) else 2
            m.Add(sum(lits) == c) if y in STARS else m.Add(sum(lits) <= c)
    for i, j in PAIRS:
        s = len(S[i] & S[j])
        prods = []
        for t in range(n):
            if t in (i, j):
                continue
            q = m.NewBoolVar("")
            m.AddBoolOr([E(i, t).Not(), E(j, t).Not(), q])
            m.AddImplication(q, E(i, t))
            m.AddImplication(q, E(j, t))
            prods.append(q)
        m.Add(sum(prods) + s + E(i, j) <= 2)
    # (B) c(l) = 1: connectivity of the letter graph on 2..13 (mates fixed, links through L_0 u L_1)
    letters = list(range(2, 14))
    link = {}
    for a, b in itertools.combinations(letters, 2):
        if b == MATE(a):
            continue
        cands = [E(IDX[frozenset((r, a))], IDX[frozenset((s_, b))]) for r in (0, 1) for s_ in (0, 1)]
        z = m.NewBoolVar("")
        m.AddMaxEquality(z, cands)
        link[(a, b)] = link[(b, a)] = z
    flow = {}
    for a in letters:
        for b in letters:
            if a != b:
                f = m.NewIntVar(0, 11, "")
                if b != MATE(a):
                    m.Add(f <= 11 * link[(a, b)])
                flow[(a, b)] = f
    for a in letters:
        out_ = sum(flow[(a, b)] for b in letters if b != a)
        in_ = sum(flow[(b, a)] for b in letters if b != a)
        m.Add(out_ - in_ == 11) if a == 2 else m.Add(in_ - out_ == 1)
    # (E3) and (C2a) at both roots
    for (a0, a1) in ((0, 1), (2, 3)):
        roots = [(x, x + 1) for x in range(0, 14, 2) if x not in (a0, a1)]
        Q = [[IDX[frozenset((r, t))] for r in (a0, a1) for t in rt] for rt in roots]
        for q in Q:
            m.Add(sum(E(i, j) for i, j in itertools.combinations(q, 2)) != 3)
        for size in range(1, 4):
            for Sub in itertools.combinations(range(6), size):
                if size == 3 and 0 not in Sub:
                    continue
                inside = set(i for k in Sub for i in Q[k])
                outside = set(i for k in range(6) if k not in Sub for i in Q[k])
                cross = [(i, j) for i in inside for j in outside]
                cut = sum(E(i, j) for i, j in cross)
                b2 = m.NewBoolVar("")
                m.Add(cut == 2).OnlyEnforceIf(b2)
                m.Add(cut != 2).OnlyEnforceIf(b2.Not())
                same_star = [E(i, j) for i, j in cross if S[i] & S[j] & {a0, a1}]
                m.Add(sum(same_star) == 0).OnlyEnforceIf(b2)
                Sl = set(t for k in Sub for t in roots[k])
                other = [t for t in range(14) if t not in Sl and t not in (a0, a1)]
                sig = lambda x, y: E(IDX[frozenset((a0, x))], IDX[frozenset((a1, y))])
                for a in Sl:
                    m.Add(sum(sig(a, y) for y in other) + sum(sig(y, a) for y in other) <= 1).OnlyEnforceIf(b2)
                for d in other:
                    m.Add(sum(sig(b, d) for b in Sl) + sum(sig(d, b) for b in Sl) <= 1).OnlyEnforceIf(b2)
    # positivity margin (Kelley): for every stored vector x, x^t T8 x >= tau |x|^2 and x^t U8 x >= tau |x|^2 ;
    # a PSD structure satisfies them with tau = 0, so a proven optimum (or bound) tau* < 0 excludes positivity
    tau = m.NewIntVar(-400, 400, "tau")
    I24K = 24 * np.eye(n, dtype=np.int64) - K8
    for typ, xv in cuts.get("PV", []):
        x = np.array(xv, dtype=np.int64)
        nx = int(x @ x)
        lin = [(PID[(i, j)], 16 * int(x[i] * x[j])) for i, j in PAIRS if x[i] * x[j] != 0]
        base = int(x @ I24K @ x)
        if typ == "T":      # base - 16 sum x x Gamma >= tau |x|^2
            m.Add(base - sum(c * e[k] for k, c in lin) - nx * tau >= 0)
        else:               # floor(56 x^t Pi x) - (base - 16 sum) >= tau |x|^2
            fl = int(np.floor(56 * float(x @ PiS @ x) + 1e-6))
            m.Add(fl - base + sum(c * e[k] for k, c in lin) - nx * tau >= 0)
    m.Maximize(tau)
    # lazy cuts
    for cut in cuts.get("P", []):
        coeffs, rhs = cut
        m.Add(sum(int(c) * e[int(k)] for k, c in coeffs) <= int(rhs))
    for cvec in cuts.get("R", []):
        add_R(m, e, np.array(cvec, dtype=np.int64))
    for vset, var_pairs in cuts.get("B2", []):
        m.Add(sum(e[k] for k in var_pairs) >= 1)
    m.AddDecisionStrategy(e, cp_model.CHOOSE_FIRST, cp_model.SELECT_MIN_VALUE if rng.random() < 0.5 else cp_model.SELECT_MAX_VALUE)
    return m, e, tau


def add_R(m, e, cvec):
    """c^t R c = 2  =>  h = T_S P c in {0,+-1}, same-sign labels not adjacent, not sharing a letter."""
    pc = PR @ cvec                                       # integer vector on labels
    # c^t R c = pc^t T_S pc = (1/8) pc^t (24 I - 8 Gamma - K8) pc = const - 2 sum_{i<j} pc_i pc_j Gamma_ij
    const8 = int(24 * pc @ pc - pc @ K8 @ pc)            # 8 * (pc^t (3I - K) pc)
    assert const8 % 8 == 0
    lin = [(k, -2 * int(pc[i] * pc[j])) for k, (i, j) in enumerate(PAIRS) if pc[i] * pc[j] != 0]
    b = m.NewBoolVar("")
    expr = sum(c * e[k] for k, c in lin) + const8 // 8
    m.Add(expr == 2).OnlyEnforceIf(b)
    m.Add(expr != 2).OnlyEnforceIf(b.Not())
    # 8 h_w = 8 (3 pc_w - (K pc)_w) - 8 sum_b Gamma_wb pc_b ; (K pc)_w integral for rectangle combinations
    kp8 = K8 @ pc
    h = []
    for w in range(n):
        assert kp8[w] % 8 == 0
        const = 3 * int(pc[w]) - int(kp8[w]) // 8
        terms = [(-int(pc[t]), e[pid(w, t)]) for t in range(n) if t != w and pc[t] != 0]
        h.append((const, terms))
    def hx(w):
        const, terms = h[w]
        return sum(c * v for c, v in terms) + const
    for w in range(n):
        m.Add(hx(w) <= 1).OnlyEnforceIf(b)
        m.Add(hx(w) >= -1).OnlyEnforceIf(b)
    for i, j in PAIRS:
        if S[i] & S[j]:
            m.Add(hx(i) + hx(j) <= 1).OnlyEnforceIf(b)
            m.Add(hx(i) + hx(j) >= -1).OnlyEnforceIf(b)
        else:
            m.Add(hx(i) + hx(j) + 2 * e[pid(i, j)] <= 3).OnlyEnforceIf(b)
            m.Add(hx(i) + hx(j) - 2 * e[pid(i, j)] >= -3).OnlyEnforceIf(b)


def perp_eigs(M):
    ev, V = np.linalg.eigh(Pp @ M @ Pp)
    keep = [k for k in range(n) if np.linalg.norm(Qz.T @ V[:, k]) < 1e-6]
    return ev[keep], V[:, keep]


def psd_cuts(G, maxcuts=6):
    """integer vectors violating x^t T x >= 0 or x^t U x >= 0; return linear cuts sum coef e <= rhs."""
    T8 = 24 * np.eye(n, dtype=np.int64) - 8 * G - K8
    T = T8 / 8.0
    U = 7 * PiS - T
    out = []
    for which, M in (("T", T), ("U", U)):
        ev, V = perp_eigs(M)
        order = np.argsort(ev)
        for k in order[:maxcuts]:
            if ev[k] > -1e-9:
                break
            v = V[:, k]
            for scale in (6, 10, 16, 25, 40):
                x = np.rint(v / np.max(np.abs(v)) * scale).astype(np.int64)
                if which == "T":
                    val8 = int(x @ T8 @ x)               # 8 x^t T x, must be >= 0
                    if val8 >= 0:
                        continue
                    # 8 x^t T x = x^t (24 I - K8) x - 16 sum_{i<j} x_i x_j Gamma_ij >= 0
                    coeffs = [(PID[(i, j)], 16 * int(x[i] * x[j])) for i, j in PAIRS if x[i] * x[j] != 0]
                    rhs = int(x @ (24 * np.eye(n, dtype=np.int64) - K8) @ x)
                    out.append((coeffs, rhs, ("T", [int(t) for t in x])))
                    break
                else:
                    # x^t U x = 7 x^t Pi x - x^t T x >= 0  <=>  16 sum x_i x_j Gamma_ij >= x^t(24I - K8)x - 56 x^t Pi x
                    val = float(7 * x @ PiS @ x - x @ T @ x)
                    if val >= -1e-9:
                        continue
                    base = int(x @ (24 * np.eye(n, dtype=np.int64) - K8) @ x)
                    # valid: -16 sum x_i x_j Gamma_ij <= 56 x^t Pi x - base ; the left side is an integer, so the floor of a
                    # slightly enlarged right side is still valid (weaker)
                    rhs = int(np.floor(56 * float(x @ PiS @ x) + 1e-6)) - base
                    coeffs = [(PID[(i, j)], -16 * int(x[i] * x[j])) for i, j in PAIRS if x[i] * x[j] != 0]
                    out.append((coeffs, rhs, ("U", [int(t) for t in x])))
                    break
    return out


def rl_violation(G):
    """first c in {-1,0,1}^11 with c^t R c = 2 whose visible h breaks a co-Heawood rule (entries, letters, adjacency)."""
    T8 = 24 * np.eye(n, dtype=np.int64) - 8 * G - K8
    R8 = PR.T @ T8 @ PR
    cs = np.array(list(itertools.product((-1, 0, 1), repeat=len(RECTS))), dtype=np.int64)
    vals = np.einsum("ij,jk,ik->i", cs, R8, cs)
    for ci in np.where(vals == 16)[0]:
        c = cs[ci]
        h8 = T8 @ (PR @ c)
        h = h8 // 8
        if np.any(h8 % 8) or np.any(np.abs(h) > 1):
            return c
        for i, j in PAIRS:
            if h[i] != 0 and h[i] == h[j] and (S[i] & S[j] or G[i, j]):
                return c
    return None


def b2_cut(G):
    """a balanced 2-cut of G_l whose two crossings are fixed letter-mate edges -> its variable crossing pairs."""
    edges = [[sorted(S[i]), sorted(S[j])] for i, j in PAIRS if G[i, j]]
    L, EE = orient(S, edges, 0)
    V, pos, A = line_graph(L, EE)
    b = min_bal_cut(V, A)
    if b is None or b[0] != 2:
        return None
    _, q, C = b
    A = np.array(A)
    cut = [(i, j) for i in range(36) for j in range(36) if A[i, j] and (i in C) and (j not in C)]
    is_letter = lambda x: isinstance(x, tuple)            # ("L", a) for a letter, a frozenset for a label
    if not all(is_letter(V[i]) and is_letter(V[j]) for i, j in cut):
        return None
    lab = [V[i] for i in C if not is_letter(V[i])]
    others = [V[i] for i in range(36) if i not in C and not is_letter(V[i])]
    var_pairs = [pid(IDX[a], IDX[b]) for a in lab for b in others]
    return [[sorted(x) for x in lab], var_pairs]


def main():
    cutfile, secs = sys.argv[1], float(sys.argv[2])
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    per = float(sys.argv[4]) if len(sys.argv) > 4 else 40.0
    rng = random.Random(seed)
    cuts = json.load(open(cutfile)) if os.path.exists(cutfile) else {}
    for k in ("P", "PV", "R", "B2"):
        cuts.setdefault(k, [])
    # convert old coefficient-only cuts: keep them as hard constraints (valid), they are already in "P"
    t0 = time.time()
    rounds = 0
    while time.time() - t0 < secs - 15:
        rounds += 1
        m, e, tau = build_model(cuts, rng)
        sv = cp_model.CpSolver()
        sv.parameters.num_search_workers = 2
        sv.parameters.max_time_in_seconds = min(per, max(10.0, secs - (time.time() - t0)))
        sv.parameters.random_seed = rng.randint(0, 10 ** 6)
        st = sv.Solve(m)
        bound = sv.BestObjectiveBound() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE, cp_model.UNKNOWN) else None
        if st == cp_model.INFEASIBLE:
            print("round %d: INFEASIBLE => (SV1) holds for the encoded lemmas" % rounds, flush=True)
            break
        if bound is not None and bound < 0:
            print("round %d: best bound on tau = %s < 0  =>  no positive structure: (SV1) holds for the encoded lemmas"
                  % (rounds, bound), flush=True)
            break
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print("round %d: %s, bound %s" % (rounds, sv.StatusName(st), bound), flush=True)
            continue
        G = np.zeros((n, n), dtype=np.int64)
        for k, (i, j) in enumerate(PAIRS):
            if sv.Value(e[k]):
                G[i, j] = G[j, i] = 1
        tv = sv.Value(tau)
        pc = psd_cuts(G, maxcuts=8)
        T = (24 * np.eye(n) - 8 * G - K8) / 8.0
        lt = perp_eigs(T)[0].min()
        lu = perp_eigs(7 * PiS - T)[0].min()
        if pc:
            nimg = int(os.environ.get("NIMG", "0"))
            for coeffs, rhs, vec in pc:
                typ, xv = vec
                cuts["PV"].append([typ, list(xv)])
                for _ in range(nimg):
                    cuts["PV"].append([typ, random_image(xv, rng)])
            print("round %d: tau %d (bound %s, %s), true lambda_T %.3f lambda_U %.3f: +%d vectors (total %d)" % (
                rounds, tv, bound, sv.StatusName(st), lt, lu, len(pc), len(cuts["PV"])), flush=True)
        else:
            c = rl_violation(G)
            if c is not None:
                cuts["R"].append([int(x) for x in c])
                print("round %d: PSD, killed by a norm-14 co-Heawood direction: +1 R cut (total %d)" % (rounds, len(cuts["R"])),
                      flush=True)
            else:
                b = b2_cut(G)
                if b is not None:
                    cuts["B2"].append(b)
                    print("round %d: PSD, killed by a balanced letter 2-cut: +1 B2 cut" % rounds, flush=True)
                else:
                    fn = os.path.join(HERE, "unbiased_walks", "sv1_survivor_%d.json" % int(time.time()))
                    json.dump({"labels": [sorted(l) for l in S], "edges": [[i, j] for i, j in PAIRS if G[i, j]]},
                              open(fn, "w"))
                    nu = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-7))
                    print("round %d: SURVIVOR (PSD, c = 1, no encoded lemma applies), nu = %d, saved %s" % (rounds, nu, fn),
                          flush=True)
                    json.dump(cuts, open(cutfile, "w"))
                    break
        json.dump(cuts, open(cutfile, "w"))
    json.dump(cuts, open(cutfile, "w"))
    print("end after %d rounds, %.0f s; vectors %d, P %d, R %d, B2 %d" % (rounds, time.time() - t0, len(cuts["PV"]),
          len(cuts["P"]), len(cuts["R"]), len(cuts["B2"])), flush=True)


if __name__ == "__main__":
    main()
