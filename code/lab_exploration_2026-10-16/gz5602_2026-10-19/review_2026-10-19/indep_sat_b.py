
def model(core, bd, fam, att, sigma):
    lab, A, N, outside, q12, YR, yoff = build(core, bd, fam, att, sigma)
    n = len(lab)
    need = {}
    for u, v in combinations(range(n), 2):
        need[u, v] = (1 if A[u][v] else 2) - len(set(lab[u]) & set(lab[v])) - len(N[u] & N[v])
        if need[u, v] < 0:
            return None
    lq = {}
    for u in range(n):
        for l in range(14):
            lq[u, l] = 2 - (l in lab[u]) - ((l ^ 1) in lab[u]) - sum(1 for w in N[u] if l in lab[w])
            if lq[u, l] < 0:
                return None
    od = {u: 12 - len(N[u]) for u in range(n)}
    doms = []
    for q in outside:
        r = tuple(sorted((q[0] // 2, q[1] // 2)))
        groups = [(list(range(8)), base(r, (0, 1)) + base(r, (0, 2)))]
        if q12:
            groups.append((list(range(8, 12)), base(r, (1, 2))))
        for g, f in enumerate(YR):
            groups.append((list(range(yoff + 4*g, yoff + 4*g + 4)), base(r, f)))
        opts = [()]
        for vs, k in groups:
            opts = [o + c for o in opts for c in combinations(vs, k)]
        good = []
        for o in opts:
            so = set(o)
            if any(lq[v, l] < 1 for v in o for l in q):
                continue
            if any(need[min(a, b), max(a, b)] < 1 for a, b in combinations(o, 2)):
                continue
            if any(len(N[v] & so) > (1 if v in so else 2) - len(set(q) & set(lab[v])) for v in range(n)):
                continue
            if any(sum(1 for v in o if l in lab[v]) > 2 - (l in q) - ((l ^ 1) in q) for l in range(14)):
                continue
            good.append(o)
        doms.append(good)
    return lab, N, outside, need, lq, od, doms

def witness_ok(sel, M):
    lab, N, outside, need, lq, od, doms = M
    for q, o, d in zip(outside, sel, doms):
        if tuple(o) not in d:
            return 'PROFILE_NOT_IN_INDEPENDENT_DOMAIN'
    cnt = {}
    for q, o in zip(outside, sel):
        for a, b in combinations(o, 2):
            cnt['p', a, b] = cnt.get(('p', a, b), 0) + 1
        for u in o:
            cnt['d', u] = cnt.get(('d', u), 0) + 1
            for l in q:
                cnt['l', u, l] = cnt.get(('l', u, l), 0) + 1
    if any(cnt.get(('p', u, v), 0) != t for (u, v), t in need.items()):
        return 'PAIR_COUNT_VIOLATED'
    if any(cnt.get(('l', u, l), 0) != t for (u, l), t in lq.items()):
        return 'LETTER_COUNT_VIOLATED'
    if any(cnt.get(('d', u), 0) != t for u, t in od.items()):
        return 'DEGREE_VIOLATED'
    for a, b in combinations(range(len(outside)), 2):
        if len(set(sel[a]) & set(sel[b])) > 2 - len(set(outside[a]) & set(outside[b])):
            return 'OUTSIDE_C2_VIOLATED'
    return 'WITNESS_OK'

def sat(M):
    lab, N, outside, need, lq, od, doms = M
    if any(not d for d in doms):
        return 'UNSAT(empty domain)', {}
    s = pycryptosat.Solver(threads=1)
    top = [0]
    def new():
        top[0] += 1
        return top[0]
    X = [[new() for _ in d] for d in doms]
    false_lit = new(); s.add_clause([-false_lit])
    def exactly(lits, k):
        m = len(lits)
        if k < 0 or k > m:
            s.add_clause([false_lit]); return
        if k == 0:
            for x in lits: s.add_clause([-x])
            return
        if k == m:
            for x in lits: s.add_clause([x])
            return
        prev = {}
        for i, x in enumerate(lits):
            cur = {}
            for j in range(1, min(i + 1, k + 1) + 1):
                v = new(); cur[j] = v
                a = prev.get(j)
                b = prev.get(j - 1) if j > 1 else True
                if a is not None: s.add_clause([-a, v])
                if b is True: s.add_clause([-x, v])
                elif b is not None: s.add_clause([-x, -b, v])
                s.add_clause([-v, x] + ([a] if a is not None else []))
                if b is not True: s.add_clause([-v] + ([a] if a is not None else []) + ([b] if b is not None else []))
            prev = cur
        s.add_clause([prev[k]]); s.add_clause([-prev[k + 1]])
    for row in X:
        exactly(row, 1)
    feat = {}
    for qi, (q, d) in enumerate(zip(outside, doms)):
        for oi, o in enumerate(d):
            x = X[qi][oi]
            for a, b in combinations(o, 2):
                feat.setdefault(('p', a, b), []).append(x)
            for u in o:
                feat.setdefault(('d', u), []).append(x)
                for l in q:
                    feat.setdefault(('l', u, l), []).append(x)
    for (u, v), t in need.items(): exactly(feat.get(('p', u, v), []), t)
    for (u, l), t in lq.items(): exactly(feat.get(('l', u, l), []), t)
    for u, t in od.items(): exactly(feat.get(('d', u), []), t)
    masks = [[sum(1 << v for v in o) for o in d] for d in doms]
    nc2 = 0
    for a, b in combinations(range(len(outside)), 2):
        cap = 2 - len(set(outside[a]) & set(outside[b]))
        for i, ma in enumerate(masks[a]):
            for j, mb in enumerate(masks[b]):
                if bin(ma & mb).count('1') > cap:
                    s.add_clause([-X[a][i], -X[b][j]]); nc2 += 1
    ok, _ = s.solve()
    return ('SAT' if ok else 'UNSAT'), {'vars': top[0], 'c2': nc2, 'options': sum(len(d) for d in doms)}

if __name__ == '__main__':
    cover, fam, jobs = sys.argv[1], sys.argv[2], sys.argv[3]
    src = json.loads(gzip.decompress(open(cover, 'rb').read()))
    for job in json.load(open(jobs)):
        bd = tuple(bytes.fromhex(src['boundaries_hex'][job['boundary_index']]))
        M = model(src['core'], bd, fam, job['attachment'], job['sigma'])
        if M is None:
            res, info = 'KNOWN_VIOLATION', {}
        elif job.get('selected_profiles'):
            res, info = witness_ok(job['selected_profiles'], M), {}
        else:
            res, info = sat(M)
        print(json.dumps({'b': job['boundary_index'], 'att': job['attachment'], 'sigma': job['sigma'],
                          'expected': job.get('expected'), 'independent': res, 'info': info}), flush=True)
