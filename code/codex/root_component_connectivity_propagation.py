"""Exact known-component propagation under the GLOBAL hypothesis c>=4.

For any triangle L in srg(99,14,1,2), its outside neighbourhood has36
vertices in three colour classes. Each vertex has exactly one neighbour
in each colour, including its own. Every connected component therefore
has equally many vertices of each colour and its order is a multiple of6.
At least four components force every component to have at most18 vertices.

A known connected component exceeding18 vertices (or six of one colour)
is impossible. A known18-component is closed: every edge to another known
neighbour of L is zero. Its known neighbours outside it cannot acquire
an edge to L. These implications are interleaved with exact C1/C2 binary
propagation. This is unavailable without the global c>=4 hypothesis.
"""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_propagation import LABELS, PAIRS, VARIABLE, propagate
from root_component_boundary_psd import fixed_line_graph
from root_component_resources import atomic_json_write,limit_research_process


def full_partial_graph(assignments):
    a=[[-1]*99 for _ in range(99)]
    for i in range(99):a[i][i]=0
    for i in range(1,99):a[0][i]=a[i][0]=int(i<=14)
    for i,j in combinations(range(14),2):a[i+1][j+1]=a[j+1][i+1]=int(j==(i^1))
    for w,label in enumerate(LABELS):
        for i in range(14):a[i+1][w+15]=a[w+15][i+1]=int(i in label)
    for vi,value,*_ in assignments:
        u,v=PAIRS[vi];a[u+15][v+15]=a[v+15][u+15]=value
    return a


def inspect_known_triangles(a):
    neighbours=[{v for v,value in enumerate(row) if value==1} for row in a]
    triangles=[(u,v,w) for u in range(99) for v in sorted(neighbours[u]) if u<v
               for w in sorted(neighbours[u]&neighbours[v]) if v<w]
    implications={};closed=[];maximum=0
    def force_zero(u,v,reason):
        if a[u][v]==0:return
        assert a[u][v]==-1 and u>=15 and v>=15
        implications[VARIABLE[tuple(sorted((u-15,v-15)))]]=reason
    for line in triangles:
        colours={}
        for i,l in enumerate(line):
            for w in neighbours[l]-set(line):
                if w in colours:
                    return {},{'kind':'two_neighbours_on_triangle','line':line,'vertex':w}
                colours[w]=i
        remaining=set(colours);components=[]
        while remaining:
            first=min(remaining);component={first};pending=[first];remaining.remove(first)
            while pending:
                u=pending.pop()
                adjacent=neighbours[u]&remaining
                component.update(adjacent);remaining.difference_update(adjacent);pending.extend(adjacent)
            maximum=max(maximum,len(component))
            counts=Counter(colours[w] for w in component)
            reason={'line':list(line),'component':sorted(component),'colour_counts':[counts[i] for i in range(3)]}
            components.append((component,counts,reason))
            if len(component)>18 or max(counts.values())>6:
                return {},dict(reason,kind='known_component_exceeds_global_c4_bound')
            saturated=[i for i in range(3) if counts[i]==6]
            for u in component:
                for v in neighbours[u]-component-set(line):
                    for colour in saturated:force_zero(v,line[colour],reason)
            if len(component)!=18:continue
            assert [counts[i] for i in range(3)]==[6,6,6]
            for u in component:
                for colour in range(3):
                    if not any(v!=u and colours[v]==colour and a[u][v]!=0 for v in component):
                        return {},dict(reason,kind='closed_component_missing_colour_neighbour',vertex=u,colour=colour)
                for v in set(colours)-component:
                    force_zero(u,v,reason)
                for v in neighbours[u]-component-set(line):
                    for l in line:force_zero(v,l,reason)
            closed.append(reason)
        # Two known pieces need not already be full18 components. If their
        # union exceeds any colour capacity, even one joining edge is forbidden.
        for (left,lc,lr),(right,rc,rr) in combinations(components,2):
            if any(lc[i]+rc[i]>6 for i in range(3)):
                reason={'line':list(line),'incompatible_components':[lr,rr]}
                for u in left:
                    for v in right:force_zero(u,v,reason)
    return implications,{'known_triangles':len(triangles),'closed18_components':closed,
                         'maximum_known_component_vertices':maximum}


def propagate_global_c4(template,extra_initial):
    assert min(template['component_count_by_root_line'])>=4
    extra=dict(extra_initial);rounds=[];all_added={}
    while True:
        binary=propagate(template,extra_initial=extra)
        if binary['status']=='PROPAGATION_CONTRADICTION':
            return {'status':'INFEASIBLE','method':'C1_C2_AFTER_COMPONENT_CLOSURE',
                    'rounds':rounds,'binary':binary,'added_zeros':all_added}
        implications,info=inspect_known_triangles(full_partial_graph(binary['assignments']))
        if 'kind' in info:
            return {'status':'INFEASIBLE','method':'KNOWN_TRIANGLE_COMPONENT',
                    'conflict':info,'rounds':rounds,'binary':binary,'added_zeros':all_added}
        rounds.append(dict(info,new_zeros=len(implications)))
        if not implications:
            return {'status':'UNRESOLVED','rounds':rounds,'binary':binary,'added_zeros':all_added}
        for vi,reason in implications.items():
            assert vi not in extra
            extra[vi]=0;all_added[str(vi)]=reason


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',type=Path)
    p.add_argument('--codes-from',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();limit_research_process(1)
    if args.output.exists():raise FileExistsError(args.output)
    source=json.loads(args.codes_from.read_text(encoding='utf-8-sig'))
    record=source['records'][0];case=record['cases'][0]
    template=json.loads((args.directory/'root_component_templates.json').read_text())['survivors'][record['template_index']]
    tables=json.loads((args.directory/'line_component_pattern_tables_e3_all_colours.json').read_text())
    results=[]
    for i,code in enumerate(case['component_codes']):
        empty=[[-1]*84 for _ in range(84)]
        for u in range(84):empty[u][u]=0
        fixed=fixed_line_graph(empty,template,tables,case['component_root'],case['component_part'],code)
        extra={vi:fixed[u][v] for vi,(u,v) in enumerate(PAIRS) if fixed[u][v]!=-1}
        result=propagate_global_c4(template,extra)
        # Keep the exact inputs and closure reasons, without duplicating the
        # many elementary root-cardinality propagation steps in every row.
        result['fixed_edges']=result['binary']['fixed_edges']
        result['binary_conflict']=result['binary']['conflict'];del result['binary']
        results.append(dict(component_index=i,code=code,**result))
        print(json.dumps({'code':i,'status':result['status'],'added_zeros':len(result['added_zeros'])}),flush=True)
    output={'scope':__doc__,'global_minimum_components':4,'source':str(args.codes_from),
            'template_index':record['template_index'],'gram_index':case['gram_index'],
            'uses_fixed_gram':False,'component_codes':case['component_codes'],'results':results,
            'counts':dict(Counter(r['status'] for r in results))}
    atomic_json_write(args.output,output)


if __name__=='__main__':main()
