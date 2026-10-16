"""Global Conway search with cardinalities and certified lazy cuts.

Every candidate already has ALL root-incidence counts exactly right.
Consequently it is (k-2)-regular. For every row p of Gamma,

 sum_{q!=p} (Gamma^2[p,q]+Gamma[p,q]+|p intersect q|)
 = (k-2)(k-3)+(k-2)+2(k-3) = k*(k-2)-2 = 2*(n-1).

Thus the upper bounds Gamma^2[p,q]+Gamma[p,q]+|p intersect q|<=2
force equality for EVERY pair. No lower-bound products are necessary.
An excessive entry supplies a positive forbidden pattern on3,4,5 or6
edges, encoded by ONE clause. All such clauses are universal necessary
conditions, independently of the candidate that exposed them.

The search covers all graphs via conway_global_cover's normalization.
It retains learned clauses between candidates and only terminates SAT
after the exact 99-vertex test. The space is finite, but affordable
exhaustion is NOT proved. UNKNOWN and a near-solution are not exclusions.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import sys
from threading import Timer
import time

import numpy as np
from pysat.solvers import Solver
from pysat.card import CardEnc,EncType
from pysat.formula import IDPool
from ortools.sat.python import cp_model

sys.path.insert(0,str(Path(__file__).resolve().parent))
from conway_global_cover import coverage,reconstruct_and_check


class CardinalityCP:
    """CP candidate engine; retains explicit universal cuts, not CDCL state."""
    def __init__(self,variable_count,clauses):
        self.model=cp_model.CpModel()
        self.variables=[None]+[self.model.NewBoolVar('e_%d'%i) for i in range(1,variable_count+1)]
        self.solver=cp_model.CpSolver()
        self.solver.parameters.num_search_workers=1
        self.solver.parameters.symmetry_level=0
        self.solver.parameters.cp_model_probing_level=0
        self.stats=dict(conflicts=0,branches=0,wall_time=0.0)
        for clause in clauses:
            self.add_clause(clause)
    def literal(self,lit):
        return self.variables[lit] if lit>0 else self.variables[-lit].Not()
    def add_clause(self,clause):
        self.model.AddBoolOr([self.literal(lit) for lit in clause])
    def add_atmost(self,lits,bound):
        self.model.Add(sum(self.literal(lit) for lit in lits)<=bound)
    def supports_atmost(self):
        return True
    def clear_interrupt(self):
        pass
    def interrupt(self):
        self.solver.StopSearch()
    def solve_limited(self,expect_interrupt=True):
        status=self.solver.Solve(self.model)
        self.stats['conflicts']+=self.solver.NumConflicts()
        self.stats['branches']+=self.solver.NumBranches()
        self.stats['wall_time']+=self.solver.WallTime()
        if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            return True
        if status==cp_model.INFEASIBLE:
            return False
        assert status==cp_model.UNKNOWN,self.solver.StatusName(status)
        return None
    def get_model(self):
        return [i if self.solver.Value(var) else -i for i,var in enumerate(self.variables) if i]
    def accum_stats(self):
        return self.stats
    def set_phases(self,literals):
        self.model.ClearHints()
        for lit in literals:
            self.model.AddHint(self.variables[abs(lit)],int(lit>0))
    def __enter__(self):
        return self
    def __exit__(self,*args):
        pass


def problem(k=14,low_prism_flag=False):
    assert k>=4 and k%2==0
    if low_prism_flag:
        assert k==14
    labels=[p for p in combinations(range(k),2) if p[1]!=(p[0]^1)]
    index={p:i for i,p in enumerate(labels)}
    n=len(labels)
    graph=np.zeros((n,n),dtype=np.int64)
    edges=list(combinations(range(n),2))
    for var,(p,q) in enumerate(edges,1):
        graph[p,q]=graph[q,p]=var
    cards=[]
    clauses=[]
    def exactly(lits,value):
        cards.extend([(lits,value),([-v for v in lits],len(lits)-value)])
    for p,label in enumerate(labels):
        # Degree follows by summing the root equations, so is not duplicated.
        for r in range(k):
            lits=[int(graph[p,q]) for q,other in enumerate(labels) if r in other and p!=q]
            exactly(lits,2-int(r in label)-int((r^1) in label))
    cover=coverage(k,pointed=low_prism_flag)
    a=0 if low_prism_flag or k==4 else 4
    letters=[r for r in range(k) if r not in (a,a^1)]
    star=[index[tuple(sorted((a,r)))] for r in letters]
    selectors=list(range(len(edges)+1,len(edges)+1+cover['case_count']))
    exactly(selectors,1)
    for selector,case in zip(selectors,cover['cases']):
        for p,q in case['canonical_matching']:
            clauses.append([-selector,int(graph[star[p],star[q]])])
    if low_prism_flag:
        def edge(p,q):
            return int(graph[index[tuple(sorted(p))],index[tuple(sorted(q))]])
        low=[edge((0,y),(1,y)) for y in range(2,k)]
        cards.append((low,7))
        for a in range(2,k,2):
            other=[edge((a,y),(a^1,y)) for y in range(k) if y not in (a,a^1)]
            cards.append((low+[-v for v in other],len(other)))
        clauses.append([-edge((0,2),(0,3)),-edge((1,2),(1,3)),
                        -edge((0,2),(1,2)),-edge((0,3),(1,3))])
    return labels,graph,edges,cards,clauses,selectors,cover


def certified_clause(labels,graph,witness):
    """Validate a universal positive-pattern cut, using only its labels."""
    p,q=map(int,witness['pair'])
    common=list(map(int,witness['common_vertices']))
    assert p!=q and len(set(common))==len(common) and p not in common and q not in common
    cap=2-len(set(labels[p])&set(labels[q]))
    adjacent=bool(witness['include_pair_edge'])
    assert len(common)+int(adjacent)==cap+1
    edge_vars=[int(graph[p,q])] if adjacent else []
    for z in common:
        edge_vars.extend([int(graph[p,z]),int(graph[q,z])])
    assert min(edge_vars)>0 and len(set(edge_vars))==len(edge_vars)
    return tuple(-v for v in sorted(edge_vars))


def separate(labels,graph,candidate,per_pair=4):
    square=candidate@candidate
    n=len(labels)
    cuts={}
    excess=0
    defective_pairs=0
    for p,q in combinations(range(n),2):
        cap=2-len(set(labels[p])&set(labels[q]))
        value=int(square[p,q])+int(candidate[p,q])
        if value<=cap:
            continue
        excess+=value-cap
        defective_pairs+=1
        common=np.flatnonzero(candidate[p]&candidate[q]).tolist()
        modes=[(True,cap)] if candidate[p,q] else []
        if len(common)>cap:
            modes.append((False,cap+1))
        for include_pair,count in modes:
            for number,vertices in enumerate(combinations(common,count)):
                if number>=per_pair:
                    break
                witness=dict(pair=[p,q],include_pair_edge=include_pair,common_vertices=list(vertices))
                clause=certified_clause(labels,graph,witness)
                cuts[clause]=witness
    return cuts,dict(excess=excess,defective_pairs=defective_pairs)


def root_check(k,labels,candidate):
    assert np.array_equal(candidate,candidate.T) and not np.any(np.diag(candidate))
    assert np.all(candidate.sum(axis=1)==k-2)
    for p,label in enumerate(labels):
        for r in range(k):
            observed=sum(int(candidate[p,q]) for q,other in enumerate(labels) if r in other)
            assert observed==2-int(r in label)-int((r^1) in label)


def run(output,k=14,seconds=60,low_prism_flag=False,resume=None,max_iterations=10000,solver_name='glucose4',initial_candidate=None):
    assert solver_name in ('glucose4','cpsat'), 'The native Minicard pilot exited without a verdict on this Windows build.'
    start=time.monotonic()
    labels,graph,edges,cards,clauses,selectors,cover=problem(k,low_prism_flag)
    known={}
    initial_positives=None
    if initial_candidate:
        seed=json.loads(Path(initial_candidate).read_text(encoding='utf-8'))
        array=np.array(seed['candidate'],dtype=np.int64)
        root_check(k,labels,array)
        initial_positives={i for i,(p,q) in enumerate(edges,1) if array[p,q]}
        initial_positives.add(selectors[seed['matching_case']])
        def truth(lit):
            return (lit in initial_positives) if lit>0 else (-lit not in initial_positives)
        assert all(sum(truth(lit) for lit in lits)<=bound for lits,bound in cards)
        assert all(any(truth(lit) for lit in clause) for clause in clauses)
    if resume:
        old=json.loads(Path(resume).read_text(encoding='utf-8'))
        assert old['root_count']==k and old['labels']==[list(p) for p in labels]
        for witness in old['universal_cuts']:
            clause=certified_clause(labels,graph,witness)
            known[clause]=witness
    report=dict(root_count=k,labels=labels,parameters=[1+k+len(labels),k,1,2],
                status='UNKNOWN',covers_all_graphs=True,fixed_local_seed=False,
                low_prism_flag=low_prism_flag,coverage=cover,
                variables=len(edges)+len(selectors),edge_variables=len(edges),
                product_variables=0,base_clauses=len(clauses),cardinality_constraints=len(cards),
                complete_global_decision=False,affordable_solve_proved=False,
                inherited_universal_cuts=len(known),iterations=[],num_search_workers=1,
                initial_candidate=initial_candidate,initial_candidate_only_a_soft_hint=True,
                termination_reason=None)
    output=Path(output)
    best=None
    if solver_name!='cpsat':
        pool=IDPool(start_from=len(edges)+len(selectors)+1)
        for lits,bound in cards:
            clauses.extend(CardEnc.atmost(lits=lits,bound=bound,vpool=pool,encoding=EncType.seqcounter).clauses)
        report.update(variables=pool.top,encoded_clauses=len(clauses))
    report['solver_name']=solver_name
    report['termination_reason']='BUILD_COMPLETE_SOLVE_NOT_FINISHED'
    output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    engine=(CardinalityCP(len(edges)+len(selectors),clauses) if solver_name=='cpsat'
            else Solver(name=solver_name,bootstrap_with=clauses,use_timer=True))
    with engine as solver:
        if solver_name=='cpsat':
            assert solver.supports_atmost()
            for lits,bound in cards:
                solver.add_atmost(lits,bound)
        for clause in known:
            solver.add_clause(list(clause))
        if initial_positives is not None:
            phases=[i if i in initial_positives else -i for i in range(1,len(edges)+len(selectors)+1)]
            solver.set_phases(phases)
        report['build_seconds']=time.monotonic()-start
        print(json.dumps({key:report[key] for key in ('variables','cardinality_constraints','product_variables','covers_all_graphs','build_seconds')}),flush=True)
        deadline=time.monotonic()+seconds
        for iteration in range(max_iterations):
            remaining=deadline-time.monotonic()
            if remaining<=0:
                report['termination_reason']='TIME_LIMIT'
                break
            supplied=(iteration==0 and initial_positives is not None and not known)
            if supplied:
                feasible=True
            else:
                solver.clear_interrupt()
                timer=Timer(remaining,solver.interrupt)
                timer.daemon=True
                timer.start()
                try:
                    feasible=solver.solve_limited(expect_interrupt=True)
                finally:
                    timer.cancel()
                    timer.join()
            if feasible is None:
                report['termination_reason']='TIME_LIMIT'
                break
            if not feasible:
                report.update(status='UNSAT',complete_global_decision=True,
                              termination_reason='ALL_NORMALIZED_GRAPHS_EXCLUDED',
                              certificate_scope='Solver verdict. Exported CNF and external UNSAT proof still required; the added pattern cuts are individually certified.')
                break
            positives=initial_positives if supplied else {v for v in solver.get_model() if v>0}
            candidate=np.zeros_like(graph)
            for var,(p,q) in enumerate(edges,1):
                candidate[p,q]=candidate[q,p]=int(var in positives)
            root_check(k,labels,candidate)
            cuts,statistics=separate(labels,graph,candidate)
            case=next(i for i,var in enumerate(selectors) if var in positives)
            entry=dict(iteration=iteration,elapsed_seconds=time.monotonic()-start,
                       matching_case=case,**statistics)
            report['iterations'].append(entry)
            if best is None or statistics['excess']<best:
                best=statistics['excess']
                report['best_candidate']=candidate.tolist()
                report['best_candidate_excess']=best
                print(json.dumps(dict(stage='BEST_CANDIDATE_NOT_AN_SRG' if best else 'EXACT_SRG',**entry)),flush=True)
            if not cuts:
                report.update(status='SAT',complete_global_decision=True,termination_reason='EXACT_SRG',
                              adjacency=reconstruct_and_check(k,labels,candidate),exact_all_pair_check=True)
                break
            new=0
            for clause,witness in cuts.items():
                # Every witness must be violated by the current candidate.
                assert all(-lit in positives for lit in clause)
                if clause not in known:
                    solver.add_clause(list(clause))
                    known[clause]=witness
                    new+=1
            assert new>0,'A repeated fully cut candidate is a solver/encoding error.'
            entry['added_universal_cuts']=new
            if iteration%10==0:
                report.update(universal_cuts=list(known.values()),universal_cut_count=len(known),
                              checkpoint_seconds=time.monotonic()-start,termination_reason='RUNNING')
                output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        else:
            report['termination_reason']='ITERATION_LIMIT'
        report['solver_stats']=solver.accum_stats()
    report.update(total_seconds=time.monotonic()-start,universal_cuts=list(known.values()),
                  universal_cut_count=len(known))
    output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:value for key,value in report.items() if key not in
                      ('labels','coverage','iterations','best_candidate','adjacency','universal_cuts')},ensure_ascii=False),flush=True)
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True)
    parser.add_argument('--roots',type=int,default=14)
    parser.add_argument('--seconds',type=float,default=60)
    parser.add_argument('--low-prism-flag',action='store_true')
    parser.add_argument('--resume')
    parser.add_argument('--max-iterations',type=int,default=10000)
    parser.add_argument('--solver',choices=['glucose4','cpsat'],default='glucose4')
    parser.add_argument('--initial-candidate')
    args=parser.parse_args()
    run(args.output,args.roots,args.seconds,args.low_prism_flag,args.resume,args.max_iterations,args.solver,args.initial_candidate)
