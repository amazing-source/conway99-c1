r"""Enumeration farm v2 (C1, 27/09 night): y_pairs_gamma.py on a queue of envelopes, each lattice split into chunks, under a
machine-wide governor shared with the other sessions on this PC.
Governor (what Task Manager shows): CPU = max(% Processor Utility, Win32_Processor LoadPercentage), averaged over 3 samples;
RAM = % of physical memory in use. A job (1 thread) starts only below --cpu / --ram and with at most --threads jobs of ours;
above --shed-cpu / --shed-ram the NEWEST job is killed and re-queued.
Per lattice: plan (the y1 stage; writes the y1 representatives) -> n chunks (--from-plan, --chunk k/n) -> merge -> commit + push.
The union of the chunks is exactly the single-run list (the y2 reduction is done per y1 representative).
RAM: every job runs inside run_capped.ps1. A job killed for its OWN RAM is re-queued with twice the cap (at most --max-cap MB)
and starts only when the machine has room for that cap. A job killed because the MACHINE was low is re-queued unchanged.
Usage: python enum_farm2.py <ids comma-separated> [--threads 4] [--cpu 70] [--ram 72] [--shed-cpu 80] [--shed-ram 78]
       [--per-chunk 30] [--max-chunks 32] [--adopt ids]   (--adopt: lists being produced by jobs started elsewhere; commit them
       when they appear complete)"""
import json, math, os, subprocess, sys, time

ROOT = r'C:\Users\RESEARCHER\Desktop\c1_recherche'
ENV = 'C:/home/researcher/Desktop/c99_structures_lab/involution/envelopes/U/%03d.json'
RUNS = r'C:\Users\RESEARCHER\AppData\Local\Temp\claude\runs'
WORK = os.path.join(RUNS, 'farm2')
PY = r'C:\Users\RESEARCHER\AppData\Local\Python\pythoncore-3.14-64\python.exe'
RC = r'C:\Users\RESEARCHER\.claude\tools\run_capped.ps1'
STATUS = os.path.join(RUNS, 'enum_farm2.status.jsonl')
FINAL = os.path.join(ROOT, 'data', 'finishC', 'ypairs', 'gpairs_%03d.json')


def arg(name, default):
    return type(default)(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


def machine():
    ps = ("$p=Get-CimInstance Win32_PerfFormattedData_Counters_ProcessorInformation -Filter \"Name='_Total'\";"
          "$l=(Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average;"
          "$o=Get-CimInstance Win32_OperatingSystem;"
          "Write-Output ('{0} {1} {2} {3}' -f $p.PercentProcessorUtility, $l, "
          "[math]::Round(100*($o.TotalVisibleMemorySize-$o.FreePhysicalMemory)/$o.TotalVisibleMemorySize), "
          "[math]::Round($o.TotalVisibleMemorySize/1024))")
    out = subprocess.run(['powershell', '-NoProfile', '-Command', ps], capture_output=True, text=True).stdout.split()
    try:
        return max(float(out[0]), float(out[1])), float(out[2]), float(out[3])
    except (ValueError, IndexError):                                  # LoadPercentage can come back empty
        return float(out[0]), float(out[-2]), float(out[-1])


def machine_avg(n=3):
    s = [machine() for _ in range(n)]
    return sum(a for a, _, _ in s) / n, max(b for _, b, _ in s), s[0][2]


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


def plan_path(i):
    return os.path.join(WORK, 'plan_%03d.json' % i)


def chunk_path(i, k, n):
    return os.path.join(WORK, 'chunk_%03d_%d_%d.json' % (i, k, n))


def read_json(p):
    try:
        return json.load(open(p))
    except Exception:
        return None


class Task:
    def __init__(self, kind, i, k=0, n=1, cap=2000, prio=0.0):
        self.kind, self.i, self.k, self.n, self.cap, self.prio = kind, i, k, n, cap, prio

    def name(self):
        return 'plan_%03d' % self.i if self.kind == 'plan' else 'chunk_%03d_%d_%d' % (self.i, self.k, self.n)

    def out(self):
        return plan_path(self.i) if self.kind == 'plan' else chunk_path(self.i, self.k, self.n)


def launch(t, ms):
    g, kind = gamma_file(t.i)
    lg = os.path.join(WORK, t.name() + '.log')
    if os.path.exists(t.out()):
        os.remove(t.out())
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
    env.pop('PYTHONPATH', None)
    args = 'code/y_pairs_gamma.py %s %s %s --max-seconds %d' % (ENV % t.i, g.replace('\\', '/'), t.out().replace('\\', '/'), ms)
    if t.kind == 'plan':
        args += ' --plan'
    else:
        args += ' --from-plan %s --chunk %d/%d' % (plan_path(t.i).replace('\\', '/'), t.k, t.n)
    p = subprocess.Popen(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', RC, '-LimitMB', str(t.cap),
                          '-TimeoutSec', str(ms + 600), '-MinFreeMB', '2500', '-MinFreeCommitMB', '3000', '-StatusSec', '60',
                          '-WorkDir', ROOT, '-Log', lg, '-Exe', PY, '-ArgList', args],
                         env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    log({'event': 'start', 'task': t.name(), 'cap': t.cap, 'gamma': kind})
    return p


def killed_reason(t):
    try:
        txt = open(os.path.join(WORK, t.name() + '.log')).read()
    except Exception:
        return 'nolog'
    if 'KILLED: job RAM' in txt:
        return 'ram'
    if 'KILLED: machine' in txt:
        return 'machine'
    if 'KILLED' in txt:
        return 'other-kill'
    return 'exit'


def git(*a):
    return subprocess.run(['git'] + list(a), cwd=ROOT, capture_output=True, text=True)


def commit_final(i, info):
    out = FINAL % i
    git('add', out)
    r = git('-c', 'user.email=206353265+amazing-source@users.noreply.github.com', 'commit', '-q', '-m',
            'gpairs_%03d: complete y-pair list (%s pairs) from the enumeration farm (sweep-first)\n\n'
            'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n'
            'Claude-Session: https://claude.ai/code/session_01VphcnaUZ6bgz8pdMW3WTVM' % (i, info.get('pairs')), '--', out)
    git('pull', '-q', '--rebase', '--autostash')
    p = git('push', '-q')
    log({'event': 'done', 'id': i, 'pairs': info.get('pairs'), 'cpu_seconds': info.get('seconds'),
         'chunks': info.get('chunks'), 'commit_rc': r.returncode, 'push_rc': p.returncode})


def merge(i, n):
    parts = [read_json(chunk_path(i, k, n)) for k in range(n)]
    plan = read_json(plan_path(i))
    info = dict(plan['plan'])
    tot = {'y2_candidates': 0, 'y2_orbits': 0, 'truncated': 0, 'pairs': 0}
    pairs, secs = [], plan['plan'].get('seconds', 0)
    for k, d in enumerate(parts):
        st = d['stats']
        assert st.get('complete') and (n == 1 or st.get('chunk') == [k, n]), (i, k, n)
        for key in tot:
            tot[key] += st.get(key, 0)
        secs += st.get('seconds', 0)
        pairs.extend(d['pairs'])
    info.update(tot)
    info.update(complete=True, seconds=round(secs, 1), chunks=n)
    info.pop('chunk', None); info.pop('y1_orbits_chunk', None)
    assert tot['pairs'] == len(pairs)
    json.dump({'id': i, 'pairs': pairs, 'stats': info, 'note': parts[0].get('note', '') +
               ('; merged from %d chunks (enum_farm2)' % n if n > 1 else '')}, open(FINAL % i, 'w'))
    commit_final(i, info)


def main():
    os.makedirs(WORK, exist_ok=True)
    ids = [int(x) for x in sys.argv[1].split(',')]
    TH, CPU, RAM, MS = arg('--threads', 4), arg('--cpu', 70.0), arg('--ram', 72.0), arg('--max-seconds', 86400)
    SHED_CPU, SHED_RAM = arg('--shed-cpu', 80.0), arg('--shed-ram', 78.0)
    PER, NMAX, MAXCAP = arg('--per-chunk', 30), arg('--max-chunks', 32), arg('--max-cap', 8000)
    adopt = set(int(x) for x in arg('--adopt', '').split(',') if x)
    queue, nchunks, pending = [], {}, {}
    for i in ids:
        if os.path.exists(FINAL % i) or i in adopt:
            log({'event': 'skip-exists-or-adopted', 'id': i}); continue
        if gamma_file(i)[0] is None:
            log({'event': 'skip-nogamma', 'id': i}); continue
        queue.append(Task('plan', i, prio=1e9 - i))           # plans first (they size the work), small ids first
    running = {}                                              # name -> (task, popen)
    order = []
    log({'event': 'farm2-start', 'plans': len(queue), 'threads': TH, 'cpu_max': CPU, 'ram_max': RAM, 'adopt': sorted(adopt)})

    def on_plan_done(t):
        pl = read_json(t.out())
        if pl is None:
            return False
        y1 = pl['plan']['y1_orbits']
        n = max(1, min(NMAX, math.ceil(y1 / PER)))
        nchunks[t.i] = n
        pending[t.i] = set(range(n))
        lv = pl['plan'].get('label_vectors', 1)
        for k in range(n):
            if (read_json(chunk_path(t.i, k, n)) or {}).get('stats', {}).get('complete'):
                pending[t.i].discard(k); continue
            queue.append(Task('chunk', t.i, k, n, cap=t.cap, prio=y1 * lv / n))
        log({'event': 'planned', 'id': t.i, 'y1_orbits': y1, 'label_vectors': lv, 'chunks': n,
             'plan_seconds': pl['plan'].get('seconds')})
        if not pending[t.i]:
            merge(t.i, n)
        return True

    for t in [t for t in queue if t.kind == 'plan']:              # restart: reuse finished plans made with the same Gamma
        pl = read_json(t.out()) if os.path.exists(t.out()) else None
        if pl and pl.get('gamma_sha') and 'y1_reps' in pl:
            queue.remove(t)
            on_plan_done(t)
    while queue or running or adopt:
        for i in list(adopt):
            d = read_json(FINAL % i) if os.path.exists(FINAL % i) else None
            if d and d.get('stats', {}).get('complete'):
                commit_final(i, d['stats']); adopt.discard(i)
        for name, (t, p) in list(running.items()):
            if p.poll() is None:
                continue
            del running[name]; order.remove(name)
            d = read_json(t.out())
            ok = d is not None and (t.kind == 'plan' or d.get('stats', {}).get('complete'))
            if ok and t.kind == 'plan':
                on_plan_done(t)
            elif ok:
                pending[t.i].discard(t.k)
                log({'event': 'chunk-done', 'task': name, 'pairs': d['stats'].get('pairs'), 's': d['stats'].get('seconds'),
                     'left': len(pending[t.i])})
                if not pending[t.i]:
                    merge(t.i, t.n)
            else:
                why = killed_reason(t)
                if why == 'ram' and t.cap < MAXCAP:
                    t.cap = min(MAXCAP, 2 * t.cap); queue.append(t)
                elif why == 'machine':
                    queue.append(t)
                log({'event': 'FAILED', 'task': name, 'why': why, 'requeued': t in queue, 'cap': t.cap})
        cpu, ram, totmb = machine_avg()
        if running and (cpu > SHED_CPU or ram > SHED_RAM):
            name = order.pop(); t, p = running.pop(name)
            subprocess.run(['taskkill', '/T', '/F', '/PID', str(p.pid)], capture_output=True)
            queue.append(t)
            log({'event': 'SHED', 'task': name, 'cpu': round(cpu), 'ram': ram, 'running': len(running)})
            time.sleep(90); continue
        if queue and len(running) < TH and cpu < CPU and ram < RAM:
            queue.sort(key=lambda t: -t.prio)
            fit = [t for t in queue if t.cap <= 2000 or ram + 100.0 * t.cap / totmb < RAM + 8]
            if fit:
                t = fit[0]; queue.remove(t)
                running[t.name()] = (t, launch(t, MS)); order.append(t.name())
                time.sleep(20); continue
        time.sleep(30)
    log({'event': 'farm2-end'})


if __name__ == '__main__':
    main()
