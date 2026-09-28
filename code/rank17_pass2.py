r"""Rank-17 PASS 2 driver (C1, 28/09 ~04:40): every y-pair of the given V types, exhaustively.
Per (V, pair), in a memory-capped child (run_capped.ps1): rank17_z4export.py -> rank17_z4.exe run (H-canonical skeleton
enumeration, partial and full exact mod-4 test). Verdict per pair:
  EXCLUDED   complete enumeration, no skeleton survives the mod-4 relaxation
             (label COMPUTED: class filters of rank17_skeleton + SPEC section-1 domains + exact mod-4 relaxation)
  MOD4_FEASIBLE  a skeleton passes the mod-4 relaxation (the search stops at the first one): not excluded here
  UNDECIDED  timeout / crash
Several drivers can run at once (claim files). Results: data/rank17/z4_<tag>.jsonl.
Usage: python rank17_pass2.py <tags comma-separated>   (child mode: rank17_pass2.py child <tag> <pair>)"""
import sys, os, json, time, hashlib, subprocess, socket
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data', 'rank17')
WORK = 'C:/home/researcher/AppData/Local/Temp/claude/runs/pass2'
CAPPED = 'C:/home/researcher/.claude/tools/run_capped.ps1'
EXE = os.path.join(HERE, 'rank17_z4.exe')


def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:16]


def child(tag, pid):
    sys.path.insert(0, HERE)
    import rank17_z4export as ex
    os.makedirs(WORK, exist_ok=True)
    binf = os.path.join(WORK, '%s_%d.bin' % (tag, pid))
    survf = os.path.join(WORK, '%s_%d.surv' % (tag, pid))
    info = ex.export(tag, pid, binf)
    t0 = time.time()
    env = dict(os.environ, Z4_MAXSURV='1')                  # classification: stop at the first mod-4 survivor
    r = subprocess.run([EXE, binf, 'run', survf], capture_output=True, text=True, timeout=7200, env=env)
    js = [l for l in r.stdout.splitlines() if l.startswith('{')]
    out = {'tag': tag, 'pair': pid, 'V': info['V'], 'classes': info['classes'], 'H_generators': info['H_generators'],
           'export_s': info['export_s'], 'returncode': r.returncode}
    if js:
        d = json.loads(js[0])
        out.update({k: d[k] for k in ('skeletons', 'empty', 'z4_killed', 'survivors', 'nodes', 'sigma_mismatch', 'complete',
                                      'partial_tested', 'partial_pruned')})
        out['run_s'] = round(time.time() - t0, 1)
    ok = js and r.returncode == 0 and out['sigma_mismatch'] == 0
    if ok and out['complete'] and out['survivors'] == 0:
        out['verdict'] = 'EXCLUDED'
        out['label'] = ('COMPUTED (pass 2: exhaustive H-canonical skeleton enumeration; class filters + SPEC section-1 '
                        'domains + exact mod-4 relaxation)')
        os.remove(binf)
        if os.path.exists(survf) and os.path.getsize(survf) == 0:
            os.remove(survf)
    elif ok and out['survivors'] > 0:
        out['verdict'] = 'MOD4_FEASIBLE'
        out['first_survivor'] = open(survf).read().split(chr(10))[0] if os.path.exists(survf) else None
        out['label'] = ('a skeleton passes the mod-4 relaxation (search stopped at the first one): '
                        'NOT excluded here, needs the integer level')
        os.remove(binf)
    else:
        out['verdict'] = 'UNDECIDED'
        out['label'] = 'engine error or incomplete'
        out['stderr_tail'] = r.stderr[-400:]
    out['engine_sha'] = sha(EXE); out['exporter_sha'] = sha(os.path.join(HERE, 'rank17_z4export.py'))
    out['source_sha'] = sha(os.path.join(HERE, 'rank17_z4.c')); out['machine'] = socket.gethostname()
    print('RESULT ' + json.dumps(out), flush=True)


def driver(tags, claims='claims2'):
    os.makedirs(os.path.join(WORK, claims), exist_ok=True)
    for tag in tags:
        K = json.load(open(os.path.join(DATA, 'K_%s.json' % tag)))
        ids = [r['id'] for r in K['K']]
        outf = os.path.join(DATA, 'z4_%s.jsonl' % tag)
        print('PASS2', tag, 'pairs', len(ids), flush=True)
        for pid in ids:
            if os.path.exists(outf) and pid in {json.loads(l)['pair'] for l in open(outf) if l.strip()
                                                 and json.loads(l)['verdict'] in ('EXCLUDED', 'MOD4_FEASIBLE')}:
                continue
            try:
                os.close(os.open(os.path.join(WORK, claims, '%s_%d' % (tag, pid)), os.O_CREAT | os.O_EXCL | os.O_WRONLY))
            except FileExistsError:
                continue
            log = os.path.join(WORK, '%s_%d.log' % (tag, pid))
            subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', CAPPED, '-LimitMB', '1500',
                            '-TimeoutSec', '7500', '-MinFreeMB', '3000', '-Log', log, '-Exe', sys.executable,
                            '-ArgList', '%s child %s %d' % (os.path.abspath(__file__), tag, pid), '-WorkDir', WORK],
                           capture_output=True, text=True)
            txt = open(log + '.out').read() if os.path.exists(log + '.out') else ''
            line = [l for l in txt.splitlines() if l.startswith('RESULT ')]
            if not line:
                tail = open(log).read().strip().splitlines()[-1:] if os.path.exists(log) else ['no log']
                rec = {'tag': tag, 'pair': pid, 'verdict': 'UNDECIDED', 'label': 'child failed', 'log_tail': tail}
            else:
                rec = json.loads(line[0][7:])
            with open(outf, 'a') as f:
                f.write(json.dumps(rec) + chr(10))
            print(json.dumps({k: rec.get(k) for k in ('tag', 'pair', 'verdict', 'skeletons', 'survivors', 'nodes',
                                                      'export_s', 'run_s')}), flush=True)
    print('PASS2 DONE', ','.join(tags), flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'child':
        child(sys.argv[2], int(sys.argv[3]))
    elif len(sys.argv) > 2 and sys.argv[2] == 'retry':          # a fresh claim space: retries UNDECIDED pairs only
        driver(sys.argv[1].split(','), claims='claims_retry_%d' % int(time.time() // 3600))
    else:
        driver(sys.argv[1].split(','))
