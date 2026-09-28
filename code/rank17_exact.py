r"""Exact closure of small rank-17 pairs (C1, 28/09): stage 1 = rank17_z4.exe (H-canonical skeletons, DC, partial and full
mod-4 test, integer phi forward checking, Z4_INTPHI=2 writes every (skeleton, phi) still alive); stage 2 = structures'
sbdfs_g on the phi-restricted SPEC domains of each alive (skeleton, phi) (pairwise rule, stars, PSD, exact leaf).
Verdict EXCLUDED (COMPUTED) iff stage 1 is complete and every stage-2 run is EXCLUDED. A FOUND anywhere stops everything.
Usage: python rank17_exact.py <tag> <pair>            (appends to data/rank17/exact_<tag>.jsonl)"""
import sys, os, json, time, subprocess, hashlib, socket
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, 'C:/home/researcher/Desktop/conway99-rank17/z17')
DATA = os.path.join(HERE, '..', 'data', 'rank17')
WORK = 'C:/home/researcher/AppData/Local/Temp/claude/runs/exact'
EXE = os.path.join(HERE, 'rank17_z4_exact.exe')


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def stage2(tag, pid, phif):
    import rank17_engine as eng
    import stageB
    from rank17_vsearch import CELLS
    case = eng.Case(tag, pid)
    nB = case.nB
    G24 = np.zeros((7 + nB, 7 + nB), dtype=np.int64); G24[:7, :7] = np.eye(7, dtype=np.int64); G24[7:, 7:] = case.Gv
    groups = {}
    for l in open(phif):
        t = l.split()
        if len(t) == 14 and t[0] == 'S' and t[7] == 'M':
            groups.setdefault(tuple(int(x) for x in t[1:7]), []).append([int(x) for x in t[8:14]])
    verdicts = {}
    os.makedirs(os.path.join(WORK, 'sb'), exist_ok=True)
    for S, Ms in groups.items():
        S = list(S)
        gv = [((np.array([(g >> i) & 1 for i in range(15)], dtype=np.int64)) @ case.Kv) % 2 for g in S]
        b = []
        for d in range(2, 8):
            v = np.zeros(7 + nB, dtype=np.int64); v[0] = 1; v[d - 1] = 1; v[7:] = gv[d - 2]; b.append(v)
        b = np.array(b); bG = b @ G24
        kap = {}
        for c in range(6):
            for d in range(c + 1, 6):
                kap[(c, d)] = int(sum(1 << e for e in range(6) if int(((b[c] * b[d]) @ G24 @ b[e]) % 2)))
        doms = case.domains(S)
        sig = []
        for (c, d), (P, Mn) in zip(CELLS, doms):
            ep = np.zeros(7, dtype=np.int64); ep[c - 1] = 1; ep[d - 1] = 1
            Q = np.hstack([np.tile(ep, (len(P), 1)), np.asarray(P, dtype=np.int64)])
            x = ((Q - Q % 2) % 4) // 2
            sig.append(((x @ bG.T) % 2) @ (1 << np.arange(6)))
        for M in Ms:
            def phi(c, d):
                return M[d - 2] if c == 1 else M[c - 2] ^ M[d - 2] ^ kap[(c - 2, d - 2)]
            rd = []
            for k, ((c, d), (P, Mn)) in enumerate(zip(CELLS, doms)):
                keep = sig[k] == phi(c, d)
                rd.append((np.asarray(P)[keep], np.asarray(Mn)[keep]))
            path = os.path.join(WORK, 'sb', '%s_%d_%d.bin' % (tag, pid, os.getpid()))
            if any(len(P) == 0 for P, _ in rd):
                v = 'EXCLUDED'
            else:
                stageB.export_g(path, 10 ** 8, case.Gv, case.M, rd)
                r = stageB.solve_g(path)
                os.remove(path)
                v = r['verdict']
                if v == 'FOUND':
                    print('FOUND!!! skeleton', S, 'phi', M, flush=True)
            verdicts[v] = verdicts.get(v, 0) + 1
    return len(groups), sum(len(m) for m in groups.values()), verdicts


def main(tag, pid):
    import rank17_z4export as ex
    os.makedirs(WORK, exist_ok=True)
    binf = os.path.join(WORK, '%s_%d.bin' % (tag, pid)); phif = binf + '.phi'
    t0 = time.time()
    info = ex.export(tag, pid, binf)
    r = subprocess.run([EXE, binf, 'run', phif], capture_output=True, text=True, timeout=10 ** 6,
                       env=dict(os.environ, Z4_INTPHI='2', Z4_DC='1'))
    js = [l for l in r.stdout.splitlines() if l.startswith('{')]
    s1 = json.loads(js[0]) if js else {'error': r.stderr[-300:]}
    t1 = time.time()
    nsk, nphi, verd = stage2(tag, pid, phif) if js else (0, 0, {})
    ok1 = bool(js) and s1.get('complete') and s1.get('sigma_mismatch') == 0 and r.returncode == 0
    if ok1 and set(verd) <= {'EXCLUDED'}:
        verdict = 'EXCLUDED'
        label = ('COMPUTED (exact: H-canonical skeletons; class filters + DC (PROVEN, user handoff) + SPEC domains + mod-4 + '
                 'integer phi FC; every surviving (skeleton, phi) excluded by sbdfs_g)')
    elif 'FOUND' in verd:
        verdict, label = 'FOUND', 'a phi-restricted skeleton has a frame: LOOK AT IT'
    else:
        verdict, label = 'UNDECIDED', 'stage 1 incomplete or a solver LIMIT'
    rec = {'tag': tag, 'pair': pid, 'verdict': verdict, 'label': label,
           'stage1': {k: s1.get(k) for k in ('skeletons', 'empty', 'z4_killed', 'survivors', 'nodes', 'complete', 'int_killed',
                                              'int_survivors', 'leaf_pre_killed', 'dc_forbidden')},
           'stage1_s': round(t1 - t0, 1), 'stage2_skeletons': nsk, 'stage2_phi': nphi, 'stage2_verdicts': verd,
           'stage2_s': round(time.time() - t1, 1), 'engine_sha': sha(EXE), 'machine': socket.gethostname()}
    with open(os.path.join(DATA, 'exact_%s.jsonl' % tag), 'a') as f:
        f.write(json.dumps(rec) + chr(10))
    print(json.dumps(rec), flush=True)
    for f_ in (binf,):
        if os.path.exists(f_):
            os.remove(f_)


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))
