"""Exact joint selection of all sixty outside profiles of a K3 block24.

The Boolean model contains profile choices, all residual known-pair
equalities, known-letter equalities, N/Z counts, and outside-pair C2
bounds. It contains no unknown outside-outside adjacency variables.
SAT means 24 complete rows, not a Conway graph. UNSAT proofs are saved
and checked by reverse unit propagation, ignoring proof deletions.
"""

import argparse
from collections import defaultdict,deque
import hashlib
from itertools import combinations
import json
from pathlib import Path
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process
from root_component_shared_k3_extend import OUTSIDE,frontier


def encode(data):
    from pysat.formula import CNF,IDPool
    from pysat.card import CardEnc,EncType
    domains=data['domains'];vpool=IDPool();cnf=CNF();features=defaultdict(list)
    variables=[];kinds=defaultdict(int)
    def equal(lits,target,kind):
        before=len(cnf.clauses)
        if target<0 or target>len(lits):cnf.append([])
        elif lits:
            cnf.extend(CardEnc.equals(lits=lits,bound=target,vpool=vpool,encoding=EncType.seqcounter).clauses)
        elif target:cnf.append([])
        kinds[kind]+=len(cnf.clauses)-before
    for qi,(q,domain) in enumerate(zip(OUTSIDE,domains)):
        row=[];roots={l//2 for l in q}
        region='N' if 3 in roots and roots&{4,5,6} else (
            'Z' if 0 in roots and roots&{3,4,5,6} else None)
        for pi,p in enumerate(domain):
            var=vpool.id(('profile',qi,pi));row.append(var)
            for i,u in enumerate(p):
                for v in p[i:]:features['pair',u,v].append(var)
                for l in q:features['letter',u,l].append(var)
                if region:features[region,u].append(var)
        variables.append(row);equal(row,1,'one_profile')
    for u in range(24):
        for v in range(u,24):equal(features['pair',u,v],data['residual_gram'][u][v],'known_pair')
        for l in range(14):equal(features['letter',u,l],data['letter_deficits'][u][l],'known_letter')
        equal(features['N',u],3 if u<12 else 1,'region')
        equal(features['Z',u],0 if u<8 else (4 if u<12 else 2),'region')
    masks=[[sum(1<<v for v in p) for p in d] for d in domains]
    for a,b in combinations(range(60),2):
        cap=2-len(set(OUTSIDE[a])&set(OUTSIDE[b]))
        for i,p in enumerate(masks[a]):
            for j,q in enumerate(masks[b]):
                if (p&q).bit_count()>cap:
                    cnf.append([-variables[a][i],-variables[b][j]]);kinds['outside_C2']+=1
    return cnf,variables,dict(kinds)


def unit_contradiction(clauses):
    """Explicit unit propagation for an empty native proof at bootstrap."""
    occurrences=defaultdict(list);remaining=[];sums=[];satisfied=[];queue=deque()
    for ci,raw in enumerate(clauses):
        clause=set(raw);tautology=any(-l in clause for l in clause)
        remaining.append(len(clause));sums.append(sum(clause));satisfied.append(tautology)
        if tautology:continue
        if not clause:return {'contradiction_clause':ci,'forced_literals':0}
        for l in clause:occurrences[l].append(ci)
        if len(clause)==1:queue.append((next(iter(clause)),ci))
    assignment={}
    while queue:
        l,reason=queue.popleft();var=abs(l)
        if var in assignment:
            if assignment[var]!=l:return {'contradiction_clause':reason,'forced_literals':len(assignment)}
            continue
        assignment[var]=l
        for ci in occurrences[l]:satisfied[ci]=True
        for ci in occurrences[-l]:
            if satisfied[ci]:continue
            remaining[ci]-=1;sums[ci]+=l
            if not remaining[ci]:return {'contradiction_clause':ci,'forced_literals':len(assignment)}
            if remaining[ci]==1:queue.append((sums[ci],ci))
    return None


def check_rup(cnf,proof):
    from pysat.solvers import Solver
    checked=0;empty=False
    with Solver(name='g3',bootstrap_with=cnf.clauses) as checker:
        if not proof:
            certificate=unit_contradiction(cnf.clauses)
            assert certificate is not None,'No proof and no bootstrap unit contradiction'
            return {'checked_additions':1,'empty_clause_verified':True,
                    'empty_input_proof':True,'unit_certificate':certificate}
        for line in proof:
            words=line.split()
            if not words or words[0]=='d':continue
            assert words[-1]=='0'
            clause=list(map(int,words[:-1]))
            ok,_=checker.propagate(assumptions=[-l for l in clause])
            assert not ok,('Not RUP',checked,line)
            consistent=checker.add_clause(clause,no_return=False);checked+=1
            if not consistent:
                return {'checked_additions':checked,'empty_clause_verified':True,
                        'terminal_root_conflict':True,'deletions_ignored':True}
            if not clause:empty=True
    assert empty
    return {'checked_additions':checked,'empty_clause_verified':empty,'deletions_ignored':True}


def finished_proof(solver):
    """Flush the native writer before reading its proof on Windows.

    The installed PySAT reader sees only complete C stdio buffers while
    the solver is alive. Python file flush and the native destructor do
    not flush that stream in this build; UCRT fflush does.
    """
    import ctypes
    runtime=ctypes.CDLL('ucrtbase' if sys.platform=='win32' else None)
    runtime.fflush.argtypes=[ctypes.c_void_p]
    runtime.fflush.restype=ctypes.c_int
    assert runtime.fflush(None)==0
    return solver.get_proof()


def select_profiles(data,conflicts=100000,solver_name='g3'):
    from pysat.solvers import Solver
    start=time.process_time();cnf,variables,kinds=encode(data)
    out={'variables':cnf.nv,'clauses':len(cnf.clauses),'clause_kinds':kinds,
         'solver':solver_name,'is_complete_graph':False}
    proof=None
    with Solver(name=solver_name,bootstrap_with=cnf.clauses,with_proof=True) as solver:
        solver.conf_budget(conflicts)
        answer=solver.solve_limited()
        out['solver_statistics']=solver.accum_stats()
        if answer is None:out['status']='UNKNOWN'
        elif answer:
            model=set(solver.get_model())
            selected=[next(i for i,v in enumerate(row) if v in model) for row in variables]
            out.update(status='SAT_24_COMPLETE_ROWS',selected_profile_indices=selected,
                       outside_profiles=[data['domains'][q][i] for q,i in enumerate(selected)])
        else:
            # Keeping deleted clauses is sound, so the compact RUP
            # certificate needs only additions.
            proof=[line for line in finished_proof(solver) if not line.startswith('d ')]
            out.update(status='EXCLUDED_PROFILE_SELECTION_UNSAT',proof_check=check_rup(cnf,proof))
    out['cpu_seconds']=time.process_time()-start
    return out,cnf,proof


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pilot',type=Path,required=True)
    parser.add_argument('--output-prefix',type=Path,required=True)
    parser.add_argument('--conflicts',type=int,default=100000)
    parser.add_argument('--solver',choices=('g3','cadical195'),default='g3')
    args=parser.parse_args();resources=limit_research_process(1);start=time.process_time()
    output=args.output_prefix.with_suffix('.json');assert not output.exists()
    source=json.loads(args.pilot.read_text(encoding='utf8'));record=source['cases'][-1]
    witness=record['result']['witness'];data=frontier(witness['rows'],True)
    assert data['status']=='PASSES_PROFILE_PROPAGATION'
    result,cnf,proof=select_profiles(data,args.conflicts,args.solver)
    cnf_path=args.output_prefix.with_suffix('.cnf');cnf.to_file(str(cnf_path))
    out={'scope':__doc__,'source':str(args.pilot),'boundary_index':record['boundary_index'],
         **result,
         'cnf_sha256':hashlib.sha256(cnf_path.read_bytes()).hexdigest(),
         'resources':resources,'is_complete_graph':False}
    if proof is not None:
        proof_path=args.output_prefix.with_suffix('.drup')
        proof_path.write_text('\n'.join(proof)+'\n',encoding='ascii')
        out['proof_sha256']=hashlib.sha256(proof_path.read_bytes()).hexdigest()
    out['cpu_seconds']=time.process_time()-start;atomic_json_write(output,out,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k not in ('outside_profiles','selected_profile_indices','scope')}))


if __name__=='__main__':main()
