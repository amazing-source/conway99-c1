"""Lift weighted capacity certificates to freely varying 59/60-vertex borders.

Unlike population cuts on one fixed positive support, every condition here
is expressed in adjacency, common-neighbour and multiplicity variables of
the border itself. No coclique colours of residual copies are assumed.
"""
from pathlib import Path
from itertools import combinations
import argparse
import hashlib
import json
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from ortools.sat.python import cp_model
from coclique_two_exception_cycles import build, verify_witness


def border_data(w):
    n=w['vertices'];adj=[set() for _ in range(n)]
    for u,v in w['edges']:adj[u].add(v);adj[v].add(u)
    m={tuple(item['vertices']):item['count'] for item in w['remaining_population'] if len(item['vertices'])==2}
    d={u:14-len(adj[u]) for u in range(18,n)}
    r={(u,i):2-int(i in adj[u])-len(adj[u]&adj[i]) for u in range(18,n) for i in range(4,16)}
    allowed={(u,row):d[u]>0 and all(r[u,i]>0 for i in row)
             and sum((int(row[0] in adj[u]),int(row[1] in adj[u]),int(row[1] in adj[row[0]])))<=1
             for u in range(18,n) for row in m}
    sat={(u,v) for u,v in combinations(range(18,n),2) if len(adj[u]&adj[v])==2-int(v in adj[u])}
    return n,adj,m,d,r,allowed,sat


def evaluate(w,cut):
    if cut.get('kind')=='integer_residual_square':
        from coclique_residual_squares import evaluate as square_evaluate
        return square_evaluate(w,cut)
    n,adj,m,d,r,allowed,sat=border_data(w)
    group=cut['group']; coefficients=cut['coefficients']
    if any(u>=n for u in group):return dict(applies=False)
    if any(tuple(sorted(e)) not in sat for e in combinations(group,2)):
        return dict(applies=False)
    left=sum(c[0]*d[u]+sum(c[i-3]*r[u,i] for i in range(4,16)) for u,c in zip(group,coefficients))
    bound=0; terms=[]
    for row,mult in m.items():
        values=[c[0]+sum(c[i-3] for i in row) if allowed[u,row] else 0 for u,c in zip(group,coefficients)]
        capacity=sum(sorted([max(0,x) for x in values],reverse=True)[:mult]) if cut.get('simple_factors') else mult*max(0,*values)
        bound+=capacity
        if capacity:terms.append(dict(type=row,multiplicity=mult,total_capacity=capacity))
    return dict(applies=True,left=left,upper=bound,gap=left-bound,violated=left>bound,positive_terms=terms)


def separate_group(w,group,data,seconds=2,simple=False):
    n,adj,m,d,r,allowed,sat=data
    count=len(group)*13; rows=list(m); rr=[];cc=[];vv=[];bounds=[]
    # y_u=(degree price, twelve L prices). t_T bounds the largest
    # admissible score for any member of the saturated clique.
    rownum=0
    for k,row in enumerate(rows):
        eligible=[offset for offset,u in enumerate(group) if allowed[u,row]]
        subsets=[c for size in range(1,min(m[row] if simple else 1,len(eligible))+1) for c in combinations(eligible,size)]
        for subset in subsets:
            ids=[j for offset in subset for j in [offset*13]+[offset*13+i-3 for i in row]]
            for j in ids:
                rr.extend([rownum,rownum]);cc.extend([j,count+j]);vv.extend([1.,-1.])
            rr.append(rownum);cc.append(2*count+k);vv.append(-1.)
            bounds.append(0.);rownum+=1
    target=np.array([value for u in group for value in [d[u]]+[r[u,i] for i in range(4,16)]],dtype=float)
    for j,value in enumerate(target):
        if value:
            rr.extend([rownum,rownum]);cc.extend([j,count+j]);vv.extend([-value,value])
    for k,row in enumerate(rows):
        rr.append(rownum);cc.append(2*count+k);vv.append(float(1 if simple else m[row]))
    bounds.append(-1.)
    A=coo_matrix((vv,(rr,cc)),shape=(rownum+1,2*count+len(rows))).tocsr()
    lp=linprog(np.r_[np.ones(2*count),np.zeros(len(rows))],A_ub=A,b_ub=np.array(bounds),bounds=(0,None),
               method='highs',options={'time_limit':seconds})
    if lp.x is None:return None
    raw=lp.x[:count]-lp.x[count:2*count]
    for scale in (1,2,3,4,6,8,12,24,48,96):
        coefficients=[[round(scale*float(x)) for x in raw[i*13:(i+1)*13]] for i in range(len(group))]
        cut=dict(group=list(group),coefficients=coefficients,
                 simple_factors=simple,
                 law='Weighted capacity of simultaneous residual degree factors on a saturated clique')
        value=evaluate(w,cut)
        if value['violated']:
            cut['separation']=value;return cut
    return None


def discover(w,max_group=3,seconds=2,simple=False):
    data=border_data(w);n,adj,m,d,r,allowed,sat=data
    active=[u for u in range(18,n) if d[u] or any(r[u,i] for i in range(4,16))]
    attempted=0;start=time.monotonic()
    for size in range(1,max_group+1):
        for group in combinations(active,size):
            if any(tuple(sorted(e)) not in sat for e in combinations(group,2)):continue
            attempted+=1;cut=separate_group(w,group,data,seconds,simple)
            if cut:
                cut['search']=dict(groups=attempted,seconds=time.monotonic()-start)
                return cut
    return dict(status='NO_CERTIFICATE',groups=attempted,max_group=max_group,seconds=time.monotonic()-start)


class Master:
    def __init__(self,partition,root_h,factors=False,all_pairs=False,simple=False):
        self.ctx={};self.partition=partition;self.root_h=root_h
        self.all_pairs=all_pairs
        self.simple=simple
        self.factors={}
        if factors:
            from coclique_pair_factors import factor_model
            self.model,self.variables,self.fixed,self.colours,self.populations,self.factors=factor_model(
                partition,root_h,packing=all_pairs,triangle_capacity=True,context=self.ctx,simple=simple)
        else:
            self.model,self.variables,self.fixed,self.colours,self.populations=build(
                partition,root_h=root_h,population=True,hcomplete=True,context=self.ctx)
        self.m={row:x for row,x,c in self.populations if len(row)==2}
        self.cache={};self.installed=[]

    def edge(self,u,v):return self.ctx['edge'](u,v)
    def residue(self,u,i):return 2-self.edge(u,i)-self.ctx['common'][tuple(sorted((u,i)))]

    def predicate(self,key,expr,threshold):
        if key not in self.cache:
            flag=self.model.NewBoolVar('_'.join(map(str,key)))
            self.model.Add(expr>=threshold).OnlyEnforceIf(flag)
            self.model.Add(expr<threshold).OnlyEnforceIf(flag.Not())
            self.cache[key]=flag
        return self.cache[key]

    def allowed(self,u,row):
        key=('allowed',u,*row)
        if key not in self.cache:
            flags=[self.predicate(('free',u),14-self.ctx['degree'][u],1)]
            flags.extend(self.predicate(('rpos',u,i),self.residue(u,i),1) for i in row)
            crowded=self.predicate(('crowded',u,*row),self.edge(u,row[0])+self.edge(u,row[1])+self.edge(*row),2)
            flags.append(crowded.Not())
            flag=self.model.NewBoolVar('_'.join(map(str,key)))
            self.model.AddBoolAnd(flags).OnlyEnforceIf(flag)
            self.model.AddBoolOr([f.Not() for f in flags]).OnlyEnforceIf(flag.Not())
            self.cache[key]=flag
        return self.cache[key]

    def install(self,cut):
        if cut.get('kind')=='integer_residual_square':
            from coclique_residual_squares import install
            return install(self,cut)
        group=cut['group'];coef=cut['coefficients'];n=self.ctx['n']
        if any(u>=n for u in group):return False
        conditions=[]
        for u,v in combinations(group,2):
            a,b=sorted((u,v))
            conditions.append(self.predicate(('sat',a,b),self.ctx['common'][a,b]+self.edge(a,b),2))
        left=sum(c[0]*(14-self.ctx['degree'][u])+sum(c[i-3]*self.residue(u,i) for i in range(4,16))
                 for u,c in zip(group,coef))
        rhs=[]
        for row,m in self.m.items():
            scores=[];maximum=0
            for u,c in zip(group,coef):
                score=c[0]+sum(c[i-3] for i in row)
                if score<=0:continue
                scores.append(score*self.allowed(u,row));maximum=max(maximum,score)
            if not scores:continue
            cap=self.model.NewIntVar(0,maximum,f'cap_{len(self.installed)}_{row}')
            self.model.AddMaxEquality(cap,[0]+scores)
            term=self.model.NewIntVar(0,2*maximum,f'bound_{len(self.installed)}_{row}')
            if cut.get('simple_factors'):
                cap2=self.model.NewIntVar(0,2*maximum,f'cap2_{len(self.installed)}_{row}')
                self.model.AddMaxEquality(cap2,[0]+scores+[a+b for a,b in combinations(scores,2)])
                present=self.predicate(('multiplicity_positive',*row),m,1)
                repeated=self.predicate(('multiplicity_two',*row),m,2)
                self.model.Add(term==0).OnlyEnforceIf(present.Not())
                self.model.Add(term==cap).OnlyEnforceIf([present,repeated.Not()])
                self.model.Add(term==cap2).OnlyEnforceIf(repeated)
            else:self.model.AddMultiplicationEquality(term,[m,cap])
            rhs.append(term)
        self.model.Add(left<=sum(rhs)).OnlyEnforceIf(conditions)
        self.installed.append(cut)
        return True

    def solve(self,output,seconds=90,workers=2,no_lp=False):
        solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=seconds
        solver.parameters.num_search_workers=workers;solver.parameters.log_search_progress=True
        solver.parameters.log_to_stdout=False
        if no_lp:solver.parameters.subsolvers.append('no_lp')
        with output.with_suffix('.log').open('w') as log:
            solver.log_callback=lambda s:(log.write(s+'\n'),log.flush())
            status=solver.Solve(self.model)
        report=dict(partition=self.partition,root_h=self.root_h,vertices=self.ctx['n'],hcomplete=True,population=True,triangle=False,
                    scope='All normalized (0,2) cores and borders for this partition and epsilon',
                    relaxation='Variable border with lifted capacity cuts, not a full SRG',
                    status=solver.StatusName(status),seconds=solver.WallTime(),cuts=len(self.installed),
                    branches=solver.NumBranches(),conflicts=solver.NumConflicts(),workers=workers,limit_seconds=seconds,
                    local_integer_factors=bool(self.factors),
                    factor_packing=self.all_pairs,triangle_capacity=bool(self.factors),simple_factors=self.simple,
                    model_stats=self.model.ModelStats(),response_stats=solver.ResponseStats())
        if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            report['edges']=sorted(self.fixed|{e for e,v in self.variables.items() if solver.Value(v)})
            report['coclique']=[u for u,v in self.colours.items() if solver.Value(v)]
            report['remaining_population']=[dict(vertices=row,count=solver.Value(x),coclique_count=solver.Value(c))
                                           for row,x,c in self.populations if solver.Value(x)]
            verify_witness(report)
            if self.factors:
                from coclique_pair_factors import verify
                report['factors']=[dict(vertex=u,type=row,count=solver.Value(y)) for (u,row),y in self.factors.items() if solver.Value(y)]
                report.update(factor_packing=self.all_pairs,triangle_capacity=True,simple_factors=self.simple)
                verify(report)
            assert all(not evaluate(report,c).get('violated',False) for c in self.installed)
            report['verified']=True
        output.write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({k:v for k,v in report.items() if k not in ('edges','coclique','remaining_population','model_stats','response_stats','factors')}),flush=True)
        return report


def run(folder,partition,root_h,seeds,rounds=6,seconds=90,workers=2,no_lp=False,resume=None,factors=False,all_pairs=False,simple=False,squares=False,max_group=3):
    folder.mkdir(parents=True,exist_ok=True);master=Master(partition,root_h,factors,all_pairs,simple)
    config=dict(partition=partition,root_h=root_h,seed_sources=list(map(str,seeds)),rounds=rounds,seconds=seconds,
                workers=workers,no_lp=no_lp,resume=str(resume) if resume else None,factors=factors,
                all_pairs=all_pairs,simple=simple,squares=squares,oracle_max_group=max_group,
                code_sha256={name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in
                             ('coclique_variable_border_cuts.py','coclique_pair_factors.py','coclique_residual_squares.py','coclique_two_exception_cycles.py')})
    (folder/'config.json').write_text(json.dumps(config,indent=2)+'\n')
    cuts=[]
    if resume:
        for cut in json.loads(resume.read_text()):
            if master.install(cut):cuts.append(cut)
        print(json.dumps(dict(stage='resumed',cuts=len(cuts),local_integer_factors=factors)),flush=True)
    for seed in seeds:
        witness=json.loads(seed.read_text());cut=discover(witness,max_group=max_group,simple=simple)
        if cut.get('status')=='NO_CERTIFICATE':
            print(json.dumps(dict(seed=str(seed),**cut)),flush=True);continue
        cut['source']=str(seed);master.install(cut);cuts.append(cut)
        print(json.dumps(dict(stage='seed_cut',source=str(seed),group=cut['group'],separation=cut['separation'])),flush=True)
    (folder/'cuts.json').write_text(json.dumps(cuts,indent=2)+'\n')
    for iteration in range(rounds):
        source=folder/f'border_{iteration:03d}.json'
        witness=master.solve(source,seconds,workers,no_lp)
        if witness['status'] not in ('OPTIMAL','FEASIBLE'):break
        if squares:
            from coclique_residual_squares import discover as square_discover
            new_cuts=square_discover(witness)
            if new_cuts:
                for cut in new_cuts:
                    cut['source']=str(source);master.install(cut);cuts.append(cut)
                (folder/'cuts.json').write_text(json.dumps(cuts,indent=2)+'\n')
                print(json.dumps(dict(stage='integer_squares',iteration=iteration,added=len(new_cuts),certificates=[c['separation'] for c in new_cuts])),flush=True)
                continue
        cut=discover(witness,max_group=max_group,simple=simple)
        if cut.get('status')=='NO_CERTIFICATE':
            (folder/f'oracle_{iteration:03d}.json').write_text(json.dumps(cut,indent=2)+'\n')
            print(json.dumps(dict(stage='oracle',**cut)),flush=True);break
        cut['source']=str(source);master.install(cut);cuts.append(cut)
        (folder/'cuts.json').write_text(json.dumps(cuts,indent=2)+'\n')
        print(json.dumps(dict(stage='learned',iteration=iteration,group=cut['group'],separation=cut['separation'],search=cut['search'])),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path)
    ap.add_argument('--partition',default='6');ap.add_argument('--root-h',type=int,choices=(0,1),default=1)
    ap.add_argument('--seed',type=Path,action='append',default=[]);ap.add_argument('--rounds',type=int,default=6)
    ap.add_argument('--seconds',type=float,default=90);ap.add_argument('--workers',type=int,default=2);ap.add_argument('--no-lp',action='store_true')
    ap.add_argument('--resume-cuts',type=Path);ap.add_argument('--factors',action='store_true')
    ap.add_argument('--all-pairs',action='store_true')
    ap.add_argument('--simple',action='store_true')
    ap.add_argument('--square-cuts',action='store_true')
    ap.add_argument('--max-group',type=int,default=3)
    args=ap.parse_args();run(args.folder,tuple(map(int,args.partition.split(','))),args.root_h,args.seed,args.rounds,args.seconds,args.workers,args.no_lp,args.resume_cuts,args.factors,args.all_pairs,args.simple,args.square_cuts,args.max_group)
