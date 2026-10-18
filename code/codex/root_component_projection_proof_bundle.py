"""Bundle already checked projection proofs without rerunning the solvers.

The manifest binds each exact CNF and DRAT to its recorded successful check.
This certifies unsatisfiability of the encoded necessary projection; the
mathematical reduction and the upstream Gram cover remain separate inputs.
"""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--summaries', type=Path, nargs='+', required=True)
    parser.add_argument('--projection-report', type=Path, required=True)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    args = parser.parse_args()
    limit_research_process(1)
    assert not args.archive.exists() and not args.manifest.exists()
    projection = json.loads(args.projection_report.read_text(encoding='utf-8-sig'))
    expected = set(projection['excluded_gram_indices'])
    seen = set(); entries = []; members = []
    for path in args.summaries:
        summary = json.loads(path.read_text(encoding='utf-8-sig'))
        assert summary['template_index'] == projection['template_index']
        assert summary['root_order'] == projection['root_order'] == 'weighted_prisms_grids'
        assert summary['root_prism_budget'] == projection['root_choice']['root_prism_budget']
        assert summary['source_gram_cover_sha256_lf'] == projection['source_gram_cover_sha256_lf']
        for case in summary['cases']:
            gi = case['gram_index']
            assert gi in expected and gi not in seen
            assert case['status'] == 'UNSAT' and case['checked_drat']
            assert case['solver_exit_code'] == 20 and case['checker_exit_code'] == 0
            seen.add(gi); entry = dict(case); files = []
            paths = [Path(case[key]) for key in ('cnf', 'proof', 'solver_log', 'checker_log')]
            paths.append(Path(case['cnf']).with_suffix('.encoding.json'))
            for source in paths:
                data = source.read_bytes(); sha = digest(data)
                if source == Path(case['cnf']):
                    assert sha == case['cnf_sha256']
                if source == Path(case['proof']):
                    assert sha == case['proof_sha256']
                if source == Path(case['checker_log']):
                    assert b's VERIFIED' in data
                name = f'gram_{gi}/{source.name}'
                members.append((name, data))
                files.append({'path': name, 'sha256': sha, 'bytes': len(data)})
            entry['archived_files'] = files; entries.append(entry)
    assert seen == expected, 'Do not publish an incomplete proof bundle.'
    manifest = {'scope': __doc__, 'template_index': projection['template_index'],
                'root_order': projection['root_order'],
                'root_prism_budget': projection['root_choice']['root_prism_budget'],
                'excluded_gram_indices': sorted(seen), 'all_drat_checked': True,
                'usable_in_arbitrary_low_budget_root_frontier': False,
                'source_projection': str(args.projection_report),
                'source_projection_sha256': digest(args.projection_report.read_bytes()),
                'solver_cpu_seconds_total': sum(e['solver_cpu_seconds'] for e in entries),
                'cases': sorted(entries, key=lambda e: e['gram_index'])}
    members.append(('manifest.json', (json.dumps(manifest, indent=2)+'\n').encode()))
    args.archive.parent.mkdir(parents=True, exist_ok=True)
    with args.archive.open('wb') as raw:
        with gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode='w|') as archive:
                for name, data in sorted(members):
                    info = tarfile.TarInfo(name); info.size = len(data)
                    info.mode = 0o644; info.mtime = 0
                    archive.addfile(info, io.BytesIO(data))
    manifest['archive'] = str(args.archive)
    manifest['archive_sha256'] = digest(args.archive.read_bytes())
    manifest['archive_bytes'] = args.archive.stat().st_size
    atomic_json_write(args.manifest, manifest, indent=2)
    print(json.dumps({k: manifest[k] for k in ('excluded_gram_indices', 'all_drat_checked',
                     'archive_bytes', 'solver_cpu_seconds_total')}), flush=True)


if __name__ == '__main__':
    main()
