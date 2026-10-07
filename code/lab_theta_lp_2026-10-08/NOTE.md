# Level-7 theta series and an exact linear programme for srg(99,14,1,2) (lab session, 2026-10-07/08)

Status: derivation and programs by the lab session. Codex checked independently the lattice L1, the bound 22 on its new
vectors, the form Q, the basis and the Fricke formula (its note 167 and `code/codex/theta7_audit.py`); it found no
theta/Fricke programme in the earlier notes. The laptop session supplied part of the list of short dual vectors.
The LP results below have NOT yet been refereed. AI sessions only; nothing formalised. Nothing here proves non-existence.

## 1. Set-up

Gamma a srg(99,14,1,2), A its adjacency matrix, P = (27I - 9A + J)/63 the projector on the (-4)-eigenspace (dimension 44),
r = rank_7(A - 3I).

* L = Z^99 cap ker(A + 4I). Every non-zero vector has norm >= 14 (entries 0, +-1 need two supports of size >= 7; an entry
  of absolute value >= 2 costs norm >= 20). Norm 14 = the Fano configuration (Codex, note 165), which forces r >= 33.
* L1 = L + Z (21 P e_v) = { phi - (s/3) 1 : phi in Z^99, A phi = -4 phi + 6s 1 } (then sum phi = 33 s). Index 3 over L,
  independent of v, even (|phi|^2 - 11 s^2 = sum phi - 11 s = 22 s mod 2), and 7 L1* is contained in L1. A vector outside L
  is phi - (1/3) 1 with sum phi = +-33, so its norm |phi|^2 - 11 is >= 22. Hence L1 is an even lattice of rank 44 and
  level 7, of determinant 7^d with d = r - 1 (given det L = 9 * 7^(r-1), rank7.tex of the earlier work), and
  **L1 and L have the same vectors of norm 14, 16, 18, 20**.
* M = sqrt7 L1*, where L1* = { P psi : psi in Z^99, 3 | sum psi }. Its form is
  Q(psi) = psi^t (3I - A) psi + (sum psi / 3)^2, even, determinant 7^(44-d). sqrt7 M is contained in L1.
* theta_L1 = sum a_n q^n and theta_M = sum b_n q^n (n = norm/2) lie in M_22(Gamma_0(7)) with trivial character (d even;
  d odd is impossible by Milgram's formula, and d = 0, 44 because 44 is not a multiple of 8). Dimension 15, basis
  F_j = G t^j (j = 0..14), G = theta_{x^2+xy+2y^2} (eta(7 tau)^7 / eta(tau))^7 = q^14 + ..., t = (eta(tau)/eta(7 tau))^4,
  all with integer coefficients, and (G t^j)|W_7 = -7^(2j-14) G t^(14-j). If theta_L1 = sum c_j F_j then
  theta_M = sum_j c_j 7^(d/2+2j-25) F_(14-j).
  `theta_lp.py` checks the basis and this formula exactly on E8^a + (sqrt7 E8)^(5-a) + A + A, a = 0..5.
* a_0 = b_0 = 1 and a_1 = ... = a_6 = 0 leave **seven free parameters, which are b_1, ..., b_7**. Every a_n and b_n is an
  explicit affine function of them, for each d.

## 2. Constraints used (set "ext")

| constraint | reason |
|---|---|
| a_n >= 0, b_n >= 0 (n <= N) | counts |
| a_7k >= b_k | sqrt7 M inside L1 |
| b_2 >= 462 | +-t_T, T one of the 231 triangles, Q(1_T) = 4 |
| b_3 >= 24948 | e_u - e_v, u, v non-adjacent (8316); +-(e_u + e_v + e_w) on an induced 2-path (16632) |
| b_4 >= 388080 | e_u - e_v adjacent (1386); +- a triple with exactly one edge (99792); 1_e - 1_e' for two disjoint edges with no edge between (693 * 366 = 253638); 1_T - 1_T' for two triangles with exactly one edge between (33264 + 6 * prisms, the prisms dropped) |
| b_5 >= 196812 | +- an independent triple |

Distinctness in M: two listed psi, psi' are equal in M iff psi - psi' lies in Z^99 cap (E_3 + Q 1); the sums of entries
force it into E_3, and a non-zero integer 3-eigenvector has norm >= 12 if its entries are 0, +-1 (the + support has minimum
degree 3, so at least 6 vertices) and >= 18 otherwise. This separates all the vectors counted above; it does NOT separate the
norm-6 vectors 1_T - 1_T' (no edge between), which can coincide for "twin prisms", so those are not counted.
"a_7 = 0" (when used) is Codex's lemma for r <= 31.

## 3. Results (exact rational simplex, N = 84 coefficients; identical with N = 70)

`theta_lp_exact.py` solves each LP in Fractions and re-verifies what it returns; `certificates.py` stores and re-checks
the Farkas multipliers (15 of 15 verified, `certificates_N84_check.txt`).

| r | set "ext" | with a_7 = 0 | largest minimum of L1 allowed |
|---|---|---|---|
| <= 27 | infeasible (exact certificate) | | |
| 29 | feasible only with a_7 >= 2 558 811 and b_1 >= 174 | infeasible (exact) | 14 |
| 31 | feasible only with a_7 >= 316 | infeasible (exact) | 14 |
| 33 | feasible | then a_8 >= 100 986 | 16 |
| 35, 37 | feasible | feasible | 20 |
| 39, 41 | feasible | feasible | 24 |
| 43 | feasible | then b_2 >= 1000 and b_3 >= 7 561 631 | 26 |

Consequences, each conditional on sections 1 and 2 being right:

1. **r >= 29** from the theta series alone, and **r >= 33** with Codex's lemma (r = 29 and 31 need Fano vectors, which need
   r >= 33). The earlier lower end was 25 (computer-assisted) / 23 (by hand).
2. **A srg(99,14,1,2) has a non-zero vector of L1 of norm <= 26**, more precisely <= 16 if r = 33, <= 20 if r = 35, 37,
   <= 24 if r = 39, 41, <= 26 if r = 43 (`OUTPUT_ladder_N84.txt`). The Hermite-type bound was 44. Norms 14..20 are integer
   (-4)-eigenvectors; norms 22..26 are those or vectors phi - (1/3) 1 with sum phi = 33, |phi|^2 = norm + 11.
   So the "ladder" of support cores is finite and short: norms 14 (one core, Codex), 16 (five cores, Codex), 18, 20, 22, 24, 26.
3. What-if runs (hypotheses, not facts), `OUTPUT_N84.txt`: if M had no root, at most 3234 vectors of norm 4 and at most
   32340 of norm 6, then r = 39, 41, 43 would be infeasible and r = 31 too. With b_1 = 0 and b_2 <= 3234 alone, r = 43
   needs b_3 >= 10 561 586, r = 41 needs b_3 >= 1 390 256, r = 39 needs b_3 >= 80 066. So UPPER bounds on the numbers of
   vectors of M of norm 2, 4, 6 (a classification of the short dual vectors) would close the top of the window.

## 4. Files

`theta_lp.py` (series, basis, Fricke check, affine family; its own main is a floating-point first version, superseded),
`theta_lp_exact.py` (exact simplex and the constraint sets), `certificates.py`, `ladder.py`, `certificates_N84.json`,
`certificates_N84_check.txt`, `OUTPUT_N84.txt`, `OUTPUT_ladder_N84.txt`.
Run: `python theta_lp_exact.py 84 ext`, `python certificates.py 84 check`, `python ladder.py 84` (standard library only, one
process, under a minute each).
