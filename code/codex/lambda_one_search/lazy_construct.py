"""Construct asymmetric SRG(243,22,1,2) by lazy exact SAT constraints.

Fixed boundary equations and degrees are encoded first. Forbidden diamonds
(an edge with two common neighbours) and K2,3 witnesses are separated from
each SAT candidate. For a 22-regular graph of order 243, these upper bounds
force ALL SRG equalities: for each vertex, both the actual and permitted sums
of off-diagonal common-neighbour counts equal 22*21 = 462.

Repeatedly violated pairs receive their complete quadratic equation. Every
nontrivial automorphism found in a completed SRG produces a clause requiring
that permutation to fail for subsequent graphs. These cuts are necessary
for Aut=1 and never impose a nontrivial symmetry on the graph sought.
"""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys
import time

import numpy as np
import pycryptosat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
from mixed_windows import load, graph, verify
sys.path.insert(0, str(HERE / "lab_engine"))
from row_census import counter


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--graph", choices=["6", "8"], required=True)
    p.add_argument("--mix", default="24,8,8")
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--star-root", type=int)
    p.add_argument("--star-extra", type=int, default=0)
    p.add_argument("--seconds", type=float, default=900)
    p.add_argument("--solve-seconds", type=float, default=30)
    p.add_argument("--witnesses", type=int, default=2)
    p.add_argument("--materialize-after", type=int, default=3)
    p.add_argument("--max-materialized", type=int, default=1000)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.seed)
    src = ROOT / "data/codex_asymmetry_synthesis_20261014/lab_sources"
    path = src / ("new243_trade_aut108.edges" if args.graph == "6" else "new243_trade_aut108_b.edges")
    A0 = load(path)
    assert verify(A0)
    mix = list(map(int, args.mix.split(",")))
    R = sorted(v for b, count in enumerate(mix) for v in rng.sample(range(81*b, 81*(b+1)), count))
    if args.star_root is not None:
        star = {args.star_root} | set(map(int, np.flatnonzero(A0[args.star_root])))
        R = sorted(star | set(rng.sample(sorted(set(range(243))-star), args.star_extra)))
    Rs = set(R)
    F = [v for v in range(243) if v not in Rs]
    C = A0[:, R] @ A0[R, :]
    forbidden = C >= 2
    saturated = C[R, :] == 2-A0[R, :]
    forbidden |= (A0[:, R] @ saturated.astype(np.int64)) > 0
    forbidden |= forbidden.T
    assert not any(A0[u, v] and forbidden[u, v] for u, v in itertools.combinations(F, 2))
    pairs = [(u, v) for u, v in itertools.combinations(F, 2) if not forbidden[u, v]]
    rng.shuffle(pairs)
    ids = np.zeros((243, 243), dtype=np.int64)
    for i, (u, v) in enumerate(pairs, 1):
        ids[u, v] = ids[v, u] = i
    nv = [len(pairs)]
    stats = Counter()
    solver = pycryptosat.Solver(threads=1)
    def new():
        nv[0] += 1
        return nv[0]
    def emit(clause):
        solver.add_clause(list(map(int, clause)))
        stats["clauses"] += 1
    start = time.monotonic()
    deadline = start+args.seconds
    report = {"graph": args.graph, "mix": mix, "seed": args.seed, "R": R,
              "star_root": args.star_root, "star_extra": args.star_extra if args.star_root is not None else None,
              "edge_variables": len(pairs), "status": "encoding",
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "exact_target": [243, 22, 1, 2], "target_automorphism_order": 1,
              "limits": vars(args) | {"output": str(args.output)}}
    discovered = []
    last_print = [0.0]
    def save():
        report.update(seconds=round(time.monotonic()-start, 3), stats=dict(stats),
                      total_variables=nv[0], discoveries=discovered)
        (args.output / "result.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    save()
    for f in F:
        counter(emit, new, [int(ids[f, g]) for g in F if ids[f, g]], 22-int(A0[f, R].sum()))
    for r in R:
        for f in F:
            lits = [int(ids[f, g]) for g in F if A0[r, g] and ids[f, g]]
            counter(emit, new, lits, 2-int(A0[r, f])-int(C[r, f]))
    report["encoding_seconds"] = round(time.monotonic()-start, 3)
    print("ENCODED " + json.dumps({"edges": len(pairs), "vars": nv[0], "clauses": stats["clauses"],
                                  "seconds": report["encoding_seconds"]}), flush=True)
    # A known full SRG is a cheap meaningful positive check of the base model.
    sat, _ = solver.solve(assumptions=[i for i, (u, v) in enumerate(pairs, 1) if A0[u, v]], time_limit=30)
    assert sat is True, "The seed SRG must satisfy the uncut boundary model"
    report["seed_satisfies_base_model"] = True
    xor_cache = {}
    aut_cuts = set()
    def break_automorphism(perm):
        perm = tuple(map(int, perm))
        if perm in aut_cuts or perm == tuple(range(243)):
            return False
        diffs = set()
        for u, v in itertools.combinations(range(243), 2):
            a, b = int(ids[u, v]), int(ids[perm[u], perm[v]])
            if a and b:
                if a == b:
                    continue
                key = tuple(sorted((a, b)))
                if key not in xor_cache:
                    d = new()
                    solver.add_xor_clause([a, b, d], False)
                    stats["xor_definitions"] += 1
                    xor_cache[key] = d
                diffs.add(xor_cache[key])
            elif a:
                diffs.add(-a if A0[perm[u], perm[v]] else a)
            elif b:
                diffs.add(-b if A0[u, v] else b)
            elif A0[u, v] != A0[perm[u], perm[v]]:
                return False  # Already broken by fixed entries.
        emit(sorted(diffs))
        aut_cuts.add(perm)
        stats["nontrivial_automorphisms_forbidden"] += 1
        return True
    for perm in graph(A0).automorphism_group():
        break_automorphism(perm)
    and_cache = {}
    materialized = set()
    pair_hits = Counter()
    def complete_pair(u, v):
        items = []
        constant = 0
        for h in range(243):
            if h == u or h == v:
                continue
            a, b = int(ids[u, h]), int(ids[v, h])
            if a and b:
                key = tuple(sorted((a, b)))
                if key not in and_cache:
                    z = new()
                    emit([-z, a]); emit([-z, b]); emit([z, -a, -b])
                    and_cache[key] = z
                items.append(and_cache[key])
            elif a:
                if A0[v, h]: items.append(a)
            elif b:
                if A0[u, h]: items.append(b)
            else:
                constant += int(A0[u, h] and A0[v, h])
        if ids[u, v]:
            items.append(int(ids[u, v]))
        else:
            constant += int(A0[u, v])
        counter(emit, new, items, 2-constant)
        materialized.add((u, v))
        stats["materialized_pair_equations"] += 1
    witness_cache = set()
    def forbid_edges(edges):
        clause = []
        for u, v in edges:
            if ids[u, v]: clause.append(-int(ids[u, v]))
            else: assert A0[u, v] == 1
        key = tuple(sorted(set(clause)))
        if key not in witness_cache:
            emit(key)
            witness_cache.add(key)
            stats["forbidden_common_neighbour_witnesses"] += 1
    refs = sorted((ROOT / "data/srg243").rglob("*.edges")) + sorted(src.glob("*.edges"))
    known = [(str(f.relative_to(ROOT)), graph(load(f))) for f in refs]
    report["status"] = "searching"
    save()
    while time.monotonic() < deadline:
        sat, sol = solver.solve(time_limit=min(args.solve_seconds, deadline-time.monotonic()))
        stats["solver_calls"] += 1
        if sat is False:
            report["status"] = "UNSAT_with_boundary_and_asymmetry_cuts"
            break
        if sat is None:
            stats["undecided_calls"] += 1
            save()
            print("WAIT " + json.dumps({"seconds": report["seconds"], "stats": dict(stats)}), flush=True)
            continue
        A = A0.copy()
        for i, (u, v) in enumerate(pairs, 1):
            A[u, v] = A[v, u] = int(sol[i])
        assert np.all(A.sum(1) == 22)
        common = A @ A
        bad = list(zip(*np.where(np.triu(common+A > 2, 1))))
        stats["regular_candidates"] += 1
        report["last_bad_pairs"] = len(bad)
        report["best_bad_pairs"] = min(report.get("best_bad_pairs", 100000), len(bad))
        if not bad:
            assert verify(A)
            g = graph(A)
            order = g.count_automorphisms()
            hit = next((name for name, h in known if g.isomorphic_bliss(h)), None)
            stats["exact_SRG_candidates"] += 1
            if hit is None:
                name = f"constructed_{len(discovered):03d}_aut{order}.edges"
                (args.output / name).write_text("".join(f"{u} {v}\n" for u, v in zip(*np.where(np.triu(A, 1)))), encoding="ascii")
                discovered.append({"file": name, "automorphism_group_order": order, "exact_srg_check": True})
                known.append((name, g))
            print("SRG " + json.dumps({"aut_order": order, "known": hit}), flush=True)
            if order == 1:
                report["status"] = "success_asymmetric_srg"
                break
            cuts = sum(break_automorphism(perm) for perm in g.automorphism_group())
            assert cuts, "Symmetric candidate must provide a new automorphism cut"
            save()
            continue
        rng.shuffle(bad)
        for u, v in bad:
            u, v = int(u), int(v)
            assert u not in Rs and v not in Rs
            pair_hits[(u, v)] += 1
            if pair_hits[(u, v)] >= args.materialize_after and len(materialized) < args.max_materialized:
                assert (u, v) not in materialized, "Materialized equation violated"
                complete_pair(u, v)
                continue
            neighbours = list(map(int, np.flatnonzero(A[u] & A[v])))
            rng.shuffle(neighbours)
            if A[u, v]:
                for a, b in itertools.islice(itertools.combinations(neighbours, 2), args.witnesses):
                    forbid_edges([(u,v),(u,a),(v,a),(u,b),(v,b)])
            if len(neighbours) >= 3:
                for triple in itertools.islice(itertools.combinations(neighbours, 3), args.witnesses):
                    forbid_edges([(z, h) for z in (u,v) for h in triple])
        save()
        if time.monotonic()-last_print[0] >= 5:
            print("PROGRESS " + json.dumps({"seconds": report["seconds"], "bad_pairs": len(bad),
                                            "best_bad_pairs": report["best_bad_pairs"], "stats": dict(stats)}), flush=True)
            last_print[0] = time.monotonic()
    if report["status"] == "searching":
        report["status"] = "time_limit_no_asymmetric_SRG"
    save()
    print("FINAL " + json.dumps(report), flush=True)


if __name__ == "__main__":
    main()
