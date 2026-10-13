# Review of the written proof of C3 (lab session, 13 October 2026)

Text reviewed: `pdf/preuve_c3.tex` of the repository `amazing-source/conway99-c3-experimental` (406 lines, dated
23 September 2026, last commit of that day), read in full at the user's request. Line numbers refer to that file.
I re-derived every step while reading. I did not read the Lean files, the referees' reports (I do not have them) or the
cited papers.

## Verdict
* **Mathematics: every step of the main line closes.** I found no false statement that affects a conclusion.
* **Writing: not publishable as it stands; the referees are right.** The text is a compressed note. In about fifteen
  places the reader has to supply an argument, redo a computation, or adapt an earlier step himself. One displayed
  intermediate identity is wrong as written. Section 4 is the worst part.

## A. Places where the reader must fill in (in order)
1. l.124-128, Lemma 4: "Phi is a ring morphism" is asserted from one formula; additivity, the unit, and the fact that
   the formula for (XY)_b needs the invariance of BOTH X and Y under g are not said.
2. l.151-152, Step 1(b): uses QJ = 14J, which is only stated four lines later, in 1(d).
3. l.154-156, Step 1(d): "14 is a simple eigenvalue and W = V + Q.1" needs: Q symmetric hence diagonalisable, the
   hyperplane orthogonal to 1 is invariant, and on it the eigenvalues are roots of t^2 + t - 12.
4. **l.156: wrong intermediate formula.** The text writes (Q-3I)(Q-14I) N_W = 18 (Q-14I) J = 0. The correct value is
   (Q-14I)(18J - 11J) = 7 (Q-14I) J = 0: the term -(Q-3I)J = -11J was dropped. The conclusion is unaffected.
5. l.159-162, Step 2: the existence of C with CB = I and the identity BCv = v on L are one line each but are not
   derived (splitting of 0 -> L -> R^n -> R^n/L -> 0); that Z[omega] is a principal ideal domain is used without a word.
6. l.165-167: "d-prime is real and in Z[omega], hence in Z" and "G-prime is positive definite" (B-prime injective) are
   not justified.
7. l.177, Step 3: the three identities for N-prime, G-prime K-prime = 7I and G_W K_W = 21 I are covered by "de meme";
   for the hermitian case the transposes become conjugate transposes and this should be written once.
8. l.180: "K-prime hermitian, so its determinant is an integer" (same argument as 6) and "d-prime divides a power of 7
   in Z" are not spelled out.
9. l.185-191, Step 4: det T != 0 and v_11(det G_W) = 0 are used silently in the valuation count.
10. l.194-206, Step 5: rho(X^*) = (rho X)^T is used for B-prime and C-prime without recalling it; "the first identity
    factors K-bar through F_3^r" is the rank argument and should be written as such.
11. **Section 4, l.223-224:** "M is hermitian, M^2 + M = 12I (in the computation of section 2 the paths through a t_i
    and the J term are multiplied by 1 + omega + omega^2 = 0)". This parenthesis replaces a proof: with fixed points the
    morphism Phi of section 2 does not apply as stated; one must write (A^2)_b = sum_c A_c A_{b-c} + a a^T for every b.
12. **l.236-237:** "(A~ - 3I) N~ = 0 and N~ x = 77 x if A~ x = 3x (then w^T x = 0)": A~ is NOT symmetric, so the argument
    of Step 1(a) does not apply. One needs w^T A~ = 14 w^T, which follows from the symmetry of D A~. Not said.
13. **l.240-244:** "X = N~ Delta is symmetric, D X = 3 N~^T, its columns are in L": three claims, none verified in the
    text (they follow from the symmetry of D N~ and D Delta = 3I). The integrality of G~ = (1/3) B^T D B is given half a
    line.
14. **l.249-250:** "Step 5, word for word, gives r = r-prime and det G~ = d-prime = 1 (mod 3)". It is not word for
    word: the matrices now have different sizes (35 on one side, 32 on the other) and only the 32 x 32 blocks B_1, C_1
    enter. The adapted identities must be written.
15. **l.251-256:** "W ... has rank r + 1", "N_W = 9(A~ + 4I) - 1 w^T is 63 times the projector on W", "the computation
    of point 2 gives G_W K_W = 189 I": each needs the D-self-adjointness of A~ and a short computation; none is shown.
16. l.277-284, Lemma 7: correct, but the three cases are run together in one paragraph, and the letter A (the
    adjacency matrix since l.58) is reused for a set of eight vertices.

## B. Things a journal would not accept, independently of the gaps
* Title page: "Redaction: Claude (Opus 5.5), pour D. Djematene" and "Preuve candidate, non encore relue par un tiers".
  (Standing rule of the project: author Dilan Djematene alone; assistance in the acknowledgements, without model name.)
* No preliminaries: the eigenvalues 14, 3, -4, the reduction map rho, and the convention for hermitian matrices over
  Z[omega] are introduced in passing.
* The idea of the proof ("Mecanisme", l.313-315) comes at the very end; it should open the paper.
* "Generalisation" (l.321-325): six other parameter sets are claimed excluded "by the same proof" with "integrality
  hypotheses checked case by case", without statement or proof. Either a theorem with hypotheses and a proof, or delete.
* "Controles numeriques" (l.326-330): anecdotal; belongs in a supplement.
* The Lean paragraph is longer than several proofs. The formalisation supports the paper; it cannot replace the
  written argument.
* The survey of the literature (l.84-104) attributes precise statements to eight papers. I did not check them; a
  referee will. In particular the sentence "together these results give |G| in {1,2,3}" should be derived line by line.
* Language: French; cross-references such as "corollaire 8" in the abstract.

## C. What I checked and found correct
Lemma 4 (i)-(iv); Step 1 (a)-(d) (with the correction of item 4); Steps 2 to 6; in section 4 the form of A~, w, D,
Delta, point 1 (the last three rows of N~ vanish modulo 3), point 2 (G~ K = 77 I), point 3 (blocks), point 4 (the
valuation at 11); Lemma 7 (all three cases, including the count 12 + 5s <= 0); the logic of Corollaries 3 and 8 given
the cited results.

## D. What a publishable version needs
A rewrite, not a patch: preliminaries; one general lemma "Gram matrix of an eigenlattice" proved once over Z and over
Z[omega] and for a diagonal weight D (it is used five times in different clothes); section 4 written in full; the
fixed-point lemma split into cases; the generalisation either proved or removed; the Lean material in a short
appendix. Length: about 12 to 15 pages instead of 6.
