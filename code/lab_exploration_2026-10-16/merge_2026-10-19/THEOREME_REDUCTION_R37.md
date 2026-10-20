# Théorème de réduction au rang 37 : l'étoile d'un sommet proche, sur les droites à au plus 7 triangles transversaux

LAB, 20/10/2026, après-midi. Demande : énoncé et preuve autonomes de la réduction « si tout graphe de droite admissible
à c ≤ 4 échoue au test d'étoile de rang 37, alors r ≠ 37 », statut de chaque maillon, audit du code ligne à ligne.

**Statuts.** Aucun n'est monté.
- **P** : prouvé dans cette note. Preuve écrite à la main, **non relue par un tiers**.
- **A** : archive, avec fichier:ligne. Le statut d'origine est rappelé.
- **E** : calcul exact reproductible, sans certificat exporté (programme maison, non audité).
- **X** : ouvert.

Les fichiers cités sans chemin sont dans `work/exploration_2026-10-16/merge_2026-10-19/`. Les calculs de contrôle
faits pour cette note sont au §8.

NOTE_BOOST a été modifiée par un autre agent pendant la rédaction. Ses numéros de ligne renvoient à sa version de
15 h 45.

---

## 0. En bref

**Théorème 6.1** (P, conditionnel au Lemme 2.2 « P ≤ 852 », de statut A + E).
- *Hypothèse (H₃₇).* Pour tout graphe de droite admissible G ayant au plus 7 triangles transversaux, il existe un
  sommet x ∈ C₀ hors de tout triangle transversal tel que, pour **chaque** variante v ∈ 𝒱₃₇(G), le système d'étoile
  𝒮(G, x, v) n'a pas de solution. Les variantes sont : forme du résidu δ, cas équilibré ou déséquilibré, direction de
  torsion.
- *Conclusion.* Alors aucun srg(99,14,1,2) n'a rang₇(A − 3I) = 37.
- La forme demandée, « tout G_T admissible à c ≤ 4 », en découle (Corollaire 6.2). En effet, t ≤ 7 entraîne c ≤ 4
  et l'existence de x.

**Établi ici (P).**
- m ≤ 4, sous une forme plus précise : au moins 18 droites ont t ≤ 7, et chacune a c ≤ 4 (§2). La seule entrée est
  P ≤ 852.
- La décomposition r = 38 − d + 2 r(T) + ρ(T), avec 0 ≤ r(T) ≤ d − c, pour toute droite (§3).
- Les encodages du résidu, y compris pour r(T) ≥ 2, et la liste exacte des variantes au rang 37 (§3.6,
  Définition 3.7).
- La nécessité de chaque contrainte du test, projecteur lointain réel compris (§4).
- La validité des trois raccourcis du moteur : réduction par O(D), règle b₁, découpage par direction de torsion (§5).

**Non établi (X).** Que l'hypothèse du théorème soit vraie. Il manque trois choses (§7) :
- l'énumération complète des classes ;
- la couverture de tous les types (c, d) :
  - rien n'existe pour d ≥ 5 ;
  - (1,4) et (2,4) n'ont aucun générateur d'instances ;
  - (4,4) n'a encore aucun résultat ;
  - (3,4) est partiel : 6 droites avec filtre, et en exacte seule les seules variantes équilibrées d'une droite ;
- la certification des verdicts UNSAT.

**Code et mathématiques (§5.9).**
- Les contraintes exactes sont fidèles, ligne par ligne.
- Le filtre réel et les tests de feuille sont en flottant, avec des tolérances absolues : ce n'est pas une preuve.
- Aujourd'hui, 25 runs relancés sans aucun flottant, sur 7 types (c, d), restent tous UNSAT (E, §8.3 et §8.4). La
  correction est donc simple.

**Relecture (§8.7).** Un relecteur en contexte neuf n'a trouvé aucune erreur mathématique. Il a relevé des défauts de
citation et de preuve d'appui, tous corrigés.

**Nouveau par rapport à NOTE_BOOST §7 (version de 15 h 45, l. 232-239).** NOTE_BOOST passait par l'exclusion de m = 4 (verdicts CP-SAT
sans certificat) et énonçait la réduction pour c ≤ 3. La version d'ici n'utilise ni CP-SAT ni le registre m = 3. Elle
évite aussi un trou de cette formulation : une droite à c ≤ 3 peut avoir t = 12, et alors aucun x n'est utilisable par
le moteur (§6.4).

---

## 1. Définitions et notations

### 1.1 Le graphe

- Γ est un srg(99,14,1,2) de matrice A. Donc A² = 14I + A + 2(J − I − A) = 12I − A + 2J.
- Valeurs propres : 14 (simple), 3 (multiplicité 54), −4 (multiplicité 44).
- On pose M := A − 3I, vue sur F₇, et r := rang₇ M. Comme −4 ≡ 3 (mod 7), M est aussi A + 4I mod 7.

### 1.2 Droites, classes, graphe de droite

**Droites.**
- Par λ = 1, toute arête est dans un unique triangle. Les triangles sont les **droites** : 7 par sommet, 231 en tout.
- On fixe une droite T = {t₀, t₁, t₂}. On pose C_i := N(t_i) ∖ T (12 sommets) et N(T) := C₀ ∪ C₁ ∪ C₂.
- On note N := T ∪ N(T) (39 sommets) et F := V ∖ N, l'ensemble des **lointains** (60 sommets).

**Partenaires.**
- Le partenaire x̄ de x ∈ C_i est le troisième point de la droite t_i x. On étiquette C_i = {(i, a) : 0 ≤ a ≤ 11}, avec
  (i, a) et (i, a ⊕ 1) partenaires.
- Pour x ∈ C₀, on note b₁(x) et b₂(x) ses voisins dans C₁ et C₂. Ils existent et sont uniques (Lemme 4.1).

**Graphe de droite.**
- G = G_T est le graphe induit sur N(T). Il est cubique (Lemme 4.1) : 18 arêtes partenaires plus trois bijections
  s₀₁ : C₀ → C₁, s₁₂ : C₁ → C₂ et s₂₀ : C₂ → C₀.
- Abstraitement, un **graphe de droite étiqueté** est un triple (s₀₁, s₁₂, s₂₀) ∈ S₁₂³. On lui associe le graphe G
  (partenaires (i, a)–(i, a ⊕ 1) et les trois bijections) et la matrice
  K := 12I − G − G² + 2J − J_cl (36 × 36),
  où J_cl est l'indicatrice « même classe ».
- G est **admissible** si K ≥ 0 coefficient par coefficient.

**Invariants.**
- t(G) : nombre de triangles de G. Ils sont tous transversaux et disjoints deux à deux (Lemme 2.1).
- c(G) : nombre de composantes connexes.
- d(G) := dim ker₇(3I − G).
- τ(G) : nombre d'arbres couvrants.
- U := vect(1_{C₀}, 1_{C₁}, 1_{C₂}), et U^⊥ l'espace des vecteurs de sommes de classe nulles (sur F₇ ou sur ℝ selon le
  contexte).

**Ré-étiquetages.** Λ := (S₂ ≀ S₆)³ ⋊ S₃ est le groupe des ré-étiquetages qui préservent les paires partenaires et
permutent les classes. Son ordre est (2⁶·6!)³·6 ≈ 5,87·10¹⁴.

### 1.3 Lointains, noms, étoile

- Pour w ∈ F et chaque i, p_i(w) := N(w) ∩ C_i est une paire non partenaire (Lemme 4.1).
- Les **noms** de w sont W(w) := p₀(w) ∪ p₁(w) ∪ p₂(w) (6 sommets).
- On note e_w := 1_{W(w)} ∈ {0,1}³⁶, et ê_w ∈ F₇³⁹ le même vecteur prolongé par 0 sur T.
- E (36 × 60) est la matrice des colonnes e_w, et R (60 × 60) l'adjacence de Γ sur F.
- P_i est l'ensemble des 60 paires non partenaires de C_i.
- Pour x ∈ C₀, l'**étoile** de x est star(x) := {w ∈ F : w ∼ x}.

### 1.4 Bloc proche, noyau, résidu

- M_NN (39 × 39), M_NF = M_FNᵀ (39 × 60) et M_FF = R − 3I. La colonne w de M_NF est ê_w, car un lointain n'a aucun voisin
  dans T.
- k := ker₇ M_NN, de dimension d + 1 (Lemme 3.1). On fixe une base (κ_l) de k et on pose
  ek(w) := (ê_w · κ_l)_l ∈ F₇^{d+1}. Dans le code : `ek = (e @ ker) % 7`.
- X est un g-inverse **réflexif symétrique** de M_NN (M X M = M, X M X = X, Xᵀ = X). On pose β_X(w, w') := ê_wᵀ X ê_{w'}.
- **Partie déséquilibrée** : r(T) := dim M_FN(k). On pose F₀ := (M_FN k)^⊥ ⊂ F₇⁶⁰.
- Q_X := (R − 3I) − (β_X(w, w'))_{w,w'}. Le **résidu** est Res_T := Q_X restreint à F₀ × F₀ ; il ne dépend pas de X
  (Lemme 3.2).
- ρ(T) := rang Res_T. Si ρ ≥ 1, δ(T) ∈ {1, 3} désigne la classe du discriminant de sa partie non dégénérée.
- La droite est **équilibrée** si r(T) = 0.

### 1.5 Objets réels

- L := 3I − G + J, sur ℝ. P_ker est le projecteur orthogonal sur ker L : les différences de composantes, de dimension
  c − 1, ou 0 si c = 1 (Théorème 4.3).
- Z := (L + P_ker)⁻¹. Si c = 1, Z = L⁻¹.
- H := 3I − R − EᵀZE + J/9 (60 × 60).
- Π_T est le projecteur orthogonal sur E₋₄(Γ) ∩ ℝ^F, les vecteurs propres −4 de Γ portés par F.
- Si d = 1 : Ω := L⁻¹ mod 7. Il existe, car det L = 36²τ ≡ τ (mod 7) (théorème des arbres couvrants, 36² ≡ 1).

---

## 2. Lemme m ≤ 4, sous la forme t ≤ 7

**Lemme 2.1 (P).** Soit P le nombre de 6-parties de Γ qui induisent un prisme K₃ × K₂. Alors Σ_T t(G_T) = 2P. De plus,
les triangles de G_T sont transversaux, c'est-à-dire qu'ils ont un sommet par classe, et ils sont deux à deux
disjoints.

*Preuve.*
1. **Les triangles sont transversaux.** Un triangle de G contenant une arête partenaire {u, ū} ⊂ C_i aurait un
   troisième sommet voisin de u et de ū. C'est impossible : un sommet d'une autre classe a un seul voisin dans C_i
   (Lemme 4.1), et u n'a pas d'autre voisin que ū dans C_i.
2. **Ils sont disjoints.** Un sommet a un seul voisin dans chaque autre classe, donc il est dans au plus un triangle
   transversal.
3. **Un triangle transversal donne un prisme induit.** Soit Δ = {a, b, c} un triangle transversal (a ∈ C₀, b ∈ C₁,
   c ∈ C₂). Le sous-graphe induit par T ∪ Δ est un prisme : les arêtes sont celles de T, de Δ, et t₀a, t₁b, t₂c. Il
   n'y en a pas d'autre : si a ∼ t₁, alors t₀ et t₁ auraient deux voisins communs, t₂ et a, contre λ = 1.
4. **Un prisme induit donne un triangle transversal.** Dans un prisme induit de triangles T et Δ, chaque sommet de Δ a
   exactement un voisin dans T, et ces voisins sont distincts. Donc Δ est un triangle transversal de G_T.
5. **Décompte.** Un prisme a exactement deux triangles, et chacun joue une fois le rôle de T. ∎

**Lemme 2.2 (A + E).** Dans tout srg(99,14,1,2), P ≤ 852.
- **Source A** : AUDIT_EXCLUSIONS_2026-10-18.md §8, l. 211-238, et §4, l. 145 ; NOTE_MANDAT_REPRESENTATION §1.2,
  l. 76.
- **Contenu.** Le recensement d'ordre 9 exprime le nombre N_H de 9-parties qui induisent chaque type H comme une forme
  affine en 57 paramètres. Le paramètre P est le nombre de prismes induits (NOTE_TRESOR §2.1, l. 75-76). Les comptes
  d'un ordre somment à C(99, n) (AUDIT l. 230) : ce sont donc des comptes de parties, et le P du certificat est bien
  celui du Lemme 2.1.
- **Certificat.** 16 poids w_H ≥ 0 tels que Σ w_H N_H = 11088/13 − P identiquement. Comme N_H ≥ 0, on obtient
  P ≤ 852,92, donc P ≤ 852.
- **Contrôles archivés.**
  - Le certificat a été vérifié exactement sur deux implantations indépendantes du recensement : celle de Codex et
    `census2.py` (LAB), avec 0 désaccord sur 6 533 formules (AUDIT l. 231).
  - Le programme linéaire a été refait (l. 233).
- **Relance du 20/10 (E, §8.1).** `p852_identity.py` répond `IDENTITY 11088/13 - P: True`. Les empreintes SHA256 sont
  inchangées : a4816605…59a1 pour le certificat, a49f811e…a291 pour le recensement.
- **Sur quoi cela repose.** La dérivation du recensement est un système d'identités de double comptage engendré par
  programme. Il y a deux programmes indépendants, mais pas de preuve à la main. Le contrôle positif sur srg(243,22,1,2)
  ne teste que les coefficients des paramètres non nuls dans ces graphes (AUDIT l. 221-224).

**Lemme 2.3 (P, sous 2.2).**
- Au moins 18 droites de Γ vérifient t(G_T) ≤ 7.
- Pour une telle droite, (i) c(G_T) ≤ 4 et (ii) chaque classe contient au moins 5 sommets hors de tout triangle
  transversal.
- Enfin, G_T est admissible.

*Preuve.*
1. **Les 18 droites.** Par 2.1 et 2.2, Σ_T t(T) ≤ 1704. Si au plus 17 droites avaient t ≤ 7, les 214 autres
   donneraient Σ t ≥ 8·214 = 1712 > 1704.
2. **Taille des composantes.** Une composante C de G est stable par partenaire, donc |C ∩ C_i| est pair. La bijection
   s₀₁ envoie C ∩ C₀ sur C ∩ C₁, et de même pour les autres. Donc |C ∩ C_i| = 2k pour chaque i, et |C| = 6k.
3. **Composantes à 6 sommets.** Une telle composante contient {a, ā}, {b, b̄} et {c, c̄}. Les six arêtes de
   bijection y forment un 2-facteur tripartite : soit deux triangles, soit un 6-cycle.
   - Deux triangles plus les partenaires donnent un prisme.
   - Dans un 6-cycle, deux sommets d'une même classe ne sont pas à distance 2 : leur voisin commun aurait deux voisins
     dans cette classe. Ils sont donc antipodaux, et le 6-cycle plus les partenaires donne K₃,₃. Dans K₃,₃, deux
     sommets non adjacents de classes différentes ont 3 voisins communs, donc K(·,·) = 2 − 3 < 0 : ce cas est exclu.
   - Une composante à 6 sommets est donc un prisme, qui porte 2 triangles transversaux.
4. **c ≤ 4.** Soit g le nombre de ces composantes. Alors 2g ≤ t ≤ 7, donc g ≤ 3. Les c − g autres composantes ont au
   moins 12 sommets, donc 6g + 12(c − g) ≤ 36, soit c ≤ 3 + g/2, d'où c ≤ 4.
5. **Sommets hors triangle.** Au plus t ≤ 7 triangles disjoints, chacun ayant un sommet par classe : au moins
   12 − 7 = 5 sommets de chaque classe sont hors triangle.
6. **Admissibilité.** K(u, v) compte les lointains voisins de u et de v (Théorème 4.3, (I1)), donc K ≥ 0. ∎

*Remarque.* La liste à énumérer peut donc se limiter aux G admissibles avec t ≤ 7, ce qui force c ≤ 4. Les profils de
composantes possibles sont :
- c = 1 : 36 ;
- c = 2 : 18 + 18, 12 + 24, 6 + 30 ;
- c = 3 : 12 + 12 + 12, 6 + 12 + 18, 6 + 6 + 24 ;
- c = 4 : 6 + 6 + 12 + 12 (g = 2, t ≥ 4) et 6 + 6 + 6 + 18 (g = 3, t ≥ 6).

Pour un graphe uniforme, E[t] = 1 (12 sommets de C₀, chacun dans un triangle avec probabilité 1/12). La restriction
t ≤ 7 retire donc peu de graphes. Elle sert surtout à la logique : elle garantit x et élimine c ≥ 5.

---

## 3. Décomposition du rang et variantes au rang 37

### 3.1 Le noyau du bloc proche

**Lemme 3.1 (P).** rang₇ M_NN = 38 − d, et

    k = ker M_NN = vect{κ₀₁, κ₁₂} ⊕ {(0_T, z) : z ∈ ker₇(3I − G) ∩ U^⊥},

où κ_{ij} := −4(e_{t_i} − e_{t_j}) + (1_{C_i} − 1_{C_j}). En particulier dim k = d + 1.

*Preuve.*
1. **Élimination de T.** Par blocs, M_NN = [[J₃ − 4I, B], [Bᵀ, G − 3I]], avec B_{t_i,v} = [v ∈ C_i]. Mod 7,
   (J₃ − 4I)⁻¹ = 5(I + J₃). En effet, (J₃ − 4I)(I + J₃) = −4I + (1 + 3 − 4)J₃ = −4I, et 5·(−4) = −20 ≡ 1. Le complément
   de Schur est
   Σ = G − 3I − 5Bᵀ(I + J₃)B = G − 3I + 2J_cl + 2J,
   car BᵀB = J_cl et BᵀJ₃B = J. Donc rang M_NN = 3 + rang Σ.
2. **Σ est diagonal par blocs.** La Gram des 1_{C_i} vaut 12 I₃ ≡ 5 I₃, qui est inversible. Donc F₇³⁶ = U ⊕ U^⊥. Σ
   préserve U et U^⊥ : G 1_{C_i} = 𝟏, et J, J_cl envoient tout dans U et tuent U^⊥.
3. **Σ sur U.** Σ1_{C_i} = 𝟏 − 3·1_{C_i} + 24·1_{C_i} + 24·𝟏 ≡ 4·𝟏. Le noyau est formé des différences de classes,
   de dimension 2.
4. **Σ sur U^⊥.** Σ = G − 3I. L'opérateur 3I − G préserve U et U^⊥. Sur U, dans la base (1_{C_i}), G agit comme J₃ : la
   valeur propre est 0 sur 𝟏 et 3 ≢ 0 sur les différences. Donc ker(3I − G) ∩ U = vect(𝟏), et dim(ker(3I − G) ∩ U^⊥)
   = d − 1.
5. **Bilan.** dim ker Σ = d + 1, rang Σ = 35 − d, et rang M_NN = 38 − d.
6. **Relèvement.** z_T = −5(I + J₃)Bz_N.
   - Pour z_N = 1_{C_i} − 1_{C_j} : Bz_N = 12(e_i − e_j), d'où z_T = −60(e_i − e_j) ≡ −4(e_i − e_j).
   - Pour z_N ∈ U^⊥ : Bz_N = 0, donc z_T = 0. ∎

*Contrôle (E, A).* `star_prep_gen.py` l. 127-128 vérifie rang M_NN = 38 − d à chaque exécution. L'assertion ne s'est
jamais déclenchée, ni sur les 260 runs `gen37_*` du §8.2, ni sur les 25 runs exacts du §8. En revanche, les runs (1,1)
de `cost37*` passent par `star39_prep.py` (forme Ω), qui ne construit pas M_NN : ils n'ont pas ce contrôle.

### 3.2 La formule de rang

**Lemme 3.2 (P).** Soit 𝕂 un corps de caractéristique ≠ 2 et S = [[A, B], [Bᵀ, D]] symétrique. On note
- k = ker A ;
- X un g-inverse réflexif symétrique de A ;
- W := Bᵀk ;
- Q := D − BᵀXB.

Alors Q|_{W^⊥} ne dépend pas de X, et

    rang S = rang A + 2 dim W + rang(Q|_{W^⊥}).

*Preuve.*
1. **Q|_{W^⊥} ne dépend pas de X.** Soit f ∈ W^⊥. Alors Bf ⊥ k = (Im A)^⊥, car A est symétrique, donc Bf = Ag pour un
   certain g. Pour f, f' ∈ W^⊥, fᵀBᵀXBf' = gᵀAXAg' = gᵀAg'. Cette quantité ne dépend pas de X.
2. **Première décomposition.** Soit C un supplémentaire de k. A|_C est non dégénérée, donc 𝕂^{N⊔F} = C ⊕ C^{⊥_S} et
   rang S = rang A + rang S|_{C^⊥}.
3. **Base de C^⊥.** Pour f ∈ 𝕂^F, soit Y f l'unique élément de C tel que cᵀA(Yf) = cᵀBf pour tout c ∈ C. Alors
   C^⊥ = k ⊕ {(−Yf, f)}.
4. **Gram sur C^⊥.** Dans cette base, la Gram vaut [[0, B_k], [B_kᵀ, Q′]], avec B_k = (κᵀBf)_{κ,f}, de rang dim W, et
   Q′(f, f') = fᵀDf' − fᵀBᵀYf'.
   - Pour f ∈ W^⊥, on a AYf = Bf. En effet, A(Yf − g) est orthogonal à C et à k, donc nul. Ainsi Q′ = Q sur W^⊥.
5. **Scindage hyperbolique.** Soient κ₁, …, κ_w des éléments de k dont les images Bᵀκ_i forment une base de W, et
   f₁, …, f_w duaux (κ_iᵀBf_l = δ_il). Ces 2w vecteurs engendrent un sous-espace non dégénéré, de Gram
   [[0, I], [I, ∗]]. Son orthogonal est formé des f − Σ_l S(f, f_l)κ_l, pour f ∈ W^⊥ ; la forme y vaut Q|_{W^⊥}. Les
   autres vecteurs de k sont dans le radical. ∎

*Contrôles.* `schur_check.py` : 300 matrices aléatoires sur F₇, 0 écart (A : NOTE_FUSION R5, l. 71-74, statut E).
L'identité est celle de Codex (notes 124 à 127, A).

### 3.3 Quels vecteurs du noyau sont tués

**Lemme 3.3 (P).** (M_FN κ)_w = ê_w · κ. Les vecteurs κ₀₁, κ₁₂ et les c − 1 différences de composantes sont tués par
M_FN. Donc r(T) ≤ d − c.

*Preuve.*
1. **κ_{ij}.** e_w · (1_{C_i} − 1_{C_j}) = 2 − 2 = 0, et ê_w est nul sur T.
2. **Différences de composantes.** Soient deux composantes C, C′ de tailles 6k, 6k′. Le vecteur v := k′1_C − k1_{C′}
   est dans ker(3I − G), car les composantes sont cubiques. Il est dans U^⊥ : ses sommes de classe valent
   2kk′ − 2kk′ = 0. Par L4 (Théorème 4.3 (e)), e_w · v = k′k − kk′ = 0.
3. **Indépendance.** Les c − 1 vecteurs k₀1_C − k1_{C₀} (C ≠ C₀) sont indépendants mod 7, car k₀ ∈ {1, …, 6}.
4. **Majoration.** Il reste au plus (d + 1) − 2 − (c − 1) = d − c directions qui peuvent ne pas être tuées. ∎

**Corollaire 3.4 (P).** Pour toute droite :

    r = 38 − d + 2 r(T) + ρ(T),    0 ≤ r(T) ≤ d − c.

**Au rang 37 : 2 r(T) + ρ(T) = d − 1.**

*Preuve.* On applique 3.2 à S = M, A = M_NN, B = M_NF et D = R − 3I. Alors W = M_FN k, Q = Q_X, et rang A = 38 − d par
3.1. ∎

*Remarque.*
- d − c est le 7-rang du groupe critique, le produit des « sandpile » des composantes.
- d = c équivaut à 7 ∤ Π τ(C_i).
- Pour c = 1, d = 1 équivaut à 7 ∤ τ.

### 3.4 Encodage du résidu

**Proposition 3.5 (P).** On pose j := r(T) et Δ_T := vect{ek(w) : w ∈ F} ⊂ F₇^{d+1}. Alors :

**(a)** dim Δ_T = j. Soit (g₁, …, g_j) une base de Δ_T ; on écrit ek(w) = Σ_i b_i(w) g_i. Alors M_FN k = vect(b₁, …, b_j)
et F₀ = {f : b_i · f = 0 pour tout i}.

**(b)** Il existe c₁, …, c_j ∈ F₇⁶⁰ et U ∈ F₇^{60×ρ} tels que

    R − 3I = (β_X(w, w'))_{w,w'} + Σ_i (b_i c_iᵀ + c_i b_iᵀ) + U D_{ρ,δ} Uᵀ,    D_{ρ,δ} := diag(1, …, 1, δ),

avec δ = δ(T) si ρ ≥ 1.

**(c)** On pose u_w := (b(w), c(w), U_w) et q(u, u') := Σ_i (b_i c'_i + c_i b'_i) + vᵀD v'. Alors :
- pour w ≠ w' : R(w, w') ≡ β_X(w, w') + q(u_w, u_{w'}) (mod 7) ;
- sur la diagonale : q(u_w, u_w) = −3 − β_X(w, w).

**(d)** Cas j = 1, celui du code. L'encodage (b + c, b − c) avec diag(4, 3) donne
4(b + c)(b′ + c′) + 3(b − c)(b′ − c′) = 7bb′ + bc′ + cb′ + 7cc′ ≡ bc′ + cb′. Sur la diagonale, cela vaut 2bc.

*Preuve.*
- **(a)** La matrice 60 × (d + 1) de coefficients ek(w)_l = ê_w · κ_l = (M_FN κ_l)_w a pour espace colonne M_FN k et
  pour espace ligne Δ_T. On a M_FN κ_l = Σ_i (g_i)_l b_i, avec (g_i) libre.
- **(b), partie résiduelle.** Sur F₇, une forme symétrique est classée par son rang et par la classe de son
  discriminant (corps fini de caractéristique impaire). Il existe donc φ : F₀ → F₇^ρ linéaire avec
  Res_T(f, f') = φ(f)ᵀ D φ(f'). On la prolonge en U : F₇⁶⁰ → F₇^ρ.
- **(b), partie hyperbolique.** Q′ := Q_X − UDUᵀ s'annule sur F₀ × F₀. Soient f₁, …, f_j avec b_i · f_l = δ_il. On
  pose c_i := Q′f_i − ½ Σ_l Q′(f_i, f_l) b_l. On décompose f = Σ_i (b_i · f) f_i + f⁰, avec f⁰ ∈ F₀, et de même f′.
  Un calcul direct donne Q′(f, f′) = Σ_i [(b_i · f)(c_i · f′) + (c_i · f)(b_i · f′)].
- **(c)** C'est (b) lu coefficient par coefficient, avec R(w, w) = 0. ∎

*Lecture.*
- Dans tous les cas, u_w a 2j + ρ = d − 1 coordonnées au rang 37 (`star_prep_gen.py` l. 118 : `rho = r - 38 + d`).
- Les coordonnées b sont **fixées par G** : ce sont les coordonnées de ek(w) dans la base de Δ. Les coordonnées c et v
  sont libres, sous la contrainte diagonale.

### 3.5 Forme de Green (droite générique)

**Proposition 3.6 (P ; A : PROMPT_CHATGPT_CORE37 §3, l. 112-134 ; Codex, note 124).** Supposons d = 1. Alors
β_X(w, w') ≡ 4 − e_wᵀΩe_{w'} pour tous w, w' ∈ F et tout X. Au rang 37 (ρ = 0) :
- R(w, w') ≡ 4 − e_wᵀΩe_{w'} pour w ≠ w' ;
- e_wᵀΩe_w ≡ 0.

*Preuve.*
1. **Indépendance de X.** Par 3.3, ê_w ⊥ k, donc ê_w ∈ Im M_NN : β ne dépend pas de X.
2. **Identités sur Ω.** L𝟏 = 36·𝟏 ≡ 𝟏, donc Ω𝟏 = 𝟏. On vérifie L(𝟏 + 5·1_{C_i}) ≡ 1_{C_i}, d'où Ω1_{C_i} = 𝟏 + 5·1_{C_i}.
   Donc 1_{C_i}ᵀΩe = 6 + 10 ≡ 2 pour e de sommes de classe (2, 2, 2).
3. **Solution du système.** x := −Ωe + 3·𝟏 vérifie Σx = e. En effet, Σ = −L + 3J + 2J_cl, avec −L x = e − 3·𝟏,
   3Jx ≡ 5·𝟏 et 2J_cl x ≡ 5·𝟏.
4. **Conclusion.** β(w, w') = e_{w'}ᵀx = −e_{w'}ᵀΩe_w + 18 ≡ 4 − e_{w'}ᵀΩe_w. On applique ensuite 3.5 (c) avec u = (). ∎

*Contrôles (A, E).*
- `omega_check.py` : 0 écart sur 6 000 tests (NOTE_FUSION R5, l. 63-68).
- `check_identities.py`.
- NOTE_BOOST §2.2, l. 131-136 : `star39_prep.py` (Ω) et `star_prep_gen.py` (X) donnent les mêmes candidats et les mêmes
  nœuds.
- §8.3 (E) : sans filtre réel, `star_prep_gen.py` donne pour la graine 1 exactement les tailles de domaines de
  `star_csp.py` (Ω, code Python indépendant).

### 3.6 Les variantes au rang 37

**Définition 3.7.** Pour G admissible d'invariants (c, d), 𝒱₃₇(G) est l'ensemble des quadruplets (j, ρ, δ, Δ) tels
que :
- **(j, ρ)** : j ∈ ℕ, j ≤ d − c, 2j ≤ d − 1 et ρ = d − 1 − 2j ;
- **δ** : δ ∈ {1, 3} si ρ ≥ 1, et δ = ∗ si ρ = 0 ;
- **Δ** : un sous-espace de dimension j de F₇^{d+1}. Pour j = 1, c'est une droite F₇g.

*Option L23* (A, non auditée, §7.4) : on pose 𝒱₃₇(G) = ∅ si c = d = 1 et (τ | 7) = +1. **Elle n'est pas utilisée par
le Théorème 6.1.**

**Proposition 3.8 (P).** Si Γ est de rang 37, v_true := (r(T), ρ(T), δ(T), Δ_T) ∈ 𝒱₃₇(G_T).

*Preuve.* Corollaire 3.4 et Proposition 3.5 (a). ∎

**Table des variantes pour c ≤ 4** (P pour l'arithmétique ; la couverture logicielle est détaillée au §7.2).

| (c, d) | (j, ρ) possibles | coordonnées de u | variantes par droite |
|---|---|---:|---|
| (1, 1) | (0, 0) | 0 | 1 |
| (1, 2) | (0, 1) seul : j = 1 donnerait ρ = −1 | 1 | 2 (δ) |
| (1, 3) | (0, 2), (1, 0) | 2 | 2 (δ) + 1 par droite Δ (8 si l'espace des ek est de dimension 2) |
| (1, 4) | (0, 3), (1, 1) | 3 | 2 + 2 par Δ |
| (1, d ≥ 5) | (0, d − 1), (1, d − 3), (2, d − 5), … | d − 1 ≥ 4 | — |
| (2, 2) | (0, 1) | 1 | 2 |
| (2, 3) | (0, 2), (1, 0) | 2 | 2 + 1 par Δ |
| (2, 4) | (0, 3), (1, 1) | 3 | 2 + 2 par Δ |
| (2, d ≥ 5) | idem, j ≤ d − 2 | ≥ 4 | — |
| (3, 3) | (0, 2) | 2 | 2 |
| (3, 4) | (0, 3), (1, 1) | 3 | 2 + 2 par Δ |
| (3, 5) | (0, 4), (1, 2), (2, 0) | 4 | — |
| (3, d ≥ 6) | (0, d − 1), (1, d − 3), …, avec j ≤ min(d − 3, (d − 1)/2) | d − 1 ≥ 5 | — |
| (4, 4) | (0, 3) | 3 | 2 |
| (4, 5) | (0, 4), (1, 2) | 4 | — |
| (4, 6) | (0, 5), (1, 3), (2, 1) | 5 | — |
| (4, d ≥ 7) | (0, d − 1), (1, d − 3), …, avec j ≤ min(d − 4, (d − 1)/2) | d − 1 ≥ 6 | — |

Règle générale : (j, d − 1 − 2j) pour 0 ≤ j ≤ min(d − c, ⌊(d − 1)/2⌋), et u a toujours d − 1 coordonnées.

La table est d'accord avec NOTE_FUSION §1.4 (l. 106-122) et NOTE_BOOST §3 (l. 164-189). Elle complète NOTE_BOOST §7
(l. 269-278), qui oublie le type (1, 4) : il n'est ni dans la liste « couvert » ni dans la liste « non couvert ».

---

## 4. Conditions nécessaires sur l'étoile de x

Dans tout ce paragraphe, Γ est un srg(99,14,1,2), T une droite, G = G_T et x ∈ C₀.

**Lemme 4.1 (structure ; P).**
- (a) Les C_i sont deux à deux disjoints. G est cubique : une arête partenaire, plus un voisin dans chacune des deux
  autres classes.
- (b) Tout w ∈ F a exactement 2 voisins dans chaque C_i, non partenaires.
- (c) Pour chaque i, w ↦ p_i(w) est une bijection de F sur P_i.
- (d) star(x) = {w_y : y ∈ C₀ ∖ {x, x̄}}, avec p₀(w_y) = {x, y}. Les 10 paires q_y := p₁(w_y) sont distinctes, et de
  même les 10 paires s_y := p₂(w_y).

*Preuve.*
- **(a)** Un sommet de C_i ∩ C_j serait un second voisin commun de t_i et t_j. Soit u ∈ C_i.
  - λ(u, t_i) = 1 : le voisin commun est ū ∈ C_i, et c'est le seul voisin de u dans C_i.
  - μ(u, t_j) = 2 : les voisins communs sont t_i et un unique sommet de C_j (u ≁ t_k).
- **(b)** μ(w, t_i) = 2, et w ≁ t_j, t_k : les deux voisins communs sont dans C_i. S'ils étaient partenaires u, ū,
  alors u et ū auraient pour voisins communs t_i et w, contre λ = 1.
- **(c)** Soient u, v ∈ C_i non partenaires.
  - Ils ne sont pas adjacents, puisque le seul voisin de u dans C_i est ū.
  - Leurs voisins communs : t_i, aucun dans N(T) (leurs voisins dans C_j sont distincts par bijection, et ū ≁ v), donc
    exactement un lointain.
  - L'application est injective : sinon trois voisins communs.
  - |P_i| = 66 − 6 = 60 = |F|, donc elle est bijective.
- **(d)** C'est (c) pour i = 0. Les autres bijections donnent les q_y et s_y distincts. ∎

**Lemme 4.2 (L2, L3 ; P ; A : NOTE_REDUCTION §2.2).**
- Pour v ∈ N(T) et w ∈ F : |N_G(v) ∩ W(w)| ≤ 2 − [v ∈ W(w)].
- Pour w ≠ w' ∈ F : |W(w) ∩ W(w')| ≤ 2 − R(w, w').

*Preuve.* Les voisins communs de v et w qui sont proches forment exactement N_G(v) ∩ W(w), car w n'a pas de voisin dans
T. Ceux de w et w' qui sont proches forment W(w) ∩ W(w'). On conclut par λ = 1 et μ = 2. ∎

**Théorème 4.3 (cadre lointain ; P ; A : NOTE_MANDAT_REPRESENTATION §4, l. 219-274 ; NOTE_BOOST §2.3, l. 138-162 ;
NOTE_OBSTRUCTION §1.1, l. 58-76).**

**(I) Identités.**
- (I1) EEᵀ = K ;
- (I2) ER = 2J − E − GE ;
- (I3) R² + R + EᵀE = 12I + 2J.

**(e) L4.** Pour toute composante C de G et tout w ∈ F, |W(w) ∩ C| = |C|/6.

**(f) Spectre.** rang E = 35 − c. R préserve ker E, de dimension 25 + c. Sur ker E, les valeurs propres de R sont 3, de
multiplicité 18, et −4, de multiplicité 7 + c.

**(g)** E₋₄(Γ) ∩ ℝ^F = E₋₄(R) ∩ ker E. Cet espace est de dimension 7 + c.

**(h) Projecteur.** H = 7Π_T. Donc H² = 7H, 0 ⪯ H ⪯ 7I et rang H = 7 + c.

**(i) Étoile.** H 𝟏_{star(x)} = 0.

*Preuve.*

**(I)** On restreint A² = 12I − A + 2J aux blocs (N(T), N(T)), (N(T), F) et (F, F). Les voisins communs se trouvent :
- dans T : J_cl pour le premier bloc, rien pour les deux autres ;
- dans N(T) : G², GE, EᵀE ;
- dans F : EEᵀ, ER, R².

**(K) Spectre de K** (étape auxiliaire).
- K vaut 60 sur 𝟏 et 0 sur les différences de classes.
- Sur Y := U^⊥ (réel), K = (3I − G)(4I + G).
- Les valeurs propres de G sont ≥ −3, donc 4I + G ≻ 0.
- Donc ker K = {différences de classes} ⊕ (Y ∩ E₃(G)). L'espace Y ∩ E₃(G) est engendré par les c − 1 différences de
  composantes.

**(e)** y := 1_C − (|C|/36)𝟏 est dans Y ∩ E₃(G). Donc ‖Eᵀy‖² = yᵀKy = 0. Comme Eᵀ𝟏 = 6·𝟏_F, on obtient
|W(w) ∩ C| = |C|/6.

**(f)**
1. Par (K), rang E = rang K = 36 − 2 − (c − 1) = 35 − c, donc dim ker E = 25 + c.
2. Pour f ∈ ker E, 𝟏ᵀf = (1/6)𝟏ᵀEf = 0. Par (I2), ERf = 0, donc R préserve ker E. Par (I3), R² + R = 12 sur ker E : les
   valeurs propres y sont 3 et −4, de multiplicités a et b avec a + b = 25 + c.
3. Sur Im Eᵀ, R agit comme suit :
   - R Eᵀy = −(1 + θ)Eᵀy pour y ∈ Y ∩ (diff. comp.)^⊥ avec Gy = θy (par (I2)) ;
   - R𝟏_F = 8·𝟏_F.
4. On a tr(G | Y ∩ (diff. comp.)^⊥) = −3 − 3(c − 1) = −3c, sur un espace de dimension 34 − c. Donc
   tr(R | Im Eᵀ) = 8 − (34 − c) + 3c = 4c − 26.
5. Comme tr R = 0, on a 3a − 4b = 26 − 4c. D'où b = 7 + c et a = 18.

**(g)** Soit f ∈ ℝ^F prolongé par 0 à V. Alors Af vaut 0 sur T, Ef sur N(T) et Rf sur F.

**(h)**
1. R commute avec le projecteur I − EᵀK⁺E sur ker E, donc Π_T = (3I − R)(I − EᵀK⁺E)/7.
2. (I2) transposée donne (3I − R)Eᵀ = Eᵀ(4I + G) − 2J.
3. On calcule [Eᵀ(4I + G) − 2J]K⁺E par blocs :
   - la partie 𝟏 (K = 60) donne −J/12, d'où un terme +J/12 ;
   - la partie des différences de classes donne 0 (K⁺ y est nul) ;
   - la partie Y donne Eᵀ(3I − G)⁺_Y E, car sur Y, K = (3I − G)(4I + G) avec 4I + G inversible et commutant, donc
     (4I + G)K⁺ = (3I − G)⁺ ; le terme 2J s'y annule.
4. D'où, coefficient par coefficient, 7Π_T(w, w') = 3δ_{ww'} − R(w, w') + 1/12 − f_Wᵀ Γ_R f_{W'}. Ici
   f_W := e_W − 𝟏/6 ∈ Y ∩ (diff. comp.)^⊥ (par (e)), et Γ_R est l'inverse de 3I − G sur Y ∩ (diff. comp.)^⊥.
5. L, ou L + P_ker si c ≥ 2, vaut 36 sur 𝟏, 3 sur les différences de classes, 3I − G sur Y ∩ (diff. comp.)^⊥, et 1 sur
   les différences de composantes. Donc e_WᵀZe_{W'} = f_WᵀΓ_R f_{W'} + 1/36.
6. Comme 1/12 + 1/36 = 1/9, on obtient H = 7Π_T.

**(i)** Pour f ∈ E₋₄(Γ) ∩ ℝ^F, (Af)_x = Σ_{w ∈ star(x)} f_w = −4 f_x = 0. Donc 𝟏_{star(x)} ⊥ Im Π_T. ∎

*Contrôles.*
- Sur deux srg(243,22,1,2) réels (A : NOTE_MANDAT l. 281-286, statut C), les identités (I1)–(I3) ont été contrôlées
  exactement.
- La formule générale du projecteur, (r − s)Π = (rI − R)(I − Eᵀ(EEᵀ)⁺E), c'est-à-dire l'étape (h)1 seule, n'y a été
  vérifiée qu'à 10⁻¹⁵ près.
- L4, le rang 7 + c et la forme en Z de H sont propres à k = 14. Ils ne se calibrent pas à 243 (NOTE_MANDAT
  l. 287-288) : pour eux, il n'y a que la preuve écrite ici.
- La formule de H coïncide avec celle de ChatGPT, obtenue par un autre chemin (A : NOTE_CHATGPT_CORE37_VERIF l. 15-17).

**Lemme 4.4 (marges ; P).** Pour n ∈ N(T), #{w ∈ star(x) : n ∈ W(w)} = K(x, n). Pour n ∈ C₀ ∖ {x, x̄}, K(x, n) = 1.
De plus Σ_{n∈C₁} K(x, n) = Σ_{n∈C₂} K(x, n) = 20.

Si chaque W_y a deux noms dans C₁, ces comptes ne dépassent pas K(x, ·) et ils somment à 20. L'égalité est alors
automatique.

*Preuve.*
- K(x, n) = (EEᵀ)_{xn} par (I1).
- Pour n ∈ C₀ non partenaire de x : K(x, n) = 2 − 1 − (G²)_{xn} = 1, car deux sommets de C₀ n'ont aucun voisin commun
  dans G.
- **La somme est une identité de G seul**, vraie pour tout G étiqueté et pas seulement pour un Γ réalisé. Pour
  n ∈ C₁, K(x, n) = 2 − G_{xn} − (G²)_{xn}. Or Σ_{n∈C₁} G_{xn} = 1 (le seul voisin b₁), et Σ_{n∈C₁} (G²)_{xn} = 3 : il
  y a exactement trois chemins de longueur 2 de x vers C₁, par x̄, par b₁ (vers b̄₁) et par b₂. Donc
  Σ_{n∈C₁} K(x, n) = 24 − 1 − 3 = 20, et de même pour C₂.
- **Conséquence.** Dans toute affectation de 𝒮⁻ où chaque W_y a deux noms dans C₁ et dans C₂, les comptes sont
  ≤ K(x, ·) et somment à 20 = Σ K(x, ·). Ils sont donc égaux à K(x, ·). ∎

**Lemme 4.5 (couplage en x ; P).**
- N(x) induit un couplage parfait (λ = 1).
- Pour w ∈ star(x), le nombre de voisins de w dans star(x) vaut cap(W(w)) := 1 − |N_G(x) ∩ W(w)| ∈ {0, 1}.
- Si w ∼ w' dans star(x), alors W(w) ∩ W(w') = {x}.
- Si x n'est dans aucun triangle transversal, K(x, b₁) = 1, et l'unique w ∈ star(x) avec b₁ ∈ W(w) a cap = 0.

*Preuve.*
1. **Voisins de w dans N(x).** N(x) = {t₀, x̄, b₁, b₂} ∪ star(x).
   - w ≁ t₀ (w est lointain), et w ≁ x̄ car x̄ ∉ {x, y} = p₀(w).
   - w ∼ b_i si et seulement si b_i ∈ W(w). Par L2 en x, b₁ et b₂ ne sont pas tous deux dans W(w).
   - λ(x, w) = 1 : w a exactement un voisin dans N(x). Il a donc 1 − [b₁ ∈ W(w)] − [b₂ ∈ W(w)] = cap(W(w)) voisins
     dans star(x).
2. **Deux sommets adjacents de l'étoile.** λ(w, w') = 1, et x est leur voisin commun.
3. **K(x, b₁).** K(x, b₁) = 1 − (G²)_{x b₁} = 1 − [b₁ ∼ b₂]. ∎

*Forme du couplage.* Le couplage de N(x) a 7 arêtes, dont t₀x̄.
- Si x est hors triangle transversal, b₁ et b₂ sont couplés à deux lointains distincts, de cap 0. Les 8 autres sommets
  de l'étoile sont couplés entre eux. L'étoile induit donc 4K₂ + 2K₁.
- Sinon, b₁ ∼ b₂ est une arête du couplage, et l'étoile induit 5K₂.

**Lemme 4.6 (NF ; P).** Si w ∼ w' dans F, tout z ∈ W(w') ∖ W(w) vérifie |N_G(z) ∩ W(w)| ≤ 1.

*Preuve.* z ≁ w et μ(z, w) = 2. Or w' est un voisin commun. ∎

Dans l'étoile, W ∩ W' = {x} quand W ∼ W'. NF s'applique donc à tout z ≠ x, comme dans le code.

**Lemme 4.7 (conditions mod 7 ; P).** Supposons Γ de rang 37 et prenons la variante v_true. Alors, pour tout w ∈ F :
- ek(w) ∈ Δ_T ;
- u_w = (b(w), c(w), U_w) vérifie la condition diagonale ;
- toutes les paires vérifient R ≡ β_X + q.

*Preuve.* Propositions 3.5 et 3.8. ∎

---

## 5. Le test d'étoile : définition et audit du code

### 5.1 Le système 𝒮(G, x, v)

Soit G admissible, x ∈ C₀ et v = (j, ρ, δ, Δ) ∈ 𝒱₃₇(G).

**Données calculées depuis G seul.** K, X, β_X, k, ek, Z, Ω si d = 1, et une base (g_i) de Δ.

**Inconnues.** Pour chaque y ∈ C₀ ∖ {x, x̄} (10 cases) :
- un nom W_y = {x, y} ∪ q_y ∪ s_y, avec q_y ∈ P₁ et s_y ∈ P₂ ;
- un vecteur u_y = (b(W_y), c_y, v_y) ∈ F₇^j × F₇^j × F₇^ρ. Ici b(W_y) est déterminé par ek(W_y) = Σ_i b_i g_i.

**Contraintes.**
- **(S1) Marges.** #{y : n ∈ W_y} = K(x, n) pour n ∈ C₁ ∪ C₂.
- **(S2)** L2 pour chaque W_y ; L4 pour chaque W_y si c ≥ 2.
- **(S3)** ek(W_y) ∈ Δ.
- **(S4) Diagonale.** q(u_y, u_y) = −3 − β_X(W_y, W_y).
- **(S5) Paires**, pour y ≠ y' :
  - q_y ≠ q_{y'} et s_y ≠ s_{y'} ;
  - |W_y ∩ W_{y'}| ≤ 2 ;
  - R_{yy'} := (β_X(W_y, W_{y'}) + q(u_y, u_{y'}) mod 7) ∈ {0, 1} ;
  - si R_{yy'} = 1 : |W_y ∩ W_{y'}| = 1 et NF dans les deux sens.
- **(S6) Couplage.** #{y' : R_{yy'} = 1} = cap(W_y).
- **(S7) Réel.** Soit H la matrice 10 × 10 avec H_{yy} = 3 + 1/9 − e_yᵀZe_y et H_{yy'} = −R_{yy'} + 1/9 − e_yᵀZe_{y'}.
  On demande 0 ⪯ H ⪯ 7I, et rang H ≤ 8 si c = 1.

**Relaxation.** 𝒮⁻ est la relaxation utilisée pendant la recherche :
- (S1) devient « ≤ K(x, n) », et K(x, n) ≥ 1 pour les noms de C₁ ∪ C₂. On garde la seule conséquence d'égalité
  qu'utilise le moteur : si K(x, b₁) = 1, une case contient b₁ (règle b₁, §5.4) ;
- (S6) devient « ≤ cap » ;
- (S7) se réduit à la positivité sur les blocs déjà affectés, sans test de rang.

Toute solution de 𝒮 est une solution de 𝒮⁻. Si 𝒮⁻ est sans solution, 𝒮 l'est donc aussi.

**Proposition 5.2 (P).** Si Γ est de rang 37 et que l'étiquetage de sa droite T est G, alors 𝒮(G, x, v_true) a une
solution, pour tout x ∈ C₀ : les 10 sommets de star(x) avec leurs u_w.

*Preuve.*
- (S1) : Lemme 4.4 ;
- (S2) : Lemme 4.2 et Théorème 4.3 (e) ;
- (S3), (S4) et les valeurs R : Lemme 4.7 ;
- (S5) : Lemmes 4.1 (d), 4.2, 4.5 et 4.6 ;
- (S6) : Lemme 4.5 ;
- (S7) : Théorème 4.3 (h) : H est un bloc principal de 7Π_T, de rang ≤ 7 + c. ∎

### 5.2 Où chaque contrainte est implantée

Moteurs.
- `star39.cpp` : u à au plus 2 coordonnées.
- `star3.cpp` : identique, avec 3 coordonnées. Diff vérifiée au §8.6.
- `line37.cpp` : lignes 1-240 identiques octet pour octet à `star39.cpp` (§8.6), suivies de `line37_tail.inc`.

Préparations.
- `star_prep_gen.py` : forme X, tout type.
- `star39_prep.py` : forme Ω, d = 1.
- `prep_star` dans `line37_tail.inc` : forme Ω, ρ = 0.

| contrainte | préparation | moteur | verdict de lecture |
|---|---|---|---|
| 10 cases y ≠ x, x̄ ; W = (x, y, q, s) | `star_prep_gen.py` l. 159-161, 226 ; `line37_tail.inc` l. 113-122 | `NV = 10` | conforme |
| (S1) K(x, n) ≥ 1 pour n ∈ q ∪ s | l. 221-225 ; tail l. 118, 121 | — | conforme |
| (S1) marges ≤ K(x, n) | — | l. 201 (validation), l. 214 (anticipation) | conforme ; l'égalité est automatique (4.4) |
| (S2) L2 | l. 228-236 ; tail l. 124-135 | — | conforme |
| (S2) L4 (c ≥ 2) | l. 237-242 | — | conforme |
| (S3) équilibré : ek = 0 | l. 252-255 | — | conforme. Pour d = c, une assertion (ek = 0 est automatique par 3.3), jamais déclenchée |
| (S3) déséquilibré : ek ∈ F₇κ | l. 247-251 | — | conforme (§5.5) |
| (S4) diagonale | l. 262-276 (X) ; tail l. 139-140 (Ω, g ≡ 0) | — | conforme : `t = -3 - β` ; déséquilibré `2bc + q(v) = t` |
| (S5) bijections | — | l. 60, 212 | conforme |
| (S5) \|W ∩ W'\| ≤ 2 | — | l. 61-62 | conforme |
| (S5) R ∈ {0,1} | Y = 3 − Xe (l. 277) ou Ωe | `Rval` l. 49-57, l. 63-64 | conforme : Σ_k Y_a[noms_b] = 18 − β ≡ 4 − β, donc R ≡ β + q |
| (S5) R = 1 ⇒ partage = 1, cap = 1, NF | `nbc` l. 280 | l. 65-69 | conforme (4.5, 4.6) |
| (S6) couplage ≤ cap | `cap` l. 279 | l. 187-195, 218, 220 | conforme |
| (S6) couplage = cap | — | feuille l. 145 | conforme ; **jamais atteint** |
| (S7) unaire 0 ≤ H_ww ≤ 7 | l. 256-261 ; tail l. 136-138 | — | **flottant**, tolérance 10⁻⁹ (§5.6) |
| (S7) Schur incrémental | `zq`, `dd` | l. 79-113 | **flottant**, tolérance 10⁻⁹, filtre coupé si pivot < 10⁻⁷ (§5.6) |
| (S7) feuille : spectre ⊂ [0, 7], rang ≤ 8 | — | l. 146-156 | **flottant** (Jacobi), tolérances 10⁻⁷ et 10⁻⁶ ; **jamais atteint** |
| rang ≤ 8 coupé pour c ≥ 2 | — | `STAR_NORANK` | conforme : rang ≤ 9 est automatique par 4.3 (i) |
| réduction O(D) | `canon` : `oblr_prep.py` l. 85-101 ; `star_prep_gen.py` l. 93-106, 139-142, 283 | l. 185 | valide (§5.3) |
| règle b₁ | `h1` l. 281 | l. 171-174 | valide (§5.4) |
| directions de torsion | l. 184-211 ; `gen_batch.py`, boucle `--kappa` | — | valide (§5.5) |

**Recherche.** Profondeur d'abord, avec anticipation : chaque validation filtre tous les domaines ouverts contre la
case validée et les cases saturées. Aucune branche n'est coupée sans qu'une contrainte de 𝒮⁻ soit violée, à une
exception près : les branches non canoniques sous O(D) (l. 185).
- Elles ne violent rien. La recherche est donc complète **à l'action de O(D) près**, ce qui suffit, puisque l'ensemble
  des solutions est stable par O(D) (§5.3).
- La règle b₁ n'explore que les affectations où une case contient b₁. C'est une contrainte de 𝒮⁻ par définition
  (§5.1, §5.4).
- Un verdict UNSAT signifie donc : 𝒮⁻ n'a aucune solution.

Les journaux le confirment (§8.2) : sur 1 067 runs « boost » au rang 37 (807 runs (1,1), 260 sur les autres types ; état à 16 h 09),
**aucune feuille n'est jamais atteinte** (`leaves = 0`, ce qui confirme NOTE_BOOST l. 47). Les verdicts UNSAT
n'utilisent donc que 𝒮⁻ : bijections, L2, L3, L4, marges ≤, couplage ≤, NF, valeurs mod 7 et, si activé, le filtre
réel de positivité.

### 5.3 La réduction par O(D) est valide (P)

**Ce que fait le code.** Tant que toutes les u affectées sont nulles (`anynz` faux), le code n'essaie, pour une
candidate non nulle, que le représentant canonique de son orbite sous O(D). Le représentant est :
- le minimum lexicographique de l'orbite si ρ ≤ 2 (le groupe est énuméré par force brute) ;
- pour ρ = 3, le plus petit vecteur de même norme, par Witt.

*Preuve de validité.*
1. **Invariance des solutions.** Soit g ∈ O(D). Appliquer g à toutes les u préserve q(u, u'), les ensembles de
   niveau de la diagonale, R, donc H et toutes les contraintes. L'ensemble des solutions est donc stable par O(D).
2. **Invariance des domaines.** Sur un chemin où toutes les u affectées sont nulles, les valeurs R contre les cases
   affectées ne dépendent pas des u des candidates : R = β + q(0, u') = β. Les domaines filtrés, l'ordre de choix des
   variables (taille des domaines, règle b₁) et l'ensemble de branchement sont donc O(D)-invariants.
3. **Conclusion.** Soit S une solution. Au premier nœud de son chemin où S donne une u ≠ 0 à la case choisie,
   l'élément g qui envoie cette u sur son représentant produit une solution gS. Elle coïncide avec S sur les cases
   déjà affectées (u = 0) et sa candidate est canonique : elle est explorée. Ensuite la recherche est complète.
4. **Transitivité (Witt).** Le théorème de Witt (forme non dégénérée, caractéristique impaire) donne la transitivité
   de O(D) sur les vecteurs non nuls de norme donnée, isotropes compris. `witt_reps` est donc correct.

Le cas déséquilibré n'utilise aucune symétrie (`canon = 1`, l. 283) : c'est sûr.

### 5.4 La règle b₁ est valide (P)

**Ce que fait le code.** Si K(x, b₁) = 1 et qu'aucune case affectée ne contient b₁, il branche sur l'ensemble des
couples (case non affectée, candidate contenant b₁).

*Preuve.*
- Dans toute solution de 𝒮, exactement une case contient b₁ : c'est (S1) avec K(x, b₁) = 1. C'est pourquoi
  « une case contient b₁ » figure dans 𝒮⁻ (§5.1). Le branchement est exhaustif pour 𝒮⁻ ainsi défini, et donc pour 𝒮.
  La vraie étoile de Γ (Proposition 5.2) vérifie (S1) avec égalité : elle est explorée.
- Ensuite, la marge K(x, b₁) = 1 retire b₁ des autres domaines (l. 214).
- Si x est dans un triangle transversal, K(x, b₁) = 0 et la règle ne s'applique pas. Le code refuse d'ailleurs ces x
  en préparation (`star_prep_gen.py` l. 152-153 ; tail l. 104).

### 5.5 Le découpage par direction de torsion est valide (P), pour j = 1

**Ce que fait le code.**
- Il collecte les ek des candidates qui passent L2, L4 et les marges : l'ensemble `seen` (l. 187-202).
- Si leur espace engendré est de dimension ≥ 2, il fait une exécution par droite F₇g de cet espace (`directions`).
- S'il est de dimension 1, il prend la seule droite. S'il est nul, b = 0 partout.

*Preuve.*
- Si j = 1, tous les lointains ont ek(w) ∈ Δ_T = F₇g.
- Si un sommet de star(x) a ek ≠ 0, c'est une candidate (toutes les contraintes testées sont nécessaires), donc
  g ∈ vect(seen), et l'exécution « g » contient la vraie configuration.
- Si tous les sommets de star(x) ont ek = 0, la vraie configuration vérifie b = 0 sur l'étoile et appartient à
  **chaque** exécution, quelle que soit la droite choisie (l. 248-251 : ek = 0 passe toujours).
- La normalisation de κ (première coordonnée non nulle égale à 1) remplace b par αb. On l'absorbe en remplaçant c par
  c/α.
- Les droites g hors de vect(seen) ne laissent que les candidates à ek = 0. Elles sont donc couvertes par n'importe
  quelle exécution.

**Non couvert.** j ≥ 2, avec des sous-espaces Δ de dimension 2 et deux plans hyperboliques, n'est pas implanté (X).

### 5.6 Le filtre réel en flottant

**Où le flottant intervient.**
- (i) Z est calculé par inversion numérique : `numpy.linalg.inv` (l. 158), ou Gauss–Jordan à pivot partiel (tail
  l. 82-98).
- (ii) Test unaire : on rejette si H_ww < −10⁻⁹ ou H_ww > 7 + 10⁻⁹ (l. 260 ; tail l. 138).
- (iii) Schur incrémental : on rejette si d − yᵀy < −10⁻⁹, ou s'il en va de même pour 7I − H (l. 92). Le filtre est
  coupé dès qu'un pivot est < 10⁻⁷ (l. 109). Couper le filtre est conservateur.
- (iv) Feuilles : valeurs propres par Jacobi, rejet si λ_min < −10⁻⁷, λ_max > 7 + 10⁻⁷ ou λ₂ > 10⁻⁶ (l. 153, 155).

**Est-ce sûr pour une exclusion ? Non, pas comme preuve.**
- Une coupe est juste si et seulement si le complément de Schur **exact** est < 0.
- Le code coupe dès que la valeur **calculée** est < −10⁻⁹. Aucune borne d'erreur rigoureuse ne garantit que l'erreur
  d'arrondi reste < 10⁻⁹. Les pivots peuvent descendre à 10⁻⁷, ce qui amplifie l'erreur par un facteur allant jusqu'à
  ≈ 3·10³ à chaque substitution.
- Le cas dangereux n'est pas hypothétique : une vraie configuration a souvent un complément **exactement nul**.
  - Pour c = 1, rang H = 8, donc tout bloc de 9 cases est singulier.
  - Pour tout c, le bloc des 10 cases l'est aussi, car 𝟏_{star(x)} ∈ ker H_star (4.3 (i)).
  - Le test du 9ᵉ sommet (c = 1) ou du 10ᵉ porte donc sur un complément exactement nul, et seul l'arrondi décide de son
    signe calculé.
- **Atténuation (E).**
  - Les journaux de `star39` n'enregistrent pas la profondeur des coupes. Pour le moteur de droite complète `oblr`,
    l'archive donne des morts à la profondeur 2 à 4 (NOTE_FUSION l. 197, 343-348). Si l'étoile meurt aussi à faible
    profondeur, les blocs d'une vraie configuration y sont génériquement définis positifs. Pour l'étoile, c'est une
    hypothèse non vérifiée.
  - Sur les 25 runs relancés sans aucun filtre réel (7 types), le verdict ne change pas (§8.3, §8.4).
  - « Très probablement sans effet » n'est pourtant pas une preuve.

**Alternatives exactes**, par ordre de simplicité.
1. **Recherche purement exacte** : `STAR_NOREAL=1`, avec le test unaire retiré en préparation.
   - Mesures du jour (E, §8.3), toutes UNSAT : c = 1 en 13 897 nœuds (contre 2 511) ; c = 2 (3,3) en 175 358 (contre
     55 514) ; c = 3 (2,2,2) en 4 669 583 (contre 3 687 137, 53 s dans les deux cas).
   - Les variantes à torsion (c1t, c = 2 à torsion équilibrée et déséquilibrée, c1tt avec ses 8 directions, (3,4)
     équilibré) restent aussi toutes UNSAT.
   - Le facteur sur les nœuds va de ×1,3 à ×14.
   - Le plus gros run exact conclu est le (3,3) : 4 669 583 nœuds. Parmi les variantes à torsion, le plus gros est de
     356 110 nœuds.
   - Une variante déséquilibrée de (3,4) n'a pas conclu en 280 s (§8.3).
   - Il n'y a alors plus aucun flottant dans le verdict : seulement des entiers et des calculs mod 7. Recommandé pour la
     passe de preuve.
2. **Coupes à témoin entier.**
   - Pour c = 1, B := 9·det(L)·H est entier : B_ab = 9 det L (3δ_ab − R_ab) + det L − 9 e_aᵀ adj(L) e_b. Ses entrées
     sont de l'ordre de 10¹⁵ à 10¹⁷ (det L = 36²τ).
   - Pour c ≥ 2, on calcule Z une fois par G en fractions exactes, puis B = D·H avec D le dénominateur commun.
   - Chaque coupe flottante fournit le vecteur z = (−L_S⁻ᵀy, 1). On l'arrondit à des entiers d'au plus ~10⁶ et on
     vérifie zᵀB_{S∪w}z < 0 exactement, sur 128 bits ou en entiers longs. Si la vérification échoue, on ne coupe pas.
   - C'est sûr, peu coûteux, et le flottant n'y est plus qu'une heuristique.
3. **LDLᵀ rationnel** (Bareiss, entiers longs) réservé aux cas limites |marge| < 10⁻⁶. C'est un repli de 2.

### 5.7 Tests aux feuilles

- Ils sont en flottant (Jacobi) et n'ont **jamais été atteints** (§8.2). Ils n'ont donc rien décidé.
- Une passe de preuve doit traiter toute feuille comme un événement à examiner exactement : rang et positivité en
  fractions sur la 10 × 10.
- Une feuille qui passe tous les tests exacts serait une étoile SAT. Le test échouerait alors à exclure cette droite
  avec ce x.

### 5.8 Contrôle positif

- Aucun contrôle positif n'existe aux paramètres de Conway. Il n'y a pas d'instance SAT connue (A : NOTE_FUSION
  l. 160-163).
- Le seul indice de complétude est l'ablation du moteur Python indépendant : sans les valeurs de Green, l'étoile est
  SAT en 128 nœuds (A : NOTE_OBSTRUCTION §2.1, l. 109).
- À faire : des instances plantées pour `star39.cpp` et `star3.cpp`. On remplace les tables de compatibilité par celles
  d'une configuration choisie, puis on vérifie que le moteur la retrouve (X).

### 5.9 Écarts et hypothèses relevés

**Écarts du code avec les mathématiques.**
1. **Filtre réel et tests de feuille en flottant** (§5.6, §5.7). Les tolérances sont absolues et sans borne d'erreur
   rigoureuse. C'est le seul endroit où le code n'implante pas exactement une condition nécessaire.
2. **Couverture limitée.** u a au plus 2 coordonnées (`star39`) ou 3 (`star3`), et j ≤ 1. Les variantes à d − 1 ≥ 4
   coordonnées, ou à j = 2, n'existent pas (§7.2).
3. **Mode torsion choisi par le nom de la spécification** (`star_prep_gen.py` l. 117 : `c1t`, `c1tt`, `blockst`), et non
   calculé à partir de (c, d). C'est sans danger sur les lots faits : les spécifications `lg` et `blocks` ne tirent que
   des graphes à d = c, et une candidate non orthogonale au noyau y lèverait une assertion (l. 255). Mais une chaîne de
   production doit calculer d > c et choisir les variantes elle-même.

**Points de procédure.**

4. **`line37.cpp` ne teste que (1,1).** Les statuts `7-torsion`, `disconnected`, `no-x` et `TIMEOUT` ne sont pas des
   morts. `L23` n'est une mort que si l'on admet L23 (A). Seuls `K<0` et `UNSAT` le sont sans condition.
5. **Copie d'archive du pilote : point clos.** À 15 h 12, `boost_logs/gen_batch.py` (14 h 42) n'avait ni `u3` ni
   `GB_FMT3`. Il a été remplacé à 15 h 14, et il est maintenant identique, aux fins de ligne près, au pilote utilisé
   (`scratchpad/boost/gen_batch.py`) : vérifié par le relecteur.
6. **Binaires.** On suppose que les `.exe` correspondent aux sources : les horodatages coïncident. Une preuve doit
   recompiler depuis les sources, avec compilateur et options consignés.

**Documentation.**

7. L'en-tête de `star39.cpp` décrit la forme Ω (« R = 4 − eᵀΩe′ + uᵀDu′ »). Avec `star_prep_gen.py`, c'est R = β + uᵀDu′,
   par Y = 3 − Xe. C'est cohérent, mais l'en-tête est inexact pour cette entrée.
8. NOTE_BOOST §7 :
   - l'énoncé « c ≤ 3 » repose sur m = 4, exclu par des verdicts CP-SAT sans certificat ;
   - il ne traite pas les droites à t = 12, où aucun x n'est hors triangle ;
   - le type (1, 4) manque dans ses deux listes.
9. NOTE_FUSION §1.4 estimait d = 3 à « environ 0,05 % » (Cohen–Lenstra). La mesure de NOTE_BOOST donne 0,35 %
   (`lg_counts` : 56 sur 15 838). Sans conséquence logique.

**Hypothèses de la note.**

10. La chaîne suppose que les fichiers binaires intermédiaires ne sont ni tronqués ni corrompus : `star39.cpp` ne
    vérifie pas les retours de `fread`. Ce n'est pas une question de justesse des verdicts sur des fichiers valides,
    mais de robustesse.

**Aucun écart** n'a été trouvé dans les contraintes exactes : bijections, L2, L3, L4, marges, couplage, NF, valeurs mod 7,
diagonale, réduction O(D), règle b₁ et directions de torsion.

---

## 6. Le théorème

**Théorème 6.1 (P, conditionnel au Lemme 2.2 : P ≤ 852, statut A + E).**
- *Hypothèse (H₃₇).* Pour tout graphe de droite étiqueté admissible G avec t(G) ≤ 7, il existe x ∈ C₀ hors de tout
  triangle transversal de G tel que, pour toute v ∈ 𝒱₃₇(G), le système 𝒮(G, x, v) n'a pas de solution. Il suffit que
  ce soit vrai de 𝒮⁻.
- *Conclusion.* Aucun srg(99,14,1,2) n'a rang₇(A − 3I) = 37.
- *Variante.* L'hypothèse peut être vérifiée sur un représentant par Λ-orbite.

*Preuve.*
1. Soit Γ de rang 37. Par 2.3, Γ a une droite T avec t(G_T) ≤ 7.
2. On choisit l'ordre (t₀, t₁, t₂) et les étiquettes dans les classes, avec les partenaires (i, a), (i, a ⊕ 1). On
   obtient ainsi un graphe étiqueté G, admissible par 2.3. Si l'on ne dispose que d'un représentant G′ de son
   Λ-orbite, on ré-étiquette Γ par l'élément de Λ correspondant : la droite T a alors exactement G′ pour graphe
   étiqueté.
3. Soit x le sommet fourni par (H₃₇), et v_true = (r(T), ρ(T), δ(T), Δ_T). Par 3.8, v_true ∈ 𝒱₃₇(G).
4. Par 5.2, l'étoile de x dans Γ, avec les u_w de 3.5, est une solution de 𝒮(G, x, v_true), donc de 𝒮⁻. Cela
   contredit (H₃₇). ∎

**Corollaire 6.2 (forme demandée ; P sous 2.2).** Supposons que tout G admissible avec c(G) ≤ 4 qui possède un sommet
de C₀ hors des triangles transversaux échoue au test, pour un tel x et dans toutes les variantes de 𝒱₃₇(G). Alors
aucun Conway n'a r = 37.

*Preuve.* Un G admissible avec t ≤ 7 vérifie c ≤ 4 et possède un tel x (2.3). (H₃₇) en découle. ∎

**Remarque 6.3 (L23).**
- Si l'on admet L23 (A, §7.4), les droites (1,1) avec (τ | 7) = +1 n'ont plus aucune variante. `line37.cpp` les saute
  (statut `L23`, tail l. 177-178).
- Le Théorème 6.1 ne l'admet pas, et il n'en a pas besoin à un coût raisonnable : sur 5 droites (1,1) avec
  (τ | 7) = +1, l'étoile exacte, sans aucun flottant, meurt au rang 37 en 7 654 à 13 989 nœuds, 0,1 s chacune (E,
  §8.4).

**Remarque 6.4 (comparaison avec NOTE_BOOST §7).**
- NOTE_BOOST utilise m = 4 exclu (A, CP-SAT) pour se ramener à c ≤ 3.
- Ici, on n'utilise que P ≤ 852. Le prix est d'inclure les droites c = 4 à t ≤ 7, de profils 6 + 6 + 12 + 12 et
  6 + 6 + 6 + 18 : peu de graphes.
- La formulation « c ≤ 3 » a un trou que la présente version n'a pas : une droite à c ≤ 3 peut avoir t = 12
  (G = 12 triangles transversaux disjoints plus les partenaires, ce que K ≥ 0 n'exclut pas). Le moteur ne trouve
  alors aucun x (`no-x`).

---

## 7. Ce qui manque pour que le calcul devienne une preuve

### 7.1 L'énumération (X ; en construction par un autre agent)

**Objet.** Les triples (s₀₁, s₁₂, s₂₀) admissibles avec t ≤ 7, à l'action de Λ près.
- (12!)³/|Λ| ≈ 1,87·10¹¹ classes (A : NOTE_BOOST l. 242-243, en supposant l'action libre).
- 79,2 % des tirages sont admissibles (E : `boost_logs/lg_counts_20000_seed2026.txt`).

**Exigence.** Au moins un représentant par orbite. Les doublons sont sans danger ; une omission est fatale.

**Pourquoi les orbites suffisent (P).** Voir l'étape 2 de la preuve de 6.1. Le test peut prendre n'importe quel x ; seul
compte qu'un x convienne pour le représentant.

**Certification de l'énumération (X).** Au choix :
- deux générateurs indépendants qui donnent des ensembles de formes canoniques identiques, comme pour l'audit des
  gabarits c3 (A : AUDIT l. 13-19) ;
- un générateur plus une formule de masse Σ |Λ|/|Aut G| = nombre de triples étiquetés admissibles à t ≤ 7, ce qui
  exige un comptage indépendant de ce nombre.

Des fichiers de validation sur de petites tailles sont en cours chez un autre agent, dans `scratchpad/boost/runs/` :
`brute4_census.json`, `brute6_census.json`, `cmp_counts_n8.json`, `cmp_counts_n10.json`, `cmp_counts_n12_part1.json`. Ils
ne sont pas lus ici.

**Aiguillage par classe.**
- Calculer c, d, t, τ mod 7, une base de k et ek.
- Choisir x (le premier hors triangle) et lister 𝒱₃₇(G) selon la Définition 3.7 et la table du §3.6.
- Lancer chaque variante jusqu'à un UNSAT définitif. Tout autre statut veut dire « non fait » : TIMEOUT, SAT, erreur
  de préparation, ou en sortie de `line37` : `no-x`, `7-torsion`, `disconnected`.

### 7.2 Couverture des types

| (c, d) | variantes (j, ρ) | moteur | instances testées au 20/10 (toutes UNSAT, 0 feuille) | statut |
|---|---|---|---|---|
| (1, 1) | (0, 0) | `line37`, `star39` | 40 (`cost37`, graines 1-40) + 767 (`cost37_2000`, graines 41-807), toutes à (τ\|7) = −1 ; 33 754 droites testées sur 100 000 tirages uniformes par `line37` (graine 777001, 0 SAT, 0 TIMEOUT ; `boost_logs/line37_rand100k_seed777001.json`, lu ici) ; + §8 : 1 exacte, et 5 à (τ\|7) = +1 exactes | E (échantillon) |
| (1, 2) | (0, 1) | `star39` (c1t) | 10 droites × 2 formes | E |
| (1, 3) | (0, 2), (1, 0) | `star39` (c1tt) | 6 droites, 60 runs (8 directions) | E |
| (1, 4) | (0, 3), (1, 1) | `star3` accepte 3 coordonnées, mais **aucun générateur** d'instances (§7.5, point 2) | 0 | X |
| (2, 2) | (0, 1) | `star39` | 30 droites, 60 runs | E |
| (2, 3) | (0, 2), (1, 0) | `star39` | 18 droites, 54 runs | E |
| (2, 4) | (0, 3), (1, 1) | idem : **aucun générateur** d'instances | 0 | X |
| (3, 3) | (0, 2) | `star39` | 14 droites, 28 runs (NOTE_BOOST) ; 21 droites, 42 runs dans les journaux du scratchpad | E |
| (3, 4) | (0, 3), (1, 1) | `star3` | 6 droites, 24 runs (`gen37_c3t`, en cours), jusqu’à 2,7·10⁷ nœuds et 392 s par run ; en exacte seule, seules les deux variantes équilibrées d’une droite (§8.3) | E (partiel) |
| (4, 4) | (0, 3) | `star3` | lot `gen37_c4` lancé à 14 h 57, aucun résultat à 16 h 09 | X |
| d ≥ 5, tout c ≤ 4 ; (4, 5), (4, 6) | u à ≥ 4 coordonnées, ou j = 2 | **aucun** | 0 | X |

**Fréquence des types rares** (estimation heuristique, sans statut P/A/E).
- Parmi les c = 1 : d = 2 pour 14,1 % et d = 3 pour 0,35 % (E : `lg_counts`).
- En prolongeant la décroissance, il y aurait de l'ordre de 10⁵ à 10⁶ classes à d = 4 et quelques milliers à d = 5.
- Leur coût par droite devrait rester modéré : l'orthogonalité au noyau (d − 1 conditions) compense les 7^{d−1}
  vecteurs u, comme pour c1tt (3 602 candidats). Ce n'est pas mesuré.
- Les types d ≥ 5 exigent d'étendre le moteur (X).

### 7.3 Certifier les verdicts UNSAT : proposition concrète

**(a) Passe exacte.** Toute la production en recherche purement exacte (§5.6, option 1). Il n'y a plus aucun flottant
dans un verdict. Le coût est à mesurer sur 10⁴ droites ; sur les 25 essais du jour, de ×1,3 à ×14 en nœuds. Pour
une variante déséquilibrée lourde de (3,4), on **estime** environ ×3 en temps, par extrapolation d'un TIMEOUT : arrêt
à 280 s avec 98 % des branches faites, contre 92 s avec filtre (§8.3). Ce n'est pas un verdict.

**(b) Double implémentation.**
- Un second moteur écrit à part : autre auteur, autre langage, pas de code partagé. Il porte sur le système exact
  𝒮⁻, sans filtre réel, avec les formalismes X et Ω, et tous les encodages de 3.5 (j ≤ 2).
- Il doit rendre UNSAT sur chaque classe. Tout désaccord bloque.
- `star_csp.py` en est déjà une ébauche pour (1,1) : même domaine et même verdict que `star39` sur la graine 1 (§8.3).

**(c) Format de certificat CERT-R37** (proposé ; X).
- **Enregistrement par classe.** On stocke :
  - le triple (s₀₁, s₁₂, s₂₀) et sa forme canonique ;
  - c, d, t, (τ mod 7) et x ;
  - pour chaque v ∈ 𝒱₃₇(G), dans l'ordre canonique : v (une base de Δ en forme échelonnée), puis le verdict et une
    preuve LRAT.
- **Formule régénérée.** La formule CNF Φ(G, x, v) n'est **pas** stockée : le vérificateur la régénère à partir de
  (G, x, v) avec son propre code, court et relisible. Variables : X_{y,i}, pour « la case y prend la candidate i ».
  Ses clauses :
  - exactement une candidate par case ;
  - une clause binaire ¬X_{y,i} ∨ ¬X_{y',i'} pour chaque paire incompatible selon (S5), calcul entier et mod 7 ;
  - les marges Σ_{(y,i) : n ∈ W_i} X_{y,i} ≤ K(x, n), par compteur séquentiel ;
  - le couplage X_{y,i} → Σ_{R(i,i') = 1} X_{y',i'} ≤ cap(i) ;
  - **aucune contrainte réelle**, ou alors des clauses-lemmes réelles accompagnées chacune de leur témoin entier z
    (§5.6, option 2), vérifié à part.
- **Vérification.** La preuve LRAT est émise par CaDiCaL ou kissat et vérifiée par `cake_lpr`, vérifié formellement.
  Base de confiance : le générateur de Φ, l'énumération et `cake_lpr`.
- **Coût.** Inconnu. Un solveur SAT peut être bien plus lent que le moteur dédié. À mesurer sur 100 droites avant tout
  choix (X).
- **Repli réaliste.** (a) et (b) partout, et (c) sur un échantillon aléatoire de classes.

**(d) Contrôles du moteur.** Instances plantées (§5.8) et tests de mutation : en retirant une contrainte, un UNSAT peut
devenir SAT, jamais l'inverse.

### 7.4 Statut des maillons d'entrée

| maillon | énoncé | statut | où |
|---|---|---|---|
| Lemme 2.1 | Σ t = 2P ; triangles transversaux disjoints | P | §2 |
| Lemme 2.2 | P ≤ 852 | **A + E** : certificat exact ; recensement engendré par programme (deux implantations, 0 écart) ; aucune preuve à la main du recensement | AUDIT §8 l. 211-238 ; §8.1 ici |
| Lemme 2.3 | ≥ 18 droites à t ≤ 7 ; c ≤ 4 ; ≥ 5 sommets hors triangle | P (sous 2.2) | §2 |
| Lemmes 3.1-3.3, Cor. 3.4 | noyau, formule de rang, r(T) ≤ d − c | P ; aussi E (assertion de `star_prep_gen.py` sur les runs qui l'utilisent, `schur_check.py`) | §3 ; NOTE_FUSION R5 |
| Prop. 3.5 | encodages, j quelconque | P | §3.4 |
| Prop. 3.6 | forme de Green | P ; A (PROMPT_CORE37 l. 112-134) ; E (`omega_check.py`) | §3.5 |
| Théorème 4.3 | cadre lointain, H = 7Π_T, rang 7 + c, L4 | P ; A (NOTE_MANDAT §4). Seules (I1)–(I3) sont contrôlées exactement à 243 ; le projecteur général l'est à 10⁻¹⁵ près ; L4, le rang 7 + c et la forme en Z n'ont aucun contrôle possible à 243 | §4 |
| Lemmes 4.4-4.7 | marges, couplage, NF, mod 7 | P | §4 |
| §5.3-5.5 | O(D), règle b₁, directions | P | §5 |
| L23 | (τ \| 7) = −1 pour (1,1) au rang 37 | **A, non audité** : note 102 de Codex (25/09, §0, 1.4, 4, 5 ; dépôt conway99-c1, absente de cet espace) ; `work/c1_theta_lp_2026-10-07/NOTE.md` l. 3083-3131 (« Hand derivation, not audited ») ; NOTE_RESEAUX_DE_DROITE l. 36-42 (« non relu ») | **non utilisé** par 6.1 |
| règle de forme δ | δ fixé par d₀ et la torsion | A, non audité (NOTE.md l. 3162-3176 ; NOTE_RESEAUX l. 29-34) | **non utilisé** : les deux formes sont testées |
| m = 4 exclu | CP-SAT, 79 gabarits | A, sans certificat portable (NOTE_MANDAT l. 77 ; AUDIT l. 75) | **non utilisé** |
| (H₃₇) | toutes les étoiles meurent | **X** : échantillons E seulement | §7.1-7.3 |

### 7.5 Les trous, par ordre de gravité

1. **(H₃₇) n'est vérifiée que sur des échantillons.**
   - Environ 3,5·10⁴ droites, dont 33 754 testées par `line37`, presque toutes (1,1), sur ≈ 1,9·10¹¹ classes.
   - L'énumération n'existe pas encore, et sa certification non plus.
   - Coût (A : NOTE_BOOST, version de 15 h 45, l. 80-82 et 256-262) : ≈ 8·10⁵ heures-cœur avec le moteur actuel et
     L23, et 1,5 à 2·10⁵ après une optimisation qui n'est pas encore faite.
   - Sans L23 et en passe exacte, ce sera davantage ; non mesuré.
2. **Types non couverts.**
   - Aucun moteur pour d ≥ 5 (u à ≥ 4 coordonnées, ou j = 2).
   - (1,4) et (2,4) : `star3` accepte 3 coordonnées, mais **aucune spécification de `star_prep_gen.py` ne produit ces
     types**. `lg` donne d = 1, `c1t` et `blockst` d = c + 1, `c1tt` d = 3 et `blocks` d = c. Le mode torsion étant
     choisi par le nom (l. 117), il faut un générateur et le choix du mode à partir de (c, d) avant tout run.
   - (4,4) et (3,4) sont en cours, avec 0 et 6 droites.
3. **Aucun certificat des UNSAT.**
   - Un seul moteur C++ pour le formalisme général ; le moteur Python indépendant ne couvre que (1,1).
   - Les binaires ne sont pas recompilés de façon reproductible.
   - Aucun contrôle positif aux paramètres de Conway.
4. **Flottant.** Le filtre réel (unaire et Schur) et les tests de feuille ne sont pas rigoureux (§5.6). La correction
   est simple : passe exacte, déjà UNSAT sur 7 types (25 runs) aujourd'hui, ou coupes à témoin entier. Le coût de la
   passe exacte sur les variantes lourdes, (3,4) déséquilibré et c = 4, n'est pas mesuré.
5. **P ≤ 852** repose sur un recensement engendré par programme. Le certificat est exact, et les deux implantations
   sont indépendantes. Il manque une vérification formelle ou une dérivation lisible du recensement. Statut A + E, pas P.
6. **Chaîne de production non écrite.** Mode torsion décidé par le nom de la spécification ; statuts de `line37` à
   reclasser ; binaires à recompiler de façon traçable (§5.9, points 3, 4 et 6).
7. **Preuves P non relues.** Théorème 4.3, Lemmes 3.1 à 3.3, Propositions 3.5 et 3.6, §5.3 à 5.5. Leurs identités
   sont contrôlées numériquement, mais aucun tiers ne les a relues.
8. **Si L23 est utilisé pour réduire le coût.** Lemme A non audité. Le théorème peut s'en passer (Remarque 6.3).

---

## 8. Calculs de contrôle faits pour cette note (E)

Un processus à la fois, priorité IDLE pour les moteurs, au plus 5 minutes chacun. Répertoire :
`C:/home/researcher/AppData/Local/Temp/claude/…/scratchpad/boost/runs/thm_r37/`. Python :
`C:/home/researcher/conway99-env/.venv/Scripts/python.exe`.

**8.1 P ≤ 852.**
- Commande : `p852_identity.py` (dossier audit) appliqué à `codex_order9_prism_cap.json` et `codex_order9_census.json`
  (`C:/home/researcher/Desktop/Recherche_Conway/c1-codex/data/`).
- Sortie : 16 termes, 0 poids négatif ; Σ w N = {1 : 11088/13, P : −1} ; `IDENTITY 11088/13 - P: True`.
- SHA256 : a48166055b0a…24159a1 et a49f811e4b64…ff699a291, identiques à `p852_identity.out` du 18/10.

**8.2 Lecture des journaux** (`scan_logs.py`, lecture seule). Sur les journaux du scratchpad à 16 h 09 :

| fichier | droites | runs | statuts | feuilles | erreurs de préparation |
|---|---:|---:|---|---:|---:|
| `cost37` | 40 | 40 | UNSAT | 0 | 0 |
| `cost37_2000` | 767 (en cours) | 767 | UNSAT | 0 | 0 |
| `gen37_c2` | 40 (30 en (2,2), 10 en (1,2)) | 80 | UNSAT | 0 | 0 |
| `gen37_c2t` | 18 | 54 | UNSAT | 0 | 0 |
| `gen37_c1tt` | 6 | 60 | UNSAT | 0 | 0 |
| `gen37_c3_*` | 21 | 42 | UNSAT | 0 | 0 |
| `gen37_c3t` | 6 (en cours) | 24 | UNSAT | 0 | 0 |
| `gen37_c4` | 0 (lancé à 14 h 57) | 0 | — | — | — |

Total : 898 droites et 1 067 runs, tous UNSAT, sans aucune feuille.

**8.3 Recherche purement exacte, sans aucun filtre réel.**
- *Préparation.* Copie locale `prep_nounary.py` de `star_prep_gen.py`, avec le test unaire l. 260-261 désactivé ; seul
  le chemin d'import change. Moteur lancé avec `STAR_NOREAL=1`.

| instance | avec filtre réel (journal) | exacte seule | verdict |
|---|---|---|---|
| (1,1), `lg:-1`, graine 1, x = 0 | 3 070 candidats, 2 511 nœuds | 3 585 candidats, 13 897 nœuds, 0,1 s | UNSAT |
| (2,2), blocs 3,3, graine 1, δ = 1 | 9 305 candidats, 55 514 nœuds | 9 427 candidats, 175 358 nœuds, 1,5 s | UNSAT |
| (3,3), blocs 2,2,2, graine 1, δ = 1 | 30 596 candidats, 3 687 137 nœuds, 53,5 s | 30 596 candidats, 4 669 583 nœuds, 53,0 s | UNSAT |

- *Bilan intermédiaire.* Avec le test unaire en préparation mais sans le filtre de Schur : (1,1) en 8 532 nœuds et
  (2,2) en 169 245 nœuds, tous deux UNSAT.

*Variantes à torsion*, recherche exacte. Script `exact_batch.sh`, sortie `exact_batch.out`. Même x que dans les
journaux.

| instance | variante | avec filtre réel (journal) | exacte seule | verdict |
|---|---|---:|---:|---|
| (1,2) c1t, graine 1, x = 0 | δ = 1 / δ = 3 | 507 / 627 | 6 995 / 7 598 | UNSAT / UNSAT |
| (2,3) `blockst:3,3`, graine 1, x = 1 | δ = 1 / δ = 3 | 1 858 / 2 133 | 12 316 / 13 835 | UNSAT / UNSAT |
| (2,3) `blockst:3,3`, graine 1, x = 1 | déséquilibré (1 direction) | 48 498 | 356 110 | UNSAT |
| (1,3) c1tt, graine 1, x = 0 | δ = 1 / δ = 3 | 648 / 744 | 1 611 / 1 748 | UNSAT / UNSAT |
| (1,3) c1tt, graine 1, x = 0 | déséquilibré, 8 directions | 5 037 à 5 743 | 12 562 à 14 536 | 8 × UNSAT |
| (3,4) `blockst:2,2,2`, graine 2, x = 2, `star3` | δ = 1 / δ = 3 | 24 781 / 47 401 | 132 137 / 203 933 | UNSAT / UNSAT |

Variante déséquilibrée de (3,4), `u3` (graine 2, x = 2).
- Avec filtre, le journal donne 6 593 161 nœuds en 92 s.
- En exacte seule, le run est **arrêté à 280 s (TIMEOUT, pas un verdict)**, après 27 557 888 nœuds et 3 995 branches
  de profondeur 1 sur 4 088, sans aucune feuille.
- **Extrapolation, pas une mesure** : il aurait fini vers 290 s, soit environ ×3 en temps.
- La variante `u` (1,45·10⁷ nœuds avec filtre) n'a pas été relancée.

**Bilan exact du jour.** 25 runs sur 7 types : (1,1), (1,2), (1,3), (2,2), (2,3), (3,3), (3,4) équilibré. Les 5 runs de
§8.4 y sont comptés. Tous sont UNSAT, sans feuille.
- *Moteur indépendant.* `star_csp.py 1 0` (Python, forme Ω, aucun flottant) donne UNSAT en 12 817 nœuds, avec des
  tailles de domaines 350, 354, 355, 375, 348, 354, 348, 379, 362, 360. Ce sont **exactement** celles de
  `prep_nounary.py` sur la même droite : la génération des candidats concorde entre deux implantations.

**8.4 Droites (1,1) à (τ | 7) = +1, sans L23**, recherche exacte. Spécification `lg:1`, premier x hors triangle.

| graine | x | candidats | nœuds |
|---:|---:|---:|---:|
| 1 | 1 | 3 628 | 13 988 |
| 2 | 0 | 3 108 | 9 347 |
| 3 | 0 | 2 720 | 7 654 |
| 4 | 0 | 3 217 | 10 752 |
| 5 | 0 | 3 645 | 13 989 |

Les cinq sont UNSAT en 0,1 s chacune.

**8.5 Sens du paramètre P.**
- Le recensement de Codex (`codex_order9_census.json`) a pour premier paramètre `P`.
- Le recensement LAB l'appelle `N6_29327` : c'est lui qui porte le coefficient −1 dans `p852_recheck.json`.
- Décodage à la main de 29327 = 2⁰ + 2¹ + 2² + 2³ + 2⁷ + 2⁹ + 2¹² + 2¹³ + 2¹⁴, comme masque d'adjacence sur 6 sommets,
  les paires étant rangées en ordre colexicographique (01, 02, 12, 03, 13, 23, 04, …). On obtient les arêtes 01, 02,
  12, 03, 14, 34, 25, 35 et 45 : deux triangles {0,1,2} et {3,4,5} reliés par 03, 14 et 25. C'est le prisme.
- La convention d'ordre est supposée, mais le résultat concorde avec NOTE_TRESOR l. 76.

**8.6 Copies de moteur.**
- `line37.cpp` l. 1-240 est identique à `star39.cpp` l. 1-240, et `line37.cpp` l. 242-fin est identique à
  `line37_tail.inc`.
- `star3.cpp` ne diffère de `star39.cpp` que par la troisième coordonnée (`Cand`, `Dq`, `Rval`, lecture et
  affichage).

**8.7 Relecture indépendante (20/10, 16 h).** Un agent relecteur, en contexte neuf et sans importer le code du
projet, a vérifié la note contre le code et la mathématique.
- **Contrôles numériques** (`scratchpad/boost/runs/review/check_review.py`). Sur 60 G étiquetés aléatoires (51
  admissibles, 45 à d = 1), 0 écart sur :
  - rang M_NN = 38 − d, avec κ₀₁ et κ₁₂ dans le noyau ;
  - Ω𝟏 = 𝟏, Ω1_{C_i} = 𝟏 + 5·1_{C_i} et Σx = e ;
  - β = 4 − eᵀΩe′ sur 1 800 paires, M_NN g = ê étant résolu par son propre code ;
  - Σ_{C₁} K(x, ·) = Σ_{C₂} K(x, ·) = 20 et K(x, b₁) = 1 − [b₁ ∼ b₂].
- **Remarque 6.4.** Il a aussi construit un étiquetage avec t = 12, c = 1 et K ≥ 0, ce qui la confirme.
- **Verdict.** Mathématique et références de code justes ; Théorème 6.1 conforme aux lemmes.
- **Corrections intégrées depuis** :
  - portée de l'assertion de rang (§3.1) ;
  - coût et numéros de ligne de NOTE_BOOST ;
  - attribution du contrôle à 243 (§4.3) ;
  - exception O(D) et contrainte b₁ dans 𝒮⁻ (§5.1, §5.2, §5.4) ;
  - identité Σ K(x, ·) = 20 pour tout G (Lemme 4.4) ;
  - générateurs manquants pour (1,4) et (2,4) ;
  - extrapolations marquées comme telles ;
  - le point « pilote archivé périmé », devenu faux après 15 h 14.

Rien n'a été écrit dans `reference/` ni dans `provenance/`, et aucun fichier existant n'a été modifié. Les copies et
scripts de contrôle sont restés dans le scratchpad.
