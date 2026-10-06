# 157 — Route Ω : une route finie complète, prouvée, et ce qu'elle implique (06/10, nuit)

*Demande de l'utilisateur : prouver qu'une route finie, même extrêmement longue, décide l'existence ; puis chercher tout ce
qu'elle implique et comment la réduire. Tout ici est démontré dans la note ou vérifié exactement sur des graphes connus.
Rien ne dépend de la disjonction 18/26/37 de la passation, qui n'est pas revérifiée. Code : `code/omega/`.*

## 0. Notations
- G est un srg(99,14,1,2) et A sa matrice d'adjacence ; M = 3I − A.
- Spectre : 14¹, 3⁵⁴, (−4)⁴⁴. Donc rang M = 45, et ker M = E₃ (dimension 54).
- On fixe une racine v. N(v) = 7K₂, sur les éléments a₁, a₁′, …, a₇, a₇′ ; a′ désigne la mate de a.
- **Les 84 labels.** Les 84 non-voisins de v sont en bijection avec les 84 paires non mates {a, b} de N(v) : chacun est
  adjacent, dans N(v), exactement à ses deux éléments. En effet μ(a, b) = 2 = v + un seul autre sommet.
  - L est l'ensemble des 84 labels, et Γ le graphe induit sur L.
  - B (14 × 84) est l'incidence élément–label, et Mt (14 × 14) la matrice des mates.
  - **L'étoile** L_a est l'ensemble des 12 labels qui contiennent a.

## 1. Théorème Ω (complétude)
**Lemme 1.** Aucun vecteur propre de A pour la valeur 3 n'est supporté par N[v].

*Preuve.*
1. Soit x ∈ E₃ supporté par N[v]. Pour un non-voisin w de label {a, b}, on a (Ax)_w = 3x_w = 0, donc x_a + x_b = 0.
2. Prenons a, b, c deux à deux non mates : il en existe, car N(v) a 7 ≥ 3 paires. On obtient x_a = −x_b = −x_c, puis
   x_b = x_c = −x_b, donc x_b = 0. Ainsi x est nul sur N(v).
3. Enfin (Ax)_a = x_v = 3x_a = 0. Donc x = 0. ∎

*Contrôle.* Paley9 n'a que 2 paires : le lemme y est faux, et le rang des lignes y vaut 4 au lieu de 5. BvLS243 a 11 paires :
le lemme y est vrai, avec un rang de 23 sur 23.

**Lemme 2 (complément étoilé contenant N[v]).** Il existe W ⊂ L, |W| = 30, tel que M_HH soit inversible pour
H = N[v] ∪ W.

*Preuve.*
1. Par le lemme 1, les lignes de M indexées par N[v] sont indépendantes : y^T M = 0 avec y supporté sur N[v] donnerait
   y ∈ E₃.
2. On les complète en une base I des lignes, avec |I| = 45 = rang M.
3. Pour M symétrique, M_II est inversible. En effet, chaque ligne s'écrit M_j = Σ c_ji M_i, donc M_{·I} = C·M_II. Si
   M_II x = 0, alors M_{·I} x = 0 ; or les colonnes I sont indépendantes, puisque ce sont les lignes I par symétrie.
   Donc x = 0. ∎

**Lemme 3 (reconstruction).** Soient X = L ∖ W (54 labels), B_H = A_{HX} et R = (3I − A_H)⁻¹. Alors
3I − A_X = B_Hᵀ R B_H.

*Preuve.* rang M = 45 = rang M_HH, donc le complément de Schur M_XX − M_XH M_HH⁻¹ M_HX est nul. Il suffit d'y remplacer
M_XX = 3I − A_X et M_XH = −B_Hᵀ. ∎

Pour chaque colonne b_x, cela donne :
- b_xᵀ R b_x = 3 ;
- b_xᵀ R b_y = −A_xy pour x ≠ y.

Chaque colonne a la forme b_x = e_a + e_b + 1_{S_x}, où {a, b} est le label de x et S_x ⊂ W.

**Procédure Ω (finie).**
1. Énumérer les couples (W, Γ_W), avec W ⊂ L de taille 30 et Γ_W un graphe sur W, tels que 3I − A_H soit inversible et
   que les plafonds λ/μ soient respectés dans H.
2. Pour chaque label x ∉ W, énumérer les S_x ⊂ W tels que b_xᵀ R b_x = 3 et que les plafonds locaux soient respectés.
3. Choisir un S_x par label, de sorte que b_xᵀ R b_y ∈ {0, −1} pour tous x ≠ y.
4. Poser A_X = −(b_xᵀ R b_y), puis vérifier A² + A = 12I + 2J.

**Théorème Ω.**
- **Complétude :** si un srg(99,14,1,2) existe, la procédure en produit un. Les vrais W, Γ_W et S_x passent toutes les
  étapes, par les lemmes 2 et 3.
- **Correction :** tout ce qu'elle produit est vérifié à l'étape 4.
- **Finitude :** tous les choix sont pris dans des ensembles finis.

**Elle décide donc l'existence de Conway, et en particulier le cas C1** : on lit |Aut| sur les graphes trouvés. ∎

**Validation de bout en bout** (`omega_small.py`, arithmétique rationnelle exacte, énumération de tous les H par geng).
La même procédure retrouve exactement l'unique graphe de chacun des trois cas tests, et rien d'autre :
- Petersen srg(10,3,0,1), avec r = 1 et |H| = 5 ;
- Paley9 srg(9,4,1,2), avec r = 1 et |H| = 5 ;
- Clebsch srg(16,5,0,2), avec r = 1 et |H| = 6.

Sur BvLS243 (r = 4, |H| = 111 ⊇ N[v], `bvls_check.py`), tout est vérifié exactement : 1ᵀR1 = −27/2, bᵀR1 = −1 et
BᵀRB = 4I − A_X.

## 2. Ce qui émerge de la route

### 2.1. Deux conditions sont automatiques
- On a P⁻¹1_{N[v]} = −2e_v − ½·1_{N(v)}, avec P = 3I − A_{N[v]} (le moulin à vent).
- On en déduit 1ᵀR1 = −9 et bᵀR1 = −1 identiquement, dès que H ⊇ N[v]. Ce ne sont pas des filtres.
- Formules générales pour λ = 1, μ = 2, valeur propre r : 1ᵀR1 = −n/(k − r) et bᵀR1 = −1. Vérifiées sur BvLS.

### 2.2. Forme close du complément de Schur sur les labels
En éliminant le bloc rigide N[v], on obtient sur les 84 labels :

  **T = 3I − Γ − K**, avec K_ℓℓ′ = (3/8)|ℓ ∩ ℓ′| + (1/8)·m(ℓ, ℓ′) − 1/4,

où m(ℓ, ℓ′) compte les relations de mates entre les éléments de ℓ et ceux de ℓ′.
- La matrice **8T est exactement la matrice L de la passation (§5.1)** : 24I − 8Γ − 3BᵀB − BᵀMtB + 2J.
- De (3I − A)² = 7(3I − A) + 2J et de C ᵀP⁻¹1 + 1_W = 0, on tire **T² = 7T et rang T = 30**.
- La forme close est vérifiée exactement sur BvLS : T² = 9T, rang 88.

**Équivalence (★).** Un srg(99,14,1,2) existe si et seulement s'il existe un graphe Γ **12-régulier** sur les 84 labels
tel que T² = 7T.

*Preuve de ⇐.*
1. La régularité de Γ rend le graphe enraciné 14-régulier.
2. T² = 7T donne rang M = 45, donc la valeur 3 a la multiplicité 54.
3. Les traces de A et A² donnent alors, pour les 44 valeurs propres restantes, une somme de −176 et une somme de carrés de
   704. Leur variance est nulle : elles valent toutes −4.
4. On obtient le spectre 14¹, 3⁵⁴, (−4)⁴⁴. C'est un srg(99,14,1,2), et les conditions λ/μ sont des conséquences, pas des
   hypothèses. ∎

### 2.3. Image en repère
T/7 est un projecteur de rang 30. Les 84 labels donnent donc **un repère tendu η_ℓ de R³⁰** (Σ ηηᵀ = I).
- Chaque vecteur a la norme 5/14.
- Les produits scalaires valent −(Γ + K)/7.
- **Sommes d'étoile.** On a BT = 0 : on le calcule de BΓ = 2J − B − MtB, avec BBᵀ = 11I + J − Mt. Chaque étoile L_a a donc
  ses 12 vecteurs de somme nulle. Ce sont exactement les différences d'étoiles fermées (A + 4I)(e_a − e_v).
- **Lien avec les réseaux.** η_ℓ ∈ N_v^*, où N_v est le réseau, de rang 30, des fonctions entières de valeur propre −4
  nulles sur N[v]. On a 56·N_v^* ⊂ N_v et min N_v ≥ 14.
- C'est l'analogue C1 du repère de la route (C), mais en rang 30, non classifiable.

### 2.4. Deux étoiles mates
- Γ sur L_a ∪ L_a′ vaut **exactement τ_a ∪ τ_a′ ∪ σ_aa′** :
  - chaque label de L_a a un seul voisin dans L_a (λ avec a) et un seul dans L_a′ (μ avec a′) ;
  - τ_a et τ_a′ sont des appariements, σ une bijection.

  Vérifié sur BvLS.
- **Mesure sur 20 000 structures (τ, τ′, σ) admissibles tirées au hasard :**
  - le bloc T_S est **toujours** semi-défini positif ;
  - son rang vaut 22 dans 99,97 % des cas, et 21 dans 7 cas ;
  - **ce niveau n'élague donc rien**, alors qu'il compte de l'ordre de 10¹¹ à 10¹² structures à symétrie près.

### 2.5. Pression de rang
- Une fois deux étoiles mates fixées (22 dimensions), les 60 autres labels ont leurs résidus dans **R⁸**.
- Ils y forment un repère tendu de trace 8.
- Chaque label restant a 2 voisins dans L_a et 2 dans L_a′. Son résidu vaut (1/7)(5/2 − tᵀT_SS⁺t).
- Mesures sur trois structures de premier niveau tirées au hasard (`residual8.py`) :
  - par label, 46 à 76 % des 4 356 choix (2+2) ont un résidu ≥ 0 ;
  - le résidu (×7) vaut au plus 1,52 ;
  - or la somme imposée, 56 sur 60 labels, donne une moyenne de 0,93 : presque tous les labels doivent être près du
    maximum.
- **Trois étoiles** L_a, L_a′, L_b couvrent 34 labels avec 3 relations d'étoile. Le rang générique serait 31, il doit être
  ≤ 30. Toute structure à trois étoiles doit donc porter une relation supplémentaire. C'est une condition algébrique
  locale (49 sommets), nécessaire pour tout triplet (v ; a, a′, b).

## 3. Taille de la route, et où réduire
- **Naïvement**, il y a C(84, 30) choix de W fois les graphes Γ_W : c'est astronomique, mais fini.
- **Premier niveau canonique** (W ⊇ deux étoiles mates moins leurs deux relations, soit 22 labels) : de l'ordre de 10¹¹
  à 10¹² structures, sans élagage. Viennent ensuite 8 labels de base et leurs adjacences, puis 52 colonnes forcées.
- **Leviers identifiés** (le programme de lemmes, comme pour C2) :
  1. La condition à trois étoiles (§2.5) : la caractériser combinatoirement, et en tirer un lemme qui coupe les
     structures (τ, τ′, σ, τ_b, arêtes croisées).
  2. Le repère de trace 8 en R⁸ après le premier niveau : sommes de résidus imposées. C'est un problème de type sac à dos,
     très contraint.
  3. Raccorder les branches 18, 26 et 37 comme accélérateurs. Si une fonction courte existe, son noyau naturel est un
     complément étoilé, et elle restreint fortement Γ. Cela demande d'abord de revérifier la disjonction.
  4. Le test de classe mod 7 (note 155) sur les germes de la route.

## 4. Fichiers (`code/omega/`)
- `graphs_test.py` : graphes témoins.
- `lemma_nv.py` : lemme 1, contrôlé sur Paley9 et BvLS.
- `omega_small.py` : procédure de bout en bout, exacte.
- `bvls_check.py` : identités exactes avec H ⊇ N[v].
- `schur_root_check.py` : T² = (r − s)T et forme close de K.
- `stars_check.py` : BT = 0, structure et rang des deux étoiles.
- `twostar_psd.py` : premier niveau.
- `residual8.py` : résidus en R⁸.
