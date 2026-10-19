"""Entropy budget of the line-local system (LAB 19/10/2026): a first-moment HEURISTIC, not a proof.
For a line of a srg(v,k,1,2), n = k - 2, m = n(n-2)/2 far vertices: the line-local unknown is the pair of bijections
(far -> q-pair, far -> s-pair), (m!)^2 candidates.  log10 E[#solutions] is estimated per labelled G_T as
    2 log10 m!  +  sum over the three class pairs of log10 P(X = K_ab)  +  log10 P(L2)  +  log10 P(L3)
with, for one class pair, X_uv = #{far f : u in p(f), v in q(f)} under a uniform random bijection:
    P(X = K) ~ (2 pi)^(-d/2) det(Sigma)^(-1/2) exp(-(K - mu)^T Sigma^+ (K - mu) / 2),  d = (n-1)^2,
    Sigma = (A (x) A) / (m - 1)  (Hoeffding's combinatorial CLT, exact covariance), A = centred incidence Gram of CP(n/2),
the three pairs treated as independent; L3: each pair of far vertices sharing a p- and a q-letter (sum C(K_pq, 2)) must
not share an s-letter (probability 2(n-3)/(m-1) each, independent); L2: for each far f and each of its 6 names x, the
two G-neighbours of x in the other classes are not both names of f (probability (2/n)^2 each).
Also: counts of labelled G_T (Monte Carlo of K >= 0 and of c = 1), symmetry order (n/2)! 2^(n/2) per class and 3!.
usage: python budget.py <samples> [edges file of a real srg(243) for its real lines]"""
import math
import random
import sys

import numpy as np

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from ll_test import components, extract, gt_matrix, k_matrix, pairs_of  # noqa: E402


def lg_fact(x):
    return math.lgamma(x + 1) / math.log(10)


def class_gram(n):
    P = pairs_of(n)
    m = len(P)
    Inc = np.zeros((n, m))
    for f, (i, j) in enumerate(P):
        Inc[i, f] = Inc[j, f] = 1
    C = Inc - Inc.mean(axis=1, keepdims=True)
    return C @ C.T, m


def pair_logp(n, Kab, A, m):
    """log10 of the Gaussian local-CLT estimate of P(X = Kab) for one class pair"""
    Sigma = np.kron(A, A) / (m - 1)
    w, V = np.linalg.eigh(Sigma)
    keep = w > 1e-9
    d = int(keep.sum())
    mu = 2.0 * (n - 2) / n
    r = (Kab.astype(float) - mu).reshape(-1)
    coef = V[:, keep].T @ r
    quad = float((coef ** 2 / w[keep]).sum())
    logdet = float(np.log(w[keep]).sum())
    return (-0.5 * d * math.log(2 * math.pi) - 0.5 * logdet - 0.5 * quad) / math.log(10), d, quad


def budget(n, s01, s12, s20, A, m):
    G = gt_matrix(n, s01, s12, s20)
    K = k_matrix(n, G)
    blocks = (K[0:n, n:2 * n], K[0:n, 2 * n:3 * n], K[n:2 * n, 2 * n:3 * n])
    lp = [pair_logp(n, B, A, m) for B in blocks]
    L1 = 2 * lg_fact(m) + sum(x[0] for x in lp)
    pshare = 2 * (n - 3) / (m - 1)
    npairs = sum(math.comb(int(x), 2) for x in blocks[0].reshape(-1))
    L3 = npairs * math.log10(1 - pshare)
    L2 = 6 * m * math.log10(1 - (2 / n) ** 2)
    return dict(L1=round(L1, 1), L2=round(L2, 1), L3=round(L3, 1), total=round(L1 + L2 + L3, 1),
                quad=[round(x[2], 1) for x in lp], c=components(G)[0])


def main():
    samples = int(sys.argv[1])
    rng = random.Random(1)
    out = {}
    n = 12
    A, m = class_gram(n)
    ok = conn = 0
    recs = []
    for _ in range(samples):
        s01, s12, s20 = (rng.sample(range(n), n) for _ in range(3))
        K = k_matrix(n, gt_matrix(n, s01, s12, s20))
        if (K < 0).any():
            continue
        ok += 1
        b = budget(n, s01, s12, s20, A, m)
        if b["c"] == 1:
            conn += 1
            recs.append(b)
    lab = 3 * lg_fact(n)
    sym = 3 * (lg_fact(n // 2) + (n // 2) * math.log10(2)) + math.log10(6)
    frac_ok, frac_c1 = ok / samples, conn / samples
    tot = np.array([r["total"] for r in recs])
    l1 = np.array([r["L1"] for r in recs])
    out["conway"] = dict(n=n, far=m, samples=samples, frac_K_nonneg=round(frac_ok, 4), frac_c1=round(frac_c1, 4),
                         log10_labelled_GT_c1=round(lab + math.log10(max(frac_c1, 1e-300)), 2),
                         log10_symmetry=round(sym, 2),
                         log10_classes_GT_c1=round(lab + math.log10(max(frac_c1, 1e-300)) - sym, 2),
                         L1_per_labelled_GT=[round(float(l1.min()), 1), round(float(np.median(l1)), 1),
                                             round(float(l1.max()), 1)],
                         total_per_labelled_GT=[round(float(tot.min()), 1), round(float(np.median(tot)), 1),
                                                round(float(tot.max()), 1)],
                         example=recs[0])
    out["conway"]["log10_expected_classes_c1_L1"] = round(out["conway"]["log10_classes_GT_c1"] + float(np.median(l1)), 1)
    out["conway"]["log10_expected_classes_c1_L123"] = round(out["conway"]["log10_classes_GT_c1"] + float(np.median(tot)), 1)
    if len(sys.argv) > 2:
        n2 = 20
        A2, m2 = class_gram(n2)
        reals = []
        for ln in (0, 57, 200):
            k, nn, T, s01, s12, s20, names = extract(sys.argv[2], ln)
            reals.append(budget(nn, s01, s12, s20, A2, m2))
        rng2 = random.Random(2)
        rnd = []
        tries = 0
        while len(rnd) < 20 and tries < 20000:
            tries += 1
            s01, s12, s20 = (rng2.sample(range(n2), n2) for _ in range(3))
            if (k_matrix(n2, gt_matrix(n2, s01, s12, s20)) < 0).any():
                continue
            rnd.append(budget(n2, s01, s12, s20, A2, m2))
        out["srg243"] = dict(n=n2, far=m2, real_lines=reals,
                             random_GT_total=[min(r["total"] for r in rnd), sorted(r["total"] for r in rnd)[10],
                                              max(r["total"] for r in rnd)],
                             log10_labelled_GT=round(3 * lg_fact(n2), 1),
                             log10_symmetry=round(3 * (lg_fact(n2 // 2) + (n2 // 2) * math.log10(2)) + math.log10(6), 1))
    for nn in (8, 10, 12):
        A3, m3 = class_gram(nn)
        out["planted_n%d" % nn] = dict(far=m3, log10_candidates=round(2 * lg_fact(m3), 1))
    import json
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
