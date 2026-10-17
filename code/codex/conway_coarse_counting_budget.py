"""A symmetry-free counting budget from both four-star Gram forms.

For each root v and unordered pair of its seven triangle lines, let E be
the10x10 adjacency-count matrix between the four-label exterior buckets.
The local separable integer inequality and its global sum hold in every
Conway SRG(99,14,1,2). No local automorphism group is assumed.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import sys

import sympy as sp

sys.path.insert(0,str(Path(__file__).resolve().parent))
from four_star_profile_join import LABELS, upper_entry
from three_star_column_domains import k8

OUTSIDE=tuple(range(4,14))
BUCKETS=[[i for i,p in enumerate(LABELS) if x in p] for x in OUTSIDE]


def count_matrix(gamma):
    return [[sum(gamma[i][j] for i in a for j in b) for b in BUCKETS] for a in BUCKETS]


def budget(E):
    square=sum(x*x for row in E for x in row)
    diagonal=sum(E[i][i] for i in range(10))
    mates=sum(E[i][i+1] for i in range(0,10,2))
    total=sum(map(sum,E))
    score=15*square+86*diagonal+92*mates-74*total
    return dict(score=score,upper_bound=3520,passes=score<=3520,
                squared_norm=square,trace=diagonal,mate_entry_sum=mates,entry_sum=total)


def integer_terms():
    result=[]
    for i in range(10):
        for j in range(i,10):
            if i==j:
                quadratic,linear,domain=15,12,[0,2,4]
            elif j==(i^1):
                quadratic,linear,domain=30,-56,list(range(5))
            else:
                quadratic,linear,domain=30,-148,list(range(9))
            result.append(dict(entry=[OUTSIDE[i],OUTSIDE[j]],indices=[i,j],
                               quadratic=quadratic,linear=linear,
                               exact_value_table=[[x,quadratic*x*x+linear*x] for x in domain]))
    return result


def edge_count_weights():
    labels=list(p for p in combinations(range(14),2) if p[1]!=(p[0]^1))
    centre_sets=[set((2*a,2*a+1,2*b,2*b+1)) for a,b in combinations(range(7),2)]
    coefficients={}
    for p,q in combinations(labels,2):
        overlap=len(set(p)&set(q))
        mate_incidence=sum((x^1) in q for x in p)
        values=[0,0,0,0]  # traceE, mate sum, overlap edges, totalE
        for C in centre_sets:
            pc=[x for x in p if x in C]; qc=[x for x in q if x in C]
            if len(pc)==len(qc)==2:
                values[2]+=1
            if len(pc)==len(qc)==1:
                x=next(x for x in p if x not in C)
                y=next(x for x in q if x not in C)
                values[3]+=2
                if x==y: values[0]+=2
                if y==(x^1): values[1]+=1
        key=(overlap,mate_incidence)
        coefficients.setdefault(key,set()).add(tuple(values))
    expected={(1,0):(2,0,0,10),(1,1):(10,5,1,20),(0,0):(0,0,0,8),
              (0,1):(0,1,0,10),(0,2):(0,10,1,20)}
    assert coefficients=={k:{v} for k,v in expected.items()}
    return expected


def report():
    incidence=sp.Matrix([[int(i in bucket) for i in range(44)] for bucket in BUCKETS])
    mate=sp.Matrix(10,10,lambda i,j:int(j==(i^1)))
    C=6*sp.eye(10)+2*(sp.ones(10)-mate)
    cap=sp.Rational(14,15)*(19*sp.eye(10)-mate-sp.ones(10))
    # Own algebraic fixture only; deliberately not claimed to be a graph seed.
    gamma=[[0]*44 for _ in range(44)]
    for i,j in combinations(range(44),2):
        gamma[i][j]=gamma[j][i]=int((i*j+7*i+3*j)%13==0)
    E=sp.Matrix(count_matrix(gamma))
    M8=sp.Matrix(44,44,lambda i,j:24*int(i==j)-8*gamma[i][j]-k8(LABELS[i],LABELS[j]))
    N15=sp.Matrix(44,44,lambda i,j:upper_entry(LABELS[i],LABELS[j],gamma[i][j],i==j))
    M=incidence*M8*incidence.T/8
    V=incidence*N15*incidence.T/15
    assert M==C-E and M+V==cap
    score=budget([list(map(int,row)) for row in E.tolist()])['score']
    assert 15*sp.trace(M*V)==3520-score
    weights=edge_count_weights()
    t,d,z=sp.symbols('t d z')
    type_counts={(1,0):84-t,(1,1):t,(0,0):336+t+d,
                 (0,1):84-t-2*d,(0,2):d}
    sums=[sp.expand(sum(type_counts[k]*v[j] for k,v in weights.items())) for j in range(4)]
    assert sums==[168+8*t,84+4*t+8*d,t+d,4368+8*t+8*d]
    root_score=sp.expand(15*z+86*sums[0]+92*sums[1]-74*sums[3])
    assert root_score==15*z+464*t+144*d-301056
    assert 21*3520+301056==374976
    assert 99*374976//3==12374208
    # Uniform average over the21 line pairs, then relabel the5 exterior
    # mate pairs and their orientations. This loses all non-invariant data.
    s=84-t-d
    mean_m=[sp.Rational(4,105)*s,sp.Rational(3,35)*s,8+sp.Rational(8,105)*d]
    cap_eigenvalues=[sp.Rational(112,15),sp.Rational(84,5),sp.Rational(56,3)]
    mean_v=[sp.expand(a-b) for a,b in zip(cap_eigenvalues,mean_m)]
    assert mean_v==[sp.Rational(64,15)+sp.Rational(4,105)*(t+d),
                    sp.Rational(48,5)+sp.Rational(3,35)*(t+d),
                    sp.Rational(32,3)-sp.Rational(8,105)*d]
    return dict(status='EXACT_LOCAL_AND_GLOBAL_COARSE_COUNTING_BUDGET',
                labels=LABELS,exterior_letters=OUTSIDE,bucket_indices=BUCKETS,
                local_inequality='15*||E||_F^2+86*tr(E)+92*sum_x_mate_pairs E[x,xbar]-74*sum(E)<=3520',
                equivalent_integer_terms=integer_terms(),integer_term_sum_upper_bound=3520,
                per_root_inequality='15*sum_21_line_pairs ||E||_F^2+464*t_v+144*d_v<=374976',
                global_inequality='5*sum_v_and_21_line_pairs ||E||_F^2+928*P+48*Z<=12374208',
                definitions=dict(P='Number of unordered pairs of disjoint triangles joined as a triangular prism.',
                                 t_v='Sum of the prism degrees of the seven triangle lines through v.',
                                 d_v='Number of far edges {a,x}~{abar,xbar} on two distinct root mate pairs.',
                                 Z='sum_v d_v: induced seven-vertex configurations with edges va,vabar,vx,vxbar,aabar,xxbar,ap,xp,abarq,xbarq,pq.',
                                 global_multiplicities='sum_v t_v=6P; sum_v d_v=Z.'),
                edge_weight_columns=['sum traceE','sum mate entries','sum overlap edges','sum all entries'],
                edge_type_weights=[dict(shared_letters=k[0],mate_incidence=k[1],weights=v) for k,v in weights.items()],
                per_root_count_identities=list(map(str,sums)),
                averaged_coarse_forms=dict(sector_order=['constant','mate_symmetric_zero_sum','mate_antisymmetric'],
                    dimensions=[1,4,5],M_eigenvalues=list(map(str,mean_m)),V_eigenvalues=list(map(str,mean_v)),
                    elementary_domain='t>=0, d>=0, t+2d<=84',
                    conclusion='Both averaged forms are automatically PSD on this elementary domain; averaged V is positive definite. In particular they cannot rule out t=0.',
                    at_t_d_zero=dict(M=[str(x.subs({t:0,d:0})) for x in mean_m],V=[str(x.subs({t:0,d:0})) for x in mean_v])),
                proof=[
                    'Compress T and U to the ten exterior incidence vectors: M=6I+2(J-Mt)-E, V=(176I+16Mt-44J)/15+E. In every Conway both are PSD. Their sum is(14/15)(19I-Mt-J). Consequently tr(MV)>=0. Expanding15 tr(MV) gives3520 minus the displayed local score.',
                    'At each root the far graph has84 vertices of degree12, hence504 edges. The14 far stars are matchings on12 labels, accounting for84 shared-label edges. Summing edges between each root mate pair gives t_v+b_v+2d_v=84. Thus the five edge-type counts are84-t,t,336+t+d,84-t-2d,d.',
                    'Counting how each single far edge contributes to the21 pairs of root lines gives the four coefficient sums recorded above. Summing the local budget then gives the per-root inequality. Finally sum_v t_v=6P and sum_v d_v=Z give the global inequality.',
                    'The score involves squared integer edge counts, hence ordered pairs of edges in the same buckets. The55 displayed univariate integer tables implement it exactly as one scalar budget. No automorphisms are required.'
                ],
                limitations='This is a necessary second-moment budget, not a positive lower bound on P or an exclusion of Conway. No solver speedup or independence from every pre-existing inequality is asserted.',
                validation='Exact compression and trace identity on own algebraic fixture; all84-label edge types enumerated; symbolic global coefficients checked. No peer graph audited.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',required=True)
    a=p.parse_args(); result=report()
    output=Path(a.output); output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('status','local_inequality','per_root_inequality','global_inequality','validation')}))
