# 117 — (P2) linéarisé par types en torsion maximale générique : la majorité des configurations locales meurt

*26/09. Labo c1_experimental (X19 à X20). Méthode reprise de C2, qui a tué H-β ainsi (labo C2, note 32). DÉRIVÉ =
preuve écrite ; OBSERVÉ = calcul. Les PL servent à tester la faisabilité de systèmes dérivés à la main, en quelques
secondes chacun. Chaque infaisabilité est certifiée par un vecteur de Farkas rationnel vérifié en arithmétique
exacte. Un certificat a été revérifié indépendamment par « structures ».*

## 0. Résumé
| résultat | statut |
|---|---|
| modèle par types : relaxation exacte de toute configuration réelle en un sommet | DÉRIVÉ |
| 19 configurations aléatoires localement admissibles sur 31, en torsion maximale, sont infaisables avec (P2) | OBSERVÉ, chaque cas certifié |
| un certificat revérifié indépendamment (types, 735 seconds membres, valeur exacte 5,9916) | recalcul « structures » |
| environ 40 % survivent ; le lemme du triangle en tue 1 sur 11 ; le raffinement V/P, 0 sur 3 | OBSERVÉ |
| niveau paires (466 000 colonnes) : hors de la règle des 5 minutes sur le portable | non fait |
| (P2) ⟺ repère ajusté Σ_z ξ_zξ_zᵀ = 196·P_{E₋₂} dans l'espace de Johnson de dimension 14 | DÉRIVÉ, contrôle exact |
| cellules antipodales : le témoin de Fano tendu meurt (Farkas exact, revérifié) ; environ 7 % des configurations passent blocs et cellules | certifié pour le témoin ; échantillon en flottants pour le reste |

## 1. Le modèle (en un sommet x, données locales (τ, σ) fixées)
- **Type d'une paire z** : le multigraphe de classes de son graphe de voisins génériques G_z, c'est-à-dire
  8 arêtes sur les 10 étiquettes hors de ses classes, sans arête de mates, de degrés 2 − h_z (fentes). On ne garde
  que les multigraphes réalisables sur les étiquettes. Les 4 voisins spéciaux (2 τ, 2 σ) sont fixés par (τ, σ).
- **Variables** : x[z,t] ≥ 0, avec Σ_t x[z,t] = 1.
- **Lignes**, toutes des conséquences exactes de srg(99,14,1,2) :
  - équilibre des blocs : N(R,R′) = N(R′,R) ;
  - équilibre étiquette : Σ_{y∋u} cnt(y,R) = 8 (μ(w,u) = 2 pour chaque w ∈ R) ;
  - les 231 identités (P2) de notes/116 (forme générale, diagonale 16 − 2e(R)). Elles deviennent linéaires, car
    cnt(z,R)·cnt(z,R′) ne dépend que du type de z.
- Toute configuration réelle donne un point entier de ce système : **infaisable ⟹ ces données (τ, σ) sont
  impossibles** en tout sommet de tout srg(99,14,1,2).

## 2. Résultats (OBSERVÉ, échantillon)
- Contrôles :
  - le témoin de Fano tendu (notes/116) est faisable, avec ou sans (P2) ;
  - sans (P2), toutes les configurations testées sont faisables.
- **Avec (P2) : 19 infaisables sur 31** configurations aléatoires localement admissibles (graines 1 et 11 ; τ sans
  boucle, σ_c(v) ∉ {v, v̄}).
  - Chaque cas a son certificat de Farkas : b·y − Σ_colonnes max(0, col·y) > 0 en rationnels exacts, avec des
    valeurs de 6 à 94.
- **Vérification indépendante** (« structures », `verify_c1_x19.py`) du certificat de la graine 1, configuration 1 :
  - types de toutes les paires retrouvés à l'identique (4 968 colonnes, par énumération des vrais graphes
    d'étiquettes) ;
  - les 735 seconds membres recalculés sans écart ;
  - valeur 5,9916 identique en rationnel exact.
- Survivants :
  - le lemme du triangle en tue 1 sur 11 ;
  - le raffinement V/P de la diagonale (sommets en V et arêtes parallèles comptés séparément dans chaque bloc,
    identités exactes) ne tue aucun des 3 premiers.

## 2 bis. Lecture de (P2) : un repère ajusté dans un espace de dimension 14 (DÉRIVÉ)
- On part de A_Δ² + A_Δ − 12I = 2J − ∂ᵀ∂ (notes/116) et on complète le carré : **(2A_Δ + I)² = 49I + 8J − 4∂ᵀ∂**.
- Pour un bloc R, soit w_R = (2A_Δ + I)1_R, c'est-à-dire w_R(z) = 2·cnt(z,R) + [z ∈ R], un vecteur entier. Alors :
  - **Gram(w_R) = 128J + 132I − 32A_J**, où A_J relie les blocs qui partagent une classe (graphe de Johnson J(7,2)).
    Sa diagonale vaut 260, et ses entrées 96 (classe commune) ou 128 (blocs disjoints). Ses valeurs propres sont
    **50², 6², 14²**, sur les espaces de Johnson E₁₀ (dim 1), E₃ (dim 6) et E₋₂ (dim 14) ;
  - pour toute paire z, Σ_R w_R(z) = 25 ;
  - les sommes par classe de w(z) = (w_R(z))_R valent 8 hors des classes de z et 5 sur elles (fentes). Les parties
    E₁₀ ⊕ E₃ de w(z) ne dépendent donc que du bloc de z, et les identités correspondantes sont automatiques.
- **Tout le contenu de (P2) est dans E₋₂.** Soit ξ_z la projection de w(z) sur E₋₂. Alors (P2) équivaut à :
  **Σ_z ξ_z ξ_zᵀ = 196·P_{E₋₂}**. Les 84 vecteurs ξ_z forment un repère ajusté (« tight frame ») de constante 196
  dans R¹⁴, de trace 2744 (moyenne ‖ξ_z‖² = 98/3). S'y ajoutent des conditions croisées linéaires (moments
  d'ordre 1 par bloc).
- Valable en tout sommet de tout srg(99,14,1,2), quelle que soit la torsion. Contrôle exact sur le témoin de Fano :
  Gram, repère et sommes 25 vérifiés sans écart.
- **Forme concrète : l'identité du 4-cycle alterné.** E₋₂ est engendré par les 4-cycles alternés de classes
  f = (+1, −1, +1, −1) sur ab, bc, cd, da. On pose δ(z) = cnt(z,ab) − cnt(z,bc) + cnt(z,cd) − cnt(z,da). Alors :
  **Σ_z δ(z)² + 2N(ab,cd) + 2N(bc,da) − [e-internes] = 192 + 2[N(ab,bc) + N(bc,cd) + N(cd,da) + N(da,ab)]**,
  où [e-internes] = N(ab,ab) + N(bc,bc) + N(cd,cd) + N(da,da), nul sans σ-arête interne.
  - À droite, N(ab,bc) etc. sont des arêtes σ par la classe commune, connues depuis (τ, σ).
  - À gauche, N(ab,cd) et N(bc,da) comptent des arêtes génériques.
  - On en a 105, une par 4-cycle de classes, plus les identités croisées. Toutes vérifiées sur le témoin de Fano.
- **Lecture des morts.** Les parties spéciales des ξ_z sont fixées par (τ, σ) ; leurs parties génériques parcourent
  des types en nombre fini. Une configuration meurt quand aucun choix de types ne rend le repère isotrope. Une
  preuve à la main passerait par une direction f ∈ E₋₂ où Σ_z ⟨ξ_z, f⟩² = 196‖f‖² est impossible. Le lien avec L19 :
  (2A_Δ + I)/7 est la réflexion R de notes/93 sur ker ∂, et (P2) dit que R est une isométrie sur les 14 dimensions
  des fonctions constantes par blocs de ker ∂.

## 2 ter. Cellules antipodales (raffinement proposé par « structures », issu de C2)
- **Cellules.** Dans le bloc {c < d} : A = {c_s d_t : s = t}, B = {s ≠ t}.
- **Identité** (même dérivation que (P2), pour toute partition) :
  Σ_z c_z(C)·c_z(C′) = 12|C∩C′| + 2|C||C′| − e(C,C′) − L(C,C′), avec L(C,C′) = Σ_{w∈C, w′∈C′} |w ∩ w′|.
  - La partie nouvelle est portée par les 21 vecteurs signés ε_R (+1 sur A, −1 sur B), qui sont dans ker ∂. Les
    u_R = (2A_Δ + I)ε_R ont un Gram égal à 196·I et sont orthogonaux aux w_R′.
- **Relaxation désagrégée** (`c1_experimental/scripts/x19i_cells.py`) : chaque type de classes x[z,t] est
  découpé en variables s[z,t,R,(k_A,k_B)], avec Σ_k s = x.
  - Lignes imposées :
    - cellule signée de R contre le bloc R′ (tous R, R′) ;
    - cellules d'un même bloc ;
    - e(C,C′) = e(C′,C) ;
    - Σ_{y∋u} c_y(C) = 4.
  - Les produits de cellules de deux blocs différents ne sont pas imposés (il faudrait des découpages conjoints),
    ce qui ne fait qu'affaiblir la relaxation.
- **Résultats.**
  - **Le témoin de Fano tendu de notes/116 est infaisable.** Farkas exact, 75 381 256 à l'échelle 10⁶, sur
    29 652 lignes et 66 948 colonnes.
    - **Vérification indépendante par « structures »** (`verify_c1_cells.py`, code séparé, entiers seuls) :
      spéciaux, types (4 872 colonnes x), découpages (62 076 colonnes s, tous présents), puis les 29 652 lignes
      reconstruites depuis leurs noms, avec 0 écart sur A et b. La valeur de Farkas est identique.
  - **Survivants du niveau blocs** (points intérieurs, en flottants ; certificats exacts non encore extraits) :
    - 10 sur 11 infaisables (graine 11) ;
    - 10 sur 12 infaisables (graine 21, échantillon neuf).
    - **Au total, 3 configurations sur 45 passent blocs et cellules**, soit environ 7 %.
  - **Profil des survivants** (petits effectifs) : les plus « équirépartis ». τ est surtout en 6-cycles, et les
    comptes e des familles triangle sont les plus uniformes. Les filtres tuent les irrégularités. Le cœur restant
    n'est pas une classe spéciale.

## 3. Portée (à lire telle quelle)
- **Chaque certificat réfute une configuration (τ, σ).** « 19 sur 31 » est un énoncé d'échantillon, pas un théorème.
- Il n'existe pas de certificat universel à ce niveau, puisque le témoin de Fano et d'autres survivants sont
  faisables. Un certificat entièrement symétrique serait un comptage moyenné, et le profil de torsion maximale les
  satisfait tous (notes/100).
- **Ce que cela établit** : la majorité des données locales génériques en torsion maximale sont impossibles. Un Γ de
  C1 doit donc avoir, en chacun de ses 99 sommets, des données locales du type « survivant ». C'est la première
  contrainte exacte du corpus qui mord massivement sur le cœur. Elle vient de la méthode de C2 appliquée aux
  identités de notes/116.
- **Suite** : caractériser les survivants (statistiques en cours), puis chercher la propriété qui les distingue et
  la démontrer à la main. Le niveau paires serait l'étape de calcul suivante, mais il sort de la règle des 5 minutes.

Scripts (copies dans `code/`) : x19_block_lp_generic.py, x19b_certify.py, x19c_survey.py, x19d_vp_refined.py,
x19f_export_cert.py ; données `c1_experimental/data/x19_cert_s1_c1.json`.
