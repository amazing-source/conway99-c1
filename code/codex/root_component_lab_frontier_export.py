"""Export surviving known blocks of one LAB boundary without running SAT.

Read the LAB implementation in memory and stop before its batch driver.
This supplies new mathematical filters with actual hard blocks; it does
not repeat the peer's SAT runs or alter any LAB file.
"""

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import limit_research_process


def export(lab_source, boundary_path, index, family, output):
    resources = limit_research_process(1)
    raw = Path(lab_source).read_bytes()
    source = raw.decode('utf-8-sig')
    marker = '\nOUT = next('
    assert source.count(marker) == 1, 'Inspect the changed LAB driver before exporting.'
    prefix = source.split(marker)[0]
    before = sys.argv[:]
    sys.argv = [str(lab_source), str(Path(__file__).resolve().parent), family,
                str(boundary_path), str(index), '1', '--outside-c2', '--dump=memory']
    ns = {'__name__': 'lab_frontier_export', '__file__': str(lab_source)}
    try:
        exec(compile(prefix, str(lab_source), 'exec'), ns)
    finally:
        sys.argv = before
    boundary_raw = Path(boundary_path).read_bytes()
    document = json.loads(gzip.decompress(boundary_raw))
    assert document['status'] == 'COMPLETE_BOUNDARY_COVER'
    core = document['core']; boundary = tuple(bytes.fromhex(document['boundaries_hex'][index]))
    attach = ns['Attachments'](core) if ns['Q12K'] else None
    counts = Counter(); blocks = []
    start = time.process_time()
    for attached in attach.for_boundary(boundary) if attach else [()]:
        for sigma in ns['P4'] if ns['YY'] else [None]:
            ns['DUMPED'].clear()
            rows = ns['materialize'](core, boundary, attached, sigma)
            cert = ns['frontier'](rows, True)
            counts[cert['status']] += 1
            if not cert['status'].startswith('EXCLUDED'):
                assert cert['status'] == 'PASSES_PROFILE_PROPAGATION'
                assert len(ns['DUMPED']) == 1
                block = ns['DUMPED'][0]
                block.update({'attachments': attached, 'sigma': sigma})
                blocks.append(block)
    result = {'scope': 'Surviving known blocks for mathematical analysis; no SAT calls or family exclusion.',
              'family': family, 'core_index': document['core_index'], 'boundary_index': index,
              'boundary_hex': document['boundaries_hex'][index],
              'lab_source_sha256': hashlib.sha256(raw).hexdigest(),
              'boundary_source_sha256': hashlib.sha256(boundary_raw).hexdigest(),
              'resources': resources, 'cpu_seconds': time.process_time()-start,
              'attachment_statuses': dict(counts), 'blocks': blocks}
    output = Path(output)
    assert not output.exists()
    output.write_bytes(gzip.compress(json.dumps(result, separators=(',', ':')).encode(), mtime=0))
    output.with_suffix('.source.py.gz').write_bytes(gzip.compress(raw, mtime=0))
    print(json.dumps({k: v for k, v in result.items() if k != 'blocks'}))
    print(json.dumps({'blocks': len(blocks), 'output': str(output)}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('lab_source', type=Path)
    parser.add_argument('boundary', type=Path)
    parser.add_argument('--index', type=int, required=True)
    parser.add_argument('--family', choices=('P3N', '2K2N', 'P3', '2K2'), required=True)
    parser.add_argument('--output', type=Path, required=True)
    a = parser.parse_args()
    export(a.lab_source, a.boundary, a.index, a.family, a.output)
