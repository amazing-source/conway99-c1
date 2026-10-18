"""Count and identify complete-star branches without launching any solver."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from math import prod
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_complete_star import component_parts
from root_component_resources import atomic_json_write, limit_research_process


def source_templates(data):
    if 'templates' in data:
        return [(t, {'grids': data.get('grids')}) for t in data['templates']]
    # The LAB compressed file also carries one Gram witness per template.
    # Deliberately extract the template and provenance fields only.
    return [(r['template'], {k: r[k] for k in ('grids', 'graph') if k in r})
            for r in data['open']]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('sources', type=Path, nargs='+')
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args(); limit_research_process(1)
    if args.output.exists():
        raise FileExistsError(args.output)
    records = []; sources = []
    for path in args.sources:
        raw = path.read_bytes()
        data = json.loads(gzip.decompress(raw) if path.suffix == '.gz' else raw)
        rows = source_templates(data)
        sources.append({'path': path.as_posix(), 'sha256': hashlib.sha256(raw).hexdigest(), 'templates': len(rows)})
        for i, (t, meta) in enumerate(rows):
            counts = [prod(prod(range(1, 2*len(part), 2)) for part in component_parts(t, r)) for r in range(7)]
            root = min(range(7), key=lambda r: (counts[r], r))
            records.append({'source_file': path.as_posix(), 'template_index': i, **meta,
                            'root_line': root, 'part_sizes': list(map(len, component_parts(t, root))),
                            'matching_count': counts[root], 'kernel_dimension': t['kernel_dimension']})
    histogram = dict(sorted(Counter(r['matching_count'] for r in records).items()))
    output = {'scope': __doc__, 'sources': sources, 'template_count': len(records),
              'matching_tasks': sum(r['matching_count'] for r in records),
              'matching_count_histogram': histogram, 'gram_witnesses_used': False,
              'affordable_runtime_proved': False, 'solver_launched': False, 'records': records}
    atomic_json_write(args.output, output)
    print(json.dumps({k: v for k, v in output.items() if k not in ('records', 'sources', 'scope')}))


if __name__ == '__main__':
    main()
