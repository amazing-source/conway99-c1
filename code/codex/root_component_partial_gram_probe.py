"""Probe a named principal Gram block with all other Gram entries free.

An infeasible branch excludes the stated block inside the stated template,
NEVER the entire component template. This is not a complete branch cover.
"""

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--directory',type=Path,required=True)
    p.add_argument('--block',type=Path,required=True)
    p.add_argument('--design-seconds',type=float,default=8)
    p.add_argument('--joint-seconds',type=float,default=0)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();assert not a.output.exists()
    resources=limit_research_process(1)
    from root_component_partial_gram import canonical_block,filter_catalogue,add_graph_block
    from root_component_z_design import solve_design
    template=json.loads((a.directory/'partition.json').read_text(encoding='utf-8-sig'))['template']
    catalogue_record=json.loads((a.directory/'catalogue.json').read_text(encoding='utf-8-sig'))
    catalogue=catalogue_record['catalogue']
    assert json.loads(Path(catalogue_record['source_bundle']).read_text(encoding='utf-8-sig'))['template']==template
    source=json.loads(a.block.read_text(encoding='utf-8-sig'))
    if 'template' in source:assert source['template']==template
    block=canonical_block(source.get('best_block',source))
    filtered,counts=filter_catalogue(catalogue,block)
    result={'scope':__doc__,'resources':resources,'template':template,'partial_gram':block,
            'source_catalogue':str(a.directory/'catalogue.json'),'source_block':str(a.block),
            'row_filter':counts,'whole_template_excluded':False,'complete_branch_cover':False,
            'global_conway_exclusion':False,'partial_branch_excluded':False}
    atomic_json_write(a.output,result)
    design=solve_design(template,filtered,a.design_seconds,exclude_three_edges=True,
                        short_columns=True,partial_gram=block)
    result['design']=design
    result['partial_branch_excluded']=design['status']=='INFEASIBLE'
    atomic_json_write(a.output,result)
    print(json.dumps({'stage':'design',**{k:v for k,v in design.items() if k!='row_multisets'}}),flush=True)
    if a.joint_seconds<=0 or result['partial_branch_excluded']:return
    if any(not item['states'] for item in filtered['row_types']):
        raise AssertionError('An empty row domain should have been excluded by the design.')
    from root_component_z_joint import build_joint,solve_joint
    info={}
    model,labels,graph=build_joint(14,filtered['row_types'],nongrid=template['nongrid_edges'],
                                  row_moment_coordinates=catalogue['free_coordinates'],
                                  short_columns=True,mate_normalize=True,corner_c2=True,diagnostics=info)
    info['partial_gram']=add_graph_block(model,graph,labels,block)
    joint=solve_joint(model,labels,graph,14,a.joint_seconds)
    result['joint']={**info,**joint}
    result['partial_branch_excluded']=joint['status']=='INFEASIBLE'
    atomic_json_write(a.output,result)
    print(json.dumps({'stage':'joint',**{k:v for k,v in result['joint'].items() if k!='relaxation_edges'}}),flush=True)


if __name__=='__main__':main()
