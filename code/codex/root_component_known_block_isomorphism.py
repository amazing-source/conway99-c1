"""Transport a 2K2 continuation obstruction by exact root/letter relabelling.

The permutation fixes the shared root 0, preserves {1,2}, and permutes
the two grid root pairs {3,4},{5,6}. Arbitrary flips within each upper
letter pair are allowed. Thus it preserves H01=-H02 and all three grid
assumptions, as well as the complete set of 84 lower labels. A supplied
isomorphism is checked directly on labels and every known adjacency.
"""

import argparse
import gzip
import hashlib
from itertools import permutations, product
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import limit_research_process, atomic_json_write


def root_permutations():
    for rp in permutations(range(7)):
        if rp[0]!=0 or set(rp[1:3])!={1,2}:
            continue
        if {frozenset(rp[i] for i in (3,4)),frozenset(rp[i] for i in (5,6))}!={frozenset((3,4)),frozenset((5,6))}:
            continue
        yield rp


def mappings(labels):
    target={tuple(q):i for i,q in enumerate(labels)}
    for rp in root_permutations():
        for flips in product(range(2),repeat=7):
            lp=[2*rp[l//2]+((l%2)^flips[l//2]) for l in range(14)]
            known=[target[tuple(sorted(lp[l] for l in q))] for q in labels]
            yield {'root_permutation':rp,'letter_permutation':lp,'known_vertex_permutation':known}


def transform(rows, mapping):
    vp=mapping['known_vertex_permutation']; result=[0]*len(rows)
    for u,row in enumerate(rows):
        mask=row
        while mask:
            bit=mask&-mask;mask^=bit
            result[vp[u]]|=1<<vp[bit.bit_length()-1]
    return tuple(result)


def check(source,target,mapping):
    rp=tuple(mapping['root_permutation']);lp=mapping['letter_permutation'];vp=mapping['known_vertex_permutation']
    assert rp in tuple(root_permutations())
    assert sorted(lp)==list(range(14)) and all(lp[l]//2==rp[l//2] for l in range(14))
    assert sorted(vp)==list(range(len(source['rows'])))
    assert len(source['rows'])==len(target['rows'])
    assert all(sorted(lp[l] for l in q)==target['known_labels'][vp[i]] for i,q in enumerate(source['known_labels']))
    assert transform(source['rows'],mapping)==tuple(target['rows'])
    assert {tuple(sorted(lp[l] for l in q)) for q in source['outside_labels']}=={tuple(q) for q in target['outside_labels']}
    return True


def classes(blocks):
    targets={}
    for i,b in enumerate(blocks):targets.setdefault(tuple(b['rows']),[]).append(i)
    covered=set();groups=[]
    for i,b in enumerate(blocks):
        if i in covered:continue
        members={i:None};covered.add(i)
        for m in mappings(b['known_labels']):
            for j in targets.get(transform(b['rows'],m),[]):
                if j in covered:continue
                assert check(b,blocks[j],m)
                members[j]=m;covered.add(j)
        groups.append({'representative':i,'members':[{'case_index':j,'mapping_from_representative':m} for j,m in sorted(members.items())]})
    return groups


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('lab_source',type=Path);p.add_argument('catalogue',type=Path)
    p.add_argument('boundary_dir',type=Path);p.add_argument('--output-dir',type=Path,required=True)
    a=p.parse_args();resources=limit_research_process(1)
    assert not a.output_dir.exists();a.output_dir.mkdir(parents=True)
    raw=a.lab_source.read_bytes();source=raw.decode('utf-8-sig');marker='\nOUT = next('
    assert source.count(marker)==1
    before=sys.argv[:];sys.argv=[str(a.lab_source),str(Path(__file__).resolve().parent),'2K2','unused','0','0']
    ns={'__name__':'lab_2k2_materialize','__file__':str(a.lab_source)}
    try:exec(compile(source.split(marker)[0],str(a.lab_source),'exec'),ns)
    finally:sys.argv=before
    catalogue_raw=a.catalogue.read_bytes();catalogue=json.loads(catalogue_raw)
    (a.output_dir/'catalogue.json').write_bytes(catalogue_raw)
    (a.output_dir/'lab_source.py.gz').write_bytes(gzip.compress(raw,mtime=0))
    covers={};blocks=[]
    for record in catalogue:
        ci=record['core_index'];filename='core_%03d.json.gz'%ci
        if ci not in covers:
            cover_raw=(a.boundary_dir/filename).read_bytes()
            covers[ci]=json.loads(gzip.decompress(cover_raw))
            (a.output_dir/filename).write_bytes(cover_raw)
        cover=covers[ci];index=record['boundary_index'];hx=cover['boundaries_hex'][index]
        assert cover['status']=='COMPLETE_BOUNDARY_COVER' and hx==record['boundary_hex'] and cover['core_index']==ci
        rows=ns['materialize'](cover['core'],tuple(bytes.fromhex(hx)),record['attachment'],record['sigma'])
        blocks.append({**record,'rows':rows,'known_labels':[list(q) for q in ns['LABELS']],
                       'outside_labels':[list(q) for q in ns['OUTSIDE']]})
    groups=classes(blocks)
    atomic_json_write(a.output_dir/'cases.json',{'source_sha256':hashlib.sha256(raw).hexdigest(),
                     'catalogue_sha256':hashlib.sha256(catalogue_raw).hexdigest(),'cases':blocks})
    atomic_json_write(a.output_dir/'isomorphisms.json',{'scope':'Family-preserving relabellings of known blocks; no new SAT search.',
                     'resources':resources,'permitted_root_permutations':len(list(root_permutations())),
                     'letter_flips_per_root_permutation':128,'classes':groups})
    print(json.dumps({'cases':len(blocks),'classes':[[m['case_index'] for m in g['members']] for g in groups]}))


if __name__=='__main__':main()
