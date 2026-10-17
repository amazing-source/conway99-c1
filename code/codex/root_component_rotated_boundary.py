"""A rotated no-three-edge rectangle forbids outside rainbow triples.

For a triangle (a,b,c) in the coloured cubic neighbourhood of a line,
write (a',b',c') for the same-colour mates. If their only edge is a'b',
no outside vertex z can be adjacent to a',b',c simultaneously.
Indeed, root at a and use its lines (a,L_a,a') and (a,b,c).
Their four corners are L_b,L_c,b',z, inducing the path L_c-L_b-b'-z.
This is exactly the universally forbidden three-edge rectangle.

The rule is valid for every external boundary. It does not fix a local
code: Boolean flags are linked to the whole allowed code table.
"""

from itertools import combinations
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_propagation import LABELS


def forbidden_triples(record,code):
    pi,ma,mb=code;p=record['cross_permutations'][pi];n=len(p)
    mates=[[i^1 for i in range(n)]]
    for mi in (ma,mb):
        row=[None]*n
        for a,b in record['internal_matchings'][mi]:row[a]=b;row[b]=a
        mates.append(row)
    triples=set()
    for i in range(n):
        if p[i]!=i:continue
        values=[mates[c][i] for c in range(3)]
        edge_pairs=[]
        if values[0]==values[1]:edge_pairs.append((0,1))
        if values[0]==values[2]:edge_pairs.append((0,2))
        if p[values[1]]==values[2]:edge_pairs.append((1,2))
        if len(edge_pairs)!=1:continue
        a,b=edge_pairs[0]
        triple=[i]*3;triple[a]=values[a];triple[b]=values[b]
        triples.add(tuple(triple))
    return sorted(triples)


def add_code_cuts(model,graph,record,codes,selectors,stars,root,part):
    codes=sorted(set(tuple(c) for c in codes))
    sets=[set(forbidden_triples(record,c)) for c in codes]
    triples=sorted(set().union(*sets))
    if not triples:return {'root_line':root,'part':part,'rainbow_triples':0,'cuts':0}
    flags=[model.new_bool_var(f'rotated_triple_{root}_{part[0]}_{i}') for i in range(len(triples))]
    model.add_allowed_assignments(selectors+flags,
                                 [list(code)+[int(t in ts) for t in triples] for code,ts in zip(codes,sets)])
    letters=[2*j+b for j in sorted(part) for b in range(2)]
    cuts=0
    for flag,(i,j,k) in zip(flags,triples):
        letter=letters[i];u,v=stars[0][j],stars[1][k]
        for w,label in enumerate(LABELS):
            if root in (a//2 for a in label) or letter not in label:continue
            model.add(graph[w][u]+graph[w][v]+flag<=2)
            cuts+=1
    return {'root_line':root,'part':part,'codes':len(codes),'rainbow_triples':len(triples),'cuts':cuts}


def fixed_forbidden_triples(c,colours):
    mates=[]
    for u,row in enumerate(c):
        same=[v for v,value in enumerate(row) if value and colours[u]==colours[v]]
        assert len(same)==1;mates.append(same[0])
    triples=set()
    for tri in combinations(range(len(c)),3):
        if not all(c[u][v] for u,v in combinations(tri,2)):continue
        assert len({colours[u] for u in tri})==3
        values=[mates[u] for u in tri]
        edges=[(a,b) for a,b in combinations(range(3),2) if c[values[a]][values[b]]]
        if len(edges)!=1:continue
        a,b=edges[0];other=3-a-b
        triples.add(tuple(sorted((values[a],values[b],tri[other]))))
    return sorted(triples)


def check_rotated_witness(record,code):
    """Check the actual rooted P4 for every forbidden triple of this code."""
    from root_component_prism_frame import component
    c,colours=component(record,code);n=len(c)//3;checked=0
    expected={tuple(sorted((a,n+b,2*n+d))) for a,b,d in forbidden_triples(record,code)}
    assert expected==set(fixed_forbidden_triples(c,colours))
    mates=[next(v for v in range(len(c)) if c[u][v] and colours[u]==colours[v]) for u in range(len(c))]
    for tri in combinations(range(len(c)),3):
        if not all(c[u][v] for u,v in combinations(tri,2)):continue
        vals=[mates[u] for u in tri]
        edges=[(a,b) for a,b in combinations(range(3),2) if c[vals[a]][vals[b]]]
        if len(edges)!=1:continue
        a,b=edges[0];third=3-a-b
        selected={vals[a],vals[b],tri[third]}
        z=3+len(c);g=[set() for _ in range(z+1)]
        def edge(u,v):g[u].add(v);g[v].add(u)
        for u,v in combinations(range(3),2):edge(u,v)
        for u in range(len(c)):
            edge(colours[u],3+u)
            for v in range(u):
                if c[u][v]:edge(3+u,3+v)
        for u in selected:edge(z,3+u)
        root=3+tri[a]
        first=(colours[tri[a]],3+vals[a]);second=(3+tri[b],3+tri[third])
        corners=[]
        for u in first:
            for v in second:
                common=(g[u]&g[v])-{root}
                assert len(common)==1,(code,tri,u,v,common)
                corners.append(next(iter(common)))
        assert len(set(corners))==4 and all(v not in g[root] for v in corners)
        assert sorted(len(g[u]&set(corners)) for u in corners)==[1,1,2,2]
        assert sum(len(g[u]&set(corners)) for u in corners)==6
        checked+=1
    return checked


if __name__=='__main__':
    import argparse,json
    from pathlib import Path
    from root_component_resources import limit_research_process,atomic_json_write
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',type=Path);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();resources=limit_research_process(1)
    library=json.loads((args.directory/'line_component_pattern_tables_rotated.json').read_text())
    cover=json.loads((args.directory/'line_component_colored_orbits.json').read_text())
    rows=[]
    for record in library['records']:
        if record['vertices'] not in (12,18):continue
        orbits=next(r for r in cover['records'] if r['vertices']==record['vertices'] and r['allow_colour_permutations'])
        for i,orbit in enumerate(orbits['orbits']):
            code=orbit['representative'];count=check_rotated_witness(record,code)
            rows.append({'vertices':record['vertices'],'orbit':i,'code':code,'rooted_P4_witnesses_checked':count})
    output={'scope':__doc__,'resources':resources,'component_types_checked':len(rows),
            'rooted_P4_witnesses_checked':sum(r['rooted_P4_witnesses_checked'] for r in rows),'records':rows}
    atomic_json_write(args.output,output)
    print({k:v for k,v in output.items() if k not in ('scope','records')},flush=True)
