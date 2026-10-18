"""Positive/negative controls of the auxiliary partition, not Conway examples."""
import argparse
from itertools import combinations
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortools.sat.python import cp_model
from root_component_minimum_partition import add_partitions_for_lines
from root_component_resources import atomic_json_write, limit_research_process


def neighbourhood(joins):
    graph = [[0]*99 for _ in range(99)]
    def edge(u, v):
        graph[u][v] = graph[v][u] = 1
    for u, v in combinations(range(3), 2):
        edge(u, v)
    for component in range(6):
        first = 3+6*component
        for colour in range(3):
            for bit in (0, 1):
                edge(colour, first+2*colour+bit)
            edge(first+2*colour, first+2*colour+1)
        for bit in (0, 1):
            for a, b in combinations(range(3), 2):
                edge(first+2*a+bit, first+2*b+bit)
    for a, b in joins:
        edge(3+6*a, 3+6*b)
    # Supply the exterior component balance, without claiming an SRG:
    # every exterior vertex sees one vertex in each six-vertex component.
    for w in range(39,99):
        for component in range(6):
            edge(w,3+6*component)
    return graph


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args(); limit_research_process(1)
    assert not args.output.exists()
    cases = []
    for count, joins in ((6, []), (3, [(0,1), (2,3), (4,5)]),
                         (1, [(0,1), (1,2), (2,3), (3,4), (4,5)])):
        for minimum in (3,4):
            for balance in ((False,True) if count == 6 else (False,)):
                model = cp_model.CpModel()
                info = add_partitions_for_lines(model, neighbourhood(joins), [(0,1,2)],
                                                balance=balance, minimum_components=minimum)
                assert not model.validate(), model.validate()
                solver = cp_model.CpSolver(); solver.parameters.num_search_workers = 1
                solver.parameters.max_time_in_seconds = 10
                status = solver.solve(model)
                assert status in (cp_model.OPTIMAL,cp_model.INFEASIBLE)
                assert (status == cp_model.OPTIMAL) == (count >= minimum)
                cases.append({'actual_components': count, 'required_components': minimum,
                              'degree_balance': balance, 'status': solver.status_name(status),
                              'auxiliary_bins': info['auxiliary_bins_per_line']})
    result = {'scope': __doc__, 'passed': True, 'cases': cases}
    atomic_json_write(args.output, result)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
