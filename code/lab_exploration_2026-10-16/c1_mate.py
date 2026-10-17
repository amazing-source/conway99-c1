"""(MATE_j): every x in K = ker(3I - A_Omega) has x_a = x_a' on the outer line j = {a, a'}.
If it holds for one j and K_0 = 0 (no 3-eigenvector of Gamma_S with zero letter sums), then nu <= 13.
Per side: K over F_p (p large), number of outer lines with MATE, dim K_0, nu.
usage: python c1_mate.py cache file max | walks f1 ... | rank30 file max"""
import itertools, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, rank_mod, relabel, gl_connected
from c1_newinv import ball
from c1_rs_test import nullspace_mod
P = 1000000007
Bm = [[1 if r in l else 0 for l in S] for r in range(14)]


def mate_info(EE, psd_check=True):
    A = ball(EE)
    M = (3 * np.eye(59, dtype=np.int64) - A).tolist()
    K = nullspace_mod(M, P)
    nu = len(K)
    nmate = 0
    lines = []
    for a in range(4, 14, 2):
        # letter a is vertex 1+a
        ok = all((v[1 + a] - v[2 + a]) % P == 0 for v in K)
        lines.append(ok)
        nmate += ok
    # K_0: kernel vectors vanishing on N[v] (vertices 0..14)
    Kn = np.array(K, dtype=object) if K else None
    k0 = 0
    if K:
        sub = nullspace_mod([[K[b][i] for b in range(nu)] for i in range(15)], P)
        k0 = len(sub)
    psd = None
    if psd_check:
        G = A[15:, 15:].astype(float)
        from c1_margin56 import k8
        K8 = np.array([[k8(x, y) for y in S] for x in S], float)
        psd = bool(np.linalg.eigvalsh(3 * np.eye(44) - G - K8 / 8)[0] > -1e-9)
    return nu, nmate, k0, psd, lines


def main():
    tab = Counter()
    which = sys.argv[1]
    if which == "cache":
        mx = int(sys.argv[3]); done = 0
        for line in open(sys.argv[2]):
            d = json.loads(line)
            if len(d["labels"]) != 44:
                continue
            S0 = [frozenset(x) for x in d["labels"]]
            E0 = [(frozenset(a), frozenset(b)) for a, b in d["edges"]]
            for side in (0, 1):
                L, EE = relabel(S0, E0, side)
                conn, degok = gl_connected(EE)
                if not (conn and degok):
                    continue
                nu, nm, k0, psd, _ = mate_info(EE)
                tab[(psd, nu, nm, k0)] += 1; done += 1
            if done >= mx:
                break
    elif which == "walks":
        for f in sys.argv[2:]:
            d = json.load(open(f))
            lab = [frozenset(x) for x in d["labels"]]
            EE = {frozenset((lab[i], lab[j])) for i, j in d["edges"]}
            r = mate_info(EE)
            print(f.split("/")[-1].split("\\")[-1], "nu", r[0], "lines with MATE", r[1], "K0", r[2], "psd", r[3], r[4])
            tab[r[:4]] += 1
    else:
        d = json.load(open(sys.argv[2]))
        lab = [frozenset(x) for x in d["labels"]]
        for s in d["structures"][: int(sys.argv[3])]:
            EE = {frozenset((lab[i], lab[j])) for i, j in s["edges"]}
            nu, nm, k0, psd, _ = mate_info(EE, psd_check=False)
            tab[(str(s["c"]), nu, nm, k0)] += 1
    print("(positive or c, nu, #outer lines with MATE, dim K_0) : count")
    for k, v in sorted(tab.items(), key=str):
        print("   ", k, v)


if __name__ == "__main__":
    main()
