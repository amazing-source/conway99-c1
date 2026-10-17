"""Find an exact P=0 point in the accepted order-nine counting relaxation.

Consumes existing affine census identities; does not regenerate or audit
the census. A feasible point is a counting relaxation, never a graph.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import time

from ortools.linear_solver import pywraplp


def investigate(source, seconds):
    started=time.monotonic()
    raw=Path(source).read_bytes()
    data=json.loads(raw)
    names=data['parameters']
    rows=[[(j,F(x)) for j,x in enumerate(row['affine']) if F(x)] for row in data['counts']]
    solver=pywraplp.Solver.CreateSolver('GLOP')
    solver.SetTimeLimit(int(1000*seconds))
    variables=[solver.NumVar(0,0 if name=='P' else solver.infinity(),name) for name in names]
    for row in rows:
        constant=next((c for j,c in row if j==0),F(0))
        scale=max((abs(c) for j,c in row if j>0),default=F(1))
        constraint=solver.Constraint(float(-constant/scale),solver.infinity())
        for j,c in row:
            if j:
                constraint.SetCoefficient(variables[j-1],float(c/scale))
    # A sparse basic solution is easier to reconstruct exactly.
    for variable in variables:
        solver.Objective().SetCoefficient(variable,1)
    solver.Objective().SetMinimization()
    status=solver.Solve()
    answer=dict(source=str(Path(source).resolve()),source_sha256=sha256(raw).hexdigest(),
                supplied_census_types=len(rows),parameters=len(names),
                solver_status=int(status),scope='The supplied order9 affine counting relaxation only; no realization as a graph asserted.')
    if status not in (solver.OPTIMAL,solver.FEASIBLE):
        answer['status']='NO_FEASIBLE_POINT_RETURNED_NO_EXACT_CONCLUSION'
        return answer
    approximation=[v.solution_value() for v in variables]
    def assess(point):
        if min(point)<0 or point[names.index('P')]!=0:
            return None
        augmented=[F(1)]+point
        values=[sum(c*augmented[j] for j,c in row) for row in rows]
        if min(values)<0:
            return None
        return values
    point=values=None
    for denominator in (1,2,6,12,60,360,2520,10000,1000000):
        proposal=[F(x).limit_denominator(denominator) for x in approximation]
        test=assess(proposal)
        if test is not None:
            point,values=proposal,test
            break
    if point is None:
        # Reconstruct the numerical basic point using exact active equations.
        import sympy as sp
        equations=[]
        targets=[]
        for j,x in enumerate(approximation):
            if abs(x)<1e-6:
                equations.append([int(i==j) for i in range(len(names))]); targets.append(F(0))
        for row in rows:
            constant=next((c for j,c in row if j==0),F(0))
            terms=[float(c)*approximation[j-1] for j,c in row if j]
            residual=float(constant)+sum(terms)
            scale=max(1,abs(float(constant)),sum(map(abs,terms)))
            if abs(residual)<=1e-9*scale:
                coefficients=[F(0)]*len(names)
                for j,c in row:
                    if j: coefficients[j-1]=c
                equations.append(coefficients); targets.append(-constant)
        matrix=sp.Matrix(equations)
        pivots=matrix.T.rref()[1]
        if len(pivots)==len(names):
            selected=matrix[list(pivots),:]
            target=sp.Matrix([targets[i] for i in pivots])
            proposal=[F(str(x)) for x in selected.inv(method='DM')*target]
            test=assess(proposal)
            if test is not None:
                point,values=proposal,test
    answer['seconds']=time.monotonic()-started
    if point is None:
        answer.update(status='NUMERICAL_P_ZERO_POINT_ONLY',numerical_point=dict(zip(names,approximation)))
        return answer
    answer.update(status='EXACT_FEASIBLE_P_ZERO_CENSUS_POINT',
                  point={name:str(x) for name,x in zip(names,point)},
                  minimum_count=str(min(values)),zero_counts=sum(x==0 for x in values),
                  nonintegral_counts=sum(x.denominator!=1 for x in values),
                  all_5311_counts_nonnegative_exactly=True,
                  total_order9_count=str(sum(values)),
                  conclusion='This real counting relaxation has no positive lower bound on P; integer graph existence is not implied.')
    return answer


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',required=True)
    p.add_argument('--seconds',type=float,default=15)
    p.add_argument('--output',required=True)
    a=p.parse_args()
    result=investigate(a.source,a.seconds)
    output=Path(a.output); output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('point','numerical_point')}))
