"""Extract a finite integer domain-propagation proof for a global core design.

Every deletion is justified by a tight lower/upper count in one equation.
Every split enumerates all live columns of one vertex. No LP or SAT
oracle is needed inside this proof-producing search.
"""
import argparse
import json
from pathlib import Path
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parent))
from conway_core_column_dual import features,ColumnPropagation


def run(domain_file,output,seconds=60,max_nodes=10000,separators=None):
    started=time.monotonic()
    record=json.loads(Path(domain_file).read_text(encoding='utf-8'))
    metadata,targets,vectors=features(record)
    certified=[]
    if separators:
        tree=json.loads(Path(separators).read_text(encoding='utf-8'))
        assert tree['domain_file']==domain_file
        def collect(node):
            for branch in node['branches']:
                if 'subtree' in branch:
                    collect(branch['subtree'])
                elif branch['complete']:
                    certificate=json.loads(Path(branch['certificate_file']).read_text(encoding='utf-8'))
                    assert certificate['status']=='EXACT_GLOBAL_COLUMN_SEPARATOR'
                    fixed={record['missing_labels'].index(c['label']):c['domain_index'] for c in certificate['fixed_columns']}
                    weights=[0]*len(targets)
                    for item in certificate['weights']: weights[item['equation_index']]=item['weight']
                    minimum=sum(min(sum(weights[i] for i in ids) for ids in ([g[fixed[p]]] if p in fixed else g))
                                for p,g in enumerate(vectors))
                    target=sum(w*t for w,t in zip(weights,targets))
                    assert minimum-target==certificate['margin'] > 0
                    certified.append(dict(file=branch['certificate_file'],assignment=list(fixed.items()),margin=minimum-target))
        collect(tree)
    propagation=ColumnPropagation(targets,vectors,[c['assignment'] for c in certified])
    nodes=[]
    leaves=0
    def search(live):
        nonlocal leaves
        if time.monotonic() >= started+seconds or len(nodes)>=max_nodes:
            return None,False
        node_id=len(nodes)
        node=dict(id=node_id)
        nodes.append(node)
        live,trace,conflict=propagation.run({},live)
        node['propagation']=trace
        if conflict:
            leaves+=1
            node.update(status='COUNT_CONTRADICTION',conflict=conflict)
            return node_id,True
        options=[(mask.bit_count(),p) for p,mask in enumerate(live) if mask.bit_count()>1]
        if not options:
            assignment=[mask.bit_length()-1 for mask in live]
            sums=[0]*len(targets)
            for p,d in enumerate(assignment):
                for i in vectors[p][d]: sums[i]+=1
            assert sums==targets
            node.update(status='COLUMN_DESIGN_FOUND',assignment=assignment)
            return node_id,False
        _,p=min(options)
        node.update(status='SPLIT',column=p,label=record['missing_labels'][p],branches=[])
        for d in range(len(vectors[p])):
            if not (live[p]>>d&1): continue
            child_live=live.copy()
            child_live[p]=1<<d
            child,closed=search(child_live)
            node['branches'].append(dict(domain_index=d,node=child,closed=closed))
            if not closed:
                node['status']='OPEN_SPLIT'
                return node_id,False
        if len(nodes)%100==0:
            print(json.dumps(dict(stage='INTEGER_PROOF',nodes=len(nodes),leaves=leaves,seconds=time.monotonic()-started)),flush=True)
        return node_id,True
    root,closed=search(propagation.full)
    found=next((n['assignment'] for n in nodes if n.get('status')=='COLUMN_DESIGN_FOUND'),None)
    result=dict(domain_file=str(domain_file),status='EXACT_COUNT_TREE_REFUTATION' if closed else 'COLUMN_DESIGN_FOUND' if found is not None else 'COUNT_TREE_INCOMPLETE',
                complete=closed or found is not None,refutation_complete=closed,
                seconds=time.monotonic()-started,node_count=len(nodes),leaves=leaves,root=root,
                scope='Exact count bounds and exhaustive domain splits on the specified core; only EXACT_COUNT_TREE_REFUTATION certifies exclusion.',
                equations=[dict(target=t,**m) for t,m in zip(targets,metadata)],integer_separators=certified,nodes=nodes)
    if found is not None:
        result['column_indices']=found
    Path(output).write_text(json.dumps(result,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('nodes','equations','integer_separators')}
                     |dict(integer_separators=len(certified))),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--domains',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--seconds',type=float,default=60)
    parser.add_argument('--max-nodes',type=int,default=10000)
    parser.add_argument('--separators',help='Use exact integer separator leaves from a previous split tree as domain nogoods.')
    args=parser.parse_args()
    run(args.domains,args.output,args.seconds,args.max_nodes,args.separators)
