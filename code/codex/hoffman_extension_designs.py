"""Measure the coverage of a variable-boundary theorem, without graph rows.

Enumeration is only exhaustive if CP-SAT finishes OPTIMAL without the cap.
Symmetry normalization retains at least one representative of each extension
up to free point names and interchangeable outside column labels.
"""
from pathlib import Path
import argparse
import json

from ortools.sat.python import cp_model
from hoffman_coexistence_extensions import ExtensionModel, SOURCE, OUT
from hoffman_two_point_trades import design_key


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--prefix',default='37c3bb63972f')
    ap.add_argument('--free',default='3,4,5,6,7')
    ap.add_argument('--seconds',type=float,default=60)
    ap.add_argument('--limit',type=int,default=10000)
    args=ap.parse_args()
    item=next(x for x in json.loads(SOURCE.read_text())['items'] if x['design']['key'].startswith(args.prefix))
    model=ExtensionModel(item['design']['blocks'],list(map(int,args.free.split(','))))
    class Boundaries(cp_model.CpSolverSolutionCallback):
        def __init__(self):
            super().__init__()
            self.classes={}; self.count=0; self.capped=False
        def on_solution_callback(self):
            self.count+=1
            blocks=[[p for p in range(22) if self.value(model.y[p][j])] for j in range(77)]
            key,aut=design_key(blocks)
            if key not in self.classes:
                self.classes[key]=dict(key=key,aut=int(aut),blocks=blocks)
                print('CLASS',len(self.classes),key[:12],'Aut',aut,flush=True)
            if self.count>=args.limit:
                self.capped=True; self.stop_search()
    cb=Boundaries()
    solver=cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions=True
    solver.parameters.num_search_workers=1
    solver.parameters.max_time_in_seconds=args.seconds
    status=solver.solve(model.m,cb)
    result=dict(status=solver.status_name(status),seconds=solver.wall_time,
                exhaustive=status==cp_model.OPTIMAL and not cb.capped,
                symmetry_normalized_labelled_solutions=cb.count,
                isomorphism_classes=list(cb.classes.values()),free=model.free,
                source=item['design']['key'],arguments=vars(args))
    OUT.mkdir(exist_ok=True)
    name='family_'+args.prefix+'_'+args.free.replace(',','-')+'_members.json'
    (OUT/name).write_text(json.dumps(result,indent=2))
    print('RESULT',result['status'],'exhaustive',result['exhaustive'],'labelled',cb.count,
          'classes',len(cb.classes),'seconds',result['seconds'],flush=True)


if __name__=='__main__':main()
