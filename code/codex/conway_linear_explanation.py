"""Explain a new CP contradiction by exact Boolean bound propagation.

This is an extraction tool for our construction failures, not an audit
of a peer solver. A failed extraction has no bearing on a CP verdict.
Only selected active linear constraints are used, with integer bounds.
"""
from fractions import Fraction
from math import gcd,lcm


def exact_farkas(rows,domains,proto):
    """A numerical LP proposes multipliers, then integer sums certify them."""
    from ortools.linear_solver import pywraplp
    inequalities=[]
    for row in rows:
        if row['upper'] < 2**60:
            inequalities.append(dict(variables=row['variables'],coefficients=row['coefficients'],
                                     bound=row['upper'],source=dict(guards=row['guards'],side='upper',proto_index=row['proto_index'])))
        if row['lower'] > -2**60:
            inequalities.append(dict(variables=row['variables'],coefficients=[-c for c in row['coefficients']],
                                     bound=-row['lower'],source=dict(guards=row['guards'],side='lower',proto_index=row['proto_index'])))
    for v,domain in domains.items():
        inequalities.append(dict(variables=[v],coefficients=[1],bound=domain[-1],source=dict(kind='variable_upper',name=proto.variables[v].name)))
        inequalities.append(dict(variables=[v],coefficients=[-1],bound=-domain[0],source=dict(kind='variable_lower',name=proto.variables[v].name)))
    solver=pywraplp.Solver.CreateSolver('GLOP')
    solver.SetTimeLimit(5000)
    weights=[solver.NumVar(0,1,'w%d'%i) for i in range(len(inequalities))]
    balance={v:solver.Constraint(0,0) for v in domains}
    normalization=solver.Constraint(1,1)
    objective=solver.Objective()
    for weight,row in zip(weights,inequalities):
        normalization.SetCoefficient(weight,1)
        objective.SetCoefficient(weight,row['bound'])
        for v,c in zip(row['variables'],row['coefficients']):
            balance[v].SetCoefficient(weight,c)
    objective.SetMinimization()
    status=solver.Solve()
    base=dict(status='NO_EXACT_LINEAR_SEPARATOR',complete=False,lp_status=int(status))
    if status not in (pywraplp.Solver.OPTIMAL,pywraplp.Solver.FEASIBLE):
        return base
    base['numerical_objective']=objective.Value()
    if objective.Value()>=-1e-8:
        return base
    raw=[w.solution_value() for w in weights]
    for denominator_limit in (1000,1000000,1000000000):
        rationals=[Fraction(v).limit_denominator(denominator_limit) if v>1e-9 else Fraction(0) for v in raw]
        denominator=lcm(*(v.denominator for v in rationals))
        integers=[v.numerator*(denominator//v.denominator) for v in rationals]
        divisor=gcd(*integers)
        if divisor:
            integers=[v//divisor for v in integers]
        coefficients={v:0 for v in domains}
        bound=0
        for weight,row in zip(integers,inequalities):
            bound+=weight*row['bound']
            for v,c in zip(row['variables'],row['coefficients']):
                coefficients[v]+=weight*c
        if min(integers)>=0 and bound<0 and not any(coefficients.values()):
            terms=[dict(weight=weight,**row) for weight,row in zip(integers,inequalities) if weight]
            used=sorted({v for row in terms for v in row['variables']})
            return dict(status='EXACT_INTEGER_FARKAS_CONTRADICTION',complete=True,
                        terms=terms,coefficient_sum_zero=True,summed_bound=bound,
                        variables=[dict(index=v,name=proto.variables[v].name,domain=domains[v]) for v in used],
                        numerical_objective=objective.Value())
    return base


def explain_linear(model,guard_names,active_guards):
    proto=model.Proto()
    active=set(active_guards)
    rows=[]
    for index,constraint in enumerate(proto.constraints):
        guards=list(constraint.enforcement_literal)
        if any(g not in active for g in guards) or not constraint.has_linear():
            continue
        data=constraint.linear
        if len(data.domain)!=2:
            continue
        rows.append(dict(proto_index=index,guards=[guard_names[g] for g in guards],
                         variables=list(map(int,data.vars)),coefficients=list(map(int,data.coeffs)),
                         lower=int(data.domain[0]),upper=int(data.domain[1])))
    involved=sorted({v for row in rows for v in row['variables']})
    # pybind repeated fields do not reliably implement Python negative
    # indexing; materialize the domains before accessing their last bound.
    domains={v:list(map(int,proto.variables[v].domain)) for v in involved}
    bounds={v:[domains[v][0],domains[v][-1]] for v in involved}
    assert all(a in (0,1) and b in (0,1) for a,b in bounds.values())
    trail=[]
    proof_of={}
    def limits(row):
        lo=sum(min(c*bounds[v][0],c*bounds[v][1]) for v,c in zip(row['variables'],row['coefficients']))
        hi=sum(max(c*bounds[v][0],c*bounds[v][1]) for v,c in zip(row['variables'],row['coefficients']))
        return lo,hi
    def dependencies(row,exclude=None):
        return [proof_of[v] for v in row['variables'] if v!=exclude and v in proof_of]
    def finish(contradiction):
        needed=set()
        def visit(step):
            if step in needed:
                return
            needed.add(step)
            for earlier in trail[step]['dependencies']:
                visit(earlier)
        for step in contradiction['dependencies']:
            visit(step)
        kept=sorted(needed)
        used_rows=sorted({contradiction['row']}|{trail[i]['row'] for i in kept})
        row_index={old:new for new,old in enumerate(used_rows)}
        step_index={old:new for new,old in enumerate(kept)}
        output=[]
        for i in kept:
            item=trail[i].copy()
            item['row']=row_index[item['row']]
            item['dependencies']=[step_index[j] for j in item['dependencies']]
            output.append(item)
        contradiction=dict(contradiction,row=row_index[contradiction['row']],
                           dependencies=[step_index[i] for i in contradiction['dependencies']])
        variables=sorted({v for i in used_rows for v in rows[i]['variables']})
        return dict(status='EXACT_BOUND_PROPAGATION_CONTRADICTION',complete=True,
                    constraints=[rows[i] for i in used_rows],
                    variables=[dict(index=v,name=proto.variables[v].name,domain=list(map(int,proto.variables[v].domain))) for v in variables],
                    forced=output,contradiction=contradiction,
                    original_constraint_count=len(rows),untrimmed_forced_count=len(trail))
    changed=True
    while changed:
        changed=False
        for ri,row in enumerate(rows):
            lo,hi=limits(row)
            if hi<row['lower'] or lo>row['upper']:
                return finish(dict(row=ri,possible_lower=lo,possible_upper=hi,
                                   required_lower=row['lower'],required_upper=row['upper'],
                                   dependencies=dependencies(row)))
            for v,c in zip(row['variables'],row['coefficients']):
                if bounds[v][0]==bounds[v][1]:
                    continue
                invalid=[]
                trials=[]
                for bit in (0,1):
                    low=lo-min(0,c)+c*bit
                    high=hi-max(0,c)+c*bit
                    trials.append([low,high])
                    invalid.append(high<row['lower'] or low>row['upper'])
                if all(invalid):
                    return finish(dict(row=ri,variable=v,bitwise_ranges=trials,
                                       required_lower=row['lower'],required_upper=row['upper'],
                                       dependencies=dependencies(row)))
                if any(invalid):
                    value=int(invalid[0])
                    step=dict(variable=v,name=proto.variables[v].name,value=value,row=ri,
                              rejected_value=1-value,rejected_range=trials[1-value],
                              dependencies=dependencies(row,exclude=v))
                    proof_of[v]=len(trail)
                    trail.append(step)
                    bounds[v]=[value,value]
                    changed=True
                    lo,hi=limits(row)
    result=exact_farkas(rows,domains,proto)
    result['bound_propagation_forced']=len(trail)
    return result
