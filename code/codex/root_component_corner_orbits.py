"""Factor a corner table through auxiliary square orientations.

All eight square orientations remain existentially available, independently
in each rectangle. This is a local table encoding, not a normalization of
graph vertices and not an assumed graph automorphism. Completeness of every
table orbit is checked before replacing it by its canonical representative.
"""

import argparse
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process
from root_component_low_budget_transport import digest

CORNER_PAIRS = tuple(combinations(range(4), 2))
SQUARE_ORIENTATIONS = tuple(sorted({tuple(((i >> 1) | ((i & 1) << 1) if swap else i) ^ mask
                                         for i in range(4))
                                    for swap in (False, True) for mask in range(4)}))
ROW_MAPS = tuple(tuple([0]+[1+i for i in p]+[5+CORNER_PAIRS.index(tuple(sorted((p[i],p[j]))))
                                                   for i,j in CORNER_PAIRS]) for p in SQUARE_ORIENTATIONS)
assert len(SQUARE_ORIENTATIONS) == 8
assert all((i^j).bit_count() == (p[i]^p[j]).bit_count()
           for p in SQUARE_ORIENTATIONS for i,j in CORNER_PAIRS)


def transforms(row):
    return {tuple(row[i] for i in mapping) for mapping in ROW_MAPS}


def compress(record, progress=None):
    result = deepcopy(record)
    counts = []
    for ti, table in enumerate(result['corner_signature_tables']):
        original = {tuple(row) for row in table['rows']}
        assert len(original) == len(table['rows'])
        canonical = set()
        while original:
            row = original.pop()
            orbit = transforms(row)
            assert orbit-{row} <= original, 'Corner table not closed under all square orientations.'
            original.difference_update(orbit)
            canonical.add(min(orbit))
        counts.append({'rectangle': table['rectangle'], 'before': len(table['rows']), 'after': len(canonical)})
        table['rows'] = sorted(map(list, canonical))
        table['encoding'] = 'existential_square_orientations_v1'
        if progress:
            progress(ti, counts[-1])
    result['corner_orientation_factorization'] = {
        'scope': __doc__, 'all_orbits_closed': True,
        'square_orientations': [list(p) for p in SQUARE_ORIENTATIONS], 'rectangle_counts': counts,
        'before': sum(c['before'] for c in counts), 'after': sum(c['after'] for c in counts)}
    return result


def add_factored_table(model, selector, corner_selectors, corners, graph, table):
    assert table['encoding'] == 'existential_square_orientations_v1'
    orientation = model.new_int_var(0,7,f"square_orientation_{table['rectangle']}")
    old_states = [corner_selectors[w] for w in corners]
    old_edges = [graph[corners[i]][corners[j]] for i,j in CORNER_PAIRS]
    normalized_states = []
    normalized_edges = []
    for i in range(4):
        state = model.new_int_var(0,len(table['catalog'])-1,f'square_state_{corners[i]}')
        model.add_element(orientation,[old_states[p[i]] for p in SQUARE_ORIENTATIONS],state)
        normalized_states.append(state)
    for ei,(i,j) in enumerate(CORNER_PAIRS):
        edge = model.new_bool_var(f'square_edge_{corners[0]}_{ei}')
        model.add_element(orientation,[old_edges[CORNER_PAIRS.index(tuple(sorted((p[i],p[j]))))]
                                       for p in SQUARE_ORIENTATIONS],edge)
        normalized_edges.append(edge)
    model.add_allowed_assignments([selector]+normalized_states+normalized_edges,table['rows'])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cover',type=Path,required=True)
    p.add_argument('--indices',type=int,nargs='+',required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args(); resources=limit_research_process(1)
    assert not a.output.exists()
    source=json.loads(a.cover.read_text(encoding='utf-8-sig'))
    start=time.process_time()
    for record in source['records']:
        if record['template_index'] not in a.indices:continue
        index=record['template_index']
        transformed=compress(record,lambda i,counts: print(json.dumps({'template_index':index,
            'rectangle_processed':i+1,**counts,'cpu_seconds':time.process_time()-start}),flush=True))
        record.clear();record.update(transformed)
    source['corner_factorization']={'scope':__doc__,'source_cover':str(a.cover),
        'source_cover_sha256_lf':digest(a.cover),'indices':a.indices,
        'resources':resources,'cpu_seconds':time.process_time()-start,'newly_excluded_grams':0}
    atomic_json_write(a.output,source)
    print(json.dumps({'status':'COMPLETE','cpu_seconds':time.process_time()-start,
        'counts':{r['template_index']: {'before':r['corner_orientation_factorization']['before'],
                                       'after':r['corner_orientation_factorization']['after']}
                  for r in source['records'] if r['template_index'] in a.indices}}),flush=True)


if __name__=='__main__':main()
