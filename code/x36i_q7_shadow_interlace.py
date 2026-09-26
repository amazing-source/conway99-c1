"""Single-shadow interlacing: for the odd ball S_B (19 orbits) plus one far orbit f with column n_f = (block part a_f;
U-shadow s_f = 1_{Phi(z)} - 1_{Phi(sigma z)}), the 20x20 principal submatrix [[S_B, n],[n^T, 0]] of S must have
spectrum in [-4, 3].  How many a-priori shadows (Phi(z), Phi(sigma z) non-mate pairs) survive?"""
import numpy as np, itertools, random
exec(open('x36h_q7_interlace.py', encoding='utf-8').read().split("viol_o = viol_e")[0])
random.seed(3)
stats = []
for trial in range(12):
    tau = random.choice(reps); eta = random.choice(ALL)
    So, Se = balls(tau, eta)
    # odd coordinates: 0 = block c, 1..6 = blocks d (reps 2d i.e. d+), 7..18 = U points w in X
    nonmate = [(b, bp) for b, bp in itertools.combinations(X, 2) if tau[b] != bp]
    far_labels = [(a, ap) for a, ap in itertools.combinations(X, 2) if a // 2 != ap // 2]
    ok = tot = 0
    for (a, ap) in far_labels[:20]:
        for P1 in nonmate:
            for P2 in nonmate[::5]:
                n = np.zeros(19)
                for l in (a, ap):
                    n[1 + l // 2] = 1 if l % 2 == 0 else -1
                for b in P1: n[7 + b] += 1
                for b in P2: n[7 + b] -= 1
                M = np.zeros((20, 20)); M[:19, :19] = So; M[:19, 19] = n; M[19, :19] = n
                ev = np.linalg.eigvalsh(M); tot += 1
                if ev[-1] <= 3 + 1e-9 and ev[0] >= -4 - 1e-9: ok += 1
    stats.append(ok / tot)
print('fraction of a-priori single shadows passing odd interlacing, per random ball:', ['%.3f' % s for s in stats])
