# Le résidu lointain d'une droite est-il global ? Règle des classes, droites latérales, conditions globales

LAB, 20/10/2026, fin d'après-midi. Mission : la classe du résidu 7-adique d'une droite comme idée pour les rangs 39 à 43.

**Statuts.**
- **P** : preuve écrite ici, non relue par un tiers.
- **A** : déjà dans l'archive (fichier:ligne).
- **E** : calcul fait ici (un processus, moins d'une minute chacun).
- **X** : ouvert.

Rien ici n'exclut un rang. Les calculs (§6) ont été faits avant 16:33. Aucun calcul n'a été lancé après la demande
d'arrêt (l'utilisateur est revenu sur le PC).

**Sources lues.**
- RD = `work/c1_index_2026-10-09/NOTE_RESEAUX_DE_DROITE.md`.
- TL = `work/c1_theta_lp_2026-10-07/NOTE.md`, §17.80 et addenda (lignes 3083-3200).
- Dans ce dossier : NOTE_OBSTRUCTION, NOTE_BOOST, NOTE_FUSION, `oblr_prep.py`, `star39.cpp`, ainsi que deux notes écrites
  en parallèle aujourd'hui, NOTE_BORNE_RANG et NOTE_ORDRE2_7ADIQUE (A, non relues).

**Notations.**
- M = A − 3I mod 7 et r = rang₇ M = 37 + 2k. On note v_u = M e_u.
- C = Im M ⊂ 𝔽₇⁹⁹, de dimension r, munie de b(My, My′) = yᵀMy′. Cette forme est bien définie et non dégénérée sur C.
  On a b(v_u, v_w) = M_uw et b(v_u, c) = c_u pour tout c ∈ C.
- C₀ = C ∩ 𝟏^⊥, de dimension r − 1. C'est le « D » de NOTE_BORNE_RANG.
- Pour une droite T : N = N[T] (39 sommets), F (60 lointains), N_T = vect{v_p : p ∈ N}.
- C_T = {c ∈ C : c|_N = 0} = N_T^{⊥_b}. C'est le « C(T) » de NOTE_BORNE_RANG.
- Moteur : Res_T = R − 3I − β = U D_δ Uᵀ, où D_δ = diag(1, …, 1, δ) est de taille ρ = r − 38 + d.
- Une droite est **équilibrée** si M_FN tue ker M_NN. C'est le cas de toute droite générique, et des droites c ≥ 2 sans
  torsion (par L4).

---

## 0. Réponse courte

### Q1. La règle est juste (P), et elle s'étend à tout type de droite équilibrée
- **Énoncé, dans la convention du moteur.** Pour toute droite équilibrée (c et d quelconques) :

      χ(det D_δ) = (−1)^((r+1)/2) · χ(disc_nd M_NN).

  Ici disc_nd est le discriminant de la partie non dégénérée de M_NN mod 7, et χ le caractère de Legendre.
- **Cas particuliers.**
  - c = 1, 7 ∤ τ : χ(disc_nd M_NN) = (τ|7). On retrouve χ(det U″) = (−1)^{k+1}(τ|7) (RD:29-32).
  - d = c, sans torsion : χ(disc_nd M_NN) = (−1)^{c+1} ∏ᵢ (τᵢ|7). Au rang 37, cela donne χ(δ) = (τ₁τ₂|7) pour c = 2
    (c'est TL 17.80, corollaire B) et χ(δ) = −∏ᵢ(τᵢ|7) pour c = 3.
- **Trois preuves indépendantes, toutes à la main.**
  - Dans l'archive : la formule d'oddité (TL 17.80, lemme), et la complétion de Witt (règle B′ de TL, arbitrée par Codex).
  - Ici : la formule du produit des invariants de Hasse, via c₂(V₋) = −1 parce que E₋ ⊗ ℤ₂ ≅ H²² (§1.2).
  - Ici : le scindage C = N_T ⊥ C_T, avec le déterminant bordé exact 144τ (§1.3).
- **Ce qu'est U″.** 7U″ est le constituant 7-modulaire de Λ₋(T) ⊗ ℤ₇. De façon équivalente, U″⁻¹ ≅ −(C_T, b) ≅ −D_δ
  mod 7 (§1.1).
- **Aucune faille trouvée.** Seul point délicat : le signe, qui compte quand ρ est impair (§1.5).
- **Conséquence pratique.** Une seule forme δ par droite suffit (algorithme au §1.6). Cela divise par 2 tous les runs où le
  moteur essaie les deux formes.

### Q2. Non : la classe du résidu n'est pas un invariant global
- **Ce qui est global (P ; en partie A).**
  - La classe de (C, b), de caractère χ = (−1)^{(r+1)/2}.
  - L'inclusion C_T ⊂ C₀, pour toute droite.
  - La partie unimodulaire de Λ₋(T) ⊗ ℤ₇ : elle est isométrique à celle de E₋, de caractère χ = (−1)^{k+1}, pour **toutes**
    les droites génériques.
- **Ce qui varie.** La classe de N_T, qui vaut (τ(T)|7) et ne dépend que de G_T. La classe de C_T s'en déduit.
- Au rang 37 seulement, C_T = 0 force N_T = C, donc (τ|7) = −1 : c'est L23.
- Une réponse « oui » ne diviserait de toute façon le travail que par 2.

### Q3. Les droites latérales n'apportent rien (P)
La partie 7-adique de cet énoncé est déjà dans NOTE_ORDRE2:204-206 (A) ; je la redémontre autrement et j'y ajoute la
partie réelle.
- **Théorème B (§3.2).** Soit U un ensemble de sommets contenant N[T]. Le contenu 7-adique d'ordre 1 du modèle de droite
  sur U est exactement :
  - rang₇ M_UU ≤ r ;
  - en cas d'égalité, χ(disc_nd M_UU) = (−1)^{(r+1)/2}.

  Cette condition **ne dépend pas de la droite de base**.
- **Le contenu réel ne dépend pas non plus de la droite de base.** Il s'agit de la positivité du projecteur lointain pour
  les valeurs −4 et 3, avec les bornes de rang. La preuve passe par des compléments de Schur (§3.3), et les identités
  utilisées sont vérifiées (E).
- **Sur la double étoile (x, x̄), tout ce qu'impose T_x découle du modèle de T :**
  - L23 ou la règle de classe pour T_x ;
  - son résidu ;
  - ses coupes réelles sur les 20 sommets de (C₁ ∪ C₂) ∖ {x₁, x₂, x̄₁, x̄₂} ;
  - ses comptes μ.
- **Réfuté :** le « filtre gratuit, qui divise par 2 environ » de NOTE_OBSTRUCTION:178-181 est vide. Au rang 37,
  (τ(G_{T_x})|7) = −1 découle déjà des valeurs de Green sur la double étoile.
- **Gain d'élagage : nul.**

### Q4. Aucune condition globale entre résidus au-delà du rang lui-même (P)
- Pour U = V, le théorème B se lit simplement : rang₇(A − 3I) = r. La condition de classe est automatique.
- Toute relation entre les résidus de droites dont les boules sont contenues dans U découle de la condition de rang sur U.
- **Monotonie.** Le test au rang 43 contient ceux des rangs inférieurs : il vaut pour toute la fenêtre.
- **Sommes en étoile.** Σ_{F_x} u = 0 ne change aucun verdict. Ces relations ne font qu'éliminer des réalisations
  redondantes.

### Prochaine étape (§5)
1. **Une seule forme δ par droite, tout de suite.**
2. **Clore les pistes « droites latérales » et « combinaisons globales de résidus ».**
3. **Aux rangs 39 à 43, il ne reste que deux leviers par droite : des unités plus grandes et la positivité.** Un test unique
   au rang 43, sur la double étoile, vaut pour les quatre rangs. Il est déjà proposé dans NOTE_BORNE_RANG:459 (A) ; le
   théorème B en donne le contenu exact. Avant de l'écrire, il faut savoir si les étoiles des rangs 41 et 43 survivent
   (NOTE_ORDRE2 §6).

---

## 1. Q1 : la règle des classes

### 1.1 Énoncé, et ce qu'est U″

Soit T générique (c = 1, 7 ∤ τ), au rang r = 37 + 2k. On a Λ₋(T) ⊗ ℤ₇ ≅ U_{8−2k} ⊥ 7U″_{2k}, où U et U″ sont
unimodulaires. Les seules échelles possibles sont 1 et 7, car 7Π_T est 7-entier (A, NOTE_OBSTRUCTION:69-74).

U″ est défini à isométrie près par les trois descriptions équivalentes suivantes.
- 7U″ est le constituant de Jordan 7-modulaire de Λ₋(T) ⊗ ℤ₇.
- U″⁻¹ mod 7 est la forme induite par 7Π_T mod 7 sur son image, c'est-à-dire 7 fois la forme discriminante de Λ₋(T) en 7.
- Cette image est C_T, et 7Π_T ≡ −Res_T (mod 7) (E, T5). Donc U″⁻¹ ≅ −(C_T, b) ≅ −D_δ.
  - Pour ρ = 2k pair, det U″ ≡ det D_δ ≡ disc(C_T, b) modulo les carrés.

**Règle.** χ(det U″) = (−1)^{k+1}(τ|7). La partie unimodulaire a une classe fixe : χ(det U_{8−2k}) = (−1)^{k+1}
(A : NOTE_ORDRE2 §2.2 ; P : cela découle aussi de d(X) ≡ τ, sans passer par l'indice j).

### 1.2 Preuve par la formule du produit (P)

Convention : c_p = ∏_{i<j} (aᵢ, aⱼ)_p sur une diagonalisation. Avec cette convention, c_∞ = 1 pour une forme définie
positive, et ∏_p c_p = 1.

1. **En 2.**
   - E₋ est pair : si Ax = −4x, alors 18 Σxᵢ = 0, et x·x ≡ Σxᵢ (mod 2).
   - Son déterminant 9·7^{r−1} est impair et ≡ 1 (mod 8), puisque r est impair.
   - Un ℤ₂-réseau pair unimodulaire de rang 44 est H²² (déterminant 1) ou H²¹ ⊥ A (déterminant −3 ≡ 5). C'est donc H²².
   - Sur ℚ₂, H ≅ ⟨1, −1⟩. D'où c₂ = (−1, −1)₂^{C(22,2)} = (−1)^{231} = **−1**.
   - Contrôle de la convention : on obtient +1 en rang 8 (E₈), et −1 en rang 4, où il n'existe aucun réseau pair
     unimodulaire défini positif.
2. **En 3.** E₋ ⊗ ℤ₃ = U₄₃ ⊥ 9U₁ (colle cyclique d'ordre 9), donc c₃ = 1.
3. **Ailleurs.** Pour p ∉ {2, 3, 7}, E₋ est unimodulaire, donc c_p = 1.
4. **Conclusion.** **c₇(V₋) = −1, à tout rang impair.**
   - Appliqué à E₋ ⊗ ℤ₇ = U_{45−r} ⊥ 7U_{r−1} : c₇ = (−1)^{(r−1)/2} χ(det U_{r−1}), d'où χ(det U_{r−1}) = (−1)^{(r+1)/2}.
   - C'est exactement le lemme de TL 17.80 (« disc V non carré aux rangs 37 et 41, carré aux rangs 39 et 43 »), qui y est
     obtenu par la formule d'oddité. Les deux voies concordent.
5. **Décomposition de V₋.** V₋ = W ⊥ X, où W est engendré par les 36 projections proches. Leur Gram est (L + J/9)/7, avec
   L + J/9 7-unimodulaire de déterminant 144τ.
   - c₇(W) = (7, 144τ)₇^{35} = (τ|7).
   - d(W) ≡ d(X) ≡ τ, et (τ, τ)₇ = 1.
   - Donc c₇(X) = c₇(V₋) c₇(W) = −(τ|7).
6. **Réseau de droite.** Pour U_a ⊥ 7U_b, on a c₇ = χ(det U_a)^b χ(det U_b)^{b−1} (−1)^{b(b−1)/2}. Avec b = 2k, cela
   donne c₇(X) = (−1)^k χ(det U″). D'où **χ(det U″) = (−1)^{k+1}(τ|7)**. ∎

**Entrées utilisées (A).** 7Π_T est 7-entier, et rang₇(7Π_T mod 7) = ρ. La formule du déterminant avec j (RD:21) n'est
pas nécessaire.

### 1.3 Preuve par le code (P), valable pour toute droite équilibrée

1. **La forme globale.** (C, b) est non dégénérée de dimension r, et C = C₀ ⊥_b ⟨𝟏⟩.
   - En effet 𝟏 = M(2·𝟏), b(𝟏, 𝟏) = 4·1089 ≡ 2, qui est un carré, et b(𝟏, C₀) = 0.
   - Comme 7P₋ = 3I − A + J/9 ≡ −(M − 4J) et M − 4J = M(I − J), la forme (C₀, b) est l'opposée de 7 fois la forme
     discriminante de E₋ en 7. Sa dimension r − 1 étant paire, le signe n'y change rien.
   - Donc χ(disc C₀) = χ(det U_{r−1}) = (−1)^{(r+1)/2} (§1.2.4), et **χ(disc C) = (−1)^{(r+1)/2}**.
2. **Le scindage.** Pour une droite équilibrée, rang M[:, N] = rang M_NN. Donc b restreinte à N_T est non dégénérée,
   isométrique à la partie non dégénérée de M_NN, et **C = N_T ⊥_b C_T**.
   - C_T est exactement l'ensemble des mots de C nuls sur N[T], car b(v_p, c) = c_p.
3. **Identification avec la forme du moteur.**
   - La composante de v_w dans C_T est c_w = S e_w, où S est le complément de Schur.
   - Res_T est la Gram des c_w.
   - Dans la base des colonnes de U, b|_{C_T} = D_δ⁻¹, qui est isométrique à D_δ. Donc **classe(D_δ) = classe(C_T, b)**.
4. **D'où la formule.** χ(det D_δ) = χ(disc C)·χ(disc_nd M_NN) = (−1)^{(r+1)/2} χ(disc_nd M_NN).
   - La règle de scindage est vérifiée sur 215 matrices symétriques aléatoires de 𝔽₇, avec le g-inverse réflexif du moteur
     (E, T3).
5. **Calcul de disc_nd M_NN.**
   - **c = 1.** Les 37 coordonnées {t₀} ∪ proches forment un supplémentaire de ker M_NN. Par le théorème matrice-arbre,
     adj(L) = τJ, et adj(−L) = (−1)^{35} adj(L). D'où

         det [[−3, 𝟏_{C₀}ᵀ], [𝟏_{C₀}, G − 3I]] = −𝟏_{C₀}ᵀ adj(G − 3I) 𝟏_{C₀} = 144τ.

     Vérifié exactement sur 150 G_T sur 150 (E, T1).
   - **d = c.** Même calcul sur chaque composante, plus un plan hyperbolique. On obtient
     disc_nd ≡ (−1)^{c+1} ∏ᵢ τᵢ, et rang 38 − c (E, T2 : tous les cas tirés, profils 18+18, 12+24, 6+30, 12+12+12,
     6+6+24 et 6+12+18).
6. **Pour c = 1**, on retrouve χ(det D_δ) = (−1)^{19+k}(τ|7) = (−1)^{k+1}(τ|7) : c'est la règle de RD. ∎

### 1.4 L'archive, et ce que cela change

- **TL 17.80** (NOTE.md:3083-3160) : le lemme (formule d'oddité) et trois corollaires.
  - Corollaire A = L23 (note 102 de Codex, 25/09).
  - Corollaire B : c = 2 sans torsion, c₀ = τ₁τ₂. Le §1.3 donne la même chose.
  - Corollaire C : les autres rangs, c'est-à-dire la règle de RD.
- **Addendum de TL** (NOTE.md:3162-3200) : la règle B′, avec torsion, arbitrée par Codex, mais « non utilisée dans les runs
  ».
- **NOTE_BOOST:47-48** écrit que le type δ n'est « fixé par aucune règle prouvée » pour c ≥ 2 et pour les droites à
  torsion. En réalité, TL corollaire B et la règle B′ (A) le fixent, et le §1.3 le redémontre (P).
- **NOTE_ORDRE2:226-232** compte RD:31 parmi les dépendances non relues de (C43) et du choix de δ dans star39_prep.
- **Statut.** La règle a maintenant trois dérivations indépendantes, toutes à la main, et ses identités exactes sont
  vérifiées sur des boules aléatoires. Elle n'a été relue par aucun tiers, et il n'existe aucun graphe sur lequel la
  tester.

### 1.5 Signe et conventions

- D_δ représente (C_T, +b), où b est construite à partir de M = A − 3I, et non de −M.
- **ρ pair** : ±b ont la même classe, le signe est sans effet.
- **ρ impair** : le signe compte. C'est le cas de c = 2 au rang 37 (ρ = 1) et au rang 39 (ρ = 3), et de c1t au rang 37
  (ρ = 1).
  - Il faut alors appliquer la formule avec M_NN = (A − 3I)_NN, exactement comme le construit star_prep_gen
    (`near_block(...) − 3I`).
- **Côté Λ** : U″⁻¹ ≅ −(C_T, b) (T5).

### 1.6 Conséquence pratique : choisir δ (P, sous réserve de la règle)

**Algorithme**, dans la préparation, pour toute droite équilibrée :
1. Calculer (rang, d) = disc_nd(M_NN mod 7), par élimination symétrique sur la matrice 39 × 39. On peut prendre la routine
   `disc_nd` de `residu_checks.py`, ou `disc_mod7` de TL.
2. Poser ε = (−1)^{(r+1)/2}·χ(d).
3. Prendre δ = 1 si ε = +1, et δ = 3 si ε = −1. Un seul run par droite.

**Ce que cela donne.**
- **Rang 39, c = 1** : les runs « hors règle » de NOTE_BOOST §5 (graines 1 et 4, δ = 1) n'apportent rien. Ils explorent
  des configurations impossibles.
- **Rang 37, c = 2 (d = 2)** : δ = 1 si et seulement si (τ₁τ₂|7) = +1.
- **Rang 37, c = 3** : χ(δ) = −∏ᵢ(τᵢ|7).
- **c1t et c = 2 à torsion équilibré** : δ se lit directement sur d.
- **Codages déséquilibrés** (D = diag(4, 3)) : inchangés, il n'y a pas de choix.
- **Gain** : un facteur 2 sur les types où le moteur essaie les deux formes (c = 2, c = 3 et torsion, dans le plan de
  NOTE_BOOST §7). La partie c = 1 générique au rang 37 (ρ = 0) ne change pas.
- **Réserve** : abandonner les runs de sur-ensemble fait dépendre les verdicts de la règle. L'utilisateur peut préférer les
  garder jusqu'à une relecture.

---

## 2. Q2 : ce qui est global, ce qui varie

**Proposition 2 (P ; (a) est aussi dans A, TL 17.80 ; (b) dans NOTE_BORNE_RANG §2.2 ; (c) dans NOTE_BORNE_RANG,
théorème 5).**

(a) **La classe de (C, b)** est χ = (−1)^{(r+1)/2}, et celle de (C₀, b) aussi. Elle est la même pour tout graphe de 7-rang
r.

(b) **C_T ⊂ C₀ pour toute droite.**
- Soit c = My ∈ C_T. Alors Mc = M²y = 2(𝟏·y)𝟏.
- Or (Mc)_{t₀} = 0, puisque N(t₀) ⊂ N[T].
- Donc Mc = 0, et c ∈ C ∩ ker M = C₀.

(c) **La partie unimodulaire est commune à toutes les droites génériques.**
- Soit Λ̄ = Λ₋(T)/7 ⊂ D₋ := E₋/7 ⊂ 𝔽₇⁹⁹.
- rad D₋ = C₀, et rad Λ̄ = Im(7Π_T mod 7) = C_T.
- Comme C₀ ⊥ D₋, on a Λ̄ ∩ C₀ ⊂ rad Λ̄, donc Λ̄ ∩ C₀ = C_T.
- Ainsi Λ̄/C_T s'injecte isométriquement dans D₋/C₀. Les deux sont de dimension 8 − 2k = 45 − r : c'est une isométrie.
- Chaque droite générique porte donc la même partie unimodulaire, de caractère (−1)^{k+1}.

(d) **Ce qui varie.**
- (N_T, b) a pour caractère χ(disc_nd M_NN) = (τ(T)|7).
- De C = N_T ⊥ C_T, on tire classe(C_T) = classe(C) · classe(N_T).
- « Classe du résidu globale » équivaut donc à « (τ(T)|7) constant sur les droites génériques ».

(e) **Pourquoi rien ne force cette constance.**
- Pour r ≥ 39, un espace (C, b) de dimension r contient des sous-espaces non dégénérés de codimension 2k des deux classes.
- La seule contrainte qui lie N_T à N_{T′} est la réalisabilité de la Gram sur N[T] ∪ N[T′] (théorème B). Elle porte sur
  l'adjacence lointaine, et non sur le couple ((τ(T)|7), (τ(T′)|7)).
- Au rang 37, C_T = 0 force N_T = C, donc (τ|7) = −1. C'est le seul rang où la classe est globale.

(f) **Ce que vaudrait un « oui ».** Une division par 2 au plus : les deux classes se partagent les G_T à parts égales
(NOTE_BOOST:232).

---

## 3. Q3 : droites latérales

### 3.1 Géométrie (P, élémentaire)

Soit T = {t₀, t₁, t₂}, x ∈ C₀(T) de partenaire x̄, et T_x = {t₀, x, x̄}.
- N[T] ∩ N[T_x] = T ∪ C₀ ∪ {x₁, x₂, x̄₁, x̄₂} : 19 sommets.
- N(T_x) ∖ N[T] = F_x ∪ F_x̄ =: Δ. Ce sont les 20 lointains de T qui forment la double étoile.
- N(T) ∖ N[T_x] = (C₁ ∪ C₂) ∖ {x₁, x₂, x̄₁, x̄₂} =: Δ′, 20 sommets. Ils sont lointains pour T_x : c'est la double étoile de
  (t₁, t₂) vue depuis T_x, puisque T est latérale à T_x.
- |N[T] ∪ N[T_x]| = 59, et F(T) ∩ F(T_x) compte 40 sommets.
- La double étoile (noms de Δ et valeurs R sur Δ × Δ) fixe A sur les 59 sommets. Elle fixe donc G_{T_x}, τ(G_{T_x}) et
  les noms de Δ′ vus depuis T_x (A, NOTE_OBSTRUCTION §4.2).

### 3.2 Théorème B : indépendance de la droite de base, mod 7 (P)

**Hypothèses.** T générique, U ⊇ N[T], et S = U ∖ N[T] formé de lointains à noms légaux (deux par classe, aucun dans T).

**Énoncé.** Pour une adjacence candidate sur U, les deux conditions suivantes sont équivalentes.
- (i) Le modèle de droite de T (moteur, ρ = r − 37, D_δ fixé par la règle) admet des u_w, w ∈ S, tels que
  M_ww′ − β_ww′ = u_wᵀ D_δ u_w′ pour tous w, w′ ∈ S.
- (ii) rang₇ M_UU ≤ r, et en cas d'égalité, χ(disc_nd M_UU) = (−1)^{(r+1)/2}.

**Preuve.**
1. Des noms légaux donnent e_w ⊥ ker M_NN, puisque κ_ab·e_w = 2 − 2 = 0. Le scindage s'applique donc :
   - rang M_UU = 37 + rang Res_S ;
   - disc_nd M_UU = disc_nd M_NN · disc_nd Res_S (T3).
2. **Lemme (Witt).** Une matrice symétrique G de rang g sur 𝔽₇ est la Gram de vecteurs d'un espace non dégénéré Q de
   dimension ρ si et seulement si g ≤ ρ et, quand g = ρ, classe(G) = classe(Q).
   - Si g < ρ, on plonge le quotient non dégénéré : un espace de dimension g se complète par un espace de dimension
     ρ − g ≥ 1 du discriminant voulu.
   - Si g = ρ, il faut une isométrie.
   - Réciproquement, l'espace W engendré par les vecteurs vérifie g + 2 dim rad W ≤ ρ.
3. On applique le lemme avec G = Res_S, Q = (𝔽₇^ρ, D_δ), et la règle du §1. ∎

La condition (ii) ne fait pas intervenir T.

**Corollaire B1 (droite latérale).**
- Prenons U = N[T] ∪ Δ = N[T_x] ∪ Δ′, avec T_x générique. Les noms de Δ′ vus depuis T_x sont légaux dès que les marges de
  l'étoile de T sont satisfaites.
- Alors le modèle de T sur Δ et celui de T_x sur Δ′ acceptent les mêmes configurations.
- En particulier, la règle de classe pour T_x (ou L23) ne filtre jamais une double étoile acceptée par T.
- **Au rang 37**, (ii) donne rang M_UU ≤ 37, avec χ = −1 en cas d'égalité.
  - Or rang M_{N[T_x]} = 37 force l'égalité, et vect N[T_x] = vect U.
  - Donc χ(disc_nd M_{N[T_x]}) = (τ(T_x)|7) = −1, automatiquement.
  - **Cela réfute NOTE_OBSTRUCTION:178-181.**

**Corollaire B2 (redondance des u).**
- On peut imposer aux u les relations linéaires de ker M_UU sans changer aucun verdict sur les données (noms, R).
- Exemple : Σ_{F_x} u = 0. Elle vient du vecteur propre de droite κ = 3(e_x − e_{t₀}) + 𝟏_{N(x)∖T_x} − 𝟏_{N(t₀)∖T_x} de T_x,
  dont le support est contenu dans N[T] ∪ F_x.
- Raison : s'il existe une réalisation, la réalisation minimale (relations = ker M_UU) existe aussi.
- Ces relations ne font qu'éliminer des branches u redondantes, comme une coupure de symétrie. Cela précise
  NOTE_ORDRE2:26-31, où la somme en étoile est dite « automatique dès que rang U_S = ρ ».

**Corollaire B3 (monotonie).**
- (ii) au rang r entraîne (ii) au rang r′ > r.
- Un test au rang 43 (ρ = 6) est donc une relaxation valable pour toute la fenêtre. Le seul bit propre au rang est la
  classe en cas d'égalité.

### 3.3 Partie réelle (P et E)

On pose :
- Y_U = 3I − A_U + J/9, qui vaut 7 fois la Gram des P₋e_v ;
- Y³_U = 4I + A_U − (2/11)J, qui vaut 7 fois la Gram des P₃e_v.

**Identités (E, T4 et T6, pour des valeurs lointain–lointain arbitraires).**
- Le complément de Schur de Y_U par rapport au bloc de la boule N[T] est exactement H = 3I − R + J/9 − Eᵀ(3I − G + J)⁻¹E
  sur S.
- Celui de Y³_U est H₃ = 4I + R − (2/35)J − Eᵀ(4I + G)⁻¹E.
- Les blocs de boule sont semi-définis positifs de rang 36, et les conditions d'image sont vérifiées (20/20).
- Les formules de H et H₃ elles-mêmes sont dans l'archive (A : NOTE_BOOST §2.3, NOTE_ORDRE2 §3.1, avec un contrôle positif
  sur des srg(243) réels).

**Conséquences.**
- H_SS ⪰ 0 équivaut à Y_U ⪰ 0, et rang H_SS = rang Y_U − 36. De même pour H₃ et Y³_U.
- Ces conditions sur Y_U et Y³_U ne mentionnent pas T.
- Pour U = N[T] ∪ Δ = N[T_x] ∪ Δ′ : les coupes réelles de T sur Δ équivalent à celles de T_x sur Δ′, et
  rang H[Δ] = rang H′[Δ′]. Ces deux rangs valent 8 − dim(V₋ ∩ ℝ⁴⁰).
- NOTE_ORDRE2 §3.5 (A) montre que ces conditions forment tout le contenu réel de second ordre vu depuis T. Ce qui précède
  montre que c'est le même vu depuis T_x.
- **Réserve.** Le test « 7I − H ⪰ 0 » du moteur est plus faible que H₃ ⪰ 0 (A, NOTE_ORDRE2 §3.3). Je n'affirme
  l'indépendance de la base que pour H et H₃.

### 3.4 Bilan pour Q3

| condition de couplage entre T et T_x | statut |
|---|---|
| (τ(G_{T_x})\|7) = −1 par L23, au rang 37 | automatique (B1) |
| classe du résidu de T_x (règle), aux rangs ≥ 39 | automatique (B1) |
| structure résiduelle de T_x sur Δ′ (u′, valeurs des paires) | équivalente au modèle de T (théorème B) |
| sommes en étoile EU = 0 en x et x̄ | redondantes pour les verdicts (B2) |
| coupes réelles de T_x sur Δ′ | équivalentes (§3.3) |
| comptes μ des lointains de T_x, dans Δ′ et dans les 40 lointains communs | ce sont les marges et les comptes proche–lointain de T |

- **Élagage : nul**, au niveau des configurations (noms, R) acceptées.
- Ce que T_x apporte en plus se trouve dans ses 40 lointains extérieurs à N[T] ∪ N[T_x], donc au-delà de la double étoile.

---

## 4. Q4 : conditions globales entre résidus

(a) **Le théorème B avec U = V** se réduit à rang₇(A − 3I) = r. La condition de classe est automatique (proposition 2(a)).
- Toute la famille des résidus est déterminée par A, et cohérente pour tout graphe hypothétique. Cela comprend :
  - leurs classes ;
  - les inclusions C_T ⊂ C₀ ;
  - les intersections C_T ∩ C_T′, qui sont les mots nuls sur N[T] ∪ N[T′] ;
  - les relations en un sommet (au moins 6r − 244 entre les C(Tᵢ), NOTE_BORNE_RANG proposition 7).
- Toute condition qui couple les résidus de droites dont les boules sont dans U découle de (ii) sur U.
- Pour obtenir davantage, il faut agrandir U (c'est l'unité de recherche) ou utiliser la positivité et le caractère 0/1.

(b) **Concordance** avec NOTE_BORNE_RANG §4.2 (le modèle de position générale reproduit toutes les dimensions) et avec
NOTE_ORDRE2 §2.1 (tous les ordres, X ⊂ F).

(c) **Autres pistes examinées, par le raisonnement seul.**
- La trace de la somme des projecteurs sur les C_T vaut 231·2k ≡ 0 (mod 7), puisque 231 = 7·33. Elle est vide.
- Une borne d'Hermite sur 7Λ^# : mon premier essai était faux. Λ^#/Λ a aussi une partie en τ, donc 7Λ^# ⊄ Λ. Je l'ai
  corrigé avant toute conclusion.
- Le côté 3 (Λ₃(T)) donne le même résidu au signe près, car Θ ≡ −τ (A, NOTE_BORNE_RANG §4.3). Aucun bit nouveau.
- La borne de repère Σ_{T≠T′} tr(Π_TΠ_T′) ≥ 75 768 donne une moyenne ≥ 1,43, contre 1,45 pour des 8-plans aléatoires de
  V₋. Aucune tension.

(d) **Conclusion.**
- Aucune condition globale sur les résidus ne peut exclure 39, 41 ou 43, ni rendre ces rangs finis.
- Reste ouvert (X) : savoir si le contenu 0/1 et de positivité d'une unité bornée est UNSAT indépendamment du rang.

---

## 5. Prochaine étape

1. **Immédiat, peu coûteux.** Une seule forme δ par droite équilibrée (§1.6). Quand le calcul reprendra, arrêter les runs
   hors règle. Gain : un facteur 2 sur les types concernés.
2. **Clore les filtres par droites latérales et les combinaisons globales de résidus** (§3 et §4).
3. **Aux rangs 39 à 43, il ne reste que des unités plus grandes et la positivité.**
   - Par B3, un test unique au rang 43 (ρ = 6, bit de classe seulement en cas d'égalité) couvre toute la fenêtre.
   - L'unité naturelle est la double étoile, déjà proposée dans NOTE_BORNE_RANG:459 (A) : « double étoile, rang réel ≤ 8
     exact et 7-rang ≤ 6 ».
   - Le théorème B et le §3.3 en donnent le contenu exact : (noms, R) sur 59 sommets, avec
     - Y ⪰ 0, de rang ≤ 44 ;
     - Y³ ⪰ 0, de rang ≤ 54 ;
     - rang₇ M₅₉ ≤ 43 ;
     - la combinatoire.

     Il n'y a **rien à ajouter** venant de T_x.
   - Avant de l'écrire, mesurer si les étoiles des rangs 41 et 43 survivent (estimation de Knuth, NOTE_ORDRE2 §6). La double
     étoile ne compte que pour les étoiles survivantes. Coût non estimé (X).
4. **Constat honnête.** Les routes droite par droite aux rangs 39 à 43 restent de l'ordre de 10¹¹ droites. Une route finie
   demande un théorème global fondé sur le caractère 0/1, pas sur les résidus.

---

## 6. Contrôles (E) et ce qui n'a pas été vérifié

**Sorties** : `residu_checks_out.json`, copie des fichiers de `scratchpad/boost/runs/`. Graine 20261020, sauf T3
(générateur numpy de graine 7 ; rang 20 à 49, |U| = 5 à 29) et T6 (graine 3).

| test | énoncé | résultat |
|---|---|---|
| T1 | det M[{t₀} ∪ proches] = 144τ, en exact | 150/150 |
| T2, c = 1 | rang 37 et χ(disc_nd M_NN) = (τ\|7) | 129/129 (21 droites avec 7 \| τ écartées ; 58 résidus, 71 non-résidus) |
| T2, blocs | χ = (−1)^{c+1}∏(τᵢ\|7), rang 38 − c | 18+18 : 30/30 ; 12+24 : 25/25 ; 6+30 : 34/34 ; 12+12+12 : 23/23 ; 6+6+24 : 36/36 ; 6+12+18 : 24/24 (cas à torsion écartés : 10, 15, 6, 17, 4, 16) |
| T3 | règle de scindage (rang additif, χ multiplicatif), matrices symétriques aléatoires de 𝔽₇, n = 60 | 215/215 |
| T4 | complément de Schur côté −4 : Bᵀ Y⁺ B = Eᵀ Z E ; bloc de boule semi-défini positif de rang 36 ; image | erreur ≤ 2,0·10⁻¹⁴ ; 20/20 ; 20/20 |
| T5 | e_wᵀ X e_w′ ≡ 4 − e_wᵀ Ω e_w′ (mod 7), soit 7Π_T ≡ −Res_T | 17/17 droites (toutes les paires de 12 vecteurs de noms) |
| T6 | complément de Schur côté 3 | erreur ≤ 9,5·10⁻¹⁵ ; 20/20 ; 20/20 |

**Non vérifié.**
- L'entrée globale c₇(V₋) = −1, équivalente au lemme de TL 17.80 : deux preuves à la main indépendantes, mais aucun graphe
  sur lequel la tester.
- La règle pour les droites à torsion équilibrées (d > c) : elle ne repose que sur la règle générale de scindage (T3).
  Aucun test spécifique.
- Les droites déséquilibrées ne sont pas traitées (règle B′ de TL, A).
- Aucune modification du moteur, aucun run avec un seul δ : les calculs sont suspendus depuis 16:33.
- L'équivalence latérale n'a pas été testée sur une vraie double étoile. Il n'en existe pas : les étoiles meurent aux rangs
  37 et 39. Sa preuve repose sur l'algèbre linéaire et sur les identités T3 à T6.
- Pour le test « 7I − H ⪰ 0 » du moteur, l'indépendance de la base n'est pas affirmée : seulement pour H et H₃.
- La formule du déterminant avec j (RD:21) n'est pas revérifiée. Mes preuves ne l'utilisent pas.

---

## 7. Fichiers

**Dans `merge_2026-10-19/`** :
- `residu_checks.py` : tests T1 à T5 ;
- `residu_checks3.py` : test T6 ;
- `residu_checks_out.json` : les sorties ;
- cette note.

Aucun fichier existant n'a été modifié.
