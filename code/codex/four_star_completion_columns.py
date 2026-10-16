"""Construct columns from a saturated four-star block toward Conway99.

For a rank30 T block, global rank30 forces every new column into its
range and fixes its Schur norm. The range equations of U are necessary
as well. Integer congruences provide exact early impossibility witnesses.
"""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys
from math import lcm
from functools import reduce
from math import gcd
import time

import numpy as np
import sympy as sp
from sympy.matrices.normalforms import hermite_normal_form
from ortools.sat.python import cp_model
from ortools.linear_solver import pywraplp

sys.path.insert(0,str(Path(__file__).resolve().parent))
from hmatch_cycle_reflections import B, LABELS, load_graph
from hmatch_pure_switch_kernel_gate import integer_kernel


def prepare(record):
    gamma=load_graph(record)
    return prepare_gamma(gamma)


def prepare_gamma(gamma):
    mate=[r ^ 1 for r in range(14)]
    mate_gram=B.T@B[mate]
    t8=24*np.eye(44,dtype=np.int64)-8*gamma-3*(B.T@B)-mate_gram+2
    u15=60*np.eye(44,dtype=np.int64)+15*gamma-4*(B.T@B)+mate_gram-2
    kt,ku=integer_kernel(t8),integer_kernel(u15)
    assert not np.any(t8@kt) and not np.any(u15@ku)
    return gamma,t8,u15,kt,ku


def column_geometry(label):
    root=np.array([int(r in label) for r in range(14)],dtype=np.int64)
    intersection=B.T@root
    mate_incidence=B.T@root[[r ^ 1 for r in range(14)]]
    return 3*intersection+mate_incidence-2,4*intersection-mate_incidence+2


def range_constraints(label,kt,ku):
    k8,l15=column_geometry(label)
    equations=[]
    for form,kernel,offset,denominator,sign in [('T',kt,k8,8,-1),('U',ku,l15,15,1)]:
        for j in range(kernel.shape[1]):
            q=kernel[:,j]
            rhs=sign*int(q@offset)
            if rhs%denominator:
                return None,dict(form=form,outside_label=label,kernel_vector=list(map(int,q)),
                    required_integer_equation=dict(coefficients=list(map(int,q)),
                        rhs_numerator=rhs,rhs_denominator=denominator),
                    obstruction='An integer adjacency column cannot satisfy this kernel range equation.')
            equations.append((list(map(int,q)),rhs//denominator))
    return equations,None


def inverse_on_range(matrix):
    exact=sp.Matrix(matrix.tolist())
    pivots=list(exact.rref()[1])
    inverse=exact.extract(pivots,pivots).inv()
    denominator=lcm(*(int(x.q) for x in inverse))
    numerator=np.array([[int(x*denominator) for x in row] for row in inverse.tolist()],dtype=object)
    return pivots,numerator,denominator


def integer_range_certificate(label,kt,ku):
    equations,failure=range_constraints(label,kt,ku)
    if failure:
        return dict(status='INDIVIDUAL_CONGRUENCE',witness=failure)
    a=sp.Matrix([row for row,rhs in equations])
    b=sp.Matrix([rhs for row,rhs in equations])
    h=hermite_normal_form(a)
    rows=list(h.T.rref()[1])
    inverse=h.extract(rows,list(range(h.cols))).inv()
    coordinates=inverse*b.extract(rows,[0])
    if h*coordinates!=b:
        return dict(status='RATIONAL_RANGE_INCONSISTENT')
    fractional=next((j for j,x in enumerate(coordinates) if x.q!=1),None)
    if fractional is None:
        return dict(status='INTEGER_RANGE_SOLVABLE_BOUNDS_NOT_CHECKED',rank=h.cols)
    functional=sp.zeros(1,a.rows)
    for k,row in enumerate(rows):
        functional[row]=inverse[fractional,k]
    denominator=lcm(*(int(x.q) for x in functional))
    weights=[int(x*denominator) for x in functional]
    combined=(sp.Matrix([weights])*a)
    rhs=int((sp.Matrix([weights])*b)[0])
    coefficients=list(map(int,combined))
    assert all(x%denominator==0 for x in coefficients) and rhs%denominator
    return dict(status='EXACT_INTEGER_LATTICE_OBSTRUCTION',outside_label=label,
        equation_multipliers=weights,combined_coefficients=coefficients,
        combined_rhs=rhs,divisor=denominator,
        conclusion='Every left coefficient is divisible by divisor, but the integer right side is not.')


def column_inequalities(label,gamma,kt,ku):
    equations,failure=range_constraints(label,kt,ku)
    if failure:
        raise ValueError('An individual integer range congruence already fails.')
    rows=[]
    def add(coefficients,rhs,name):
        rows.append(dict(coefficients=list(map(int,coefficients)),rhs=int(rhs),name=name))
    for k,(coefficients,rhs) in enumerate(equations):
        add(coefficients,rhs,'range_%d_upper'%k)
        add([-x for x in coefficients],-rhs,'range_%d_lower'%k)
    for r in range(14):
        coefficients=[int(r in p) for p in LABELS]
        target=2-int(r in label)-int((r ^ 1) in label)
        add(coefficients,target,'root_%d_upper'%r)
        if r<4:
            add([-x for x in coefficients],-target,'root_%d_lower'%r)
    for i,p in enumerate(LABELS):
        coefficients=list(map(int,gamma[i]))
        coefficients[i]+=1
        add(coefficients,2-len(set(p)&set(label)),'common_neighbour_cap_%d'%i)
    capacity=2-gamma-gamma@gamma-B.T@B
    for i,j in combinations(range(44),2):
        if capacity[i,j]==0:
            add([int(k==i or k==j) for k in range(44)],1,'old_pair_cap_%d_%d'%(i,j))
    for i in range(44):
        coefficients=[int(j==i) for j in range(44)]
        add(coefficients,1,'binary_upper_%d'%i)
        add([-x for x in coefficients],0,'binary_lower_%d'%i)
    return rows


def farkas_certificate(label,gamma,kt,ku,extra_rows=()):
    """Find a short exact nonnegative combination giving 0 <= negative.

    GLOP only proposes a support. Its weights are reconstructed over Q
    and the final inequality is verified using Python integer arithmetic.
    """
    rows=column_inequalities(label,gamma,kt,ku)+list(extra_rows)
    solver=pywraplp.Solver.CreateSolver('GLOP')
    solver.SetTimeLimit(5000)
    weights=[solver.NumVar(0,solver.infinity(),'w_%d'%i) for i in range(len(rows))]
    for j in range(44):
        constraint=solver.Constraint(0,0)
        for w,row in zip(weights,rows):
            if row['coefficients'][j]:
                constraint.SetCoefficient(w,row['coefficients'][j])
    rhs_constraint=solver.Constraint(-1,-1)
    for w,row in zip(weights,rows):
        if row['rhs']:
            rhs_constraint.SetCoefficient(w,row['rhs'])
    objective=solver.Objective()
    for w in weights:
        objective.SetCoefficient(w,1)
    objective.SetMinimization()
    status=solver.Solve()
    if status!=pywraplp.Solver.OPTIMAL:
        return dict(status='NO_LINEAR_CERTIFICATE_FOUND',solver_status=status)
    support=[i for i,w in enumerate(weights) if w.solution_value()>1e-7]
    exact=sp.Matrix(45,len(support),lambda j,k:
        rows[support[k]]['coefficients'][j] if j<44 else rows[support[k]]['rhs'])
    solutions=sp.linsolve((exact,sp.Matrix([0]*44+[-1])))
    if solutions is sp.EmptySet:
        return dict(status='FLOAT_SUPPORT_NOT_EXACT')
    solution=next(iter(solutions))
    symbols=set().union(*(x.free_symbols for x in solution))
    solution=[x.subs({symbol:0 for symbol in symbols}) for x in solution]
    if any(x<0 for x in solution):
        return dict(status='EXACT_SUPPORT_HAS_NEGATIVE_WEIGHT')
    denominator=lcm(*(int(x.q) for x in solution))
    multipliers=[int(x*denominator) for x in solution]
    common=reduce(gcd,multipliers)
    multipliers=[x//common for x in multipliers]
    combined=[sum(weight*rows[i]['coefficients'][j] for i,weight in zip(support,multipliers)) for j in range(44)]
    rhs=sum(weight*rows[i]['rhs'] for i,weight in zip(support,multipliers))
    assert not any(combined) and rhs<0
    terms=[dict(multiplier=weight,**rows[i]) for i,weight in zip(support,multipliers) if weight]
    return dict(status='EXACT_FARKAS_CERTIFICATE',outside_label=label,terms=terms,
                combined_left_coefficients=combined,combined_rhs=rhs,
                conclusion='Every displayed inequality holds for a valid completion; their nonnegative integer sum gives 0 <= combined_rhs < 0.')


def binary_split_certificate(label,gamma,kt,ku):
    """Seek an adjacency entry forced strictly between0 and1 by the LP.

    Both binary cases are then refuted by exact integer Farkas sums.
    LP optima merely select a proposed split; they are not the proof.
    """
    rows=column_inequalities(label,gamma,kt,ku)
    solver=pywraplp.Solver.CreateSolver('GLOP')
    solver.SetTimeLimit(5000)
    variables=[solver.NumVar(-solver.infinity(),solver.infinity(),'d_%d'%i) for i in range(44)]
    for row in rows:
        constraint=solver.Constraint(-solver.infinity(),row['rhs'])
        for x,c in zip(variables,row['coefficients']):
            if c:
                constraint.SetCoefficient(x,c)
    objective=solver.Objective()
    for i in range(44):
        objective.Clear()
        objective.SetCoefficient(variables[i],1)
        objective.SetMinimization()
        if solver.Solve()!=pywraplp.Solver.OPTIMAL:
            return dict(status='LP_OPTIMIZATION_FAILED')
        lower=objective.Value()
        if lower<1e-7:
            continue
        objective.SetMaximization()
        if solver.Solve()!=pywraplp.Solver.OPTIMAL:
            return dict(status='LP_OPTIMIZATION_FAILED')
        upper=objective.Value()
        if upper>1-1e-7:
            continue
        positive=[int(j==i) for j in range(44)]
        zero=farkas_certificate(label,gamma,kt,ku,[dict(coefficients=positive,rhs=0,name='branch_d_%d_is0'%i)])
        one=farkas_certificate(label,gamma,kt,ku,[dict(coefficients=[-x for x in positive],rhs=-1,name='branch_d_%d_is1'%i)])
        if zero['status']==one['status']=='EXACT_FARKAS_CERTIFICATE':
            return dict(status='EXACT_BINARY_SPLIT_CERTIFICATE',outside_label=label,
                split_index=i,split_vertex_label=LABELS[i],case_zero=zero,case_one=one,
                conclusion='The adjacency entry is0 or1. Each case gives an exact integer contradiction.')
    return dict(status='NO_SINGLE_BINARY_SPLIT_FOUND')


def binary_tree_certificate(label,gamma,kt,ku,max_nodes=64):
    """Exact case-split proof, with an integer Farkas certificate at leaves."""
    rows=column_inequalities(label,gamma,kt,ku)
    solver=pywraplp.Solver.CreateSolver('GLOP')
    solver.SetTimeLimit(5000)
    variables=[solver.NumVar(-solver.infinity(),solver.infinity(),'d_%d'%i) for i in range(44)]
    for row in rows:
        constraint=solver.Constraint(-solver.infinity(),row['rhs'])
        for x,c in zip(variables,row['coefficients']):
            if c:
                constraint.SetCoefficient(x,c)
    count=0
    leaves=0
    def visit(branch_rows):
        nonlocal count,leaves
        count+=1
        if count>max_nodes:
            return dict(status='NODE_LIMIT')
        status=solver.Solve()
        if status==pywraplp.Solver.INFEASIBLE:
            certificate=farkas_certificate(label,gamma,kt,ku,branch_rows)
            if certificate['status']=='EXACT_FARKAS_CERTIFICATE':
                leaves+=1
            return certificate
        if status!=pywraplp.Solver.OPTIMAL:
            return dict(status='LP_FAILURE')
        values=[x.solution_value() for x in variables]
        fractional=[i for i,v in enumerate(values) if abs(v-round(v))>1e-7]
        if not fractional:
            return dict(status='NO_FRACTIONAL_BRANCH')
        index=max(fractional,key=lambda i:abs(values[i]-round(values[i])))
        children=[]
        for value in (0,1):
            variables[index].SetBounds(value,value)
            coefficients=[(1 if value==0 else -1)*int(j==index) for j in range(44)]
            extra=dict(coefficients=coefficients,rhs=-value,name='branch_d_%d_is%d'%(index,value))
            child=visit(branch_rows+[extra])
            variables[index].SetBounds(-solver.infinity(),solver.infinity())
            children.append(child)
            if child['status'] not in ('EXACT_FARKAS_CERTIFICATE','EXACT_BINARY_CASE_SPLIT'):
                return dict(status='INCOMPLETE_BINARY_TREE',failed_child=child)
        return dict(status='EXACT_BINARY_CASE_SPLIT',split_index=index,
                    split_vertex_label=LABELS[index],case_zero=children[0],case_one=children[1])
    tree=visit([])
    return dict(status=tree['status'],nodes=count,leaves=leaves,outside_label=label,tree=tree,
                scope='Binary adjacency case splits only; all terminal infeasibilities are exact nonnegative integer combinations of necessary inequalities.')


def linear_column_model(label,gamma,kt,ku):
    equations,failure=range_constraints(label,kt,ku)
    if failure:
        return None,None,failure
    model=cp_model.CpModel()
    variables=[model.NewBoolVar('d_%d'%i) for i in range(44)]
    for coefficients,rhs in equations:
        model.Add(sum(c*x for c,x in zip(coefficients,variables) if c)==rhs)
    for r in range(14):
        expression=sum(variables[i] for i,p in enumerate(LABELS) if r in p)
        target=2-int(r in label)-int((r ^ 1) in label)
        if r<4:
            model.Add(expression==target)
        else:
            model.Add(expression<=target)
    for i,p in enumerate(LABELS):
        model.Add(variables[i]+sum(variables[j] for j in range(44) if gamma[i,j])<=2-len(set(p)&set(label)))
    capacity=2-gamma-gamma@gamma-B.T@B
    for i,j in combinations(range(44),2):
        if capacity[i,j]==0:
            model.Add(variables[i]+variables[j]<=1)
    return model,variables,None


def probe_extension(gamma,seconds=10,per_column=.5,kernels=None):
    """Necessary binary range/cap feasibility for all40 missing vertices.

    This is a construction filter, not a sufficient completion test.
    UNKNOWN never excludes a candidate.
    """
    started=time.monotonic()
    if kernels is None:
        _,_,_,kt,ku=prepare_gamma(gamma)
    else:
        kt,ku=kernels
    witnessed=[]
    for label in [p for p in combinations(range(4,14),2) if p[1]!=(p[0] ^ 1)]:
        remaining=started+seconds-time.monotonic()
        if remaining<=0:
            return dict(status='UNKNOWN',label=label,processed=len(witnessed),seconds=time.monotonic()-started)
        model,variables,failure=linear_column_model(label,gamma,kt,ku)
        if failure:
            return dict(status='NO_INTEGER_COLUMN',label=label,failure=failure,seconds=time.monotonic()-started)
        solver=cp_model.CpSolver()
        solver.parameters.num_search_workers=1
        solver.parameters.max_time_in_seconds=min(remaining,per_column)
        status=solver.Solve(model)
        if status==cp_model.INFEASIBLE:
            return dict(status='NO_BINARY_COLUMN',label=label,processed=len(witnessed),seconds=time.monotonic()-started)
        if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            return dict(status='UNKNOWN',label=label,processed=len(witnessed),seconds=time.monotonic()-started)
        witnessed.append(dict(label=label,neighbours=[i for i,x in enumerate(variables) if solver.Value(x)]))
    return dict(status='ALL_LINEAR_COLUMNS_FEASIBLE',columns=witnessed,seconds=time.monotonic()-started,
                scope='Necessary binary range equations and partial common-neighbour caps only. Schur norms and mutual compatibility still required.')


def enumerate_column(label,gamma,kt,ku,t_inverse,u_inverse,seconds):
    model,variables,failure=linear_column_model(label,gamma,kt,ku)
    if failure:
        return dict(label=label,status='CONGRUENCE_IMPOSSIBLE',complete=True,domains=[],failure=failure)
    k8,l15=column_geometry(label)
    ti,tn,td=t_inverse
    ui,un,ud=u_inverse
    domains=[]
    stats=Counter()
    rejected_examples=[]

    class Collect(cp_model.CpSolverSolutionCallback):
        def on_solution_callback(self):
            d=np.array([self.Value(x) for x in variables],dtype=np.int64)
            b=(-8*d-k8)[ti].astype(object)
            norm_t=int(b@tn@b)
            stats['binary_range_solutions']+=1
            if norm_t!=20*td:
                stats['WRONG_T_SCHUR_NORM']+=1
                if len(rejected_examples)<3:
                    rejected_examples.append(dict(neighbours=np.flatnonzero(d).tolist(),
                        T_norm_numerator=str(norm_t),T_norm_denominator=str(td),required_T_norm=20))
                return
            u=(15*d-l15)[ui].astype(object)
            residual=50*ud-int(u@un@u)
            if residual<0:
                stats['NEGATIVE_U_SCHUR_DIAGONAL']+=1
                return
            stats['ADMISSIBLE_COLUMNS']+=1
            domains.append(dict(neighbours=np.flatnonzero(d).tolist(),
                T_coordinates=list(map(int,b)),U_coordinates=list(map(int,u)),
                U_residual_numerator=str(residual),U_residual_denominator=str(ud)))

    solver=cp_model.CpSolver()
    solver.parameters.num_search_workers=1
    solver.parameters.max_time_in_seconds=max(.01,seconds)
    solver.parameters.enumerate_all_solutions=True
    callback=Collect()
    status=solver.Solve(model,callback)
    return dict(label=label,status=solver.StatusName(status),
        complete=status in (cp_model.OPTIMAL,cp_model.INFEASIBLE),
        domains=domains,statistics=dict(stats),rejected_examples=rejected_examples,
        solver_seconds=solver.WallTime())


def run(source,output,columns=False,seconds=45,per_column=5):
    started=time.monotonic()
    record=json.loads(Path(source).read_text(encoding='utf-8'))
    gamma,t8,u15,kt,ku=prepare(record)
    outside=[p for p in combinations(range(4,14),2) if p[1]!=(p[0] ^ 1)]
    failures=[]
    for label in outside:
        _,failure=range_constraints(label,kt,ku)
        if failure is not None:
            failures.append(failure)
    result=dict(source_file=str(source),outside_labels=40,
        T_kernel_dimension_used=kt.shape[1],U_kernel_dimension_used=ku.shape[1],
        congruence_obstructions=failures,
        status='NO_INTEGER_COMPLETION' if failures else 'RANGE_CONGRUENCES_PASS_NOT_A_COMPLETION',
        scope='Necessary integer range equations for the same fixed labelled block in a full SRG99. Passing is not sufficient.')
    if columns and not failures:
        assert kt.shape[1]==14, 'This completion mode requires T rank exactly30.'
        t_inverse,u_inverse=inverse_on_range(t8),inverse_on_range(u15)
        result['column_domains']=[]
        result['T_inverse_numerator']=[[str(x) for x in row] for row in t_inverse[1]]
        result['T_inverse_denominator']=str(t_inverse[2])
        result['U_inverse_numerator']=[[str(x) for x in row] for row in u_inverse[1]]
        result['U_inverse_denominator']=str(u_inverse[2])
        result['T_pivot_indices']=t_inverse[0]
        result['U_pivot_indices']=u_inverse[0]
        print(json.dumps(dict(stage='COLUMN_ENUMERATION',T_rank=len(t_inverse[0]),U_rank=len(u_inverse[0]))),flush=True)
        for label in outside:
            remaining=started+seconds-time.monotonic()
            if remaining<=0:
                result['status']='COLUMN_SEARCH_TIME_LIMIT'
                break
            entry=enumerate_column(label,gamma,kt,ku,t_inverse,u_inverse,min(per_column,remaining))
            result['column_domains'].append(entry)
            print(json.dumps({k:v for k,v in entry.items() if k not in ('domains','rejected_examples')}
                             | dict(domain_size=len(entry['domains']))),flush=True)
            if entry['complete'] and not entry['domains']:
                result['status']='NO_COMPLETION_EMPTY_COLUMN_DOMAIN'
                result['empty_label']=label
                if entry['status']=='INFEASIBLE':
                    result['integer_range_certificate']=integer_range_certificate(label,kt,ku)
                    print(json.dumps(dict(stage='INTEGER_RANGE_CERTIFICATE',**result['integer_range_certificate'])),flush=True)
                    result['linear_certificate']=farkas_certificate(label,gamma,kt,ku)
                    cert=result['linear_certificate']
                    print(json.dumps(dict(stage='CERTIFICATE',status=cert['status'],
                        terms=len(cert.get('terms',[])),rhs=cert.get('combined_rhs'))),flush=True)
                    if cert['status']!='EXACT_FARKAS_CERTIFICATE':
                        result['binary_certificate']=binary_split_certificate(label,gamma,kt,ku)
                        cert=result['binary_certificate']
                        print(json.dumps(dict(stage='BINARY_CERTIFICATE',status=cert['status'],
                            split_vertex=cert.get('split_vertex_label'))),flush=True)
                        if cert['status']!='EXACT_BINARY_SPLIT_CERTIFICATE':
                            result['binary_tree_certificate']=binary_tree_certificate(label,gamma,kt,ku)
                            cert=result['binary_tree_certificate']
                            print(json.dumps(dict(stage='TREE_CERTIFICATE',status=cert['status'],
                                nodes=cert['nodes'],leaves=cert['leaves'])),flush=True)
                break
            if not entry['complete']:
                result['status']='COLUMN_SEARCH_INCOMPLETE'
                break
        else:
            result['status']='ALL_40_COLUMN_DOMAINS_COMPLETE_PAIR_JOIN_REQUIRED'
        result['seconds']=time.monotonic()-started
    Path(output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],failed_outside_labels=len(failures),
                         processed_columns=len(result.get('column_domains',[])),empty_label=result.get('empty_label'),
                         first_obstruction=failures[0] if failures else None)),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--columns',action='store_true')
    parser.add_argument('--seconds',type=float,default=45)
    parser.add_argument('--per-column',type=float,default=5)
    args=parser.parse_args()
    run(args.source,args.output,args.columns,args.seconds,args.per_column)
