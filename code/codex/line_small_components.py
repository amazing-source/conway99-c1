"""Enumerate necessary coloured cubic line-neighbourhood components of size6s.

Three colour classes have n=2s vertices each, with one neighbour of every
colour. Normalize two cross matchings to identity and the first internal
matching to (0 1)(2 3)... . All remaining permutations/matchings are tried.
Pair codegree upper bounds account for the shared vertex on the root line.
"""

import argparse
from collections import Counter
from itertools import permutations
import json
from pathlib import Path
import time


def matchings(vertices):
    if not vertices:
        yield ()
        return
    a = vertices[0]
    for i, b in enumerate(vertices[1:], 1):
        for rest in matchings(vertices[1:i] + vertices[i+1:]):
            yield ((a, b),) + rest


def enumerate_components(n):
    started = time.monotonic()
    ms = list(matchings(tuple(range(n))))
    histogram = Counter()
    witnesses = {}
    counts = Counter()
    for p in permutations(range(n)):
        for m1 in ms:
            for m2 in ms:
                masks = [0] * (3*n)
                def edge(a, b):
                    masks[a] |= 1 << b
                    masks[b] |= 1 << a
                for i in range(n):
                    edge(i, n+i)
                    edge(i, 2*n+i)
                    edge(n+i, 2*n+p[i])
                for offset, matching in ((0, tuple((i, i+1) for i in range(0,n,2))), (n,m1), (2*n,m2)):
                    for i, j in matching:
                        edge(offset+i, offset+j)
                counts["candidates"] += 1
                bad = False
                for i in range(3*n):
                    for j in range(i):
                        adj = (masks[i] >> j) & 1
                        if (masks[i] & masks[j]).bit_count() > 2 - adj - int(i//n == j//n):
                            bad = True
                            break
                    if bad:
                        break
                if bad:
                    continue
                seen, frontier = 0, 1
                while frontier:
                    bit = frontier & -frontier
                    frontier ^= bit
                    seen |= bit
                    frontier |= masks[bit.bit_length()-1] & ~seen
                if seen.bit_count() != 3*n:
                    counts["disconnected"] += 1
                    continue
                triangles6 = sum((masks[i] & masks[j]).bit_count() for i in range(3*n) for j in range(3*n)
                                 if (masks[i] >> j) & 1)
                assert triangles6 % 6 == 0
                triangles = triangles6 // 6
                histogram[triangles] += 1
                witnesses.setdefault(triangles, {"cross_permutation": p, "internal_matchings": [m1, m2],
                    "edges": [[i,j] for i in range(3*n) for j in range(i) if (masks[i] >> j)&1]})
    return {"vertices": 3*n, "counts": dict(counts), "triangle_histogram": dict(sorted(histogram.items())),
            "witnesses": witnesses, "seconds": time.monotonic()-started,
            "scope": "Complete necessary component enumeration, not SRG completion."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sizes", type=int, nargs="+", default=[2,4,6])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    results = []
    for n in args.sizes:
        result = enumerate_components(n)
        results.append(result)
        args.output.write_text(json.dumps({"records": results}, separators=(",", ":"))+"\n", encoding="utf-8")
        print(json.dumps({k:v for k,v in result.items() if k != "witnesses"}), flush=True)


if __name__ == "__main__":
    main()
