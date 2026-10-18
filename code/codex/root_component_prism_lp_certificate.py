"""Exact linear lower certificates for prism incidence in fixed root Grams.

The LP only discovers multipliers. Rational multipliers and bound slacks
are then checked by exact arithmetic against every original edge column.
The exported identity is s-lower = a sum of necessary nonnegative slacks.
Equality slacks may have either multiplier sign. Upper-bound slacks have
nonpositive multipliers; reduced costs use the appropriate 0 or 1 bound.
No weighted-root upper bound is included in the LP itself.
"""
import argparse
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_propagation import LABELS,PAIRS,RECTANGLES,VARIABLE,constraints,propagate
from root_component_resources import limit_research_process,atomic_json_write
from root_component_low_budget_transport import digest


def matrix_of(cover,values):
    lift=[[F(*q) for q in row] for row in cover['lift_matrix']]
    small=[[F(0)]*len(lift[0]) for _ in lift[0]]
    for (i,j),q in zip(cover['anchor_pairs'],values):small[i][j]=small[j][i]=F(q)
    result=[[sum(x*small[a][b]*y for a,x in enumerate(u) for b,y in enumerate(v))
             for v in lift] for u in lift]
    assert all(q.denominator==1 for row in result for q in row)
    return [[int(q) for q in row] for row in result]


def system(template,matrix,matching_blossoms=False):
    propagated=propagate(template);assert not propagated['conflict']
    fixed={i:v for i,v,_ in propagated['assignments']}
    rows=[]
    def add(terms,target,equality,label):
        coefficients=defaultdict(int)
        for i,c in terms:
            if i in fixed:target-=c*fixed[i]
            else:coefficients[i]+=c
        rows.append({'label':label,'equality':equality,'rhs':target,
                     'terms':{i:c for i,c in coefficients.items() if c}})
    equations,bounds,_=constraints(template)
    for ids,target,reason in equations:add(((i,1) for i in ids),target,True,reason)
    for ids,target,reason in bounds:add(((i,1) for i in ids),target,False,reason)
    if matching_blossoms:
        lookup={label:w for w,label in enumerate(LABELS)}
        for root,parts in enumerate(template['nontrivial_component_groups']):
            for part in parts:
                for bit in (0,1):
                    star=[lookup[tuple(sorted((2*root+bit,a)))] for j in part for a in (2*j,2*j+1)]
                    for size in range(3,len(star),2):
                        for subset in combinations(star,size):
                            add(((VARIABLE[tuple(sorted((u,v)))],1) for u,v in combinations(subset,2)),
                                (size-1)//2,False,['matching_blossom',root,bit,list(part),list(subset)])
    edges=[tuple(e) for e in template['nongrid_edges']]
    for i,e in enumerate(edges):
        for j in range(i+1):
            f=edges[j]
            if i==j:
                terms=[(VARIABLE[tuple(sorted((u,v)))],2) for u,v in combinations(RECTANGLES[e],2)]
                rhs=8-matrix[i][i]
            else:
                terms=[(VARIABLE[tuple(sorted((u,v)))],1) for u in RECTANGLES[e] for v in RECTANGLES[f]]
                rhs=(0 if set(e)&set(f) else 4)-matrix[i][j]
            add(terms,rhs,True,['Gram',i,j])
    objective=defaultdict(int);constant=0
    for corners in RECTANGLES.values():
        for u,v in combinations(corners,2):
            if not set(LABELS[u]) & set(LABELS[v]):continue
            i=VARIABLE[tuple(sorted((u,v)))]
            if i in fixed:constant+=fixed[i]
            else:objective[i]+=1
    return fixed,rows,dict(objective),constant


def lower_certificate(template,matrix,matching_blossoms=False):
    from ortools.linear_solver import pywraplp
    fixed,rows,c,c0=system(template,matrix,matching_blossoms)
    solver=pywraplp.Solver.CreateSolver('GLOP');solver.SetTimeLimit(60000)
    variables={i:solver.NumVar(0,1,f'e{i}') for i in range(len(PAIRS)) if i not in fixed}
    cts=[]
    for ri,row in enumerate(rows):
        ct=solver.Constraint(row['rhs'] if row['equality'] else -solver.infinity(),row['rhs'],f'r{ri}')
        for i,value in row['terms'].items():ct.SetCoefficient(variables[i],value)
        cts.append(ct)
    for i,value in c.items():solver.Objective().SetCoefficient(variables[i],value)
    solver.Objective().SetOffset(c0);solver.Objective().SetMinimization()
    start=time.process_time();status=solver.Solve()
    result={'lp_status':int(status),'cpu_seconds':time.process_time()-start,'exact_certificate':False}
    if status!=solver.OPTIMAL:return result
    # A common dyadic denominator keeps the exported exact identity small.
    # Any rounding error is absorbed by the exact reduced-cost bound slacks.
    denominator=1<<20
    multipliers={i:F(round(ct.dual_value()*denominator),denominator) for i,ct in enumerate(cts)
                 if abs(ct.dual_value())>1e-8}
    multipliers={i:q for i,q in multipliers.items() if q}
    assert all(rows[i]['equality'] or q<=0 for i,q in multipliers.items())
    residual={i:F(c.get(i,0)) for i in variables};lower=F(c0)
    for ri,q in multipliers.items():
        row=rows[ri];lower+=q*row['rhs']
        for i,value in row['terms'].items():residual[i]-=q*value
    residual={i:q for i,q in residual.items() if q}
    lower+=sum(q for q in residual.values() if q<0)
    # Check the exported affine identity exactly, including its constant.
    collected=defaultdict(F)
    constant=-sum(q*rows[ri]['rhs'] for ri,q in multipliers.items())
    for ri,q in multipliers.items():
        for i,value in rows[ri]['terms'].items():collected[i]+=q*value
    for i,q in residual.items():collected[i]+=q
    constant-=sum(q for q in residual.values() if q<0)
    assert all(collected[i]==c.get(i,0) for i in variables)
    assert constant==F(c0)-lower
    return dict(result,exact_certificate=True,numerical_minimum=solver.Objective().Value(),
        exact_lower=str(lower),integer_lower=-((-lower.numerator)//lower.denominator),
        equality_or_upper_row_multipliers=[[i,str(q)] for i,q in sorted(multipliers.items())],
        variable_bound_multipliers=[[i,str(q),int(q<0)] for i,q in sorted(residual.items())],
        rows=len(rows),free_edge_columns_checked=len(variables),
        identity='s-lower=sum y_r*(A_r*x-b_r)+sum r_i*(x_i-bound_i)')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',type=Path);p.add_argument('--gram-cover',type=Path,required=True)
    p.add_argument('--projection-report',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--matching-blossoms',action='store_true',help='Add all odd-set inequalities within each internal star component.')
    a=p.parse_args();resources=limit_research_process(1)
    if a.output.exists():raise FileExistsError(a.output)
    report=json.loads(a.projection_report.read_text())
    assert report['source_gram_cover_sha256_lf']==digest(a.gram_cover)
    index=report['template_index'];templates=a.directory/'root_component_templates.json'
    template=json.loads(templates.read_text())['survivors'][index]
    cover=next(r for r in json.loads(a.gram_cover.read_text())['records'] if r['template_index']==index)
    positions={gi:i for i,gi in enumerate(cover['source_gram_indices'])}
    result={'scope':__doc__,'resources':resources,'template_index':index,
        'templates_sha256_lf':digest(templates),'gram_cover_sha256_lf':digest(a.gram_cover),
        'projection_report':str(a.projection_report),'projection_report_sha256_lf':digest(a.projection_report),
        'lower_bounds_valid_without_root_choice':True,'matching_blossoms':a.matching_blossoms,'cases':[]}
    for gi in report['excluded_gram_indices']:
        values=cover['gram_anchor_values'][positions[gi]]
        case=lower_certificate(template,matrix_of(cover,values),a.matching_blossoms)
        case.update(gram_index=gi,gram_anchor_values=values)
        case['excluded_at_weighted_root']=case.get('integer_lower',0)>report['root_choice']['root_prism_budget']
        result['cases'].append(case);atomic_json_write(a.output,result)
        print(json.dumps({k:case[k] for k in ('gram_index','lp_status','exact_certificate','excluded_at_weighted_root')}
                         |{k:case[k] for k in ('exact_lower','integer_lower') if k in case}),flush=True)


if __name__=='__main__':main()
