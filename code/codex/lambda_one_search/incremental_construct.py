"""Construct lambda-one SRGs by assigning complete rows incrementally.

Starts from the mixed boundary of a known (243,22,1,2) graph. At each node,
CryptoMiniSat produces possible complete neighbourhoods for one more vertex.
The chosen row becomes part of the fixed boundary before the next SAT call.
Every returned graph is checked exactly, then its full group is computed.

This is a construction search, NOT a census: time and candidate limits may
leave branches unexplored. Optional X pruning uses Claude LAB's reported
classification of completions containing the folded Hamming 81-vertex graph.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random
import sys
import time

import igraph as ig
import numpy as np
import pycryptosat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
from mixed_windows import load, graph, verify
sys.path.insert(0, str(HERE / "lab_engine"))
from row_census import counter


def folded_hamming():
    vertices = list(itertools.product(range(3), repeat=4))
    idx = {v: i for i, v in enumerate(vertices)}
    directions = [tuple(int(i == j) for i in range(4)) for j in range(4)] + [(1, 1, 1, 1)]
    edges = set()
    for i, v in enumerate(vertices):
        for d in directions:
            for sign in (1, -1):
                j = idx[tuple((x + sign*y) % 3 for x, y in zip(v, d))]
                edges.add(tuple(sorted((i, j))))
    return ig.Graph(n=81, edges=sorted(edges))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--graph", choices=["6", "8"], required=True)
    p.add_argument("--mix", default="30,10,10")
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--seconds", type=float, default=600)
    p.add_argument("--row-seconds", type=float, default=3)
    p.add_argument("--row-cap", type=int, default=24)
    p.add_argument("--node-cap", type=int, default=10000)
    p.add_argument("--solution-cap", type=int, default=500)
    p.add_argument("--prune-x", action="store_true")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    src = ROOT / "data/codex_asymmetry_synthesis_20261014/lab_sources"
    path = src / ("new243_trade_aut108.edges" if args.graph == "6" else "new243_trade_aut108_b.edges")
    A0 = load(path)
    assert verify(A0)
    rng = random.Random(args.seed)
    mix = list(map(int, args.mix.split(",")))
    assert len(mix) == 3 and all(0 <= c <= 81 for c in mix)
    R0 = sorted(v for b, count in enumerate(mix) for v in rng.sample(range(81*b, 81*(b+1)), count))
    g0 = graph(A0)
    order_R = g0.count_automorphisms(color=[int(v in set(R0)) for v in range(243)])
    refs = sorted((ROOT / "data/srg243").rglob("*.edges")) + sorted(src.glob("*.edges"))
    known = [(str(f.relative_to(ROOT)), graph(load(f))) for f in refs]
    X = folded_hamming()
    start = time.monotonic()
    deadline = start + args.seconds
    stats = Counter()
    tally = Counter()
    discoveries = []
    report = {"graph": args.graph, "source": str(path), "mix": mix, "seed": args.seed,
              "initial_R": R0, "initial_set_stabilizer_order": order_R,
              "prune_X_using_peer_classification": args.prune_x,
              "construction_search_not_census": True, "status": "running"}
    last_save = [0.0]
    best = [len(R0)]
    stop = [False]
    def save(force=False):
        now = time.monotonic()
        if not force and now-last_save[0] < 5:
            return
        report.update(stats=dict(stats), by_isomorphism_class=dict(tally), discoveries=discoveries,
                      seconds=round(now-start, 3), maximum_fixed_rows=best[0])
        (args.output / "result.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        last_save[0] = now
    save(True)
    print("START " + json.dumps(report), flush=True)

    def possible_rows(A, R, F, f, C):
        row_start = time.monotonic()
        row_deadline = min(deadline, row_start+args.row_seconds)
        variables = [g for g in F if g != f]
        rng.shuffle(variables)
        var = {g: i+1 for i, g in enumerate(variables)}
        nv = [len(var)]
        clauses = []
        def new():
            nv[0] += 1
            return nv[0]
        for r in R:
            lits = [var[g] for g in variables if A[r, g]]
            target = 2-int(A[r, f])-int(C[r, f])
            counter(clauses.append, new, lits, target)
        counter(clauses.append, new, list(var.values()), 22-int(A[f, R].sum()))
        for g in variables:
            if C[f, g] >= 2:
                clauses.append([-var[g]])
        for g, h in itertools.combinations(variables, 2):
            if C[g, h] >= 2:
                clauses.append([-var[g], -var[h]])
        solver = pycryptosat.Solver(threads=1)
        solver.add_clauses(clauses)
        rows = []
        complete = False
        while len(rows) < args.row_cap:
            remaining = row_deadline-time.monotonic()
            if remaining <= 0:
                break
            sat, sol = solver.solve(time_limit=remaining)
            if sat is False:
                complete = True
                break
            if sat is None:
                break
            N = tuple(g for g in variables if sol[var[g]])
            rows.append(N)
            solver.add_clause([-var[g] for g in N])
        if not complete:
            stats["incomplete_row_enumerations"] += 1
        stats["sat_rows_generated"] += len(rows)
        old = set(np.flatnonzero(A0[f]))
        # Changes first, but keep every row we have generated.
        rows.sort(key=lambda N: -len(set(N) ^ (old & set(F))))
        return rows, complete

    def record(A):
        assert verify(A), "A constructed candidate violates the exact SRG equations"
        stats["verified_completions"] += 1
        g = graph(A)
        hit = next((name for name, h in known if g.isomorphic_bliss(h)), None)
        if hit is None:
            aut = g.count_automorphisms()
            name = f"constructed_{len(discoveries):03d}_aut{aut}.edges"
            (args.output / name).write_text("".join(f"{u} {v}\n" for u, v in zip(*np.where(np.triu(A, 1)))), encoding="ascii")
            discoveries.append({"file": name, "aut_order": aut, "exact_srg_check": True})
            known.append((name, g))
            hit = name
            print("NEW " + json.dumps(discoveries[-1]), flush=True)
            if aut == 1:
                report["status"] = "success_asymmetric_srg"
                stop[0] = True
        tally[hit] += 1
        if stats["verified_completions"] >= args.solution_cap:
            stop[0] = True
        save(True)

    def search(A, R, checked_blocks):
        if stop[0] or time.monotonic() >= deadline or stats["nodes"] >= args.node_cap:
            return
        stats["nodes"] += 1
        if len(R) > best[0]:
            best[0] = len(R)
        Rs = set(R)
        F = [v for v in range(243) if v not in Rs]
        if not F:
            record(A)
            return
        if args.prune_x:
            for b in range(3):
                if b in checked_blocks:
                    continue
                S = list(range(81*b, 81*(b+1)))
                if sum(v not in Rs for v in S) <= 1:
                    checked_blocks = checked_blocks | {b}
                    if graph(A[np.ix_(S, S)]).isomorphic_bliss(X):
                        stats["known_X_branch_prunes"] += 1
                        save()
                        return
        C = A[:, R] @ A[R, :]
        sub = C[np.ix_(F, F)].copy()
        np.fill_diagonal(sub, 0)
        if (sub > 2).any() or (C[np.ix_(R, F)] > 2-A[np.ix_(R, F)]).any() or (A[np.ix_(F, R)].sum(1) > 22).any():
            stats["partial_count_contradictions"] += 1
            save()
            return
        # Most constrained first, with random ties and no symmetry constraints.
        degrees = [(int(A[f, R].sum()), rng.random(), f) for f in F]
        f = max(degrees)[2]
        rows, complete = possible_rows(A, R, F, f, C)
        if not rows:
            stats["unsat_row_nodes" if complete else "undecided_row_nodes"] += 1
            save()
            return
        if stats["nodes"] % 10 == 0 or len(rows) > 1:
            print(json.dumps({"node": stats["nodes"], "fixed": len(R), "vertex": f,
                              "rows": len(rows), "complete": complete, "seconds": round(time.monotonic()-start, 1)}), flush=True)
        save()
        old_row = A[f].copy()
        for N in rows:
            A[f, F] = 0
            A[F, f] = 0
            if N:
                A[f, list(N)] = 1
                A[list(N), f] = 1
            search(A, R+[f], checked_blocks)
            A[f, :] = old_row
            A[:, f] = old_row
            if stop[0] or time.monotonic() >= deadline or stats["nodes"] >= args.node_cap:
                break

    search(A0.copy(), R0, set())
    if report["status"] == "running":
        report["status"] = "search_limit" if time.monotonic() >= deadline or stats["nodes"] >= args.node_cap or stop[0] else "sampled_branches_finished"
    save(True)
    print("FINAL " + json.dumps(report), flush=True)


if __name__ == "__main__":
    main()
