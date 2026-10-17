# K7 : étude ciblée, résultats partiels

**Pas de preuve complète de K7, ni de contre-exemple.**

Résultats mathématiques démontrés dans `PREUVES.md` :

1. Pour tout c de la coclique de Hoffman, Γ_c ∪ M_c et Γ_c/M_c sont connexes.
   Preuve par le laplacien local du projecteur Q, puis parité.
2. Q[N(c),N(c)] a rang réel 13. Après élimination de treize vecteurs indépendants,
   le Gram résiduel sur les 63 autres blocs est positif de rang 9.
3. Dans le type ternaire (7,15,0), les sept points de couleur zéro satisfont
   n_ef ≤ 3. Sur dix-huit de leurs vingt et un quadruplets, on a même n_ef ≤ 2.
   Un éventuel n_ef=3 est confiné aux trois paires de fibres pures.
4. Les défauts K7 sont exactement les normes 8,6,4 des sommes marquées w_e+w_f.
   C'est une reformulation, pas une exclusion de ces normes.

Le fixture local respecte une partie explicite des contraintes et viole K7,
mais laisse 3 276 arêtes indéterminées : **ce n'est pas un contre-exemple**.

Vérifications finies, sans dépendance externe :

```sh
python3 code/verify.py
```

Le programme vérifie les calculs finis et le fixture, pas une formalisation
informatique des preuves universelles. Aucun calcul massif ni résolution du
modèle complet à 99 sommets ne fait partie de cette livraison.

Source GitHub figée : `fd7a1f1c90410b3514b2ce1974ef64f1370c5305`, branche
`claude/v7-simultaneous`. Aucun fichier distant ni aucune recherche en cours
n'a été modifié.
