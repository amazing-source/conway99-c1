# 123 — Porte I_x en torsion maximale (P = 0) : relecture, hexagones, comptage local constant

*26/09, nuit. Mathématiques pures (partage du dossier n° 3 : C1 prend le cas général, porte I_x à P = 0 ; Astra prend le
Fano tendu). DÉRIVÉ = preuve écrite ; les seuls calculs sont des contrôles exacts sur BvLS = srg(243,22,1,2), où les
mêmes raisonnements valent avec k = 22. Aucun solveur.*

**Avertissement (auto-correction).** Une première version de cette note présentait comme nouveaux plusieurs énoncés qui
figuraient déjà dans le corpus. Ils sont maintenant crédités à leur source. Le seul apport nouveau est le §2.

## 0. Résumé
| énoncé | statut | source |
|---|---|---|
| prismes sur une droite T = points fixes de l'holonomie σ_T (courbure = prismes) | DÉRIVÉ | **déjà F1 (notes/10) et notes/99 §4 bis** |
| comptes par droite n₀ = 32 − fix, n₂ = 36 − 3fix ; F_T contient 32 − fix droites | DÉRIVÉ | **déjà notes/114 §1 et L16** |
| bijection d'ombre : Q_U ≅ arêtes de K₁₂ − τ_u | DÉRIVÉ | **déjà notes/114 §1** (« les lointains sont en bijection avec les 60 paires non partenaires ») |
| schéma des droites à P = 0 : (Y − 4)(Y + 17) = 0, et sa forme locale en deux droites sécantes | DÉRIVÉ | **déjà notes/99 §4 et notes/109 §4** |
| hexagones induits : H + 3P = 213 444 | DÉRIVÉ, contrôle BvLS | **théorème de Reimbayev** (arXiv:2409.10620), retrouvé indépendamment |
| **à P = 0 et S = 0 : H(x) = 12 936 en tout sommet**, par N(q) = 306 + 2s(q) | DÉRIVÉ, cadre contrôlé sur BvLS | **nouveau** (automatique, sans prise) |

## 1. Hexagones induits (Reimbayev), comptabilité explicite
- Nombre total de 6-cycles : une paire non adjacente est opposée dans 2k² − 7k + 5 cycles, une paire adjacente dans
  C(k − 2, 2). Pour 99, c₆ = (4 158·299 + 693·66)/3 = 429 660.
- Classement selon les cordes, avec deux cordes longues impossibles :
  - L = 37 422 + 3P (une longue) ; S = 158 004 + 6P (une courte) ;
  - SS_o = n₂ = 4 158 − 3P (deux courtes opposées) ; SS_a = 8 316 (deux courtes à sommet commun) ;
  - SL = 8 316 − 6P ; SSL = 3P (hamiltoniens des prismes).
- D'où **H = 213 444 − 3P**, c'est-à-dire H = 209 286 + n₂ (Reimbayev).
- Contrôle : la même comptabilité pour srg(v,k,1,2) donne sur BvLS H = 4 980 690, égal au comptage direct.
- Le plafond visé par notes/100 (P ≥ 1152) équivaut donc à H ≤ 209 988.

## 2. Nouveau : le compte d'hexagones par sommet est constant en torsion maximale
- On pose H(x) = ½ Σ_{q∈Δ_x} N(q).
  - Un **barreau** de q est un couple (u, p) avec x ~ u ~ p ~ q, u étiquette non contenue dans q et p ∈ Δ_x.
  - N(q) compte les couples ordonnés de barreaux ((u,p),(u′,p′)) qui ferment un 6-cycle induit x–u–p–q–p′–u′.
  - Les conditions sont : u′ ∉ {u, ū} ; p′ ≠ p et p′ ≁ p ; u ∉ p′ et u′ ∉ p.
- q = {c, d} a 22 barreaux : 1 par τ-partenaire, 2 par σ-partenaire, 2 par voisin générique.
- Les exclusions se comptent catégorie par catégorie : même étiquette (20), étiquette mate (40), même paire (20), paire
  adjacente (40), u ∈ p′ (18), u′ ∈ p (18). Le seul recouvrement vient de « étiquette mate » et « paire adjacente »,
  quand l'arête opposée à q d'une droite interne par q est une σ-arête.
- **À P = 0 et S = 0 : N(q) = 306 + 2s(q)**, où s(q) est le nombre de droites internes par q dont l'arête opposée à q
  est une σ-arête.
- Chaque σ-arête est sur une seule droite interne, donc Σ_q s(q) = 84, d'où **H(x) = 153·84 + 84 = 12 936 pour tout x**.
- Cohérence : 99·12 936/6 = 213 444, ce qui redonne H + 3P = 213 444 à P = 0.
- Contrôle du cadre (barreaux ⟺ 6-cycles induits par x) : sur BvLS, 122 980 des deux façons.
- **Portée.** Même au troisième ordre, le compte est localement constant en torsion maximale. Cela prolonge le constat
  de notes/109 (premier et second ordre) : aucune contradiction ne sortira de comptages de ce type.

## 3. Conditions P = 0 dans le repère de x (synthèse)
Les deux triangles d'un prisme sont chacun une droite de x, une droite d'étiquette ou une droite interne. P = 0 équivaut
donc à cinq familles de conditions :
- (a) τ_u(v) ≠ v̄ ;
- (b) σ_U sans point fixe, qui découle de (a) ;
- (c) τ_u ∩ σ_U⁻¹τ_ūσ_U = ∅ (« ρ sans point fixe », L13, JOURNAL du 26/09) ;
- (i) en chaque {u,v}, l'appariement des droites internes, transporté par l'ombre β_u, évite τ_u ;
- (ii) aucun prisme entre droites internes.

Comptes par classe U à P = 0 et S = 0 : 12 droites uūQ, 48 uQQ, 48 ūQQ et 32 QQQ, soit les 32 droites de F_{T_U}.

## 4. Portée
- Tout cela est automatique. Le plafond ne peut venir que des **arêtes génériques effectives**, au niveau paire × bloc
  et au-delà.
- Les bornes ordonnées d'Astra (JOURNAL, dossier n° 3) mordent dès que les comptes sont fixés. En torsion maximale
  générique, ils ne le sont pas.
- Piste ouverte : une strate rigide **forcée** à P = 0 (famille tendue, G(L) non connexe, revêtement au sens d'Astra).
- **Leçon de méthode : relire notes/99, 109 et 114 avant d'annoncer une identité sur les droites.**

Scripts (`code/`) : x29_bvls_triangle.py, x29b_hex_bvls.py, x29c_hex_local.py, x29d_sigma_signed.py.
