"""Solver-free support propagation for a fixed common apex of two stars.

Every deletion has an integer, mod-7 pair-support, or exact-sum reason.
The replay verifier rebuilds the domains and checks the complete trace.
This is a finite certificate for an apex branch, not a uniform lemma.
"""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

import numpy as np

from generic_star_apex_audit import cyclic_ball
from joint_generic_stars import branch_domains, prepare


def setup(prepared, u, v, apex):
    g, green, k, c4, pu, pv, commons = prepared
    common = commons[apex]
    labels, domains = branch_domains(green, u, v, pu, pv, common)
    arrays = [np.array([[int(p in s) for p in range(36)] for s in dom], dtype=np.int64).reshape(-1, 36)
              for dom in domains]
    w = np.array([int(p in common) for p in range(36)], dtype=np.int64)
    sides = [[i for i, label in enumerate(labels) if label[0] == side] for side in (0, 1)]
    targets = [k[:, center]-w for center in (u, v)]
    compat = {}
    saturated = [a@g+a == 2 for a in arrays]
    for i, j in combinations(range(18), 2):
        si, sj = labels[i][0], labels[j][0]
        ni, nj = arrays[i], arrays[j]
        prod = (ni@green@nj.T) % 7
        edge = 3-prod
        overlap = ni@nj.T
        good = ((edge == 0) | (edge == 1)) & (overlap <= 2-edge)
        # Internal and transverse degrees are 0/1, with their precise
        # candidate-dependent values forced by the mixed SRG equation.
        ci = 1-ni@g[(u, v)[si]] if si == sj else 2-ni@g[(u, v)[sj]]
        cj = 1-nj@g[(u, v)[sj]] if si == sj else 2-nj@g[(u, v)[si]]
        good &= (edge <= ci[:, None]) & (edge <= cj[None, :])
        good &= (edge == 0) | ((saturated[i].astype(np.int64)@nj.T == 0)
                              & (ni@saturated[j].T.astype(np.int64) == 0))
        # A shared pair of near points is already counted twice; add the
        # common apex once as well before comparing to its K entry.
        for a, b in zip(*np.nonzero(good & (overlap == 2))):
            shared = np.flatnonzero(ni[a] & nj[b])
            p, q = map(int, shared)
            if 2+int(w[p]*w[q]) > k[p, q]:
                good[a, b] = False
        compat[i, j], compat[j, i] = good, good.T
    return common, labels, arrays, sides, targets, compat


def propagate(system):
    common, labels, arrays, sides, targets, compat = system
    alive = [np.ones(len(a), dtype=bool) for a in arrays]
    trace = []

    def delete(i, removed, reason):
        removed = [int(c) for c in removed]
        if not removed:
            return False
        assert all(alive[i][c] for c in removed)
        event = {"variable": i, "removed": removed, **reason}
        trace.append(event)
        alive[i][removed] = False
        return True

    def finish(reason):
        return {"contradiction": reason, "trace": trace,
                "remaining_domain_sizes": [int(a.sum()) for a in alive],
                "deletion_counts": dict(Counter(e["kind"] for e in trace))}

    changed = True
    while changed:
        changed = False
        for i in range(18):
            if not alive[i].any():
                return finish({"kind": "empty_domain", "variable": i})
        for side, indices in enumerate(sides):
            minima = np.array([arrays[i][alive[i]].min(axis=0) for i in indices])
            maxima = np.array([arrays[i][alive[i]].max(axis=0) for i in indices])
            low, high = minima.sum(axis=0), maxima.sum(axis=0)
            impossible = np.flatnonzero((low > targets[side]) | (high < targets[side]))
            if len(impossible):
                p = int(impossible[0])
                return finish({"kind": "sum_outside_bounds", "side": side, "point": p,
                               "minimum": int(low[p]), "maximum": int(high[p]),
                               "target": int(targets[side][p])})
            for pos, i in enumerate(indices):
                bad = ((arrays[i]+(low-minima[pos]) > targets[side])
                       | (arrays[i]+(high-maxima[pos]) < targets[side]))
                # Use the first failing coordinate as an explicit reason.
                for p in range(36):
                    removed = np.flatnonzero(alive[i] & bad[:, p])
                    changed |= delete(i, removed, {"kind": "sum_support", "side": side, "point": p})
                    if not alive[i].any():
                        return finish({"kind": "empty_domain", "variable": i})
        for i in range(18):
            for j in range(18):
                if i == j:
                    continue
                supported = compat[i, j][:, alive[j]].any(axis=1)
                changed |= delete(i, np.flatnonzero(alive[i] & ~supported),
                                  {"kind": "pair_support", "other_variable": j})
                if not alive[i].any():
                    return finish({"kind": "empty_domain", "variable": i})
    return finish(None)


def replay(system, result):
    """Check each supplied deletion, without running the propagation algorithm.

    Current domains may be smaller than the snapshots used by the producer;
    this only strengthens a valid no-support or sum-bound reason.
    """
    common, labels, arrays, sides, targets, compat = system
    alive = [set(range(len(a))) for a in arrays]
    for event in result["trace"]:
        i, removed = event["variable"], event["removed"]
        assert 0 <= i < len(arrays) and removed
        assert len(set(removed)) == len(removed) and set(removed) <= alive[i]
        if event["kind"] == "pair_support":
            j = event["other_variable"]
            assert 0 <= j < len(arrays) and j != i
            for c in removed:
                assert not any(bool(compat[i, j][c, d]) for d in alive[j])
        elif event["kind"] == "sum_support":
            side, p = event["side"], event["point"]
            assert side in (0, 1) and i in sides[side] and 0 <= p < 36
            others = [j for j in sides[side] if j != i]
            assert all(alive[j] for j in others)
            low = sum(min(int(arrays[j][d, p]) for d in alive[j]) for j in others)
            high = sum(max(int(arrays[j][d, p]) for d in alive[j]) for j in others)
            for c in removed:
                target = int(targets[side][p])-int(arrays[i][c, p])
                assert target < low or target > high
        else:
            raise AssertionError("unknown deletion reason")
        alive[i].difference_update(removed)
    reason = result["contradiction"]
    if reason is not None:
        if reason["kind"] == "empty_domain":
            assert not alive[reason["variable"]]
        elif reason["kind"] == "sum_outside_bounds":
            side, p = reason["side"], reason["point"]
            assert all(alive[i] for i in sides[side])
            low = sum(min(int(arrays[i][c, p]) for c in alive[i]) for i in sides[side])
            high = sum(max(int(arrays[i][c, p]) for c in alive[i]) for i in sides[side])
            target = int(targets[side][p])
            assert (low, high, target) == (reason["minimum"], reason["maximum"], reason["target"])
            assert target < low or target > high
        else:
            raise AssertionError("unknown terminal reason")
    assert [len(a) for a in alive] == result["remaining_domain_sizes"]
    assert dict(Counter(e["kind"] for e in result["trace"])) == result["deletion_counts"]
    return alive


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ball", type=Path)
    parser.add_argument("--u", type=int, default=0)
    parser.add_argument("--v", type=int, default=12)
    parser.add_argument("--apex", type=int, default=0)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    g0 = json.loads(args.ball.read_text(encoding="utf-8"))["adjacency"] if args.ball else cyclic_ball()
    prepared = prepare(g0, args.u, args.v)
    system = setup(prepared, args.u, args.v, args.apex)
    old = json.loads(args.out.read_text(encoding="utf-8")) if args.verify_only else None
    result = old["propagation"] if old else propagate(system)
    replay(system, result)
    report = {"ball": str(args.ball) if args.ball else "cyclic(2,4,1)", "centers": [args.u, args.v], "common_apex_index": args.apex,
              "common_apex_support": list(system[0]), "variable_labels": [list(t) for t in system[1]],
              "initial_domain_sizes": [len(a) for a in system[2]], "propagation": result,
              "scope": "one fixed common-apex branch; no full-ball or uniform exclusion"}
    if old:
        assert report == old
    else:
        args.out.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"apex": args.apex, "contradiction": result["contradiction"],
                      "deletion_counts": result["deletion_counts"],
                      "remaining": result["remaining_domain_sizes"]}))


if __name__ == "__main__":
    main()
