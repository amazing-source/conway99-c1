# Audit of the order-2 paper before consolidation (lab session, 13 October 2026, 22:53 UTC)

Text audited: `papers/conway99_order2/order2.tex` of the repository `strongly-regular-graphs-research` (1061 lines,
"Draft of 7 October 2026", 23 pages; it compiles here). Line numbers refer to that file. I read all of it and re-derived
by hand every statement of Sections 3 to 6 and of the first two pages of Section 7 (the part "proved by hand"). I did
not re-run or re-read any program, and I did not open the three lemma files T16, T18, T20 for this audit.

Context: A. Woldar and P. Cesarz, who reviewed the order-3 text, wrote on 13 October that it needs a complete
overhaul ("sections not suitably motivated, notations and terminology vague and at times ambiguous, exposition lacking
on multiple levels"), that they will rewrite its Sections 1-3 themselves, and that in the meantime the order-2 argument
should be refined. Their written report (a PDF attached to their mail of 12 October) is not available to me yet.

## 1. Verdict
* **The hand part is correct as far as I re-derived it** (Proposition 3.1, the frame, Propositions 5.1 and 5.2,
  Theorem 6.1 = Theorem R, Lemmas 6.3 to 6.8, the list of witnesses). I found no false statement.
* **It is much better written than the order-3 note** (introduction, outline, notation section, honest verification
  section), but **the hand part has the same defect in a milder form**: about twenty-five places where one sentence
  stands for an argument the reader must reconstruct. List in Section 2.
* **Three structural weaknesses** would stop a journal or a computer-free reader before any detail. Section 3.

## 2. Places where the reader must fill in (hand part, in order)
Section 3 (an involution fixes exactly one vertex)
1. l.209-210: "all 84 such pairs occur" - the bijection between the 84 vertices at distance 2 from p and the 84
   non-adjacent pairs of neighbours of p is not argued (why the two neighbours are in different blocks; why the map is
   onto).
2. l.210-214: the counts 2 s_p (s_p - 1) and 2 r_p and the formula f = 1 + 2 s_p^2 + 2 r_p are stated without the
   one-line computations.
3. l.216-219: "the common neighbours of v and sigma v are p and one further vertex, which is fixed" (invariance of the
   set of common neighbours), and above all "the number of such vertices is n_2 = 2 sum r_p": this is a double count
   (each such vertex lies in a moved block at each of its two fixed neighbours), not written.
4. l.227-230: the trace condition. The idempotent is quoted, the trace of the permutation matrix against A and J is
   not computed (trace(A P) = a_1, trace(J P) = 99), and "the trace is an integer" is not justified (eigenvalues +-1).
5. l.231-234: the list of triples is given without the enumeration that produces it; "for 19 <= f <= 73 the triple is
   the same at every fixed vertex" is true because each such f occurs once in the list, which is not said.
6. l.236-243: seven numerical cases in six lines; each is correct, none is displayed.
7. l.251-252: "it is a single orbit {v, sigma v} of outer vertices" - that the two common neighbours of u and sigma u
   are outer (and not the two ends of a block) is not argued.

Section 4 (signed quotient, frame)
8. l.289-297: the symmetry of S and the passage from A to S on odd functions are asserted.
9. l.298-299: multiplicities 27 and 22 from the trace: computation omitted.
10. l.299-306: "suitable outer representatives", the columns e_i + e_j and e_i - e_j of C, and "exactly ten nonzero
    entries in each row of T" are explained only by a parenthesis and by the caption of Figure 2.
11. l.311-320: H^2 = 7H, rank 22, (u_i, u_j) = H_ij, the tight-frame identity and the relation (4.4) are each one
    clause. The same letter u denotes vertices, all 49 frame vectors (u_i) and the 42 outer ones (u_o).

Section 5 (the lattice)
12. l.324-331: K* = H Z^49 / 7 and N = sqrt 7 K* : compressed but complete; the sentence on the coordinates
    a_i = (v, u_i) needs one line.
13. l.334-335: "so Z^49 / (K + K') is F_7^g with g the rank of S - 3I over F_7; thus det K = 7^g" - the identification
    of the dimension with that rank is not proved (it is: the image of H modulo 7 is 7K*/7K).
14. l.344-350: the 2-adic paragraph. "sum of m_o is even" (T is symmetric with zero diagonal) and "the number of outer
    rows with r_o = 2 mod 4 is odd" are not argued; the last congruence (c, c) = 6 mod 8 uses the inverse of 7 modulo 8.
15. **l.352-360: the oddity formula.** One displayed congruence, 22 + 6g + 4[eps = -1] = 6 mod 8, carries the
    whole proposition. The 7-excess of each Jordan constituent, the fact that the other primes contribute nothing, and
    the identification "oddity = norm of a characteristic vector modulo 8" are not written. For a reader who is not a
    lattice specialist this is the least accessible step of the paper. It is also the step on which everything after
    depends (the anisotropic plane, hence the gluing).
16. l.356-360: "the discriminant form of N is the form of the unimodular constituent of K", "Witt index m - 1", "the
    preimage of a totally isotropic subspace is N_max": three assertions, each needing two or three lines.
17. l.373-388 (dual minimum): correct and nearly complete; the sum over P and Q of the binomials, the identity
    B^2 = 2I + 2J and "equal multiplicities since the characteristic polynomial is rational" deserve a displayed line
    each.

Section 6 (the envelope)
18. l.411-418: the gluing. "An anisotropic plane and its negative both have square determinant", the integrality of
    the glued lattice, its determinant and the primitivity of the two summands are asserted with references.
19. l.420-423: (R6) and (R7): "the projection of v on V lies in N_max* " and the identity sum a_i^2 = E(v) need the
    decomposition of v along V and its orthogonal plane.
20. l.443-452 (Lemma 6.3): "polarising (R5) and applying it to u_o" and "pairing (6.1) with u_o' " are two
    computations left to the reader; "the graph 'sharing exactly one block' is connected" is asserted.
21. l.480-484 and l.490-493 (new roots, characteristic vectors of norm 16): correct, each a chain of congruences
    written in two lines.
22. l.501-506 (twins): "both project onto M* " and "the function phi_v depends only on that projection".

Section 7 (energy)
23. l.539-547: "Going through the norms 2, 3, 4 shows that the vectors of energy 8, 9, 10 are exactly the following
    witnesses" - the residues modulo 7 are not displayed. Same for "a vector of energy at most 7 has a representative
    of norm 2 or 3".
24. l.549-550: N_3 = 4096 and N_4 = 196560 - 24 N_2 - 24 N_3 are quoted from the theta series without the two lines
    that give them.

## 3. Structural weaknesses
A. **The three lemmas are not in the paper.** Theorem 7.1 (no integer odd eigenfunction of squared norm 16, 18, 20)
   is used for every lattice, and its proof is "given in full in the supplement" as three Markdown files of a
   repository. A journal will require the proofs, or at least their hand parts and a precise statement of each
   machine step, in the paper or in a typeset appendix.
B. **One computational item is declared open by the paper itself** (l.881-897 and item 5 of the summary): the
   transfers of the first and third form, 4,163,099 pairs, of which at most 2,479,669 are not covered by Corollary
   7.3, were not recertified without floating point and without the recorded order of treatment. As written, the
   theorem is not fully established by the paper's own standard.
C. **The searches rest on one program** (about 2.6 x 10^7 pairs), and the completeness of the enumeration of pairs was
   compared with a second enumerator on four lattices only. The paper says so; a referee will ask for more.
Also: the abstract says the repository is private (it must be public or archived at submission); the corollary on
asymmetry cites two unpublished manuscripts of the same project.

## 4. What consolidation can mean, in order of certainty
1. **Write the hand part in full** (Sections 3 to 6: Theorem R, "an involution gives a frame in one of 156
   lattices, with every vector outside the plane of the normals of energy at least 8"). It is a complete,
   computer-free statement; it is the part a human expert can referee line by line; every item of Section 2 is
   removed by writing, no new mathematics is needed. Estimated size: 18 to 22 pages instead of 8.
2. **Bring the three lemmas into the text**: hand reductions written in full, machine steps isolated and stated as
   finite checks with their sizes. (An agent of this session found two shortenings on 13 October: the case k = 2 of
   the squared norm 16, and one identity replacing two lemmas for 18; report `work/c2_elegant_2026-10-13/
   LEMMAS_AGENT_REPORT.md`.)
3. **Close item B** (the recertification). It is a computation of several hundred core-hours, prepared and not
   launched; it needs the user's decision.
4. **Change the architecture of the second half.** Result of 13 October (not audited by a third party,
   `work/c2_elegant_2026-10-13/NOTE_MISSION_C2.md`): the theta series of the lattice with its two normals lies in an
   explicit space of dimension 61, and this forces a vector of energy at most 12 outside the plane of the normals.
   With it, Theorem 6.2 (the 156 lattices, items B and C above included) would be replaced by two more lemmas of the
   same kind as the three existing ones, for the squared norms 22 and 24. These two lemmas are not proved; a sounding
   of their size was running on 13 October.
