"""Read saved CP-SAT logs; do not confuse search counters with proofs."""
from datetime import datetime, timezone
from pathlib import Path
import argparse
import json
import re


def table(lines, title):
    for index, line in enumerate(lines):
        if not line.startswith(title+' '):
            continue
        headers = re.split(r'\s{2,}', line.strip())[1:]
        rows = {}
        for row in lines[index+1:]:
            match = re.match(r"\s*'([^']+)':\s+(.*)", row)
            if not match:
                break
            values = match[2].split()
            assert len(values) == len(headers), (title, headers, values)
            def number(value):
                return int(value.replace("'", '')) if re.fullmatch(r"[0-9']+", value) else value
            rows[match[1]] = dict(zip(headers, map(number, values)))
        return rows
    return {}


def diagnose(folder):
    config = json.loads((folder/'config.json').read_text(encoding='utf-8'))
    result_file = folder/'result.json'
    result = json.loads(result_file.read_text(encoding='utf-8')) if result_file.exists() else {}
    log = (folder/'search.log').read_text(encoding='utf-8')
    lines = log.splitlines()
    observations = [json.loads(line) for line in (folder/'resources.jsonl').read_text().splitlines() if line]
    updates = [dict(seconds=float(t), variables_left=int(v), variables_total=int(n),
                    constraints_left=int(c), constraints_total=int(m))
               for t, v, n, c, m in re.findall(
                   r'#Model\s+([\d.]+)s var:(\d+)/(\d+) constraints:(\d+)/(\d+)', log)]
    buckets = []
    for second in range(300, int(config['seconds'])+1, 300):
        earlier = [u for u in updates if u['seconds'] <= second]
        buckets.append(dict(at_seconds=second, last_reported_model=earlier[-1] if earlier else None))
    start = re.search(r'Starting search at ([\d.]+)s', log)
    search, clauses, sat = (table(lines, name) for name in ('Search stats', 'Clauses shared', 'SAT stats'))
    lp_rows = {}
    for match in re.finditer(r"^\s*'([^']+)':\s+([\d']+) rows, ([\d']+) columns, ([\d']+) entries", log, re.M):
        lp_rows[match[1]] = dict(zip(('rows', 'columns', 'entries'),
                                   (int(value.replace("'", '')) for value in match.groups()[1:])))
    return dict(name=folder.name, status=result.get('status', 'NO_FINAL_RESULT'),
                seconds=result.get('seconds'), workers=config['workers'],
                scope=config['scope'], ignored_subsolvers=config.get('ignored_subsolvers', []),
                actual_portfolio=[line for line in lines if re.match(r'\d+ .*subsolvers:', line)],
                search_start_seconds=float(start[1]) if start else None,
                search_stats=search, clauses_shared=clauses, sat_stats=sat,
                lp_dimensions=lp_rows, lp_stats=table(lines, 'Lp stats'),
                shared_bounds=table(lines, 'Improving bounds shared'),
                total_worker_conflicts=sum(row['Conflicts'] for row in search.values()) if search else None,
                model_update_count=len(updates), model_samples_5min=buckets,
                last_model_update=updates[-1] if updates else None,
                final_resource=observations[-1] if observations else None,
                peak_working_set=max((x['peak_working_set'] or 0 for x in observations), default=0),
                persisted_learned_clause_database=False,
                cautions=['UNKNOWN is not a nonexistence certificate',
                          'Counters do not measure the fraction of graphs excluded',
                          'Worker conflicts measure activity, not comparative effectiveness',
                          'Different models and time budgets prevent a controlled speed comparison',
                          'Shared clauses are exchanged within this run, not saved as a reusable database'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    runs = [diagnose(args.data/name) for name in
            ('global_columns_v7', 'global_triangles_v7', 'global_center_v7', 'global_integrated_v7')]
    report = dict(captured_utc=datetime.now(timezone.utc).isoformat(), runs=runs,
                  purpose='Empirical calibration evidence, not a mathematical exclusion or progress percentage')
    args.output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps([dict(name=r['name'], status=r['status'], conflicts=r['total_worker_conflicts'],
                          last_model_update=r['last_model_update'], lp_dimensions=r['lp_dimensions'])
                      for r in runs]), flush=True)
