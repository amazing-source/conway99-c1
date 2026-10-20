# Adversarial review of NOTE_ORDRE2_7ADIQUE.md (agent, 20/10/2026, read-only)

Reviewer: an adversarial-reviewer agent launched by LAB at 16:25. It was asked to stop computing at 16:34, because the user
was back on the PC. It ran no script. Below is its report, condensed by LAB; the substance and the line references are
kept. Line numbers refer to the version of the note before corrections. The corrections are integrated in the current
note (see §0.9 and §6 bis there).

## Findings

**1. should-fix: the scope of "before 7 far vertices, nothing acts" is overstated.**
- The case "first layer full, s degenerate, |X| <= 6" was not covered by (i)-(iv).
- Counterexample:
  - Rank 41 (rho = 4, U4 elliptic, Witt index 1), m = 6, s = 0 on K_X (dimension 2), and B = (N', H/49) unimodular and
    anisotropic.
  - Any representation of B(7) in U4 reduces mod 7 to a totally isotropic subspace of dimension <= 1. So some primitive y
    would need v7(y^T H y) >= 3, whereas all of them equal 2.
  - Hence H_XX is not represented.
- The same mechanism works at ranks 37 and 39 (corank 2 at 6 vertices, with an elliptic rank-4 complement).
- Corank 1 at m <= 6 is genuinely free: the complement has rank 9 - m >= 3, so it is isotropic.
- These cases have probability of order 7^-3, but "only exception / single rule / closed" was not proved.
- Fix: restrict the statements to "first layer full and corank(s) <= 1", and move corank >= 2 at m = 6 to (X).

**2. should-fix: §2.3 (ii) used k for |X|, which clashes with k = rho/2.** Read with k = 8, "(-1)^{k+1}" gives -1,
whereas the correct value at ranks 39 and 43 is +1. Write (-1)^{rho/2+1}.

**3. should-fix: overclaims about the measurements.**
- The rank-39 depth statements rest on prefixes covering 1.0-5.4% of the depth-1 branches.
- §5's "no local 7-adic or p-adic device can reduce the ~1e15 estimate" does not follow from the theorem, which only says
  nothing acts below depth 7 in the generic cases. Label it H.

**4. optional: "(ii) implies (i)" needs the inclusion U~ in Im M.**
- ker M mod 7 is not totally isotropic.
- Justification of the inclusion: the columns of H lie in 7 Lambda^# within 7 E^#, and 7P = M(A - 14I)/18. The direct
  variant already proves (i).

**5. optional: Prop. 2 item 4 (independence of the lift) cited only a numerical check.** Hand computation, for
U -> U + 7Y and D -> D + 7D':
- U'^T S' y = U^T S y on K;
- N' = N + U^T Y, and Q' + D'^{-1} = Q + D^{-1} + U^T Y + Y^T U, so (b) is unchanged;
- (c) is unchanged, using (a) and U^T U = 0.

**6. optional: "corrects TL:3604-3608" is a mischaracterisation.**
- The quoted phrase is at TL:3597.
- TL works with H+ mod 49 (TL:3608), while the corank-1 rule needs H mod 7^3 (e' = 2 versus e' >= 3).
- So it adds a condition at higher precision rather than correcting TL.

**7. optional: citations and notation.**
- The square-class confirmation by Codex is at TL:2461-2463.
- The rank 8 of Lambda_-(T) is stated at RD:14.
- The kappa_t are kernel vectors of the 39 x 39 N[T] block; the 36 x 36 N(T) block is nonsingular.
- e_a should be read as column a of E.

## Item by item

**a) Propositions 1 and 2: correct.**
- The exact identity UD(I+QD)U^T - UDU^T S - SUDU^T = 7(S - S^2) was re-derived.
- The block reading on K + Im C is valid, and (c) follows mod 49.
- Lattice reading: Q = G1, S = B0 G0^-1 B0^T, N = 0, S^2 = S.

**b) Section 2.2: correct. chi(det U_{8-rho}) = (-1)^{k+1} and the Witt column (3/2/1/0) were confirmed.**

Independent derivation by the reviewer, not re-checked by LAB:
- Assume 7 does not divide tau. Then Lambda' = E- cap span(near projections) is 7-modular of rank 36.
- There is no glue at 7, so E- (x) Z7 = Lambda_-(T) _|_ Lambda', and the unimodular part U_E of E- is isometric to
  U_{8-rho}.
- c7(V-) = (-1)^k chi(det U_E), with:
  - c2 = -1: E- is even with det = 1 mod 8, so its 2-adic class is H^22;
  - c3 = 1: the 3-part of the discriminant group is cyclic;
  - the product formula then gives c7 = -1.
- This yields chi(det U_{8-rho}) = (-1)^{k+1}, and RD:31.

**c) Theorem §2.3: (i), (ii), (iii) and (C43), including the "iff", are correct.**
- The anisotropic unimodular plane at 7 is the norm form of Z49, with norms {0} U 7^{2j} units.
- Issues: findings 1, 2 and 6.

**d) §2.5 Legendre rule: correct.** The first version was indeed wrong.

**e) §3: correct.**
- H3 = 4I + R - (2/35)J - E^T(4I+G)^-1 E was re-derived as a Schur complement.
- H + H3 = 7 P_kerE, so 7I - H = H3 + 7E^T K^+ E.
- 7I - H is vacuous on blocks of size <= 2 once H >= 0.
- "7I - H never cuts" in the engine is empirical, not a theorem.

**f) Cited archive lines** (RD:9, 21, 23-24, 29-32; TL:2335, 2338, 2463 and 3604-3607) say what the note claims. The
slips are listed in findings 6 and 7.

## Not checked by the reviewer
- No script was run.
- Not read: SYNTHESE §3.5/§8, NOTE_BOOST §2.3, NOTE_OBSTRUCTION §1.1, NOTE_PROOFS_1410, most of NOTE_FUSION R5.
- The table arithmetic was checked.

## Verdict
The mathematics is sound. Findings 1-3 needed rewording of scope and measurement claims, not changes to the results.
