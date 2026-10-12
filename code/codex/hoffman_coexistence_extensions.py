"""Couple an unfinished Hoffman design to several actual graph rows.

Incidences at free coclique points are VARIABLES, not discarded constraints.
All 2-(22,4,2) equations, block intersections <=2, row quotas, within-row
pair conflicts, and between-row graph equations are imposed simultaneously.
INFEASIBLE excludes every design extension of the fixed incidence template.
A feasible result is only a partial graph and is explicitly labelled so.
"""
from collections import defaultdict
from itertools import combinations
from pathlib import Path
import argparse
import json
import time

from ortools.sat.python import cp_model

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'data/codex_hoffman_trades/proof_bundle.json'
OUT = ROOT / 'data/codex_hoffman_extensions'


class ExtensionModel:
    def __init__(self, blocks, free, symmetry=True):
        self.blocks = [set(b) for b in blocks]
        self.free = sorted(free)
        self.fixed = set(range(22))-set(free)
        self.m = m = cp_model.CpModel()
        self.counter = 0
        self.rows = {}
        self.y = [[0]*77 for _ in range(22)]
        for j, block in enumerate(self.blocks):
            deficit = 4-len(block & self.fixed)
            for p in range(22):
                if p in self.fixed:
                    self.y[p][j] = int(p in block)
                elif deficit == 0:
                    self.y[p][j] = 0
                elif deficit == len(free):
                    self.y[p][j] = 1
                else:
                    self.y[p][j] = m.new_bool_var(f'y{p}_{j}')
            m.add(sum(self.y[p][j] for p in self.free) == deficit)
        for p in self.free:
            m.add(sum(self.y[p]) == 14)
        self.point_pair = {}
        for p, q in combinations(range(22), 2):
            xx = [self.both(self.y[p][j],self.y[q][j]) for j in range(77)]
            self.point_pair[p,q] = xx
            if p in self.free or q in self.free:
                m.add(sum(xx) == 2)
        self.block_overlap = {}
        for i, j in combinations(range(77), 2):
            ov = sum(self.both(self.y[p][i],self.y[p][j]) for p in range(22))
            self.block_overlap[i,j] = ov
            m.add(ov <= 2)
        if symmetry:
            # Free point names are interchangeable; every orbit has a sorted representative.
            for p, q in zip(self.free,self.free[1:]):
                self.lex_le(self.y[p],self.y[q])
            # Columns having equal fixed incidences are also interchangeable.
            groups = defaultdict(list)
            for j,b in enumerate(self.blocks):
                groups[tuple(sorted(b & self.fixed))].append(j)
            for group in groups.values():
                for i,j in zip(group,group[1:]):
                    self.lex_le([self.y[p][i] for p in self.free],
                                [self.y[p][j] for p in self.free])

    def both(self,a,b):
        if isinstance(a,int):
            return b if a else 0
        if isinstance(b,int):
            return a if b else 0
        self.counter += 1
        z = self.m.new_bool_var(f'and{self.counter}')
        self.m.add(z <= a)
        self.m.add(z <= b)
        self.m.add(z >= a+b-1)
        return z

    def lex_le(self,a,b):
        eq = 1
        for x,y in zip(a,b):
            if isinstance(x,int) and isinstance(y,int):
                if x == y:
                    continue
                self.m.add(eq == 0 if x > y else eq >= 0)
                return
            self.m.add(x <= y).only_enforce_if(eq)
            self.counter += 1
            same = self.m.new_bool_var(f'eq{self.counter}')
            self.m.add(x == y).only_enforce_if(same)
            self.m.add(x != y).only_enforce_if(same.Not())
            eq = self.both(eq,same)

    def add_row(self,r):
        if r in self.rows:
            return
        m = self.m
        row = [m.new_bool_var(f'r{r}_{j}') for j in range(77)]
        m.add(row[r] == 0)
        m.add(sum(row) == 10)
        for p in range(22):
            m.add(sum(self.both(row[j],self.y[p][j]) for j in range(77)) == 2-self.y[p][r])
        # Selected blocks cannot share a coclique pair: any such pair would
        # already have its two C-neighbours plus root r as common neighbours.
        for xx in self.point_pair.values():
            m.add(sum(self.both(row[j],xx[j]) for j in range(77)) <= 1)
        for j in range(77):
            if r != j:
                m.add(self.block_overlap[tuple(sorted((r,j)))] <= 1).only_enforce_if(row[j])
        for s,other in self.rows.items():
            m.add(row[s] == other[r])
            common = sum(self.both(row[j],other[j]) for j in range(77))
            m.add(common + self.block_overlap[tuple(sorted((r,s)))] + row[s] == 2)
        self.rows[r] = row

    def add_resolution(self,r,pairwise=True,with_centre=True):
        """Ten transported neighbour rows must resolve the fixed overlap quotas.

        Here B_r is entirely retained, so its 40 overlap-one and 30
        disjoint outside blocks are fixed. Labelling the ten artificial
        rows by the ten blocks on one root point removes their S_10 symmetry.
        """
        assert self.blocks[r] <= self.fixed
        m=self.m
        z=[len(self.blocks[r] & b & self.fixed) for b in self.blocks]
        one=[j for j in range(77) if j!=r and z[j]==1]
        zero=[j for j in range(77) if j!=r and z[j]==0]
        assert len(one)==40 and len(zero)==30
        p=min(self.blocks[r])
        anchors=[j for j in one if p in self.blocks[j]]
        assert len(anchors)==10
        copies=[]
        for anchor in anchors:
            row=[m.new_bool_var(f't{r}_{anchor}_{j}') for j in range(77)]
            copies.append(row)
            m.add(row[r]==0)
            m.add(row[anchor]==1)
            m.add(sum(row)==10)
            for j in range(77):
                if z[j]>=2:m.add(row[j]==0)
            for p in range(22):
                m.add(sum(self.both(row[j],self.y[p][j]) for j in range(77)) == 2-self.y[p][r])
            for xx in self.point_pair.values():
                m.add(sum(self.both(row[j],xx[j]) for j in range(77)) <= 1)
        for j in range(77):
            m.add(sum(row[j] for row in copies)==(2-z[j] if j!=r else 0))
        if pairwise:
            for a,b in combinations(copies,2):
                m.add(sum(self.both(a[j],b[j]) for j in range(77))<=2)
        if with_centre:
            self.add_row(r)
            centre=self.rows[r]
            for row in copies:
                shared_one=sum(self.both(row[j],centre[j]) for j in one)
                shared_zero=sum(self.both(row[j],centre[j]) for j in zero)
                m.add(2*shared_one+shared_zero==2)
        return dict(root=r,anchors=anchors,one=one,zero=zero,
                    pairwise=pairwise,with_centre=with_centre)

    def solve(self,seconds=10,workers=1):
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = seconds
        solver.parameters.num_search_workers = workers
        solver.parameters.random_seed = 20261012
        status = solver.solve(self.m)
        result = dict(status=solver.status_name(status), seconds=solver.wall_time,
                      conflicts=solver.num_conflicts, branches=solver.num_branches,
                      free=self.free, roots=sorted(self.rows), stats=solver.response_stats())
        if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            result['blocks'] = [[p for p in range(22) if solver.value(self.y[p][j])]
                                for j in range(77)]
            result['rows'] = {str(r): [j for j in range(77) if solver.value(row[j])]
                              for r,row in self.rows.items()}
            result['interpretation'] = 'FEASIBLE_PARTIAL_GRAPH_NOT_SRG'
            self.validate_witness(result)
        return result

    def validate_witness(self,result):
        blocks = [set(b) for b in result['blocks']]
        assert len(set(map(tuple,result['blocks']))) == 77
        assert all(len(b) == 4 for b in blocks)
        assert all(sum(p in b for b in blocks) == 14 for p in range(22))
        assert all(sum(p in b and q in b for b in blocks) == 2 for p,q in combinations(range(22),2))
        assert all(len(a&b) <= 2 for a,b in combinations(blocks,2))
        assert all(b & self.fixed == old & self.fixed for b,old in zip(blocks,self.blocks))
        rows = {int(r):set(row) for r,row in result['rows'].items()}
        for r,row in rows.items():
            assert len(row) == 10 and r not in row
            assert all(sum(p in blocks[j] for j in row) == 2-int(p in blocks[r]) for p in range(22))
            assert all(len(blocks[j]&blocks[k]) <= 1 for j,k in combinations(row,2))
            assert all(len(blocks[r]&blocks[j]) <= 1 for j in row)
        for r,s in combinations(rows,2):
            assert (s in rows[r]) == (r in rows[s])
            assert len(rows[r]&rows[s])+len(blocks[r]&blocks[s]) == 2-int(s in rows[r])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seconds',type=float,default=10)
    ap.add_argument('--workers',type=int,default=1)
    ap.add_argument('--prefix',default='37c3bb63972f')
    ap.add_argument('--free',help='Comma-separated free points for one run')
    ap.add_argument('--roots',help='Override comma-separated coupled outside rows')
    ap.add_argument('--no-symmetry',action='store_true')
    args = ap.parse_args()
    item = next(x for x in json.loads(SOURCE.read_text())['items'] if x['design']['key'].startswith(args.prefix))
    blocks = item['design']['blocks']
    roots = list(map(int,args.roots.split(','))) if args.roots else item['compact_certificate']['smallest_incompatible_pair']['rows']
    OUT.mkdir(exist_ok=True)
    record = dict(source_key=item['design']['key'], roots=roots, trials=[])
    free = set()
    if args.free:
        orders = [set(map(int,args.free.split(',')))]
    else:
        mandatory = set().union(*(set(blocks[r]) for r in roots))
        orders = [{p} for p in sorted(set(range(22))-mandatory)]
    for addition in orders:
        trial = free | addition
        start = time.monotonic()
        model = ExtensionModel(blocks,trial,symmetry=not args.no_symmetry)
        for r in roots:
            model.add_row(r)
        build_seconds = time.monotonic()-start
        result = model.solve(args.seconds,args.workers)
        result['build_seconds'] = build_seconds
        record['trials'].append(result)
        if result['status'] == 'INFEASIBLE':
            free = trial
        record['excluded_free_points'] = sorted(free)
        name = 'extensions_'+args.prefix+('_'+args.free.replace(',','-') if args.free else '')+'.json'
        (OUT/name).write_text(json.dumps(record,indent=2))
        print('FREE',sorted(trial),result['status'],'build',round(build_seconds,3),
              'solve',round(result['seconds'],3),'conflicts',result['conflicts'],flush=True)
    print('EXCLUDED',sorted(free),flush=True)


if __name__ == '__main__':
    main()
