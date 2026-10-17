"""Exact row domains and cross-row compatibility for mutated Hoffman designs.

Rows are enumerated by LAB's existing, scoped and documented C++ engine.
All 77 rows, reciprocity and exact common-neighbour counts are coupled.
An empty complete domain or an arc-consistency contradiction excludes the
whole fixed design, not just a local attempt. Incomplete enumeration stays
UNKNOWN. Surviving arc consistency is not called a graph completion.
"""
from collections import deque
from pathlib import Path
import argparse
import json
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'data/codex_hoffman_trades'


def instance(blocks):
    y = [[int(s in b) for b in blocks] for s in range(22)]
    lines = ['22 77'] + [' '.join(map(str, r)) for r in y]
    lines += ['10 ' + ' '.join(str(2-y[s][i]) for s in range(22)) for i in range(77)]
    return '\n'.join(lines) + '\n'


def arc_consistency(dom, blocks):
    n = len(dom)
    overlap = [[len(set(b)&set(c)) for c in blocks] for b in blocks]
    alive = [(1 << len(d))-1 for d in dom]
    support = {}
    deletions = []
    queue = deque((i,j) for i in range(n) for j in range(n) if i != j)
    queued = set(queue)
    while queue:
        i,j = queue.popleft()
        queued.discard((i,j))
        if (i,j) not in support:
            sd = []
            for x in dom[i]:
                edge = (x >> j)&1
                bits = 0
                for iy,y in enumerate(dom[j]):
                    if edge == ((y >> i)&1) and (x&y).bit_count()+overlap[i][j] == 2-edge:
                        bits |= 1 << iy
                sd.append(bits)
            support[i,j] = sd
        todo = alive[i]
        changed = False
        while todo:
            bit = todo & -todo
            todo -= bit
            ix = bit.bit_length()-1
            if not (support[i,j][ix] & alive[j]):
                alive[i] ^= bit
                deletions.append([i,ix,j])
                changed = True
        if not alive[i]:
            return dict(status='UNSAT_FIXED_DESIGN', reason='arc_consistency',
                        empty_row=i, deletions=deletions,
                        remaining_counts=[a.bit_count() for a in alive])
        if changed:
            for k in range(n):
                if k != i and k != j and (k,i) not in queued:
                    queue.append((k,i))
                    queued.add((k,i))
    return dict(status='ARC_CONSISTENT_NOT_DECIDED', remaining_counts=[a.bit_count() for a in alive],
                deletions=deletions)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-designs', type=int, default=36)
    ap.add_argument('--row-seconds', type=float, default=5)
    args = ap.parse_args()
    designs = json.loads((OUT/'two_point_trades.json').read_text())['new_designs'][:args.max_designs]
    start = time.monotonic()
    results = []
    for index, design in enumerate(designs):
        folder = OUT / ('design_' + design['key'][:12])
        folder.mkdir(exist_ok=True)
        inst = folder/'input.inst'
        inst.write_text(instance(design['blocks']))
        run_start = time.monotonic()
        process = subprocess.run([str(OUT/'rows22.exe'), str(inst), str(folder/'row'),
                                  str(args.row_seconds), '1000000'], capture_output=True, text=True,
                                 timeout=77*args.row_seconds+60, check=True)
        (folder/'rows.log').write_text(process.stdout)
        stats = [s.split() for s in process.stdout.splitlines() if s.strip()]
        assert len(stats) == 77
        counts = [int(s[1]) for s in stats]
        if any(s[3] == 'EXHAUSTED' and int(s[1]) == 0 for s in stats):
            status = dict(status='UNSAT_FIXED_DESIGN', reason='empty_complete_domain',
                          empty_row=next(int(s[0]) for s in stats if s[3]=='EXHAUSTED' and int(s[1])==0))
        elif any(s[3] != 'EXHAUSTED' for s in stats):
            status = dict(status='UNKNOWN', reason='incomplete_domain_enumeration')
        else:
            dom = [[sum(1 << int(j) for j in line.split())
                    for line in (folder/f'row_{i}.rows').read_text().splitlines()] for i in range(77)]
            assert [len(d) for d in dom] == counts
            status = arc_consistency(dom, design['blocks'])
        status.update(design_key=design['key'], automorphism_order=design['aut'],
                      domain_counts=counts, row_statistics=stats, elapsed_seconds=time.monotonic()-run_start)
        (folder/'result.json').write_text(json.dumps(status,indent=2))
        results.append({k:v for k,v in status.items() if k not in ('deletions','row_statistics','domain_counts')})
        (OUT/'completion_results.json').write_text(json.dumps(dict(results=results,
            elapsed_seconds=time.monotonic()-start, arguments=vars(args)),indent=2))
        print(index, design['key'][:12], 'Aut',design['aut'], status['status'],status.get('reason'),
              'domains', min(counts), max(counts),'seconds',round(status['elapsed_seconds'],3),flush=True)


if __name__ == '__main__':
    main()
