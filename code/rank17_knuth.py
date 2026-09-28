r"""Knuth survey (C1, 28/09 morning): estimated size of the H-canonical skeleton tree, with the partial mod-4 tests (leaves
reached = leaves that the full search would still have to test at the leaf and integer level), per (V, pair).
Usage: python rank17_knuth.py <tag> <pair ids comma-separated> [walks]   (appends to data/rank17/knuth_<tag>.jsonl)"""
import sys, os, json, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rank17_z4export as ex
DATA = os.path.join(HERE, '..', 'data', 'rank17')
WORK = 'C:/home/researcher/AppData/Local/Temp/claude/runs/knuth'
EXE = os.path.join(HERE, 'rank17_z4_k.exe')
TAGSUFFIX = os.environ.get('KNUTH_SUFFIX', '')

tag, ids = sys.argv[1], [int(x) for x in sys.argv[2].split(',')]
walks = int(sys.argv[3]) if len(sys.argv) > 3 else 300
os.makedirs(WORK, exist_ok=True)
for pid in ids:
    binf = os.path.join(WORK, '%s_%d.bin' % (tag, pid))
    t0 = time.time()
    info = ex.export(tag, pid, binf)
    r = subprocess.run([EXE, binf, 'run', binf + '.surv'], capture_output=True, text=True, timeout=3600,
                       env=dict(os.environ, Z4_KNUTH=str(walks)))
    js = [l for l in r.stdout.splitlines() if l.startswith('{')]
    rec = {'tag': tag, 'pair': pid, 'classes': info['classes'], 'export_s': info['export_s']}
    if js:
        rec.update(json.loads(js[0]))
    else:
        rec['error'] = r.stderr[-300:]
    rec['total_s'] = round(time.time() - t0, 1)
    print(json.dumps(rec), flush=True)
    with open(os.path.join(DATA, 'knuth%s_%s.jsonl' % (TAGSUFFIX, tag)), 'a') as f:
        f.write(json.dumps(rec) + chr(10))
    for f_ in (binf, binf + '.surv'):
        if os.path.exists(f_):
            os.remove(f_)
