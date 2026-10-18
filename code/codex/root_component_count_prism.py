"""Count relaxation under global c>=4: at least77 grids and P>=6G.

Each root has at least seven grid rectangles, hence the total number G
of induced3x3 grids is at least77. Each grid contains six triangular
prisms. A prism can belong to at most one grid: the third vertices of its
three non-triangle edges are unique because lambda=1. Thus P>=6G.
The affine census is an input to this experiment, not regenerated here.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process


def run(source, minimum_grids):
    limit_research_process(1)
    from ortools.linear_solver import pywraplp
    raw=source.read_bytes();packet=json.loads(raw)
    assert packet['srg_parameters']==[99,14,1,2]
    names=packet['stages'][-1]['parameters'];rows=[]
    grid=next(r for r in packet['stages'][-1]['counts'] if r['degrees']==[4]*9)
    assert grid['code']==13262907120
    gform=list(map(F,grid['affine']))
    for stage in packet['stages']:
        assert stage['parameters']==names[:len(stage['parameters'])]
        for row in stage['counts']:
            coeff=list(map(F,row['affine']))
            coeff += [F(0)]*(len(names)+1-len(coeff))
            rows.append((f"count_{stage['order']}_{row['code']}",coeff))
    p=names.index('P')+1
    relation=[-6*x for x in gform];relation[p]+=1
    rows.append(('prisms_minus_six_grids',relation))
    lower=list(gform);lower[0]-=minimum_grids
    rows.append(('grid_lower_bound',lower))
    solver=pywraplp.Solver.CreateSolver('GLOP');solver.SetTimeLimit(30000)
    variables=[solver.NumVar(-solver.infinity(),solver.infinity(),name) for name in names]
    constraints=[];scales=[]
    for label,coeff in rows:
        scale=max(F(1),*(abs(x) for x in coeff[1:]))
        ct=solver.Constraint(float(-coeff[0]/scale),solver.infinity(),label)
        for j,value in enumerate(coeff[1:]):
            if value:ct.SetCoefficient(variables[j],float(value/scale))
        constraints.append(ct);scales.append(scale)
    solver.Objective().SetCoefficient(variables[p-1],1);solver.Objective().SetMaximization()
    started=time.process_time();status=solver.Solve()
    result={'scope':__doc__,'source':str(source),'source_sha256':hashlib.sha256(raw).hexdigest(),
        'minimum_grids':minimum_grids,'requires_global_minimum_components_four':minimum_grids==77,
        'solver_status':int(status),'cpu_seconds':time.process_time()-started,
        'rows':len(rows),'variables':len(variables),'exact_upper_certificate':False}
    if status!=solver.OPTIMAL:return result
    point=[v.solution_value() for v in variables]
    result.update(numerical_prism_upper=point[p-1],
                  numerical_grid_count=float(gform[0])+sum(float(c)*x for c,x in zip(gform[1:],point)))
    active=[i for i,c in enumerate(constraints) if abs(c.dual_value())>1e-8]
    weights=[F(-constraints[i].dual_value()/float(scales[i])).limit_denominator(1000000) for i in active]
    def certificate(ws):
        if any(w<0 for w in ws):return None
        total=[sum(w*rows[i][1][j] for i,w in zip(active,ws)) for j in range(len(names)+1)]
        target=[F(-int(j==p)) for j in range(1,len(names)+1)]
        if total[1:]!=target:return None
        return total[0]
    bound=certificate(weights)
    if bound is None:
        import sympy as sp
        a=sp.Matrix([[rows[i][1][j] for i in active] for j in range(1,len(names)+1)])
        rhs=sp.Matrix([-int(j==p) for j in range(1,len(names)+1)])
        try:
            solution,parameters=a.gauss_jordan_solve(rhs)
            weights=[F(str(x.subs({symbol:0 for symbol in parameters}))) for x in solution]
            bound=certificate(weights)
        except ValueError:pass
    if bound is not None:
        result.update(exact_upper_certificate=True,exact_upper=str(bound),
            integer_upper=bound.numerator//bound.denominator,
            certificate=[{'row':rows[i][0],'weight':str(w)} for i,w in zip(active,weights) if w],
            certificate_identity='sum(nonnegative weights * necessary nonnegative counts/bounds) = upper - P')
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--minimum-grids',type=int,choices=(0,77),default=77)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    if a.output.exists():raise FileExistsError(a.output)
    result=run(a.source,a.minimum_grids);atomic_json_write(a.output,result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('certificate','scope')}))


if __name__=='__main__':main()
