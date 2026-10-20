"""Positive control on real srg(243,22,1,2) graphs (LAB 20/10/2026).

For each graph: (1) verify A^2 = 22 I + A + 2 (J - I - A) exactly; (2) for several vertices v and random relabellings
of the 11 lines (order of the lines, orientation inside each line), extract the local structure on the model labels of
the K = 22 analogue of R8 (stars 0..3 exact, all 16 labels {4,t}; letter 4 exact as well since L_4 is inside S) and run
the independent checker Model.check, with the letters 0..4 exact; (3) also check the implied constraints L4B and XPAIR
directly; (4) save one planted structure per graph as JSON (labels + edges) for the CNF unit-propagation test.
usage: python control243.py <out dir> <edges files...>"""
import itertools
import json
import os
import random
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r8lib  # noqa: E402


def load(path):
    E = [tuple(map(int, l.split())) for l in open(path) if l.strip()]
    nv = 1 + max(max(e) for e in E)
    A = np.zeros((nv, nv), dtype=np.int64)
    for a, b in E:
        A[a, b] = A[b, a] = 1
    return A


def is_srg(A, k, lam, mu):
    n = A.shape[0]
    I = np.eye(n, dtype=np.int64)
    J = np.ones((n, n), dtype=np.int64)
    return bool((A.sum(1) == k).all() and (A @ A == k * I + lam * A + mu * (J - I - A)).all() and not A.diagonal().any())


def local(A, v, rng):
    nb = [int(x) for x in np.nonzero(A[v])[0]]
    mate = {}
    for y in nb:
        m = [z for z in nb if A[y, z]]
        assert len(m) == 1
        mate[y] = m[0]
    lines = []
    for y in nb:
        if all(y not in L for L in lines):
            lines.append((y, mate[y]))
    rng.shuffle(lines)
    order = []
    for a, b in lines:
        order += [a, b] if rng.random() < 0.5 else [b, a]
    letter = {y: i for i, y in enumerate(order)}
    far = [x for x in range(A.shape[0]) if x != v and not A[v, x]]
    lab = {}
    for x in far:
        ls = [letter[y] for y in nb if A[x, y]]
        assert len(ls) == 2 and (ls[0] ^ 1) != ls[1]
        lab[frozenset(ls)] = x
    assert len(lab) == len(far)
    return lab


def main():
    outdir = sys.argv[1]
    rng = random.Random(243)
    M = r8lib.Model(22)
    xl = 4
    res = []
    for path in sys.argv[2:]:
        A = load(path)
        ok = is_srg(A, 22, 1, 2)
        rec = {"graph": os.path.basename(path), "srg(243,22,1,2)": ok, "tests": 0, "checker_ok": 0, "L4B_ok": 0,
               "XPAIR_ok": 0}
        for v in rng.sample(range(A.shape[0]), 6):
            for _ in range(3):
                lab = local(A, v, rng)
                E = [(i, j) for i, j in M.pairs if A[lab[M.S[i]], lab[M.S[j]]]]
                bad = M.check(E, extra_exact=(xl,))
                rec["tests"] += 1
                rec["checker_ok"] += int(not bad)
                adj = set(E)
                nb = lambda i: [j for j in range(M.n) if (min(i, j), max(i, j)) in adj]
                # L4B: every base label has exactly c(y,4) neighbours in L_4
                l4b = all(sum(1 for j in nb(i) if xl in M.S[j]) == r8lib.c_need(M.S[i], xl) for i in range(len(M.B)))
                rec["L4B_ok"] += int(l4b)
                Bp = [i for i in range(len(M.B)) if xl not in M.S[i] and 5 not in M.S[i]]
                C4 = [i for i in range(len(M.B)) if xl in M.S[i]]
                Xi = list(range(len(M.B), M.n))
                z = sum(1 for y in Bp if not any((min(y, c), max(y, c)) in adj for c in C4))
                a = sum(1 for p, q in itertools.combinations(Xi, 2) if (p, q) in adj)
                rec["XPAIR_ok"] += int(z + a <= len(Xi) * (len(Xi) - 1) // 2)
                if rec["tests"] == 1:
                    rec["example"] = {"v": v, "violations": bad[:3], "z": z, "a": a}
                    json.dump({"K": 22, "graph": rec["graph"], "v": v, "labels": [sorted(l) for l in M.S],
                               "edges": [list(p) for p in E]},
                              open(os.path.join(outdir, "planted_%s.json" % rec["graph"].split(".")[0]), "w"))
        print(json.dumps(rec), flush=True)
        res.append(rec)
    json.dump(res, open(os.path.join(outdir, "control243.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
