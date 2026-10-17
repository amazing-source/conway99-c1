"""Local grid relations from bipartite complement components, and rank43 caps.

The general proof is in note206. Exhaustively enumerate the 17 possible
nontrivial bipartite complement types, verify exact 99-coordinate identities,
and check the three obstructions to >=16 grids at one vertex when r=43.
Certify tau<=1326 and b3>=46000 by exact rational certificates.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
from math import floor
import argparse
import gzip
import json

from higher_census_minima import ROOT, certify
from grid_kernel_rank_obstruction import rank_pivots
from grid_dense_hub_moment_bounds import refined_profiles, refined_model
from grid_neighbour_moment_bounds import census_cut, discover, exact_bound
from grid_class_bounds import systems

PAIRS = list(combinations(range(7), 2))


def grid_vector(edge):
    result = [0]*99
    result[0] = 1
    for i in edge:
        result[1+2*i] = result[2+2*i] = 1
    k = PAIRS.index(edge)
    result[15+4*k:19+4*k] = [1]*4
    return result


def ball_image(yv, ys):
    # Exact (A+4I)y on the root, its 14 neighbours, and 84 corners.
    result = [4*yv+2*sum(ys)]
    result += [5*ys[i]+yv for i in range(7) for _ in range(2)]
    result += [ys[i]+ys[j] for i, j in PAIRS for _ in range(4)]
    assert len(result) == 99
    return result


def matrices(edges):
    nonedges = set(PAIRS)-set(edges)
    Q = [[(sum(i in p for p in nonedges) if i == j else int(tuple(sorted((i, j))) in nonedges))
          for j in range(7)] for i in range(7)]
    M = [[9 if a == b else 3 if set(a) & set(b) else 1 for b in edges]+[2] for a in edges]
    M.append([2]*len(edges)+[1])
    qnull = 7-rank_pivots(Q)[0]
    rank = rank_pivots(M)[0]
    assert rank == len(edges)+1-qnull
    return Q, M, qnull, rank


def bipartite_types():
    # Connected bipartite components with min degree >=2 have 4..7 vertices.
    # Enumerate all incidence matrices; canonicalise only by bipartition
    # permutations (and swapping equal parts). This is not a graph-atlas input.
    result = []
    for n in range(4, 8):
        for a in range(2, n//2+1):
            b = n-a
            seen = set()
            row_perms, col_perms = list(permutations(range(a))), list(permutations(range(b)))
            for bits in range(1 << (a*b)):
                cells = [[(bits >> (i*b+j)) & 1 for j in range(b)] for i in range(a)]
                if min(map(sum, cells)) < 2 or any(sum(cells[i][j] for i in range(a)) < 2 for j in range(b)):
                    continue
                def key(transpose=False):
                    return min(sum((cells[j][i] if transpose else cells[i][j]) << (u*b+v)
                                   for u, i in enumerate(rp) for v, j in enumerate(cp))
                               for rp in row_perms for cp in col_perms)
                canonical = min(key(), key(True)) if a == b else key()
                if canonical in seen:
                    continue
                seen.add(canonical)
            for bits in sorted(seen):
                missing = [(i, a+j) for i in range(a) for j in range(b) if bits >> (i*b+j) & 1]
                for triangle in (False, True) if n == 4 else (False,):
                    nonedges = sorted(missing+(list(combinations(range(4, 7), 2)) if triangle else []))
                    edges = sorted(set(PAIRS)-set(nonedges))
                    z = [1]*a+[-1]*b+[0]*(7-n)
                    assert all(z[i]+z[j] == 0 for i, j in nonedges)
                    coefficients = [z[i]+z[j] for i, j in edges]
                    indicators = [grid_vector(edge) for edge in edges]
                    image = ball_image(sum(z), z)
                    assert image == [sum(c*v[t] for c, v in zip(coefficients, indicators)) for t in range(99)]
                    ds = [sum(i in edge for edge in edges) for i in range(7)]
                    assert set(ds) <= {0, 1, 2, 3, 4, 6} and sum(ds) <= 34
                    _, _, nullity, rank = matrices(edges)
                    hubs = ds.count(6)
                    result.append({'bipartition': [a, b], 'remaining_triangle': triangle,
                                   'complement_edges': nonedges, 'grid_edges': edges, 'z': z,
                                   'coefficients': coefficients, 'ball_y_root': sum(z),
                                   'profile': [len(edges), sum(d*(d-1)//2 for d in ds), sum(d >= 2 for d in ds), hubs],
                                   'local_relation_dimension': hubs+1,
                                   'signless_nullity_mod7': nullity, 'augmented_gram_rank': rank})
    assert len(result) == 17 and len({tuple(t['profile']) for t in result}) == 17
    return result


def finite_checks():
    types = bipartite_types()
    # The 4+3 identity from LAB is an integer equality, not just mod7.
    edges = list(combinations(range(4), 2))+list(combinations(range(4, 7), 2))
    vectors = [grid_vector(edge) for edge in edges]
    target = [1+sum((1 if i < 6 else -1)*v[t] for i, v in enumerate(vectors)) for t in range(99)]
    assert ball_image(-1, [1]*4+[0]*3) == target
    dense = []
    for name, nonedges in [
        ('C4+3isolates', [(0,1),(1,2),(2,3),(0,3)]),
        ('C5+2isolates', [(0,1),(1,2),(2,3),(3,4),(0,4)]),
        ('diamond+3isolates', [(0,1),(0,2),(0,3),(1,2),(1,3)])]:
        edges = sorted(set(PAIRS)-set(nonedges))
        Q, M, nullity, rank = matrices(edges)
        assert rank > 13
        dense.append({'complement': name, 'complement_edges': nonedges,
                      'grid_count': len(edges), 'signless_nullity_mod7': nullity,
                      'augmented_gram_rank': rank})
    return {'scope': __doc__, 'extra_relation_types': types, 'rank43_dense_obstructions': dense}


def moments(verify_only):
    _, all_profiles = refined_profiles()
    grouped = [p for p in all_profiles if p[0] <= 15]
    assert len(grouped) == 174
    path = ROOT/'data/codex_rank43_vertex_moments.json.gz'
    if verify_only:
        with gzip.open(path, 'rt') as stream:
            report = json.load(stream)
        assert report['profiles'] == list(map(list, grouped)) and report['rank'] == 43
    else:
        report = {'rank': 43, 'profiles': grouped, 'cases': {}}
    maxima = []
    for s in range(74):
        _, expanded, rows, caps, objective = refined_model(s, grouped)
        rows[-1] = ('rank39_hub_cut', F(0),
                    [F((u == 1)+2*(u == 2)-6*(u == 3)) for _, _, _, u, _ in expanded]+[F(0), F(0)])
        proof = report['cases'][str(s)] if verify_only else discover(rows, caps, objective)
        if proof['infeasible']:
            rows = [(name, c, a+[F(1)]) for name, c, a in rows]
            caps = caps+[10**6]
            objective = [F(0)]*(len(caps)-1)+[F(1)]
        bound = exact_bound(rows, caps, objective, proof['weights'])
        assert bound == F(proof['lower_bound'])
        if proof['infeasible']:
            assert bound > 0
        else:
            maxima.append((-bound, s))
        if not verify_only:
            report['cases'][str(s)] = proof
    maximum, s = max(maxima)
    summary = {'rational_upper_bound': str(maximum), 'integer_twin_cap': floor(maximum),
               'maximising_size': s, 'feasible_sizes': len(maxima), 'infeasible_sizes': 74-len(maxima)}
    assert maximum == F(63653, 48) and floor(maximum) == 1326
    if verify_only:
        assert report['summary'] == summary
    else:
        report['summary'] = summary
        with gzip.GzipFile(filename=path, mode='wb', mtime=0) as stream:
            stream.write(json.dumps(report).encode())
    print('Verified all74 rank43 moment cases:', summary, flush=True)


def shell(verify_only):
    source, _, rows = systems()
    width = len(source['parameters'])+1
    rows.append(('rank43_tau<=1326', [F(1326)]+[F(0)]*(width-1)+[F(-1), F(0)]))
    objective = [F(0)]*(width+1)+[F(1)]
    path = ROOT/'data/codex_rank43_vertex_b3_bound.json'
    if verify_only:
        proof = json.loads(path.read_text())
    else:
        proof = certify(rows, objective)
        proof.update(objective=list(map(str, objective)), rank=43, tau_cap=1326,
                     scope='Exact dual lower certificate; no attainment of the relaxation asserted.')
        path.write_text(json.dumps(proof, indent=2)+'\n')
    # A lower bound needs the nonnegative dual identity, not a primal
    # point attaining it. The discovery helper may return no exact point.
    lookup = dict(rows)
    total = [F(0)]*len(objective)
    for name, weight in proof['certificate']:
        weight = F(weight)
        assert weight >= 0
        total = [a+weight*b for a, b in zip(total, lookup[name])]
    assert total[1:] == objective[1:]
    assert objective[0]-total[0] == F(proof['lower_bound'])
    assert proof['objective'] == list(map(str, objective))
    assert proof['verified_identity_coefficients'] == list(map(str, total))
    assert proof['rank'] == 43 and proof['tau_cap'] == 1326 and F(proof['lower_bound']) == 46000
    print('Verified exact rank43 consequence b3>=46000.', flush=True)


def main(verify_only):
    report = finite_checks()
    path = ROOT/'data/codex_grid_vertex_relations.json'
    if verify_only:
        assert json.loads(path.read_text()) == json.loads(json.dumps(report))
    else:
        path.write_text(json.dumps(report, indent=2)+'\n')
    print('Verified17 types, integer 4+3 relation and3 rank43 dense obstructions.', flush=True)
    census_cut(verify_only=True)
    moments(verify_only)
    shell(verify_only)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-only', action='store_true')
    main(parser.parse_args().verify_only)
