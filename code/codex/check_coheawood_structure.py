"""Exact finite checks for the co-Heawood boundary normalisation.

No claim of existence or nonexistence of a 99-vertex completion is made.
The rank-16 assertion is proved from Q^2=21Q in the accompanying note.
"""
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path
from coheawood_completion import boundary


def matchings(vertices):
    if not vertices:
        yield ()
        return
    a = vertices[0]
    for b in vertices[1:]:
        rest = tuple(x for x in vertices if x not in (a,b))
        for m in matchings(rest):
            yield tuple(sorted(((a,b),)+m))


def main():
    allowed = {m for m in matchings(tuple(range(6))) if all(a//2 != b//2 for a,b in m)}
    assert len(allowed) == 8
    standard = ((0,2),(1,5),(3,4))
    orbit = set()
    for bits in product((0,1),repeat=3):
        p = [i ^ bits[i//2] for i in range(6)]
        orbit.add(tuple(sorted(tuple(sorted((p[a],p[b]))) for a,b in standard)))
    assert orbit == allowed
    a,names,b,cells = boundary()
    assert len(names) == 99
    assert Counter(map(len,cells.values())) == {1:28,2:21}
    for u in range(14):
        assert all(isinstance(x,int) for x in a[u]) and sum(a[u]) == 14
        for v in range(u+1,14):
            assert sum(a[u][w]*a[v][w] for w in range(99)) == 2-a[u][v]
    for u,v in combinations(range(7),2):
        assert sum(b[u][t]*b[v][t] for t in range(7)) == 2
    cross_edges=sum(names[u][1] != names[v][1] and names[u][2] != names[v][2]
                    for u,v in combinations(range(14,84),2))
    assert cross_edges==1806
    assert sum(a[u][v] is None for u,v in combinations(range(99),2))==2940
    # Check the Gram projection coefficient, independently of the unknown
    # R adjacencies and the unknown triples on Z.
    for (s,t),(u,v) in product(cells,cells):
        kr=[1-b[s][j]-3*int(j==t) for j in range(7)]
        kq=[1-b[u][j]-3*int(j==v) for j in range(7)]
        assert sum(kr)==sum(kq)==0
        dot=sum(x*y for x,y in zip(kr,kq))
        assert dot == -5+2*int(s==u)+9*int(t==v)+3*(b[s][v]+b[u][t])
    report=dict(status='PASS', local_matchings=8, independent_cell_flip_orbit=8,
                column_matching_patterns=8**7, single_cells=28,double_cells=21,
                cross_row_column_pairs=cross_edges, solver_edge_variables=2940,
                gram_coefficients_checked=49**2,
                scope='boundary and normalisation only; no completion or exclusion')
    out=Path(__file__).resolve().parents[2]/'data/codex_coheawood/structure_checks.json'
    out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report),flush=True)


if __name__=='__main__': main()
