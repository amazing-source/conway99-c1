"""Crash-proof cube-and-conquer for the S3 parity skeleton (s3grid.py model) with CryptoMiniSat assumptions.
Cube = root case (A|B1|B2|B3) + patterns (s1,s2,s3) in {000,100,010,001,111} for the first d pairs (0,R) of ORDER.
A cube not decided within TL seconds is SPLIT into the <= 5 patterns of the next pair: the children cover it exactly.
Ledger: ledger.jsonl (append, flock + fsync).  python3 s3cubes.py init | work TL | status"""
import sys, os, json, time, fcntl, itertools, collections, random
sys.argv_saved = list(sys.argv); sys.argv = ['x']
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 's3grid.py')).read().split('if __name__')[0])
sys.argv = sys.argv_saved
D = os.path.dirname(os.path.abspath(__file__)); LED = os.path.join(D, 'ledger.jsonl'); LOCK = LED + '.lock'
PATS = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)]
def build(TL=1e9):
    import pycryptosat
    sol = pycryptosat.Solver(threads=1, time_limit=TL)
    nv = [0]
    def new(): nv[0] += 1; return nv[0]
    E = {}
    for i in range(n):
        for j in adj[i]:
            if i < j: E[(i, j)] = E[(j, i)] = new()
    seen, dq, tree = {0}, collections.deque([0]), []
    while dq:
        u = dq.popleft()
        for v in sorted(nbs[u]):
            if v not in seen: seen.add(v); dq.append(v); tree.append((u, v))
    for u, v in tree: sol.add_clause([-E[(u, v)]])
    for d in dirs:
        for x in range(n):
            y = I[add(V[x], d)]; z = I[add(V[y], d)]
            if x < y and x < z: sol.add_xor_clause([E[(x, y)], E[(y, z)], E[(x, z)]], False)
    B = {}
    def bvar(P, Z, R):
        if (P, Z, R) not in B:
            t = new(); sol.add_xor_clause([E[(P, Z)], E[(Z, R)], t], False); B[(P, Z, R)] = t
        return B[(P, Z, R)]
    SQ = {}
    for P in range(n):
        for R in range(P + 1, n):
            if R in nbs[P]: continue
            gp = grid_pairs(P, R); bs = [(bvar(P, Z, R), bvar(P, Z2, R)) for Z, Z2 in gp]; s = []
            for b1, b2 in bs:
                v = new(); sol.add_xor_clause([b1, b2, v], False); s.append(v)
            SQ[(P, R)] = s; s1, s2, s3 = s
            sol.add_clause([-s1, -s2, s3]); sol.add_clause([-s1, s2, -s3]); sol.add_clause([s1, -s2, -s3])
            r = [bs[0][0], bs[1][0], bs[2][0]]
            for j, k in ((0, 1), (1, 2)):
                sol.add_clause([s1, s2, s3, -r[j], r[k]]); sol.add_clause([s1, s2, s3, r[j], -r[k]])
            for i in range(3):
                j, k = [t for t in range(3) if t != i]; base = [-s[i], s[j], s[k]]
                sol.add_clause(base + [r[j], r[k]]); sol.add_clause(base + [-r[j], -r[k]])
    return sol, E, SQ
R0 = min(R for R in range(1, n) if R not in nbs[0])
ORDER = [R for R in range(1, n) if R not in nbs[0] and R != R0]       # pairs (0,R) to split on, in index order
ROOT = {'A': (1, 1, 1), 'B1': (1, 0, 0), 'B2': (0, 1, 0), 'B3': (0, 0, 1)}
def lits(cube, SQ):
    out = [v if b else -v for v, b in zip(SQ[(0, R0)], ROOT[cube['root']])]
    for R, p in zip(ORDER, cube['pats']):
        out += [v if b else -v for v, b in zip(SQ[(0, R)], PATS[p])]
    return out
def cid(c): return c['root'] + ('.' + '.'.join(map(str, c['pats'])) if c['pats'] else '')
def append(rec):
    with open(LOCK, 'a') as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        with open(LED, 'a') as f: f.write(json.dumps(rec) + '\n'); f.flush(); os.fsync(f.fileno())
        fcntl.flock(lk, fcntl.LOCK_UN)
def state():
    st = {}
    if os.path.exists(LED):
        for line in open(LED):
            if line.strip():
                r = json.loads(line); st[r['id']] = r
    return st
if sys.argv[1] == 'init':
    if not os.path.exists(LED):
        for rt in ROOT: append({'id': rt, 'root': rt, 'pats': [], 'st': 'PENDING', 't': time.time()})
    print('init ok')
elif sys.argv[1] == 'status':
    st = state(); cnt = collections.Counter(r['st'] for r in st.values())
    print(dict(cnt), 'solver-seconds:', int(sum(r.get('secs', 0) for r in st.values())))
    for r in st.values():
        if r['st'] in ('RUNNING', 'SAT'): print(' ', r['id'], r['st'], r.get('pid'))
elif sys.argv[1] == 'work':
    TL = float(sys.argv[2])
    alive = lambda pid: bool(pid) and os.path.exists(f'/proc/{pid}')
    while True:
        st = state()
        if any(r['st'] == 'SAT' for r in st.values()): print('SAT found, stopping', flush=True); break
        todo = [r for r in st.values() if r['st'] == 'PENDING' or (r['st'] == 'RUNNING' and not alive(r.get('pid')))]
        if not todo:
            if not any(r['st'] == 'RUNNING' for r in st.values()): print('all cubes decided', flush=True); break
            time.sleep(20); continue
        todo.sort(key=lambda r: (len(r['pats']), r['id'])); c = random.choice(todo[:4])
        append(dict(c, st='RUNNING', pid=os.getpid(), t=time.time()))
        time.sleep(1 + random.random())
        if state()[c['id']].get('pid') != os.getpid(): continue
        t0 = time.time(); sol, E, SQ = build(TL); res, model = sol.solve(lits(c, SQ)); dt = time.time() - t0
        if res is True:
            append(dict(c, st='SAT', secs=dt, t=time.time(), eps={f'{a}-{b}': int(model[v]) for (a, b), v in E.items() if a < b}))
            print('SAT', cid(c), flush=True); break
        if res is False:
            append(dict(c, st='UNSAT', secs=dt, t=time.time())); print('UNSAT', cid(c), int(dt), flush=True); continue
        d = len(c['pats'])
        if d >= len(ORDER): append(dict(c, st='STUCK', secs=dt, t=time.time())); continue
        kids = []
        for p in range(5):
            k = {'id': cid({'root': c['root'], 'pats': c['pats'] + [p]}), 'root': c['root'], 'pats': c['pats'] + [p], 'st': 'PENDING', 't': time.time()}
            append(k); kids.append(k['id'])
        append(dict(c, st='SPLIT', secs=dt, t=time.time(), kids=kids)); print('SPLIT', cid(c), flush=True)
