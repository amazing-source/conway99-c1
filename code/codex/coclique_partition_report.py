"""Summarize completed partition jobs without assigning mathematical progress."""
from collections import Counter
from datetime import datetime
from pathlib import Path
import argparse
import json
import statistics


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def summary(folder):
    plan = read(folder/'protocol.json')
    report = read(folder/'report.json')
    jobs = {}
    curves = []
    for name, result in sorted(report['results'].items()):
        path = folder/name
        if not (path/'diagnostics.json').exists():
            jobs[name] = dict(status=result.get('status','ERROR'), returncode=result['returncode'])
            continue
        diag, config = read(path/'diagnostics.json'), read(path/'config.json')
        final_result = read(path/'result.json')
        rows = [json.loads(line) for line in (path/'resources.jsonl').read_text().splitlines() if line]
        curves.append(rows)
        jobs[name] = dict(status=result['status'], seconds=result['seconds'],
                          presolve_seconds=diag['search_start_seconds'],
                          peak_gib=diag['peak_working_set']/2**30,
                          sampled_cpu_seconds=rows[-1]['cpu_seconds'],
                          process_cpu_seconds=final_result.get('process_cpu_seconds'),
                          summed_worker_conflicts=diag['total_worker_conflicts'],
                          diagnostic_reduced_edges=result['diagnostic_reduced_edge_domains'],
                          model_sha256=config['model_sha256'],
                          actual_portfolio=diag['actual_portfolio'])
    complete = [x for x in jobs.values() if 'sampled_cpu_seconds' in x]
    def stats(key):
        values = [x[key] for x in complete if x[key] is not None]
        return dict(min=min(values), median=statistics.median(values), max=max(values)) if values else None
    # 10-second process samples underestimate CPU at exit by up to one interval.
    cpu = sum(x['sampled_cpu_seconds'] for x in complete)
    exact_cpu = (sum(x['process_cpu_seconds'] for x in complete)
                 if complete and all(x['process_cpu_seconds'] is not None for x in complete) else None)
    started = datetime.fromisoformat(plan['start_utc']).timestamp()
    max_sampled_rss = 0
    for dt in range(0, int(report['elapsed_seconds'])+10, 10):
        total = 0
        for rows in curves:
            eligible = [x for x in rows if started+dt-15 <= datetime.fromisoformat(x['utc']).timestamp() <= started+dt]
            if eligible:
                total += eligible[-1]['working_set']
        max_sampled_rss = max(max_sampled_rss,total)
    return dict(name=folder.name, wall_seconds=report['elapsed_seconds'],
                jobs=jobs, status_counts=dict(Counter(x['status'] for x in jobs.values())),
                workers_per_job=plan['workers_per_job'], concurrent_jobs=plan['concurrent_jobs'],
                sampled_cpu_seconds=cpu,
                sampled_average_cpu_cores=cpu/report['elapsed_seconds'],
                cpu_seconds_at_solve_end=exact_cpu,
                average_cores_at_solve_end=exact_cpu/report['elapsed_seconds'] if exact_cpu else None,
                approximate_peak_sum_process_rss_gib=max_sampled_rss/2**30,
                presolve_seconds=stats('presolve_seconds'), peak_job_gib=stats('peak_gib'),
                summed_worker_conflicts=stats('summed_worker_conflicts'),
                diagnostic_reduced_edges=stats('diagnostic_reduced_edges'),
                scheduled_whole_partition=report['exhaustive_partition_scheduled'],
                rigorous_new_exclusions=0, proof_certificates=0)


def compare(folders, output):
    campaigns = [summary(p) for p in folders]
    comparisons = []
    for index in range(1, len(folders)):
        same = []; changed = []; pairs = []
        left, right = campaigns[0], campaigns[index]
        for name in sorted(left['jobs'].keys() & right['jobs'].keys()):
            a,b = left['jobs'][name],right['jobs'][name]
            if 'model_sha256' not in a or 'model_sha256' not in b:
                continue
            pairs.append(dict(branch=name, same_model=a['model_sha256'] == b['model_sha256']))
            d1 = read(folders[0]/name/'edge_domain_diagnostics.json')['edges']
            d2 = read(folders[index]/name/'edge_domain_diagnostics.json')['edges']
            (same if d1 == d2 else changed).append(name)
        comparisons.append(dict(left=left['name'],right=right['name'],model_pairs=pairs,
                                same_diagnostic_edge_domains=same, different_diagnostic_edge_domains=changed))
    value = dict(campaigns=campaigns, comparisons=comparisons,
                 caveats=['UNKNOWN branches remain open',
                          'No comparative time-to-proof gain without decisions',
                          'Conflicts and presolve domains are diagnostic, not exclusions',
                          'CPU and aggregate RSS are sampled estimates',
                          'No learned clauses are saved or exchanged between jobs'])
    output.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
    print(json.dumps([{k:v for k,v in c.items() if k != 'jobs'} for c in campaigns]))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('folders',nargs='+',type=Path)
    p.add_argument('--output',required=True,type=Path)
    a = p.parse_args()
    compare(a.folders,a.output)
