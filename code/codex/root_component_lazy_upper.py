"""Learn small exact C2 upper-bound clauses from complete C1 candidates.

C1 fixes degree 12. For each row, the sum over v!=u of
Gamma_uv+(Gamma^2)_uv equals 144, as does sum(2-|label_u intersect label_v|).
Consequently ALL C2 upper bounds imply ALL C2 equalities. It suffices to
forbid observed excesses, with clauses on at most six actual graph edges.

This avoids introducing all common-neighbour product variables at once.
Each run concerns one identified Gram in a complete source cover.
"""

import argparse
from collections import Counter
from itertools import combinations, islice
import json
from pathlib import Path
import sys
import threading
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import limit_research_process, atomic_json_write
from root_component_signature_joint import build
from root_component_signature_moments import gram_matrix
from root_component_propagation import LABELS, PAIRS
from root_component_obstruction_layers import pair_layer
from ortools.sat.python import cp_model


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--index', type=int, required=True)
    parser.add_argument('--gram-index', type=int, required=True)
    parser.add_argument('--seconds', type=float, default=120, help='Total actual process CPU budget.')
    parser.add_argument('--round-seconds', type=float, default=20)
    parser.add_argument('--clauses-per-pair', type=int, default=4)
    parser.add_argument('--local-tables', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    resources = limit_research_process(4)
    covers = {r['template_index']:r for r in json.loads((args.directory/'root_component_gram_orbits20.json').read_text())['records']}
    cover = covers[args.index]
    assert cover['exhaustive'] and cover['usable_as_gram_cover']
    values = cover['gram_anchor_values'][args.gram_index]
    template = json.loads((args.directory/'root_component_templates.json').read_text())['survivors'][args.index]
    tables = json.loads(args.local_tables.read_text())
    model, graph, info = build(template, gram_matrix(cover,values), four_corners=True,
                               local_tables=tables, short_vectors=True, normalize_component=True)
    pair_index = {p:i for i,p in enumerate(PAIRS)}
    def pi(u,v): return pair_index[tuple(sorted((u,v)))]
    clauses, seen, rounds = [], set(), []
    saved = args.output.with_suffix('.clauses.json')
    def add_clause(clause):
        model.add_bool_or([graph[PAIRS[e][0]][PAIRS[e][1]].Not() for e in clause])
    if saved.exists():
        old = json.loads(saved.read_text())
        assert old['template'] == args.index and old['gram'] == args.gram_index and old['values'] == values
        for clause in old['clauses']:
            add_clause(clause); clauses.append(clause); seen.add(tuple(clause))
    started = time.process_time()
    case = dict(info, gram_index=args.gram_index, gram_anchor_values=values, status='RUNNING',
                rounds=rounds, learned_clauses=len(clauses), full_C2=False)
    record = {'template_index':args.index, 'complete_source_gram_count':cover['gram_count'], 'cases':[case]}
    def checkpoint():
        case['elapsed_cpu_seconds'] = time.process_time()-started
        atomic_json_write(args.output,{'scope':__doc__, 'resources':resources,'records':[record]})
        atomic_json_write(saved,{'template':args.index,'gram':args.gram_index,'values':values,'clauses':clauses})
    checkpoint()
    while time.process_time()-started < args.seconds:
        remaining = args.seconds-(time.process_time()-started)
        budget = min(args.round_seconds,remaining)
        assert not model.validate(), model.validate()
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        solver.parameters.max_time_in_seconds = max(600,100*budget)
        solver.parameters.cp_model_probing_level = 0
        solver.parameters.symmetry_level = 0
        solver.parameters.linearization_level = 0
        search_start = time.process_time()
        done = threading.Event()
        def interrupt():
            while not done.wait(.05):
                if time.process_time()-search_start >= budget:
                    solver.stop_search(); return
        timer = threading.Thread(target=interrupt, daemon=True); timer.start()
        try: status = solver.solve(model)
        finally: done.set(); timer.join()
        result = {'round':len(rounds),'solver_status':solver.status_name(status),
                  'cpu_seconds':time.process_time()-search_start,'branches':solver.num_branches,
                  'conflicts':solver.num_conflicts}
        if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            gamma = [[solver.value(e) for e in row] for row in graph]
            bits = [sum(e<<j for j,e in enumerate(row)) for row in gamma]
            assert all(sum(row)==12 for row in gamma)
            violations, excesses = Counter(), Counter()
            before = len(clauses)
            for u,v in PAIRS:
                common = [w for w in range(84) if (bits[u] & bits[v]) >> w & 1]
                target = 2-len(set(LABELS[u]) & set(LABELS[v]))
                actual = gamma[u][v]+len(common)
                if actual != target: violations[pair_layer(u,v)] += 1
                if actual <= target: continue
                excesses[pair_layer(u,v)] += 1
                contributions = ([[pi(u,v)]] if gamma[u][v] else []) + [[pi(u,w),pi(v,w)] for w in common]
                added = 0
                for subset in combinations(contributions,target+1):
                    clause = tuple(sorted({e for term in subset for e in term
                                           if not isinstance(graph[PAIRS[e][0]][PAIRS[e][1]],int)}))
                    if clause in seen: continue
                    assert all(gamma[PAIRS[e][0]][PAIRS[e][1]] for e in clause)
                    seen.add(clause); clauses.append(list(clause)); add_clause(clause)
                    added += 1
                    if added >= args.clauses_per_pair: break
            result.update(violated_C2_by_layer=dict(violations),excesses_by_layer=dict(excesses),
                          new_clauses=len(clauses)-before)
            if not violations:
                case.update(status='OPTIMAL',full_C2=True,candidate_edges=[list(PAIRS[i]) for i in range(len(PAIRS)) if gamma[PAIRS[i][0]][PAIRS[i][1]]])
            else:
                assert len(clauses)>before, 'Fixed degrees imply an excess whenever C2 fails.'
                case['status']='RUNNING'
        else:
            case['status']=solver.status_name(status)
        rounds.append(result)
        case['learned_clauses']=len(clauses)
        checkpoint()
        print(json.dumps(dict(result,status=case['status'],learned_clauses=len(clauses))),flush=True)
        if case['status'] != 'RUNNING': break
    if case['status'] == 'RUNNING':
        case['status']='UNKNOWN'; checkpoint()


if __name__ == '__main__': main()
