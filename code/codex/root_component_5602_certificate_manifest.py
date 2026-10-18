"""Assemble the complete 5602 ledger and replay its elementary frontier certificates.

The earlier finite core/boundary/join enumerations remain explicit proof
inputs, with their source code and hashes. This reader checks coverage
and reconstructs each surviving 36-vertex graph from its permutations;
it replays the empty-domain or capacity contradiction using integers.
It is not an independent proof of the completeness of the enumerators.
"""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process
from root_component_5602_grid_join import materialize,check_graph
from root_component_5602_frontier import test as frontier_test


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def build_manifest(cover_path,join_path,frontier_path):
    cover,join,frontier=map(read,(cover_path,join_path,frontier_path))
    orbits=cover['orbit_reduction']['orbits']
    assert cover['complete_eight_vertex_enumeration']
    assert cover['counts']['e2_C2']==sum(o['orbit_size'] for o in orbits)==304
    expected={(i,j) for i,o in enumerate(orbits) for j in range(len(o['boundaries']['cases']))}
    assert len(expected)==1328
    for o in orbits:
        assert o['boundaries']['status'] in ('COMPLETE_BOUNDARY_COVER','EXCLUDED_CORE')
        if o['boundaries']['status']=='EXCLUDED_CORE':assert o['three_grids']['status']=='EXCLUDED_CORE'
    records={(c['orbit'],c['boundary_index']):c['result'] for c in join['cases']}
    assert len(records)==len(join['cases']) and set(records)==expected
    allowed={'EXCLUDED_BY_EXHAUSTIVE_JOIN','EXCLUDED_BY_INTEGER_MARGINS','FEASIBLE_PARTIAL_36'}
    assert all(r['status'] in allowed for r in records.values())
    remaining={key for key,r in records.items() if r['status']=='FEASIBLE_PARTIAL_36'}
    assert remaining=={(6,517),(6,562),(6,603)}
    endings={(c['orbit'],c['boundary_index']):c['result'] for c in frontier['cases']}
    assert len(endings)==len(frontier['cases']) and set(endings)==remaining
    certificates=Counter();partial_counts={};replayed=0
    for (i,j),result in sorted(endings.items()):
        assert result['status']=='EXCLUDED_BY_EXHAUSTIVE_JOIN'
        assert result['complete_frontier_enumeration']
        certs=result['frontier_certificates']
        assert len(certs)==result['valid_partial36_graphs']
        assert len({json.dumps(c['pair_witness']) for c in certs})==len(certs)
        assert result['rejected_joins']['frontier_obstruction']==len(certs)
        assert sum(result['rejected_joins'].values())==result['joined_candidates']
        partial_counts[f'{i}:{j}']=len(certs)
        boundary=orbits[i]['boundaries']['cases'][j]['core_neighbours_of_grid_vertices']
        for record in certs:
            a,b=record['pair_witness']
            g=materialize(orbits[i]['representative'],boundary,a,b)
            assert check_graph(g) is None
            claimed=record['certificate'];actual=frontier_test(g)
            assert actual['status'] in ('EXCLUDED_EMPTY_VERTEX_DOMAIN','EXCLUDED_PROFILE_CAPACITY')
            for key,value in claimed.items():
                assert json.loads(json.dumps(actual[key]))==value,(i,j,key)
            certificates[actual['status']]+=1;replayed+=1
    assert partial_counts=={'6:517':6,'6:562':4,'6:603':48}
    assert certificates==Counter(EXCLUDED_EMPTY_VERTEX_DOMAIN=56,EXCLUDED_PROFILE_CAPACITY=2)
    files=[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
           for p in (cover_path,join_path,frontier_path)]
    return {'scope':'All occurrences of template 5602; also the C4 disjoint C3 grid closure rule.',
            'inputs':files,'core_orbits':len(orbits),'complete_boundary_cases':len(expected),
            'join_statuses':dict(Counter(r['status'] for r in records.values())),
            'partial36_counts':partial_counts,'frontier_statuses':dict(certificates),
            'elementary_certificates_replayed':replayed,
            'coverage_checked':True,'whole_template_excluded':True,
            'uses_E3':True,'fixed_Gram_required':False,'automorphism_assumption':False,
            'global_Conway_exclusion':False,
            'completeness_argument':'notes/COEUR_HUIT_SOMMETS_5602_2026_10_19.txt',
            'reader_scope':__doc__}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cover',type=Path,required=True)
    p.add_argument('--join',type=Path,required=True)
    p.add_argument('--frontier',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();assert not a.output.exists();resources=limit_research_process(1)
    out=build_manifest(a.cover,a.join,a.frontier);out['resources']=resources
    atomic_json_write(a.output,out)
    print(json.dumps(out),flush=True)


if __name__=='__main__':main()
