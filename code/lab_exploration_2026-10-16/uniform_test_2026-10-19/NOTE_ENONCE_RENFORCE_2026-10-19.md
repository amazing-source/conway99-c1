# Vers un énoncé plus contraignant (19/10/2026, après-midi)

Demande de l'utilisateur : rendre l'énoncé de départ (le test de Gram entier) beaucoup plus contraignant, pour qu'il
puisse balayer c = 1, 2 et 3, avec des outils plus forts, sans rien supposer qui ne soit prouvé.

Tout ce qui suit est déduit de λ = 1, μ = 2. Pour chaque point, on dit s'il est **nouveau** ou **déjà dans l'archive**,
avec la référence.

## 1. Littérature (agent du 19/10, fiche `BIBLIO_99_2026-10-19.md`)

Trois apports.
- **Makhnev 1988** (prouvé) : P = 1386 est exclu.
- **Reimbayev** (non relu) : 62 types de sous-graphes induits à 6 sommets avec 1 paramètre libre, et 208 types à
  7 sommets avec 2 paramètres. **Confirmé ici à l'ordre 6** par un moteur indépendant (section 3).
- **Liao–Wang–Yu–Cai (octobre 2026)** : positivité de Gegenbauer projetée sur un sous-graphe de référence, combinée
  aux comptes. Codex l'avait signalée le 16/10 sans la lancer. **Je l'ai réimplémentée ici sans leur code** (section 2).

## 2. Tests globaux de positivité (nouveaux ; tous négatifs)

**Principe.** On projette les vecteurs sommets sur l'orthogonal d'une copie de H, dans E₋₄ (dimension 44) et dans E₃
(dimension 54). Pour chaque degré k, la matrice indexée par les motifs d'adjacence à H doit être semi-définie
positive. Ses entrées sont des comptes de sous-graphes induits.

| Test | Script | Résultat |
|---|---|---|
| H = sommet, arête, non-arête, triangle (comptes fixés par copie, à la main) | `gegen_ref_test.py` | Tout passe jusqu'au degré 60. Les zéros exacts aux degrés 1 et 2 valident les comptes. |
| Les 4 graphes à 3 sommets (comptes d'ordre 5, tous fixés) | `gegen_ref_sdp.py … 3` | Rien |
| Les 9 graphes à 4 sommets, dans les deux espaces, k ≤ 40 (comptes d'ordre 6, affines en P) | `gegen_ref_sdp.py … 4` | Aucune contrainte sur P ∈ [0, 1386] (`gegen_m4_K40.jsonl`) |
| Sommets + 231 droites, noyaux de Gegenbauer et noyaux produits G_k⁽⁴⁴⁾·G_l⁽⁵⁴⁾, k, l ≤ 20 | `gegen_lines.py` | P ≤ 1151 seulement (degré 3 dans E₋₄), comme l'agent |

**Conclusion.** À ces tailles, la positivité est plus faible que le programme linéaire de recensement d'ordre 9 de
l'archive (P ≤ 852). C'est un négatif à ne pas refaire. Cela concorde avec la littérature : Liao et al. n'excluent rien
à 4 points, et de Laat et al. n'obtiennent rien au niveau 3 de Lasserre pour v ≤ 200.

**Autre négatif.** Le Delsarte des 84 vecteurs étiquettes ψ_w (S²⁹, voir la section 5) est trivial : 84 points sont
trop peu en dimension 30.

## 3. Moteur de comptage indépendant (nouveau code, résultat connu)

`subgraph_counts.py` part des équations d'extension (Wilbrink–Brouwer). Seules les deux bornes de voisins communs
définissent les types admissibles.

| Ordre | Types | Paramètres libres |
|---|---:|---:|
| 2 à 5 | 2, 4, 9, 21 | 0 |
| 6 | 62 | 1 |

- Le paramètre libre est N(K2 + 4K1) = 9P + 275 371 866, où P est le nombre de prismes. La positivité redonne
  0 ≤ P ≤ 1386.
- Ces chiffres sont identiques à ceux de census2 (archive, 08/10) et à ceux de Reimbayev : trois sources concordent.

## 4. Ce que l'archive avait déjà (non refait ; à réutiliser)

- **Intégralité du recensement.** Aucune congruence, même à l'ordre 10 (`census_cong.py`, note C1 §… « Integrality
  of the census »). L'idée d'un programme en nombres entiers sur le recensement est donc morte.
- **Sous-espace lointain d'une droite.** dim(E₋₄ ∩ R^{R(T)}) = 7 + c(T) et dim(E₃ ∩ R^{R(T)}) = 18 (EXPLORATION.md,
  ligne 479). Redérivé ici avec le spectre exact de R_T : {8, 3¹⁸, (−4)^{7+c}, −1 − θ_i}, où les θ_i sont les valeurs
  propres de G_T hors de 3.
  - Lecture utile : la dimension qui fait survivre les gabarits c ≤ 2 à la racine (jusqu'à 14) est grande vue de la
    racine, mais petite vue de la droite (8 ou 9). Les rangs « T_S » de l'archive (rang F ≤ 7 + c(l)) exploitent déjà
    ce fait.
- **p-rangs.** rang₂(A) = 54 et rang₃(A + I) = 55 sont forcés (Brouwer–van Eijl : seul p = 7 est libre). La fenêtre de
  rang 7 et ses verrous sont dans la note C1 §17.
- **Une droite dans six grilles** (note C1 §17.46) : c'est exactement un design à 60 « noms » dans (Z₃ × Z₂)⁶, avec
  20 triangles et 6 couplages. L'objet était fixé mais pas tranché.

## 5. Faits redérivés ou précisés aujourd'hui

- **Le cadre de Gram des 84 étiquettes, sous forme explicite.** 7 P₋₄(B) = 3I − B − K, avec
  K = (3 UᵀU + UᵀPU − 2J)/8.
  - Les ψ_w ont pour norme 5/2 et ⟨ψ_w, ψ_u⟩ = −B_wu + κ, où κ ∈ {−1/4, 0, −1/8, 1/8, 1/4} selon le motif de lettres
    (côté, diagonale, même lettre, lettres partenaires, droites disjointes).
  - La distribution des produits scalaires ne dépend que de S (côtés) et de D (diagonales). C'est pourquoi le Delsarte
    est trivial.
  - Analogue pour une droite : 7 Π_T = 3I − R_T − K_T, avec K_T ≈ Eᵀ(3I − G_T)⁺E.
- **c(T) comme nombre d'orbites.** Vu d'un point s de T, G_T est fixé par trois couplages et une permutation des
  12 lettres de s : μ_s (les droites en s), μ_p et μ_q (arêtes « même lettre » en p et q) et π (arêtes croisées).
  - c(T) est le nombre d'orbites de ⟨μ_s, μ_p, μ_q, π⟩.
  - Q_{T,b} est une grille si et seulement si μ_p et μ_q fixent la paire {b₀, b₁} et π fixe b₀ et b₁.
- **Lien prismes–gabarits.** 3P = nombre de (quadrangle, paire d'arêtes opposées) dont les tiers points sont
  adjacents. Donc P = Σ_r côtés(r) / 6 = 6G + Σ_r s'(r) / 6.
- **Six grilles : les colonnes ne sont pas uniques.** L'archive n'avait pas examiné ce point. Une énumération exacte
  (`sixgrid_columns.py`, à symétrie S₆ × S₃ près) trouve plus de 536 classes de solutions pour la partie colonnes en
  moins de 5 minutes, et elle n'est pas finie.
  - Conséquence : on ne peut pas fixer une solution de colonnes canonique.
  - Le modèle complet de l'étape A (colonnes, signes, au plus 2 coïncidences ; `sixgrid_sat.py`) ne se tranche pas en
    280 s (CaDiCaL).

## 6. Diagnostic

- **Pourquoi les relaxations globales échouent.**
  - Elles ne voient que des moyennes ; la moyenne d'une vraie solution sur toutes les permutations est réalisable.
  - La positivité sur les sommets et les droites est loin d'être serrée : 99 ou 231 points en dimension 44 ou 54.
- **Pourquoi le recensement ne peut pas trancher c ≤ 2.** c(T) est une propriété de 39 sommets, hors de portée d'un
  ordre ≤ 10.
- **Ce qui tue vraiment.** Les calculs finis exacts sur des cœurs (familles K3U, 2K2, P3NB, K2BC, 2K2N…, avec preuves
  RUP). Les 28 gabarits c = 3 encore ouverts hors P3 n'ont pas de cœur forcé assez petit.

## 7. Pistes, avec leur meilleur résultat possible et leur coût

| Piste | Meilleur résultat | Coût, état |
|---|---|---|
| Design « six grilles » : décomposition colonnes, puis signes, puis graphe, avec symétrie | Lemme « aucune droite dans six grilles », qui tue 7 des 19 gabarits sans paire (9302, 9791, 9912, 9966, 10003, 10006, 10025) et c = 6 partout | Local, quelques heures de travail ; énumération des colonnes à finir proprement (génération ordonnée) |
| Recensement d'ordre 10 avec E3, en programme linéaire | Meilleures bornes sur P et G (aujourd'hui P ≤ 852, 3P + 4G ≤ 2772) ; aucune exclusion attendue | Le PL n'a pas fini en 5 min le 18/10 ; une machine Spot pendant moins d'une heure, moins de 5 USD, sur accord |
| Recensement + positivité (références ≤ 7 sommets) dans le même programme semi-défini | Peut réduire P au-delà de 852 | Quelques heures de code ; machine modeste |
| Route B′ (une racine avec au moins 6 droites à c ≥ 3) | Étend l'exclusion c = 3 aux sommets n'ayant qu'une droite à c ≤ 2 | Énumération de gabarits plus large : coût à mesurer par un pilote |
