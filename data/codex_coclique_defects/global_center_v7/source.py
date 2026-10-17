"""Whole (0,2) boundary with a shared residual degree graph and column caps.

New obligations beyond the V6 B-B Gram model:
  D[:,a].D[:,b] + E[a,b] <= 2;
  E supplies all missing degrees and the defect-charge equations;
  a pair already sharing two B neighbours has no common E neighbour;
  all C-M mixed equations use this same E.
The model is still NECESSARY. Any boundary factor found is passed to the
exact affine completion solver. No core or cycle partition is fixed.
"""
from pathlib import Path
from itertools import combinations
from datetime import datetime, timezone
import argparse
import ctypes
import hashlib
import json
import os
import threading
import time
from ortools.sat.python import cp_model
from coclique_global_boundary import build as original_build


def build(mixed='coclique', saturated=True, triangles=False, rook_cut=False, center_kind='none'):
    model, variables, fixed, B, M, oldedge, oldproducts = original_build()
    residual = {(u, v): model.NewBoolVar(f'e{u}_{v}') for u, v in combinations(M, 2)}
    def edge(u, v):
        if u == v: return 0
        key = tuple(sorted((u, v)))
        return residual[key] if key in residual else oldedge(u, v)
    if rook_cut:
        # The incidence count excludes a rook on H+X+{v}; Lou-Murin 2.1
        # additionally excludes a rook with just one opposite edge missing.
        for v in range(99):
            if v not in range(21, 29):
                for u, w in ((25, 27), (26, 28)):
                    model.Add(edge(u, w)+sum(edge(v, x) for x in range(25, 29)) <= 4)
    products = {}
    def mul(a, b):
        if isinstance(a, int): return b if a else 0
        if isinstance(b, int): return a if b else 0
        key = tuple(sorted((a.Index(), b.Index())))
        if key not in products:
            p = model.NewBoolVar(f'cp{len(products)}')
            model.Add(p <= a); model.Add(p <= b); model.Add(p >= a+b-1)
            products[key] = p
        return products[key]
    center_count = 0
    if center_kind != 'none':
        assert rook_cut, 'The center reduction uses the proven rook exclusions'
        possible = (list(range(8, 21)) if center_kind in ('any', 'coclique') else [])
        possible += (list(range(63, 99)) if center_kind in ('any', 'zero') else [])
        centers = []
        for v in possible:
            center = model.NewBoolVar(f'four_X_center{v}')
            for x in range(25, 29): model.Add(center <= edge(v, x))
            model.Add(center >= sum(edge(v, x) for x in range(25, 29))-3)
            centers.append(center)
            if v >= 63:
                # All four triangle mates live in C without H or in Z0.
                allowed = list(range(8, 21))+list(range(63, 99))
                for x in range(25, 29):
                    model.Add(sum(mul(edge(v, w), edge(x, w)) for w in allowed if w != v) == 1).OnlyEnforceIf(center)
        model.Add(sum(centers) == 1)
        model.Add(edge(25, 27) == 0); model.Add(edge(26, 28) == 0)
        center_count = len(centers)
    model.Add(edge(37, 38) == 1)
    for u in M:
        model.Add(sum(edge(u, v) for v in B+M if u != v) == 14)
        if u >= 63:
            model.Add(sum(edge(u, v) for v in range(25, 37)) - edge(u, 37) - edge(u, 38) == 2)
    overlaps = {}
    for u, v in combinations(M, 2):
        count = model.NewIntVar(0, 2, f'overlap{u}_{v}')
        model.Add(count == sum(mul(edge(w, u), edge(w, v)) for w in B))
        model.Add(count + edge(u, v) <= 2)
        overlaps[u, v] = count
        if saturated:
            full = model.NewBoolVar(f'saturated{u}_{v}')
            used = count+edge(u, v) if triangles else count
            model.Add(used == 2).OnlyEnforceIf(full)
            model.Add(used <= 1).OnlyEnforceIf(full.Not())
            for w in M:
                if w not in (u, v):
                    model.Add(edge(u, w) + edge(v, w) <= 1).OnlyEnforceIf(full)
    triangle_count = 0
    if triangles:
        assert saturated, 'Mixed saturated pairs exclude triangles on edges already covered in B'
        uncovered = {}
        for (u, v), count in overlaps.items():
            x = model.NewBoolVar(f'uncovered{u}_{v}')
            model.Add(x+count == 1).OnlyEnforceIf(edge(u, v))
            model.Add(x == 0).OnlyEnforceIf(edge(u, v).Not())
            uncovered[u, v] = x
        incident = {key: [] for key in uncovered}
        for u, v, w in combinations(M, 3):
            pairs = ((u, v), (u, w), (v, w))
            t = model.NewBoolVar(f'triangle{u}_{v}_{w}')
            for pair in pairs:
                model.Add(t <= uncovered[pair]); incident[pair].append(t)
            model.Add(t >= sum(uncovered[pair] for pair in pairs)-2)
            triangle_count += 1
        for pair in uncovered:
            model.Add(sum(incident[pair]) == uncovered[pair])
        # Explicit arithmetic consequences improve propagation of the same cover.
        for u in M:
            half_degree = model.NewIntVar(0, 7, f'half_uncovered_degree{u}')
            model.Add(sum(x for pair, x in uncovered.items() if u in pair) == 2*half_degree)
        number = model.NewIntVar(0, 88, 'missing_triangles')
        model.Add(sum(uncovered.values()) == 3*number)
    rows = list(range(21)) if mixed == 'coclique' else B if mixed == 'all' else []
    for u in rows:
        for v in M:
            model.Add(sum(mul(edge(u, w), edge(v, w)) for w in B+M if w not in (u, v)) == 2-edge(u, v))
    metadata = dict(old_product_variables=oldproducts, new_product_variables=len(products),
                    edge_variables=len(variables)+len(residual), mixed_rows=rows,
                    saturated_pairs=saturated, residual_edges=len(residual), column_pairs=len(overlaps),
                    triangle_variables=triangle_count, rook_center_cuts=182 if rook_cut else 0,
                    center_kind=center_kind, possible_centers=center_count)
    return model, B, M, edge, metadata


class ProcessMemory(ctypes.Structure):
    _fields_ = [('cb', ctypes.c_ulong), ('PageFaultCount', ctypes.c_ulong)] + [
        (name, ctypes.c_size_t) for name in ('PeakWorkingSetSize', 'WorkingSetSize',
        'QuotaPeakPagedPoolUsage', 'QuotaPagedPoolUsage', 'QuotaPeakNonPagedPoolUsage',
        'QuotaNonPagedPoolUsage', 'PagefileUsage', 'PeakPagefileUsage')]


def observe(folder, stop):
    previous = None
    with (folder/'resources.jsonl').open('w', encoding='utf-8') as out:
        while True:
            now, cpu = time.monotonic(), time.process_time()
            memory = ProcessMemory(); memory.cb = ctypes.sizeof(memory)
            handle = ctypes.windll.kernel32.GetCurrentProcess
            handle.restype = ctypes.c_void_p
            ok = ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.c_void_p(handle()), ctypes.byref(memory), memory.cb)
            row = dict(utc=datetime.now(timezone.utc).isoformat(), pid=os.getpid(), cpu_seconds=cpu,
                       working_set=memory.WorkingSetSize if ok else None,
                       peak_working_set=memory.PeakWorkingSetSize if ok else None)
            if previous:
                row['average_cpu_cores'] = (cpu-previous[1])/(now-previous[0])
            out.write(json.dumps(row)+'\n'); out.flush()
            previous = (now, cpu)
            if stop.wait(10): break


def run(folder, seconds, workers, mixed, saturated, triangles=False, no_max_lp=False, rook_cut=False, center_kind='none'):
    folder.mkdir(parents=True, exist_ok=False)
    config = dict(start_utc=datetime.now(timezone.utc).isoformat(), seconds=seconds, workers=workers,
                  mixed=mixed, saturated=saturated, triangles=triangles, no_max_lp=no_max_lp,
                  rook_cut=rook_cut, pid=os.getpid(),
                  center_kind=center_kind,
                  scope='All (0,2); binary Gram, residual degree graph, column caps and mixed equations',
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  boundary_source_sha256=hashlib.sha256(Path(__file__).with_name('coclique_global_boundary.py').read_bytes()).hexdigest())
    if center_kind != 'none':
        config['scope'] = 'Only (0,2) with a common neighbour of all four X; center_kind='+center_kind
    (folder/'config.json').write_text(json.dumps(config, indent=2)+'\n', encoding='utf-8')
    (folder/'source.py').write_bytes(Path(__file__).read_bytes())
    stop = threading.Event(); monitor = threading.Thread(target=observe, args=(folder, stop), daemon=True)
    monitor.start()
    try:
        start = time.monotonic()
        model, B, M, edge, meta = build(mixed=mixed, saturated=saturated, triangles=triangles,
                                      rook_cut=rook_cut, center_kind=center_kind)
        meta.update(build_seconds=time.monotonic()-start, model_stats=model.ModelStats(), border=B, missing=M)
        (folder/'model.json').write_text(json.dumps(meta, indent=2)+'\n', encoding='utf-8')
        print(json.dumps({k: v for k, v in meta.items() if k not in ('model_stats', 'border', 'missing', 'mixed_rows')}), flush=True)
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = seconds
        solver.parameters.num_search_workers = workers
        if no_max_lp: solver.parameters.ignore_subsolvers.append('max_lp')
        solver.parameters.log_search_progress = True
        solver.parameters.log_to_stdout = False
        with (folder/'search.log').open('w', encoding='utf-8') as log:
            solver.log_callback = lambda line: (log.write(line+'\n'), log.flush())
            status = solver.Solve(model)
        result = dict(status=solver.StatusName(status), seconds=solver.WallTime(),
                      branches=solver.NumBranches(), conflicts=solver.NumConflicts(),
                      response_stats=solver.ResponseStats(), full_srg=False,
                      scope=config['scope'], necessary_model=True)
        if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            import sympy as sp
            from coclique_global_completion import encode
            from coclique_affine_completion import binary_completions
            value = lambda u, v: edge(u, v) if isinstance(edge(u, v), int) else solver.Value(edge(u, v))
            BB = sp.Matrix(len(B), len(B), lambda u, v: value(B[u], B[v]))
            DD = sp.Matrix(len(B), len(M), lambda u, v: value(B[u], M[v]))
            EE = sp.Matrix(len(M), len(M), lambda u, v: value(M[u], M[v]))
            result.update(B=encode(BB), D=encode(DD), residual_degree_graph=encode(EE))
            (folder/'boundary_candidate.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
            completion = binary_completions(BB, DD, seconds=60)
            (folder/'completion.json').write_text(json.dumps(completion, indent=2)+'\n', encoding='utf-8')
            result.update(full_srg=bool(completion['completions']), completion_verdict=completion.get('verdict', completion['status']))
        (folder/'result.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
        print(json.dumps({k: v for k, v in result.items() if k not in ('B', 'D', 'residual_degree_graph', 'response_stats')}), flush=True)
    finally:
        stop.set(); monitor.join(timeout=3)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=Path)
    parser.add_argument('--seconds', type=float, default=600)
    parser.add_argument('--workers', type=int, default=8)
    parser.add_argument('--mixed', choices=('none', 'coclique', 'all'), default='coclique')
    parser.add_argument('--no-saturation', action='store_true')
    parser.add_argument('--triangles', action='store_true')
    parser.add_argument('--no-max-lp', action='store_true')
    parser.add_argument('--rook-cut', action='store_true')
    parser.add_argument('--center-kind', choices=('none', 'any', 'coclique', 'zero'), default='none')
    args = parser.parse_args()
    run(args.folder, args.seconds, args.workers, args.mixed, not args.no_saturation,
        args.triangles, args.no_max_lp, args.rook_cut, args.center_kind)
