"""C1, lab session. Robustness of the exclusion of r = 33: the exact maximum of b_4 (number of vectors of M of norm 8)
compatible with set "ext" (b_4 >= 388080 only) and the caps a_7 <= 7920, a_8 <= CAP8, for several CAP8; also for r = 35.
  python threshold33.py <N>"""
import theta_lp as T
import theta_lp_exact as X
T.selfcheck()
for d in (32, 34):
    for cap8 in (27720, 69300, 90090, None):
        A, B, C = X.build(d, "ext")
        C.append(("a_7 <= 7920", T.add(T.aff(7920), A[7], -1)))
        if cap8 is not None: C.append(("a_8 <= %d" % cap8, T.add(T.aff(cap8), A[8], -1)))
        hi4 = X.minimise(C, T.sc(B[4], -1)); hi3 = X.minimise(C, T.sc(B[3], -1)); hi2 = X.minimise(C, T.sc(B[2], -1))
        print("d = %d (r = %d), a_7 <= 7920, a_8 <= %s: max b_4 = %s; max b_3 = %s; max b_2 = %s" % (d, d + 1, cap8, X.show(-hi4[1]), X.show(-hi3[1]), X.show(-hi2[1])), flush=True)
