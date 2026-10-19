# Independent existence test of a Q12 colouring: split the 24 copies of T into 4 simple graphs F_j with
# deg_{F_j}(v) = 2 - |letters(v) & letters(Q12_j)|  (no forbidden-triple filter: the bare factor lemma).
import json, sys
from itertools import combinations, product
cores = json.load(open(sys.argv[1] + "/paircores8.json"))
reps = [0, 1, 6, 7, 8, 9, 10, 20, 21, 22, 23, 25, 26, 27, 30, 45, 47, 50, 51, 52, 75, 76, 88]
CORE = [(s, 2*r+t) for r in (1, 2) for s, t in product(range(2), repeat=2)]
Q12 = [(2 + j // 2, 4 + j % 2) for j in range(4)]
deg0 = [[2 - len(set(CORE[v]) & set(Q12[j])) for v in range(8)] for j in range(4)]
for ci in reps:
    T = {(u, v): cores[ci]['T']['%d-%d' % (u, v)] for u, v in combinations(range(8), 2)}
    copies = [e for e, n in sorted(T.items()) for _ in range(n)]
    d = [list(r) for r in deg0]; cls = [set() for _ in range(4)]; last = [0] * len(copies); nsol = [0]
    def bt(i):
        if i == len(copies):
            if all(x == 0 for r in d for x in r): nsol[0] += 1
            return nsol[0] >= 1
        e = copies[i]; u, v = e
        for j in range(4):
            if e in cls[j] or d[j][u] == 0 or d[j][v] == 0: continue
            if i and copies[i-1] == e and j < last[i-1]: continue
            cls[j].add(e); d[j][u] -= 1; d[j][v] -= 1; last[i] = j
            if bt(i + 1): return True
            cls[j].discard(e); d[j][u] += 1; d[j][v] += 1
        return False
    print(ci, 'colouring exists' if bt(0) else 'NO COLOURING')
