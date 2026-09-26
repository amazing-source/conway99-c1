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
