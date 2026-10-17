"""Bounded sweep of exact real-projector propagation, with gzip JSONL proofs."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import time

import numpy as np

from generic_star_apex_audit import cyclic_ball
from joint_generic_stars import prepare
from joint_star_propagation import propagate, replay
from two_star_core_ablation import MODES
from two_star_real_projector import LEVELS, exact_green, real_system


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ball", type=Path)
    parser.add_argument("--u", type=int, default=0)
    parser.add_argument("--v", type=int, default=12)
    parser.add_argument("--mode", choices=MODES, default="green")
    parser.add_argument("--level", choices=LEVELS, default="triples")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--max-apex", type=int, default=0)
    parser.add_argument("--indices", type=int, nargs="+")
    parser.add_argument("--seconds", type=float, default=180)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    started = time.monotonic()
    if args.verify_only:
        report = json.loads(args.out.read_text(encoding="utf-8"))
        g, (u, v), mode, level = report["adjacency"], report["centers"], report["pair_mode"], report["real_level"]
        proof_path = args.out.parent/report["proof_file"]
        assert hashlib.sha256(proof_path.read_bytes()).hexdigest() == report["proof_sha256"]
    else:
        g = json.loads(args.ball.read_text(encoding="utf-8"))["adjacency"] if args.ball else cyclic_ball()
        u, v, mode, level = args.u, args.v, args.mode, args.level
        proof_path = args.out.with_suffix(".proofs.jsonl.gz")
    prepared = prepare(g, u, v)
    green = exact_green(prepared)
    count = len(prepared[6])
    verified, norm_dead, propagation_dead, survivors = [], [], [], []

    def process(index, old=None):
        system, geometry = real_system(prepared, u, v, index, mode, level, green)
        if old is not None:
            assert old["index"] == index and old["geometry"] == geometry
        result = None
        if system is None:
            norm_dead.append(index)
        else:
            result = old["propagation"] if old is not None else propagate(system)
            replay(system, result)
            if result["contradiction"] is not None:
                propagation_dead.append(index)
            else:
                survivors.append(index)
        verified.append(index)
        if len(verified) % 25 == 0:
            print(json.dumps({"processed": len(verified), "norm_dead": len(norm_dead),
                "propagation_dead": len(propagation_dead), "survivors": len(survivors),
                "seconds": round(time.monotonic()-started, 1)}), flush=True)
        return {"index": index, "geometry": geometry, "propagation": result}

    if args.verify_only:
        with gzip.open(proof_path, "rt", encoding="utf-8") as stream:
            for expected, line in zip(report["processed_indices"], stream, strict=True):
                process(expected, json.loads(line))
        assert report["apex_candidates"] == count
        assert norm_dead == report["norm_contradictions"]
        assert propagation_dead == report["propagation_contradictions"]
        assert survivors == report["survivors"]
    else:
        end = count if args.max_apex == 0 else min(count, args.start+args.max_apex)
        requested = list(range(args.start, end)) if args.indices is None else args.indices
        assert requested == sorted(set(requested)) and all(0 <= i < count for i in requested)
        with gzip.open(proof_path, "wt", encoding="utf-8") as stream:
            for index in requested:
                if time.monotonic()-started >= args.seconds:
                    break
                stream.write(json.dumps(process(index), separators=(",", ":"))+"\n")
        report = {"ball": str(args.ball) if args.ball else "cyclic(2,4,1)", "adjacency": np.asarray(g).tolist(),
            "centers": [u, v], "pair_mode": mode, "real_level": level, "apex_candidates": count,
            "processed_indices": verified, "norm_contradictions": norm_dead,
            "propagation_contradictions": propagation_dead, "survivors": survivors,
            "proof_file": proof_path.name, "proof_sha256": hashlib.sha256(proof_path.read_bytes()).hexdigest(),
            "seconds": time.monotonic()-started, "scope": "one input ball; not a uniform or global rank exclusion"}
    complete = verified == list(range(count))
    conclusion = "ALL_APEX_BRANCHES_EXCLUDED_BY_REAL_FILTER_AND_PROPAGATION" if complete and not survivors else "PARTIAL_EXCLUSION"
    if args.verify_only:
        assert report["conclusion"] == conclusion
    else:
        report["conclusion"] = conclusion
        args.out.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"verified_replay": args.verify_only, "conclusion": conclusion,
        "processed": len(verified), "total": count, "norm_dead": len(norm_dead),
        "propagation_dead": len(propagation_dead), "survivors": survivors,
        "seconds": round(time.monotonic()-started, 2)}), flush=True)


if __name__ == "__main__":
    main()
