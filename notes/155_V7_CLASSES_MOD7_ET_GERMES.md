# 155 — Transferts = une classe mod 7 ; V7 reconstruit ; tests de classe sur germes (06/10, reprise C1)

*Reprise de la passation du 06/10 (ligne « fonctions courtes », menée hors dépôt). Les fichiers locaux de cette ligne
(`global_*`) ne sont pas dans le dépôt : tout ce qui suit est recalculé ici, indépendamment. Code : `code/v7/`.*

**Portée.** §1 vaut pour tout srg(99,14,1,2). §2–§6 vivent dans le sous-cas V7 de la passation :
- branche affine 37 **résiduelle** : pas d'entière 26, donc pas d'affine 21 ;
- a = 2, pas de triangle NZZ, m = e = 0 ;
- D = N(x) ∪ N(y) déconnecté, donc D = C6 + cubique 20.

Aucune hypothèse d'automorphisme n'est faite. Les permutations utilisées ne sont que des changements d'étiquettes
de problèmes partiels.

## 1. Théorème : un transfert est un élément de la classe de q

**Notations.**
- Λ est le réseau des fonctions affines entières, (A+4I)q ∈ 2Z·1, de niveau k = Σq/11.
- M = ⟨q_v, 1⟩_Z ⊂ Λ, où q_v = (A−3I)e_v. Pour c entier de somme s, on pose Q_c = Σ c_v q_v.

**Énoncé.**
1. Pour m = Q_c + j·1 ∈ M de niveau k, ‖m‖² = 7(3‖c‖² − cᵀAc) + 2s² + 99j² + 22js ≡ 2k² (mod 7). Le Gram des q_v est
   21I + 2J − 7A.
2. Posons φ(z) = ‖z‖² − 2k(z)² mod 7. On a z·q_v = 2k − 7z_v et z·1 = 11k. Donc φ(z + m) = φ(z) pour tout m ∈ M, et
   φ est une forme quadratique sur Λ/M.
3. Λ/M ≅ Λ₋₄/M₀ ≅ L/7Λ₋₄^#, avec L = π(Λ). C'est un 7-groupe d'ordre 7^{30−k}, avec k de notes/101. φ y est la forme
   U mod 7, non déployée (notes/101–102).
4. Les « transferts » de la passation (q − Q_T + Q_U, 1 − q − Q_S, …) sont **exactement** les éléments de la classe
   [q] = q + M. Leurs éléments de niveau 0 sont **exactement** les fonctions entières de cette classe.

**Valeurs de φ.** Pour les entières : 14 → 0, 16 → 2, **18 → 4**, 20 → 6, 22 → 1, 24 → 3, **26 → 5**. Les affines 21,
37 et 34 (niveau 2) donnent toutes 5.

**Corollaires.**
- Dans [q], au niveau 0, les normes sont paires et ≡ 5 (mod 7) : 12 (impossible, < 14), 26, 40, …
  **Le minimum vaut 26 ou 40, et 40 est toujours atteint** : q − q_x − q_y − q_w, pour un zéro w voisin d'un seul des
  deux négatifs. Un tel w existe toujours, car x a quatre zéros voisins dont au plus deux sont communs avec y.
- « 37 ⇒ 26 par transfert » équivaut à « min₀[q] = 26 ». C'est un énoncé global de minimum de classe. Aucune liste
  finie de formes de transfert n'est garantie de suffire. L'échec des formes à 7 marques en m = e = 0 ne prouve rien.
- Aucun transfert ne produit une entière 18 (φ = 4 ≠ 5).
- q ∉ M.
- **Minima résiduels de [q] par niveau.** Ils viennent de la congruence, de la parité et de Σ ≤ norme ; 21 et 26 sont
  exclus.

  | \|ℓ\| | 0 | 1 | 2 | 3 | 4 |
  |---|---|---|---|---|---|
  | minimum | 40 | 35 | 34 | 37 | 44 |

  Les minima 40, 35 (q − q_x − q_y), 34 (q − q_x) et 37 (q) sont atteints.

## 2. V7 reconstruit indépendamment (`core27.py`)
- **24 noyaux étiquetés** à 27 sommets, comme dans la passation. Tous ont K semi-défini positif de rang 26.
- **12 orbites** sous le groupe de Klein des symétries de la configuration :
  - σ₁ : x↔y, c↔d, α_c↔β_d, α_d↔β_c ;
  - σ₂ : c↔d, α_c↔α_d, β_d↔β_c.

  Représentants : 0, 1, 3, 4, 5, 6, 10, 11, 13, 14, 15, 17.
- **Les six t sont distincts (preuve nouvelle).** Supposons qu'un sommet τ voie trois mates. Alors r = a − q_τ est une
  racine (norme 14). On a q·r = 33 − (54 − 7·4) = 7, donc q − r est une affine 37. Elle a au moins trois coordonnées −1
  (x, y, τ), alors que Σ q'(q'−1) = 37 − 33 = 4. Contradiction.
- **Les 13 a-positifs sont indépendants.** On compte les voisins communs des paires de t : 29 − s ≥ 25 + 4s, donc s = 0.
- **Noyau de K_C.** Il est engendré par κ = (−7 sur x, y, c, d ; −6 sur les mates ; −1 sur les t ; +1 sur les 13). On a
  Σ κ_v q_v = −5·1. La condition de colonne κ·b = −5 est automatique : elle n'apporte aucun filtre.

## 3. Recherche exhaustive des transferts supportés par le noyau (`coset_cvp.py`, `core_full_sweep.py`)
C'est un problème du vecteur le plus proche (CVP), résolu exactement par Fincke–Pohst sur le Gram entier de
{q_v (noyau), 1}. Seules interviennent l'adjacence du noyau et les valeurs de q sur le noyau.

Sur 17 160 couples (noyau, trous), l'équation propre aux t en élimine 3 348. Restent **13 812 couples admissibles** :
- **1 816 sont tués** par un élément de niveau 0 et de norme 26 ;
- **12 sont tués** par un élément de niveau −1 et de norme 21 (une affine 21).

**Forme du transfert trouvé.** z = q − 3a + Q_{T₄} − Q_H, avec a = 1 − Q₈, H l'ensemble des trous et T₄ quatre des t.
Ce transfert passe par la fonction auxiliaire a. Il est hors des formes à 3, 5, 6 et 7 marques.

**11 984 survivants, dont 5 849 sur les représentants d'orbite.** Pour eux, la partie de [q] supportée par le noyau a un
minimum de 40 au niveau 0. **Aucun transfert n'utilise donc seulement les 27 marques du noyau.**

## 4. Filtre de colonnes résiduel (`colfilter.py`)
Une colonne (b, q_u) d'un sommet extérieur u est tuée s'il existe w (élément de classe du noyau) et ε = ±1 tels que
w + εq_u tombe sous les minima.

Sur (noyau 0, trous 14, 15, 16, 18), à la borne 77 : **2 812 colonnes tuées sur 12 120.** Chaque type de sommet
obligatoire (classe de grille × q) garde pourtant des centaines de colonnes. Ce filtre ne suffit donc pas seul.

## 5. Germes croissants : noyau + O_x (`seedcvp.py`, `ox_dfs.py`, `depth*_rate.py`)
**Le germe.** O_x est formé des 10 voisins extérieurs de x : 6 Bx et 4 Zx. Ils forment 5 paires appariées, 4 Bx–Zx et
1 Bx–Bx, sans aucune autre arête. L'adjacence du germe est donc entièrement connue.

**Le test.** Il combine λ/μ, la positivité du Gram des q_v et de K, et les minima de classe du §1. La base du réseau
est obtenue de façon exacte : LLL sur [I | W·G], puis LLL sur le Gram.

**Échantillons sur (noyau 0, trous 14, 15, 16, 18) :**
- **niveau 1** (29 sommets), 1 000 paires : 710 meurent par λ/μ, 103 par une norme 26, 3 par défaut de positivité,
  1 par une affine 21 ; **18 % survivent** ;
- **niveau 2**, 2 000 extensions : 66 % meurent par la demande, 21 % par λ/μ, 7 % par une norme 26, 1 % par défaut de
  positivité. On voit aussi apparaître (3, 23) et (4, 30), impossibles dans tout graphe. **4,4 % survivent** ;
- **niveau 3 : 0,55 % survivent** ;
- **configurations O_x complètes échantillonnées : 40 sur 40 meurent.**

**Taille de l'arbre exhaustif.** Il y a 546 109 paires Bx–Zx admissibles. Le niveau 2 compte de l'ordre de 10⁹ nœuds.
C'est hors de portée en Python. Il faut du C, un branchement par étiquettes (couverture exacte des demandes de x) et
des tests indépendants des trous partagés entre choix de trous.

## 6. Étage colonnes et SAT complet
**Étage colonnes (CP-SAT, `bstage*.py`, `projected.py`).**
- Design pur (BBᵀ = M, sans q) : réalisable (236 s).
- Avec les conséquences linéaires de F (symétrie de BFBᵀ, sommes de lignes) : réalisable (350 s).
- Avec q, trous libres ou fixés : UNKNOWN (600 à 1 200 s).

**SAT complet (`srgsat.py`, `v7sat.py`).** Le modèle impose srg sur toutes les paires, l'équation affine de q aux
99 sommets, m = e = 0 et un ordre lexicographique. Il fait 2,15 M variables et 6,9 M clauses.
- L'encodeur est validé : Paley9, Petersen et BvLS243 masqué sont SAT et vérifiés ; deux témoins UNSAT.
- kissat : UNKNOWN en 1 h à trous fixés, et rien après plus de 2 h à trous libres (run plafonné à 4 h).

## 7. Conséquences
1. 37 ⇒ 26 est un problème de minimum de classe. Dans V7, la classe contient une norme 26 pour 1 828 couples, tués.
   Pour les 11 984 autres, les marques du noyau ne suffisent pas.
2. **La méthode qui avance est le test de classe sur germes croissants**, pas les formes de transfert. C'est une
   propagation exacte des minima du réseau.
   - Elle vaut dans toute branche munie d'un germe de classe non nulle : 18 (φ = 4), 26 et 37 (φ = 5).
   - Les combinaisons de marques seules sont automatiquement cohérentes (normes ∈ 14Z au niveau 0) : le pouvoir vient
     de la fonction germe.
   - Elle est la plus forte dans le résiduel 37, où 21 et 26 sont interdits.
3. **Obligation suivante, précise.** Énumérer exhaustivement O_x, puis O_y, pour chacun des 5 849 couples représentants
   (noyau, trous), en C, avec les tests de classe.
   - UNSAT : V7 est fermé.
   - Survivants : on obtient des germes à 37 sommets, puis à 47 (noyau + O_x + O_y, avec trois relations connues :
     κ et les étoiles de x et de y). Le rang 44 y est atteignable. On passe alors à la reconstruction par colonnes
     forcées : les 52 autres sommets ont un complément de Schur nul.
   - Hors couverture : V8 (D connexe), m + e ≥ 1, les branches 18 et 26.

## 8. Fichiers (`code/v7/`)
- **Noyaux** : `core27.py` → `cores27.json` ; `core_orbits.json`.
- **CVP** : `coset_cvp.py` ; `fp_enum.c` (Fincke–Pohst exact, test des minima côté C) ; `seedcvp.py` (base LLL, test
  de germe).
- **Balayages** : `cvp_sweep.py` / `.log` ; `core_full_sweep.py` → `core_full_sweep.json` (survivants par noyau).
- **Filtres et échantillonnage** : `colfilter.py`, `filter_types.py` ; `ox_dfs.py`, `ox_exhaust.py` (prototype trop
  lent) ; `depth1_rate.py`, `depth2_rate.py`.
- **Étage colonnes** : `bstage.py`, `bstage2.py`, `projected.py`, `reduced_bstage.py`.
- **SAT** : `srgsat.py`, `test_srgsat.py`, `v7sat.py`, `make_cnf*.py`.
