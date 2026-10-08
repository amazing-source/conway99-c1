"""All locally admissible ten-vertex graphs of minimum degree at least three.

Necessary candidates for one binary sign support in a mass-ten kernel
vector. This does not classify cross edges or nonbinary kernel vectors.
"""
from collections import Counter
import gzip
import json
import time

from higher_census_minima import ROOT
from targeted_order10_census import admissible, canonical
from seven_vertex_census import decode


def main():
    start = time.monotonic()
    packet = json.loads((ROOT/'data/codex_census_validation_99.json').read_text())
    nine = packet['stages'][-1]
    graphs = {}
    tested = 0
    for row in nine['counts']:
        if min(row['degrees']) < 2:
            continue
        adj = tuple(row['adjacency_bits'])
        mandatory = sum(1 << i for i, mask in enumerate(adj) if mask.bit_count() == 2)
        optional = 511 ^ mandatory
        chosen = optional
        while True:
            neighbours = mandatory | chosen
            if neighbours.bit_count() >= 3:
                tested += 1
                extension = tuple(adj[i] | (((neighbours >> i) & 1) << 9) for i in range(9))+(neighbours,)
                if admissible(extension):
                    code, _ = canonical(extension)
                    graphs[code] = decode(10, code)
            if not chosen:
                break
            chosen = (chosen-1) & optional
    with gzip.open(ROOT/'data/codex_targeted_order10_census.json.gz', 'rt', encoding='utf-8') as stream:
        partial = json.load(stream)
    included = {int(name.split('_')[1]) for name in partial['parameters'] if name.startswith('C10_')}
    assert included <= graphs.keys()
    report = {'graph_types': len(graphs), 'neighbourhood_candidates_tested': tested,
              'already_in_targeted_census': len(included), 'missing_from_targeted_census': sorted(graphs.keys()-included),
              'edge_histogram': dict(Counter(sum(x.bit_count() for x in adj)//2 for adj in graphs.values())),
              'counts': [{'code': code, 'adjacency_bits': list(adj),
                          'degrees': sorted(x.bit_count() for x in adj)} for code, adj in sorted(graphs.items())],
              'seconds': round(time.monotonic()-start, 3),
              'scope': 'Exhaustive necessary graph types for binary ten-point sign supports only; cross-support compatibility and nonbinary vectors remain unaudited.'}
    (ROOT/'data/codex_mass10_support_catalogue.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print('Dense order-ten types:', len(graphs), '; included in targeted census:', len(included),
          '; seconds:', report['seconds'], flush=True)


if __name__ == '__main__':
    main()
