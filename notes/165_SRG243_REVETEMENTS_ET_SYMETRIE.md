# 165 — srg(243,22,1,2) : revêtements de Brouwer–Haemers, courbure, et plancher de symétrie (11/10)

*Objectif fixé : construire un srg(243,22,1,2) asymétrique (|Aut| = 1), ou une famille substantielle avec un mécanisme
démontré de brisure progressive de symétrie. Point de départ : BvLS et le jumeau Γ′ (note 159). Code :
`code/asym243/`. Ce document est tenu à jour au fil des calculs ; les statuts sont explicites.*

## 0. Résumé des statuts

| Énoncé | Statut |
|---|---|
| Bascule = rotation d'espaces propres, D = 9(P′₄ − P₄) | **démontré** (identité générale) |
| Bascule de ligne = 80 re-réglages de grilles AG(2,3) | **calculé** (exact) |
| Étalement régulier ⇒ revêtement triple de BH = srg(81,20,1,6) | **démontré** (spectre + unicité de BH) |
| Pas d'étalement régulier pour v = 99, 6273, 494019 | **démontré** (multiplicités non entières) |
| Nouveau srg(243,22,1,2) n° 3, \|Aut\| = 864 | **certifié** (srg vérifié, nauty + Schreier–Sims, invariants distincts) |
| Nouveau srg(243,22,1,2) n° 4, \|Aut\| = 3888 | **certifié** (idem) |
| Mécanisme : re-voltage invariant par Stab(S), S ⊂ BH | **implémenté** ; classifications complètes pour plusieurs S (§4 bis) |
| Grilles(Γ) = 270 + 3·(grilles plates de BH) | **démontré** (§5), vérifié sur les 4 graphes |
| Revêtements de Cayley sur un 3-groupe non abélien | **exclus** (recherche exhaustive après jauge) |
| Phénomène « deux solutions » : seuil exact à la ligne | **calculé** (sommet ≥ 2000, arête ≈ 1900, ligne 2, 2 lignes 1, grille 1) |
| Revêtement de BH : soit Z₃ (\|Aut\| divisible par 3), soit stabilisateur d'étalement = 2-groupe | **établi** (calcul, §6) |
| Existence d'un S₃-revêtement (candidat asymétrique) | **OUVERT** (§6) |
| srg(243,22,1,2) asymétrique | **non obtenu** ; réduit à l'existence d'un S₃-revêtement ou d'un graphe sans étalement régulier |

## 1. La bascule comme rotation d'espaces propres
Pour un srg(243,22,1,2), A = 9P₄ − 5I + J/9, où P₄ est le projecteur sur l'espace propre de 4. Deux srg de mêmes
paramètres sur le même ensemble de sommets diffèrent donc par **D = A′ − A = 9(P′₄ − P₄)**.

Si D est supporté par F × F, l'espace « libre » est X(F) = E₄(F) ⊕ E₋₅(F) : ce sont les vecteurs propres supportés
par F, c'est-à-dire les x à support dans F tels que Ax soit aussi à support dans F et x ⊥ 1. La bascule remplace
E₄(F) par un autre sous-espace de X(F), de même dimension.

**Critère de rigidité.** Si E₄(F) = 0 ou E₋₅(F) = 0, la complétion de F est unique.

Pour la bascule de ligne de BvLS : F = 180, dim E₄(F) = 72, dim E₋₅(F) = 50. D a pour spectre (±3√5)³², 0¹¹⁶. W₀ et
W₁ partagent 40 dimensions et sont tournés dans 32 plans, tous au **même angle cos θ = 2/3** (`frame.py`).

Pour la région lointaine d'une grille 3×3 dans BvLS : dim E₋₅(F) = 0. **Elle est rigide, sans aucune recherche.**

## 2. Anatomie : 80 re-réglages de grilles
En coordonnées de Golay (sommets = F₃⁵, voisins x ± h_i), la bascule de ligne T = ⟨h₀⟩ fait, pour chaque sommet
lointain w et chacune des 4 directions h_m dont la ligne w + ⟨h_m⟩ est entièrement lointaine, le remplacement
w + ⟨h_m⟩ → w + ⟨h_m ± h₀⟩.

Autrement dit, dans 80 plans affines AG(2,3) (cosets de ⟨h₀, h_m⟩, ce sont des grilles 3×3), on garde la classe
parallèle h₀ et on remplace la classe h_m par la classe h_m ± h₀ (`anatomy.py`). **BvLS et Γ′ sont des systèmes de
droites affines de AG(5,3)** (`lines_model.py`).

## 3. Étalements réguliers et revêtements de BH
Un *étalement* est une partition des 243 sommets en 81 lignes. Il est *régulier* si deux de ses lignes sont toujours
reliées par 0 ou 3 arêtes ; de façon équivalente, c'est une partition équitable.

**Lemme 1.** Si Γ = srg(v, k, 1, 2) a une partition équitable en lignes, le quotient Q est (k − 2)-régulier, de valeurs
propres k − 2, r − 2, s − 2, donc fortement régulier.
- *v = 243* : Q = srg(81,20,1,6) = **graphe de Brouwer–Haemers**, unique (Brouwer–Haemers 1992).
- *v = 99* : il faudrait srg(33,12,1,6), dont la multiplicité 180/7 n'est pas entière. **Aucun srg(99,14,1,2) n'a
  d'étalement régulier.** Il en va de même pour v = 6273 et v = 494019. Dans la famille, seuls v = 9 et v = 243 en
  admettent.

Un srg(243,22,1,2) à étalement régulier est donc exactement un **revêtement triple de BH à fibres triangles**. Il est
décrit par une bijection σ_e entre fibres pour chaque arête e de BH, et il est srg si et seulement si :
- (T) chaque ligne de BH se relève en trois lignes (holonomie triviale autour des triangles) ;
- (L) pour chaque paire non adjacente {P, R} de BH, les six composées σ_{ZR}σ_{PZ} (Z voisin commun) forment soit une
  classe de A₃ doublée (type 6/0), soit S₃ entier (type 3/3).

Vérifications : BvLS est un revêtement pour ses 11 classes parallèles, Γ′ pour une seule (`cover.py`).

## 4. Un troisième srg(243,22,1,2) (voir aussi Γ₄, §4 bis)
Trouvé par SAT dans l'espace des re-réglages selon h₀ (`run_affine.py`, puis retrouvé par `ucover.py`).

| | BvLS | Γ′ | **Γ₃ (nouveau)** |
|---|---|---|---|
| \|Aut\| | 3 849 120 | 4 320 | **864** |
| orbites | 243 | 3, 60, 180 | **27, 108, 108** |
| grilles 3×3 | 1 485 | 405 | **621** (23 par sommet, uniforme) |
| paires tordues (2 arêtes) | 0 | 19 440 | **14 256** |
| prismes | 8 910 | 2 430 | **4 158** |
| hexagones induits | 4 980 690 | 5 000 130 | **4 994 946** |
| étalements réguliers affines | 11 | 1 | 1 |

Les trois graphes sont deux à deux non isomorphes : le nombre de grilles suffit à les distinguer. Γ₃ réfute lui aussi
la conjecture de Reimbayev (n₃ = 14 256 > 0). Fichier : `code/asym243/aff0_1.npy` (export `data/srg243/family/`).

## 4 bis. Mécanisme dirigé par la symétrie, et un quatrième graphe
Pour un ensemble S de fibres (de sommets de BH), soit K = Stab_{Aut BvLS}(étalement h₀, S) ; K contient toujours la
translation h₀. On cherche, dans le modèle des droites affines (`stabcover.py`), les re-voltages **invariants par K** :
on impose des égalités sur les orbites de K agissant sur les droites candidates.

Plus K est petit, plus l'espace est grand. C'est le levier de brisure progressive, et chaque cas se résout en quelques
secondes à quelques minutes.

| S (sous-structure de BH) | \|K\| | classes obtenues | statut |
|---|---|---|---|
| sommet | 4320 | BvLS, jumeau | **complet** (INFEASIBLE ensuite) |
| arête | 432 | BvLS, jumeau | complet |
| ligne | 1296 | BvLS | complet |
| grille 3×3 | 864 | BvLS | complet |
| 3-coclique | 432 | BvLS | complet |
| **paire non adjacente** | **144** | **Γ₄ (\|Aut\| = 3888)**, jumeau | 3 solutions |
| K₂,₆ | 144 | Γ₄, jumeau | 3 solutions |
| ligne + point | 24 | jumeau, **Γ₃** | 3 solutions |
| aléatoires (\|K\| = 1296, 96, 54) | — | BvLS, jumeau, Γ₃ | complets |
| aléatoires (\|K\| = 24, 18, 12, 6, 3) | — | voir le journal `stabrun2.log` | 12 solutions par cas |

**Γ₄** : |Aut| = 3888 = 2⁴·3⁵, orbites 81 + 162, 837 grilles (31 par sommet), 189 grilles plates de BH, 9720 paires
tordues, 5670 prismes, 4 990 410 hexagones, un seul étalement régulier. Fichiers :
`data/srg243/family/gamma4_aut3888.{edges,g6,autgens}`.

Observation : dans toutes ces recherches, il n'apparaît que 4 classes : BvLS, le jumeau, Γ₃ et Γ₄.
**Conjecture : ce sont les seuls srg(243,22,1,2) Z₃-revêtements affines de BH.** Pour une classe générique (|Aut| = 3),
l'orbite de solutions serait environ 1600 fois plus grosse que celle de Γ₃ ; un tirage aléatoire la rencontrerait donc
d'abord. Or les tirages aléatoires sans symétrie (modèle affine, CP-SAT avec indices aléatoires, kissat avec
contraintes) ne redonnent que Γ₃.

## 5. La torsion est une courbure
Pour un revêtement de BH, appelons **plate** une grille 3×3 de BH (il y en a 405) dont l'holonomie autour de chaque
carré est triviale.

**Proposition.** grilles(Γ) = 270 + 3·#(grilles plates de BH).
- *Vérification :* BvLS 1485 = 270 + 3·405, Γ′ 405 = 270 + 3·45, Γ₃ 621 = 270 + 3·117 (`curvature.py`).
- *Preuve.* Une grille de Γ qui contient une fibre est l'une des 270 grilles « fibre × relevé de ligne ». Sinon, ses
  9 points tombent dans 9 fibres distinctes : deux points d'une même fibre seraient adjacents, et la fibre serait une
  droite de la grille. Elle se projette donc sur une grille de BH, et c'est une section fermée autour de chaque carré.
  En Z₃, une holonomie qui fixe un point est triviale, donc la grille de BH est plate. Réciproquement, une grille plate
  se relève en 3 sections disjointes. ∎

En particulier, la condition (*) de Makhnev (« deux lignes sécantes sont dans une grille ») équivaut à la **platitude**
de la connexion sur les carrés de grilles, et le nombre n₃ de Reimbayev mesure la **courbure totale**. BvLS est le
revêtement plat.

## 6. Plancher de symétrie : Z₃, ou un 2-groupe
Si le cocycle de parité ε (la signature des σ_e) est un cobord, on peut orienter les fibres pour que tous les σ_e soient
des rotations. La rotation (P, t) ↦ (P, t + 1) est alors un automorphisme d'ordre 3 sans point fixe.

**Faits établis.**
1. **Rang GF(2)** (`parity_lin.py`) : dim H¹(BH ; Z₂) = 460 (810 arêtes, 270 triangles disjoints en arêtes, 80
   cobords). Si toutes les paires sont de type 6/0, alors ε est un cobord.
2. **Forme linéaire de Jørgensen** (`parity_lin2.py`). Posons L_PR(ε) = somme des 12 étiquettes du K₂,₆ de la paire,
   c'est-à-dire la somme des 6 parités de chemins. On a L = 0 pour une paire 6/0 et L = 1 pour une paire 3/3. L est
   injective sur H¹ (rang 460) : **ε est déterminé par l'ensemble T des paires 3/3**, et 1_T appartient à un code
   binaire [2430, 460] invariant par Aut(BH).
3. **T ≠ tout.** Le système « L = 1 partout » est incohérent ; c'est l'argument de L. K. Jørgensen (WL2018) pour la
   non-existence du revêtement double distance-régulier {20,18,3,1; 1,3,18,20} de BH, que j'ai reproduit.
4. **Aucune symétrie d'ordre impair** (`parity_cms_aut.py`, `oddclasses2.py`, `parity_classes_test.py`). Aut(BH) a
   4 classes d'éléments d'ordre 3, de tailles 20, 60, 720 et 1440, et une classe de sous-groupes d'ordre 5. Pour
   chacune, aucune classe de parité non triviale n'est invariante (CryptoMiniSat, UNSAT). L'invariance stricte est
   sans perte de généralité pour un ordre impair (moyennisation). Pour les translations, le résultat a été retrouvé de
   façon indépendante, sur les 3 types de vecteurs.
5. **Restriction affine** : forcer une paire 3/3 dans le modèle affine est INFEASIBLE.

**Dichotomie.** Soit Γ un srg(243,22,1,2) à étalement régulier 𝒮. Alors :
- **(a)** soit Γ est un Z₃-revêtement, avec un automorphisme d'ordre 3 qui stabilise chaque ligne de 𝒮 ;
- **(b)** soit la monodromie est S₃ entier. Dans ce cas il n'y a pas de transformation de revêtement, et Aut(Γ)_𝒮
  s'injecte dans un sous-groupe de Aut(BH) sans élément d'ordre 3 ni 5, donc dans un **2-groupe d'ordre ≤ 64**.

La monodromie contient A₃ dès qu'une paire 6/0 existe, ce qui est le cas d'après le point 3.

**Statut de (b) : OUVERT.** CryptoMiniSat sans verdict en 1 h sur le problème général. Si (b) existe, ses représentants
sont génériquement **asymétriques**. La question « srg(243,22,1,2) asymétrique à étalement régulier » équivaut donc à
l'existence d'un ensemble T non trivial dans le code ci-dessus, compatible avec les conditions 6/0 et 3/3.

*Erratum interne :* une première normalisation fixait un motif incompatible avec la jauge d'arbre. Elle donnait un UNSAT
trivial, que le contrôle positif a détecté. Une lecture trop rapide du résumé de Jørgensen m'avait aussi fait croire à
l'existence du revêtement double ; le texte dit le contraire. Les deux points sont corrigés ci-dessus.

## 7. Le phénomène « deux solutions »
Candidats par ligne de la région lointaine, dans BvLS (`rowcands.py`) :

| X fixé | \|F\| | candidats par ligne |
|---|---|---|
| sommet | 220 | ≥ 2000 |
| arête | 200 | ≈ 1750–2000 |
| **ligne** | **180** | **2** |
| 2 lignes sécantes | 144 | 1 |
| grille | 72 | 1 |

La ligne est exactement le seuil. Sur Γ₃, les 7 orbites de triangles sont toutes rigides (`triswitch.py`).

## 7 bis. Tableau vérifié de la famille, et symétrie locale contre globale
Généré par `family_table.py` (`family_table.md`). Méthode :
- srg vérifié sur les 29 403 paires, en Python pur ;
- |Aut| calculé par nauty, chaque générateur vérifié comme automorphisme, puis l'ordre du groupe engendré recalculé
  par Schreier–Sims (sympy) ;
- non-isomorphisme par formes canoniques nauty et par le nombre de grilles.

| graphe | \|Aut\| | orbites | grilles | grilles plates de BH | paires tordues | prismes | hexagones | étalements réguliers |
|---|---|---|---|---|---|---|---|---|
| BvLS | 3 849 120 | 243 | 1485 | 405 | 0 | 8910 | 4 980 690 | 11 |
| jumeau Γ′ | 4 320 | 3, 60, 180 | 405 | 45 | 19 440 | 2430 | 5 000 130 | 1 |
| **Γ₄** | **3 888** | 81, 162 | 837 | 189 | 9 720 | 5670 | 4 990 410 | 1 |
| **Γ₃** | **864** | 27, 108, 108 | 621 | 117 | 14 256 | 4158 | 4 994 946 | 1 |

*Local contre global.* Pour chaque orbite de sommets, on compare deux groupes :
- le groupe du **graphe local des grilles**, sur les 11 lignes par x, deux lignes étant adjacentes si elles engendrent
  une grille ;
- le **stabilisateur global** de x.

| graphe | arêtes du graphe local | \|Aut local\| | \|Stab(x)\| |
|---|---|---|---|
| BvLS | 55 (K₁₁) | 39 916 800 | 15 840 |
| jumeau | 55 / 19 / 13 | 39 916 800 / 725 760 / 1152 | 1440 / 72 / 24 |
| Γ₄ | 31 | 17 280 | 24 / 48 |
| Γ₃ | 23 | 2 304 | 8 / 32 |

La symétrie locale dépasse la symétrie globale par des facteurs de 300 à 2500. Dans tous les cas, la ligne d'étalement
est adjacente aux 10 autres dans le graphe local (grilles « fibre × relevé »). La perte de symétrie globale vient des
grilles transverses, c'est-à-dire de la courbure.

## 8. Ce qui se transfère à (99,14,1,2)
1. **Chirurgie spectrale.** Deux srg(99,14,1,2) qui coïncident hors de F × F diffèrent par D = 7(P′₃ − P₃), une
   rotation dans E₃(F) ⊕ E₋₄(F). Le critère de rigidité (E₃(F) = 0 ou E₋₄(F) = 0 ⇒ complétion unique) s'applique tel
   quel aux complétions partielles de la route Ω.
2. **Aucun étalement régulier** (lemme 1). Le seul mécanisme qui produise des srg(243,22,1,2) non isomorphes à BvLS,
   le re-voltage sur BH, n'a pas d'analogue à 99. Inversement, l'obstruction « plancher Z₃ » ne s'y applique pas.
   Rien n'empêche donc, de ce côté, un graphe de Conway asymétrique (cas C1).
3. **Torsion = courbure.** À 243, la torsion qu'exige Makhnev se réalise sans perte de régularité locale, comme une
   courbure d'une connexion Z₃. À 99, la torsion est obligatoire (Makhnev) mais elle ne peut pas venir d'un revêtement.
4. **Où se loge la symétrie résiduelle.** À 243, tous les graphes connus gardent un Z₃ de revêtement, et le mécanisme
   ne peut pas descendre sous ce plancher sans monodromie non abélienne (§6). À 99, le cas C1 (asymétrique) est le seul
   restant. Le lemme 1 dit que ce graphe n'aurait aucune structure de revêtement, donc aucun « plancher » de ce type. Le
   cas 243 n'est donc pas un modèle de C1 ; c'est plutôt un contre-modèle, qui montre comment la symétrie *survit*
   quand une partition équitable en lignes existe.
5. **Seuil de rigidité.** Le phénomène « 2 solutions exactement à la ligne » (§7) est la version 243 de la route Ω. À
   99, la région lointaine d'un triangle a 60 sommets, et les dimensions forcées par comptage sont dim E₃(F) ≥ 54 − 39 =
   15 et dim E₋₄(F) ≥ 44 − 39 = 5. La complétion de la route Ω est donc a priori une rotation entre un espace de
   dimension ≥ 15 et un espace de dimension ≥ 5. Le critère de rigidité de §1 s'applique tel quel à chaque complétion
   partielle.

## 9. Bilan par rapport à l'objectif
- **Objectif « |Aut| = 1 » : non atteint.** Ce qui est démontré (calcul) : un srg(243,22,1,2) asymétrique n'a pas
  d'étalement régulier, **sauf** s'il existe un S₃-revêtement de BH, question ouverte (§6). Tous les mécanismes de
  re-voltage aboutissent à des Z₃-revêtements, donc à |Aut| divisible par 3.
- **Famille.** Deux nouveaux graphes (Γ₃ : 864, Γ₄ : 3888), certifiés, s'ajoutent à BvLS et au jumeau. Le mécanisme
  qui les produit (re-voltage invariant par Stab(S)) est uniforme et explique le jumeau (S = sommet). Il donne des
  classifications complètes sous symétrie (§4 bis), mais ne « descend » pas : on retombe toujours sur les mêmes 4
  classes, d'où la conjecture de §4 bis.
- **Ce que la recherche a établi en route** :
  - la chirurgie spectrale et son critère de rigidité ;
  - le seuil de rigidité exact (ligne) ;
  - le dictionnaire étalement régulier ↔ revêtement de BH ;
  - torsion = courbure (formule des grilles) ;
  - la non-existence d'étalements réguliers à 99, 6273 et 494019 ;
  - l'exclusion des revêtements de Cayley non abéliens ;
  - la dichotomie Z₃ / 2-groupe, avec la relation linéaire de Jørgensen et l'absence de symétrie d'ordre impair.
