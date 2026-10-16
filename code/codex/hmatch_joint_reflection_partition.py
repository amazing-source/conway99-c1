"""Construct H-MATCH counterexamples by simultaneous root-balanced switches.

Partition the 44 labels into disjoint even root cycles and singletons.
On a cycle q with m positive and m negative entries use I-qq^t/m.
Their block direct sum R is orthogonal and fixes B. Thus R Gamma R
inherits T/U PSD and ranks while allowing both kernels to change.
Binary adjacency, C1-prime and C2 can be enforced on pairs of cells,
including the square Gamma^2, without recomputing spectral certificates.
The CP-SAT model chooses a compatible exact cover with broken H-MATCH.
"""
import argparse
from collections import Counter
from itertools import combinations
import json
from math import lcm
from pathlib import Path
import sys
import time

import numpy as np
from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hmatch_cycle_reflections import B, CENTRAL_ROOT_INTERSECTION, H, LABELS, ROOT_INTERSECTION, ROOT_LIMIT, load_graph, new_candidate_checks, root_vectors


def make_cells(gamma, lengths):
    counts = gamma @ B.T
    capacity = 2-gamma-ROOT_INTERSECTION-gamma@gamma
    cells, rejected = [], Counter()
    proposals = [(np.array([i]), np.eye(1,dtype=np.int64), 1, None) for i in range(44)]
    for length in lengths:
        roots, _, vectors = root_vectors(length)
        for column, cycle in enumerate(roots):
            support = np.flatnonzero(vectors[:, column])
            q = vectors[support, column]
            half = length//2
            reflection = half*np.eye(length,dtype=np.int64)-np.outer(q,q)
            proposals.append((support, reflection, half, cycle))
    for support, reflection, denominator, cycle in proposals:
        projected_counts = reflection @ counts[support]
        if np.any(projected_counts % denominator) or np.any(projected_counts > denominator*ROOT_LIMIT[support]):
            rejected['ROOT_COUNTS'] += 1
            continue
        block = reflection @ gamma[np.ix_(support,support)] @ reflection
        scale = denominator**2
        if np.any(np.diag(block)) or np.any((block != 0) & (block != scale)):
            rejected['DIAGONAL_OR_BINARY'] += 1
            continue
        residual = reflection @ capacity[np.ix_(support,support)] @ reflection
        np.fill_diagonal(residual, 0)
        if np.any(residual < 0):
            rejected['WITHIN_CELL_C2'] += 1
            continue
        assert np.array_equal(B[:,support]@reflection, denominator*B[:,support])
        assert np.array_equal(reflection@reflection, scale*np.eye(len(support),dtype=np.int64))
        cells.append(dict(support=support, transform=reflection, denominator=denominator,
                          cycle=cycle, mask=sum(1 << int(i) for i in support), block=block//scale))
    return cells, capacity, dict(rejected)


def run(source, output, lengths, seconds, name=None):
    started = time.monotonic()
    records = json.loads(Path(source).read_text(encoding='utf-8'))
    if 'labels' in records:
        record_name, record = Path(source).stem, records
    else:
        if name is None:
            raise ValueError('--name is needed for a multi-record source.')
        record_name, record = name, records[name]
    gamma = load_graph(record)
    cells, capacity, rejected = make_cells(gamma, lengths)
    print(json.dumps(dict(stage='CELLS', count=len(cells), sizes=dict(Counter(len(c['support']) for c in cells)), rejected=rejected)), flush=True)
    model = cp_model.CpModel()
    chosen = [model.NewBoolVar('cell_%d' % i) for i in range(len(cells))]
    for vertex in range(44):
        model.AddExactlyOne([chosen[i] for i,c in enumerate(cells) if (c['mask'] >> vertex) & 1])
    star_edges = { (i,j):model.NewBoolVar('edge_%d_%d' % (i,j))
                  for i,j in combinations(range(44),2) if CENTRAL_ROOT_INTERSECTION[i,j] }

    def set_edges(left, right, block, indicators, same=False):
        for a,i in enumerate(left):
            for b,j in enumerate(right):
                i,j = int(i),int(j)
                if i == j or (same and i > j):
                    continue
                key = tuple(sorted((i,j)))
                if key in star_edges:
                    model.Add(star_edges[key] == int(block[a,b])).OnlyEnforceIf(indicators)

    for i, cell in enumerate(cells):
        set_edges(cell['support'], cell['support'], cell['block'], chosen[i], same=True)
    pair_counts = Counter()
    for i,j in combinations(range(len(cells)),2):
        left,right = cells[i],cells[j]
        if left['mask'] & right['mask']:
            continue
        support_l,support_r = left['support'],right['support']
        scale = left['denominator']*right['denominator']
        block = left['transform'] @ gamma[np.ix_(support_l,support_r)] @ right['transform']
        if np.any((block != 0) & (block != scale)):
            model.AddAtMostOne(chosen[i],chosen[j])
            pair_counts['BINARY_INCOMPATIBLE'] += 1
            continue
        residual = left['transform'] @ capacity[np.ix_(support_l,support_r)] @ right['transform']
        if np.any(residual < 0):
            model.AddAtMostOne(chosen[i],chosen[j])
            pair_counts['C2_INCOMPATIBLE'] += 1
            continue
        pair_counts['COMPATIBLE'] += 1
        set_edges(support_l,support_r,block//scale,[chosen[i],chosen[j]])
    differences=[]
    for edge,x in star_edges.items():
        mate_edge=tuple(sorted(H[i] for i in edge))
        if edge < mate_edge:
            difference=model.NewBoolVar('h_difference_%d_%d' % edge)
            model.AddBoolXOr([x,star_edges[mate_edge],difference.Not()])
            differences.append(difference)
    model.AddBoolOr(differences)
    solver=cp_model.CpSolver()
    solver.parameters.max_time_in_seconds=seconds
    solver.parameters.num_search_workers=1
    solver.parameters.random_seed=0
    print(json.dumps(dict(stage='SOLVE', pairs=dict(pair_counts),model_stats=model.ModelStats())),flush=True)
    status=solver.Solve(model)
    status_name=solver.StatusName(status)
    result=dict(status=status_name,source_file=str(source),source=record_name,
                root_cycle_lengths=lengths,cells=len(cells),cell_rejections=rejected,
                pair_counts=dict(pair_counts),solver_wall_seconds=solver.WallTime(),
                branches=solver.NumBranches(),conflicts=solver.NumConflicts(),
                seconds=time.monotonic()-started,
                scope='Simultaneous disjoint root-cycle reflections and singletons. All cells are chosen jointly; kernels may change. An UNSAT result covers this construction family only, not H-MATCH.')
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        selected=[cell for i,cell in enumerate(cells) if solver.Value(chosen[i])]
        denominator=lcm(*(c['denominator'] for c in selected))
        transform=np.zeros((44,44),dtype=np.int64)
        for cell in selected:
            support=cell['support']
            transform[np.ix_(support,support)]=(denominator//cell['denominator'])*cell['transform']
        assert np.array_equal(transform@transform,denominator**2*np.eye(44,dtype=np.int64))
        assert np.array_equal(B@transform,denominator*B)
        numerator=transform@gamma@transform
        assert not np.any(numerator % (denominator**2))
        candidate=numerator//(denominator**2)
        assert new_candidate_checks(candidate)=='H_MATCH_BROKEN'
        mate_gram=B.T@B[[r ^ 1 for r in range(14)]]
        t8=24*np.eye(44,dtype=np.int64)-8*gamma-3*ROOT_INTERSECTION-mate_gram+2
        u15=60*np.eye(44,dtype=np.int64)+15*gamma-4*ROOT_INTERSECTION+mate_gram-2
        new_t8=t8-8*(candidate-gamma)
        new_u15=u15+15*(candidate-gamma)
        assert np.array_equal(transform@t8@transform,denominator**2*new_t8)
        assert np.array_equal(transform@u15@transform,denominator**2*new_u15)
        hit_file=Path(output).with_name(Path(output).stem+'_HIT.json')
        hit=dict(source=record_name,source_file=str(source),labels=LABELS,
                 edges=[[i,j] for i,j in combinations(range(44),2) if candidate[i,j]],
                 transformation_numerator=transform.tolist(),transformation_denominator=denominator,
                 exact_T_U_orthogonal_congruence=True,combinatorial_verdict='H_MATCH_BROKEN',
                 chosen_root_cycles=[c['cycle'] for c in selected if c['cycle'] is not None])
        hit_file.write_text(json.dumps(hit,indent=2)+'\n',encoding='utf-8')
        result['hit_file']=str(hit_file)
        result['chosen_root_cycles']=hit['chosen_root_cycles']
    Path(output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--name')
    parser.add_argument('--lengths',default='4')
    parser.add_argument('--seconds',type=float,default=30)
    args=parser.parse_args()
    run(args.source,args.output,list(map(int,args.lengths.split(','))),args.seconds,args.name)
