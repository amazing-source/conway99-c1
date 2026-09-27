# 143 — Famille rigide D₂ₘ ⊃ D_m² : identités de bloc, lemme π, charges, recensement de 87

*27/09 soir. C1, avec C2 (morts de la paire 0 à la main). Maths d'abord ; le seul calcul est un recensement de 1 s.
Suite de notes/141 §3 et notes/142.*

## 0. Cadre
Enveloppes rigides 10, 44, 87, 132 : racines d_m^{2k}, voisin pair nb ⊃ D₂ₘ^k, avec **km = 12** (m = 2, 3, 4, 6).
- Un bloc C = D₂ₘ a deux moitiés H, H′ (= deux composantes D_m).
- **Nouvelles racines** du bloc : ±e_a ± e_b, avec a ∈ H et b ∈ H′. Il y a m² paires (a,b), chacune formée de deux items e_a + e_b et e_a − e_b.
- **Rigide.** Tout u est un spineur ±½ sur une moitié de chaque bloc. B₁ = hits(y₁) ⊔ hits(y₂), où w = 1 ; w = 3 ailleurs.
- **h sur un bloc** : S (tous ±½, norme m/2), I_j (j coordonnées ±1 sur UNE moitié) ou Z (nul).
- **y sur un bloc** : une moitié I (entière), une moitié H (dans ½+ℤ), et jamais |y_a| = 1 en même temps que |y_b| = 3/2. D'où trois types :
  - **E_e** : e coordonnées ±1 sur la moitié I, moitié H = (±½)^m ;
  - **F_f** : moitié I nulle, f coordonnées ±3/2 sur la moitié H ;
  - **O** : E₀ = F₀.
- **Comptage (tout y) : Σ_C (e_C + 2f_C) = 7 − km/4 = 4.** Vérifié sur les 3 913 paires de 87 : (4,4) partout.

## 1. Deux identités exactes par bloc (conséquences de (F) en rigide)
Notations :
- s = nombre de h de type S sur C ;
- p(a) (resp. q(b)) = nombre de h de type I dont le support contient a ∈ H (resp. b ∈ H′) ;
- t(a,b) ∈ {0,1,2} = nombre d'items de la paire (a,b) dans B₁ ;
- Y(x) = Σ_y y_x².

**(E1)** p(a) + q(b) + t(a,b) = 3 − s/2 pour toute paire.
- Équivalent : p + Y ≡ P sur H et q + Y ≡ Q sur H′, avec P + Q = 7/2 − s/2.
- C'est la diagonale de 4P_h + 7P_y, constante par moitié.
- Les profils de couverture I se LISENT sur les y, à la constante P près.
- s est pair : M(a,b) ≡ s (mod 2) et M ∈ {0, ±2} (voir (E2)). Le lemme Z par moitié redonne la même chose.

**(E2)** M := Σ_{S sur C} σ_H σ_{H′}ᵀ = −4 Σ_y y_H y_{H′}ᵀ, identité de MATRICES m × m.
- C'est le bloc croisé de 7I − Σvvᵀ. Les u n'y contribuent pas : un spineur vit sur une seule moitié.
- Seuls les y de type E contribuent (O et F sont nuls sur leur moitié I). Donc rang M ≤ #{y de type E sur C}.
- Sur les paires : |M| = 2 ⟺ paire touchée une fois, et M = 0 sinon.
- Conséquences :
  - s ≥ 2 s'il existe une paire touchée une fois ;
  - s ≤ 2 s'il existe une paire touchée deux fois (p + q = 1 − s/2) ;
  - s ≤ 4 dès qu'une paire est touchée ; s ≤ 6 toujours.

## 2. Lemme π (s = 2), forme générale
Soit s = 2, avec deux S notés h et h′, et π := σ_h σ_{h′} (fonction ±1 sur H ⊔ H′).
- Alors M(a,b) = σ_h(a)σ_h(b)(1 + π(a)π(b)). **Les paires touchées une fois sont exactement {π(a) = π(b)}.**
- **Cohérence bipartie.** Le motif des paires touchées une fois doit être de la forme (P×P′) ∪ (N×N′). Sinon, s = 2 est impossible.
- **Charge du bloc** : κ_C := (P_C h, P_C h′) = ¼ Σ_C π, lue sur les hits au signe global près.
- **Parité de classe** : h et h′ sont de même classe de D₂ₘ* ⟺ #{π = −1} est pair ⟺ 2κ_C est pair.
- **Signes** (paires touchées une fois) : σ_h(a)σ_h(b) = −sgn(y_a y_b) pour le y qui touche.

**Table des charges pour s = 2** (|κ|, au signe près), déduite des hits :

| type de bloc | paires touchées | s | \|κ_C\| si s = 2 |
|---|---|---|---|
| O=O, OxO | aucune | 0, 2, 4, 6 | 0 |
| F=O, FxO, F=F (F∩F′ = ∅ ; FxF est impossible) | doubles | 0, 2 | 0 |
| E_e=O, E_exO | simples O × H | 2, 4 | e/2 |
| E_e x F_f (la moitié H de F est la moitié I de E, et F ∩ O = ∅) | simples + doubles | **2** | e/2 |
| E=E, O₁∩O₂ ≠ ∅, O₁ ≠ O₂ | simples + doubles | **2** | \|O₁ Δ O₂\|/2 |
| E=E, O₁ = O₂ | doubles | 0, 2 | 0 |
| E=E, O₁∩O₂ = ∅ | simples | 2 (seulement si φ₂ = ±φ₁), 4 | (e₁+e₂)/2 |
| E x E (croisé) | simples + doubles | **2** | \|e₁ − e₂\|/2 |

Pour E_e x F_f et E_e=O, les signes donnent aussi (P_C h, y_E) = τ₀(m − 2e)/4, et y_E est entièrement du côté π = +g.

## 3. Compensation globale : le lemme K, écrit pour 87 (D₈³, m = 4)
**Formes de h** (colle D₈³ = ⟨svv, vsv, vvs⟩) :
- SS = (S_c, S_c, Z), avec les deux S de classe c ;
- SII = (S_s, I₁, I₁), avec le S de classe s et les deux I₁ sur les deux autres blocs ;
- IIZ = (I₂, I₂, Z) ;
- IZZ = (I₄, Z, Z).

**Lemme K.** Soit un bloc C avec s_C = 2, ses deux S notés h, h′, et sa charge κ_C. Alors, d'après (h,h′) = 0 :
- (i) SS(C,X) avec SS(C,X′), X ≠ X′ : (h,h′) = κ_C, donc κ_C = 0.
- (ii) SS(C,X) avec SS(C,X) : κ_C + (h,h′)_X = 0. Si s_X = 2, cela donne κ_X = −κ_C.
- (iii) SS(C,X) avec SII(C) : (h,h′) = κ_C ± ½ (S de h contre I₁ de h′ sur X). Donc |κ_C| = ½.
- (iv) SII(C) avec SII(C) : (h,h′) = κ_C + (coïncidences des I₁ sur les deux autres blocs), donc κ_C ∈ {0, ±1, ±2}.

Avec la parité de classe (2κ_C impair ⟺ une h est SS et l'autre SII), on obtient :
- **|κ_C| = 3/2 est IMPOSSIBLE.**
- |κ_C| = ½ ⟹ une SS et une SII.
- |κ_C| = 1 ou 2 ⟹ deux SII dont les I₁ coïncident |κ_C| fois avec des signes opposés au sens de κ, ou deux SS sur la même paire de blocs de charges opposées.

**Corollaire (mort immédiate).** Si un bloc de s = 2 FORCÉ a |κ| = 3/2, la paire est morte. Cela concerne :
- E₃xF₁, E₁xE₄, E₁=E₄ ;
- E₂=E₃ avec |O₁∩O₂| = 1.

Si le bloc n'admet que s ∈ {2,4} et a |κ| = 3/2 (par exemple E₃=O ou E₃xO), alors s = 4 est forcé.

## 4. Recensement de 87 (1 s, code/blocktypes_census.py <id> ; aucune recherche)
- 3 913 paires, 3 blocs D₈ chacune.
- **321 combinaisons distinctes** de types de bloc, **32 types de bloc**. Aucun type « BAD » : E et F ne coexistent jamais sur la même moitié.
- Types les plus fréquents :

| type | occurrences |
|---|---|
| F₁=O | 1 008 |
| E₂xO | 780 |
| E₁=E₂ | 776 |
| E₂=O | 746 |
| E₁=O | 690 |
| E₁xO | 676 |
| E₁=E₃ | 624 |
| E₁=E₁ | 568 |
| E₂=E₂ | 526 |
| E₁xF₁ | 476 |
| E₁xE₂ | 476 |
| E₂xF₁ | 452 |

- **1 722 paires** ont un bloc croisé à s = 2 forcé (ExE ou ExF).
- **328 paires sont tuées par le seul corollaire** (E₃xF₁, E₁xE₄, E₁=E₄). Les E₂=E₃ à |∩| = 1 n'ont pas été comptées : les étiquettes du recensement n'ont pas cette information.
- Une preuve paire par paire n'est pas envisageable (321 combinaisons). Le lemme de famille doit se situer au niveau des types de bloc.

## 5. Paire 0 de 87 : morte à la main (C2, 27/09)
- Blocs : A = E₂xF₁ (κ = ±1, s_A = 2 forcé), B = F₁=O, C = F₁=O.
- **Classe c** : morte par K(i)/(ii), puisque s_B, s_C ≤ 2 et que le bloc F donne κ = 0.
- **Classe s** : deux SII, avec une coïncidence exactement.
  - Sous-cas s_B = s_C = 0 : mort, selon trois mécanismes :
    - la parité des I₁ par moitié (I₂ et I₄ occupent un nombre pair de places) ;
    - la torsion : h′ = πh sur A, y_E entièrement du côté π = +g, puis h ⊥ y₁, y₂ ;
    - le débordement de couverture (E1).
  - Sous-cas (s_B, s_C) ∈ {(2,0), (0,2), (2,2)} : C2 les traite avec le même mécanisme.

## 6. Reste à faire (famille)
1. **Blocs à s = 4** (E=O et ExO avec e = 3 ; E=E disjoints ; blocs sans hits) : classer les matrices 4 × m de signes A, B avec AᵀB = Ψ. C'est un petit problème d'Hadamard.
2. **Lemme de torsion (C2), forme générale.** Pour un bloc à s = 2, h′|_C = π·h|_C. Donc (h ± gh′)/2 restreint à C vaut h restreint à {π = ±g}. Les orthogonalités à y₁ et y₂ imposent alors les parts extérieures (I₁ ou S), avec des coefficients dans {±½, ±1, ±3/2}.
3. **Même lemme K pour 132** (D₁₂², formes SI₁, I₂I₂, I₄), **44** (D₆⁴) et **10** (D₄⁶, hexacode) : seules les formes de h et la colle changent ; §1-2 valent tels quels.
4. **Conjecture (risquée).** Dans toute enveloppe rigide de la famille, les charges κ_C des blocs à s = 2 forcé ne peuvent pas être compensées simultanément avec la couverture (E1). Autrement dit, l'étage h meurt pour une raison locale-globale lisible sur le seul type de bloc. À confirmer sur 132, où il n'y a que 2 blocs et où tout SI₁ a une seule part extérieure.

## 7. 132 À LA MAIN (D₁₂², m = 6, k = 2) : test du lemme de famille
**Formes de h** (colle D₁₂² = {00, sv, vs, cc}) :
- SI = (S_s, I₁) ou (I₁, S_s) ;
- II = (I₂, I₂) ;
- I4 = I₄ sur une moitié.

**Conséquences générales pour 132 :**
- Tous les S sont de classe s, donc κ_C ∈ ℤ sur tout bloc à s = 2.
- Pour deux SI de S sur C : (h,h′) = κ_C + ε₁ε₂·[I₁ coïncidents sur C′]. Donc κ_C ∈ {0, ±1}.
- n_SI = s_A + s_B ≤ 6 (pair).
- s ≤ 4 sur tout bloc touché.

**Lemme T (torsion, |κ_C| = 1).** On pose g = signe(κ_C) et Π_g = {π = g} (le côté majoritaire). Comme h′|_C = π·h|_C, et que ε₂ = −κ_C ε₁ (I₁ coïncidents en x) :
- pour TOUT y : (h, y|_{Π_g}) = 0 et (h, y|_{Π_{−g}}) = −ε₁ y_x.

La preuve est une ligne : on ajoute et on retranche (h,y) = 0 et (h′,y) = 0.

**Or l'alignement des signes (E2)** fixe le premier terme pour le y qui produit les hits simples. Pour y de type E, on a σ(a)sgn(y_a) = −σ(b)sgn(y_b) sur ses paires touchées une fois. Cela donne :

| type de bloc (\|κ\| = 1) | (h, y\|_{Π_g}) |
|---|---|
| E₂xF₁, E₂=O (moitié I de E : 2 uns) | τ(6/4 − 1) = ±½ |
| E=E, O₁ ⊂ O₂, \|Δ\| = 2 | τ(6/4 − 1) = ±½ |
| E₂=E₂ avec \|∩\| = 1, E₃=E₃ avec \|∩\| = 2 | ±1 |
| E₁=E₁ disjoints | ±1 |
| E₂xE₄, E₁xE₃ | τ((6 − e₁)/4 − e₂/2) ≠ 0 |

Toutes ces valeurs sont non nulles. **Donc tout bloc à |κ| = 1 meurt dans 132.**

**Bilan par type de bloc (132) :**
- **Morts :** ExF (tous) ; E=E chevauchants avec O₁ ≠ O₂ ; ExE avec e₁ ≠ e₂.
- **s = 4 forcé :** E=O, ExO, E=E disjoints.
- **s = 2 avec κ = 0 (sans coïncidence) :** ExE avec e₁ = e₂.
- **s ∈ {0, 2} :** E=E avec O₁ = O₂, et les blocs F/O.

**Recensement de 132** (304 paires, 49 combinaisons) :
- mortes par le corollaire K : 102 ;
- mortes par s_A + s_B = 8 > 6 : 33 ;
- mortes par le lemme T et les nouvelles règles : 95.
- **Total : 230/304 à la main.**

**Restent 74 paires, en 14 combinaisons.** Elles ne comportent que des blocs à s = 4 (E=E disjoints, E=O), à κ = 0 (ExE avec e₁ = e₂, E=E avec O₁ = O₂) ou F/O :
- E₂=E₄ | F₁=O (20), avec E₂, E₄ disjoints, O₁∪O₂ = H et s_A = 4 ;
- E₁=E₁ | E₃=E₃ (10) ;
- E₂=E₂ | F₁=F₁ (8) ;
- E₂=E₂ | E₂=E₂ (5) ;
- F₁=F₁ | F₁=F₁ (4) ;
- E₂xE₂ | F₁=F₁ (4) ;
- E₂=E₄ | F₁xO (4) ;
- E₁xE₁ | E₃xE₃ (4) ;
- E₁xE₁ | E₃=E₃ (4) ;
- E₂xE₂ | E₂xE₂ (3) ;
- E₄xE₄ | O=O (2) ;
- E₄xE₄ | OxO (2) ;
- E₂=E₂ | E₂xE₂ (2) ;
- E₁=E₁ | E₃xE₃ (2).

**Prochaines pièces :**
- lemme s = 4 : AᵀB = Ψ, avec 4 SI dont les I₁ tombent sur l'autre bloc, et couverture p = [H∖O], q ≡ 0 ;
- torsion à κ = 0 (π constant par moitié, ou π de ExE à e₁ = e₂), sans coïncidence ;
- couverture (E1) avec parité des I₁ par moitié.

### 7.1 Deux nouveaux outils (132 ; valables pour toute la famille)
**Lemme H (s = 4, bloc dont TOUTES les paires sont touchées une fois).** C'est le cas E=E disjoints avec O₁ ∪ O₂ = H.
- **Colonnes.** On note c_x = (σ_i(x))_{i=1..4} ∈ {±1}⁴ et on renormalise : ρ_a = −ι(a) c_a sur H, t̃_b = φ₁(b) c_b sur H′.
- **Lemme Z par moitié** (Σh/2 ∈ U, avec P_X(U) ⊂ D_m* = ℤ^m ∪ (ℤ^m + ½)) : la parité de ∏_i c_x(i) est constante sur chaque moitié. (E2) donne ρ·t̃ = ±2, donc les parités des deux moitiés sont opposées. Quitte à changer le signe d'un S, t̃_b = s_b e_{k(b)}, où e₀..e₃ sont les lignes de Hadamard ±{1111, −−++, −+−+, −++−}. On écrit ρ_a = ½ Σ_k θ_a(k) e_k, avec ∏θ = 1.
- **Contraintes.** (E2) devient θ_a(k(b)) s_b = 1 (a ∈ O₁) et = λ(b) := φ₁φ₂(b) (a ∈ O₂).
  - Si chaque k apparaît : θ ≡ s sur O₁ et θ ≡ λ∘s sur O₂.
  - La Gram (h_i,h_j) = K_ij (coïncidences des I₁ sur l'autre bloc) s'écrit, dans la base ê_k = e_k/2 :
    **4 diag(n_k) + Σ_a θ_aθ_aᵀ = 12 I + 4 K̂**, où n_k = #{b : k(b) = k}.
- **E₂=E₄ disjoints** : hors diagonale, s_ks_l(2 + 4λ_kλ_l) = 4K̂_kl ∈ {0, ±2}. Il faut donc λ_kλ_l = −1 pour TOUS k ≠ l : impossible sur 4 indices.
  - La couverture de l'autre bloc force des coïncidences de type (2,1,1) ou (3,1). Dans le cas (3,1), 4K̂_kl ∈ {0, ±2, ±4, ±8, ±10} ne contient jamais ±6 : même contradiction.
  - **E₂=E₄ | F₁=O et E₂=E₄ | F₁xO : 24 paires mortes.**
- Cas K = 0 : la diagonale donne n_k = 3/2. Un bloc de s = 4 entièrement touché exige donc un nombre IMPAIR de paires coïncidentes.

**Lemme T₀ (κ = 0, sans coïncidence).**
- Pour tout y : (h, y|_{Π_g}) = −(ε₁y_{x₁} + gε₂y_{x₂})/2 et (h, y|_{Π_{−g}}) = −(ε₁y_{x₁} − gε₂y_{x₂})/2.
- Les deux valeurs sont bornées par max |y| sur les positions extérieures.
- **E₄xE₄ | O=O et E₄xE₄ | OxO** : l'alignement donne (h, y₁|_{Π_g}) = −3τ/2. Mais |y₁| ≤ ½ sur le bloc O. **4 paires mortes.**

**Bilan 132 : 258/304 à la main.** Restent 46 paires :
- E₁=E₁ | E₃=E₃ et variantes croisées (20) ;
- E₂=E₂ | F₁=F₁ et E₂xE₂ | F₁=F₁ (12) ;
- E₂=E₂ | E₂=E₂ et variantes (10) ;
- F₁=F₁ | F₁=F₁ (4). Ce dernier cas est possible sans aucun S : il faudra les cellules (u) ou la parité des I.

### 7.2 Lemme Z⁺ (structures, 27/09 soir ; preuve C1 en trois lignes)
**Énoncé.** U ∩ span(h) = ⟨h⟩ ∪ (⟨h⟩ + Σh/2). Autrement dit, (Σ_T h)/2 ∉ U pour 1 ≤ |T| ≤ 6.

**Preuve.**
1. Soit v = Σ a_c h_c ∈ U. Chaque u est une racine ±e_c ± e_d de D₇, et (u, h_c) = −C_{cu}.
2. Pour toute paire {c,d}, les deux u de signes C_cC_d = ±1 donnent a_c + a_d ∈ ℤ et a_c − a_d ∈ ℤ.
3. Donc 2a ∈ ℤ⁷, et tous les a_c sont congrus mod 1.

La condition ne dépend que des h : elle est valable dès l'étage h, puisque les u doivent exister.

**Corollaire.** La demi-somme de deux h n'est jamais un vecteur de U, en particulier jamais une racine de U. Par exemple :
- **deux I₄ de même support** sur une moitié sont exclus : leur demi-somme est une racine de D_m ;
- deux I₂I₂ de mêmes supports, dont les signes sont d'accord sur un bloc et opposés sur l'autre, sont exclus.

Cela donne un raccourci pour R1 (§7.1) : les deux I₄ de support identique sur X′_B sont exclus immédiatement.
