"""Certify our own rational fractional boundary; never call it a graph.

All linear constraints, the forced kernels, positive principal quotients,
and the nonlinear far common-neighbour caps are checked exactly. The
certificate explicitly distinguishes the linear relaxation from full C2.
"""
import argparse
from fractions import Fraction
from math import lcm
from pathlib import Path
import json
import sys
import time

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from three_star_prescribed_kernel import N, LABELS, EDGES, K8, U0, S, linear_constraints
from three_star_ambient_upper import psd_or_witness


def certify(path, denominator_bound):
    start=time.monotonic()
    source=json.loads(Path(path).read_text(encoding='utf-8-sig'))
    q=np.array(source['q'],dtype=np.int64)
    values={e:Fraction(source['last_fractional_gamma'][e[0]][e[1]]).limit_denominator(denominator_bound)
            for e in EDGES}
    assert all(0<=x<=1 for x in values.values())
    denominator=lcm(*(x.denominator for x in values.values()))
    numerator=np.zeros((N,N),dtype=object)
    for (i,j),value in values.items():
        numerator[i,j]=numerator[j,i]=int(value*denominator)
    violations=[]
    rows=list(linear_constraints(q,connected_Q=True))
    for number,(row,lo,hi,origin) in enumerate(rows):
        value=sum(a*values[e] for e,a in row.items())
        if (lo is not None and value<lo) or (hi is not None and value>hi):
            violations.append(dict(row=number,origin=origin,value=str(value)))
    report=dict(source=str(path),profile_index=source['profile_index'],labels=LABELS,q=source['q'],
                denominator=denominator,gamma_numerator=numerator.tolist(),linear_rows=len(rows),
                linear_violations=violations,
                fractional_undirected_entries=sum(0<x<1 for x in values.values()),
                is_a_binary_graph=all(x in (0,1) for x in values.values()))
    if violations:
        report['status']='RATIONAL_RECONSTRUCTION_FAILS_LINEAR_CONSTRAINTS'
        return report
    matrices={'T':denominator*(24*np.eye(N,dtype=object)-K8)-8*numerator,
              'U':denominator*U0+15*numerator}
    forced={'T':np.column_stack((S,q)), 'U':S}
    for name,matrix in matrices.items():
        assert not np.any(matrix@forced[name])
        anchors=sp.Matrix(forced[name].T.tolist()).rref()[1]
        indices=[i for i in range(N) if i not in anchors]
        # Matrices are scaled to integers before calling the exact routine.
        quotient=sp.Matrix(matrix[np.ix_(indices,indices)].tolist())
        result=psd_or_witness(quotient)
        report[name]=dict(integer_scaling=('8T' if name=='T' else '15U')+' times denominator',
                          quotient_indices=indices,quotient_certificate=result,
                          forced_nullity=len(anchors))
        if result['psd']:
            # Exact positive leading Schur pivots certify strict positivity,
            # hence full quotient rank without re-running a rank algorithm.
            reduced=quotient.copy()
            pivots=[]
            for i in range(len(indices)):
                pivot=reduced[i,i]
                assert pivot>0
                pivots.append(str(pivot))
                for j in range(i+1,len(indices)):
                    for k in range(j,len(indices)):
                        value=reduced[j,k]-reduced[j,i]*reduced[i,k]/pivot
                        reduced[j,k]=reduced[k,j]=value
            report[name].update(exact_rank=len(indices),positive_pivots=pivots)
    cap_violations=[]
    mccormick_violations=[]
    for i,j in EDGES:
        cap=2-len(set(LABELS[i])&set(LABELS[j]))
        actual=sum(numerator[i,k]*numerator[j,k] for k in range(N))+denominator*numerator[i,j]
        if actual>cap*denominator*denominator:
            cap_violations.append(dict(pair=[i,j],labels=[LABELS[i],LABELS[j]],
                excess=str(Fraction(int(actual-cap*denominator*denominator),denominator*denominator))))
        lower=sum(max(0,numerator[i,k]+numerator[j,k]-denominator) for k in range(N) if k not in (i,j))+numerator[i,j]
        if lower>cap*denominator:
            mccormick_violations.append(dict(pair=[i,j],excess=str(Fraction(int(lower-cap*denominator),denominator))))
    report['far_common_neighbour_cap_violations']=cap_violations
    report['McCormick_common_neighbour_violations']=mccormick_violations
    report['status']=('EXACT_FRACTIONAL_T_AND_U_PSD_POINT' if all(report[name]['quotient_certificate']['psd'] for name in ('T','U'))
                      else 'RATIONAL_POINT_NOT_PSD')
    report['scope']='This rational point certifies only the constraints explicitly reported as satisfied. Fractional edges are not a graph and do not refute(A).'
    report['elapsed_seconds']=time.monotonic()-start
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',required=True)
    parser.add_argument('--denominator-bound',type=int,default=1000000)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    report=certify(args.input,args.denominator_bound)
    Path(args.output).write_text(json.dumps(report,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('status','denominator','fractional_undirected_entries','elapsed_seconds') if k in report}))
    print(json.dumps(dict(linear_violations=len(report['linear_violations']),
        C2_violations=len(report.get('far_common_neighbour_cap_violations',[])),
        McCormick_violations=len(report.get('McCormick_common_neighbour_violations',[])),
        ranks={name:report[name].get('exact_rank') for name in ('T','U') if name in report})))


if __name__=='__main__':
    main()
