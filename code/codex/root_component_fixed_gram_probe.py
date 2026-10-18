"""Microscope for a supplied Gram: binary realization with shared edges.

Uses the established signature_joint model with both projectors, four-corner
tables, short integral eigenvectors and optional Gamma H=-4H equations.
The supplied Gram cover and the model both use root prism budget51.
A single fixed-Gram verdict never excludes its entire template.
"""

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sympy as sp
from root_component_resources import limit_research_process, atomic_json_write
from root_component_signature_joint import solve


def read(path):
    blob = path.read_bytes()
    return json.loads(gzip.decompress(blob) if path.suffix == '.gz' else blob)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--catalogue', type=Path, required=True)
    p.add_argument('--index', type=int, required=True)
    p.add_argument('--bundle', type=Path, required=True)
    p.add_argument('--grams', type=int, nargs='+', required=True)
    p.add_argument('--seconds', type=float, default=10)
    p.add_argument('--eigen', action='store_true')
    p.add_argument('--layer', type=int, choices=range(5), default=0)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    assert not a.output.exists()
    resources = limit_research_process(1)
    catalogue = read(a.catalogue)
    template = catalogue.get('open', catalogue.get('survivors'))[a.index]['template']
    cover = read(a.bundle)
    assert cover.get('template_index', a.index) == a.index
    edges = cover.get('edges', cover.get('edge_order'))
    assert template['nongrid_edges'] == edges
    result = dict(scope=__doc__, template_index=a.index, source_bundle=str(a.bundle),
                  source_sha256=hashlib.sha256(a.bundle.read_bytes()).hexdigest(),
                  resources=resources, cases=[], global_conway_exclusion=False,
                  whole_template_excluded=False, portable_unsat_proof=False)
    for gi in a.grams:
        print(json.dumps(dict(stage='building', gram_selector=gi, eigen=a.eigen, layer=a.layer)), flush=True)
        start = time.process_time()
        case = solve(template, sp.Matrix(cover['grams'][gi]), a.seconds, layer=a.layer,
                     eigen=a.eigen, mate_normalize=True, corners=True, short_vectors=True,
                     upper_projector=True, cpu_time=True, workers=1)
        internal_edges = 84 - sum(cover['grams'][gi][i][i] for i in range(len(edges)))//2
        case.update(gram_selector=gi, total_cpu_seconds=time.process_time()-start,
                    internal_rectangle_edges=internal_edges,
                    root_prism_budget_redundant=internal_edges <= 51)
        result['cases'].append(case)
        atomic_json_write(a.output, result)
        print(json.dumps({k: v for k, v in case.items() if k != 'relaxation_edges'}), flush=True)


if __name__ == '__main__':
    main()
