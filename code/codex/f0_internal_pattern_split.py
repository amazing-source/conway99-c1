"""Split internal F0 mass-six pairs by the intersection of negative triangles."""
import gzip
import json
import sys

from higher_census_minima import ROOT
from f0_collision_patterns import F0Representatives


def main():
    with gzip.open(ROOT/'data/codex_f0_mass6_p6_patterns.json.gz','rt') as stream:
        source = json.load(stream)
    reps = F0Representatives(source['core_adjacency'],source['profiles'],6,6)
    out = []
    nonzero = [0]*4
    for row in source['patterns']:
        counts = [reps.count(row['profiles'],row['edges'],d) for d in range(4)]
        assert sum(counts) == row['counts']['F0']
        assert counts[2:] == [0,0]
        nonzero = [a+int(bool(b)) for a,b in zip(nonzero,counts)]
        out.append(dict(row,counts={'disjoint_negative_triangles':counts[0],
                                    'shared_rung_apex':counts[1]}))
    report = dict(source,patterns=out,nonzero_patterns_by_intersection=nonzero)
    path = ROOT/'data/codex_f0_internal_pattern_split.json.gz'
    if '--verify-only' in sys.argv:
        with gzip.open(path,'rt') as stream: assert json.load(stream) == report
    else:
        with gzip.GzipFile(filename=path,mode='wb',mtime=0) as stream:
            stream.write(json.dumps(report).encode())
    print('Verified split on',len(out),'patterns;',nonzero,flush=True)


if __name__ == '__main__':
    main()
