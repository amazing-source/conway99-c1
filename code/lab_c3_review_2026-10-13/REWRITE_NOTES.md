# Rewrite of the C3 proof: status and choices (lab session, 13 October 2026, 22:40 UTC)

File: `c3_proof_rewrite.tex` (this folder), about 870 lines, English, author line "Dilan Djematene".
It replaces the argument of `pdf/preuve_c3.tex` (conway99-c3-experimental, 23 September 2026); the mathematics is the
same, the writing is new. The review that motivated it is `REVIEW_C3_PROOF.md`.

## Status
* **Not compiled.** There is no LaTeX on the lab PC. A script checked: braces, environments, labels and references,
  citations, dollar signs, custom macros, ASCII only. The first compilation has to be done elsewhere (the laptop).
* **Not yet read by anyone else.** A referee pass by a fresh agent was started after writing; its report is to be
  `REFEREE_AGENT_REPORT.md` in this folder.
* The Lean files were not opened. Section 8 only repeats the names of the formal statements given in the old text.

## What changed
1. Four lemmas are stated and proved once, in the generality both cases need, so that nothing is "as in step k":
   2.1 basis of a kernel with a retraction (over Z and Z[omega]); 2.2 the Gram identity G K = c I for a weighted form
   D and a matrix X with X D = c on the lattice; 2.3 a lattice plus one orthogonal vector (the index identity that
   brings in the prime 11); 2.4 the comparison over the field with three elements (r = r' and det H = eps^r det H').
2. The orbit matrices are introduced once for both cases (Lemma 4.1), with the product formula
   sum_e A_e A_{b-e} + a a^T = 12 delta I + 2J - A_b proved entry by entry. This replaces the "ring morphism Phi" of the
   old Lemma 4 and the parenthesis of the old section 4.
3. The case of three fixed vertices (Section 6) is written in full: seven steps, every hypothesis of the lemmas
   checked on the page (D-self-adjointness, symmetry of N-tilde Delta, the block form, the reduction modulo 3 with the
   sizes 35 and 32).
4. The fixed-vertex lemma (Section 3) is split into six steps; it now proves directly "no fixed vertex, or exactly
   three pairwise adjacent ones" (the old text proved "at most three" and added the congruence modulo 3 and the
   triangle separately).
5. The wrong intermediate formula of the old line 156 is corrected ((Q-3I) N_W = 7J).
6. The idea of the proof is in the introduction.

## What was removed, and why
* The paragraph "Generalisation" (six other parameter sets): it was claimed without statement or proof. It needs its
  own theorem (hypotheses on k - theta, theta - theta', v/3) and a proof; not written here.
* The paragraph "Numerical controls": not part of a proof.
* The long description of the Lean tool chain: reduced to one paragraph; the details belong to the repository.
* The reports of other authors on the open status ([TS26], [K26]) and the MIT PRIMES report [LM14]: not needed.

## Not verified by me (to check before any submission)
* **Every statement attributed to the literature** in Section 1.2 and in Corollary 7.1 ([MM04], [B09], [BL11],
  [CM20], [Mak10], [CW25], [I26]): copied from the old text, sources not opened. In the proof of Corollary 7.1 the step
  "2 divides the order implies the order divides 42" is attributed to [Mak10] as in the old context paragraph (the old
  proof cited [CW25] for "divides 6").
* The two textbook pointers ([IR] Chapter 1 section 4 for "Z[omega] is Euclidean"; [La] Chapter III section 7 for
  "a submodule of a free module of finite rank over a principal ideal domain is free"): given from memory.
* The names of the Lean statements (Section 8).

## Choices left to the author
* Language (English chosen, as for the C2 document).
* The acknowledgement sentence about AI assistance (one neutral sentence, no product name, per the project rule).
* Whether to keep both proofs (Section 5 without weights, Section 6 with weights) or only the weighted one, which
  contains the other (Remark after Theorem 6.1). Both are kept: the first is the new result and is easier to read.
