"""Unbiased four-star blocks at c = 1 (exploration, LAB 17/10/2026).
W = N[v] u S = N[l] u Y_2 u Y_3 (59 vertices; l = {v,0,1}, m = {v,2,3}, Y_r = far labels {r,s}).  Conway needs
lambda_2(A_W) <= 3 (<=> T_S >= 0) and nullity(A_W - 3I) = nu(T_S) >= 59 - 45 = 14.  Our biased c = 1 data: nu <= 10.
Construction with NO symmetric seed: random line type (mu_0, mu_1, sigma) with the local axioms and c(l) = 1, random
completion by CP-SAT (random objective) of the 20 far labels (2 + 2 attachments in L_0, L_1) and of all Y-Y edges,
under the necessary local conditions (exact neighbourhood counts for v, 0, 1 and the letters 2, 3, whose neighbours all
lie in W; caps lambda / mu for every other pair).  Then descent to positivity and a random walk inside
{lambda_2 <= 3} by attachment swaps inside Y_2 or inside Y_3 and 2-switches of the Y-Y edges (exact counts are
re-checked by caps_ok); exact nullity of A_W - 3I
(rank modulo two primes) at each visited structure; Laplacian gap of G_l recorded.
usage: python c1_ball59_random.py <line types> <seed> <walk steps> [seconds per completion]"""
import itertools
import json
import random
import sys
from collections import Counter

import numpy as np
from ortools.sat.python import cp_model

N, seed, steps = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
secs = float(sys.argv[4]) if len(sys.argv) > 4 else 30.0
X = list(range(2, 14))
MATE = lambda a: a ^ 1
OUT = [s for s in X if s not in (2, 3)]
PRIMES = (2147483647, 2147483629)


def rand_type(rng):
    def rm():
        p = X[:]
        rng.shuffle(p)
        mm = {}
        for i in range(0, 12, 2):
            mm[p[i]], mm[p[i + 1]] = p[i + 1], p[i]
        return mm
    mu0, mu1 = rm(), rm()
    perm = X[:]
    rng.shuffle(perm)
    return mu0, mu1, dict(zip(X, perm))


def base(mu0, mu1, sig):
    V = ["v", "p0", "p1"] + [("L", a) for a in X] + [(0, a) for a in X] + [(1, a) for a in X] + \
        [(r, s) for r in (2, 3) for s in OUT]
    pos = {x: i for i, x in enumerate(V)}
    A = np.zeros((len(V), len(V)), dtype=int)
    def e(a, b):
        A[pos[a], pos[b]] = A[pos[b], pos[a]] = 1
    e("v", "p0"); e("v", "p1"); e("p0", "p1")
    for a in X:
        e("v", ("L", a)); e("p0", (0, a)); e("p1", (1, a))
        if a < MATE(a):
            e(("L", a), ("L", MATE(a)))
        e(("L", a), (0, a)); e(("L", a), (1, a))
        if a < mu0[a]:
            e((0, a), (0, mu0[a]))
        if a < mu1[a]:
            e((1, a), (1, mu1[a]))
        e((0, a), (1, sig[a]))
    for r in (2, 3):
        for s in OUT:
            e((r, s), ("L", r)); e((r, s), ("L", s))
    return V, pos, A


def axioms_ok(mu0, mu1, sig):
    V, pos, A = base(mu0, mu1, sig)
    B = A[:39, :39]
    B2 = B @ B
    for i, j in itertools.combinations(range(39), 2):
        if B2[i, j] > (1 if B[i, j] else 2):
            return False
    G = B[3:, 3:]
    seen, st = {0}, [0]
    while st:
        u = st.pop()
        for w in np.nonzero(G[u])[0]:
            if int(w) not in seen:
                seen.add(int(w)); st.append(int(w))
    return len(seen) == 36


def complete(mu0, mu1, sig, rng):
    V, pos, A0 = base(mu0, mu1, sig)
    n = len(V)
    m = cp_model.CpModel()
    var = {}
    Yv = [pos[(r, s)] for r in (2, 3) for s in OUT]
    L0 = [pos[(0, a)] for a in X]
    L1 = [pos[(1, a)] for a in X]
    for y in Yv:
        for u in L0 + L1:
            var[(y, u)] = var[(u, y)] = m.NewBoolVar("")
    for y, y2 in itertools.combinations(Yv, 2):
        var[(y, y2)] = var[(y2, y)] = m.NewBoolVar("")
    adj = lambda i, j: 0 if i == j else (var[(i, j)] if (i, j) in var else int(A0[i, j]))
    for y in Yv:
        m.Add(sum(var[(y, u)] for u in L0) == 2)
        m.Add(sum(var[(y, u)] for u in L1) == 2)
    def AND(p, q):
        if isinstance(p, int) or isinstance(q, int):
            if isinstance(p, int) and isinstance(q, int):
                return p * q
            return (q if p else 0) if isinstance(p, int) else (p if q else 0)
        z = m.NewBoolVar("")
        m.AddBoolOr([p.Not(), q.Not(), z]); m.AddImplication(z, p); m.AddImplication(z, q)
        return z
    exact = {pos["v"], pos["p0"], pos["p1"], pos[("L", 2)], pos[("L", 3)]}
    for i, j in itertools.combinations(range(n), 2):
        terms = [AND(adj(i, t), adj(j, t)) for t in range(n) if t not in (i, j)]
        const = sum(t for t in terms if isinstance(t, int))
        terms = [t for t in terms if not isinstance(t, int)]
        e = adj(i, j)
        full = (i in exact) or (j in exact)
        if isinstance(e, int):
            tgt = 1 if e else 2
            if not terms:
                if (const != tgt) if full else (const > tgt):
                    return None
                continue
            m.Add(sum(terms) + const == tgt) if full else m.Add(sum(terms) + const <= tgt)
        else:
            m.Add(sum(terms) + const == 2 - e) if full else m.Add(sum(terms) + const <= 2 - e)
    m.Maximize(sum(rng.randint(-5, 5) * v for v in set(var.values())))
    sv = cp_model.CpSolver()
    sv.parameters.num_search_workers = 1
    sv.parameters.max_time_in_seconds = secs
    sv.parameters.random_seed = rng.randint(0, 10 ** 6)
    st = sv.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None
    A = A0.copy()
    for (i, j), v in var.items():
        A[i, j] = sv.Value(v)
    return V, pos, A, exact


def caps_ok(A, exact_idx):
    A2 = A @ A
    iu = np.triu_indices(len(A), 1)
    if np.any(A2[iu] > np.where(A[iu] == 1, 1, 2)):
        return False
    for i in exact_idx:
        tgt = np.where(A[i] == 1, 1, 2)
        tgt[i] = A2[i, i]
        if np.any(A2[i] != tgt):
            return False
    return True


def rank_mod(M, p):
    M = (M % p).astype(np.int64)
    n, mm = M.shape
    r = 0
    for c in range(mm):
        nz = np.nonzero(M[r:, c] % p)[0]
        if len(nz) == 0:
            continue
        piv = r + nz[0]
        M[[r, piv]] = M[[piv, r]]
        M[r] = (M[r] * pow(int(M[r, c]), p - 2, p)) % p
        col = M[:, c].copy()
        col[r] = 0
        nzr = np.nonzero(col)[0]
        if len(nzr):
            M[nzr] = (M[nzr] - (col[nzr, None] * M[r][None, :]) % p) % p
        r += 1
        if r == n:
            break
    return r


def nullity3(A):
    M = A.astype(np.int64) - 3 * np.eye(len(A), dtype=np.int64)
    return len(A) - max(rank_mod(M, p) for p in PRIMES)


lam2 = lambda A: np.sort(np.linalg.eigvalsh(A.astype(float)))[-2]


def main():
    rng = random.Random(seed)
    done, tries = 0, 0
    allhist = Counter()
    data_types = []
    if "--data" in sys.argv:
        # control: line types of our (bottlenecked) c = 1 data, Y completed at random as for random types
        sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else ".")
        from gg_test import orient, line_graph, components
        cache = sys.argv[sys.argv.index("--data") + 1]
        for line in open(cache):
            d = json.loads(line)
            if len(d["labels"]) != 44:
                continue
            for side in (0, 1):
                L, E = orient([frozenset(x) for x in d["labels"]], d["edges"], side)
                Vv, pp, AA = line_graph(L, E)
                if any(sum(r) != 3 for r in AA) or components(AA) != 1:
                    continue
                f = lambda a, b: frozenset((frozenset(a), frozenset(b))) in E
                mu0 = {a: b for a in X for b in X if b != a and f((0, a), (0, b))}
                mu1 = {a: b for a in X for b in X if b != a and f((1, a), (1, b))}
                sg = {a: b for a in X for b in X if f((0, a), (1, b))}
                if len(mu0) == 12 and len(mu1) == 12 and len(sg) == 12:
                    data_types.append((mu0, mu1, sg))
        rng.shuffle(data_types)
    while done < N and tries < 200 * N:
        tries += 1
        if data_types:
            mu0, mu1, sig = data_types.pop()
        else:
            mu0, mu1, sig = rand_type(rng)
        if not axioms_ok(mu0, mu1, sig):
            continue
        res = complete(mu0, mu1, sig, rng)
        if res is None:
            continue
        V, pos, A, exact = res
        exact_idx = sorted(exact)
        groups = [[pos[(r, s)] for s in OUT] for r in (2, 3)]
        L0 = [pos[(0, a)] for a in X]
        L1 = [pos[(1, a)] for a in X]
        gap = np.sort(np.linalg.eigvalsh(3 * np.eye(36) - A[3:39, 3:39]))[1]

        Yall = groups[0] + groups[1]

        def move(A):
            if rng.random() < 0.5:
                # 2-switch on edges among Y: (a,b),(c,d) -> (a,c),(b,d) or (a,d),(b,c); every vertex keeps its Y-degree
                E = [(i, j) for i, j in itertools.combinations(Yall, 2) if A[i, j]]
                if len(E) < 2:
                    return None
                (a, b), (c, d) = rng.sample(E, 2)
                if len({a, b, c, d}) < 4:
                    return None
                if rng.random() < 0.5:
                    c, d = d, c
                if A[a, c] or A[b, d]:
                    return None
                B = A.copy()
                B[a, b] = B[b, a] = 0; B[c, d] = B[d, c] = 0
                B[a, c] = B[c, a] = 1; B[b, d] = B[d, b] = 1
                return B
            Yg = rng.choice(groups)
            y, y2 = rng.sample(Yg, 2)
            Lr = L0 if rng.random() < 0.5 else L1
            au = [u for u in Lr if A[y, u] and not A[y2, u]]
            bu = [u for u in Lr if A[y2, u] and not A[y, u]]
            if not au or not bu:
                return None
            u, u2 = rng.choice(au), rng.choice(bu)
            B = A.copy()
            B[y, u] = B[u, y] = 0; B[y2, u2] = B[u2, y2] = 0
            B[y, u2] = B[u2, y] = 1; B[y2, u] = B[u, y2] = 1
            return B
        cur = lam2(A)
        start = cur
        for _ in range(6000):
            if cur <= 3 + 1e-9:
                break
            B = move(A)
            if B is None:
                continue
            val = lam2(B)
            if val < cur and caps_ok(B, exact_idx):
                A, cur = B, val
        done += 1
        if cur > 3 + 1e-9:
            print("type %d: gap %.3f  lambda_2 %.4f -> %.4f, positivity NOT reached" % (done, gap, start, cur), flush=True)
            continue
        hist = Counter([nullity3(A)])
        visited = 1
        for _ in range(steps):
            B = move(A)
            if B is None:
                continue
            val = lam2(B)
            if val > 3 + 1e-9 or not caps_ok(B, exact_idx):
                continue
            A = B
            visited += 1
            nu = nullity3(A)
            hist[nu] += 1
            if nu >= 11:
                fn = "c1_ball59_hit_seed%d_type%d_nu%d.json" % (seed, done, nu)
                json.dump({"names": [str(x) for x in V], "adjacency": A.tolist()}, open(fn, "w"))
        allhist.update(hist)
        print("type %d: gap %.3f  lambda_2 %.4f -> positive; visited %d ; nu(T_S) histogram %s" % (
            done, gap, start, visited, dict(sorted(hist.items()))), flush=True)
    print("ALL: nu(T_S) histogram over positive structures %s (Conway needs >= 14)" % dict(sorted(allhist.items())))


main()
