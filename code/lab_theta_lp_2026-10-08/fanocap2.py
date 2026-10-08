"""C1, lab session, 2026-10-08. The seed-packing cap on the Fano vectors, a_7 <= 990, in the exact LP.
  python fanocap2.py <N> [CAP ...]
Claim (NOTE.md 17.10, hand argument, uses Lemma F and min(L) >= 14): at a vertex p0, two different seeds (p0; U), (p0; U')
that both extend to a Fano vector share at most two neighbours. The 280 triples of pairwise non-adjacent neighbours of p0
are then each in at most one extending seed, so at most 70 seeds extend at p0 and a_7 <= 99 * 70 / 7 = 990.
Two settings per rank:
  AUDITED : margins.py (b_2 >= 462, b_3 >= 24948, b_4 >= 1431738, Codex's note-175 b_5..b_8, 7a_7 + 8a_8 <= 55440, b_1 <= 88);
  NEW     : r35.py with Codex's corrected bound b_4 >= 3826746 - 30 P - 4572 rho (twin prisms subtracted), P and rho free."""
import sys
from fractions import Fraction as Fr
import theta_lp as T
import theta_lp_exact as X
import r35 as R
T.selfcheck()
LOW = {2: 462, 3: 24948, 4: 1431738, 5: 18001368, 6: 86272956, 7: 208016424, 8: 263126556}
for CAP in ([int(x) for x in sys.argv[2:]] or [990]):
    for d in (34, 36, 38, 40, 42):
        A, B, C = X.build(d, "ext"); C = [c for c in C if not c[0].startswith(("b_2 >=", "b_3 >=", "b_4 >=", "b_5 >="))]
        for n, lo in LOW.items(): C.append(("b_%d >= %d" % (n, lo), T.add(B[n], T.aff(lo), -1)))
        C.append(("7 a_7 + 8 a_8 <= 55440", T.add(T.aff(55440), T.add(T.sc(A[7], 7), T.sc(A[8], 8)), -1)))
        C.append(("b_1 <= 88", T.add(T.aff(88), B[1], -1))); C.append(("a_7 <= %d" % CAP, T.add(T.aff(CAP), A[7], -1)))
        st = X.feasible(C)
        if st[0] == "infeasible":
            m = min(l for _, l in st[1]); line = "INFEASIBLE; certificate: " + "; ".join("%s x %s" % (nm, X.show(l / m)) for nm, l in st[1])
        else:
            lad = None
            for mm in range(8, 16):
                if X.feasible(C + [("a_%d <= 0" % n, T.sc(A[n], -1)) for n in range(8, mm)])[0] == "infeasible": lad = 2 * (mm - 1); break
            s = T.aff(0)
            for n in range(8, 14): s = T.add(s, A[n])
            line = "feasible; a vector of norm 16..%s is forced; min(a_8+..+a_13) = %s" % (lad, X.show(X.minimise(C, s)[1]))
        print("a_7 <= %d, d = %d (r = %d), AUDITED: %s" % (CAP, d, d + 1, line), flush=True)
        A, B, C = R.build(d)
        C = [(nm, f) for nm, f in C if not nm.startswith("b_4 >= 3826746")]
        C.append(("b_4 >= 3826746 - 30 P - 4572 rho", R.add(B[4], R.lin(3826746, P=-30, rho=-4572), -1)))
        C.append(("a_7 <= %d" % CAP, R.add(R.lin(CAP), A[7], -1)))
        st = R.feasible(C)
        if st[0] == "infeasible":
            m = min(l for _, l in st[1]); line = "INFEASIBLE for all P, rho; certificate: " + "; ".join("%s x %s" % (nm, X.show(l / m)) for nm, l in st[1])
        else: line = "feasible; min rho = %s, min P = %s" % (X.show(R.minimise(C, R.lin(0, rho=1))[0]), X.show(R.minimise(C, R.lin(0, P=1))[0]))
        print("a_7 <= %d, d = %d (r = %d), NEW    : %s" % (CAP, d, d + 1, line), flush=True)
