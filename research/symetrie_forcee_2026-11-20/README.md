# Symétrie forcée par un bord positif à jumeaux : pourquoi l'argument tombe

20/11/2026, branche `claude/perelman-invention-conway`. Statuts : **[P]** démontré ici · **[E]** calcul reproductible
(`python3 twin_check.py`, environ 1 minute, aucune écriture dans le dépôt).

Notations de R2 §6 : w_v = √7·E₋e_v, Gram 27I − 9A + J (28 sur la diagonale, −8 sur les arêtes, 1 sinon). Un bord
positif est un ensemble S de 44 sommets dont les w_v forment une base de E₋ ≅ ℝ⁴⁴.

## L'argument tenté

Soit (u, u′) une non-arête, X = N(u) \ N(u′), Y = N(u′) \ N(u) (12 sommets chacun), et Ag les 73 sommets qui voient
u et u′ de la même façon.

1. **[P]** Les w_v, pour v ∈ Ag ∪ {u, u′}, engendrent E₋. Sinon, un vecteur propre −4 serait porté par X ∪ Y, donc
   vecteur propre −4 de A[X ∪ Y]. Or ce graphe est de degré maximal ≤ 3 : un sommet de X a au plus 1 voisin dans
   N(u) (λ = 1) et au plus 2 dans N(u′) (μ = 2).
2. Il existe donc un bord positif S ⊂ Ag ∪ {u, u′} contenant u et u′. Dans Γ[S], u et u′ sont jumeaux, et
   σ = (u u′) ∈ Aut(Γ[S]).
3. Si Γ[S] déterminait Γ, σ s'étendrait en un automorphisme fixant 42 sommets, ce que Wilbrink interdit.

## Pourquoi il tombe

**(a) Deux objets confondus [P].** V15 (NOTE_COEXISTENCE §75) donne l'unicité pour la pièce **étiquetée** (B, D),
où D est l'adjacence de S vers les 55 autres sommets. Or le reste s'en déduit par E_xy = g_xᵀ G_SS⁻¹ g_y, une formule
équivariante. Toute symétrie de (B, D) est donc un automorphisme de Γ qui stabilise S :
Aut(B, D) = Aut(Γ)_S. Pour un bord positif étiqueté, « trouver une symétrie forcée de la pièce » revient exactement à
« trouver un automorphisme de Γ ». La ligne « bord positif de 44 sommets : manque une symétrie forcée » de R2 §6
demande donc la conclusion elle-même. Aucun choix de bord ne peut la remplir.

**(b) La pièce nue est symétrique, mais σ ne s'étend jamais [P].** L'unique isométrie de E₋ qui fixe les w de
S′ = S \ {u, u′} et échange w_u et w_u′ est la réflexion R_z, avec z = w_u − w_u′ (|z|² = 54). Pour x ∈ X,
⟨w_x, z⟩ = −8 − 1 = −9, donc R_z(w_x) = w_x + z/3 et

    ⟨w_x, R_z w_x⟩ = 28 − 2·81/54 = 25 ∉ {28, −8, 1}.

R_z(w_x) n'est donc le vecteur d'aucun sommet, dans aucun graphe contenant la pièce. Les complétions de Γ[S] vont par
paires {Γ, σΓ}, et σΓ ne se ramène jamais à Γ par un réétiquetage des sommets extérieurs. Ce résultat n'utilise ni C1
ni Wilbrink. « Au plus une complétion » équivaut à « aucune » : le lemme manquant était le théorème lui-même. Le
principe L07-032 de R2 §6 (au moins |Aut(H)| complétions) donnait déjà 2 sous C1.

**(c) La même formule pour toute la famille.** Avec le Gram normalisé (diagonale 1, cosinus ω₁ = s/k et ω₂), la
valeur est 1 − (ω₁ − ω₂)²/(1 − ω₂) :

| paramètres | valeur | valeurs permises | l'échange peut-il s'étendre ? |
|---|---|---|---|
| srg(9, 4, 1, 2) | 1/4 | 1, −1/2, 1/4 | oui |
| srg(99, 14, 1, 2) | 25/28 | 1, −2/7, 1/28 | non |
| srg(243, 22, 1, 2) | 413/440 | 1, −5/22, 1/55 | non |

## Calcul [E]

`twin_check.py` traite la grille 3×3 (18 non-arêtes) et les huit srg(243) du dépôt (20 non-arêtes chacun).

- **Grille 3×3.** L'engendrement est vérifié, la valeur vaut 1/4, et R_z préserve toute la configuration dans
  18 cas sur 18 : l'échange s'étend.
- **Huit srg(243).** L'engendrement est vérifié dans 160 cas sur 160 et la valeur observée est toujours 413/440.
  Aucun R_z(w_x) n'est un sommet, aucune extension n'existe, et aucun couple (x, y) ∈ X × Y n'a le même motif sur S′.
  La distance minimale entre motifs va de 7 à 9.

L'argument, recopié mot pour mot, « prouverait » donc que la pièce jumelle détermine le graphe, dans des graphes qui
existent et où c'est faux. Le calibrage 243 l'aurait arrêté avant la troisième étape.

## Remarque sur R2-12

La raison structurelle donnée en R2-12 vaut pour les pièces symétriques connues : N[x], les grilles et les prismes
jumeaux sont des supports de relations entre les w_v, donc jamais des bords positifs. Elle ne vaut pas en général. La
pièce jumelle est un bord positif symétrique, présent dans tout Conway (point 1). La raison générale est (a) : sur un
bord positif étiqueté, une symétrie de la pièce est un automorphisme de Γ. Le slogan « forced symmetry dies at the
first gluing » est (a). Pour les jumeaux, on voit cette mort en (b), au produit scalaire 25.

Seule la ligne du cadre reste ouverte dans le tableau de R2 §6 : sa symétrie (645 120) est forcée localement, mais il
faudrait borner ses complétions sous 63 866 880. R2 note qu'aucune méthode n'est en vue pour cela.
