"""Small satisfiable algebraic fixtures for the residual-product domain bug.

These exercise the real Gram/eigen builders. They are not Conway witnesses:
negative scalar products, positive products equal to nine, and the -4
eigenvector of K4,4 must survive the encoding independently of SRG existence.
"""
from itertools import combinations
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortools.sat.python import cp_model
from root_component_resources import limit_research_process
from root_component_rotated_gram import add_gram_cuts, add_eigen_cuts, add_gram_kernel_cuts


def contexts(vectors):
    lines = [(2*i, 2*i+1) for i in range(6)]
    original = [{'line': lines[i], 'edge_count': 0,
                 'integer_residual_coordinates': vectors.get((0,i+1), [0]*98)}
                for i in range(6)]
    return [{'root': 0, 'all_lines': lines, 'old_root_rectangles': original,
             'base_vertices': [*lines[i], *lines[j]],
             'integer_residual_coordinates': vectors.get((i+1,j+1), [0]*98)}
            for i,j in combinations(range(6),2)]


def solve(model):
    assert not model.validate()
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = 10
    status = solver.solve(model)
    assert status in (cp_model.OPTIMAL, cp_model.FEASIBLE), solver.status_name(status)
    return solver.status_name(status)


def run():
    limit_research_process(1)
    results = {}
    probe = cp_model.CpModel(); x = probe.new_int_var(-2,3,'probe')
    raw = probe.proto.variables[x.index].domain
    results['upstream_wrapper'] = {'list': list(raw), 'negative_last': raw[-1],
                                   'positive_last': raw[len(raw)-1]}
    for name, second, vx, vy, constants in (
            ('negative_dot_product', (1,3), 3, -2, False),
            ('positive_product_nine', (3,4), 3, 3, True)):
        model = cp_model.CpModel()
        x = model.new_int_var(-2,3,'x'); y = model.new_int_var(-2,3,'y')
        left = [x]*7 + ([3]*7 if constants else [0]*7) + [0]*84
        right = [y]*7 + ([-2]*7 if constants else [0]*7) + [0]*84
        info = add_gram_cuts(model, contexts({(1,2):left, second:right}), 'all')
        products = [v for v in model.proto.variables if v.name.startswith('rotated_residual_dot_product_')]
        assert products and all(list(v.domain) == [-6,9] for v in products)
        model.add(x == vx); model.add(y == vy)
        results[name] = {'status': solve(model), 'product_domain': [-6,9],
                         'product_count': info['integer_products']}
    model = cp_model.CpModel()
    positive = model.new_int_var(-2,3,'positive')
    negative = model.new_int_var(-2,3,'negative')
    edge = model.new_bool_var('edge')
    gamma = [positive]*4 + [negative]*4 + [0]*76
    graph = [[edge if (u<4 and 4<=v<8) or (v<4 and 4<=u<8) else 0
              for v in range(84)] for u in range(84)]
    info = add_eigen_cuts(model, graph, contexts({(0,1):[0]*14+gamma}), 1)
    products = [v for v in model.proto.variables if v.name.startswith('rotated_residual_eigen_product_')]
    assert products and all(list(v.domain) == [-2,3] for v in products)
    model.add(edge == 1); model.add(positive == 1); model.add(negative == -1)
    results['bipartite_minus_four_eigenvector'] = {'status': solve(model),
        'product_domain': [-2,3], 'product_count': info['edge_integer_products']}
    # Rank-one Gram R=4uu^t, u alternating on a four-cycle of K7.
    # Its eigenvalue is16, its incidence kernel is exact, and 7R is the
    # Gram of the explicit residual vectors below (norm28 at nonzero rows).
    model = cp_model.CpModel()
    cycle = {(0,1):1,(1,2):-1,(2,3):1,(0,3):-1}
    rects = contexts({p:[2*sign]*7+[0]*91 for p,sign in cycle.items()})
    lines = rects[0]['all_lines']
    for item in rects:
        a,b = sorted((lines.index(tuple(item['base_vertices'][:2])),
                      lines.index(tuple(item['base_vertices'][2:]))))
        e = 2 if (a+1,b+1) in cycle else 4
        item['edges'] = [1]*e+[0]*(6-e)
    for i,item in enumerate(rects[0]['old_root_rectangles']):
        item['edge_count'] = 2 if (0,i+1) in cycle else 4
    add_gram_cuts(model,rects,'all')
    info = add_gram_kernel_cuts(model,rects)
    results['four_cycle_gram_kernel_and_energy'] = {'status':solve(model),'cuts':info['roots']}
    return results


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
