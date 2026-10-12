"""Learn exact, reusable coexistence cuts, rather than reject whole witnesses.

Single-vertex Farkas certificates become conditional linear covering cuts.
Multi-vertex certificates are symmetrized within identical cells and become
one polynomial inequality in the cell populations. Product variables are
created only for positive terms of learned cuts, and are reused.
"""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction
from math import lcm,gcd
from functools import reduce
from itertools import combinations
import argparse
import hashlib
import json
import time

from ortools.sat.python import cp_model
from coclique_defect_gluing import gluing_data
from coclique_defect_star import population,targets,compatible
from coclique_completion_certificate import certificate,equations,verify


class Master:
    def __init__(self,core,order=99,coclique_size=21):
        self.core=core;self.data=gluing_data(core,order,coclique_size)
        self.rows=self.data['rows'];self.n=len(core['charges']);self.lookup={r:i for i,r in enumerate(self.rows)}
        self.degree=core['parameters']['degree'];self.cdegree=4 if self.degree==14 else 2
        self.model=cp_model.CpModel();self.x,self.c=population(self.model,self.data,core)
        self.upper=[]
        for r in self.rows:
            ids=[i for i in range(self.n) if r>>i&1]
            u=min([order-self.n]+[self.data['outside_degrees'][i] for i in ids]+[self.data['residual'][i,j] for i,j in combinations(ids,2)])
            self.upper.append(min(u,1) if len(ids)>=3 else u)
        self.f=[self.model.NewIntVar(0,u,f'free{t}') for t,u in enumerate(self.upper)]
        for t in range(len(self.rows)):self.model.Add(self.f[t]+self.c[t]==self.x[t])
        self.p=[v for t in range(len(self.rows)) for v in (self.c[t],self.f[t])]
        self.present=[]
        for a,v in enumerate(self.p):
            used=self.model.NewBoolVar(f'present{a}');self.model.Add(v>=used);self.model.Add(v<=self.upper[a//2]*used)
            self.present.append(used)
        self.h=[targets(self.data,r) for r in self.rows]
        self.allowed=[[u for u,s in enumerate(self.rows) if compatible(self.data,r,s)] for r in self.rows]
        self.products={};self.cuts=[]
        # Seed with coordinate capacity cuts; learning will couple coordinates.
        for t,r in enumerate(self.rows):
            for colour in range(2):
                population_vars=self.f if colour==0 else self.x
                a=2*t+colour;self_candidate=int(t in self.allowed[t] and colour==1)
                self.model.Add(sum(population_vars[u] for u in self.allowed[t])>=self.degree-r.bit_count()+self_candidate).OnlyEnforceIf(self.present[a])
                for i,need in enumerate(self.h[t]):
                    if need:
                        self.model.Add(sum(population_vars[u] for u in self.allowed[t] if self.rows[u]>>i&1)>=need+self_candidate*int(r>>i&1)).OnlyEnforceIf(self.present[a])
                if colour==1:
                    self.model.Add(sum(self.c[u] for u in self.allowed[t])>=self.cdegree).OnlyEnforceIf(self.present[a])

    def witness(self,solver):
        return dict(selected_rows=[dict(vertices=[i for i in range(self.n) if r>>i&1],count=solver.Value(self.x[t]),coclique_count=solver.Value(self.c[t]))
                                  for t,r in enumerate(self.rows) if solver.Value(self.x[t])])

    def extract_weights(self,population,proof):
        eq,edges,rows,c=equations(self.core,population,prune_incompatible=proof.get('prune_incompatible',False))
        yy=[0]*len(eq)
        for item in proof['coefficients']:
            assert item['reason']==eq[item['equation']]['reason']
            yy[item['equation']]=item['coefficient']
        assert verify(eq,edges,yy)['valid']
        per_vertex=defaultdict(lambda:[0]*(self.n+2)) # degree, C degree, core coordinates
        for item in proof['coefficients']:
            reason=item['reason'];v=reason[1]
            coord=0 if reason[0]=='degree' else 1 if reason[0]=='coclique_degree' else 2+reason[2]
            per_vertex[v][coord]+=item['coefficient']
        return per_vertex,rows,c

    def learn(self,population,proof):
        weights,vertex_rows,colours=self.extract_weights(population,proof)
        if len(weights)==1:
            v,w=next(iter(weights.items()));r=sum(1<<i for i in vertex_rows[v]);t=self.lookup[r]
            colour=0 if colours[v] else 1;a=2*t+colour
            lhs=w[0]*(self.degree-r.bit_count())+w[1]*(self.cdegree if colour==1 else 0)+sum(w[2+i]*h for i,h in enumerate(self.h[t]))
            rhs_terms=[];rhs_observed=0;counts={tuple(x['vertices']):x for x in population['selected_rows']}
            for u in self.allowed[t]:
                row=self.rows[u]
                for col in range(2):
                    if colour==0 and col==0:continue
                    coefficient=w[0]+(w[1] if col==0 else 0)+sum(w[2+i] for i in range(self.n) if row>>i&1)
                    if coefficient<=0:continue
                    rhs_terms.append((2*u+col,coefficient))
                    observed=counts.get(tuple(i for i in range(self.n) if row>>i&1),dict(count=0,coclique_count=0))
                    value=observed['coclique_count'] if col==0 else observed['count']-observed['coclique_count']
                    rhs_observed+=coefficient*value
                    if a==2*u+col:lhs+=coefficient
            assert lhs>rhs_observed,(lhs,rhs_observed)
            self.model.Add(sum(k*self.p[b] for b,k in rhs_terms)>=lhs).OnlyEnforceIf(self.present[a])
            cut=dict(kind='conditional_cover',root=sorted(vertex_rows[v]),in_coclique=colours[v],
                     weights=w,left=lhs,observed_right=rhs_observed,positive_terms=len(rhs_terms),
                     terms=[dict(cell=b,coefficient=k) for b,k in rhs_terms])
        else:
            # Averaging over permutations within each identical cell cannot
            # decrease the Farkas gap, by convexity of max(0,edge weight).
            cell_counts=defaultdict(int);totals=defaultdict(lambda:[0]*(self.n+2))
            for v,row in enumerate(vertex_rows):
                a=2*self.lookup[sum(1<<i for i in row)]+int(not colours[v]);cell_counts[a]+=1
                if v in weights:
                    for i,value in enumerate(weights[v]):totals[a][i]+=value
            denominator=lcm(*(cell_counts[a] for a in totals))
            ww={a:[v*(denominator//cell_counts[a]) for v in values] for a,values in totals.items()}
            divisor=reduce(gcd,(abs(v) for values in ww.values() for v in values if v),0)
            ww={a:[v//divisor for v in values] for a,values in ww.items()}
            zero=[0]*(self.n+2);left=[];right=[];observed_left=observed_right=0
            for a,w in ww.items():
                t=a//2
                value=w[0]*(self.degree-self.rows[t].bit_count())+w[1]*(self.cdegree if a%2 else 0)+sum(w[2+i]*h for i,h in enumerate(self.h[t]))
                if value:left.append(value*self.p[a]);observed_left+=value*cell_counts.get(a,0)
            positive_terms=0
            for a in range(len(self.p)):
                for b in range(a,len(self.p)):
                    if a not in ww and b not in ww:continue
                    if not(a%2 or b%2) or b//2 not in self.allowed[a//2]:continue
                    wa,wb=ww.get(a,zero),ww.get(b,zero);ra,rb=self.rows[a//2],self.rows[b//2]
                    value=wa[0]+wb[0]+(wa[1] if b%2==0 else 0)+(wb[1] if a%2==0 else 0)
                    value+=sum(wa[2+i] for i in range(self.n) if rb>>i&1)+sum(wb[2+i] for i in range(self.n) if ra>>i&1)
                    if value<=0:continue
                    ua,ub=self.upper[a//2],self.upper[b//2]
                    if a==b and ua<2:continue
                    if ua==0 or ub==0:continue
                    if (a,b) not in self.products:
                        if a==b:
                            square=self.model.NewIntVar(0,ua*ua,f'square{a}')
                            self.model.AddMultiplicationEquality(square,[self.p[a],self.p[a]])
                            product=self.model.NewIntVar(0,ua*(ua-1)//2,f'pairs{a}')
                            self.model.Add(2*product==square-self.p[a])
                        else:
                            product=self.model.NewIntVar(0,ua*ub,f'product{a}_{b}')
                            self.model.AddMultiplicationEquality(product,[self.p[a],self.p[b]])
                        self.products[a,b]=product
                    right.append(value*self.products[a,b]);positive_terms+=1
                    pa,pb=cell_counts.get(a,0),cell_counts.get(b,0)
                    observed_right+=value*(pa*(pa-1)//2 if a==b else pa*pb)
            assert observed_left>observed_right,(observed_left,observed_right)
            self.model.Add(sum(left)<=sum(right))
            cut=dict(kind='shared_edge_polynomial',weights={str(a):w for a,w in ww.items()},
                     observed_left=observed_left,observed_right=observed_right,positive_terms=positive_terms,
                     total_product_variables=len(self.products))
        self.cuts.append(cut);return cut


def local_choices(core,population):
    eq,edges,rows,c=equations(core,population,prune_incompatible=True)
    results=[]
    for vertex in range(len(rows)):
        constraints=[e for e in eq if e['reason'][1]==vertex]
        variables=sorted({v for e in constraints for v in e['variables']})
        model=cp_model.CpModel();x={v:model.NewBoolVar(f'x{v}') for v in variables}
        for e in constraints:model.Add(sum(x[v] for v in e['variables'])==e['rhs'])
        solver=cp_model.CpSolver();solver.parameters.num_search_workers=1;solver.parameters.max_time_in_seconds=2
        status=solver.Solve(model)
        item=dict(vertex=vertex,status=solver.StatusName(status))
        if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            chosen=[v for v in variables if solver.Value(x[v])]
            assert all(sum(v in chosen for v in e['variables'])==e['rhs'] for e in constraints)
            item['neighbours']=[(edges[v][1] if edges[v][0]==vertex else edges[v][0]) for v in chosen]
        results.append(item)
    return dict(feasible=sum(r['status'] in ('OPTIMAL','FEASIBLE') for r in results),total=len(rows),
                scope='Each vertex separately chooses all linear degree/common quotas; reciprocity not required',results=results)


def run(core_path,folder,*,iterations=20,seconds=20,workers=4,prune=False,resume_from=()):
    folder.mkdir(parents=True,exist_ok=False)
    raw=core_path.read_bytes();core=json.loads(raw);master=Master(core)
    started=time.monotonic();trace=[];inherited=[]
    for previous in resume_from:
        state=json.loads((previous/'result.json').read_text())
        assert state['core_sha256']==hashlib.sha256(raw).hexdigest()
        for proof_path in sorted(previous.glob('certificate_*.json')):
            proof=json.loads(proof_path.read_text())
            if proof['status']!='EXACT_CONTRADICTION':continue
            witness=json.loads(proof_path.with_name(proof_path.name.replace('certificate_','population_')).read_text())
            master.learn(witness,proof);inherited.append(str(proof_path))
    print(json.dumps(dict(inherited_cuts=len(inherited),products=len(master.products))),flush=True)
    with (folder/'trace.jsonl').open('w',encoding='utf8') as log:
        for step in range(iterations):
            solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=seconds;solver.parameters.num_search_workers=workers
            solver.parameters.log_search_progress=True;solver.parameters.log_to_stdout=False
            with (folder/f'solver_{step:03d}.log').open('w',encoding='utf8') as solver_log:
                solve_start=time.monotonic()
                def log_line(line):solver_log.write(f'{time.monotonic()-solve_start:.3f} {line}\n');solver_log.flush()
                solver.log_callback=log_line
                status=solver.Solve(master.model)
            entry=dict(step=step,status=solver.StatusName(status),seconds=solver.WallTime(),cuts=len(master.cuts),products=len(master.products),
                       branches=solver.NumBranches(),conflicts=solver.NumConflicts())
            if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):
                trace.append(entry);log.write(json.dumps(entry)+'\n');log.flush();print(json.dumps(entry),flush=True);break
            population=master.witness(solver)
            (folder/f'population_{step:03d}.json').write_text(json.dumps(population,indent=2)+'\n')
            local=local_choices(core,population)
            (folder/f'local_choices_{step:03d}.json').write_text(json.dumps(local,indent=2)+'\n')
            entry['individually_feasible_vertices']=local['feasible']
            proof=certificate(core,population,seconds,sparse=True,prune_incompatible=prune)
            (folder/f'certificate_{step:03d}.json').write_text(json.dumps(proof,indent=2)+'\n')
            entry['oracle']=proof['status'];entry['oracle_seconds']=proof['seconds']
            if proof['status']=='EXACT_CONTRADICTION':
                cut=master.learn(population,proof)
                (folder/f'cut_{step:03d}.json').write_text(json.dumps(cut,indent=2)+'\n')
                entry.update(kind=cut['kind'],positive_terms=cut['positive_terms'])
                master.model.ClearHints()
                for variables in (master.x,master.c):
                    for v in variables:master.model.AddHint(v,solver.Value(v))
            trace.append(entry);log.write(json.dumps(entry)+'\n');log.flush();print(json.dumps(entry),flush=True)
            if proof['status']!='EXACT_CONTRADICTION':break
    report=dict(core=str(core_path),core_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                seconds=time.monotonic()-started,iterations=len(trace),cuts=len(master.cuts),pruned_oracle=prune,trace=trace,
                inherited=inherited,parameters=dict(iterations=iterations,seconds_per_master=seconds,workers=workers),
                scope='Cuts valid for all common populations of this fixed support; no global C1 claim')
    (folder/'result.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('core',type=Path);ap.add_argument('folder',type=Path)
    ap.add_argument('--iterations',type=int,default=20);ap.add_argument('--seconds',type=float,default=20);ap.add_argument('--workers',type=int,default=4);ap.add_argument('--prune',action='store_true')
    ap.add_argument('--resume-from',type=Path,action='append',default=[])
    args=ap.parse_args();run(args.core,args.folder,iterations=args.iterations,seconds=args.seconds,workers=args.workers,prune=args.prune,resume_from=args.resume_from)
