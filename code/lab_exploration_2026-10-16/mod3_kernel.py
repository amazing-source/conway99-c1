"""Mod-3 kernel of A_Omega on random c(l) = 1 four-star structures (CNF axioms of stars_rank.build, optional E3 clauses).
Prints nullity over F_3 and over Q, and tests candidate universal mod-3 kernel vectors.
usage: python mod3_kernel.py seed nsamples [--e3]"""
import itertools, json, os, random, sys
import numpy as np
from pycryptosat import Solver
SR = r"C:\Users\RESEARCHER\Downloads\conway_c2_researcher2_start_2026_09_30\conway_c2_researcher2_start_2026_09_30\work\stars_rank_2026-10-14"
sys.path.insert(0, SR)
sys.path.insert(0, ".")
from stars_rank import build  # noqa
from c1_margin56 import S as S0, rank_mod, gl_connected  # noqa


def nullspace_mod(M, p):
    A = [[int(x) % p for x in r] for r in M]
    n = len(A[0]); rows = len(A)
    piv = []; r = 0
    for c in range(n):
        pr = next((i for i in range(r, rows) if A[i][c]), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        iv = pow(A[r][c], p - 2, p)
        A[r] = [(x * iv) % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        piv.append(c); r += 1
    free = [c for c in range(n) if c not in piv]
    basis = []
    for f in free:
        v = [0] * n; v[f] = 1
        for i, c in enumerate(piv):
            v[c] = (-A[i][f]) % p
        basis.append(v)
    return basis


def ball(S, EE):
    n = 59
    A = np.zeros((n, n), dtype=np.int64)
    for a in range(14):
        A[0, 1 + a] = A[1 + a, 0] = 1
    for a in range(0, 14, 2):
        A[1 + a, 2 + a] = A[2 + a, 1 + a] = 1
    for i, l in enumerate(S):
        for a in l:
            A[15 + i, 1 + a] = A[1 + a, 15 + i] = 1
    for i, j in itertools.combinations(range(44), 2):
        if frozenset((S[i], S[j])) in EE:
            A[15 + i, 15 + j] = A[15 + j, 15 + i] = 1
    return A


def sample(seed, e3):
    rng = random.Random(seed)
    S, idx, e, F = build([0, 1, 2, 3], rng)
    sol = Solver(options={"polar": "rnd", "seed": str(seed)})
    for c in F.clauses:
        sol.add_clause(c)
    if e3:
        for (a0, a1) in ((0, 1), (2, 3)):
            for x in range(0, 14, 2):
                if {x, x + 1} & {a0, a1}:
                    continue
                Q = [idx[frozenset((r, t))] for r in (a0, a1) for t in (x, x + 1)]
                prs = [(Q[i], Q[j]) for i, j in itertools.combinations(range(4), 2)]
                for sub in itertools.combinations(range(6), 3):
                    sol.add_clause([-e[prs[k]] if k in sub else e[prs[k]] for k in range(6)])
    for _ in range(200):
        ok, model = sol.solve([v if rng.random() < 0.5 else -v for v in rng.sample(list(e.values()), 25)])
        if not ok:
            continue
        EE = {frozenset((S[i], S[j])) for (i, j), v in e.items() if i < j and model[v]}
        # reorder to the standard S0 order
        conn, degok = gl_connected(EE)
        if conn and degok:
            return EE
    return None


def main():
    seed, ns = int(sys.argv[1]), int(sys.argv[2])
    e3 = "--e3" in sys.argv
    out = []
    for k in range(ns):
        EE = sample(seed * 1000 + k, e3)
        if EE is None:
            continue
        A = ball(S0, EE)
        r3 = rank_mod(A.tolist(), 3)
        nuQ = 59 - rank_mod((A - 3 * np.eye(59, dtype=np.int64)).tolist(), 1000000007)
        ker = nullspace_mod(A.tolist(), 3)
        # how much of the mod-3 kernel lives on N[v] only / vanishes on N[v]
        onN = sum(1 for _ in [0])
        Kn = np.array(ker) if ker else np.zeros((0, 59), dtype=int)
        # dimension of kernel vectors vanishing on N[v] (cols 0..14)
        sub = nullspace_mod(Kn[:, :15].T.tolist(), 3) if len(ker) else []
        print("sample %d: rank_F3(A_Omega) = %d (nullity %d), nu_Q = %d, kernel vectors vanishing on N[v]: %d" % (
            k, r3, 59 - r3, nuQ, len(sub)), flush=True)
        out.append({"edges": [sorted([sorted(a), sorted(b)]) for a, b in (tuple(x) for x in EE)], "r3": r3, "nuQ": nuQ})
    json.dump(out, open("mod3_samples_%d%s.json" % (seed, "_e3" if e3 else ""), "w"))


if __name__ == "__main__":
    main()
