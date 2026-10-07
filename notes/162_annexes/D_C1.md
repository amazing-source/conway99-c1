*Annexe de la note 162 : rapport d’un agent de lecture (07/10/2026), versé tel quel. Les affirmations sur les autres dépôts sont celles du rapport ; voir la note 162 pour la synthèse et les réserves.*

# Inventaire du dépôt conway99-c1 (branche C1, sans hypothèse de symétrie)

Base : `/home/user/conway99-c1/`. Je n'ai rien modifié, rien commité, rien poussé. J'ai lu en entier README, LAB_INSTRUCTIONS_C1, rapport, JOURNAL et toutes les notes, ainsi que les journaux de calcul (`data/*.runlog.out`) et les registres (`data/rank17`, `code/r6`).

**Points de forme.**
- Les notes sont numérotées 00, 10, 20, …, 90, puis 91 à 161 (avec 161b et 161c). Il n'y a pas de notes 1–9 ni 11–19.
- L'historique git compte 65 commits, du 27/09 au 07/10. Le premier commit importe d'un bloc tout le corpus (843 fichiers) : l'historique des 24–27/09 n'existe pas dans git.

**Abréviations de statut utilisées partout.**
- [M] : preuve à la main.
- [M+V] : preuve à la main, plus des vérifications finies exhaustives.
- [CA] : calcul exact assisté par ordinateur, non certifié par un tiers.
- [SAT-nc] : verdict UNSAT d'un solveur, sans preuve DRAT et sans contrôle positif sur BvLS.
- [Cert] : certificat exact (Farkas rationnel), revérifié par un code indépendant.
- [Cond] : résultat conditionnel.
- [Ouv] : ouvert.

---

## 0. Notes 155–161, en bref

- **155.** Théorème : les transferts sont exactement la classe [q] = q + M, et φ = ‖z‖² − 2k² mod 7 est un invariant de classe. Au niveau 0, le minimum de [q] vaut 26 ou 40. V7 est reconstruit (24 noyaux, 12 orbites). Le CVP exhaustif tue 1 828 couples sur 13 812. La survie des germes tombe à 18 %, puis 4,4 %, puis 0,55 %. Le SAT complet de V7 reste UNKNOWN.
- **156.** Il n'y a pas de route finie à la manière de C2 : la masse du genre unimodulaire pair de rang 48 vaut environ 1,5·10¹²¹, et la branche 18 compte environ 8,4·10⁹ configurations au niveau 1.
- **157.** La route Ω est complète (lemmes 1–3). Équivalence (★) : il faut et il suffit d'un Γ 12-régulier sur les 84 labels avec T² = 7T. On obtient un repère tendu de R³⁰.
- **158.** Deux étoiles mates forment la boule d'un triangle. Théorème de rang 8 : Z = F₋₄ ⊕ F₃. L'étage F est presque forcé.
- **159–160.** Il existe un second srg(243,22,1,2), tordu, qui réfute la conjecture des hexagones de Reimbayev (arXiv:2409.10620). Estimation de non-existence : environ 75 %.
- **161, 161b, 161c.** Le dépôt openai/math ne contient rien sur 99. Sa hiérarchie de moments, réimplémentée dans `code/moments/`, redonne seulement notes/91.

---

## 1. Lemmes et théorèmes numérotés

### 1.1 Les lemmes L1–L25 (fichier maître : notes/30_LEMMES.md, synthèse dans notes/100)

| Lemme | Énoncé (cité ou quasi littéral) | Statut | Antériorité selon le dépôt | Où |
|---|---|---|---|---|
| **L1** | « Γ est tordu : il existe x, a, b ∈ N(x) avec τ_a(b) ≠ b̄ ». Tout PQ(2,t,2) grid-full est revêtu par H(t+1,3), donc n = 3^m ; 6 273 et 494 019 sont donc eux aussi forcément tordus. | [M] par revêtement universel du 2-complexe triangles + quadrangles. Seconde preuve, spectrale, via L16. | **Connu : Makhnev 1988, Mat. Zametki 44(5), théorème 2**, avec une autre preuve (srg(33,12,1,6) dérivé). La preuve par revêtement est indépendante. | 30, 94 §3.1 |
| **L2** | « rank₇(A − 3I) est impair », avec 15 ≤ rank ≤ 45. | [M] (genres 2- et 11-adiques). | « des énoncés voisins existent peut-être chez Brouwer–van Eijl » ; c'est aussi le Théorème A de C2. | 30 |
| **L3** | « la forme de recollement 7-adique de Λ₃ est non scindée ». | [M] (formules d'oddité). | Même remarque. | 30 |
| **L4** | « k(x) = rank₇((H−3I)\|_K) = rank₇(A−3I) − 15 est le même en tout sommet et pair », avec 0 ≤ k ≤ 30. | [M], plus le calcul exact du 15 (glue7.py), contrôlé sur srg(9) et BvLS. | Version démontrée de la « piste C » de ChatGPT. | 30, 20 |
| **L5** | Grilles serrées : tout point extérieur a exactement un voisin dans une grille, et (A−3I)g = g_tot·1. Le serrage est propre à 99 dans la famille (k ∈ {4, 14}). | [M] | Classique, non revendiqué (Bamberg–De Clerck–Durante 2011). | 00, 30, 104 |
| **L6** | Identités enracinées : 2-facteur étiqueté, M(x) + D(x) = \|X\|, d_X(u) = 2 + …, et χ(Σ) = 3P − 4158. | [M] | — | 30 |
| **L7** | « Un point de Hamming (τ = mate en x) n'est jamais le point fixe d'une involution ». Donc, en C2, le point fixe est tordu. | [M], quatre preuves : parité des décalages diagonaux sur 105 triplets (0 ≡ 1) ; cocycle avec H¹(K(7,2);F₂) = 0 ; Kneser signé ; lemme spectral. L'ancienne version reposait sur deux SAT (201 s et 34 s). | Aucun équivalent trouvé. | 95, 103 §2, 105 §7 |
| **L8** | « Aucun sommet n'est un point de Hamming » : x n'est jamais dans ses 21 grilles. | [M+V]. Squelette de Fano (exactement 30 fonctions ℓ), section X, lemme B/C, puis 35 configurations exclues. Quatre vérifications finies : S₄³, squelettes, 722 indépendants, systèmes F₂. L'ancienne version était un SAT non certifié (2 114 s). | Lou–Murin 2014 §3 ne s'en servent que pour étiqueter (30 plans de Fano). Seule la chaîne de preuve est revendiquée. | 105 (+103) |
| **L9, L9′** | L9 : τ_a(c) ≠ c̄, τ_c(a) = ā et τ_ā(c̄) = c ⇒ une grille G_{[c],m} manque. L9′ : τ_a(c) ≠ c̄ et τ_{c̄}(a) = ā ⇒ même conclusion. | [M]. L9′ est extrait d'un noyau UNSAT minimal de 7 contraintes. | Nouveau. | 30 |
| **L10** | g(x) ≤ 18 : 19 par L12 ou L9′, 20 par parité, 21 par L8. Amélioré ensuite en **g(x) ≤ 17** (notes/108). g ≤ 16 reste ouvert, avec 20 configurations. | [M] | — | 30, 108, 112 |
| **L11** | « Les torsions ne peuvent pas être confinées à 3 classes. » | [M] (lemme D1). L'ancienne version était un SAT de 1,2 s. | — | 108 |
| **L12** | « τ_a(c) ≠ c̄ ⇒ τ_c(ā) ≠ a, ou bien il existe y hors de [a] ∪ [c] avec τ_y(c) ≠ c̄. » Vaut dans toute géométrie localement (t+1)K₂. | [M] ; 0 violation sur 12 828 paires. | Nouveau. | 30 |
| **L13** | « Une classe est tordue par 0 ou au moins 2 étiquettes » : ρ_ℓ permute Z sans point fixe. | [M] | — | 30 |
| **L14** | « Deux étiquettes tordues ne suffisent pas. » | \|C\| = 2 : [M], relu par « structures » sauf la réduction initiale. \|C\| = 3 et 4 : [SAT-nc] (1 120 s et 2 695 s). **\|C\| = 5 : [Ouv]** (aucun verdict SAT, bilans exacts cohérents). | — | 30, 50, 111 |
| **L15** | P = 1386 − (1/6)Σ_x\|W(x)\| et Σ_x\|W(x)\| = 6048 + Σ_rot ν³. | [M] | n₃ = 3(P_max − P) = ½Σ\|W\| est la variable libre de **Reimbayev, arXiv:2608.19410** (confirmation indépendante). | 30, 60 |
| **L16 (Théorème K1)** | « 12P = 13860 − 64‖Σ_L u_L^{⊗3}‖² », donc P ≤ 1155, et **P ≤ 1151** en ajoutant les points. De façon équivalente : Σ\|W\| ≥ 1410 (≥ 14,2 par sommet en moyenne), n₃ ≥ 705, et au plus 10 prismes par droite en moyenne. | [M], audité indépendamment (notes/98) ; contrôle sur BvLS à 10⁻¹³. Ne mord qu'à t = 6 dans la famille. | Aucun équivalent trouvé. | 70 |
| **L17** | Le 70-espace K est pair, de det 2²¹·3⁸·5⁶, et K⊗Z_p = K₃ ⊥ K₋₄ pour p = 2, 3, 5 ; l'oddité donne k/2 ≡ k₇. | [M] ; contrôle sur BvLS (p = 5). | — | 80 |
| **L18** | S = #{(x,E) : E ∼ σ_x(E)}. Alors z₂ = S/2, z₃ = Σ\|W\| − 2S et z₁₁ = 2Σ\|W\| − 2S. Dans un SRG, z₁₁ = 4n₃ − 2S, et le polygone d'ordre 7 est exactement **0 ≤ S ≤ n₃**. Grilles avortées : \|Σ_G p\|² = 18(18 − e). | [M], plus comptage direct sur 3 géométries tordues, srg(9) et BvLS. | Identifie la seconde variable libre de Reimbayev. | 90 |
| **L19 / L19 bis** | La forme de Smith 7-adique de U_x = (2H + I)Σ_x est 1^k·7^{70−2k}·49^k, avec un déficit ≤ k ; si k = 0, il y a des congruences en chaque sommet. L19 bis : **k ≥ 2**. | [M] | Principe de L19 bis : van Eijl 1991 §3.3 (crédité). | 93, 94 §1 |
| **L20** | « k ≥ 11 − 2e(τ_a) ». D'où k ≥ 6 ; k = 6 ⇒ P = 0 ; P ≥ 1 ⇒ k ≥ 8 ; une étiquette non tordue ⇒ k ≥ 12. | [M], plus vérification exhaustive sur les 10 395 couplages. | Principe : van Eijl 1991 ; l'application à 99 est nouvelle. | 97 |
| **L20 bis** | k ≠ 6, donc k ≥ 8. Passe par la formule locale k = rank₇(H + 4I + 3S + P′ + 5J). | [M] | — | 97 |
| **L20 ter** | k ≠ 8, donc **k ≥ 10**, c'est-à-dire rank₇(A − 3I) ≥ 25. | [CA] : énumération sur F₇ (32 sous-espaces), puis 32 petites instances UNSAT par propagation. Pas de DRAT. | — | 97 |
| **L21** | rank₇(A−3I)[L ∪ N(L)] = 2 + rank₇(A_{G(L)} − 3I), donc **k ≥ 23 − d(L)**, où d = composantes + 7-rang du groupe critique du graphe cubique G(L). Une droite générique donne k ≥ 22. | [M] ; 700 configurations testées. La conjecture d ≤ 9 (qui donnerait k ≥ 14) n'est pas prouvée. | — | 99 ; raffiné en notes/126 |
| **L22** | rank₇(A − 3I) ≤ 43, soit **k ≤ 28**. La partie 7-unimodulaire de Λ₋₄ est non nulle et jamais hyperbolique. | [M] : à k = 30, (9\|7) = +1 alors que l'oddité exige −1. Conventions testées sur 2 300 réseaux ; schéma validé sur Petersen, T(7), T(8) et srg(9) ; seconde dérivation par K₋₄(x). | La borne connue est 45 (van Eijl 1991 ; Brouwer–van Eijl 1992). « Le raffinement semble nouveau. » | 101 |
| **L23** | Q = A − 3I + 3J est le Gram d'une forme β **non scindée**, et un bloc de rang extrême est non scindé. Pour une droite : rang 37 − d(L), et disc ≡ τ(G(L)) si d = 1. Donc **(τ(G(L))\|7) = +1 ⇒ k ≥ 24**. Il existe une version Seidel (mineurs de J − I − 2A). | [M] ; 300 configurations et 5 SRG. | « Paraissent nouveaux. » | 102 |
| **L24** | En un point de Hamming, on a une S₄-connexion sur K(7,2), et **18 ≤ k ≤ 26**. | [M]. Rendu vide par L8. | — | 103 |
| **L25** | « Aucun srg(99,14,1,2) n'est partitionné en 11 grilles induites dont chaque couplage est un iso- ou un anti-isomorphisme. » Thm A : tout anti ⇒ **plan projectif d'ordre 10 avec polarité** (exclu par Lam). Thm B : tout iso ⇒ 7 \| 220, absurde. Lemme C : les signes forment 1, 2 ou 11 classes. Thm D : deux classes ⇒ tailles {2, 9}, puis β − α/2 ≤ 2. | [M], plus l'énumération des 72 automorphismes de la grille ; contrôle inverse PG(2,4) → srg(15,6,1,3). | Recherche rapide : aucun lien connu entre 99 et l'ordre 10 (« à confirmer »). | 104 |

**Collisions de noms.**
- « L1 », « (L0)/(L1)/(L2) », « (L5) », « (L7) » réapparaissent avec d'autres sens dans les notes 137, 140, 146 et 151.
- « Lemme U » désigne deux énoncés différents (notes/108 et notes/145).

### 1.2 Autres théorèmes et lemmes nommés (hors 155–161)

**Branche C1.**
- **notes/00.**
  - F7 : rank₂(A) = 54 et rank₂(A + I) = 45, forcés.
  - F8 : t + 1 = r − s ⟺ t = 6. Le graphe des droites n'est singulier qu'à t = 6. [M]
- **notes/60 (route Hodge).**
  - **Théorème H0** : le confinement du spectre rotationnel ⇒ M = 0 ⇒ grid-full ⇒ M ≠ 0 pour t ≥ 2. Il est donc faux pour tout SRG de la famille. [M], contrôlé sur BvLS : {−20¹¹, −5⁶⁶⁰, −2⁶⁶⁰, 4⁸⁸⁰, 7²²⁰}.
  - **H1** : deux droites disjointes sont reliées par 0, 1, 2 ou 3 arêtes.
  - **H2** : ‖[Q, B_T]‖² = 24(P_max − P).
  - **H3** : traces par blocs. [M]
- **notes/80.**
  - Σ|W| = 1386 + 32‖Σ_L u_L^{⊗3}‖² : la torsion est le moment cubique des droites. [M]
  - Identité locale : « les droites éloignées portent la torsion ». [M], 3 057 couples.
- **notes/90.**
  - Δ ⪰ 0 sur E₋₄, et Δ = 0 ⟺ non tordu.
  - Z = J − I − A dans le cas non tordu.
  - s(x) ≤ |W(x)|.
  - La borne de Delsarte locale est triviale. [M]
- **notes/94.**
  - Lemme de variance pour 99 : c(F) = 99 + N(N−16) − ½Σd_i(d_i−2). Il exclut tout sous-graphe induit 4-régulier à 10 sommets. [M]
- **notes/96.**
  - Repères serrés entiers exacts : L₋₄ = 24I + 2J − 8H − 3S − P′ (rang 30, constante 56) et L₃ = 60I − 2J + 15H − 4S + P′ (rang 40, constante 105).
  - Gram des droites : K² = 21K.
- **notes/102.**
  - Structure 7-adique : N² ≡ 2J, β non scindée, forme de M_x hyperbolique.
  - S² = 49(I + J). Γ équivaut à **99 droites équiangulaires de R⁴⁵ d'angle arccos(1/7)**.
  - Smith de S : 1^{14+k}·7^{71−2k}·49^{14+k}.
  - Critère de non-existence : un S avec rang₇ Q_SS ≥ 43, ou égal à 42 et scindé.
  - R_L est de rang k − 22. [M]
- **notes/103.**
  - Le régime « aucune arête isométrique » est impossible (tournois). [M]
  - L7 local et L7 local généralisé. [M]
  - Classification des holonomies d'arête. [M+V]
  - Parité S₃ du fait C.
  - Le modèle local autour d'un triangle de classes a 1 522 solutions : la contradiction de L8 est globale.
- **notes/104, annexe.** Si α = 22 (Hoffman), les 77 sommets restants ont pour spectre 10¹, 3³³, (−1)²¹, (−4)²², et forment un 2-(22,4,2).
- **notes/105.**
  - **Théorème du squelette de Fano.**
  - Lemme B/C.
  - Lemme spectral (S_I − 5)(S_I + 2) = −KKᵀ.
  - Lemme des composantes.
  - Cas coupe (28 coupes sur 2²⁰).
- **notes/106.** « Toute preuve 7-adique doit contrôler G » ; un bloc sans inconnue a au plus 39 sommets (EKR). [M], résultat négatif.
- **notes/107.**
  - Les ensembles −4-serrés portent le défaut de L22.
  - À k = 28, deux cocliques de Hoffman se coupent en **1, 8 ou 15** points, et |C ∩ S| ≡ 4c (mod 7). [M]
- **notes/108.**
  - Lemme U (unicité des fentes).
  - **D1** (les défauts ne sont jamais deux à deux sécants).
  - **D2** (chemin impossible).
  - **g(x) ≤ 17**. [M]
- **notes/110.**
  - Les codes des droites contiennent leur dual pour p = 2, 3, 5.
  - **rank₂N = 72 + ½·rank₂(NᵀAN) ≥ 72**, rank₅N ≥ 72 et 77 ≤ rank₃N ≤ 98.
  - Arf(C₃) = 1.
  - Bornes de Minkowski : min Λ₃ ≤ 36 et min Λ₋₄ ≤ 44. [M]
- **notes/111.** Lemme : pour tout |C|, les deux torsions ont le même graphe de classes. [M]
- **notes/112.** Lemmes 0, A et B. g ≤ 16 se ramène à 20 configurations. [M], plus un contrôle fini.
- **notes/113.**
  - R3 : **no-go**, le mécanisme de C3 exige une symétrie d'ordre impair.
  - R3 bis : le gain d'Eisenstein n'a aucun spectre à 3 valeurs ou moins.
  - R4 : Σ_S (−1)^{#droites coupées} = −2⁷².
  - Auteurs : « structures », et C2 pour R3 bis.
- **notes/114.**
  - spec(F_L) est fixé par G(L) ; réseaux lointains de rang 18 et 8.
  - Équilibre d'une droite ; principe de variance nulle (Rayleigh) ; lemme E.
- **notes/115. Lemme du triangle** (à ne pas confondre avec le rang 8 de notes/158) : T ⪯ 3I − P_∂, donc e ≤ 12 ; au cas tendu, Aq = 3q. [M], recalculé par « structures ». Il tue 22 % (23 sur 103) des configurations localement admissibles en torsion maximale (échantillon).
- **notes/116.** A_Δ² + A_Δ − 12I = 2J − ∂ᵀ∂ ; identités (P2) ; critère lointain (U)/(L) ; (F5). [M], relu.
- **notes/117.**
  - **(P2) ⟺ Σ_z ξ_zξ_zᵀ = 196·P_{E₋₂}**, un repère tendu de R¹⁴.
  - Identité du 4-cycle alterné. [M]
- **notes/118.** cellcross ; fonctionnelle universelle Ψ_R au Fano tendu. [M]
- **notes/119. Lemme P-Ψ** : θ(z_X(y)) + θ(z_Y(y)) = 0 au Fano tendu. [M], relu.
- **notes/120.**
  - En tout sommet, au moins 5 vecteurs propres cellulaires de valeur 3 (sur Q), et au moins 35 − k ≥ 7 mod 7.
  - Règles des triades. [M]
- **notes/122.**
  - Lemme des différences de retournement : T(L) est sans triangle ⟺ poids(d(L)) ≠ 1.
  - Identité des parités de branche. [M], relu.
- **notes/123.** H(x) = 12 936 en tout sommet si P = S = 0. [M] Le reste de la note est déjà connu (voir §4).
- **notes/124.** Φ_F = −7Π. [M], contrôlé sur BvLS (−9Π).
- **notes/125.**
  - Σ_L c₃(G(L)) = 2P et **Σ_L c₄(G(L)) = S + 3P**.
  - Critère de maille ≥ 5 ; lemme « de Klein ».
  - À P = S = 0, seuls restent les profils connexe et (6,6). [M], vérifications exhaustives.
- **notes/126.**
  - **L21 raffiné** : 14 + k = (37 − d) + 2r + ρ, donc k ≥ 22 + r − r₀.
  - À P = S = 0, une droite (6,6) force k ≥ 22.
  - [Cond] Sous l'hypothèse NT : k ≥ 18.
- **notes/128.**
  - **Lemme R** : à P = 0, un sommet dont les 7 droites sont (4,4,4) vérifie S(x) = 84.
  - Corollaires : V₄₄₄ est indépendant, et « (4,4,4) partout » est impossible.
  - [Cond NT] k ≥ 20, et k ≥ 22 à P = 0. L'exclusion de k = 18 (§3 bis) « reste à relire ».
  - Inconditionnel : P = 0 et k ≤ 20 ⇒ au moins 26 droites à torsion équilibrée.

**Branche involution (C2), travaillée par la session C1.** Résumé en §2.5.

---

## 2. Autres découvertes

### 2.1 Nouveaux objets
- **Géométries tordues non SRG**, localement (t+1)K₂, avec λ = 1 et μ ∈ {0, 2} :
  - t = 2 : le graphe des arcs de K₅ (20 sommets, |Aut| = 240), seule géométrie connexe tordue à ≤ 34 sommets ;
  - t = 3 : 39 sommets, tripartite, ensembles de différences de PG(2,3), |Aut| = 78 ;
  - **t = 3 : 42 sommets**, 56 droites, |Aut| = 672, d'origine non identifiée. Ce n'est pas la géométrie des triangles orientés de Fano ;
  - **famille tri-incidence (S, −2S, S)** sur Z_{q²+q+1} : tordue pour q = 3, 5, 7 (39, 93, 171 sommets), et vide pour q = 2, 4.
  - Les produits cartésiens réfutent F17 naïve : il existe des géométries tordues à t = 6 sans plan d'ordre 6.
  - Fichiers : `data/t2_twisted.json`, `t3_twisted*.json`, `zoo_*`.
- **Repères et réseaux.**
  - Repères serrés L₋₄ et L₃ (notes/96).
  - Réseau des droites Λ_L : 231 vecteurs de norme 4, avec K² = 21K.
  - Repère tendu de (P2) dans R¹⁴.
  - Fusion frame Σ_x P_{V_x} = (63/4)I₄₄.
  - Repère d'Eisenstein des droites orientées, de constante 1134.
- **Codes.** Codes p-aires des droites C_p ⊇ C_p^⊥, et code des ensembles pairs de dimension ≤ 27.
- **Graphes.** Le second srg(243) (connu de vous).

### 2.2 Reformulations structurelles (exactes)
- Γ est le quadrangle partiel PQ(2,6,2). Les transitions τ forment un système de Kotzig, et on dispose de l'holonomie de droite (notes/00).
- **Point de Hamming ⟺ S₄-connexion sur K(7,2)** soumise à (K) et (T) (notes/103).
- **Tissu de 11 grilles ⟺ 55 permutations vérifiant (E)** ; le régime anti donne PG(2,10) (notes/104).
- Le facteur 7 de k se lit sur M_x = H + 4I + 3S + P′ + 5J, une matrice 84 × 84 en un seul sommet.
- Droites équiangulaires (99 dans R⁴⁵) et deux-graphe de Seidel.
- Cibles exprimées comme équivalences :
  - non-existence ⟺ « tout Γ a Σ|W| ≤ 1409 », compte tenu de L16 ;
  - une preuve de k ≤ 4 suffirait (notes/97) ;
  - « k ≥ 30 », « les 7-primitifs sont isotropes » et le critère de notes/102 sont trois formulations équivalentes (notes/107).

### 2.3 Résultats calculatoires (aucun DRAT n'existe pour un résultat C1)

| Problème | Verdict | Statut |
|---|---|---|
| Point de Hamming + σ_x ∈ Aut | UNSAT en 201 s (adjacence) et 34 s (modèle φ) | [SAT-nc], remplacé par L7 [M] |
| Point de Hamming général | adjacence : UNKNOWN à 30 min ; modèle φ : UNSAT en 2 114 s sans cassage de symétrie, 46 s avec ; adjacence + cassage : 100 s ; variante « au moins un φ non isométrique » : 2 244 s et 56 s | [SAT-nc] ; la validité du cassage n'est rédigée nulle part ; remplacé par notes/105 |
| g = 19 (3 cas) ; une étiquette ; une classe ; confinement à 3 classes | UNSAT par propagation unitaire (de 0,0 à 1,2 s) | remplacés par des preuves [M] |
| Confinement à 4 classes ; sources {00,10}, {00,10,20}, {00,01,10,11} | arrêtés entre 73 et 81 min (manque de RAM) | **UNKNOWN** |
| Deux étiquettes, \|C\| = 2 / 3 / 4 / 5 | UNSAT (68,6 s et 40,5 s ; famille 92,5 s) / 1 119,7 s / 2 695,1 s / aucun verdict | [SAT-nc] ; \|C\| = 5 **UNKNOWN** |
| Trois étiquettes (128 motifs) | 24 UNSAT (≤ 73 s), 2 UNKNOWN, 1 sans sortie, 101 non lancés | [SAT-nc] |
| Famille Fano-cohérente, fano_first, type (2,2,2), τ aléatoire, squelette CET | aucun verdict | **UNKNOWN** |
| L20 ter | 32 instances UNSAT par propagation | [CA] |
| twist_search | t = 2 : n = 19 UNSAT, n = 20 SAT, 21 ≤ n ≤ 34 UNSAT. t = 3 : 33 à 38 UNSAT, 39 SAT, 40 et 41 UNSAT, 42 SAT, 43 UNSAT | SAT vérifiés ; UNSAT [SAT-nc] |
| Tri-circulants à t = 6 | N = 34 : 0 solution (3 402 s) ; N = 35 à 60 : jamais conclu | partiel |
| Tri-incidence (Sidon) à t = 6 | N = 44 à 64 : aucune solution | [CA] |
| Analogue q = 2 | Gewirtz reconstruit en 1,9 s ; avec une fermeture en 3-cube imposée : UNSAT en 13 s ; Clebsch trouvé | validation de la méthode |
| PL de torsion maximale (notes/117–118) | 19 sur 31 configurations infaisables ; cellules 19/19 ; paire × bloc : 2 cas certifiés, 1 en flottants | [Cert] par configuration (échantillon, pas un théorème) |
| Comptage des fentes (notes/108) | étoiles \|C\| = 2 et 3 et chemin : Farkas exacts ; L14 \|C\| = 2 et 3 : relaxation faisable | [Cert] |
| Fano tendu (notes/116) | tous les systèmes dérivés sont faisables (HiGHS) | ensuite tué au niveau cellules |
| SDP/PL d'ordre ≤ 8, triplets de droites | P ∈ [0 ; 1151,08], puis [0 ; 1155] | flottants (« optimal_inaccurate » sur les minima) |
| RRR et recuit simulé | Hoffman–Singleton et Gewirtz trouvés ; srg(81,20,1,6) non trouvé ; 99 atteint 59,3 % du score de Thakkar–Severini | heuristique ; le plateau est un phénomène d'algorithme |

### 2.4 Résultats négatifs (routes closes, avec la raison)
- **Hiérarchie exacte jusqu'à l'ordre 8** (916 types), avec toutes les positivités euclidiennes et de drapeaux : on retombe sur le « mur L16 », sans aucune borne inférieure sur P ni contrainte sur S. L'intégralité p-adique à l'ordre 8 ne donne aucune congruence (notes/91 et 105).
- **Triplets de droites** (ordre 9, repère de dimension 132) : P ∈ [0, 1155]. Une droite sans aucun prisme reste admissible (notes/99).
- **Krein et Gegenbauer** jusqu'au degré 16, Krein local, drapeaux : rien au-delà de L16.
- **Route Hodge / Σν³** : close par H0 ; borner Σν³ revient à majorer n₃.
- **Second moment de Δ** : un carré linéaire contre une quantité quadratique ; échec expliqué.
- **Genre et discriminant** : tout est cohérent pour chaque k pair ≤ 28 (R1–R4, L17, notes/102 §9). Nikulin ne mord pas sur le lointain d'une droite.
- **Fonctions F₃** de somme nulle et **parités d'holonomie** : présentes dans les géométries tordues, sans loi.
- **Akiyama sur Λ_L** : en rang 48, S₂₆ ≠ 0, pas d'isolement des racines (notes/110).
- **Droites équiangulaires** : la borne 540 ne donne aucune prise.
- **Identités de comptage** μ/λ sommées sur des classes : toujours automatiques, constat méthodologique de notes/151 §2quater.
- **Contenu de C3** : no-go, il faut une symétrie d'ordre impair.
- **Repère et réseau d'ordre 6–7 de openai/math** : redonne notes/91.

### 2.5 Branche involution (C2), travaillée par la session C1 (notes 129–154)
Ces notes portent sur le cas involution et concernent votre branche C2, pas C1.
- **q:7 (notes/129–133).**
  - g = rank₇(S − 3I) est pair et ≤ 20 (C2 Th. B, « structures »), et g = rank₇(T − 3I).
  - Boule impaire : rang 6 + rang₇ Q_c ; L23 dédoublé.
  - t_c ≤ 4, par exhaustivité.
  - g⁻ = 14 est exclu ; **g⁻ = 16 est exclu** (Witt, équilibre, lignes rigides ; 96 classes ; 8 certificats de Farkas revérifiés).
  - Donc **g⁻ ∈ {18, 20}**.
  - Recensement : 3 308 types de blocs.
- **Secteur pair (notes/135).** g⁺ ≠ 14 par HiGHS, non certifié. Si g⁺ ∉ {14, 16}, alors k ≥ 22, et k = 22 force g⁻ = g⁺ = 18.
- **Motifs Σ ≠ ∅ (notes/130–131).**
  - Toute la famille ancrée est morte.
  - P₅ est tué à la main ; K₃, K₂ et 2K₂ par le modèle U de C2 ; 3K2_or14 par q:7, « sous réserve de relecture » de q7_3k2_ext.py.
  - rang K ≤ 14 ; au plus un bloc A111111 quand Σ = ∅.
- **Ligne d'arrivée (notes/134–137).**
  - Lemme mono-bloc et identité générale.
  - Échelle des pivots : Σ#piv = 42 + 2|Σ| − 2n_dis.
  - Σ_c(2#piv_c + d_c) = 84 + 4|Σ|, d'où un bloc lourd et la complétude des instances I(τ). Il reste (A), 1 507 types, et (B), le cas tout-dis.
- **Route (C) (notes/139–145).**
  - L'involution donne un repère de 51 vecteurs dans un réseau unimodulaire impair de rang 24 ; les candidats sont les 156 réseaux de la table −4 de Borcherds.
  - 10 exclus, dont 117, 134 et 142 (critère spinoriel, C1) et 154 (packing).
  - **132 exclu** par une recherche exhaustive des h sur 304 paires y, « à relire par un humain », après un bug de bitsets.
  - 87 : 328 paires tuées par le corollaire K, la paire 0 à la main. 132 à la main : 258 paires sur 304.
  - 124 (non rigide) : 40 paires sur 40 échantillonnées sont mortes avec le lemme U+.
  - Lemmes Z, Z⁺, connexité, packing ; O₂₄ réduit à 141 classes.
- **Rang 17 (notes/146–148).** 59 couples (V, paire y) sur 1 272 sont exclus par calcul ; **E8² + ℤ et D16⁺ + ℤ le sont entièrement**. 1 213 restent seulement compatibles mod 4 (statut PATTERN). Le théorème DC (passation de l'utilisateur) réduit l'arbre d'un facteur 2 à 3.
- **notes/149–150.**
  - L'identité des sept étoiles est automatique ; BvLS et Paley9 sont « tout-frère ».
  - **min K\* ≥ 9/7 tuerait les 1 272 couples.**
  - Témoins n = 5 : classes A à D ; en classe A, β ∈ {12, 14, 16} ; aucun modèle symétrique sous C₅.
- **R6 (notes/151–152).**
  - Lemme de capacité des lignes ; J1b clos.
  - **J1a clos** : types (i), (ii), (iv) et (vi) à la main ; (iii) et (v) par une énumération PSD exhaustive (4,1·10⁹ configurations), suivie d'une complétion du rang.
  - J2 et J3 restent ouverts.
- **notes/153–154 et commits ultérieurs.**
  - Moteur R5 validé ; **seule l'orbite 3 (855 structures sur 53 079) a été exécutée**, avec 0 survivant.
  - Registre rang 17 : 754 → 526 classes ouvertes après le test caractéristique de C2 (228 morts, revérifiées par C1, `data/rank17/char_coverage.json`).

### 2.6 Documents, outils, données
- **README.md** : état arrêté au 25/09 à 9 h. Il parle de « 21 lemmes » alors qu'il en existe 25.
- **rapport/RAPPORT_C1.md** : s'arrête au 25/09 (§1 terdecies), avec la feuille de route du 25/09.
- **JOURNAL.md** : couvre du 24/09 au 26/09 (note 130), puis les 06–07/10. Aucune entrée du 27/09 au 05/10.
- **LAB_INSTRUCTIONS_C1.md** : **gelé le 25/09** (« plus aucune campagne de solveurs »). Le contrôle positif CNF sur BvLS (priorité 1) et les DRAT (priorité 2) n'ont jamais été faits.
- **tools/win64** : CaDiCaL 3.0.1 et drat-trim patché (fopen en mode binaire) pour Windows, testés sur PHP(8,7), un 3-SAT aléatoire et R(4,4,18), avec des contrôles négatifs. Ils ont été construits pour la route SAT des 79 types de C2. Aucune preuve DRAT C1 n'est déposée.
- **data/** :
  - géométries tordues ;
  - journaux de toutes les exécutions (`*.runlog.out`) ;
  - régions exactes d'ordre 7 et 8 ;
  - table de Borcherds (`borcherds_odd24.json`) et route (C) (`finishC/`) ;
  - rang 17 (`rank17/`) ;
  - types de pivots, `ident_tight.json`, certificats g16 ;
  - `srg243/` avec son vérificateur autonome.
- **code/** : 314 entrées.
  - Témoins (`graphs.py`), modèles enracinés et SAT, hiérarchie (`subgraph_lp`, `euclid_gram`, `flag_sdp`).
  - Scripts x1 à x36 du labo expérimental.
  - Sous-dossiers `r6/`, `v7/`, `b18/`, `omega/`, `motifs/`, `signedU/`, `moments/`.
  - Plusieurs fichiers cités sont **hors dépôt** : `c1_experimental/data/x15_witness.pkl`, `x19_cert_*.json`, `involution_lab_c1/audit_refutations.md`, `NOTE_S5`.

---

## 3. Tables de Brouwer et autres jeux de paramètres

- **Théorème S5 de « structures » (note hors dépôt, citée en notes/114 §5).**
  - Énoncé : critère mod 4 sur det Λ_θ, pour d = r − s impair et E_θ 2-entier. Si tous les premiers de d sont ≡ 1 (mod 4), alors (−1)^{m/2}·P_θ ≡ 1 (mod 4).
  - Portée annoncée : il **« exclut 35 ensembles “?” des tables de Brouwer et la famille NL_e(n) »** (e impair, premiers de n ≡ 1 mod 4). Il redonne srg(289,54,1,12) en 5 lignes. Aucun faux positif sur 1 183 graphes connus. Pour 99, il ne redonne que « k pair ».
  - Mention explicite : « **Audit indépendant recommandé avant toute annonce** ». Rien n'est vérifiable dans ce dépôt.
- **La famille srg(2t² + 4t + 3, 2t + 2, 1, 2)**, n ∈ {9, 99, 243, 6 273, 494 019} :
  - L1 force 6 273 et 494 019 à être tordus ;
  - L16 ne mord qu'à t = 6 (pour BvLS, borne 40 contre 20 requis ; aucun effet pour 6 273 et 494 019) ;
  - F8 : t + 1 = r − s seulement à t = 6 ;
  - famille srg(1 + 2m², 2m, 1, 2) : existe pour m = 2 et 11, éventuellement 7, 56, 497 (Makhnev) ;
  - Makhnev, théorème 2 : exclut aussi un (115,18,1,3) non tordu (littérature).
- **Valeurs propres {3, −4}.** Les seuls paramètres faisables sont (49,24,11,12), (50,21,8,9), (99,14,1,2) et leurs compléments (notes/114).
  - Paley(49) et les 4 réseaux d'AG(2,7) : rank₇(A − 3I) = 16.
  - srg(50,21,8,9) : rang 17, ensemble de commutation retrouvé à la main.
  - Le mécanisme de L22 n'y exclut pas le cas α maximal : il est propre à 99.
- **p-rangs de graphes existants** (notes/110 §6, notes/97) : Clebsch 6/6, Gewirtz 20 (borne 21), srg(9) 4/5, BvLS rank₃(A − 4I) = 67 (borne 111). Pour BvLS, l'incidence des droites a rang₂ = rang₅ = 243 et rang₃ = 231.
- **L22 et L23 validés sur** Petersen, T(7), T(8), T(9), srg(9) et GQ(3,3) = srg(40,12,2,4).
- **Contrôle du tissu** : PG(2,4) avec polarité redonne srg(15,6,1,3).
- **Méthodes d'autres non-existences analysées** sans transposition à 99 : (57,14,1,4) par Wilbrink–Brouwer, (85,14,3,2) par Shpectorov–Zhao, (266,45,0,9) par Akiyama, (19,6,1,2) par Reimbayev, (28,9,0,4) par Ducey et al.
- **Coquilles relevées dans la liste d'ordre 7 de Reimbayev** (arXiv:2608.19410) : au moins deux. L'une est z₁₇₆ = 1/8 au lieu de 1/84 ; il reste un écart B(k + 6) (notes/60).
- **Second srg(243)** : la table de Brouwer ne liste que BvLS (connu de vous).

---

## 4. Incohérences, rétractations, erreurs, surinterprétations

**Documents périmés ou contradictoires.**
1. Le README, le rapport et le §2 de notes/100 sont arrêtés au 25/09. Le tableau §4 du rapport déclare encore F2′, F11, F1/F13 et F3 « tuées », alors que notes/20 les a re-scopées le 27/09 : « TUÉE HORS DIAMÈTRE 2 … OUVERTE pour le SRG », ou « non réfutée ». notes/99 dit pour F₃ : « NON TESTÉ en diamètre 2 ».
2. Dans notes/30, plusieurs remarques sont restées en place après coup :
   - à L8 : « repose sur l'exécution sans cassage … à certifier » (rendu caduc par notes/105) ;
   - à L11 : marqué [P], mais aussi « Non fait … à ne pas utiliser » (rendu caduc par notes/108) ;
   - à L10 : g ≤ 18, alors que notes/108 donne g ≤ 17.
3. **Ordre 7 des automorphismes : incohérence interne.**
   - Le rapport §1 bis, notes/20 et notes/92 disent : « |Aut(Γ)| ∈ {1, 2} … ordres 7 et 11 [exclus] par Behbahani–Lam ».
   - notes/94 §3.4 attribue à Behbahani–Lam : « un automorphisme d'ordre premier est d'ordre 2 ou 3 ».
   - Mais notes/94 §3.5 (Cesarz–Woldar : « si 7 divise |G| alors G = Z₇ ») et notes/60 (arXiv:2308.02978 : « 7 | |Aut| ⟹ Aut ≅ Z₇ ») traitent l'ordre 7 comme possible.
   - notes/160 et 161c écrivent Aut ∈ {1, Z₂, Z₃}.
   - Votre propre découpage contient une branche C7. Il faut trancher sur les textes sources.

**Rétractations et corrections dans le corpus.**
4. Corrections internes :
   - notes/95 : « exactement 1 transport isométrique » corrigé en « 2 » (notes/103 §6).
   - Contre-exemple « coupe » de notes/103 §7 : il viole (T2) (notes/105 §6). « Les triangles NNN forment un 2-cycle » n'est pas établi.
   - notes/102 §9 : « les trois points d'une droite intérieure sont des paires deux à deux disjointes » est faux en torsion maximale (notes/110 §4).
   - notes/116 : « Fano tendu survit, pas une route de plafond » est corrigé : le témoin meurt au niveau des cellules (notes/117).
   - Échantillons « S = 0 » de notes/117–118 : mal étiquetés, aucun n'est à S = 0 au sens de L18, sauf le témoin de Fano (notes/125 §7).
   - JOURNAL, commits b231c36 et d7cd060 : la correction « maille ≥ 5 » était elle-même fausse, et la strate (4,4,4) est vide à S = 0 (notes/125 §6).
   - Erratum de notes/124 §1 (bloc de Jordan).
   - notes/126 : coquille « 21 + t », à lire « 22 + t ».
   - **notes/123** présentait comme nouveaux plusieurs énoncés déjà connus (holonomie, ombres, schéma des droites, et **H + 3P = 213 444, qui est le théorème de Reimbayev**). Elle a été auto-corrigée.
   - notes/100 : la proposition de cohérence à k = 30 a été ramenée à k = 28.
   - Test du « 3-cycle étiqueté » trop strict (rapport §1 bis).
5. Artefacts numériques et bogues :
   - « P ≤ 178 » était une erreur d'échelle (notes/99).
   - Une « infaisabilité » HiGHS à l'ordre 7 était un artefact (notes/91).
   - Bogue d'énumération dans L20 ter, corrigé, résultat inchangé.
   - Exclusion de 132 par connexité : rétractée (notes/140 §3).
   - Bogue de bitsets dans notes/142 : verdicts jetés.
   - Erreur de décalage d'une profondeur qui produisait de **faux morts** dans le moteur cut25 (notes/154).
   - Rang 17 : décompte 1 026 → 1 142 ; « capped » reclassé UNDECIDED.
   - notes/151 §5 : « deux racines d'une même cellule ne sont jamais adjacentes » n'est pas prouvé.
   - notes/148 : « mod-4 faisable ⇒ DC-interdit » est FAUX.
   - notes/149 : « 11 types spectraux » est faux (1 856 spectres).
   - notes/121 : le dérangement cerise/σ a été re-scopé, « route reste OUVERTE ».

**Énoncés anciens à revoir depuis le nouveau 243** (c'est mon inférence, ce n'est pas écrit dans les anciennes notes).
6. Sont désormais faux à t = 10 :
   - la conjecture F2-SRG / F20, « tout PQ(2,t,2) SRG est grid-full » (notes/10, notes/60 §3–5, rapport §1 ter : « au moins aussi dure que l'unicité de BvLS (ouverte) ») ;
   - F23′, l'évitement sur curl₀. Par H3, un SRG avec P < P_max la viole ;
   - « Unicité de BvLS : ouverte » (notes/20) ;
   - la voie « conjecture des hexagones ⇒ non-existence via Makhnev » (notes/94 §3.1) ;
   - le « contre-poids » du rapport : « le seul SRG tordu connu est Gewirtz ».

**Surinterprétations ou certifications manquantes.**
7. Aucun DRAT n'existe, ni le contrôle positif BvLS au niveau CNF, que LAB_INSTRUCTIONS jugeait pourtant critique (« un UNSAT ici invaliderait L7, L8, L10, L11, L14 »).
   - Restent donc non certifiés : L14 pour |C| = 3 et 4, les 24 motifs à 3 étiquettes, L20 ter et le corollaire C1 de notes/100 (k = 10 ⇒ m(e) ∈ {0, 2}, via kbound_exact.py).
   - Énoncés d'échantillon, pas des théorèmes (les notes le disent) : 19/31, 22 %, ~7 %, 40/40 O_x, 40/40 paires de 124.
   - J1a : PSD par Cholesky flottante avec une marge de 10⁻³, « pas de second lecteur ».
   - Autres points à relire : 132 (« à relire par un humain »), 3K2_or14, k = 18 sous NT. g⁺ ≠ 14 repose sur HiGHS seul.
   - R5 est présenté comme « énumérable », mais une seule orbite sur 4 a été faite.
   - Plusieurs résultats viennent d'Astra, de Sol ou de la passation GPT-Pro, et C1 ne les a pas refaits : revêtement de K₇ unique, P ≥ 24 dans la branche Heawood, théorèmes thêta de Sol (« À REVÉRIFIER », notes/139), théorème DC. Seule exception : min Λ₋₄⁻ ≥ 8 d'Astra, revérifié à la main par C1.

---

## 5. Ce qui est le plus publiable (hors srg(243))

1. **Bornes sur le 7-rang : 25 ≤ rank₇(A − 3I) ≤ 43, impair** (L2, L4, L20, L20 bis/ter, **L22**). S'y ajoutent L21 (boule de droite et groupe du tas de sable), L23 (signe ; version Seidel et droites équiangulaires), L19, L17 et les codes des droites de notes/110.
   - C'est le résultat le plus net : il améliore la borne 45 de van Eijl et Brouwer–van Eijl, les preuves sont courtes, les outils classiques (Conway–Sloane), et l'ensemble est validé sur des graphes existants.
   - Réserve : L20 ter est assisté par ordinateur, mais petit et facile à certifier par DRAT.
2. **L16, P ≤ 1151** (Krein cubique sur les droites, orthogonalité des 7 droites par un point propre à 99), avec L15, la torsion comme moment cubique, **L18** (la seconde variable de Reimbayev est S), **Σ_L c₄(G(L)) = S + 3P**, H0–H3, le « mur L16 » à l'ordre 8 et les coquilles de Reimbayev. Tout se fait à la main et a été audité.
3. **Pas de point de Hamming : L8** (squelette de Fano), **L7** (utile aussi à C2), les règles L9–L13, D1/D2, **g(x) ≤ 17**, L14 pour |C| = 2, et la nouvelle preuve de L1 par revêtement (en créditant Makhnev). Combinatoire à la main avec des vérifications finies.
4. **L25** : tissu de grilles ⟺ plan projectif d'ordre 10 avec polarité, et régime pur exclu. Courte note autonome, avec en annexe la coclique de Hoffman.
5. **Géométries tordues non SRG** : famille tri-incidence par ensembles de différences planaires, géométrie à 42 sommets, produits, réfutation de la rigidité locale F2, validation du modèle enraciné sur Gewirtz.
6. **Outils techniques en torsion maximale** (lemme du triangle, repère (P2), P-Ψ, différences de retournement, lemme R) : publiables seulement si un énoncé uniforme en sort.
7. **Théorème S5 de « structures »** (tables de Brouwer) : potentiellement le plus visible, mais hors dépôt et non audité. Il faut le récupérer et le faire auditer.
8. **Matériel C2** (q:7, g⁻ ∈ {18, 20}, route (C), rang 17, R6/J1a) : à publier avec la branche involution, pas sous C1.

**Regroupement suggéré.**
- **Article I, « Arithmétique 7-adique d'un srg(99,14,1,2) hypothétique »** : items 1 et codes des droites, tight sets / cocliques à k = 28 (notes/107), formulation Seidel.
- **Article II, « Torsion, prismes et petits sous-graphes dans srg(n,k,1,2) »** : item 2. Il gagnerait à utiliser le nouveau 243 comme banc d'essai de la famille.
- **Article III, « Points de Hamming et grilles dans le 99-graphe de Conway »** : items 3 et 4, avec item 5 en annexe ou en courte note séparée.
- **Note séparée** sur S5, après audit. La partie C2 va dans l'article de la branche involution.