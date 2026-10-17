"""Search balanced star exchanges using the entire gray-block relaxation.

This repairs the twelve-row star of a supplied frame. Any extra fixed
rows from that frame are released explicitly. A successful binary linear
relaxation is not a Conway graph and not a replacement fifteen-row frame.
"""
import argparse
from collections import deque
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from conway_gray_block import read_frame, solve_relaxation
from conway_star_trades import balanced_trades, verify_partial


def search(source, output, seconds=1, max_states=40, time_limit=45):
    started = time.monotonic()
    labels, original = read_frame(source)
    fixed = {z:row for z,row in original.items() if 4 in labels[z]}
    assert len(fixed) == 12
    star = sorted(fixed)
    def key(rows):
        return tuple(tuple(rows[z]) for z in star)
    queue = deque([(fixed, [])])
    seen = {key(fixed)}
    attempts = []
    result = dict(source_file=str(source), released_extra_rows=[labels[z] for z in original if z not in fixed],
                  solver_seconds_per_state=seconds, max_states=max_states, time_limit=time_limit,
                  scope='Balanced exchanges of this L4 star, with all remaining rows jointly constrained by necessary linear equations. Not all star frames are covered.')
    while queue and len(attempts) < max_states and time.monotonic()-started < time_limit:
        rows, path = queue.popleft()
        extension = solve_relaxation(labels, rows, min(seconds, max(0.01,time_limit-(time.monotonic()-started))))
        item = dict(state=len(attempts), path_length=len(path), status=extension['status'],
                    method=extension['method'], seconds=extension['seconds'], path=path)
        attempts.append(item)
        print(json.dumps({k:v for k,v in item.items() if k!='path'}), flush=True)
        if 'binary_relaxation' in extension:
            verify_partial(labels, rows)
            result.update(status='JOINT_LINEAR_RELAXATION_CONSTRUCTED', path=path,
                          star_frame=dict(labels=labels,row_labels=[labels[z] for z in star],rows=[rows[z] for z in star]),
                          binary_relaxation=extension['binary_relaxation'])
            break
        for i,j,chosen in sorted(balanced_trades(labels, rows), key=lambda t:len(t[2])):
            child = {z:row.copy() for z,row in rows.items()}
            for _,a,b,_ in chosen:
                for q in (a,b):
                    child[i][q], child[j][q] = child[j][q], child[i][q]
            signature = key(child)
            if signature in seen:
                continue
            seen.add(signature)
            description = dict(rows=[labels[i],labels[j]],
                               changed_columns=[labels[q] for _,a,b,_ in chosen for q in (a,b)],
                               changed_edges=4*len(chosen))
            queue.append((child, path+[description]))
    if 'status' not in result:
        result['status'] = 'COMPONENT_LINEARLY_EXCLUDED' if not queue and all(a['status']=='INFEASIBLE' for a in attempts) else 'BALANCED_SEARCH_INCOMPLETE'
    result.update(attempts=attempts, queued_unvisited=len(queue), seconds=time.monotonic()-started)
    Path(output).write_text(json.dumps(result,indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('attempts','star_frame','binary_relaxation')}, ensure_ascii=False), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--seconds', type=float, default=1)
    parser.add_argument('--max-states', type=int, default=40)
    parser.add_argument('--time-limit', type=float, default=45)
    args = parser.parse_args()
    search(args.source,args.output,args.seconds,args.max_states,args.time_limit)
