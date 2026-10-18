# Passe AWS v1 (gabarits 7, 9, 19) : pourquoi les cas bloqués bloquent (LAB, 18/10/2026)

Données : les 980 sorties de la branche `lab/aws-codex-7-9-19` (commit `e441413`) ; détail par Gram dans
`per_gram_features.json`. Le décompte vient des sorties brutes ; l'import de Codex fait foi.

## Résultat brut

| Gabarit | Gram fermés | Gram ouverts | Codes de composantes | Codes essayés | INFEASIBLE | UNKNOWN | jamais atteints |
|---|---:|---:|---:|---:|---:|---:|---:|
| 7  | 5  | 451 | 60 560 | 12 333 | 9 032  | 3 301 | 48 227 |
| 9  | 4  | 12  | 580    | 241    | 190    | 51    | 339    |
| 19 | 59 | 449 | 50 698 | 17 500 | 16 799 | 701   | 33 198 |

- Aucune branche FEASIBLE/OPTIMAL nulle part : aucun témoin trouvé.
- Au total, 73 % des codes n'ont jamais été essayés : le budget de 900 s CPU par Gram s'épuise avant.

## Fermés contre bloqués

- **Nombre de codes.** Médiane par Gram, fermés contre bloqués : t7 45 contre 83 (q90 des bloqués 352) ; t9 20
  contre 38 ; t19 16 contre 66 (q90 294).
- **Couverture.** Les bloqués n'ont essayé, en médiane, que 23 % (t7), 31 % (t9) et 38 % (t19) de leurs codes.
- **Coût d'un code fermé.** Médiane du CPU par code INFEASIBLE, fermés contre bloqués : t7 2,1 s contre 1,9 s ;
  t9 26 s contre 44 s ; t19 14 s contre 23 s.

## Diagnostic

- **t19 : surtout le budget.** Sur les Gram bloqués, 96 % des codes essayés sont INFEASIBLE. Projection pour finir
  avec le même modèle (codes restants au coût observé, UNKNOWN relancés à 240 s) : environ 400 heures-CPU, soit
  environ 1,6 h sur 256 coeurs.
- **t9 : petit.** Environ 11 heures-CPU projetées. Codes le plus souvent UNKNOWN : [0,4,13] (7 sur 8 essais),
  [1,4,7], [0,4,4], [1,4,8], [0,4,8].
- **t7 : une famille de codes résiste.**
  - Les codes [16,3,5], [16,3,7], [17,3,5], [17,3,8], [16,3,4], [17,3,7] sont UNKNOWN dans environ 100 des 169 Gram
    où ils sont essayés.
  - Les autres codes de t7 tombent en environ 2 s.
  - Il faut un argument ou un modèle ciblé sur la famille [16|17, 3, *], pas seulement plus de temps.
  - Projection brute avec le même modèle : environ 1 400 heures-CPU, dominées par des UNKNOWN qui le resteraient
    probablement.
- **t19, codes UNKNOWN les plus fréquents :** [26,3,7] (22/117), [26,6,7] (14/117), [136,3,6] (13/72), [137,3,3],
  [137,3,6], [26,3,8].

Règle de l'utilisateur pour toute v2 : pilotes d'abord sur PC, puis décision.
