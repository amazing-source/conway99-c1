"""C1, lab session, 2026-10-08. Independent check of Codex's exact identity excluding rank 35 (bridge message, 01:25 UTC).
  python cert35.py <N>
In my coordinates (theta_lp.family(34): a_n and b_n as affine forms in b_1..b_7) the combination
  3110 a_9 + 5474 a_10 + 1328 a_11 + 68698 (b_3 - 24948) + 3822 (b_4 - 2729034) + 15559 (55440 - 7 a_7 - 8 a_8)
  + 876897 (990 - a_7) + 18880582 (88 - b_1)
must be the constant -919306710. Every bracket is >= 0 for a srg(99,14,1,2) of rank 35:
  a_n >= 0; b_3 >= 24948 (audited); b_4 >= 3826746 - 30 P - 4572 rho >= 3826746 - 792 P >= 2729034 (rho <= P/6, P <= 1386);
  7 a_7 + 8 a_8 <= 55440 (Codex 173); a_7 <= 990 (seed packing, NOTE.md 17.10); b_1 <= 88 (Lemma F)."""
import sys
from fractions import Fraction as Fr
import theta_lp as T
T.selfcheck()
A, B = T.family(34)
terms = [(3110, A[9]), (5474, A[10]), (1328, A[11]), (68698, T.add(B[3], T.aff(24948), -1)), (3822, T.add(B[4], T.aff(2729034), -1)),
         (15559, T.add(T.aff(55440), T.add(T.sc(A[7], 7), T.sc(A[8], 8)), -1)), (876897, T.add(T.aff(990), A[7], -1)), (18880582, T.add(T.aff(88), B[1], -1))]
tot = T.aff(0)
for c, f in terms: tot = T.add(tot, T.sc(f, c))
print("combination = %s + %s" % (tot[0], " + ".join("%s b_%d" % (tot[k], k) for k in range(1, 8))))
assert all(x == 0 for x in tot[1:]) and tot[0] == -919306710, "identity FAILS"
assert 3826746 - 792 * 1386 == 2729034
print("IDENTITY VERIFIED in the lab coordinates: the seven variable coefficients vanish, constant = -919306710 < 0. Rank 35 is excluded.")
