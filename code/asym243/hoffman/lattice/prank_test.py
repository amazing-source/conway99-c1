# Test of the structural claim used for srg(99,14,1,2):
#   ker_p(A - sI) = (K + Gamma_r) mod p,  K = Z^n ∩ E_s, Gamma_r = Z^n ∩ E_r,
# hence rank_p(A - sI) = 1 + (p-rank of disc K)  when p | r-s, p ∤ k-s, p ∤ n, p ∤ t.
import networkx as nx, itertools, sys
def rank_mod(M, p):
    M = [[x % p for x in row] for row in M]; r = 0
    rows = len(M); cols = len(M[0]) if M else 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c]), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]; inv = pow(M[r][c], p - 2, p)
        M[r] = [(x * inv) % p for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c]:
                f = M[i][c]; M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        r += 1
    return r
def int_kernel(M):
    # integer column operations on M (m x n), tracked in U (n x n); zero columns of M*U give a Z-basis of ker
    m, n = len(M), len(M[0])
    C = [[M[i][j] for i in range(m)] for j in range(n)]          # columns
    U = [[int(i == j) for i in range(n)] for j in range(n)]      # columns of U
    row = 0; start = 0
    for row in range(m):
        while True:
            nz = [j for j in range(start, n) if C[j][row] != 0]
            if len(nz) <= 1: break
            j0 = min(nz, key=lambda j: abs(C[j][row]))
            for j in nz:
                if j == j0: continue
                q = C[j][row] // C[j0][row]
                C[j] = [a - q * b for a, b in zip(C[j], C[j0])]
                U[j] = [a - q * b for a, b in zip(U[j], U[j0])]
        nz = [j for j in range(start, n) if C[j][row] != 0]
        if nz:
            j0 = nz[0]
            C[start], C[j0] = C[j0], C[start]; U[start], U[j0] = U[j0], U[start]
            start += 1
    return [U[j] for j in range(start, n)]
def test(name, G, p):
    nodes = sorted(G.nodes()); idx = {v: i for i, v in enumerate(nodes)}; n = len(nodes)
    A = [[0] * n for _ in range(n)]
    for u, v in G.edges(): A[idx[u]][idx[v]] = A[idx[v]][idx[u]] = 1
    import numpy as np
    ev = sorted(set(int(round(x)) for x in np.linalg.eigvalsh(np.array(A, float))))
    s, r, k = ev[0], ev[1], ev[2]
    As = [[A[i][j] - s * (i == j) for j in range(n)] for i in range(n)]
    Ar = [[A[i][j] - r * (i == j) for j in range(n)] for i in range(n)]
    K = int_kernel(As); Gr = int_kernel(Ar)
    rho = rank_mod(As, p)
    span = rank_mod(K + Gr, p)
    gram = [[sum(a * b for a, b in zip(x, y)) for y in K] for x in K]
    m = len(K) - rank_mod(gram, p)
    print(f"{name}: n={n} k={k} r={r} s={s} p={p} | rank_p(A-sI)={rho}  n-dim(K+Gr mod p)={n-span}  m=p-rank disc K={m}  -> rho==m+1: {rho==m+1}")
if __name__ == "__main__":
    test("Petersen", nx.petersen_graph(), 3)
    test("T(7)", nx.line_graph(nx.complete_graph(7)), 5)
    test("T(8)", nx.line_graph(nx.complete_graph(8)), 3)
    test("T(10)", nx.line_graph(nx.complete_graph(10)), 3)
    test("T(11)", nx.line_graph(nx.complete_graph(11)), 3)
    test("complement Petersen", nx.complement(nx.petersen_graph()), 3)
