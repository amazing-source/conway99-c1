"""Assemble complete coverage of the 1328 x 4 touching-grid positions.

Checks coverage, source hashes and terminal statuses. This is a proof
manifest, not an independent re-enumeration of the mathematical search.
It refuses partial files, missing positions and UNKNOWN verdicts.
"""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path


def manifest(cover_path,cores_path,results_path):
    cover=json.loads(cover_path.read_text(encoding='utf8'))
    cores=json.loads(cores_path.read_text(encoding='utf8'))
    data=json.loads(results_path.read_text(encoding='utf8'))
    orbits=cover.get('orbit_reduction',cover)['orbits']
    expected={(oi,bi,a) for oi,o in enumerate(orbits)
              for bi,_ in enumerate(o['boundaries']['cases']) for a in range(4)}
    assert len(expected)==5312 and len(cores)==114
    hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cover_path,cores_path,results_path)}
    assert data['sources']=={str(p):hashes[str(p)] for p in (cover_path,cores_path)}
    seen=set();verdicts=Counter();counts=Counter();cpu=0;by_orbit=Counter()
    for record in data['cases']:
        result=record['result'];key=(record['orbit'],record['boundary_index'],result['centre'])
        assert key in expected and key not in seen,key
        assert result['status'] in ('EXCLUDED_BY_INTEGER_MARGINS','EXCLUDED_BY_EXHAUSTIVE_JOIN'),key
        assert result['uses_E3'] and result['is_complete_graph'] is False
        seen.add(key);verdicts[result['status']]+=1;by_orbit[key[0]]+=1
        counts.update(result.get('counts',{}));cpu+=result['cpu_seconds']
        n=result.get('counts',{}).get('valid_partial36',0)
        certificates=result.get('frontier_certificates',[])
        assert n==len(certificates),key
        assert all(c['certificate']['status'].startswith('EXCLUDED_') for c in certificates),key
        assert result.get('witness') is None,key
    assert seen==expected,{'missing':len(expected-seen),'seen':len(seen)}
    assert data['counts']==dict(verdicts)
    return {'scope':__doc__,'source_sha256':hashes,'expected_positions':len(expected),
            'covered_positions':len(seen),'positions_by_core_orbit':dict(by_orbit),
            'verdicts':dict(verdicts),'search_counts':dict(counts),'cpu_seconds':cpu,
            'uses_E3':True,'fixed_Gram_required':False,'symmetry_of_sought_graph_required':False,
            'family_excluded':True,'global_Conway_exclusion':False,
            'family':'Nonzero opposite disjoint columns, three complementary grids, two adjacent X grids and two nongrid X rectangles.',
            'program_versions':data.get('program_versions',[]),
            'prefix_provenance':{'cases':1823,'commit':'5f60e37d',
                'note':'Production checkpoint resumed with the necessary 27-opposition-profile cut; no position omitted.'}}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cover',type=Path,required=True)
    p.add_argument('--pair-cores',type=Path,required=True)
    p.add_argument('--results',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();assert not args.output.exists()
    out=manifest(args.cover,args.pair_cores,args.results)
    args.output.write_text(json.dumps(out,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:out[k] for k in ('covered_positions','verdicts','search_counts','family_excluded','global_Conway_exclusion')}))


if __name__=='__main__':main()
