"""Exact small tables for the two odd-single-character U blocks in c55.

Applies to the non-grid-overlap canonical quotient of four_star_g1_c55.
Each U test reduces to a 5x5 Schur matrix, with 4*3**5=972 cases.
"""
import argparse
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path
import sys

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from three_star_ambient_upper import psd_or_witness


def row_support(j):
    return [0,3,4,5] if j == 1 else [i+1 for i in range(5) if i != j]


def balanced_rows(j):
    support = row_support(j)
    result = []
    for other in support[1:]:
        row = [0]*6
        for k in support:
            row[k] = 1 if k in (support[0],other) else -1
        result.append(row)
    return result


def schur(s, d, partitions):
    rows = [balanced_rows(j)[partitions[j]] for j in range(5)]
    m = 4+d
    return sp.Matrix(5, 5, lambda a,b:
        24*m*int(a==b)+6*m*s*int(a==b==0)-4*m
        -3*m*sum(rows[j][a+1]*rows[j][b+1] for j in range(5) if j != 1)
        -6*rows[1][a+1]*rows[1][b+1])


def schur_t(s, d, partitions):
    rows = [balanced_rows(j)[partitions[j]] for j in range(5)]
    m = 3-d
    return sp.Matrix(5,5,lambda a,b:
        30*m*int(a==b)-10*m*s*int(a==b==0)-5*m
        -2*m*sum(rows[j][a+1]*rows[j][b+1] for j in range(5) if j!=1)
        -10*rows[1][a+1]*rows[1][b+1])


def catalogue():
    counts, allowed, certificates, joint = Counter(), [], [], []
    for s,d in product((-1,1), repeat=2):
        for partitions in product(range(3), repeat=5):
            matrix = schur(s,d,partitions)
            result = psd_or_witness(matrix)
            counts[(s,d,result['psd'])] += 1
            if result['psd']:
                allowed.append([int(s==1),int(d==1),*partitions])
                result['rank'] = matrix.rank()
                t_result = psd_or_witness(schur_t(s,d,partitions))
                if t_result['psd']:
                    joint.append([int(s==1),int(d==1),*partitions])
                    t_result['rank'] = schur_t(s,d,partitions).rank()
                    assert result['rank'] == t_result['rank'] == 5
                    counts[s,d,'joint'] += 1
                result['T_schur'] = t_result
            certificates.append(dict(s=s,d=d,partitions=partitions,**result))
    # Verify the analytic single-character correction from label geometry.
    from four_star_g1_c55 import ORBITS, canonical_quotient
    from four_star_profile_join import LABELS, upper_entry
    from three_star_column_domains import k8
    for orbit_index,centres,expected in [(2,(0,1),(1,3)),(6,(2,3),(2,3))]:
        orbit=ORBITS[orbit_index]
        accepted=[]
        for offsets in combinations((1,2,3),2):
            graph=[[int((a^b) in offsets) for b in range(4)] for a in range(4)]
            stars=all(sum(graph[a][b] for b in range(4) if c in LABELS[orbit[b]])==1
                      for a in range(4) for c in centres)
            caps=all(sum(graph[a][k]*graph[b][k] for k in range(4))
                     +len(set(LABELS[orbit[a]])&set(LABELS[orbit[b]]))+graph[a][b]<=2
                     for a,b in combinations(range(4),2))
            if stars and caps:
                accepted.append(offsets)
        assert accepted==[expected]
    for chi,left in [('10',list(range(6))),('01',[0]+list(range(6,11)))]:
        chars = [1,1,-1,-1] if chi == '10' else [1,-1,1,-1]
        B = sp.zeros(44,11)
        for j,orbit in enumerate(ORBITS):
            for i,sign in zip(orbit,chars):
                B[i,j] = sign
        N0 = sp.Matrix(44,44,lambda i,j:upper_entry(LABELS[i],LABELS[j],0,i==j))
        M0 = sp.Matrix(44,44,lambda i,j:24*int(i==j)-k8(LABELS[i],LABELS[j]))
        e = sp.Matrix([int(i in left) for i in range(11)])
        assert B.T*N0*B/60 == 4*sp.eye(11)-sp.Rational(2,3)*e*e.T
        assert B.T*M0*B/32 == 3*sp.eye(11)-sp.Rational(1,2)*e*e.T
    assert len(joint)==126
    H,D = canonical_quotient()
    B0 = sp.zeros(44,11)
    for j,orbit in enumerate(ORBITS):
        for i in orbit:
            B0[i,j]=1
    N00 = B0.T*N0*B0/4+15*sp.Matrix(D)
    fixed_upper=psd_or_witness(N00)
    fixed_upper['rank']=N00.rank()
    assert fixed_upper['psd'] and fixed_upper['rank']==9
    return dict(status='EXACT_SINGLE_CHARACTER_T_U_TABLE',cases=972,
                allowed_states=allowed, joint_allowed_states=joint,
                fixed_trivial_sector=dict(T_rank=1,T_nullity=10,U15=[list(map(int,row)) for row in N00.tolist()],U_certificate=fixed_upper),
                state_order=['s_positive','d_positive','partition_row0','partition_row1','partition_row2','partition_row3','partition_row4'],
                counts=[dict(s=s,d=d,U_psd=counts[s,d,True],U_rejected=counts[s,d,False],T_U_psd=counts[s,d,'joint']) for s,d in product((-1,1),repeat=2)],
                certificates=certificates,
                proof=[
                    'Each singleton component is a genuine grid: the same-star matching requirement and the common-neighbour cap exclude the other two internal degree2 Cayley choices. Its character10 adjacency diagonal is0 on L and -2 on R (reversed in character01).',
                    'In character10 use left coordinates O,L0,...,L4 and right coordinates R0,...,R4. Put e=(1,...,1) on the six left coordinates and v=e_O-e_L0. The U block equals [[4I+s vv^t-(2/3)ee^t,B^t],[B,diag(2,4+d,2,2,2)]], with s,d in{-1,1}.',
                    'B has four signs per row, on row_support(j), and B e=0. Each row therefore has two plus and two minus entries. Up to independent row sign, there are three partitions; U positivity is unchanged by these right-coordinate sign changes.',
                    'The right diagonal is positive. Eliminate it by Schur complement and remove coordinate O from the residual matrix, whose kernel contains e. Multiplication by6(4+d) gives precisely the integer5x5 matrix returned by schur(). Thus the test is necessary and sufficient for this one U block.',
                    'For T the left block is3I-s vv^t-(1/2)ee^t and the right diagonal is(5,3-d,5,5,5). The identical elimination, scaled by10(3-d), gives schur_t(). Of the180 U-positive cases,126 also have T positive. ALL126 have both Schur matrices of rank5: each full11x11 character block has exactly the one forced star relation.',
                    'Character01 uses the same catalogue after exchanging left/right and exterior indices0/1. The two catalogues must be coupled through the same original orbit matching choices. Individual admissibility of the two U blocks does not assert full T/U positivity or any completion.'
                ],
                consequence='The trivial sector is fixed PSD for both forms, with T rank1 and U rank9. The joint tables settle both forms in characters10 and01, each of rank10. Only character11 positivity remains; T character nullities must be(10,1,1,k), and rank(T)<=30 forces k>=2. Other nontrivial rank-target patterns with extra10/01 relations are impossible here.',
                scope='Canonical G1 c55 non-grid-overlap quotient; exact positivity test for T/U10 or T/U01, not a classification of complete graphs.')


def add_upper_tables(model, choices, data):
    records = {tuple(row['orbits']):row for row in choices}
    positives = {}
    def positive(i,j,character):
        i,j = sorted((i,j))
        key = (i,j,character)
        if key not in positives:
            row = records[i,j]
            assert all(len(option)==1 for option in row['options'])
            mask = 2 if character == '10' else 1
            selected = [var for option,var in zip(row['options'],row['selected']) if not (option[0]&mask)]
            bit = model.NewBoolVar('uch_%d_%d_%s'%key)
            model.Add(bit == sum(selected))
            positives[key] = bit
        return positives[key]
    balanced_table = []
    for other in (1,2,3):
        row = [int(k in (0,other)) for k in range(4)]
        balanced_table.extend([row+[other-1],[1-x for x in row]+[other-1]])
    for chi in ('10','01'):
        swap = lambda i: 1-i if i<2 else i
        left = [0]+([1+i for i in range(5)] if chi=='10' else [6+swap(i) for i in range(5)])
        right = [6+i for i in range(5)] if chi=='10' else [1+swap(i) for i in range(5)]
        partitions=[]
        for j in range(5):
            bits=[positive(left[k],right[j],chi) for k in row_support(j)]
            partition=model.NewIntVar(0,2,'upart_%s_%d'%(chi,j))
            model.AddAllowedAssignments(bits+[partition],balanced_table)
            partitions.append(partition)
        state=[positive(0,0,chi),positive(right[1],right[1],chi)]+partitions
        model.AddAllowedAssignments(state,data.get('joint_allowed_states',data['allowed_states']))
    return dict(character_blocks=2,exact_cases_per_block=972,
                allowed_table_rows=len(data.get('joint_allowed_states',data['allowed_states'])),row_partition_variables=10,
                both_forms='joint_allowed_states' in data)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    data=catalogue()
    path=Path(args.output)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:data[k] for k in ('status','cases','counts')}))
