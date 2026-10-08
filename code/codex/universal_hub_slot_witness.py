"""Exact witness: notes 108/109 slot equations do not exclude a universal hub.

This is a witness for aggregated necessary conditions, not an SRG or a
completion of the three neighbourhoods of a line in six grids.
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'code'))
from slot_calculus import CL, PAIRS, VERT, build, cls, propagate
from slot_tests import configs
from slot_second_order import special_d

PATH = ROOT / 'data/codex_universal_hub_slot_witness.json'


def setup():
    cfg = next(configs({(0, 0): {2, 3}, (1, 0): {2, 3}}))
    var, lo, hi, eqs, incomplete = build(cfg)
    ok, lo, hi, _ = propagate(lo, hi, eqs)
    assert ok
    return cfg, var, lo, hi, eqs, incomplete


def degree_table(cfg, var, values):
    return [[special_d(cfg, v, p) if cls(v) & p else values[var[v, p]]
             for v in VERT] for p in PAIRS]


def second_order(cfg, var, values):
    d = degree_table(cfg, var, values)
    checks = 0
    for i, p in enumerate(PAIRS):
        for j in range(i, len(PAIRS)):
            r = PAIRS[j]
            edges = sum(d[j][k] for k, v in enumerate(VERT) if cls(v) == p)
            lhs = sum(a * b for a, b in zip(d[i], d[j]))
            rhs = (64 if p == r else 24 if p & r else 32) - edges
            if lhs != rhs:
                return False, checks
            checks += 1
    return True, checks


def verify(report):
    cfg, var, lo, hi, eqs, incomplete = setup()
    assert report['scope'] == __doc__
    assert report['incomplete_pairs'] == sorted(sorted(p) for p in incomplete)
    values = report['slots']
    assert len(values) == len(lo) == 840
    assert all(type(x) is int and a <= x <= b for x, a, b in zip(values, lo, hi))
    assert all(sum(a * values[j] for j, a in row.items()) == rhs for row, rhs, _ in eqs)
    ok, count = second_order(cfg, var, values)
    assert ok and count == 231
    hubs = [c for c in CL if all(c not in p for p in incomplete)]
    assert hubs == report['universal_hubs'] == [4, 5, 6]
    # A universal hub h forces n_{h,k}(v)=1 when h is not in cls(v).
    for h in hubs:
        for v in VERT:
            if h in cls(v):
                continue
            for k in CL:
                p = frozenset((h, k))
                if k != h and not (p & cls(v)):
                    assert values[var[v, p]] == 1
    # In the reverse direction, the four row degrees need not equal one.
    nonmatching = []
    d = degree_table(cfg, var, values)
    for h in hubs:
        for i, p in enumerate(PAIRS):
            if h not in p:
                continue
            for j, r in enumerate(PAIRS):
                if p & r:
                    continue
                degrees = [d[j][k] for k, v in enumerate(VERT) if cls(v) == p]
                if degrees != [1, 1, 1, 1]:
                    assert sum(degrees) == 4
                    nonmatching.append({'source': sorted(p), 'target': sorted(r), 'degrees': degrees})
    assert nonmatching and report['nonmatching_examples'] == nonmatching
    print('Verified exactly:', len(eqs), 'linear equations;', count,
          'second-order equations; hubs', hubs, '; nonmatching directions', len(nonmatching), flush=True)


def generate():
    cfg, var, lo, hi, eqs, incomplete = setup()
    free = [j for j in range(len(lo)) if lo[j] < hi[j]]
    free_set = set(free)
    rows = []
    for row, rhs, _ in eqs:
        part = {j: a for j, a in row.items() if j in free_set}
        if part:
            rows.append((part, rhs - sum(a * lo[j] for j, a in row.items() if j not in free_set)))
    order = sorted(free, key=lambda j: -sum(j in row for row, _ in rows))
    incident = {j: [(row, rhs) for row, rhs in rows if j in row] for j in order}
    current = {}
    trials = 0

    def rec(k):
        nonlocal trials
        if k == len(order):
            values = [current.get(j, v) for j, v in enumerate(lo)]
            trials += 1
            return values if second_order(cfg, var, values)[0] else None
        j = order[k]
        for value in range(lo[j], hi[j] + 1):
            current[j] = value
            possible = True
            for row, rhs in incident[j]:
                minimum = maximum = 0
                for t, a in row.items():
                    if t in current:
                        minimum += a * current[t]
                        maximum += a * current[t]
                    else:
                        minimum += a * (lo[t] if a > 0 else hi[t])
                        maximum += a * (hi[t] if a > 0 else lo[t])
                if not minimum <= rhs <= maximum:
                    possible = False
                    break
            if possible:
                found = rec(k + 1)
                if found is not None:
                    return found
            del current[j]
        return None

    values = rec(0)
    assert values is not None
    d = degree_table(cfg, var, values)
    examples = []
    for h in (4, 5, 6):
        for i, p in enumerate(PAIRS):
            if h not in p:
                continue
            for j, r in enumerate(PAIRS):
                if p & r:
                    continue
                degrees = [d[j][k] for k, v in enumerate(VERT) if cls(v) == p]
                if degrees != [1, 1, 1, 1]:
                    examples.append({'source': sorted(p), 'target': sorted(r), 'degrees': degrees})
    report = {'scope': __doc__, 'universal_hubs': [4, 5, 6],
              'incomplete_pairs': sorted(sorted(p) for p in incomplete),
              'slots': values, 'nonmatching_examples': examples}
    verify(report)
    PATH.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('Witness found after', trials, 'complete linear solutions.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    if args.verify_only:
        verify(json.loads(PATH.read_text(encoding='utf-8')))
    else:
        generate()
