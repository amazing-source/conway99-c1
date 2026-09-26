# 118 — Niveau paire × bloc ; mécanisme cellcross ; au Fano tendu, la fonctionnelle Ψ_R et 21 systèmes par bloc

*26/09, matin. Labo c1_experimental (X19n à X27). DÉRIVÉ = preuve écrite ; OBSERVÉ = calcul. Chaque PL est un test
de moins de 5 minutes sur un système dérivé à la main, sauf les calculs paire × bloc de la nuit, dont les deux
phases 1 de certification (460 s et 561 s) : ils dépassaient la règle des 5 minutes. Depuis, tout reste sous
5 minutes. Les infaisabilités annoncées « certifiées » ont un vecteur de Farkas vérifié en entiers exacts, et
« structures » les a toutes revérifiées avec son propre code.*

## 0. Résumé
| résultat | statut |
|---|---|
| niveau paire × bloc : les 3 survivants « blocs + cellules » (sur 45) sont infaisables | 2 certifiés et revérifiés par « structures » ; seed21#0 en flottants seulement |
| certificats de cellules : 19 sur 19 revérifiés par « structures » | recalcul indépendant, 0 écart |
| ablation : « blocs + cellcross » suffit à tuer le témoin de Fano et s21c#0 ; s11#1 exige une combinaison | OBSERVÉ |
| Fano tendu : cellcross se découple par bloc ; la fonctionnelle Ψ_R est universelle et a une forme close | DÉRIVÉ, contrôle exhaustif exact, reproduit par « structures » |
| Fano tendu : Ψ dépend des retournements ; 480 choix de retournements admissibles l'annulent pour σ du témoin | OBSERVÉ (énumération exacte) |
| Fano tendu : les 21 systèmes « cellules par bloc » (comptes fixés) sont infaisables dans 16 à 19 blocs sur 21 | OBSERVÉ, recoupé par les lignes de X19i |
| strate des σ internes (m = 1, 2) : 1 survivant « blocs + cellules » sur 24, indéterminé en paire × bloc | OBSERVÉ |

## 1. Niveau paire × bloc (X19n)
- **Variables.** Pour chaque paire z, chaque type t de z (multigraphe de classes, comme en notes/117) et chaque bloc
  générique R de t : s[z,t,R,S] ≥ 0, où S est la partie exacte des 4 paires de R adjacentes à z, avec |S| = t(R).
- **Lignes** (toutes exactes) :
  - cons : Σ_S s = x ;
  - labdeg : pour chaque étiquette l hors des classes de z, Σ_R Σ_S #(S ∋ l)·s = (2 − h_z(l))·x ;
  - pairblk : pour chaque paire y et chaque bloc R′, Σ_z [z~y]·cnt(z,R′) = Σ_{w∈R′} (A_Δ²)_{yw} ;
  - pairpair : pour y ≠ y′ dans un même bloc, Σ_z [z~y][z~y′] = 2 − |y∩y′| − [y~y′] ;
  - bal, lab, P2 de notes/117.
- Deux blocs différents d'un même z ne se combinent que sous la forme (partie dans R) × (compte de classes dans R′).
  C'est donc une relaxation valide.
- **Résultats.** Les 3 configurations qui passaient blocs et cellules (notes/117 §2 ter) sont infaisables.
  - seed11#0 : Farkas 168 240 155 et seed21#1 : 147 842 015, à l'échelle D = 10⁶, sur environ 78 500 lignes et
    130 000 colonnes.
    - **Vérification indépendante par « structures »** (`verify_c1_pairblock.py`) : lignes reconstruites depuis leurs
      noms, 0 écart ; énumération des parties S complète ; Farkas identique.
  - seed21#0 : infaisable en flottants seulement. La phase 1 exacte dépasse 5 minutes.
- **Cellules** : les 19 configurations tuées au niveau cellules (graines 11 et 21) ont chacune un certificat exact,
  et « structures » les a tous revérifiés.
- **Bilan de l'échantillon aléatoire S = 0** (45 configurations admissibles) : aucune ne survit au niveau paire × bloc.
  Cela reste un énoncé d'échantillon.

## 2. Quelle famille tue ? (X23, ablation au niveau cellules)
- Au témoin de Fano et à s21c#0 : « blocs + cellcross » est infaisable, alors que « blocs + cellsame », « blocs +
  cellbal » et « blocs + celllab » sont faisables. À s21c#0, retirer cellcross rend le système faisable.
- À s11#1 : aucune famille seule ne suffit avec les blocs ; il faut une combinaison.
- **cellcross**, en clair : pour tous blocs R, R′, **Σ_z δ_R(z)·c_R′(z) = −Σ_{y∈R} ε(y)·c_R′(y)**, où
  δ_R(z) = #N(z)∩A_R − #N(z)∩B_R et ε = ±1 sur les cellules. C'est l'identité ⟨(A_Δ+I)ε_R, A_Δ1_R′⟩ = 0, et ses
  parties E₁₀ ⊕ E₃ découlent de celllab.

## 3. Au Fano tendu : découplage, Ψ_R, forme close (DÉRIVÉ, contrôles exacts)
Au Fano tendu, les comptes c(z) ∈ Z²¹ sont entièrement déterminés par les classes d'atterrissage (a, b) de σ
(notes/115-116). cellcross se découple alors bloc par bloc : pour chaque R, c'est un système linéaire en les δ_R(z)
des z libres, c'est-à-dire des z dont les classes évitent R et tels que c_R(z) > 0.

- **Obstruction de rang au témoin.** Pour les 21 blocs, la matrice [c_R′(z)] est de rang 16. Le rang augmenté vaut 17
  pour 9 blocs : 02, 03, 05, 23, 24, 25, 34, 35, 36. Ces 9 systèmes sont donc insolubles, même sans les bornes
  |δ| ≤ c. « Structures » l'a reproduit en rationnels exacts.
- **Noyau effectif.** On demande l'orthogonalité aux c(z; a, b) seulement pour les atterrissages où c_R(z; a, b) > 0.
  Le noyau obtenu est de dimension 5 pour les 21 blocs. « Structures » l'a confirmé.
- **La fonctionnelle Ψ_R.** Soient R = {P,Q}, M = Φ(P,Q) et C4 le complémentaire de la droite PQM. Soit M_M les deux
  paires de C4 dont le troisième point est M ; on pose s = +1 sur l'une et −1 sur l'autre. Alors :
  **Ψ_R = Σ_{c∈C4} s(c)·[9e_Mc + e_Pc + e_Qc] + 4(e_{c₁c₂} − e_{c₃c₄})**.
  - ⟨c(z; a, b), Ψ_R⟩ = 0 dès que c_R(z; a, b) > 0 : contrôlé sur 21 blocs, tous les z libres et les 8
    atterrissages. Sinon, la valeur est ±6.
  - D'où, **à tout sommet de Fano tendu et pour chaque R : ⟨rhs_R, Ψ_R⟩ = 0**.
- **Forme close.** Pour y ∈ R, ⟨c(y), Ψ_R⟩ = 0. La partie σ s'annule aussi : {a_y, b_y} est une paire de M_P ou de
  M_Q, jamais de M_M, donc s(a_y) + s(b_y) = 0. Il reste :
  **⟨rhs_R, Ψ_R⟩ = −6·Σ_{y∈R} ε(y)·[θ(z_P(y)) + θ(z_Q(y))]**, avec :
  - z_P(y) le partenaire τ de y dans PM ;
  - θ(z) = s(a_z)·η_z, où η_z = +1 si l'atterrissage via M vaut Φ(M, a_z), et −1 s'il vaut Φ(P, a_z).
  - Donc I_R := ⟨rhs_R, Ψ_R⟩/24 ∈ {0, ±1, ±2}.
  - Au témoin, I_R vaut −1, +1, −1, +1, +1, +1, −2, −1, −1 sur les 9 blocs ci-dessus. « Structures » trouve la même
    chose, signes compris.
- **Dépendance aux retournements (auto-attaque).** Avec x_{X_s} = (−1)^{s+f(X_s,L)} :
  tot_R = Σ_{X∈R} Σ_s x_{X_s}·D^R_X(s), où D^R_X(s) = θ(X_sZ₀) − θ(X_sZ₁) ne dépend que de σ.
  - σ du témoin fixé, énumération exacte des 42 bits : l'admissibilité des 7 triangles de droites et des 7 étoiles,
    plus les 21 conditions I_R = 0, laissent **480 affectations**.
  - Les 50 premières passent même le test de rang complet (les 5 fonctionnelles) sur les 21 blocs.
  - **Ψ n'est donc pas un lemme à lui seul** : les morts de Fano de notes/117 venaient de retournements choisis pour
    la seule admissibilité.

## 4. Au Fano tendu : 21 systèmes « cellules par bloc » (OBSERVÉ)
- À comptes fixés, cellcross, cellsame et celllab se découplent aussi bloc par bloc. On obtient un petit PL par bloc,
  en variables de découpage (k_A, k_B). Seul cellbal couple les blocs.
- Résultats :
  - les 4 affectations Ψ-compatibles testées (0, 100, 250, 479) meurent au PL cellules complet (X19i) ;
  - par bloc, elles sont infaisables dans **16 à 19 blocs sur 21**, et le témoin d'origine dans 18.
- **Recoupement** : les lignes de X19i elles-mêmes, types fixés aux comptes tendus et restreintes à un bloc, donnent
  exactement les mêmes 18 blocs au témoin.
- **Conséquence.** Un sommet de Fano tendu exige que ces 21 petits systèmes soient tous faisables, ce qui n'arrive
  dans aucune configuration testée. Le lemme « aucun sommet de Fano tendu » revient à montrer qu'un bloc échoue
  toujours. C'est un problème fini, **non fait**.

## 5. La strate des σ internes au bloc (X24)
- Échantillon : configurations avec m = 1 ou 2 arêtes σ internes {P_sQ_t} ~ {P_{1−s}Q_{1−t}}. Une telle arête est les
  deux spéciaux σ de ses extrémités à la fois ; les spéciaux sont désormais dédoublonnés à la source.
- Sur 24 configurations admissibles :
  - 11 meurent au niveau bloc et 9 au niveau cellules ;
  - 3 sont indéterminées au niveau cellules (limite de temps) ;
  - **1 survit aux blocs et aux cellules** (m = 2). Au niveau paire × bloc, elle reste indéterminée : IPM et simplexe
    dual atteignent tous deux la limite de 5 minutes.
- **Auto-attaque** : un statut « limite de temps » avait d'abord été compté comme une mort. C'est corrigé ; ces cas
  sont désormais sauvés à part.

## 6. Portée
- Aucune de ces morts n'est encore un théorème sur une strate entière. Ce sont des certificats par configuration.
- La leçon nouvelle est au §3 : un tirage aléatoire meurt, mais un choix adverse (retournements Ψ-compatibles)
  échappe à une obstruction donnée. Les énoncés d'échantillon ne se transfèrent pas aux configurations structurées.
- Au Fano tendu, la situation est la plus favorable : 21 systèmes locaux explicites, presque tous infaisables. C'est
  le candidat naturel pour un premier lemme uniforme en torsion maximale.

Scripts (`c1_experimental/scripts`) : x19n_pairblock.py, x19q_pairblock_phase1.py, x19s_export_pairblock.py,
x23_cell_ablation.py, x24_survey_S.py, x25_fano_cellcross_blocks.py, x26_fano_psi.py, x26b_fano_flip_analysis.py,
x26c_fano_flip_search.py, x26d_cells_on_psi_flips.py, x27_fano_block_cells.py.
