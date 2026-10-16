"""Direct SAT translation of the Boolean grid-boundary relaxation.

Translations support the actual Boolean linear and Boolean-or constraints
of this model. Exact-cardinality counters retain both directions, including
their lower bounds. SAT boundaries are checked against the source model.
"""

import argparse
from itertools import combinations
import json
from pathlib import Path
import sys
from threading import Timer
import time

from pysat.card import CardEnc
from pysat.solvers import Solver

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_grid_boundary import build
from root_component_propagation import LABELS,PAIRS


class Encoder:
    def __init__(self,n):
        self.nv=n
        self.clauses=[]
    def var(self):
        self.nv+=1
        return self.nv
    @staticmethod
    def neg(x):return not x if type(x) is bool else -x
    def clause(self,*xs):
        if any(x is True for x in xs):return
        xs=list(dict.fromkeys(x for x in xs if x is not False))
        if any(-x in xs for x in xs):return
        self.clauses.append(xs)
    def exactly(self,xs,target):
        if target<0 or target>len(xs):self.clause();return
        if target==0:
            for x in xs:self.clause(-x)
            return
        if target==len(xs):
            for x in xs:self.clause(x)
            return
        if target>len(xs)//2:
            xs=[-x for x in xs]
            target=len(xs)-target
        previous=[True]+[False]*target
        for i,x in enumerate(xs):
            self.clause(self.neg(previous[target]),-x)
            current=[True]
            for j in range(1,target+1):
                if j>i+1:current.append(False);continue
                z=self.var()
                p,q=previous[j],previous[j-1]
                self.clause(self.neg(p),z)
                self.clause(self.neg(q),-x,z)
                self.clause(-z,p,q)
                self.clause(-z,p,x)
                current.append(z)
            previous=current
        self.clause(previous[target])
    def atmost(self,xs,k):
        if k<0:self.clause();return
        if k>=len(xs):return
        result=CardEnc.atmost(lits=xs,bound=k,top_id=self.nv,encoding=1)
        self.nv=max(self.nv,result.nv)
        self.clauses.extend(result.clauses)


def dimacs_literal(cp_literal):
    return cp_literal+1 if cp_literal>=0 else cp_literal


def encode(model):
    enc=Encoder(len(model.proto.variables))
    for i,v in enumerate(model.proto.variables):
        domain=list(v.domain)
        assert domain in ([0,1],[0,0],[1,1]),domain
        if domain==[0,0]:enc.clause(-(i+1))
        if domain==[1,1]:enc.clause(i+1)
    for c in model.proto.constraints:
        start=len(enc.clauses)
        if c.has_linear():
            assert len(c.linear.domain)==2
            literals=[]
            shift=0
            for v,coefficient in zip(c.linear.vars,c.linear.coeffs):
                assert coefficient in (-1,1),coefficient
                literals.append((v+1)*coefficient)
                shift+=int(coefficient<0)
            lo,hi=(int(x)+shift for x in c.linear.domain)
            if lo==hi:enc.exactly(literals,lo)
            else:
                enc.atmost(literals,hi)
                enc.atmost([-x for x in literals],len(literals)-lo)
        elif c.has_bool_or():
            enc.clause(*(dimacs_literal(x) for x in c.bool_or.literals))
        else:
            raise ValueError(f"Unsupported constraint: {c}")
        guards=[-dimacs_literal(x) for x in c.enforcement_literal]
        if guards:
            for row in enc.clauses[start:]:row.extend(guards)
    return enc


def check_model(model,assignment):
    def truth(lit):return assignment[lit] if lit>=0 else 1-assignment[-lit-1]
    for c in model.proto.constraints:
        if not all(truth(x) for x in c.enforcement_literal):continue
        if c.has_linear():
            value=sum(coefficient*assignment[v] for v,coefficient in zip(c.linear.vars,c.linear.coeffs))
            assert c.linear.domain[0]<=value<=c.linear.domain[1]
        elif c.has_bool_or():assert any(truth(x) for x in c.bool_or.literals)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    parser.add_argument("--indices",type=int,nargs="+",required=True)
    parser.add_argument("--seconds",type=float,default=180)
    parser.add_argument("--solver",default="glucose4")
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    templates=json.loads((args.directory/"root_component_templates.json").read_text())["survivors"]
    records=[]
    for index in args.indices:
        started=time.monotonic()
        model,graph,info=build(templates[index],normalize=True)
        enc=encode(model)
        info.update(template_index=index,cnf_variables=enc.nv,cnf_clauses=len(enc.clauses),
                    build_seconds=time.monotonic()-started,status="CNF_BUILT",solver=args.solver)
        print(json.dumps(info),flush=True)
        with Solver(name=args.solver,bootstrap_with=enc.clauses) as solver:
            started=time.monotonic()
            timer=Timer(args.seconds,solver.interrupt)
            timer.start()
            try:status=solver.solve_limited(expect_interrupt=True)
            finally:timer.cancel()
            info.update(status="SAT_BOUNDARY" if status else ("UNSAT" if status is False else "UNKNOWN"),
                        seconds=time.monotonic()-started,stats=solver.accum_stats())
            if status:
                assignment=[int(x>0) for x in solver.get_model()[:len(model.proto.variables)]]
                check_model(model,assignment)
                gamma=[[None if x is None else (x if isinstance(x,int) else assignment[x.index]) for x in row] for row in graph]
                for u,v in combinations(info["grid_vertices"],2):
                    assert gamma[u][v]+sum(gamma[u][z]*gamma[v][z] for z in range(84))==2-len(set(LABELS[u])&set(LABELS[v]))
                info["boundary_edges"]=[[u,v] for u,v in PAIRS if gamma[u][v]==1]
                info["source_model_checked"]=True
        records.append(info)
        args.output.write_text(json.dumps({"scope":__doc__,"records":records},separators=(",",":"))+"\n",encoding="utf-8")
        print(json.dumps({k:v for k,v in info.items() if k!="boundary_edges"}),flush=True)


if __name__=="__main__":main()
