"""Export fixed-Gram binary projection obstructions as CNF and checked DRAT.

The input is the same necessary C1/component/fixed-Gram system used by
the weighted projection, including its sound prior binary propagation.
Each linear row has a common positive coefficient and is encoded as an
exact cardinality or at-most constraint. The only additional restriction
is the explicitly selected root's prism budget. Native drat-trim verifies
UNSAT of the generated CNF, not the mathematical reduction to that CNF.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_prism_lp_certificate import matrix_of,system
from root_component_propagation import PAIRS
from root_component_resources import limit_research_process,atomic_json_write
from root_component_low_budget_transport import digest


def encode(template,matrix,budget):
    from pysat.card import CardEnc,EncType
    from pysat.formula import CNF
    fixed,rows,objective,constant=system(template,matrix)
    rows.append({'label':['root_prism_budget',budget],'terms':objective,
                 'rhs':budget-constant,'equality':False})
    cnf=CNF();top=len(PAIRS);mapping=[]
    for ri,row in enumerate(rows):
        coefficients=set(row['terms'].values())
        assert not coefficients or len(coefficients)==1 and min(coefficients)>0
        scale=next(iter(coefficients),1);rhs=row['rhs']
        literals=[i+1 for i in sorted(row['terms'])]
        first=len(cnf.clauses)
        if row['equality'] and rhs%scale:
            cnf.append([])
        else:
            bound=rhs//scale;n=len(literals)
            if bound<0 or row['equality'] and bound>n:
                cnf.append([])
            elif not n:
                assert bound>=0
            elif row['equality'] or bound<n:
                builder=CardEnc.equals if row['equality'] else CardEnc.atmost
                encoding=builder(lits=literals,bound=bound,top_id=top,encoding=EncType.seqcounter)
                cnf.extend(encoding.clauses);top=max(top,encoding.nv)
        mapping.append({'row':ri,'reason':row['label'],'equality':row['equality'],
                        'scale':scale,'rhs':rhs,'clause_start':first,'clause_stop':len(cnf.clauses)})
    cnf.nv=top
    return cnf,{'fixed_edge_count':len(fixed),'rows':len(rows),'prism_constant':constant,
                'free_prism_edges':len(objective),'row_clause_mapping':mapping,
                'cardinality_encoding':'pysat.CardEnc.seqcounter'}


def sha256(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def solve_checked(cnf,prefix,conflicts,checker,native_solver):
    cnf_file=prefix.with_suffix('.cnf');proof_file=prefix.with_suffix('.drat')
    check_file=prefix.with_suffix('.check.log')
    assert not any(p.exists() for p in (cnf_file,proof_file,check_file))
    cnf.to_file(str(cnf_file));started=time.monotonic()
    solver_log=prefix.with_suffix('.solver.log')
    command=[str(native_solver.resolve()),'-q','--binary=false','-c',str(conflicts),str(cnf_file),str(proof_file)]
    with solver_log.open('w',encoding='utf-8') as stream:
        process=subprocess.Popen(command,stdout=stream,stderr=subprocess.STDOUT)
        code=process.wait()
    cpu_seconds=None
    if sys.platform=='win32':
        import ctypes
        from ctypes import wintypes
        creation,ending,kernel,user=(wintypes.FILETIME() for _ in range(4))
        ok=ctypes.windll.kernel32.GetProcessTimes(wintypes.HANDLE(int(process._handle)),
            ctypes.byref(creation),ctypes.byref(ending),ctypes.byref(kernel),ctypes.byref(user))
        if ok:cpu_seconds=sum((t.dwHighDateTime<<32)|t.dwLowDateTime for t in (kernel,user))/10000000
    result={'status':'UNSAT' if code==20 else 'SAT_RELAXATION' if code==10 else 'UNKNOWN',
            'solver_cpu_seconds':cpu_seconds,'solver_wall_seconds':time.monotonic()-started,
            'solver_exit_code':code,'solver':str(native_solver),'solver_sha256':sha256(native_solver),
            'solver_log':str(solver_log),'variables':cnf.nv,'clauses':len(cnf.clauses),
            'cnf':str(cnf_file),'cnf_sha256':sha256(cnf_file),'checked_drat':False}
    if code==20:
        assert 's UNSATISFIABLE' in solver_log.read_text()
        command=[str(checker.resolve()),str(cnf_file),str(proof_file),'-t','60']
        completed=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                                 text=True,encoding='utf-8',errors='replace',check=False)
        check_file.write_text(completed.stdout,encoding='utf-8')
        result.update(proof=str(proof_file),proof_sha256=sha256(proof_file),
                      checker=str(checker),checker_sha256=sha256(checker),
                      checker_exit_code=completed.returncode,checker_log=str(check_file),
                      checked_drat=completed.returncode==0 and 's VERIFIED' in completed.stdout)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',type=Path);p.add_argument('--gram-cover',type=Path,required=True)
    p.add_argument('--projection-report',type=Path,required=True);p.add_argument('--gram-indices',type=int,nargs='+')
    p.add_argument('--conflicts',type=int,default=100000)
    p.add_argument('--checker',type=Path,default=Path('tools/win64/drat-trim.exe'))
    p.add_argument('--solver',type=Path,default=Path('tools/win64/cadical.exe'))
    p.add_argument('--output-directory',type=Path,required=True);a=p.parse_args()
    resources=limit_research_process(1)
    a.output_directory.mkdir(parents=True,exist_ok=False)
    report=json.loads(a.projection_report.read_text())
    assert report['source_gram_cover_sha256_lf']==digest(a.gram_cover)
    assert report['root_order']=='weighted_prisms_grids'
    index=report['template_index'];source=a.directory/'root_component_templates.json'
    template=json.loads(source.read_text())['survivors'][index]
    cover=next(r for r in json.loads(a.gram_cover.read_text())['records'] if r['template_index']==index)
    positions={gi:i for i,gi in enumerate(cover['source_gram_indices'])}
    selected=a.gram_indices or report['excluded_gram_indices']
    assert set(selected)<=set(report['excluded_gram_indices'])
    budget=report['root_choice']['root_prism_budget']
    result={'scope':__doc__,'resources':resources,'template_index':index,
            'root_order':'weighted_prisms_grids','root_prism_budget':budget,
            'source_gram_cover':str(a.gram_cover),'source_gram_cover_sha256_lf':digest(a.gram_cover),
            'templates_sha256_lf':digest(source),'required_gram_indices':selected,
            'usable_in_arbitrary_low_budget_root_frontier':False,'cases':[]}
    for gi in selected:
        values=cover['gram_anchor_values'][positions[gi]]
        cnf,encoding=encode(template,matrix_of(cover,values),budget)
        prefix=a.output_directory/f'gram_{gi}'
        atomic_json_write(prefix.with_suffix('.encoding.json'),encoding)
        case=solve_checked(cnf,prefix,a.conflicts,a.checker,a.solver)
        case.update(gram_index=gi,gram_anchor_values=values)
        result['cases'].append(case);atomic_json_write(a.output_directory/'summary.json',result)
        print(json.dumps({k:case[k] for k in ('gram_index','status','checked_drat','solver_cpu_seconds','variables','clauses')}),flush=True)


if __name__=='__main__':main()
