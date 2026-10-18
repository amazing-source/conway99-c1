"""Test one rank-seven Gram from a count design or the saved initial catalogue.

The design is an aggregate relaxation, not an adjacency graph. The Gram
constructed from it is one branch only, never a complete template cover.
"""

import argparse
from itertools import combinations
import gzip
import hashlib
import json
from pathlib import Path
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',type=Path)
    p.add_argument('--design-seconds',type=float,default=8)
    p.add_argument('--joint-seconds',type=float,default=0)
    p.add_argument('--saved-gram',action='store_true',
                   help='Use the initial Gram saved in the source catalogue, not a new count design.')
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();assert not a.output.exists()
    resources=limit_research_process(1)
    import sympy as sp
    from root_component_z_design import solve_design
    from root_component_corner_moment_bounds import analyze_gram
    partition=json.loads((a.directory/'partition.json').read_text(encoding='utf-8-sig'))
    template=partition['template']
    result={'scope':__doc__,'resources':resources,'source':str(a.directory),
            'global_conway_exclusion':False,'whole_template_excluded':False,'complete_Gram_cover':False}
    rectangles=list(combinations(range(7),2));edges=[tuple(q) for q in template['nongrid_edges']]
    if a.saved_gram:
        source=Path(partition['source_path']);blob=source.read_bytes()
        assert hashlib.sha256(blob).hexdigest()==partition['source_sha256']
        archive=json.loads(gzip.decompress(blob) if source.suffix=='.gz' else blob)
        record=archive.get('open',archive.get('survivors'))[partition['template_index']]
        assert record['template']==template
        R=sp.Matrix(record['gram']['R'])
        result['gram_source']={'path':str(source),'sha256':partition['source_sha256'],
                               'template_index':partition['template_index'],
                               'scope':'One previously saved quotient Gram, not a cover.'}
    else:
        catalogue=json.loads((a.directory/'catalogue.json').read_text(encoding='utf-8-sig'))['catalogue']
        design=solve_design(template,catalogue,a.design_seconds,exclude_three_edges=True,short_columns=True)
        result['design']=design
        atomic_json_write(a.output,result)
        print(json.dumps({'stage':'design',**{k:v for k,v in design.items() if k!='row_multisets'}}),flush=True)
        if design['status'] not in ('OPTIMAL','FEASIBLE'):
            return
        selected=[rectangles.index(q) for q in edges]
        hs=[[3*int(q==f)+1-len(set(q)&set(f))-z[j] for j,f in enumerate(rectangles)]
            for q,group in zip(rectangles,design['row_multisets']) for z in group['states']]
        H=sp.Matrix(hs).extract(range(84),selected)
        R=(H.T*H)/7
        assert all(x.q==1 for x in R)
        for i,fi in enumerate(selected):
            assert R[i,i]==8-sum(z[fi] for z in design['row_multisets'][fi]['states'])
    result.update(edges=[list(q) for q in edges],gram=[[int(x) for x in row] for row in R.tolist()],rank=R.rank())
    atomic_json_write(a.output,result)
    print(json.dumps({'stage':'Gram','rank':result['rank'],'trace':int(sp.trace(R))}),flush=True)
    if result['rank']!=7:
        result['rank7_exercised']=False;atomic_json_write(a.output,result);return
    started=time.process_time()
    filtered=analyze_gram(edges,result['gram'],separate_moments=True)
    result['corner_filter']=filtered;result['rank7_exercised']=True
    atomic_json_write(a.output,result)
    print(json.dumps({'stage':'rank7_corner_filter','status':filtered['status'],
                      'cpu_seconds':time.process_time()-started}),flush=True)
    if a.joint_seconds>0 and filtered['status']!='EXCLUDED':
        from root_component_signature_joint import solve
        joint=solve(template,R,a.joint_seconds,layer=0,eigen=True,mate_normalize=True,
                    corners=True,short_vectors=True,upper_projector=True,cpu_time=True,workers=1)
        result['joint']=joint;atomic_json_write(a.output,result)
        print(json.dumps({'stage':'joint',**{k:v for k,v in joint.items() if k!='relaxation_edges'}}),flush=True)


if __name__=='__main__':main()
