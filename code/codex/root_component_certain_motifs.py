"""Certified lower counts of fully fixed induced9 motifs in a partial star.

Unknown edges never count as absent. Every emitted vertex subset has all36
pairs fixed and is induced-isomorphic to a positive-weight census motif.
A CPU timeout truncates enumeration and leaves a valid LOWER bound only.
The universal certificate then bounds3P+4G by2772-ceil(weighted_lower/9504).
"""
import argparse
import json
from pathlib import Path
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process
from root_component_propagation import LABELS,PAIRS,propagate
from root_component_complete_star import matching_cover,matching_assignments
from root_component_low_budget_transport import digest


def known_graph(template,root_line,matching_index):
    extra=None
    if root_line is not None:
        _,_,_,cover=matching_cover(template,root_line)
        extra=matching_assignments(root_line,cover[matching_index])
    propagation=propagate(template,extra_initial=extra)
    assert not propagation['conflict'],propagation['conflict']
    graph=[[0]*99 for _ in range(99)]
    for a in range(14):
        graph[0][a+1]=graph[a+1][0]=1
        graph[a+1][(a^1)+1]=1
    for w,label in enumerate(LABELS):
        for a in label:graph[a+1][w+15]=graph[w+15][a+1]=1
    for u,v in PAIRS:graph[u+15][v+15]=graph[v+15][u+15]=None
    for vi,value,_ in propagation['assignments']:
        u,v=PAIRS[vi];graph[u+15][v+15]=graph[v+15][u+15]=value
    return graph,propagation


def count_pattern(graph,bits,seconds,limit):
    n=len(graph)
    positive=[sum(1<<v for v,x in enumerate(row) if x==1) for row in graph]
    negative=[sum(1<<v for v,x in enumerate(row) if v!=u and x==0) for u,row in enumerate(graph)]
    domains=[sum(1<<v for v in range(n)
                 if positive[v].bit_count()>=bits[p].bit_count()
                 and negative[v].bit_count()>=8-bits[p].bit_count()) for p in range(9)]
    found=set();calls=0;start=time.process_time();ended=False
    class StopEnumeration(Exception):pass
    def visit(remaining,available,mask):
        nonlocal calls
        calls+=1
        if calls%4096==0 and time.process_time()-start>=seconds:raise StopEnumeration
        if not remaining:
            found.add(mask)
            if len(found)>=limit:raise StopEnumeration
            return
        p=min(remaining,key=lambda p:(available[p].bit_count(),-bits[p].bit_count(),p))
        candidates=available[p];rest=remaining-{p}
        while candidates:
            flag=candidates&-candidates;candidates-=flag;v=flag.bit_length()-1
            updated=list(available)
            for q in rest:
                updated[q]&=positive[v] if bits[p]>>q&1 else negative[v]
                if not updated[q]:break
            else:visit(rest,updated,mask|flag)
    try:
        visit(set(range(9)),domains,0);ended=True
    except StopEnumeration:pass
    assert all(mask.bit_count()==9 for mask in found)
    return {'status':'EXACT_COUNT' if ended else 'PARTIAL_LOWER_BOUND',
            'lower_count':len(found),'search_calls':calls,'cpu_seconds':time.process_time()-start,
            'vertex_masks_hex':sorted(hex(mask) for mask in found)}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',type=Path)
    p.add_argument('--index',type=int,required=True)
    p.add_argument('--root-line',type=int,choices=range(7))
    p.add_argument('--matching-index',type=int)
    p.add_argument('--certificate',type=Path,required=True)
    p.add_argument('--seconds-per-pattern',type=float,default=2)
    p.add_argument('--maximum-witnesses-per-pattern',type=int,default=50000)
    p.add_argument('--controls',action='store_true')
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();resources=limit_research_process(1)
    assert not a.output.exists()
    assert (a.root_line is None)==(a.matching_index is None)
    templates=a.directory/'root_component_templates.json'
    template=json.loads(templates.read_text())['survivors'][a.index]
    certificate=json.loads(a.certificate.read_text())
    if a.controls:
        checks=[]
        for motif in certificate['positive_integer_weights']:
            bits=motif['adjacency_bits']
            graph=[[int(bits[i]>>j&1) for j in range(9)] for i in range(9)]
            positive=count_pattern(graph,bits,5,1000)
            assert positive['status']=='EXACT_COUNT' and positive['lower_count']==1
            i,j=next((i,j) for i in range(9) for j in range(i) if graph[i][j])
            graph[i][j]=graph[j][i]=0
            negative=count_pattern(graph,bits,5,1000)
            assert negative['status']=='EXACT_COUNT' and negative['lower_count']==0
            checks.append({'code':motif['code'],'positive':1,'one_deleted_edge':0})
        result={'status':'PASSED','scope':'Every census motif on itself and after deleting one edge.',
                'resources':resources,'checks':checks}
        atomic_json_write(a.output,result);print(json.dumps(result),flush=True);return
    graph,propagation=known_graph(template,a.root_line,a.matching_index)
    result={'scope':__doc__,'template_index':a.index,'root_line':a.root_line,
            'matching_index':a.matching_index,'resources':resources,
            'templates_sha256_lf':digest(templates),'certificate_sha256_lf':digest(a.certificate),
            'fixed_gamma_pairs':len(propagation['assignments']),'cases':[],
            'weighted_count_lower':0,'global_conway_exclusion':False}
    for motif in sorted(certificate['positive_integer_weights'],key=lambda m:-m['weight']):
        row=count_pattern(graph,motif['adjacency_bits'],a.seconds_per_pattern,a.maximum_witnesses_per_pattern)
        row.update(code=motif['code'],weight=motif['weight'])
        result['cases'].append(row)
        result['weighted_count_lower']+=row['lower_count']*row['weight']
        scale=certificate['integer_identity_scale']
        result['improved_3P_plus_4G_upper']=2772-(result['weighted_count_lower']+scale-1)//scale
        atomic_json_write(a.output,result)
        print(json.dumps({k:row[k] for k in ('code','weight','status','lower_count','cpu_seconds')}|
                         {k:result[k] for k in ('weighted_count_lower','improved_3P_plus_4G_upper')}),flush=True)


if __name__=='__main__':main()
