r"""Enumeration farm (C1, 27/09 night). Runs y_pairs_gamma.py on a queue of envelopes, in parallel on THIS PC, under a
machine-wide governor:
  - a new job starts only if the machine's CPU utility (Task Manager's metric, Processor Information % Processor Utility,
    averaged over 3 samples) is below --cpu and its RAM in use is below --ram, with at most --workers jobs;
  - each job runs through run_capped.ps1: per-job RAM cap 1500 MB, killed if the machine's free RAM drops under 20%,
    BLAS pinned to one thread.
Finished lists with "complete": true are committed and pushed to conway99-c1 one at a time. Incomplete ones are renamed
*.INCOMPLETE.json and never used.
Usage: python enum_farm.py <ids, comma-separated> [--workers 6] [--cpu 65] [--ram 75] [--shed-cpu 78] [--shed-ram 77] [--max-seconds 86400]
SHED rule: if the machine goes over --shed-cpu / --shed-ram (Task Manager metrics), the NEWEST job is killed and re-queued."""
import json, os, subprocess, sys, time

ROOT = r'C:\Users\RESEARCHER\Desktop\c1_recherche'
ENV = r'C:/home/researcher/Desktop/c99_structures_lab/involution/envelopes/U/%03d.json'
RUNS = r'C:\Users\RESEARCHER\AppData\Local\Temp\claude\runs'
PY = r'C:\Users\RESEARCHER\AppData\Local\Python\pythoncore-3.14-64\python.exe'
RC = r'C:\Users\RESEARCHER\.claude\tools\run_capped.ps1'
STATUS = os.path.join(RUNS, 'enum_farm.status.jsonl')


def arg(name, default):
    return type(default)(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


def machine():
    ps = ("$p=Get-CimInstance Win32_PerfFormattedData_Counters_ProcessorInformation -Filter \"Name='_Total'\";"
          "$o=Get-CimInstance Win32_OperatingSystem;"
          "Write-Output ('{0} {1}' -f $p.PercentProcessorUtility, "
          "[math]::Round(100*($o.TotalVisibleMemorySize-$o.FreePhysicalMemory)/$o.TotalVisibleMemorySize))")
    out = subprocess.run(['powershell', '-NoProfile', '-Command', ps], capture_output=True, text=True).stdout.split()
    return float(out[0]), float(out[1])


def machine_avg(n=3):
    s = [machine() for _ in range(n)]
    return sum(a for a, _ in s) / n, max(b for _, b in s)


def log(obj):
    obj['t'] = time.strftime('%H:%M:%S')
    with open(STATUS, 'a') as f:
        f.write(json.dumps(obj) + '\n')
    print(json.dumps(obj), flush=True)


def gamma_file(i):
    g = os.path.join(ROOT, 'data', 'finishC', 'gamma', 'gamma_%03d.json' % i)
    if os.path.exists(g):
        return g, 'gamma'
    g = 'C:/home/researcher/Desktop/c2_experimental_ro/data/finishC/gamma_c2/gamma_%03d.json' % i
    if os.path.exists(g):
        return g, 'gamma_c2(conway99-c2-experimental 89592e2)'
    g = os.path.join(ROOT, 'data', 'finishC', 'gamma_trivial', 'gamma_%03d.json' % i)
    return (g, 'gamma_trivial') if os.path.exists(g) else (None, None)


def launch(i, ms):
    g, kind = gamma_file(i)
    out = os.path.join(ROOT, 'data', 'finishC', 'ypairs', 'gpairs_%03d.json' % i)
    lg = os.path.join(RUNS, 'farm_%03d.log' % i)
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
    args = 'code/y_pairs_gamma.py %s %s %s --max-seconds %d' % (ENV % i, g.replace('\\', '/'), out.replace('\\', '/'), ms)
    p = subprocess.Popen(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', RC, '-LimitMB', '1500',
                          '-TimeoutSec', str(ms + 600), '-MinFreeMB', '3100', '-MinFreeCommitMB', '3000', '-WorkDir', ROOT,
                          '-Log', lg, '-Exe', PY, '-ArgList', args], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    log({'event': 'start', 'id': i, 'gamma': kind})
    return p, out


def git(*a):
    return subprocess.run(['git'] + list(a), cwd=ROOT, capture_output=True, text=True)


def finalize(i, out):
    if not os.path.exists(out):
        log({'event': 'FAILED-nofile', 'id': i}); return
    try:
        info = json.load(open(out)).get('stats', {})
    except Exception as e:
        log({'event': 'FAILED-badjson', 'id': i, 'err': repr(e)[:120]}); return
    if not info.get('complete', False):
        os.replace(out, out.replace('.json', '.INCOMPLETE.json'))
        log({'event': 'INCOMPLETE', 'id': i, 'info': {k: info.get(k) for k in ('pairs', 'y1_orbits', 'seconds')}}); return
    git('add', out)
    r = git('-c', 'user.email=206353265+amazing-source@users.noreply.github.com', 'commit', '-q', '-m',
            'gpairs_%03d: complete y-pair list (%s pairs) from the enumeration farm (sweep-first)\n\n'
            'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n'
            'Claude-Session: https://claude.ai/code/session_01VphcnaUZ6bgz8pdMW3WTVM' % (i, info.get('pairs')), '--', out)
    git('pull', '-q', '--rebase', '--autostash'); p = git('push', '-q')
    log({'event': 'done', 'id': i, 'pairs': info.get('pairs'), 'seconds': info.get('seconds'),
         'commit_rc': r.returncode, 'push_rc': p.returncode})


def main():
    ids = [int(x) for x in sys.argv[1].split(',')]
    W, CPU, RAM, MS = arg('--workers', 9), arg('--cpu', 70.0), arg('--ram', 75.0), arg('--max-seconds', 86400)
    SHED_CPU, SHED_RAM = arg('--shed-cpu', 78.0), arg('--shed-ram', 77.0)
    queue = []
    for i in ids:
        out = os.path.join(ROOT, 'data', 'finishC', 'ypairs', 'gpairs_%03d.json' % i)
        if os.path.exists(out):
            log({'event': 'skip-exists', 'id': i}); continue
        if gamma_file(i)[0] is None:
            log({'event': 'skip-nogamma', 'id': i}); continue
        queue.append(i)
    running = {}
    log({'event': 'farm-start', 'queue': queue, 'workers': W, 'cpu_max': CPU, 'ram_max': RAM})
    order = []                                   # launch order, newest last (shed newest first)
    while queue or running:
        for i, (p, out) in list(running.items()):
            if p.poll() is not None:
                finalize(i, out); del running[i]; order.remove(i)
        cpu, ram = machine_avg()
        if running and (cpu > SHED_CPU or ram > SHED_RAM):
            i = order.pop(); p, out = running.pop(i)
            subprocess.run(['taskkill', '/T', '/F', '/PID', str(p.pid)], capture_output=True)
            if os.path.exists(out):
                os.remove(out)
            queue.insert(0, i)
            log({'event': 'SHED', 'id': i, 'cpu': round(cpu), 'ram': ram, 'running': len(running)})
            time.sleep(120); continue
        if queue and len(running) < W and cpu < CPU and ram < RAM:
            i = queue.pop(0); running[i] = launch(i, MS); order.append(i); time.sleep(30); continue
        time.sleep(60)
    log({'event': 'farm-end'})


if __name__ == '__main__':
    main()
