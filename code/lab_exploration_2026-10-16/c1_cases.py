"""c = 1 as a finite list of cases, closed one by one (exploration, LAB 17/10/2026; adaptive, in Codex's manner).
Case = numbers of internal edges e(Q_0j) in {0,1,2} of the six rectangles of the root l = {v,0,1}: e of the rectangle
shared with m = {v,2,3}, then the five outer rectangles sorted (they are interchangeable): 3 x 21 = 63 cases.
(e = 3 is impossible by Codex's lemma, e = 4 is a grid, impossible at c(l) = 1.)
Model per case: c1_sv1_cuts.build_model (axioms, c(l) = 1, E3, 2-cut lemma at both roots) + the case equalities +
global pools of exact cuts (shared by all cases, every cut is valid everywhere):
  positivity vectors (x^t T_S x >= 0, x^t U_S x >= 0, hard constraints here), co-Heawood directions, letter 2-cuts.
Stages: 0 = combinatorial feasibility only; 1 = cut loop (feasibility mode): solve, add the cuts that kill the solution
(with NIMG symmetry images for positivity cuts), repeat.  Status per case: INFEASIBLE (closed), SURVIVOR (a positive
c = 1 block that no encoded lemma kills: saved), UNKNOWN (time).
usage: python c1_cases.py <pool.json> <status.json> <stage 0|1> <seconds per case> [case indices a-b] [seed]"""
import itertools
import json
import os
import random
import sys
import time

import numpy as np
from ortools.sat.python import cp_model

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c1_sv1_cuts as C  # noqa: E402

ROOT_L = [(2, 3), (4, 5), (6, 7), (8, 9), (10, 11), (12, 13)]


def all_cases():
    out = []
    for e_lm in (0, 1, 2):
        for outer in itertools.combinations_with_replacement((2, 1, 0), 5):
            out.append((e_lm,) + tuple(outer))
    return out


def build(case, pool, rng, use_cuts):
    sub = {"P": [], "PV": [], "R": [], "B2": []}
    if use_cuts:
        sub["R"] = pool.get("R", [])
        sub["B2"] = pool.get("B2", [])
    m, e, tau = C.build_model(sub, rng)
    E = lambda i, j: e[C.pid(i, j)]
    for k, rt in enumerate(ROOT_L):
        q = [C.IDX[frozenset((r, t))] for r in (0, 1) for t in rt]
        m.Add(sum(E(i, j) for i, j in itertools.combinations(q, 2)) == case[k])
    if use_cuts:
        I24K = 24 * np.eye(C.n, dtype=np.int64) - C.K8
        for typ, xv in pool.get("PV", []):
            x = np.array(xv, dtype=np.int64)
            lin = [(C.PID[(i, j)], 16 * int(x[i] * x[j])) for i, j in C.PAIRS if x[i] * x[j] != 0]
            base = int(x @ I24K @ x)
            if typ == "T":
                m.Add(sum(c * e[k] for k, c in lin) <= base)
            else:
                fl = int(np.floor(56 * float(x @ C.PiS @ x) + 1e-6))
                m.Add(sum(c * e[k] for k, c in lin) >= base - fl)
    # feasibility mode: drop the tau objective of build_model
    m.ClearObjective()
    return m, e


def solve(m, secs, seed):
    sv = cp_model.CpSolver()
    sv.parameters.num_search_workers = 2
    sv.parameters.max_time_in_seconds = secs
    sv.parameters.random_seed = seed
    st = sv.Solve(m)
    return sv, st


def local_cuts(G, frac=0.5, per=3):
    """LOCAL positivity cuts: for the most negative directions of T_S and U_S, the smallest top-|x| label set W with
    lambda_min(M_W) <= frac * lambda_min(M_S); the integer rounding of the bottom eigenvector of M_W (zero outside W)
    is kept if it still gives x^t M x < 0.  Valid for every structure (principal submatrices of PSD matrices)."""
    T8 = 24 * np.eye(C.n, dtype=np.int64) - 8 * G - C.K8
    T = T8 / 8.0
    U = 7 * C.PiS - T
    out = []
    for typ, M in (("T", T), ("U", U)):
        ev, V = C.perp_eigs(M)
        for k in np.argsort(ev)[:per]:
            if ev[k] > -1e-9:
                break
            order = list(np.argsort(-np.abs(V[:, k])))
            for size in range(3, C.n + 1):
                W = order[:size]
                w, X = np.linalg.eigh(M[np.ix_(W, W)])
                if w[0] <= frac * ev[k]:
                    break
            y = X[:, 0] / np.max(np.abs(X[:, 0]))
            for scale in (4, 6, 10, 16, 25):
                x = np.zeros(C.n, dtype=np.int64)
                x[W] = np.rint(y * scale).astype(np.int64)
                if typ == "T":
                    ok = int(x @ T8 @ x) < 0
                else:
                    ok = float(7 * x @ C.PiS @ x - x @ T @ x) < -1e-9
                if ok:
                    out.append((typ, [int(t) for t in x]))
                    break
    return out


def kill_cuts(G, pool, rng, nimg):
    """cuts that kill the structure G; returns a short description, or None if no encoded lemma kills it."""
    pc = C.psd_cuts(G, maxcuts=8)
    if pc:
        for coeffs, rhs, (typ, xv) in pc:
            pool["PV"].append([typ, list(xv)])
            for _ in range(nimg):
                pool["PV"].append([typ, C.random_image(xv, rng)])
        nloc = 0
        if os.environ.get("LOCAL"):
            nli = int(os.environ.get("NIMG_LOCAL", "20"))
            for typ, xv in local_cuts(G):
                nloc += 1
                pool["PV"].append([typ, xv])
                for _ in range(nli):
                    pool["PV"].append([typ, C.random_image(xv, rng)])
        return "P+%d L+%d" % (len(pc), nloc)
    c = C.rl_violation(G)
    if c is not None:
        pool["R"].append([int(x) for x in c])
        return "R"
    b = C.b2_cut(G)
    if b is not None:
        pool["B2"].append(b)
        return "B2"
    return None


def main():
    poolf, statf, stage, secs = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
    cases = all_cases()
    lo, hi = 0, len(cases)
    if len(sys.argv) > 5 and "-" in sys.argv[5]:
        lo, hi = [int(t) for t in sys.argv[5].split("-")]
    seed = int(sys.argv[6]) if len(sys.argv) > 6 else 1
    nimg = int(os.environ.get("NIMG", "10"))
    rng = random.Random(seed)
    pool = json.load(open(poolf)) if os.path.exists(poolf) else {}
    for k in ("PV", "R", "B2"):
        pool.setdefault(k, [])
    status = json.load(open(statf)) if os.path.exists(statf) else {}
    for ci in range(lo, min(hi, len(cases))):
        case = cases[ci]
        key = "%d:%s" % (ci, "".join(map(str, case)))
        if status.get(key, {}).get("status") in ("INFEASIBLE", "SURVIVOR"):
            continue
        t0 = time.time()
        if stage == 0:
            m, e = build(case, pool, rng, use_cuts=False)
            sv, st = solve(m, secs, rng.randint(0, 10 ** 6))
            res = {"status": sv.StatusName(st), "stage": 0, "seconds": round(time.time() - t0, 1)}
        else:
            rounds, last = 0, None
            res = {"status": "UNKNOWN", "stage": 1}
            while time.time() - t0 < secs:
                rounds += 1
                m, e = build(case, pool, rng, use_cuts=True)
                sv, st = solve(m, max(5.0, secs - (time.time() - t0)), rng.randint(0, 10 ** 6))
                if st == cp_model.INFEASIBLE:
                    res = {"status": "INFEASIBLE", "stage": 1, "rounds": rounds}
                    break
                if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                    res = {"status": "UNKNOWN", "stage": 1, "rounds": rounds, "last": last}
                    break
                G = np.zeros((C.n, C.n), dtype=np.int64)
                for k, (i, j) in enumerate(C.PAIRS):
                    if sv.Value(e[k]):
                        G[i, j] = G[j, i] = 1
                T = (24 * np.eye(C.n) - 8 * G - C.K8) / 8.0
                last = round(float(min(C.perp_eigs(T)[0].min(), C.perp_eigs(7 * C.PiS - T)[0].min())), 3)
                how = kill_cuts(G, pool, rng, nimg)
                if os.environ.get("VERB"):
                    print("  round %d: %s, lambda_min %.3f, killed by %s (%.0f s)" % (rounds, sv.StatusName(st), last, how, time.time() - t0), flush=True)
                if how is None:
                    fn = os.path.join(HERE, "unbiased_walks", "case%d_survivor.json" % ci)
                    json.dump({"labels": [sorted(l) for l in C.S], "case": case,
                               "edges": [[i, j] for i, j in C.PAIRS if G[i, j]]}, open(fn, "w"))
                    res = {"status": "SURVIVOR", "stage": 1, "rounds": rounds, "file": fn}
                    break
                json.dump(pool, open(poolf, "w"))
            res["seconds"] = round(time.time() - t0, 1)
            res["lambda_last"] = last
        status[key] = res
        json.dump(status, open(statf, "w"), indent=0)
        json.dump(pool, open(poolf, "w"))
        print("case %s: %s" % (key, res), flush=True)
    tally = {}
    for k, v in status.items():
        tally[v["status"]] = tally.get(v["status"], 0) + 1
    print("TALLY over %d recorded cases: %s ; pool PV %d R %d B2 %d" % (len(status), tally, len(pool["PV"]), len(pool["R"]),
                                                                       len(pool["B2"])), flush=True)


if __name__ == "__main__":
    main()
