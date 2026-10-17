"""Bounded search for a jointly glued coarse-floor root relaxation.

The84-label adjacency satisfies the linear star-incidence equations.
It need NOT satisfy the far-far SRG equations or full four-star PSD/rank.
This searches a precise necessary relaxation, never certifies Conway.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import sys
import time

import numpy as np
from ortools.sat.python import cp_model
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from conway_coarse_integer_floor import exact_ldl_pivots, floor_identity


def investigate(seconds, cyclic_lines=False):
    started = time.monotonic()
    labels = [p for p in combinations(range(14), 2) if p[1] != (p[0] ^ 1)]
    incidence = [[int(x in p) for x in range(14)] for p in labels]
    stars = [[i for i, p in enumerate(labels) if x in p] for x in range(14)]
    model = cp_model.CpModel()
    variables = {}
    orbit_variables = {}
    label_indices = {p:i for i,p in enumerate(labels)}
    def orbit_key(i, j):
        if not cyclic_lines:
            return (i, j)
        keys = []
        for shift in range(7):
            images = []
            for p in (labels[i], labels[j]):
                image = tuple(sorted(2*((x//2+shift)%7)+(x%2) for x in p))
                images.append(label_indices[image])
            keys.append(tuple(sorted(images)))
        return min(keys)
    for i, j in combinations(range(84), 2):
        p, q = labels[i], labels[j]
        overlap = len(set(p) & set(q))
        mates = sum((x ^ 1) in q for x in p)
        # Exactly t_v=d_v=0 in this linear root relaxation.
        if (overlap, mates) in ((1, 1), (0, 2)):
            variables[i, j] = 0
        else:
            key = orbit_key(i, j)
            if key not in orbit_variables:
                orbit_variables[key] = model.NewBoolVar(f'g_{key[0]}_{key[1]}')
            variables[i, j] = orbit_variables[key]
    def edge(i, j):
        return 0 if i == j else variables[min(i, j), max(i, j)]
    for i, p in enumerate(labels):
        for x in range(14):
            model.Add(sum(edge(i, j) for j in stars[x]) == 2 - int(x in p) - int((x ^ 1) in p))
    configurations = []
    for a, b in combinations(range(7), 2):
        centre = {2*a, 2*a+1, 2*b, 2*b+1}
        outside = [x for x in range(14) if x not in centre]
        buckets = [[i for i, p in enumerate(labels) if x in p and len(set(p) & centre) == 1] for x in outside]
        counts = {}
        for i in range(10):
            for j in range(i, 10):
                domain = [0, 2] if i == j else [0, 1] if outside[j] == (outside[i] ^ 1) else [2, 3]
                value = model.NewIntVarFromDomain(cp_model.Domain.FromValues(domain), f'E_{a}_{b}_{i}_{j}')
                model.Add(value == sum(edge(p, q) for p in buckets[i] for q in buckets[j]))
                counts[i, j] = value
        for i in range(10):
            # Additional relaxation restriction to get an immediate exact U certificate.
            model.Add(sum(counts[min(i,j), max(i,j)] for j in range(10)) >= 18)
        configurations.append((a, b, outside, counts))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 768
    status = solver.Solve(model)
    answer = dict(status=solver.StatusName(status), seconds=time.monotonic()-started,
        labels=labels, symmetry=('Cyclic rotation of seven root lines imposed ONLY to seek a witness of the relaxation.' if cyclic_lines else 'No nontrivial automorphism is imposed.'),
        adjacency_variables=len(orbit_variables),
        imposed_constraints='Binary symmetric Gamma, Gamma B=2J-B(I+mate), t_v=d_v=0; all21 coarse matrices have Delta=0 and row sums>=18.',
        omitted_constraints='Far-far common-neighbor equations, full four-star T/U PSD and rank bounds, and consistency between different roots.',
        conflicts=solver.NumConflicts(), branches=solver.NumBranches())
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        answer['conclusion'] = ('The stated stricter relaxation is infeasible.' if status == cp_model.INFEASIBLE
                                else 'Time limit without a witness; no infeasibility conclusion.')
        return answer
    gamma = [[int(solver.Value(edge(i, j))) for j in range(84)] for i in range(84)]
    G = np.array(gamma, dtype=np.int64)
    B = np.array(incidence, dtype=np.int64)
    mate14 = np.array([[int(j == (i ^ 1)) for j in range(14)] for i in range(14)])
    assert np.array_equal(G @ B, 2*np.ones((84,14), dtype=np.int64)-B@(np.eye(14,dtype=np.int64)+mate14))
    assert all(sum(row) == 12 for row in gamma)
    matrices = []
    for a, b, outside, counts in configurations:
        E = [[int(solver.Value(counts[min(i,j), max(i,j)])) for j in range(10)] for i in range(10)]
        invariants = floor_identity(E)
        assert invariants['defect'] == 0
        M_t = sp.Matrix(10,10,lambda i,j:int(outside[j] == (outside[i] ^ 1)))
        M = 6*sp.eye(10)+2*(sp.ones(10)-M_t)-sp.Matrix(E)
        V = (176*sp.eye(10)+16*M_t-44*sp.ones(10))/15+sp.Matrix(E)
        # The lower form is a graph Laplacian plus a nonnegative diagonal.
        assert all(M[i,j] <= 0 for i,j in combinations(range(10),2))
        assert all(sum(M[i,j] for j in range(10)) >= 0 for i in range(10))
        upper_margins = [V[i,i]-sum(abs(V[i,j]) for j in range(10) if j != i) for i in range(10)]
        assert min(upper_margins) > 0
        matrices.append(dict(root_lines=[a,b], E=E, invariants=invariants,
            M_certificate='Symmetric, nonpositive off-diagonal entries, nonnegative row sums.',
            V_positive_diagonal_dominance_margins=list(map(str,upper_margins))))
    assert sum(record['invariants']['squared_norm'] for record in matrices) == 10584
    # Diagnose our own construction; this is not an audit of a peer graph.
    residual = G@G+G-12*np.eye(84,dtype=np.int64)-2*np.ones((84,84),dtype=np.int64)+B@B.T
    violations = int(np.count_nonzero(np.triu(residual,1)))
    answer.update(status='EXACT_GLUED_LINEAR_ROOT_RELAXATION_WITNESS', gamma=gamma,
        matrices=matrices, root_squared_norm=10584, far_far_equation_violations=violations,
        maximum_absolute_far_far_residual=int(abs(residual).max()),
        conclusion='One binary far adjacency realizes the sharp coarse floor with all21 coarse M PSD and V PD. This linear root relaxation is not a Conway graph; omitted far-far equations remain essential.')
    return answer


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--seconds', type=float, default=15)
    p.add_argument('--cyclic-lines', action='store_true')
    p.add_argument('--output', required=True)
    a = p.parse_args()
    result = investigate(a.seconds, a.cyclic_lines)
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('labels','gamma','matrices')}))
