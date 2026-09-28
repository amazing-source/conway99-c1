# Validation of j1a_psd_gen.exe on a given base file (CHECK, independent numpy; not part of the proof runs):
#  - structural identities on every sampled configuration: Mo a = 28 a (a = 1 on star labels, 2 on V's), R^T a = 0,
#    G a = 4 a, Mo kappa = 0 (kappa = c-column of R);
#  - kernel verdicts vs numpy minimum eigenvalues on random configurations (same indexing as the C code).
import struct, subprocess, random, sys, numpy as np
basefile = sys.argv[1]; nrand = int(sys.argv[2]); random.seed(int(sys.argv[3]))
EXE = './j1a_psd_gen.exe'
raw = open(basefile, 'rb').read()
nb = struct.unpack('<i', raw[:4])[0]
V = [struct.unpack('<7b', raw[4 + 7 * k: 11 + 7 * k]) for k in range(3)]
off = 25
bases = [(struct.unpack('<12b', raw[off + 24 * i: off + 24 * i + 12]), struct.unpack('<12b', raw[off + 24 * i + 12: off + 24 * i + 24])) for i in range(nb)]
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
def mats(al, g, edges):
    R = np.zeros((15, 7))
    for L in range(12):
        K = L // 2 + 1; s = 1 if L % 2 == 0 else -1
        R[L, 0] = al[L]; R[L, K] = al[L] * s
    for k in range(3): R[12 + k] = V[k]
    G = np.zeros((15, 15))
    for L in range(12): G[L, 12 + g[L]] = G[12 + g[L], L] = 1
    for x, y in [(12, 13), (13, 14), (12, 14)]: G[x, y] = G[y, x] = 1
    for x, y in edges: G[x, y] = G[y, x] = 1
    Ra = np.abs(R); I = np.eye(15); J = np.ones((15, 15))
    return R, G, (12 * I + 4 * G - R @ R.T, 6 * I - 2 * G - Ra @ Ra.T + J, 8 * I + 2 * G + Ra @ Ra.T - J)
def verdict(M):
    w = np.linalg.eigvalsh(M)[0]
    return 1 if w < -1e-3 else (2 if w < -1e-9 else 0)
mism = 0; hist = {}
for t in range(nrand):
    b = random.randrange(nb); q = random.randrange(720); p1 = random.randrange(15); p2 = random.randrange(15)
    al, g = bases[b]
    Ap = [L for L in range(12) if al[L] == 1]; Am = [L for L in range(12) if al[L] == -1]
    ed = [(Ap[i], Am[perms[q][i]]) for i in range(6)] + [(Ap[x], Ap[y]) for x, y in match6[p1]] + [(Am[x], Am[y]) for x, y in match6[p2]]
    R, G, (Mo, Me, Mc) = mats(al, g, ed)
    a = np.array([1.0] * 12 + [2.0] * 3)
    assert np.allclose(G @ a, 4 * a) and np.allclose(R.T @ a, 0) and np.allclose(Mo @ a, 28 * a) and np.allclose(Mo @ R[:, 0], 0), 'identity failed'
    out = subprocess.run([EXE, 'check', basefile, str(b), str(q), str(p1), str(p2)], capture_output=True, text=True).stdout
    tail = out.split('|')[-1].split(); c = (int(tail[1]), int(tail[3]), int(tail[5]))
    ed_c = [tuple(map(int, s.split('-'))) for s in out.split('|')[2].split()[1:]]
    v = (verdict(Mo), verdict(Me), verdict(Mc))
    if c != v or ed_c != ed: mism += 1; print('MISMATCH', b, q, p1, p2, c, v)
    hist[v] = hist.get(v, 0) + 1
print(basefile, ': random configurations', nrand, ' mismatches', mism, ' identities OK;  verdict histogram', hist)
