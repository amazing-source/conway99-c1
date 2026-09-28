r"""Knuth survey of every MOD4_FEASIBLE pair (C1, 28/09): estimated leaves with DC + partial mod-4 pruning, to pick the pairs
small enough to finish exactly. Several workers can run at once (claim files). Results: data/rank17/knuth_all.jsonl.
Usage: python rank17_knuth_all.py <tags comma-separated> [walks]"""
import sys, os, json, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rank17_z4export as ex
DATA = os.path.join(HERE, '..', 'data', 'rank17')
WORK = 'C:/home/researcher/AppData/Local/Temp/claude/runs/knuth_all'
EXE = os.path.join(HERE, 'rank17_z4.exe')
OUT = os.path.join(DATA, 'knuth_all.jsonl')


def open_pairs(tag):
    rows = [json.loads(l) for l in open(os.path.join(DATA, 'z4_%s.jsonl' % tag)) if l.strip()]
    best = {}
    for r in rows:
        if r['pair'] not in best or best[r['pair']]['verdict'] == 'UNDECIDED':
            best[r['pair']] = r
    return sorted(p for p, r in best.items() if r['verdict'] == 'MOD4_FEASIBLE')


walks = int(sys.argv[2]) if len(sys.argv) > 2 else 150
os.makedirs(os.path.join(WORK, 'claims'), exist_ok=True)
queue = []
if sys.argv[1].endswith('.json'):                                   # explicit list of 'tag:pair'
    L = json.load(open(sys.argv[1]))
    lists = {}
    for k in L:
        t, p_ = k.split(':'); lists.setdefault(t, []).append(int(p_))
    tags = sorted(lists)
else:
    tags = sys.argv[1].split(',')
    lists = {t: open_pairs(t) for t in tags}
for i in range(max(len(v) for v in lists.values())):              # interleave the types
    for t in tags:
        if i < len(lists[t]):
            queue.append((t, lists[t][i]))
done = set()
if os.path.exists(OUT):
    done = {(json.loads(l)['tag'], json.loads(l)['pair']) for l in open(OUT) if l.strip()}
print('queue', len(queue), 'done', len(done), flush=True)
for tag, pid in queue:
    if (tag, pid) in done:
        continue
    try:
        os.close(os.open(os.path.join(WORK, 'claims', '%s_%d' % (tag, pid)), os.O_CREAT | os.O_EXCL | os.O_WRONLY))
    except FileExistsError:
        continue
    binf = os.path.join(WORK, '%s_%d.bin' % (tag, pid))
    t0 = time.time()
    try:
        info = ex.export(tag, pid, binf)
        r = subprocess.run([EXE, binf, 'run', binf + '.surv'], capture_output=True, text=True, timeout=1800,
                           env=dict(os.environ, Z4_KNUTH=str(walks), Z4_DC='1'))
        js = [l for l in r.stdout.splitlines() if l.startswith('{')]
        rec = {'tag': tag, 'pair': pid, 'dc_forbidden': info.get('dc_forbidden')}
        rec.update(json.loads(js[0]) if js else {'error': r.stderr[-300:]})
    except Exception as e:                                          # keep the survey going
        rec = {'tag': tag, 'pair': pid, 'error': repr(e)[:300]}
    rec['total_s'] = round(time.time() - t0, 1)
    with open(OUT, 'a') as f:
        f.write(json.dumps(rec) + chr(10))
    print(json.dumps({k: rec.get(k) for k in ('tag', 'pair', 'leaves_est', 'nodes_est', 'total_s')}), flush=True)
    for f_ in (binf, binf + '.surv'):
        if os.path.exists(f_):
            os.remove(f_)
print('SURVEY DONE', flush=True)
