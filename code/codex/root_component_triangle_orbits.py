"""Eight positions of a Conway triangle relative to an unlabelled root star.

The root star has seven mate pairs. Its full relabelling group is used:
these eight representatives cannot be imposed inside an already fixed
root component template without also relabelling that template.
No graph automorphism is assumed. Every root is eligible, including a
root selected by a valid global averaging bound.
"""
import argparse
from itertools import combinations,permutations,product
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_propagation import LABELS
from root_component_resources import atomic_json_write


def partial_matchings(vertices):
    vertices=tuple(vertices)
    if not vertices:
        yield ();return
    a=vertices[0]
    yield from partial_matchings(vertices[1:])
    for i,b in enumerate(vertices[1:],1):
        if a//2==b//2:continue  # a Gamma label may not be a mate pair
        for tail in partial_matchings(vertices[1:i]+vertices[i+1:]):
            yield tuple(sorted(((a,b),)+tail))


def cover():
    lookup={pair:15+i for i,pair in enumerate(LABELS)}
    records=[{'kind':'through_root','line':[0,1,2]},
             {'kind':'one_neighbour_paired','line':[1,lookup[(0,2)],lookup[(0,3)]]},
             {'kind':'one_neighbour_unpaired','line':[1,lookup[(0,2)],lookup[(0,4)]]}]
    maps=[]
    for order in permutations(range(3)):
        for flips in product(range(2),repeat=3):
            maps.append([2*order[i//2]+((i%2)^flips[i//2]) for i in range(6)])
    assert len(set(map(tuple,maps)))==48
    all_matchings=set(partial_matchings(range(6)))
    assert len(all_matchings)==51
    remaining=set(all_matchings);orbits=[]
    while remaining:
        representative=min(remaining,key=lambda r:(len(r),r))
        orbit={tuple(sorted(tuple(sorted((p[a],p[b]))) for a,b in representative)) for p in maps}
        assert orbit<=remaining
        remaining-=orbit
        # Mate edges use one root pair each. Each unmatched position uses
        # a new root pair, of which its other letter is not selected.
        letters=[None]*6;pair_index=0
        for a,b in representative:
            letters[a]=2*pair_index;letters[b]=2*pair_index+1;pair_index+=1
        for a in range(6):
            if letters[a] is None:letters[a]=2*pair_index;pair_index+=1
        gamma_labels=[tuple(sorted(letters[2*i:2*i+2])) for i in range(3)]
        assert len(set(letters))==6 and all(a//2!=b//2 for a,b in gamma_labels)
        record={'kind':'all_second_neighbourhood','mate_edges_on_six_slots':representative,
                'abstract_labelled_patterns':len(orbit),'root_pairs_used':pair_index,
                'gamma_labels':gamma_labels,'line':[lookup[pair] for pair in gamma_labels]}
        records.append(record);orbits.append(orbit)
    assert len(orbits)==5 and sum(map(len,orbits))==51 and len(records)==8
    for i,record in enumerate(records):record['index']=i
    return {'scope':__doc__,'parameters':[99,14,1,2],'record_count':8,
            'all_triangles_covered_relative_to_any_root':True,
            'complete_for_unfixed_root_template':True,
            'usable_after_fixing_arbitrary_root_template_without_relabelling':False,
            'assumed_graph_automorphism':False,'records':records,
            'second_neighbourhood_abstract_patterns':51,
            'second_neighbourhood_orbit_group_order':48,
            'small_line_existence_dependency':'c4_selected_root_closed.json',
            'prism_budget_belongs_to_root_not_selected_line':True}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();assert not a.output.exists()
    result=cover();atomic_json_write(a.output,result)
    print(json.dumps({'record_count':result['record_count'],'records':result['records']}))


if __name__=='__main__':main()
