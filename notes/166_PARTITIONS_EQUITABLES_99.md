# 166 — Structure sans symétrie : partitions équitables de srg(99,14,1,2) (11/10)

*Idée directrice : un graphe C1 n'a pas d'automorphisme, mais il peut avoir des partitions équitables. À 243, tous les
graphes connus en ont : c'est de là que viennent toutes les constructions (note 165).*

## 1. Cellules de même taille et de degré interne constant (`code/asym243`, calcul exact)
Les valeurs propres du quotient sont 14 (une fois), 3^a et (−4)^b, avec a + b = m − 1 et trace = m·d.

| v | partitions possibles |
|---|---|
| **99** | **(A)** 11 cellules de 9, d = 4, quotient 3I + J (spectre 14, 3¹⁰) ; **(B)** 3 cellules de 33, d = 2, quotient 2I + 6(J − I) (spectre 14, (−4)²) |
| 243 | 11 formes possibles (triangles, 9, 27, 81 sommets) |

Lignes (cellules de 3) : impossible à 99 (lemme 1 de la note 165).

## 2. Le cas (A) est rigide localement
Parmi les 16 graphes 4-réguliers à 9 sommets (geng), **un seul** est compatible avec λ ≤ 1 et μ ≤ 2 : la grille K3×K3.

Le cas (A) s'énonce donc ainsi : **le graphe de Conway serait la réunion de 11 grilles 3×3 disjointes, chaque sommet
ayant exactement un voisin dans chacune des 10 autres grilles.** Autrement dit, ce serait un revêtement de K₁₁ de degré 9
à fibres grilles. Les 55 bijections entre grilles sont les inconnues. Les voltages peuvent être non abéliens, donc le cas
est compatible avec C1.

Comptages : 66 lignes dans les grilles et 165 = C(11,3) lignes transverses. Chaque sommet apparie les 10 autres grilles
par ses 5 lignes transverses, si bien que les 9 sommets d'une grille donnent 9 couplages parfaits de K₁₀ couvrant ses 45
paires.

## 3. Banc d'essai à 243
Partitions équitables en grilles (quotient K_{9,9,9}), par `gridpart.py` (énumération complète) :

| graphe | partitions en grilles |
|---|---|
| BvLS | 55 |
| jumeau | 10 |
| Γ₃ | 15 |
| Γ₄ | 19 |

## 4. Programme proposé
Un même modèle SAT de « revêtement à fibres grilles », avec voltages dans Aut(K3×K3) :
- **243** : revêtements de K_{9,9,9}. Les solutions connues valident le modèle, et des voltages non abéliens donnent des
  candidats asymétriques.
- **99** : revêtements de K₁₁. Le résultat est soit un graphe de Conway, soit l'exclusion certifiée (DRAT) du sous-cas (A)
  de C1.
