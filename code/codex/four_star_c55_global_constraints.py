"""Global completion constraints for the canonical G1 c55 local family.

No peer seed is read. The local G1 action is NOT assumed to extend to
an automorphism of a completed graph. The conclusions quantify its failure.
"""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys

import sympy as sp

sys.path.insert(0,str(Path(__file__).resolve().parent))
from four_star_g1_c55 import ORBITS, canonical_quotient
from four_star_g1_sectors import action
from four_star_profile_join import LABELS, upper_entry
from three_star_column_domains import k8


def partitions(total, least=2):
    if total == 0:
        yield ()
    for first in range(least,total+1):
        for rest in partitions(total-first,first):
            yield (first,)+rest


def support_rank_bound():
    """Safe component-cap enumeration for a subgraph of K10 minus five mates."""
    viable = []
    max_nullity_without_large_component = 0
    for used in range(2,11):
        for sizes in partitions(used):
            for bipartite in product((False,True),repeat=len(sizes)):
                if any(n == 2 and not bip for n,bip in zip(sizes,bipartite)):
                    continue
                # An m-set of ten letters contains at least max(0,m-5) mate pairs.
                capacities = [n*n//4 if bip else n*(n-1)//2-max(0,n-5)
                              for n,bip in zip(sizes,bipartite)]
                rank = sum(n-int(bip) for n,bip in zip(sizes,bipartite))
                cap = sum(capacities)
                if max(sizes) <= 8:
                    max_nullity_without_large_component = max(max_nullity_without_large_component,cap-rank)
                if cap-rank >= 20:
                    viable.append(dict(component_sizes=sizes,bipartite=bipartite,
                        incidence_rank=rank,edge_upper_bound=cap,edges_at_least=20+rank))
    assert viable == [dict(component_sizes=(9,),bipartite=(False,),incidence_rank=9,edge_upper_bound=32,edges_at_least=29),
                      dict(component_sizes=(10,),bipartite=(False,),incidence_rank=10,edge_upper_bound=40,edges_at_least=30)]
    assert max_nullity_without_large_component == 17
    # Sharp only for this incidence-rank relaxation, not a Conway construction.
    edges = [(i,j) for i,j in combinations(range(9),2) if j != (i ^ 1)]
    edges = edges[3:]
    incidence = sp.Matrix([[int(x in edge) for x in range(10)] for edge in edges])
    assert len(edges) == 29 and incidence.rank() == 9
    return dict(required_matrix_rank=20,nonzero_columns_at_least=29,
        viable_component_bounds=viable,max_incidence_kernel_dimension_if_components_at_most8=17,
        sharp_incidence_only_fixture=dict(edges=edges,vertices=10,nonisolated_vertices=9,
            edge_count=29,incidence_rank=9,left_kernel_dimension=20,
            scope='A support graph for the rank argument only; no SRG or extension profile realization.'))


def add_completion_cuts(model, rows_by_label):
    """Add the proved cuts to a CP-SAT completion model, under the stated family.

    rows_by_label[u] is the44-vector of binary adjacencies to LABELS, for
    each of the40 missing labels. The caller must have imposed/established
    the canonical G1 c55 non-grid quotient and both local PSD conditions.
    The cuts are NOT valid as unconditional restrictions on all Conway graphs.
    """
    missing = [p for p in combinations(range(4,14),2) if p[1] != (p[0] ^ 1)]
    if set(rows_by_label) != set(missing) or any(len(row) != 44 for row in rows_by_label.values()):
        raise ValueError('Exactly the40 canonical missing labels with44 adjacency entries are required.')
    index = {p:i for i,p in enumerate(LABELS)}
    hpairs = [(i,index[action(p,1,1)]) for i,p in enumerate(LABELS) if i < index[action(p,1,1)]]
    histograms = [[] for _ in range(3)]
    broken = {}
    for u in missing:
        row = rows_by_label[u]
        nO = model.NewIntVar(0,2,'c55_nO_%d_%d'%u)
        model.Add(nO == sum(row[i] for i in ORBITS[0]))
        if min(u) < 8:
            model.Add(nO <= 1)
        for value in range(3):
            indicator = model.NewBoolVar('c55_nOeq%d_%d_%d'%(value,*u))
            model.Add(nO == value).OnlyEnforceIf(indicator)
            model.Add(nO != value).OnlyEnforceIf(indicator.Not())
            histograms[value].append(indicator)
        differences = []
        for k,(i,j) in enumerate(hpairs):
            xor = model.NewBoolVar('c55_diff_%d_%d_%d'%(*u,k))
            model.Add(row[i] != row[j]).OnlyEnforceIf(xor)
            model.Add(row[i] == row[j]).OnlyEnforceIf(xor.Not())
            differences.append(xor)
        broken[u] = model.NewBoolVar('c55_break_%d_%d'%u)
        model.AddMaxEquality(broken[u],differences)
    for indicators,count in zip(histograms,(10,24,6)):
        model.Add(sum(indicators) == count)
    used = []
    for x in range(4,14):
        flag = model.NewBoolVar('c55_support_letter_%d'%x)
        model.AddMaxEquality(flag,[broken[u] for u in missing if x in u])
        used.append(flag)
    model.Add(sum(used) >= 9)
    model.Add(sum(broken.values()) >= 20+sum(used))
    return dict(overlap_histogram=[10,24,6],profile_xor_pairs=22,
        broken_profile_variables=40,active_letter_variables=10,
        lower_bound='broken >=20+used_letters, used_letters>=9',
        scope='Conditional on the canonical local G1 c55 non-grid family and both local PSD forms.')


def report(catalogue_path):
    raw = Path(catalogue_path).read_bytes()
    accepted_catalogue = json.loads(raw)
    # Consume the previous exact table; do not regenerate its PSD classifications.
    assert len(accepted_catalogue['joint_allowed_states']) == 126
    H,D = map(sp.Matrix,canonical_quotient())
    w = sp.Matrix([1,-1,0,0,0,0,0,-1,0,0,0])
    assert H == w*w.T and H*H == 3*H
    B = sp.zeros(44,11)
    for j,orbit in enumerate(ORBITS):
        for i in orbit:
            B[i,j] = 1
    M0 = sp.Matrix(44,44,lambda i,j:24*int(i==j)-k8(LABELS[i],LABELS[j]))
    N0 = sp.Matrix(44,44,lambda i,j:upper_entry(LABELS[i],LABELS[j],0,i==j))
    U00 = B.T*N0*B/60+D
    basis = U00.rref()[1]
    inverse = U00.extract(basis,basis).inv()
    types = []
    for label,multiplicity in [((4,6),4),((4,8),24),((8,10),12)]:
        baseT = [-sum(sp.Rational(k8(LABELS[i],label),8) for i in orbit)/2 for orbit in ORBITS]
        baseU = [sum(sp.Rational(upper_entry(LABELS[i],label,0),15) for i in orbit)/2 for orbit in ORBITS]
        rows = []
        for overlap_count in range(5):
            alpha = baseT[0]-sp.Rational(overlap_count,2)
            counts = [2*(baseT[i]-alpha*w[i]) for i in range(11)]
            if any(x < 0 or x > 4 or x.q != 1 for x in counts):
                continue
            vectorU = sp.Matrix([baseU[i]+counts[i]/2 for i in range(11)])
            restricted = vectorU.extract(basis,[0])
            assert U00[:,basis]*inverse*restricted == vectorU
            normU = (restricted.T*inverse*restricted)[0]
            rows.append(dict(overlap_neighbours=overlap_count,orbit_neighbour_counts=list(map(int,counts)),
                T00_cross_multiplier=str(alpha),T00_projection_norm=str(alpha**2),U00_projection_norm=str(normU)))
        types.append(dict(representative_label=label,number_of_missing_labels=multiplicity,profiles=rows))
    assert [[r['overlap_neighbours'] for r in t['profiles']] for t in types] == [[0,1],[0,1],[0,1,2]]
    # The sum of the two Gram blocks is fixed and is 7 times a projection.
    for chi,left in [('10',list(range(6))),('01',[0]+list(range(6,11)))]:
        signs = [1,1,-1,-1] if chi == '10' else [1,-1,1,-1]
        C = sp.zeros(44,11)
        for j,orbit in enumerate(ORBITS):
            for i,sign in zip(orbit,signs):
                C[i,j] = sign
        e = sp.Matrix([int(i in left) for i in range(11)])
        cap = C.T*(M0/8+N0/15)*C/4
        assert cap == 7*sp.eye(11)-sp.Rational(7,6)*e*e.T
    index = {p:i for i,p in enumerate(LABELS)}
    involution = [index[action(p,1,1)] for p in LABELS]
    pairs = [(i,j) for i,j in enumerate(involution) if i < j]
    assert len(pairs) == 22 and all(involution[involution[i]] == i for i in range(44))
    missing = [p for p in combinations(range(4,14),2) if p[1] != (p[0] ^ 1)]
    overlap = ORBITS[0]
    local_z = [int(w[j]) for j,orbit in enumerate(ORBITS) for _ in orbit]
    local_z_by_label = [0]*44
    for j,orbit in enumerate(ORBITS):
        for i in orbit:
            local_z_by_label[i] = int(w[j])
    assert local_z.count(1) == 4 and local_z.count(-1) == 8
    counts = sp.Matrix([[1,1,1],[0,1,2],[1,0,1]]).inv()*sp.Matrix([40,36,16])
    assert list(counts) == [10,24,6]
    return dict(status='EXACT_C55_GLOBAL_EIGENVECTOR_AND_ASYMMETRY_CONSTRAINTS',
        scope='Any Conway completion of a G1-invariant four-star c=(5,5) boundary with non-grid overlap and both Gram forms PSD. Normalize the two distinct active exterior pairs to(4,5) and(6,7). No global automorphism is assumed.',
        accepted_character_table=dict(path=str(Path(catalogue_path).resolve()),sha256=sha256(raw).hexdigest(),
            joint_states_per_character=126,used_result='Both T and U have rank10 on each eleven-dimensional character10/01 block; only the forced star relation remains.'),
        labels=LABELS,missing_labels=missing,orbits=ORBITS,overlap_indices=overlap,
        orbit_column_profiles=types,
        column_profile_derivation='For an outside label u, write b00=B00^T*T(S,u)/2. PSD forces b00 in im(H)=span(w), H=ww^T. If nO is its number of overlap neighbors, b00=(1-nO)w/2. Solving the eleven orbit sums gives the displayed integer neighbor counts.',
        forced_global_overlap_histogram=dict(no_overlap_neighbours=10,one_overlap_neighbour=24,two_overlap_neighbours=6,
            two_neighbours_allowed_only_on='The twelve missing labels using two of the three ordinary exterior pairs(8,9),(10,11),(12,13).'),
        forced_signed_eigenvector=dict(adjacency_eigenvalue=-4,squared_norm=28,positive_entries=14,negative_entries=14,zero_entries=71,
            root_and_neighbours_entries=0,entries_on_S=local_z_by_label,entry_for_missing_label='1-nO(u)',
            definition='z=T_far*1_overlap, extended by zero to the root and its fourteen neighbors.',
            proof='The four overlap vertices have far degree12 and degree3 inside S, giving sum_u nO=36. The trivial quotient gives z=+1 on the four overlap labels,-1 on eight labels of the two active orbits,0 on the other32 S labels. Outside, z_u=1-nO(u), and the profile table gives nO<=2. Since T_far^2=7*T_far and 1_O^T*T_far*1_O=4, ||z||^2=28. Since T_far kills all root-star incidence columns, z has sum0 and A99*z=-4z. The three histogram equations are N0+N1+N2=40, N1+2N2=36, N0+N2=16.'),
        local_involution=dict(root_letter_permutation='(0 1)(2 3), fixing all ten exterior root letters',
            label_index_permutation=involution,label_index_transposition_pairs=pairs,
            broken_at_u='Some pair(s,h(s)) in S has unequal adjacency to u. Every missing label is itself fixed by this root-letter permutation.'),
        symmetry_breaking_bound=support_rank_bound(),
        symmetry_breaking_proof=[
            'Project T(S,missing) to the h-odd character10 and01 spaces, obtaining P. From T_far^2=7T_far, PP^T=7T_odd-T_odd^2=T_odd*U_odd, because the fixed cap is7 times the projection onto the two forced-star perpendicular spaces.',
            'The accepted126-state tables make both factors positive definite on those two ten-dimensional spaces. Therefore rank(P)=20.',
            'For each exterior root letter x, its S-star incidence vector is h-even. The global identity T_far*B=0 therefore gives P*B_missing=0. B_missing is the unoriented edge-vertex incidence matrix of K10 minus its five mate edges.',
            'A column of P is zero exactly when the adjacency profile of that missing vertex is h-invariant: the fixed geometric correction is h-even. Let H be the graph on the ten exterior letters whose edges are the nonzero columns. Then20<=|E(H)|-rank(B_H).',
            'A connected component on m vertices has incidence rank m-1 if bipartite and m otherwise. Enumerating component sizes up to10 with the elementary edge bounds leaves only one nonbipartite component on9 or10 vertices. The former needs at least29 edges, the latter at least30. Thus at least29 of40 exterior vertices must break h.'
        ],
        solver_constraints=dict(overlap_degree_domain='nO(u) in{0,1}; allow2 only if both root-letter pairs of u are ordinary.',
            overlap_histogram={'0':10,'1':24,'2':6},
            broken_profile_definition='break[u] = OR over the22 pairs(i,h(i)) of (Gamma[u,i] XOR Gamma[u,h(i)]).',
            broken_profiles_at_least=29,invariant_profiles_at_most=11,
            cp_sat_adapter='add_completion_cuts(model, rows_by_label), in this source file; requires the stated family as an established model condition.',
            additional_support_structure='The broken labels, viewed as edges on the ten exterior letters, form one connected nonbipartite component on9 or10 nonisolated letters. With10 letters there are at least30 broken profiles.'),
        limitations='These are conditional necessary completion constraints for the stated local family. They neither exclude that family nor show that every Conway enters it. They do not force a global automorphism, and no solver speedup is measured.',
        validation='Exact fixed-quotient projection tables, fixed character cap, histogram equations, and a finite component-size rank argument with an own29-edge support fixture. No peer seed read or re-certified.')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--catalogue',required=True)
    p.add_argument('--output',required=True)
    a = p.parse_args()
    result = report(a.catalogue)
    out = Path(a.output)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:result[key] for key in ('status','scope','forced_global_overlap_histogram','solver_constraints','limitations','validation')}))
