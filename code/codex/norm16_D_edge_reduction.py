"""Apply the necessary D-edge restrictions proved in note253."""
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    cores = [c for c in json.loads((ROOT/'data/codex_norm16_cores.json').read_text())['cases']
             if c['representatives']]
    attachments = json.loads((ROOT/'data/codex_norm16_attachments_rank.json').read_text())['cases']
    out = []
    for ci, (core, case) in enumerate(zip(cores, attachments)):
        b = core['representatives'][0]
        a = [[0]*16 for _ in range(16)]
        for i in range(8):
            for j in range(8):
                a[i][8+j] = a[8+j][i] = b[i][j]
        hist = Counter()
        total = raw = 0
        orbits = []
        for oi, orbit in enumerate(case['orbits']):
            ss = [set(row[:2]) | {8+q for q in row[2:]} for row in orbit['representative']]
            c = [[len(u & v) for v in ss] for u in ss]
            edges = []
            for i, j in combinations(range(8), 2):
                if c[i][j] > 1:
                    continue
                if any(sum(a[v][u] for u in ss[i])+(v in ss[j]) > 2-(v in ss[i]) or
                       sum(a[v][u] for u in ss[j])+(v in ss[i]) > 2-(v in ss[j])
                       for v in range(16)):
                    continue
                raw += 1
                if c[i][j] or any(c[i][k]+c[j][k] > 2 for k in range(8) if k not in (i, j)):
                    continue
                edges.append([i, j])
            hist[len(edges)] += 1
            total += len(edges)
            orbits.append({'orbit': oi, 'eligible_edges': edges})
        out.append({'case': ci, 'core': core['defect_cycle_lengths'], 'before_note253': raw,
                    'after_note253': total, 'histogram': dict(hist), 'orbits': orbits})
    result = {'scope': 'Necessary edge filters of note253 plus local core-D common-neighbour bounds. Unquotiented D endpoint labels.',
              'cases': out}
    (ROOT/'data/codex_norm16_D_edge_reduction.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'before': sum(c['before_note253'] for c in out),
                      'after': sum(c['after_note253'] for c in out)}))


if __name__ == '__main__':
    main()
