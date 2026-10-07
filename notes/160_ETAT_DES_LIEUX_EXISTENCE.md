# 160 — État des lieux : pourquoi Γ₉₉ serait absurde, et ce que le nouveau 243 vient de casser (07/10)

*Demande de l'utilisateur : est-il « normal » que 9 et 243 existent et pas 99 ? Faire un état des lieux détaillé des
raisons de croire à la non-existence (heuristique, pas une preuve).*

## 0. Fait nouveau : le second srg(243,22,1,2) est tordu, et réfute la conjecture de Reimbayev
**Conjecture de Reimbayev** (arXiv:2409.10620, §4, énoncée pour **toute** la famille λ = 1, μ = 2) : le nombre
d'hexagones induits vaut exactement nk(k − 2)(2k² − 21k + 53)/12. C'est le cas d'égalité n₃ = 0 de son théorème 2,
c'est-à-dire la condition de grille (*) de Makhnev : deux triangles reliés par deux arêtes le sont par trois.

**Comptages directs.** `data/srg243/hexagons.c` est validé contre la force brute et sur la grille 3×3 (6 = borne).
`code/omega/` contient le comptage des paires de triangles.

| | hexagones induits H | borne | paires de triangles à exactement 2 arêtes (n₃) | prismes P (P_max = 8 910) | grilles 3×3 |
|---|---|---|---|---|---|
| BvLS | 4 980 690 | 4 980 690 | 0 | 8 910 | 1 485 |
| nouveau | **5 000 130** | 4 980 690 | **19 440** | 2 430 | 405 |

Contrôles de cohérence : H − borne = n₃ = 3(P_max − P) = 19 440, et P = 6 × (nombre de grilles) dans les deux graphes.

**Conséquences.**
- La conjecture de Reimbayev est **fausse**. Le nouveau graphe est le premier membre **tordu** connu de la famille : c'est
  le « membre tordu » de structures/NOTE_S25 §6.
- Sa torsion est forte : P/P_max = 27 %. À 99, la seule contrainte connue est P ≤ 1 151 < 1 386 = P_max (L16), soit
  ≤ 83 %. Le nouveau graphe est donc proportionnellement **plus** tordu que ce que 99 exige.
- **Toute stratégie qui exclurait 99 par une loi valable pour toute la famille (grille (*) partout, plafond uniforme de
  torsion) est morte**, puisqu'elle exclurait aussi ce graphe, qui existe. Une preuve de non-existence doit utiliser une
  propriété propre à 99 (le côté 7-adique, 7 | t ; NOTE_S25 §1) ou passer par un calcul fini (route Ω, route C de C2).

## 1. « 9 et 243 existent, pas 99 » : c'est de l'arithmétique, pas de la taille
- **La famille.** λ = 1 et μ = 2 imposent v = 1 + k²/2 et t² = 4k − 7, avec t | 63. D'où
  v ∈ {9, 99, 243, 6 273, 494 019} (plus K₃ pour t = 1).
- **v est la taille de la boule de Hamming B₂(0) dans F₃^m**, avec k = 2m : 1 + 2m + 2m(m − 1) = 2m² + 1.
- **Les membres « algébriques » sont des quotients F₃^m / C par un code parfait C.** On obtient H(2,3) pour m = 2 et le
  Golay ternaire pour m = 11. Ce mécanisme exige que v divise 3^m. Or v = 99 = 9 · 11 ne divise pas 3⁷, et 6 273 et
  494 019 ne sont pas des puissances de 3. Par la classification des codes parfaits (Tietäväinen–van Lint), m = 2 et
  m = 11 sont les seuls cas.
- **Même schéma ailleurs.**
  - Plans projectifs : ils existent pour les puissances de premiers. L'ordre 6 est exclu par Bruck–Ryser et l'ordre 10
    par un calcul fini (Lam, 1989).
  - Graphes de Moore : 5, 10 et 50 sommets existent ; 3 250 reste ouvert, avec un groupe forcément petit.

## 2. Ce qui tient toujours contre l'existence
1. **Aucun mécanisme connu à 99.**
   - Pas de code parfait.
   - Pas de groupe : Aut ∈ {1, Z₂, Z₃} (Wilbrink, Behbahani–Lam, Crnković–Maksimović, Cesarz–Woldar).
   - Pas de graphe-mère à déformer. Le nouveau 243 est une déformation de BvLS : il garde la boule du triangle et
     |Aut| = 4 320.
2. **Tordu partout.**
   - Makhnev 1988 : (*) est faux à 99.
   - L8 : aucun point de Hamming, holonomie tordue en tout sommet.
   - L16 : P ≤ 1 151.
3. **Heuristique aléatoire** (espaces linéaires de droites de taille 3, μ ~ Poisson(2) sur chaque paire non colinéaire).
   L'espérance non étiquetée est ~10⁻¹⁸⁴⁰ à 99. La même heuristique donne ~10⁻¹²⁴²⁹ à 243, où deux graphes existent :
   elle exclut seulement les solutions « génériques », pas celles produites par une structure.
4. **Calculs.** Aucune quasi-solution publiée. Dans nos germes C1, la survie tombe à 18 %, puis 4,4 %, puis 0,55 % ;
   40 configurations complètes échantillonnées sur 40 meurent. Les SAT complets restent UNKNOWN.

## 3. Ce que le nouveau 243 change dans le jugement
- **Avant :** les membres connus étaient tous non tordus. « La famille impose les grilles » était une loi plausible, et
  elle tuait 99 via Makhnev.
- **Maintenant :** une torsion forte se referme globalement en SRG, au moins près d'un objet algébrique.
- **Ce qui reste :** l'absence de tout mécanisme à 99, qui est l'argument 1.
- **Estimation subjective :** non-existence ~75 % (contre 85–90 % avant ce constat).

## 4. Conséquences pour le programme
- **Abandonner** toute piste « plafond de torsion uniforme dans la famille ». Toute règle candidate doit être testée
  sur le nouveau 243 : s'il la viole, elle est fausse.
- **Pistes valides :**
  - les arguments propres à 7 | t, comme l'arithmétique 7-adique ;
  - la route Ω, avec son étage colonnes à certifier ;
  - la route C de C2.
- **Le nouveau 243 sert désormais de banc d'essai** du régime tordu. C'est le premier contrôle positif possible pour
  les filtres de C1 qui portent sur la torsion.
