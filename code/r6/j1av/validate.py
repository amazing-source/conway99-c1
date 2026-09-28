# Validation of j1av_psd.exe (CHECK, independent numpy eigenvalues; not part of the proof run).
# 1. Replicates the C indexing (base list, 720 perms by recursive swaps, 15 matchings) in Python.
# 2. Maps structures' 13 sampled odd-survivors to (b, q, p1, p2) and compares C verdicts with numpy minima.
# 3. Random (b, q, p1, p2): C verdict vs numpy minimum eigenvalue (kill <=> lambda_min < -1e-9).
import json, struct, subprocess, random, numpy as np, sys
EXE = './j1av_psd.exe'
nb = struct.unpack('<i', open('base.bin', 'rb').read(4))[0]
raw = open('base.bin', 'rb').read()[4:]
bases = []
for i in range(nb):
    rec = struct.unpack('<6b12b', raw[18 * i:18 * i + 18]); bases.append((rec[:6], rec[6:]))
base_index = {(tuple(a), tuple(g)): i for i, (a, g) in enumerate(bases)}
perms = []
def gen(arr, k):
    if k == 6: perms.append(arr[:]); return
    for i in range(k, 6):
        arr[k], arr[i] = arr[i], arr[k]; gen(arr, k + 1); arr[k], arr[i] = arr[i], arr[k]
gen(list(range(6)), 0)
match6 = []
for j in range(1, 6):
    rest = [x for x in range(1, 6) if x != j]
    for t in [((rest[0], rest[1]), (rest[2], rest[3])), ((rest[0], rest[2]), (rest[1], rest[3])), ((rest[0], rest[3]), (rest[1], rest[2]))]:
        match6.append([(0, j), t[0], t[1]])
assert len(perms) == 720 and len(match6) == 15
def ApAm(a):
    Ap, Am = [], []
    for K in range(1, 7):
        for si in (0, 1):
            L = 2 * (K - 1) + si
            (Ap if a[K - 1] == 1 else Am).append(L)
    return Ap, Am
def mats(a, g, edges):
    R = np.zeros((15, 7))
    for K in range(1, 7):
        for si, s in ((0, 1), (1, -1)):
            L = 2 * (K - 1) + si; R[L, 0] = a[K - 1]; R[L, K] = a[K - 1] * s
    R[12, 1], R[12, 2], R[13, 2], R[13, 3], R[14, 3], R[14, 1] = 1, -1, 1, -1, 1, -1
    G = np.zeros((15, 15))
    for L in range(12): G[L, 12 + g[L]] = G[12 + g[L], L] = 1
    for x, y in [(12, 13), (13, 14), (12, 14)]: G[x, y] = G[y, x] = 1
    for x, y in edges: G[x, y] = G[y, x] = 1
    Ra = np.abs(R); I = np.eye(15); J = np.ones((15, 15))
    return (12 * I + 4 * G - R @ R.T, 6 * I - 2 * G - Ra @ Ra.T + J, 8 * I + 2 * G + Ra @ Ra.T - J)
def verdict(M):
    w = np.linalg.eigvalsh(M)[0]
    return (1 if w < -1e-3 else (2 if w < -1e-9 else 0)), w
def c_check(b, q, p1, p2):
    out = subprocess.run([EXE, 'check', 'base.bin', str(b), str(q), str(p1), str(p2)], capture_output=True, text=True).stdout
    tail = out.split('|')[-1].split()
    return int(tail[1]), int(tail[3]), int(tail[5]), out
def edges_py(a, q, p1, p2):
    Ap, Am = ApAm(a)
    ed = [(Ap[i], Am[perms[q][i]]) for i in range(6)]
    ed += [(Ap[x], Ap[y]) for x, y in match6[p1]] + [(Am[x], Am[y]) for x, y in match6[p2]]
    return ed
# --- 2. structures' survivors
def lab_of(name):   # 'cK+' -> index
    K = int(name[1]); s = name[2]
    return 2 * (K - 1) + (0 if s == '+' else 1)
d = json.load(open('C:/home/researcher/Desktop/conway99-rank17/r8_data/j1a_v_odd_survivors.json'))
ok = 0
for e in d:
    a = [e['a']['c%d+' % K] for K in range(1, 7)]
    gmap = e['group(W index 1..3, v_k = e_k - e_{k+1 mod 3})']
    g = [0] * 12
    for nm, w in gmap.items(): g[lab_of(nm)] = w - 1
    b = base_index.get((tuple(a), tuple(g)))
    assert b is not None, 'structures config not in my base list: %s %s' % (a, g)
    Ap, Am = ApAm(a)
    Qp = {}
    for x, y in e['Q_pairs(rep-rep adjacent in O_c+)']:
        lx, ly = lab_of(x), lab_of(y)
        if lx in Am: lx, ly = ly, lx
        Qp[Ap.index(lx)] = Am.index(ly)
    q = perms.index([Qp[i] for i in range(6)])
    Pp, Pm = [], []
    for x, y in e['P_pairs(rep_u ~ sigma rep_w)']:
        lx, ly = lab_of(x), lab_of(y)
        if lx in Ap: Pp.append(tuple(sorted((Ap.index(lx), Ap.index(ly)))))
        else: Pm.append(tuple(sorted((Am.index(lx), Am.index(ly)))))
    key = lambda m: sorted(tuple(sorted(pr)) for pr in m)
    p1 = [key(m) for m in match6].index(sorted(Pp)); p2 = [key(m) for m in match6].index(sorted(Pm))
    co, ce, cc, _ = c_check(b, q, p1, p2)
    Mo, Me, Mc = mats(a, g, edges_py(a, q, p1, p2))
    (vo, wo), (ve, we), (vc, wc) = verdict(Mo), verdict(Me), verdict(Mc)
    same = (co, ce, cc) == (vo, ve, vc)
    ok += same
    print('structures #%d -> b=%d q=%d p1=%d p2=%d  C(odd,even,comp)=%s  numpy=%s  mins %.3f %.3f %.3f  %s' % (
        d.index(e), b, q, p1, p2, (co, ce, cc), (vo, ve, vc), wo, we, wc, 'OK' if same else 'MISMATCH'))
print('structures configs matching:', ok, '/', len(d))
# --- 3. random configurations
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
mism = 0; nrand = int(sys.argv[2]) if len(sys.argv) > 2 else 300
kinds = {}
for t in range(nrand):
    b = random.randrange(nb); q = random.randrange(720); p1 = random.randrange(15); p2 = random.randrange(15)
    co, ce, cc, out = c_check(b, q, p1, p2)
    a, g = bases[b]
    Mo, Me, Mc = mats(a, g, edges_py(a, q, p1, p2))
    vo, ve, vc = verdict(Mo)[0], verdict(Me)[0], verdict(Mc)[0]
    ed_c = [tuple(map(int, s.split('-'))) for s in out.split('|')[2].split()[1:]]
    if ed_c != edges_py(a, q, p1, p2) or (co, ce, cc) != (vo, ve, vc):
        mism += 1; print('MISMATCH', b, q, p1, p2, (co, ce, cc), (vo, ve, vc))
    kinds[(vo, ve, vc)] = kinds.get((vo, ve, vc), 0) + 1
print('random configurations:', nrand, ' mismatches:', mism, ' verdict histogram (odd,even,comp):', kinds)
