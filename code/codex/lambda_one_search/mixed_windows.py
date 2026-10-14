"""Construct SRG(243,22,1,2) completions of mixed boundaries, without symmetry.

Reuses Claude LAB's exact compatible-row engine (message 659). Adds explicit
mixed boundaries, bounded row enumeration, progress files, and independent
integer SRG verification plus BLISS identification/automorphism counts.
No claim of exhaustiveness is made after any enumeration/search limit.
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
sys.path.insert(0, str(HERE / "lab_engine"))
import boundary_census as BC
import row_census as RC


def load(path):
    edges = [tuple(map(int, line.split())) for line in Path(path).read_text().splitlines() if line.strip()]
    n = 1+max(max(edge) for edge in edges)
    A = np.zeros((n, n), dtype=np.int64)
    for u, v in edges:
        A[u, v] = A[v, u] = 1
    return A


def graph(A):
    return ig.Graph(n=len(A), edges=list(zip(*np.where(np.triu(A, 1)))))


def verify(A, k=22, lam=1, mu=2):
    return bool(
        np.array_equal(A, A.T) and not np.diag(A).any()
        and np.all((A == 0) | (A == 1)) and np.all(A.sum(1) == k)
        and np.array_equal(A @ A + (mu-lam)*A, (k-mu)*np.eye(len(A), dtype=np.int64) + mu)
    )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--graph", choices=["6", "8"], required=True)
    p.add_argument("--mix", default="36,7,7", help="numbers kept in blocks 0,1,2")
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--row-seconds", type=float, default=20)
    p.add_argument("--rows-seconds", type=float, default=600)
    p.add_argument("--search-seconds", type=float, default=300)
    p.add_argument("--row-cap", type=int, default=6000)
    p.add_argument("--max-solutions", type=int, default=5000)
    p.add_argument("--probe", type=int, default=0, help="stop after this many rows, if positive")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    src = ROOT / "data/codex_asymmetry_synthesis_20261014/lab_sources"
    path = src / ("new243_trade_aut108.edges" if args.graph == "6" else "new243_trade_aut108_b.edges")
    A0 = load(path)
    assert verify(A0)
    rng = random.Random(args.seed)
    counts = list(map(int, args.mix.split(",")))
    assert len(counts) == 3 and all(0 <= c <= 81 for c in counts)
    R = sorted(v for b, count in enumerate(counts) for v in rng.sample(range(81*b, 81*(b+1)), count))
    g0 = graph(A0)
    color = [int(v in set(R)) for v in range(243)]
    stabilizer = g0.count_automorphisms(color=color)
    info = {"graph": args.graph, "source": str(path), "mix": counts, "seed": args.seed,
            "R": R, "set_stabilizer_order": stabilizer, "row_records": [],
            "status": "running", "target": "SRG(243,22,1,2) with full Aut order 1"}
    def save():
        (args.output / "result.json").write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
    save()
    print(json.dumps({k: info[k] for k in ["graph", "mix", "seed", "set_stabilizer_order"]}), flush=True)
    started = time.monotonic()

    def rows_of(adj, R, Rs, F, f0, cap):
        t0 = time.monotonic()
        deadline = min(t0 + args.row_seconds, started + args.rows_seconds)
        var = {g: i+1 for i, g in enumerate(v for v in F if v != f0)}
        nv = [len(var)]
        cls = []
        def new():
            nv[0] += 1
            return nv[0]
        for r in R:
            RC.counter(cls.append, new, [var[g] for g in sorted(adj[r] - Rs) if g != f0],
                       (1 if f0 in adj[r] else 2) - len(adj[r] & adj[f0] & Rs))
        RC.counter(cls.append, new, list(var.values()), 22 - len(adj[f0] & Rs))
        for g in var:
            if len(adj[g] & adj[f0] & Rs) == 2:
                cls.append([-var[g]])
        for g, h in itertools.combinations(sorted(var), 2):
            if len(adj[g] & adj[h] & Rs) == 2:
                cls.append([-var[g], -var[h]])
        solver = pycryptosat.Solver(threads=1)
        solver.add_clauses(cls)
        rows = []
        complete = False
        reason = "row_cap"
        while len(rows) <= cap:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                reason = "time_limit"
                break
            sat, solution = solver.solve(time_limit=remaining)
            if sat is False:
                complete = True
                reason = "enumerated"
                break
            if sat is None:
                reason = "time_limit"
                break
            N = [g for g in var if solution[var[g]]]
            rows.append(N)
            solver.add_clause([-var[g] for g in N])
        old = adj[f0] - Rs
        if complete:
            assert any(set(row) == old for row in rows), "Input graph missing from row domain"
        rec = {"vertex": f0, "rows": len(rows), "complete": complete, "reason": reason,
               "seconds": round(time.monotonic()-t0, 4)}
        info["row_records"].append(rec)
        save()
        if len(info["row_records"]) % 10 == 0 or not complete or len(rows) > 1:
            print(json.dumps(rec), flush=True)
        if args.probe and len(info["row_records"]) >= args.probe:
            info["stop_reason"] = "probe_complete"
            return None
        if not complete:
            info["stop_reason"] = reason
            return None
        # Explore changed rows first; this does not remove any candidates.
        rows.sort(key=lambda row: (set(row) == old, -len(set(row) ^ old)))
        return rows

    BC.rows_of = rows_of
    BC.ROWCAP = args.row_cap
    matrices, status, search_info = BC.completions(A0, R, args.search_seconds, args.max_solutions)
    info["status"] = info.get("stop_reason", status)
    info["search_info"] = search_info
    info["completions"] = len(matrices)
    refs = sorted((ROOT / "data/srg243").rglob("*.edges")) + sorted(src.glob("*.edges"))
    known = [(str(f.relative_to(ROOT)), graph(load(f))) for f in refs]
    tally = Counter()
    discoveries = []
    for i, A in enumerate(matrices):
        assert verify(A), "Completion failed exact SRG check"
        g = graph(A)
        hit = next((name for name, h in known if g.isomorphic_bliss(h)), None)
        if hit is None:
            order = g.count_automorphisms()
            name = f"candidate_{i}_aut{order}.edges"
            (args.output / name).write_text("".join(f"{u} {v}\n" for u, v in zip(*np.where(np.triu(A, 1)))), encoding="ascii")
            known.append((name, g))
            discoveries.append({"file": name, "automorphism_group_order": order, "exact_srg_check": True})
            hit = name
            print("NEW " + json.dumps(discoveries[-1]), flush=True)
        tally[hit] += 1
    info["by_isomorphism_class"] = dict(tally)
    info["discoveries"] = discoveries
    info["success"] = any(d["automorphism_group_order"] == 1 for d in discoveries)
    info["seconds"] = round(time.monotonic()-started, 4)
    save()
    print("FINAL " + json.dumps({k: info[k] for k in ["status", "completions", "by_isomorphism_class", "discoveries", "seconds"]}), flush=True)


if __name__ == "__main__":
    main()
