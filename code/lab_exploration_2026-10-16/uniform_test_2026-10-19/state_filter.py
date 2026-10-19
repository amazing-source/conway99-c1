"""Exact second-order state filter (LAB 19/10/2026): local consistency of row states, no solver.
For a label w of rectangle q with state z (z_f = |N(w) cap Q_f|), its 12 neighbours satisfy, for EVERY rectangle F,
   sum_{v ~ w} z_v(F) = 8 - z(F) - 2 |q cap F| + 12 [q = F]          (lambda = 1, mu = 2, common letters; derived by hand)
and exactly z(f) of them lie in Q_f, each with a state s of Q_f such that s(q) >= 1 (it has the neighbour w in Q_q).
A state for which no multiset of neighbour states (z(f) states of Q_f for every f) meets all 21 equations cannot be
the state of any label: it is removed.  Repeat on the reduced catalogues until nothing changes (arc consistency).
Only removes impossible states (every removal is a finite exhaustive check), so the reduced catalogue still contains
the state of every label of any realisation; an empty rectangle catalogue excludes the template.
usage: python state_filter.py <codex code dir> <catalogue.json.gz> <index> [--max-rounds=10] [--out=reduced.json]"""
import gzip
import json
import sys
import time
from itertools import combinations_with_replacement
from pathlib import Path

CODEX, CAT, IDX = sys.argv[1], sys.argv[2], int(sys.argv[3])
ROUNDS = int(next((a.split('=')[1] for a in sys.argv if a.startswith('--max-rounds=')), 10))
OUT = next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--out=')), None)
sys.path.insert(0, CODEX)
from root_component_z_distribution import RECTANGLES, row_catalogue      # noqa: E402

R = [tuple(q) for q in RECTANGLES]
template = json.loads(gzip.decompress(Path(CAT).read_bytes()))['open'][IDX]['template']
cat = row_catalogue(template, max_free=8)
states = [set(tuple(z) for z in item['states']) for item in cat['row_types']]


def target(qi, z):
    q = R[qi]
    return tuple(8 - z[F] - 2 * len(set(q) & set(R[F])) + (12 if F == qi else 0) for F in range(21))


def feasible(qi, z, states):
    goal = target(qi, z)
    reach = {tuple([0] * 21)}
    order = sorted((f for f in range(21) if z[f]), key=lambda f: len(states[f]))
    for k, f in enumerate(order):
        cand = [s for s in states[f] if s[qi] >= 1]
        if not cand:
            return False
        sums = set()
        for combo in combinations_with_replacement(cand, z[f]):
            sums.add(tuple(map(sum, zip(*combo))))
        new = set()
        rest = order[k + 1:]
        # bound: the remaining rectangles add between their minimal and maximal possible sums
        lo = [0] * 21
        hi = [0] * 21
        for g in rest:
            cg = [s for s in states[g] if s[qi] >= 1]
            for F in range(21):
                vals = [s[F] for s in cg] or [0]
                lo[F] += z[g] * min(vals); hi[F] += z[g] * max(vals)
        for p in reach:
            for s in sums:
                v = tuple(a + b for a, b in zip(p, s))
                if all(lo[F] <= goal[F] - v[F] <= hi[F] for F in range(21)):
                    new.add(v)
        reach = new
        if not reach:
            return False
    return goal in reach


t0 = time.process_time()
history = []
for rnd in range(ROUNDS):
    removed = 0
    for qi in range(21):
        keep = {z for z in states[qi] if feasible(qi, z, states)}
        removed += len(states[qi]) - len(keep)
        states[qi] = keep
    history.append({'round': rnd, 'removed': removed, 'state_counts': [len(s) for s in states],
                    'cpu': round(time.process_time() - t0, 1)})
    print(json.dumps(history[-1]), flush=True)
    if removed == 0 or any(not s for s in states):
        break
res = {'index': IDX, 'initial_counts': [r['state_count'] for r in cat['row_types']],
       'final_counts': [len(s) for s in states], 'excluded_by_empty_catalogue': any(not s for s in states),
       'history': history, 'cpu': round(time.process_time() - t0, 1)}
if OUT:
    json.dump({'index': IDX, 'states': [sorted(map(list, s)) for s in states], 'result': res}, open(OUT, 'w'))
print(json.dumps({k: res[k] for k in ('index', 'initial_counts', 'final_counts', 'excluded_by_empty_catalogue', 'cpu')}))
