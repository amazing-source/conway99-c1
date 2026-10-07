# 164 — Évaluation de la piste « cartes D₇ et holonomie » proposée par ChatGPT (Sol), 07/10

## La proposition
- Autour de chaque sommet x, N(x) = 7K₂, et les 84 non-voisins correspondent bijectivement aux types (i, j; ε, δ),
  c'est-à-dire aux racines de D₇.
- Pour deux sommets adjacents x ∼ y, le changement de carte serait un élément de W(D₇) = 2⁶ ⋊ S₇.
- On étudierait ensuite le cocycle et l'holonomie autour des triangles :
  - une holonomie triviale donnerait une structure globale, donc une symétrie, d'où une contradiction ;
  - une holonomie non triviale donnerait une classe de cohomologie, donc une contrainte.

## Verdict
1. **La carte D₇ est juste et déjà connue.** C'est la bijection des 84 labels (notes 00 et 157 §0 ; Lou–Murin).
2. **L'hypothèse clé est fausse en général.** Le changement de carte forcé entre x ∼ y (la bijection
   N(x) ∖ {y, z} → N(y) ∖ {x, z} par adjacence unique) **ne préserve les paires que si la géométrie est non tordue**.
   Ce n'est donc un élément de W(D) que dans ce cas. Contrôle direct (calcul du 07/10) :

   | graphe | arêtes | paires de mates préservées (sur 10) | changement de carte hors de W(D₁₀) |
   |---|---|---|---|
   | BvLS | 2 673 | 10 partout | 0 |
   | 243 tordu | 2 673 | 1 (720 arêtes), 2 (1 620), 10 (333) | **2 340** |

3. **La branche « holonomie triviale ⇒ contradiction » est un théorème déjà acquis.** C'est Makhnev 1988 (Th. 2), et L1
   dans ce dépôt : une géométrie non tordue est revêtue par H(7,3), donc n = 3^m ≠ 99. Il n'y a besoin ni de C2 ni de C3.
4. **La branche « holonomie non triviale ⇒ contrainte » a déjà été explorée sans contradiction.**
   - Transports τ, système de Kotzig et holonomie de droite (note 00) ;
   - L7 (cocycle, H¹(K(7,2); F₂) = 0) et L13–L18 ;
   - route Hodge (note 60).

   Le 243 tordu montre en outre qu'une holonomie fortement non triviale est compatible avec un SRG de la famille.
   Toute obstruction devra donc utiliser l'arithmétique propre à 99.
5. **Inexactitude de la proposition** : C2 n'est pas encore exclu. La route C en est à 142/156 et des preuves restent à
   archiver.

**Ce qui est récupérable.** Le bon objet de transition est une bijection de 12 points (S₁₂), pas un élément de W(D₇).
L'holonomie autour d'un triangle est la permutation σ_T de la note 163, dont les points fixes sont les prismes
(Σ_T fix σ_T = 2P ≤ 2 302). Une contrainte cohomologique sur la famille (σ_T) devrait être testée sur BvLS et sur le 243
tordu avant d'être crue.
