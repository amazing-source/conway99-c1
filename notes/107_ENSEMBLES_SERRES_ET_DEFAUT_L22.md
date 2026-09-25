# 107 — Qui peut porter le défaut de L22 ? Ensembles −4-serrés (échange « structures » ↔ C2)

*25/09, après-midi. Résultats d'une discussion entre sessions demandée par l'utilisateur (session « structures », celle
de notes/104 et 106, et session C2). Chaque énoncé a été vérifié à la main par les deux sessions. L'auteur de chaque
énoncé est indiqué. Aucune hypothèse de symétrie, sauf au §5.*

Notation : Λ = Λ₋₄ = Z⁹⁹ ∩ ker(A + 4I), Λ^# son dual, et sur Z₇, Λ = U ⊥ 7V (notes/101), avec rang U = 30 − k.
L22 : U ≠ 0 et U mod 7 non hyperbolique.

## 1. Quadrangle presque parfait (C2)
Pour un 4-cycle induit Q, un sommet extérieur a au plus un voisin dans Q, sauf les 4 apex des arêtes de Q, qui en ont
exactement 2. En effet, deux voisins adjacents dans Q font de ce sommet l'apex de leur arête (λ = 1), et deux voisins
opposés sont impossibles (μ = 2). Comptes exacts : 4 sommets ont 2 voisins dans Q, 40 en ont 1, 51 n'en ont aucun.

## 2. Tout vecteur imposé localement est invisible pour U (C2, précisé ici)
v_x = 63E₋₄e_x = (28 en x, −8 sur N(x), 1 ailleurs) ∈ Λ ∩ 7Λ^#, car 63E₋₄ = −9(A − 3I) + J et E₋₄e_x ∈ Λ^#.
Donc 63E₋₄1_S ∈ 7Λ^# pour tout ensemble S. Exemple : pour une droite T, w_T = (4, −2, 1) = (1/3)Σ_{x∈T} v_x.
Or Λ ∩ 7Λ^# = 7U ⊥ 7V, et Λ/(Λ ∩ 7Λ^#) = U/7U : c'est exactement là que L22 mord, et ces vecteurs y sont nuls.
**Conséquence : aucune configuration locale (droites, boules, genre + vecteurs imposés) ne peut ajouter quoi que ce soit
à L22.** La piste « genre + vecteurs imposés », proposée puis retirée par C2, est donc vide.

## 3. Les ensembles −4-serrés portent le défaut (« structures », compléments de C2)
S est −4-serré si {S, S^c} est équitable de valeur propre −4 : |S| = 11c, degré 2c − 4 dedans et 2c dehors, 2 ≤ c ≤ 7.
- u_S = 9·1_S − c·1 ∈ Λ, et 63E₋₄1_S = 7u_S. La divisibilité par 7 est automatique. Les vecteurs de sommet ne voient
  pas u_S : v_x·1_S = 63 − 7c ou −7c.
- u_S·u_{S′} = 81|S∩S′| − 99cc′ ≡ 4|S∩S′| − cc′ (mod 7).
- (C2) Norme u_S·u_S = 891c − 99c² ≡ c(2 − c) (mod 7), soit 0, 4, 6, 6, 4, 0 pour c = 2…7. Le complément de S est
  serré de paramètre 9 − c, avec u_{S^c} = −u_S.
- Seuls c = 2 (cocliques de Hoffman) et c = 7 (leurs compléments) sont isotropes. Un seul ensemble serré avec
  c ∈ {3,…,6} témoigne donc de U ≠ 0.
- Ce sont les seuls porteurs combinatoires connus du défaut : les grilles sont dans Λ₃, et tout le local est dans 7Λ^# (§2).
- Pour tout k, la matrice de Gram mod 7 des u_S (sur tous les S serrés) a un rang au plus 30 − k.

## 4. Conséquences à k = 28 (« structures », vérifié par C2)
À k = 28, U mod 7 est un plan non dégénéré non hyperbolique, donc **anisotrope**. Une coclique de Hoffman C a une image
de norme 0, donc nulle : u_C·w ≡ 0 (mod 7) pour tout w ∈ Λ. D'où :
- (a) deux cocliques de Hoffman distinctes se coupent en **1, 8 ou 15** sommets ;
- (b) pour toute coclique de Hoffman C et tout ensemble c-serré S : |C ∩ S| ≡ 4c (mod 7) ;
- (c) le défaut de L22 n'est pas porté par des cocliques de Hoffman. Il faut des ensembles serrés avec c ∈ {3,…,6},
  ou des vecteurs sans sens combinatoire ;
- (d) trois ensembles serrés quelconques ont un Gram 3 × 3 de déterminant ≡ 0 (mod 7).

## 5. En C2 (C2)
Un ensemble serré σ-invariant est une réunion d'orbites, plus éventuellement le point fixe x, qu'il contient si et
seulement si c est impair. Aucun ensemble serré ne vérifie σS = S^c. La partition équitable du triangle D extrême
(classes de tailles 1, 6, 8, 12, 48, 24) n'a aucune réunion serrée.

## 6. Statut
- Trois formulations de la cible coïncident : « k ≥ 30 », « les vecteurs 7-primitifs sont isotropes » et le critère de
  notes/102. Toutes équivalent à la non-existence : ce sont des formulations, pas des routes.
- **Question ouverte qui ferait une route :** forcer l'existence d'un ensemble −4-serré. Aucune des deux sessions n'a
  de mécanisme, même avec σ. Une piste qui supposerait son existence serait vide.
