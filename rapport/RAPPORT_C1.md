# Branche C1 de srg(99,14,1,2) — rapport de la session du 2026-09-24

*Chercheur F (idées) + chercheur R (attaques), budget non limité. Rien ici ne résout le problème.*
*Tout résultat utilisé est redérivé ici ; l'ancien repo conway-99-research n'a servi que d'index de noms.*

## 1. En bref

1. **Γ est forcément « tordu »** (lemme L1, preuve complète) : si τ = mate en tout sommet (toute paire de droites
   concourantes engendre une grille 3×3), Γ serait un quotient de H(7,3), donc 99 | 3⁷. Donc en au moins un sommet
   x, un couplage τ_a envoie b ailleurs que sur son mate b̄. Même conclusion pour 6273 et 494019.
2. **La torsion n'a pas d'obstruction locale.** J'ai construit des géométries tordues explicites (graphes localement
   (t+1)K₂, λ = 1, μ ∈ {0,2}, non SRG) : t = 2 (20 sommets, graphe des arcs de K₅, **seule** jusqu'à 34 sommets),
   t = 3 (39 et 42 sommets), t = 5 (93), t = 7 (171). Une famille entière vient des plans projectifs (tri-incidence
   (S, −2S, S) sur Z_{q²+q+1}, q = 3, 5, 7). **Toute obstruction pour C1 doit donc être globale** (utiliser μ = 2
   pour *toutes* les paires, c.-à-d. « excès 0 »).
3. Les trois pistes de ChatGPT : **A absorbée** (la cohérence T/Δ est une condition de fermeture de grille, elle
   mesure la même torsion) ; **B tuée comme source d'obstruction** (l'holonomie existe et est canonique, mais aucune
   contrainte spectrale ne la restreint : 0 violation sur 15 765 configurations) ; **C survit sous forme d'un lemme
   démontré** (L4) : le recollement 7-adique du 70-espace est le même en tout sommet et pair — mais ce n'est pas une
   contradiction.
4. Lemmes arithmétiques démontrés : rank₇(A − 3I) est **impair** (L2) ; la forme de recollement 7-adique est
   **non scindée** (L3) ; k(x) = rank₇(A − 3I) − 15 pour tout x (L4).
5. Cas spécial « point de Hamming » (x dans ses 21 grilles) : la version où σ_x est un automorphisme est **UNSAT**
   (modèle φ, 34 s ; contrôle croisé en cours). Le cas général est en calcul.

## 2. Méthode
- Fondations redérivées des axiomes (`notes/00_FONDATIONS.md`).
- Témoins : srg(9,4,1,2), BvLS srg(243,22,1,2) (les deux **non tordus**, donc aveugles à la torsion), Gewirtz
  srg(56,10,0,2) (l'analogue q = 2, **tordu et existant** : avertissement contre les arguments de « torsion pure »),
  Clebsch, GQ(2,2), GQ(2,4) ; puis les géométries tordues construites ici.
- Chaque idée : énoncé précis → attaque la moins chère (calcul exact, contrôle, contre-exemple) → verdict.
- Calculs lourds sous plafond mémoire (`run_capped.ps1`), jamais de SAT « gros » sans budget.

## 3. Verdicts (détails : `notes/20_ATTAQUES_R.md`)

| Idée | Verdict | Raison |
|---|---|---|
| A — algèbre T/Δ | absorbée | cohérence ⟺ fermeture des grilles |
| B — monodromie des 14 transitions | tuée (obstruction) | holonomie ρ_ℓ ∈ S₁₂ canonique, mais aucune contrainte (entrelacement : 0 violation) ; les exemples tordus réalisent des holonomies non triviales |
| C — 70-espace entier + transitions | **lemme L4** | recollement 7-adique k(x) = α − 14, pair, indépendant de x |
| F2 rigidité locale q = 3 | tuée | exemples tordus t = 2, 3 |
| F2' revêtement universel | tuée | H₁ = 0 des géométries tordues |
| F3 ensembles serrés × τ | tuée | les configurations déterminées par τ sont trop creuses (degré ≤ 4) |
| F4 torsion de Fano | tuée (locale) | exemple t = 3 non cohérent par classes |
| F5 genre / oddité | **lemmes L2, L3** | pas d'obstruction |
| F6 Arf | absorbée par F5 | Arf = classe de det Λ₃ mod 8 |
| F11 variété plate cubique | tuée | pas de fermetures en 3-cubes dans les exemples tordus |
| F14 annulation de Krein | tuée | tous les q_ij^k > 0 |
| F15 point de Hamming | **en cours** | cas σ_x-invariant UNSAT |
| F16 rigidité ⇒ symétrie (C1 → C2) | ouverte | dépend de F15 et suites |
| F17 torsion ⇒ plan projectif d'ordre t | ouverte, affaiblie | famille planaire confirmée (q = 3, 5, 7), mais une 2e géométrie t = 3 (42 sommets) n'est pas planaire ; test t = 6 en cours |
| F9, F10, F12, F13, F18 | encodages / non tranchées | voir notes |

## 4. Ce qui est nouveau (à ma connaissance, à vérifier en bibliographie)
- La lecture « Γ = H(7,3) replié jusqu'au rayon 2, obligatoirement tordu » avec une preuve de revêtement complète,
  et l'observation que la torsion **comprime** (moins de sommets à distance 3) : un SRG est la compression totale.
- Les **géométries tordues** comme témoins, en particulier la famille tri-incidence (S, −2S, S) : tordue pour
  q = 3, 5, 7 ; échec pour q pair (2 est alors multiplicateur de l'ensemble de différences).
- L2–L4 (dérivation indépendante ; des énoncés voisins existent peut-être chez Brouwer–van Eijl).

## 5. Piste principale proposée
**« Torsion contre excès nul ».** Γ est tordu (L1) ; toutes les géométries tordues connues ont un excès > 0 ; un SRG
est exactement une géométrie d'excès 0. Programme :
1. Exclure les types locaux « presque non tordus » : point de Hamming (F15, en cours), puis sommets avec 20, 19, …
   grilles, par le modèle φ (compact, rapide sur le cas symétrique).
2. Chercher une identité locale reliant torsion et excès, valable dans toutes les géométries (témoins construits
   ici), qui forcerait torsion = 0 quand l'excès est nul — ce serait la contradiction avec L1.
3. En parallèle, falsifier F17 à t = 6 (tri-circulants, Cayley) : si aucune géométrie tordue n'existe à t = 6,
   c'est même plus fort que Conway ; si une existe, on a enfin un témoin au bon t.
Honnêteté : le point 2 est l'étape difficile ; rien ne garantit qu'une telle identité existe (Gewirtz montre que
l'analogue q = 2 est faux à l'ordre 3).

## 6. Calculs en cours / pour le PC du labo
- Modèle φ du point de Hamming, variantes « générale » et « non isométrique » (Cadical, 2 h).
- Tri-circulants t = 6, N = 34…60 (6 processus).
- Recherche tordue générale t = 4 (n ≥ 51) ; zoo t = 3 (n ≤ 52).
