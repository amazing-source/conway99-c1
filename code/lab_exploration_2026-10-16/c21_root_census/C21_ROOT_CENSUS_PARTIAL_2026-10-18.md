# Branches c_min = 2 et c_min = 1 : recensement PARTIEL des gabarits de racine (LAB, 18/10/2026)

**Statut : recensement partiel, VÉRIFIÉ sur les tâches terminées. Le calcul a été arrêté volontairement.**

- **Cadre.** Même racine et mêmes outils que `../c3_root_cover/C3_ROOT_COVER_2026-10-18.md`, en mode « exact » : au
  moins une droite de la racine à c = c_min. Les configurations dont toutes les droites de la racine ont c > c_min
  relèvent du balayage suivant.
- **Calcul.**
  - 1 372 tâches lancées : 664 pour c_min = 2, 708 pour c_min = 1 (racines sans grille découpées en
    type × option de la droite 1).
  - Sur AWS, 2 × 128 coeurs. Arrêt manuel au bout d'environ 1 h (environ 2 $) : 538 tâches finies, 256 très longues en
    cours, 578 jamais démarrées.

## c_min = 2, avec au moins une droite à c = 2

| Grilles | Graphes faits | Gabarits | Infaisables au Gram | Ouverts | UNKNOWN |
|---|---:|---:|---:|---:|---:|
| 0 | 4/120 tâches | 0 | 0 | 0 | 0 |
| 1 à 3 | 0/8 | – | – | – | – |
| 4 | 6/10 | 852 996 | 815 584 | 37 344 | 68 |
| 5 | 20/20 | 732 827 | 679 404 | 53 372 | 51 |
| 6 | 39/39 | 170 144 | 149 568 | 20 565 | 11 |
| 7 | 60/60 | 32 212 | 25 830 | 6 382 | 0 |
| 8 | 84/84 | 4 892 | 3 445 | 1 447 | 0 |
| 9 | 102/102 | 609 | 314 | 295 | 0 |
| 10 | 97/97 | 59 | 17 | 42 | 0 |
| 11 | 76/76 | 6 | 1 | 5 | 0 |
| 12 | 48/48 | 0 | 0 | 0 | 0 |
| **Mesuré** | 536/664 | **1 793 745** | | **119 452** | 130 |

## c_min = 1

Pratiquement pas mesuré : 2 tâches finies sur 708.

## Lecture

- Le test de Gram coupe environ 98 % des gabarits pour c_min = 3, mais seulement environ 93 % pour c_min = 2.
  Surtout, le nombre de gabarits explose : plus d'un million rien que pour 4 et 5 grilles.
- Pour c_min = 2, il reste au moins environ 1,2 × 10⁵ gabarits ouverts, alors que les plus petites valeurs de k
  (0 à 3) manquent encore.
- c_min = 1 sera plus large encore.
- À ce niveau de filtre, la méthode des gabarits de racine ne passe donc pas à l'échelle pour c ≤ 2. Il faut des
  filtres plus forts au niveau du gabarit avant le modèle global.
- Comparaison : c_min = 3 laisse 10 052 ouverts, et c_min = 4 (Codex) en laissait environ 100.
