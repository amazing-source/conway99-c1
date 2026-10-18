"""Export a positive INTEGER certificate for3P+4G<=2772 and its root bound.

Only exact Fraction arithmetic is used. The affine census is the input
identity system; this script neither reruns the LP nor regenerates it.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import lcm
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write


def certify(source, dual, template_source):
    raw=source.read_bytes();data=json.loads(raw)
    report=json.loads(dual.read_text())
    assert hashlib.sha256(raw).hexdigest()==report['source_sha256']
    assert report['exact_upper_certificate'] and report['exact_upper']=='2464/3'
    stages=data['stages'];names=stages[-1]['parameters']
    rows={f"count_{s['order']}_{r['code']}":r for s in stages for r in s['counts']}
    coefficients={r['row']:F(r['weight']) for r in report['certificate']}
    assert coefficients.pop('grid_lower_bound')==F(4,3)
    assert all(label.startswith('count_9_') for label in coefficients)
    scaled={label:3*w for label,w in coefficients.items()}
    scale=lcm(*(w.denominator for w in scaled.values()))
    integer={label:int(w*scale) for label,w in scaled.items()}
    assert all(w>0 for w in integer.values())
    total=[sum(F(rows[label]['affine'][j])*w for label,w in integer.items())
           for j in range(len(names)+1)]
    grid=rows['count_9_13262907120']
    expected=[-4*scale*F(x) for x in grid['affine']]
    expected[0]+=2772*scale;expected[names.index('P')+1]-=3*scale
    assert total==expected
    templates=json.loads(template_source.read_text())['survivors'];cover=[]
    for index in (7,9,19):
        t=templates[index];g=21-len(t['nongrid_edges'])
        cover.append({'template_index':index,'grid_count':g,'prism_lower_bound':4*g,
            'minimum_weighted_score':44*g,'selected_root_score_upper':504,
            'selected_root_prism_upper':(504-8*g)//9,
            'excluded_as_selected_root':44*g>504})
    return {'scope':__doc__,'source':str(source),'source_sha256':hashlib.sha256(raw).hexdigest(),
        'parameters':names,'universal_inequality':'3P+4G<=2772',
        'integer_identity_scale':scale,
        'integer_identity':'sum(weights*N_H) = scale*(2772-3P-4G)',
        'positive_integer_weights':[{'code':rows[label]['code'],'adjacency_bits':rows[label]['adjacency_bits'],
                                    'weight':w} for label,w in integer.items()],
        'all_affine_columns_checked_exactly':len(total),
        'selected_root_inequality':'9s(x)+8g(x)<=504',
        'derivation':'sum_x s(x)=6P; sum_x g(x)=9G; 18*2772=99*504.',
        'global_c4_consequences':{'grid_lower_bound':77,'prism_upper_bound':821,
            'grid_upper_bound_using_P_ge_6G':126,'prism_lower_bound':462},
        'root_order':'weighted_prisms_grids','requires_selected_root':True,
        'usable_in_arbitrary_low_budget_root_frontier':False,
        'earlier_76_exclusions_still_required':True,'survivor_cover':cover,
        'remaining_selected_root_templates':[r['template_index'] for r in cover if not r['excluded_as_selected_root']],
        'global_conway_exclusion':False}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True);p.add_argument('--dual',type=Path,required=True)
    p.add_argument('--templates',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    if a.output.exists():raise FileExistsError(a.output)
    result=certify(a.source,a.dual,a.templates);atomic_json_write(a.output,result)
    print(json.dumps({k:result[k] for k in ('universal_inequality','integer_identity_scale',
        'all_affine_columns_checked_exactly','survivor_cover')}))


if __name__=='__main__':main()
