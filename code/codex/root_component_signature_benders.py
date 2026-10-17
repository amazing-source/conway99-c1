"""Learn necessary signature clauses from failed global H realizations.

The master is the C1/corner/signature model. The subproblem additionally
imposes eigenvectors, triangles, boundary profiles, C2 and minc>=4. Only H
selectors are assumed in the subproblem, never the master's proposed edges.
An UNSAT assumption core therefore forbids that partial signature assignment
for every edge completion. A satisfiable relaxation or UNKNOWN is not blocked.
Only an UNSAT master with these valid clauses excludes the fixed Gram.
"""

import argparse
import hashlib
import json
from pathlib import Path
import sys
import threading
import time

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import limit_research_process,atomic_json_write
from root_component_signature_joint import build
from root_component_signature_moments import gram_matrix
from ortools.sat.python import cp_model


def bounded_solve(model,budget):
    solver=cp_model.CpSolver();solver.parameters.num_search_workers=1
    solver.parameters.max_time_in_seconds=max(600,100*budget)
    solver.parameters.linearization_level=0
    solver.parameters.symmetry_level=0
    solver.parameters.cp_model_probing_level=0
    started=time.process_time();done=threading.Event()
    def interrupt():
        while not done.wait(.05):
            if time.process_time()-started>=budget:solver.stop_search();return
    timer=threading.Thread(target=interrupt,daemon=True);timer.start()
    try:status=solver.solve(model)
    finally:done.set();timer.join()
    return solver,status,{'status':solver.status_name(status),'cpu_seconds':time.process_time()-started,
                          'branches':solver.num_branches,'conflicts':solver.num_conflicts}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',type=Path)
    p.add_argument('--index',type=int,required=True)
    p.add_argument('--gram-index',type=int,required=True)
    p.add_argument('--seconds',type=float,default=120)
    p.add_argument('--master-seconds',type=float,default=10)
    p.add_argument('--sub-seconds',type=float,default=20)
    p.add_argument('--layer',type=int,default=1,choices=range(5))
    p.add_argument('--local-tables',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();resources=limit_research_process(2)
    cover=next(r for r in json.loads((args.directory/'root_component_gram_orbits20.json').read_text())['records'] if r['template_index']==args.index)
    values=cover['gram_anchor_values'][args.gram_index]
    matrix=gram_matrix(cover,values)
    template=json.loads((args.directory/'root_component_templates.json').read_text())['survivors'][args.index]
    tables=json.loads(args.local_tables.read_text())
    source_files=('root_component_signature_joint.py','root_component_short_vectors.py',
                  'root_component_upper_signatures.py','root_component_corner_tables.py',
                  'root_component_local_tables.py','root_rectangle_domains.py')
    encoding_hash=hashlib.sha256(b''.join(Path(__file__).with_name(name).read_bytes() for name in source_files)+args.local_tables.read_bytes()).hexdigest()
    options=dict(four_corners=True,local_tables=tables,short_vectors=True,normalize_component=True,upper_projector=True)
    master,_,master_info=build(template,matrix,**options)
    strong,_,strong_info=build(template,matrix,layer=args.layer,eigen=True,minc_lines=1,
                               line_profiles=1,profile_triples=True,exact_triangles=True,**options)
    def selectors(model):
        names={v.name:i for i,v in enumerate(model.proto.variables)}
        return {w:model.get_int_var_from_proto_index(names[f'signature_{w}'])
                for w in range(84) if f'signature_{w}' in names}
    ms,ss=selectors(master),selectors(strong)
    assert set(ms)==set(ss)==set(range(84))
    for w in ms:assert list(master.proto.variables[ms[w].index].domain)==list(strong.proto.variables[ss[w].index].domain)
    # The installed OR-Tools repeated-int wrapper silently mishandles [-1].
    # Copy domains to Python lists before inspecting their final endpoint.
    variable_rows=[w for w,v in ms.items()
                   if len(set(list(master.proto.variables[v.index].domain)))>1]
    assert bool(variable_rows)==(master_info['signature_flags']>84)
    assumptions={};literal_map={};forbidden=[];rounds=[]
    def learn(core):
        alternatives=[]
        for w,value in core:
            different=master.new_bool_var(f'different_{len(forbidden)}_{w}')
            master.add(ms[w]!=value).only_enforce_if(different)
            alternatives.append(different)
        master.add_bool_or(alternatives)
        forbidden.append(core)
    if args.output.exists():
        previous_record=json.loads(args.output.read_text())['records'][0]
        assert previous_record['template_index']==args.index
        previous=previous_record['cases'][0]
        assert previous['gram_index']==args.gram_index and previous['encoding_sources_sha256']==encoding_hash
        assert previous['gram_anchor_values']==values and previous['layer']==args.layer
        for core in previous['forbidden_signature_cores']:learn(core)
        rounds.extend(previous['rounds'])
    case={'gram_index':args.gram_index,'gram_anchor_values':values,'status':'UNKNOWN','layer':args.layer,
          'encoding_sources_sha256':encoding_hash,
          'forbidden_signature_cores':forbidden,'rounds':rounds,'master':master_info,'subproblem':strong_info}
    output={'scope':__doc__,'resources':resources,'records':[{'template_index':args.index,'complete_source_gram_count':cover['gram_count'],'cases':[case]}]}
    def save():atomic_json_write(args.output,output)
    save();started=time.process_time()
    while time.process_time()-started<args.seconds:
        sm,status,stats=bounded_solve(master,min(args.master_seconds,args.seconds-(time.process_time()-started)))
        row={'master':stats};rounds.append(row)
        if status==cp_model.INFEASIBLE:
            case.update(status='INFEASIBLE',reason='all_signature_fields_refuted_by_valid_cores');save();break
        if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):save();break
        field=[(w,sm.value(ms[w])) for w in variable_rows]
        strong.clear_assumptions()
        for w,value in field:
            key=(w,value)
            if key not in assumptions:
                flag=strong.new_bool_var(f'assume_h_{w}_{value}')
                strong.add(ss[w]==value).only_enforce_if(flag)
                assumptions[key]=flag;literal_map[flag.index]=key
            strong.add_assumption(assumptions[key])
        remaining=args.seconds-(time.process_time()-started)
        if remaining<=0:save();break
        su,status,substats=bounded_solve(strong,min(args.sub_seconds,remaining))
        row['subproblem']=substats;row['assumed_rows']=len(field)
        if status==cp_model.INFEASIBLE:
            core=[list(literal_map[i]) for i in su.sufficient_assumptions_for_infeasibility()]
            assert all(tuple(item) in field for item in core)
            learn(core);row['core_size']=len(core)
            if not core:case.update(status='INFEASIBLE',reason='subproblem_unconditionally_infeasible')
        else:
            row['unresolved_signature_field']=[list(x) for x in field]
            case['reason']='signature_field_has_feasible_relaxation' if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) else 'signature_field_not_decided'
        save();print({k:v for k,v in row.items() if k!='unresolved_signature_field'},flush=True)
        if status!=cp_model.INFEASIBLE or case['status']=='INFEASIBLE':break
    print({'status':case['status'],'cores':len(forbidden),'rounds':len(rounds)},flush=True)


if __name__=='__main__':main()
