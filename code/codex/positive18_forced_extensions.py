"""Reduce the new 17-point positive-kernel cores using forced outside cells.

If phi=(2,1^16) and E_-4 phi=0, every outside vertex either sees just the
weight-two centre, or exactly two weight-one vertices. All multiplicities
are forced by the common-neighbour equations. No completion is claimed.
"""
from collections import Counter
from itertools import combinations
import json
import time

import numpy as np

from higher_census_minima import ROOT
from higher_vertex_census import ir_orders
from twisted_prism_core import is_psd_exact, negative_witness
from twisted_prism_extension import projectors, spectral_masks


def main():
    started=time.monotonic()
    source=json.loads((ROOT/'data/codex_mill_cubic_positive18.json').read_text())
    unique={}
    for row in source['prismfree_cores']:
        code,_=ir_orders(tuple(row['adjacency_bits']))
        if code not in unique:unique[code]={**row,'labelled_multiplicity':0}
        unique[code]['labelled_multiplicity']+=1
    print('Nonisomorphic rooted cores:',len(unique),flush=True)
    records=[]
    for code,row in sorted(unique.items()):
        graph=row['adjacency_bits']
        a=np.array([[(mask>>j)&1 for j in range(17)] for mask in graph],dtype=np.int64)
        phi=np.array([1]*16+[2],dtype=np.int64)
        assert np.array_equal(a@phi,3*phi+2)
        cells=[{'neighbours':[16],'count':6}]
        for u,v in combinations(range(16),2):
            deficit=2-int(a[u,v])-int(a[u]@a[v])
            assert deficit>=0
            if deficit:cells.append({'neighbours':[u,v],'count':deficit})
        assert sum(c['count'] for c in cells)==82
        masks=np.array([[int(v in c['neighbours']) for v in range(17)] for c in cells],dtype=np.int64)
        numbers=np.array([c['count'] for c in cells],dtype=np.int64)
        assert np.array_equal(numbers@masks,14-a.sum(axis=0))
        record={**row,'canonical_code':code,'forced_cells':cells}
        obstruction=None
        for i,(gram,diagonal,constant,coefficient) in enumerate(projectors(a,14)):
            if not is_psd_exact(gram)[0]:
                obstruction={'kind':'core_projector','projector':i,'witness':negative_witness(gram)}
                break
        if obstruction is None:
            kept={tuple(x) for x in spectral_masks(a,masks,14).tolist()}
            missing=next((i for i,x in enumerate(masks.tolist()) if tuple(x) not in kept),None)
            if missing is not None:
                for i,(gram,diagonal,constant,coefficient) in enumerate(projectors(a,14)):
                    g=np.zeros((18,18),dtype=np.int64)
                    g[:17,:17]=gram;g[-1,-1]=diagonal
                    g[-1,:17]=constant+coefficient*masks[missing]
                    g[:17,-1]=g[-1,:17]
                    if not is_psd_exact(g)[0]:
                        obstruction={'kind':'forced_vertex_projector','projector':i,
                                     'neighbours':cells[missing]['neighbours'],
                                     'forced_count':cells[missing]['count'],
                                     'witness':negative_witness(g)}
                        break
                assert obstruction is not None
        record['status']='excluded_exact' if obstruction else 'forced_cells_unresolved'
        if obstruction:record['obstruction']=obstruction
        records.append(record)
    counts=dict(Counter(r['status'] for r in records))
    report={'scope':__doc__,'labelled_prismfree_cores':len(source['prismfree_cores']),
            'nonisomorphic_cores':len(records),'counts':counts,'records':records,
            'seconds':time.monotonic()-started}
    (ROOT/'data/codex_positive18_forced_extensions.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'types':len(records),'counts':counts,'seconds':round(report['seconds'],2)}),flush=True)


if __name__=='__main__':main()
