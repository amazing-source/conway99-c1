"""Assemble finite K3 coverage; never certify omitted or nonexcluded borders.

This checks coverage, immutable input hashes and presence of checked RUP
certificates. It does not repeat the mathematical search. Use a dedicated
results directory, without diagnostic files that contain surviving blocks.
"""

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process


def read(path):
    raw=path.read_bytes()
    if path.suffix=='.gz':raw=gzip.decompress(raw)
    return json.loads(raw)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assemble(cover_directory,results_directory,colours_path,orbits_path,allow_partial=False):
    representatives=read(orbits_path)['representatives']
    colour_records={r['core_index']:r for r in read(colours_path)['results']}
    covers={};seen={};sources={};excluded_cores=[];missing_covers=[]
    for ci in representatives:
        path=cover_directory/f'core_{ci:03d}.json.gz'
        if not path.exists():missing_covers.append(ci);continue
        c=read(path);assert c['core_index']==ci
        sources[str(path)]=digest(path)
        if c['status']=='EXCLUDED_Q12_COLOUR_FACTORS':
            r=colour_records[ci]
            assert r['status']=='EXCLUDED_COLOUR_FACTORS' and not r['colourings']
            assert r['linear_certificate']
            excluded_cores.append(ci)
        else:
            assert c['status']=='COMPLETE_20_VERTEX_COVER'
            assert len(c['boundaries_hex'])==c['boundary_count']
            covers[ci]=c;seen[ci]=bytearray(c['boundary_count'])
    totals=Counter();verdicts=Counter();proofs=0;files=[]
    for path in sorted(results_directory.iterdir()):
        if not (path.name.endswith('.json') or path.name.endswith('.json.gz')):continue
        data=read(path);ci=data['core_index'];assert ci in covers
        cover_path=cover_directory/f'core_{ci:03d}.json.gz'
        assert data['source_sha256']==digest(cover_path)
        assert data['total_boundaries']==covers[ci]['boundary_count']
        for record in data['cases']:
            bi=record['boundary_index'];r=record['result']
            assert 0<=bi<len(seen[ci]) and not seen[ci][bi],(ci,bi,'duplicate or invalid')
            assert record['boundary_hex']==covers[ci]['boundaries_hex'][bi]
            assert r['status']=='EXCLUDED_BY_FACTOR_JOIN_AND_FRONTIER',(ci,bi,r['status'])
            assert r['is_complete_graph'] is False and r.get('witness') is None
            certs=r.get('frontier_certificates',[])
            assert r['counts'].get('valid_partial24',0)==len(certs),(ci,bi)
            for c in certs:
                certificate=c['certificate'];status=certificate['status']
                assert status.startswith('EXCLUDED_')
                verdicts[status]+=1
                if status=='EXCLUDED_PROFILE_SELECTION_UNSAT':
                    assert certificate['proof_check']['empty_clause_verified']
                    assert 'rup_proof' in c
                    proofs+=1
            totals.update(r['counts']);seen[ci][bi]=1
        files.append({'path':str(path),'sha256':digest(path),'core':ci,'covered':len(data['cases']),
                      'program_sha256':data.get('program_sha256'),
                      'inclusion_filter_sha256':data.get('inclusion_filter_sha256'),
                      'triplet_filter_sha256':data.get('triplet_filter_sha256'),
                      'profile_solver_sha256':data.get('profile_solver_sha256')})
    covered=sum(sum(flags) for flags in seen.values());expected=sum(map(len,seen.values()))
    complete=not missing_covers and covered==expected
    if not allow_partial:
        assert complete,{'covered':covered,'expected_from_available_covers':expected,'missing_core_covers':missing_covers}
    return {'scope':__doc__,'family':'H01=-H02 nonzero; grids Q12,Q45,Q46,Q56; all other rectangles free',
            'uses_E3_in_core_catalogue':True,'fixed_Gram_required':False,'graph_symmetry_required':False,
            'core_representatives':representatives,'cores_excluded_analytically':excluded_cores,
            'missing_core_covers':missing_covers,'expected_from_available_covers':expected,
            'covered_borders':covered,'coverage_by_core':{str(ci):{'expected':len(f),'covered':sum(f)} for ci,f in seen.items()},
            'search_counts':dict(totals),'frontier_verdicts':dict(verdicts),'checked_rup_proofs':proofs,
            'source_sha256':{**sources,str(colours_path):digest(colours_path),str(orbits_path):digest(orbits_path)},
            'result_files':files,'family_excluded':complete,'global_Conway_exclusion':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cover-directory',type=Path,required=True)
    parser.add_argument('--results-directory',type=Path,required=True)
    parser.add_argument('--colour-factors',type=Path,required=True)
    parser.add_argument('--core-orbits',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--allow-partial',action='store_true')
    args=parser.parse_args();assert not args.output.exists()
    limit_research_process(1)
    out=assemble(args.cover_directory,args.results_directory,args.colour_factors,args.core_orbits,args.allow_partial)
    atomic_json_write(args.output,out,indent=2)
    print(json.dumps({k:out[k] for k in ('expected_from_available_covers','covered_borders','missing_core_covers','checked_rup_proofs','family_excluded')}))
