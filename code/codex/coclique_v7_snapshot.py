"""Record the V7 results, scopes, sources and solver resource histories."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/'data/codex_coclique_defects'


def snapshot():
    runs = []
    for name in ('global_columns_v7', 'global_triangles_v7', 'global_center_v7', 'global_integrated_v7'):
        folder = DATA/name
        if not (folder/'config.json').exists(): continue
        config = json.loads((folder/'config.json').read_text(encoding='utf-8'))
        result = json.loads((folder/'result.json').read_text(encoding='utf-8')) if (folder/'result.json').exists() else {}
        assert hashlib.sha256((folder/'source.py').read_bytes()).hexdigest() == config['source_sha256']
        observations = [json.loads(line) for line in (folder/'resources.jsonl').read_text().splitlines() if line]
        log = (folder/'search.log').read_text(encoding='utf-8')
        model_updates = re.findall(r'#Model\s+([\d.]+)s var:(\d+)/(\d+) constraints:(\d+)/(\d+)', log)
        runs.append(dict(name=name, config=config,
            status=result.get('status', 'NO_FINAL_RESULT'),
            result={k: v for k, v in result.items() if k not in ('B', 'D', 'residual_degree_graph', 'response_stats')},
            resource_samples=len(observations), last_resource_sample=observations[-1] if observations else None,
            peak_working_set=max((r['peak_working_set'] or 0 for r in observations), default=0),
            model_updates=len(model_updates), last_model_update=model_updates[-1] if model_updates else None,
            cautions=['No final result does not by itself establish that a process is still alive',
                      'Response counters are not the sum of all worker counters',
                      'Eliminated auxiliary variables are not an exclusion percentage']))
    artifacts = list((DATA/'affine_completion_v7').glob('*.json'))
    artifacts += [ROOT/'code/codex'/name for name in ('coclique_affine_completion.py',
        'check_coclique_affine_completion.py', 'coclique_column_coexistence.py', 'check_coclique_rook_balance.py')]
    hashes = {str(path.relative_to(ROOT)).replace('\\', '/'): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in artifacts}
    manifest = dict(captured_utc=datetime.now(timezone.utc).isoformat(), runs=runs, sha256=hashes,
        results=[
            'Exact affine completion: delta binary free edges and delta selected quadratic equations suffice',
            'Petersen residual coexistence reduces to x+y+z=0 mod2; not a Conway exclusion',
            'A rook R satisfies sum_R q=15-7|R intersect C| for a 21-coclique',
            'No rook contains the distinguished H in any (0,2) graph',
            'Lou-Murin theorem2.1 strengthens the rook-center cuts; external dependency explicitly retained',
            'A common neighbour of all four X has a forced location, negative-edge incidence and four distinct mates'],
        frontier='No proof excluding all (0,2), alpha21 or Conway99; candidate D and any final completions require exact checking',
        old_solver_state='Historic co-Heawood solver11428 and observer17796 stopped when the PC was shut down')
    (DATA/'v7_run_manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(captured_utc=manifest['captured_utc'], runs=[dict(name=r['name'], status=r['status'],
        peak_working_set=r['peak_working_set']) for r in runs])), flush=True)


if __name__ == '__main__': snapshot()
