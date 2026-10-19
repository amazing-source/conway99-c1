"""Exact failed-profile cuts from the joint assignment LP.

Each outside label chooses one known-neighbour profile. Known common-
neighbour counts and upper-letter counts are exact. In addition:
 * two outside vertices cannot share three known neighbours;
 * two outside vertices carrying the same upper letter cannot share
   two known neighbours.
These yield clique bounds stronger than pairwise incompatibilities in
the fractional relaxation. A failed x[p]=1 assumption refutes that
binary profile only after an INTEGER Farkas certificate is replayed.
Deleted profiles can be used in subsequent certificates. No floating
point infeasibility alone is an exclusion.
"""

from collections import defaultdict
from itertools import combinations
import time

from root_component_profile_star_lp import solve_system, check_certificate


def assignment_system(rows, known, outside, domains, root_count=7):
    options = [(x,pi) for x,d in enumerate(domains) for pi in range(len(d))]
    features = defaultdict(list); triples = defaultdict(list); stars = defaultdict(list)
    for j,(x,pi) in enumerate(options):
        p = sorted(domains[x][pi])
        features['one',x].append(j)
        for u,v in combinations(p,2):
            features['pair',u,v].append(j)
            for l in outside[x]:
                stars[u,v,l].append(j)
        for u in p:
            features['degree',u].append(j)
            for l in outside[x]:
                features['letter',u,l].append(j)
        for triple in combinations(p,3):
            triples[triple].append(j)
    demands = {('one',x):1 for x in range(len(domains))}
    for u,row in enumerate(rows):
        demands['degree',u] = 2*root_count-2-row.bit_count()
        for v in range(u+1,len(rows)):
            demands['pair',u,v] = 2-((row>>v)&1)-len(set(known[u])&set(known[v]))-(row&rows[v]).bit_count()
        for l in range(2*root_count):
            demands['letter',u,l] = (1 if l//2 in {a//2 for a in known[u]} else 2)-sum(
                l in known[v] for v in range(len(rows)) if row&(1<<v))
    constraints = [{'kind':k[0],'key':k[1:],'sense':'=','rhs':rhs,'columns':features[k]}
                   for k,rhs in demands.items()]
    for kind,group in (('triple_known',triples),('known_pair_letter',stars)):
        for key,columns in sorted(group.items()):
            if len({options[j][0] for j in columns})<=1:
                continue
            if kind=='known_pair_letter' and demands['pair',key[0],key[1]]<=1:
                continue
            constraints.append({'kind':kind,'key':key,'sense':'<=','rhs':1,'columns':columns})
    return options,constraints


def fixed(j,value):
    return {'kind':'fixed_profile','key':j,'sense':'=','rhs':value,'columns':[j]}


def replay(rows,known,outside,domains,report,root_count=7):
    options,cs=assignment_system(rows,known,outside,domains,root_count)
    for step in report['cuts']:
        j=step['column']
        assert list(options[j])==list(step['option'])
        assert check_certificate(options,cs+[fixed(j,1)],step['certificate'])
        cs.append(fixed(j,0))
    if report.get('terminal_certificate') is not None:
        assert check_certificate(options,cs,report['terminal_certificate'])
    assert report['status']!='EXCLUDED_ASSIGNMENT_LP' or report.get('terminal_certificate') is not None
    return True


def filter_assignment(rows,known,outside,domains,root_count=7,cpu_seconds=45,on_progress=None):
    from ortools.linear_solver import pywraplp
    options,cs=assignment_system(rows,known,outside,domains,root_count)
    s=pywraplp.Solver.CreateSolver('GLOP');s.SetTimeLimit(1000)
    vs=[s.NumVar(0,s.infinity(),'x%d'%j) for j in range(len(options))]
    def add(c):
        r=s.Constraint(c['rhs'] if c['sense']=='=' else -s.infinity(),c['rhs'])
        for j in c['columns']:r.SetCoefficient(vs[j],1)
    for c in cs:add(c)
    guard=s.Constraint(0,s.infinity(),'assumption')
    active=set(range(len(options)));cuts=[];passes=[];start=time.process_time()
    report={'scope':'Certified necessary profile deletions; fractional feasibility is not a graph.',
            'status':'PASSES_ASSIGNMENT_LP','cuts':cuts,'passes':passes,'variables':len(options)}
    while True:
        status=s.Solve()
        if status==s.INFEASIBLE:
            proof=solve_system(options,cs,simplify=False)
            if 'certificate' in proof:
                report.update(status='EXCLUDED_ASSIGNMENT_LP',terminal_certificate=proof['certificate'])
            else:report['status']='UNKNOWN_UNVERIFIED_LP'
            break
        if status!=s.OPTIMAL:
            report['status']='UNKNOWN_LP';break
        before=len(cuts);tested=0
        for j in sorted(active):
            if time.process_time()-start>=cpu_seconds:
                report['status']='BUDGET_PARTIAL_ASSIGNMENT_LP';break
            guard.SetCoefficient(vs[j],1);guard.SetBounds(1,1)
            status=s.Solve();tested+=1
            guard.SetCoefficient(vs[j],0);guard.SetBounds(0,s.infinity())
            if status!=s.INFEASIBLE:continue
            proof=solve_system(options,cs+[fixed(j,1)],simplify=False)
            if 'certificate' not in proof:continue
            assert check_certificate(options,cs+[fixed(j,1)],proof['certificate'])
            step={'column':j,'option':options[j],'certificate':proof['certificate']}
            cuts.append(step);active.remove(j);cs.append(fixed(j,0));add(cs[-1])
            if on_progress is not None and len(cuts)%20==0:
                on_progress({'cuts':len(cuts),'cpu_seconds':time.process_time()-start})
        passes.append({'tested':tested,'new_cuts':len(cuts)-before})
        if report['status'].startswith('BUDGET') or len(cuts)==before:break
    report['cpu_seconds']=time.process_time()-start
    kept={options[j] for j in active}
    report['kept_indices']=[[pi for pi in range(len(d)) if (x,pi) in kept]
                            for x,d in enumerate(domains)]
    assert replay(rows,known,outside,domains,report,root_count)
    return report


def controls():
    result=filter_assignment([0],[(0,2)],[(0,3),(1,2),(1,3)],[[[0]],[[0]],[[],[0]]],root_count=2)
    assert result['status']=='PASSES_ASSIGNMENT_LP'
    assert result['kept_indices']==[[0],[0],[0]]
    assert replay([0],[(0,2)],[(0,3),(1,2),(1,3)],[[[0]],[[0]],[[],[0]]],result,2)
    return {'actual_rook_completion_preserved':True,'false_profile_certified':True}
