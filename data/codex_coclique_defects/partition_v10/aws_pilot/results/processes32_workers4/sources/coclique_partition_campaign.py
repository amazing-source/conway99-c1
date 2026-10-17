"""Portable bounded experiments on the disjoint V10 branches.

Each job is an independent CP-SAT process. No clauses pass between jobs.
UNKNOWN jobs remain open; a saved result is not a proof certificate.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import threading
import time

import ortools
from ortools.sat.python import cp_model
from coclique_calibration import parameters
from coclique_residual_partition import build, branches
from coclique_solver_diagnostics import diagnose


SCOPE = 'All coclique21 (0,2), partitioned by unordered negative degrees and triangle location'


def utc():
    return datetime.now(timezone.utc).isoformat()


def save(path, value):
    temporary = path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8')
    temporary.replace(path)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def observe(folder, stop):
    if os.name == 'nt':
        from coclique_column_coexistence import observe as windows_observe
        return windows_observe(folder, stop)
    previous = None
    with (folder/'resources.jsonl').open('w', encoding='utf-8') as out:
        while True:
            now, cpu = time.monotonic(), time.process_time()
            status = dict(line.split(':', 1) for line in Path('/proc/self/status').read_text().splitlines())
            row = dict(utc=utc(), pid=os.getpid(), cpu_seconds=cpu,
                       working_set=int(status['VmRSS'].split()[0])*1024,
                       peak_working_set=int(status['VmHWM'].split()[0])*1024)
            if previous:
                row['average_cpu_cores'] = (cpu-previous[1])/(now-previous[0])
            out.write(json.dumps(row)+'\n')
            out.flush()
            previous = now, cpu
            if stop.wait(10):
                break


def configure(solver, seconds, workers, seed):
    if workers not in (1, 2, 4, 8):
        raise ValueError('Calibrated process sizes: 1, 2, 4, 8 only')
    parameters(solver, 'boolean', seconds, max(8, workers), seed)
    p = solver.parameters
    p.num_workers = workers
    p.num_full_subsolvers = {1: 1, 2: 1, 4: 3, 8: 6}[workers]
    if workers == 1:
        p.search_branching = cp_model.AUTOMATIC_SEARCH
    # No extrapolation to 128 workers: OR-Tools would duplicate the first
    # configured full solver after exhausting the six named configurations.


def run_job(folder, branch, seconds, workers, seed, residual=True, keep_model=False):
    folder.mkdir(parents=True, exist_ok=False)
    source_files = [Path(__file__), Path(__file__).with_name('coclique_residual_partition.py'),
                    Path(__file__).with_name('coclique_global_boundary.py'),
                    Path(__file__).with_name('coclique_column_coexistence.py'),
                    Path(__file__).with_name('coclique_calibration.py')]
    config = dict(start_utc=utc(), pid=os.getpid(), seconds=seconds, workers=workers,
                  seed=seed, branch=branch, residual_equations=residual, scope=SCOPE,
                  platform=platform.platform(), python=platform.python_version(),
                  ortools=ortools.__version__, source_hashes={p.name:digest(p) for p in source_files},
                  reuse_learned_clauses=False, tightened_domains_reused=False)
    save(folder/'config.json', config)
    stop = threading.Event()
    monitor = threading.Thread(target=observe, args=(folder, stop), daemon=True)
    monitor.start()
    try:
        started = time.monotonic()
        model, B, M, edge, meta = build(None if branch == 'global' else branch, residual)
        meta.update(build_seconds=time.monotonic()-started, border=B, missing=M,
                    model_stats=model.model_stats())
        error = model.validate()
        if error:
            raise ValueError(error)
        model_file = folder/'model.pb'
        assert model.export_to_file(str(model_file))
        model_hash = digest(model_file)
        meta.update(model_sha256=model_hash, model_bytes=model_file.stat().st_size,
                    model_retained=keep_model)
        if not keep_model:
            model_file.unlink()
        save(folder/'model.json', meta)
        edge_map = []
        for u, v in combinations(range(99), 2):
            x = edge(u, v)
            edge_map.append(dict(u=u, v=v, fixed=x) if isinstance(x, int)
                            else dict(u=u, v=v, variable=x.index))
        save(folder/'edge_map.json', edge_map)
        solver = cp_model.CpSolver()
        configure(solver, seconds, workers, seed)
        config.update(model_sha256=model_hash, ignored_subsolvers=list(solver.parameters.ignore_subsolvers))
        save(folder/'config.json', config)
        (folder/'parameters.textproto').write_text(str(solver.parameters), encoding='utf-8')
        print(json.dumps(dict(event='SOLVE_START', branch=branch, workers=workers,
                              build_seconds=meta['build_seconds'], model_sha256=model_hash)), flush=True)
        with (folder/'search.log').open('w', encoding='utf-8') as log:
            solver.log_callback = lambda line: (log.write(line+'\n'), log.flush())
            status = solver.solve(model)
        result = dict(status=solver.status_name(status), seconds=solver.wall_time,
                      total_seconds=time.monotonic()-started,
                      response_stats=solver.response_stats(), branch=branch,
                      necessary_model=True, full_srg=False, scope=SCOPE,
                      proof_certificate=None)
        reduced = []
        tightened = solver.response_proto.tightened_variables
        if tightened:
            for entry in edge_map:
                if 'variable' not in entry:
                    continue
                idx = entry['variable']
                domain = list(tightened[idx].domain)
                if domain != list(model.proto.variables[idx].domain):
                    reduced.append(dict(**entry, domain=domain))
        save(folder/'edge_domain_diagnostics.json', dict(
            warning='Diagnostic representatives, NOT universal graph lemmas', edges=reduced))
        result['diagnostic_reduced_edge_domains'] = len(reduced)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            import numpy as np
            A = np.array([[edge(u,v) if isinstance(edge(u,v), int) else solver.value(edge(u,v))
                           for v in range(99)] for u in range(99)], dtype=np.int64)
            defect = A@A+A-12*np.eye(99, dtype=np.int64)-2
            result['full_srg'] = bool(not np.any(defect) and np.all(A.sum(axis=1) == 14))
            save(folder/'candidate.json', dict(A=A.tolist(), B=A[np.ix_(B,B)].tolist(),
                  D=A[np.ix_(B,M)].tolist(), E=A[np.ix_(M,M)].tolist(),
                  nonzero_polynomial_entries=int(np.count_nonzero(defect)),
                  polynomial_defect=defect.tolist()))
        save(folder/'result.json', result)
        print(json.dumps({k:v for k,v in result.items() if k != 'response_stats'}), flush=True)
    finally:
        stop.set()
        monitor.join(timeout=3)
    save(folder/'diagnostics.json', diagnose(folder))


def campaign(folder, seconds, workers, jobs, seed, selected=None, residual=True):
    folder.mkdir(parents=True, exist_ok=False)
    all_branches = branches()
    chosen = all_branches if selected is None else [x for x in all_branches if x['id'] in selected]
    if selected and len(chosen) != len(selected):
        raise ValueError('Invalid / repeated branch id')
    source = folder/'sources'
    source.mkdir()
    for name in ('coclique_partition_campaign.py', 'coclique_residual_partition.py',
                 'coclique_column_coexistence.py', 'coclique_global_boundary.py',
                 'coclique_calibration.py', 'coclique_solver_diagnostics.py',
                 'check_coclique_residual_partition.py'):
        (source/name).write_bytes(Path(__file__).with_name(name).read_bytes())
    plan = dict(start_utc=utc(), seconds_per_branch=seconds, workers_per_job=workers,
                concurrent_jobs=jobs, total_requested_workers=jobs*workers, seed=seed,
                residual_equations=residual, all_branches=all_branches, selected_branches=chosen,
                source_hashes={p.name:digest(p) for p in source.iterdir()},
                scope=SCOPE, persisted_clause_sharing_between_jobs=False,
                cpu_count=os.cpu_count(), platform=platform.platform())
    save(folder/'protocol.json', plan)
    started = time.monotonic()
    results = {}
    def invoke(item):
        run_folder = folder/item['id']
        command = [sys.executable, str(Path(__file__).resolve()), 'run', str(run_folder),
                   '--branch', item['id'], '--seconds', str(seconds), '--workers', str(workers),
                   '--seed', str(seed)]
        if not residual:
            command.append('--no-residual')
        with (folder/(item['id']+'.console.log')).open('w', encoding='utf-8') as out:
            proc = subprocess.run(command, stdout=out, stderr=subprocess.STDOUT)
        value = json.loads((run_folder/'result.json').read_text()) if (run_folder/'result.json').exists() else {}
        value.update(returncode=proc.returncode)
        value.pop('response_stats', None)
        return item['id'], value
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = [pool.submit(invoke, item) for item in chosen]
        for future in as_completed(futures):
            name, value = future.result()
            results[name] = value
            progress = dict(updated_utc=utc(), elapsed_seconds=time.monotonic()-started,
                            completed=len(results), scheduled=len(chosen), results=results)
            save(folder/'progress.json', progress)
            print(json.dumps(dict(event='FINISHED', branch=name, completed=len(results),
                                  scheduled=len(chosen), status=value.get('status', 'ERROR'))), flush=True)
    progress.update(finished_utc=utc(), exhaustive_partition_scheduled=len(chosen) == len(all_branches),
                    mathematically_closed=False)
    save(folder/'report.json', progress)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('run', 'campaign'))
    parser.add_argument('folder', type=Path)
    parser.add_argument('--branch', default='global')
    parser.add_argument('--select', nargs='+')
    parser.add_argument('--seconds', type=float, default=180)
    parser.add_argument('--workers', type=int, choices=(1,2,4,8), default=4)
    parser.add_argument('--jobs', type=int, default=1)
    parser.add_argument('--seed', type=int, default=1)
    parser.add_argument('--no-residual', action='store_true')
    parser.add_argument('--keep-model', action='store_true')
    args = parser.parse_args()
    if args.mode == 'run':
        run_job(args.folder, args.branch, args.seconds, args.workers, args.seed,
                not args.no_residual, args.keep_model)
    else:
        campaign(args.folder, args.seconds, args.workers, args.jobs, args.seed,
                 args.select, not args.no_residual)
