"""Detect the written square-defect obstruction and emit integer certificates."""

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process
from root_component_square_defect import find_obstruction, verify_certificate, squares, forbidden_states


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source', type=Path)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args(); assert not a.output.exists()
    resources = limit_research_process(1)
    raw = a.source.read_bytes()
    document = json.loads(gzip.decompress(raw) if a.source.suffix == '.gz' else raw)
    records = document.get('open', document.get('survivors', [document]))
    start = time.process_time()
    result = {'source': str(a.source), 'source_sha256': hashlib.sha256(raw).hexdigest(),
              'resources': resources, 'records': [], 'square_templates': 0,
              'templates': len(records), 'uses_Gram_cover': False, 'uses_prism_budget': False,
              'global_conway_exclusion': False}
    for i, record in enumerate(records):
        template = record.get('template', record)
        found = squares(template)
        result['square_templates'] += bool(found)
        certificate = find_obstruction(template) if found else None
        if certificate is not None:
            item = {'index': i, 'sample_index': record.get('sample_index'), 'template': template,
                    'certificate': certificate, 'verification': verify_certificate(template, certificate)}
            if 'catalogue' in record:
                banned, _ = forbidden_states(template, record['catalogue']['row_types'])
                item['forbidden_row_states'] = len(banned)
            result['records'].append(item)
        if (i+1) % 1000 == 0:
            result.update(processed=i+1, cpu_seconds=time.process_time()-start)
            atomic_json_write(a.output, result)
            print(json.dumps({k:result[k] for k in ('processed','square_templates','cpu_seconds')}), flush=True)
    result.update(processed=len(records), excluded=len(result['records']), cpu_seconds=time.process_time()-start)
    atomic_json_write(a.output, result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('records','resources')}), flush=True)


if __name__ == '__main__':
    main()
