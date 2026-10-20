# Énumération exacte des graphes de droite G_T : type cyclique, comptes de Burnside, énumérateur canonique, pilote

LAB, 20/10/2026, fin d'après-midi. Mandat du coordinateur : décomposition prouvée, comptes exacts, énumérateur C++,
pilote line37, coût. **Calculs arrêtés à 16 h 33** (suspension du boost, l'utilisateur est sur le PC) : ce qui n'a pas
tourné est listé au §8.

**Statuts** (ceux de NOTE_BOOST) :
- **P** : preuve écrite ici, non relue ;
- **E** : calcul exact sans certificat exporté (comparaison de programmes, verdicts d'un moteur maison) ;
- **A** : déjà dans l'archive (source citée).

---

## 0. Réponse courte

1. **Nombre exact de classes de graphes de droite (n = 12) : 187 381 435 694** (E).
   - Deux formules de Burnside indépendantes donnent ce même total. La première passe par la décomposition en λ du §1,
     la seconde est un Burnside direct sur le groupe de réétiquetage H, sans λ.
   - L'estimation à action libre donnait 10395³/6 = 187 207 063 312,5. Le rapport vaut 1,000931 : il y a
     174 millions de classes en plus, qui viennent des orbites non libres.
2. **Classes admissibles (K ≥ 0) : 147 579 095 390, soit 78,7587 %** (E, exact).
   - 68 λ sont comptés par Burnside restreint aux triples admissibles.
   - Les 9 λ de grand groupe sont comptés par énumération complète.
   - Les 8 λ comptés des deux façons concordent.
   - Pour la cible t ≤ 7 de THEOREME_REDUCTION_R37 §7.1 (A) : 187 379 400 048 classes, dont 147 577 214 193
     admissibles.
3. **Décomposition (P, validée E).** Soit σ = s20∘s12∘s01, de type cyclique λ ⊢ 12. Les classes de type λ sont en
   bijection avec les orbites, sous A_λ = Stab(F_λ), des triples (M0, M1, M2) de couplages parfaits de [12].
   - A_λ est décrit explicitement en 6 classes à gauche de C(σ), et |A_λ| = 6 z_λ (§1).
4. **Critère K ≥ 0 sur couplages partiels (P, validé E).** K ≥ 0 équivaut à : aucune σ-arête {i, σ(i)} (avec
   σ(i) ≠ i) dans M0∩M1, dans M1∩M2 ni dans σ(M2)∩M0 (§2.3).
   - On le teste dès que (M0, M1) est fixé, puis à M2.
   - Sur les 3 pilotes, il redonne exactement les K<0 de line37.
5. **Énumérateur `enum37.cpp` / `enum37.exe` (P pour l'algorithme, E pour la validation).**
   - Il sort une ligne par classe, au format 36 entiers de `line37 file`.
   - Options : tranche `--slice i/n`, filtre `--adm`.
   - Validation :
     - N = 4 et N = 6 par force brute : 373 248 000 triples, toutes les orbites, 0 doublon, 0 omission ;
     - N = 8 et N = 10 : tous les λ égaux à Burnside ;
     - N = 12 : 21 λ égaux à Burnside, soit 16,5·10⁹ classes ;
     - autotests : forme canonique comparée à la force brute sur A_λ, 0 écart (§4).
6. **Pilote (E).** Aucun SAT, aucun TIMEOUT, et toutes les droites testées sont UNSAT.

   | λ | t | classes | K<0 | disconnected | 7-torsion | L23 | no-x | UNSAT |
   |---|---:|---:|---:|---:|---:|---:|---:|---:|
   | (1¹²) | 12 | 790 | 0 | 210 | 144 | 230 | 206 | 0 |
   | (2,1¹⁰) | 10 | 29 836 | 1 024 | 3 145 | 5 050 | 10 426 | 0 | 10 191 |
   | (3,1⁹) | 9 | 182 221 | 12 927 | 11 408 | 25 092 | 66 567 | 0 | 66 227 |

   - Ces trois λ ont t ≥ 8. Ils sortent donc de la cible t ≤ 7 de THEOREME_REDUCTION_R37.
   - Les 206 `no-x` de (1¹²) illustrent le trou de la formulation « c ≤ 3 », signalé par la Remarque 6.4 de
     THEOREME_REDUCTION_R37.
7. **Coût (E).**
   - Mesure : 200 tirages par λ, pour les 77 λ, pondérés par les N_λ exacts.
   - Avec `line37.exe`, le test complet coûte environ 1,96·10⁹ s, soit environ 5,4·10⁵ heures-cœur.
   - Avec `line37_fast`, environ 10 fois plus rapide selon NOTE_LINE37_FAST (non remesuré ici) : environ 5·10⁴ à
     6,5·10⁴ heures-cœur. Cela fait environ 2 à 3 jours sur 1 000 cœurs, ou environ 6 mois sur le PC du labo (13 fils).
   - L'énumération elle-même coûte environ 50 à 160 heures-cœur (1 à 3 µs par ligne), soit moins de 0,5 % du test.
8. **Ce qui pourrait réduire.**
   - Le filtre K ≥ 0 sur couplages partiels (−21,24 % des classes, exact) et la restriction t ≤ 7 (A, −2·10⁶ classes)
     ne retirent que des droites déjà bon marché.
   - Le coût est concentré sur environ 33 % de droites (environ 6,2·10¹⁰) qui passent K, la connexité, la torsion
     et L23. Aucune condition partielle sur les couplages ne les décide, car Ω et Z sont globaux.
   - Le seul levier réel est donc le coût du test par droite, ou une preuve (§7).

---

## 1. Le modèle et le théorème de décomposition (P)

### 1.1 Objets

- **Sommets et structures.**
  - Classes C_c = {c} × [n], c ∈ {0, 1, 2}, avec n = 2m (n = 12 pour Conway), et V = C0 ∪ C1 ∪ C2.
  - Une **structure** est un graphe sur V tel que chaque classe induit un couplage parfait M_c (les partenaires), et
    que deux classes distinctes sont reliées par un couplage parfait (les arêtes croisées).
  - L'ensemble des structures est 𝓜 × 𝓕. Ici 𝓜 = PM([n])³ est l'ensemble des triples de couplages internes, avec
    |PM([12])| = 11!! = 10 395. Et 𝓕 ≅ Sym(n)³ est l'ensemble des parties croisées F = (s01, s12, s20).
  - Les arêtes croisées sont (0,i)–(1,s01 i), (1,i)–(2,s12 i) et (2,i)–(0,s20 i).
- **Groupes.**
  - W = Sym(n) ≀ S3 agit par φ(c, i) = (τ(c), π_c(i)), pour φ = (τ; π0, π1, π2). Il agit sur le graphe, donc
    diagonalement sur 𝓜 × 𝓕.
    - Sur 𝓜 : (φ·M)_{τ(c)} = π_c(M_c).
    - Sur 𝓕 : soit (a, b) une paire avant (01, 12 ou 20). Si (τa, τb) est avant, s′_{τa τb} = π_b s_ab π_a⁻¹.
      Sinon, s′_{τb τa} = π_a s_ab⁻¹ π_b⁻¹.
    - Ces deux formules sont recalculées à partir du graphe image dans `enum37_validate_group.py`, test (a).
  - **Forme standard.** M_c = P* (i ↔ i^1) pour tout c. L'ensemble X = {P*}³ × 𝓕 est celui des triples
    (s01, s12, s20) de ll_test / line37.
  - H = Stab_W(P*³) = B_m³ ⋊ S3, avec B_m = Z2 ≀ S_m d'ordre 2^m m!. C'est exactement l'équivalence du mandat :
    réétiquetages qui respectent les partenaires, et permutations des classes.

### 1.2 Lemme 1 (orbites et stabilisateur)

**Énoncé.** Un groupe G agit sur A et B. Soit O ⊆ A une G-orbite et a0 ∈ O. Alors l'application
G_{a0}·b ↦ G·(a0, b) est une bijection de G_{a0}\B sur G\(O × B).

**Preuve.**
- Elle est bien définie : si b′ = h b avec h ∈ G_{a0}, alors (a0, b′) = h·(a0, b).
- Elle est surjective : si (a, b) ∈ O × B avec a = g a0, alors g⁻¹·(a, b) = (a0, g⁻¹b).
- Elle est injective : si g·(a0, b) = (a0, b′), alors g ∈ G_{a0} et b′ = g b. □

### 1.3 Théorème 1 (décomposition par type cyclique)

**(i) Les H-orbites de X sont les W-orbites des structures.**
- On applique le Lemme 1 avec A = 𝓜, a0 = P*³ et B = 𝓕.
- W, et même Sym(n)³, est transitif sur 𝓜.
- G_{a0} = H.

**(ii) L'invariant σ.** On pose σ_F = s20 s12 s01 ∈ Sym(n).
- Sous τ = id, on a σ′ = π0 σ π0⁻¹.
- Sous la rotation (0→1→2→0) avec π = id, on a (s′01, s′12, s′20) = (s20, s01, s12), d'où
  σ′ = s20⁻¹ σ s20.
- Sous τ = (1 2) avec π = id, on a (s′01, s′12, s′20) = (s20⁻¹, s12⁻¹, s01⁻¹), d'où σ′ = σ⁻¹.
- σ⁻¹ est conjugué à σ. Le type λ ⊢ n de σ est donc un invariant de W. Il est vérifié sur des tirages par le test (c).
- **Lecture géométrique.** Les arêtes croisées forment un 2-facteur. Chacun de ses cycles parcourt les classes dans
  l'ordre 0, 1, 2, 0, … et a pour longueur 3k, où k est la longueur du cycle de σ correspondant.
  - Une part 1 de λ est un triangle transversal. Le nombre t de triangles transversaux vaut donc m₁(λ).

**(iii) Transitivité.** Toute partie croisée de type λ est Sym(n)³-équivalente à F_λ = (id, id, σ_λ), où σ_λ est la
permutation canonique : cycles en blocs consécutifs, de longueurs décroissantes.
- On prend π0 = id, π1 = s01⁻¹ et π2 = (s12 s01)⁻¹. Cela donne (id, id, σ_F).
- On conjugue ensuite par (g, g, g) avec g σ_F g⁻¹ = σ_λ.

**(iv) Conclusion.** On applique le Lemme 1 avec A = 𝓕, O = O_λ, a0 = F_λ et B = 𝓜.

> **Théorème 1.** Les classes de G_T de type λ sont en bijection avec les orbites de A_λ := Stab_W(F_λ) sur
> PM([n])³. À (M0, M1, M2) correspond la forme standard de la structure (F_λ, M), obtenue en réétiquetant chaque classe
> par ψ_c avec ψ_c(M_c) = P* :
> s01 = ψ1 ψ0⁻¹, s12 = ψ2 ψ1⁻¹, s20 = ψ0 σ ψ2⁻¹.
> La conversion est vérifiée par le test (e), puis par la force brute N = 6 du §4.

### 1.4 Proposition 2 (A_λ explicite)

**Notations.** C = C(σ) et R = {h : hσh⁻¹ = σ⁻¹} = C r0, où r0 est le réverseur canonique (x ↦ −x sur chaque cycle).

**Énoncé.** A_λ est la réunion disjointe des 6 ensembles du tableau, chacun de cardinal z_λ = |C|. Donc
|A_λ| = 6 z_λ.

| τ | (π0, π1, π2) | image de T = (M0, M1, M2) |
|---|---|---|
| id | (g, g, g), g ∈ C | (gM0, gM1, gM2) |
| (0 1 2) | (g, g, gσ) | (gσM2, gM0, gM1) |
| (0 2 1) | (g, gσ, gσ) | (gσM1, gσM2, gM0) |
| (1 2) | (h, hσ, hσ), h ∈ R | (hM0, hσM2, hσM1) |
| (0 1) | (h, h, hσ) | (hM1, hM0, hσM2) |
| (0 2) | (h, h, h) | (hM2, hM1, hM0) |

**Preuve.**
- On écrit, pour chaque τ, les trois équations « s′ = (id, id, σ) » avec les formules du §1.1.
- Pour τ = id : π1 = π0, π2 = π1 et π0 σ π0⁻¹ = σ.
- Pour la rotation : π1 = π0, π2 = π0σ et π2 = σπ1. Donc π0 ∈ C.
- Pour τ = (1 2) : π1 = π2, π2 = π0σ et π0 = σπ1 = σπ0σ. Donc π0 σ π0⁻¹ = σ⁻¹.
- Les trois autres τ se traitent de même.
- Contrôle d'ordre :
  - |O_λ| = (n!)²·n!/z_λ, car on choisit s01 et s12 librement, puis σ dans sa classe de conjugaison ;
  - |W| = 6 (n!)³ ;
  - donc |A_λ| = 6 z_λ, et les six ensembles l'épuisent. □

- Les six images sont vérifiées sur le graphe par le test (b), sur 14 types λ.
- **Conséquence.** On pose s = σ et r = r0. L'orbite de T sous A_λ est la réunion des C-orbites (action diagonale)
  des six variantes :

      V0 = (M0, M1, M2)          V1 = (sM2, M0, M1)            V2 = (sM1, sM2, M0)
      V3 = (rM0, rsM2, rsM1)     V4 = (rM1, rM0, rsM2)         V5 = (rM2, rM1, rM0)

  Pour les classes R, on écrit h = g r0 avec g ∈ C.

---

## 2. Comptes exacts

### 2.1 Burnside par λ (P, E) : `enum37_burnside.py`

**Formule.**

    N_λ = [ Σ_{g∈C} f(g)³ + 2 Σ_{g∈C} f(σg³) + 3 Σ_{h∈R} f(h) f(h²) ] / (6 z_λ)

- f(p) est le nombre de couplages parfaits fixés par p.
- Points fixes des classes :
  - rotation : (M, gM, g²M) avec σg³M = M ;
  - (0 2) : (M0, M1, hM0) avec h²M0 = M0 et hM1 = M1.
- Les trois classes de transpositions donnent la même somme, car elles sont conjuguées dans A_λ (qui se projette sur S3).
  De même pour les deux 3-cycles, par l'inverse.
- **Calcul de f.** f(p) = Π_k g_k(c_k), où c_k est le nombre de k-cycles de p.
  - k impair : (c − 1)!! k^{c/2} si c est pair, 0 sinon.
  - k pair : Σ_j C(c, 2j)(2j − 1)!! k^j.
  - Raison : une arête invariante relie deux k-cycles (k façons), ou bien elle est un diamètre d'un cycle pair.
- **Les sommes, par le produit en couronne.** C = Π_k Z_k ≀ S_{m_k}, et g(j, x) = (βj, x + a_j).
  - Pour un β-cycle de longueur ℓ, de décalage total s (uniforme sur Z_k, de poids k^{ℓ−1}) :
    - g a pgcd(s, k) cycles de longueur ℓk/pgcd(s, k) ;
    - pour σg³, si 3 ∤ ℓ : décalage 3s + ℓ sur un ℓ-cycle de fibres ;
    - pour σg³, si 3 | ℓ : trois sous-cycles de longueur ℓ/3, de décalage s + ℓ/3.
  - Les réverseurs sont h(j, x) = (βj, b_j − x).
    - ℓ impair : h^ℓ est une réflexion c − x. On obtient #{2x = c} cycles de longueur ℓ et (k − #)/2 cycles de
      longueur 2ℓ. h² a k cycles de longueur ℓ.
    - ℓ pair : h^ℓ est une translation d. On obtient pgcd(d, k) cycles de longueur ℓk/pgcd(d, k). h² en a deux fois
      plus, de longueur moitié.
  - On convole sur les cycles de β (m!/z_μ choix de β de type μ), puis sur les blocs.
- **Contrôles (E).**
  - Les distributions calculées ainsi sont égales à celles obtenues en énumérant C(σ) et R(σ) dans S_n, pour n = 4, 6 et
    8, sur toutes les partitions.
  - La somme est toujours divisible par 6 z_λ.
  - Un Burnside C++ sur le groupe A_λ explicite (`enum37 --burnside`) redonne les mêmes N_λ pour les 68 λ avec
    z ≤ 20 000 à n = 12, et pour tous les λ avec z ≤ 20 000 à n = 8 et 10.

### 2.2 Total indépendant, Burnside direct sur H (P, E)

**Formule.**

    N = [ Σ_μ n_μ³ z_μ³ + 2|B|² Σ_μ n_μ z_μ + 3|B| Σ_μ a_μ n_μ z_μ r_μ ] / (6|B|³)

**Notations.**
- B = B_m ;
- n_μ = #{p ∈ B : type p = μ} ;
- a_μ = #{p ∈ B : type p² = μ} ;
- z_μ = |C_{S_n}(μ)| ;
- r_μ = nombre de racines carrées dans S_n d'une permutation de type μ.

**Dérivation par classe.**
- id : s01 conjugue π0 en π1, d'où z(π0)³ si les types sont égaux.
- Rotation : z(π2π1π0).
- (1 2) : z(π0²)·r(π1π2) si type π0² = type π1π2. En effet :
  - s01 π0² s01⁻¹ = π2π1 ;
  - (s12π2)² = π1π2.

**Résultats.** Les deux formules donnent le même total pour chaque n.

| n | classes | admissibles K ≥ 0 |
|---:|---:|---:|
| 4 | 24 | - |
| 6 | 886 | - |
| 8 | 204 367 | 144 414 |
| 10 | 141 318 684 | 106 405 725 |
| 12 | **187 381 435 694** | **147 579 095 390** |

**Coïncidences.** Les égalités N(…,2) = N(…,1,1), par exemple (10,2) et (10,1,1), ou (5,5,2) et (5,5,1,1), ont lieu
quand le reste de λ n'a pas de part 1 ni 2.
- Dans ce cas, C(σ) est le même groupe de permutations dans les deux cas : Z2 agit sur les deux points.
- Les distributions de σg³ et des réverseurs coïncident.
- Les orbites, elles, diffèrent.

### 2.3 Proposition 3 (critère K ≥ 0) (P, E)

**Énoncé.** On note K = nI − G − G² + 2J − J_cl.
- Diagonale : K_aa = n − 2.
- Dans une même classe, deux sommets distincts n'ont aucun voisin commun : un sommet a un seul voisin dans chaque autre
  classe et un seul partenaire. Donc K vaut 0 sur les partenaires et 1 sur les autres paires.
- Pour a ∈ C_c et b ∈ C_d avec c ≠ d :
  - s'ils sont adjacents, a′ ≁ b et b′ ≁ a (b a un seul voisin dans C_c). Donc G²_ab ≤ 1 et K_ab ≥ 0 automatiquement ;
  - sinon, K_ab = 2 − G²_ab, et les voisins communs possibles sont a′, b′ et un sommet de C_e. Donc K_ab < 0 si et
    seulement si a′ ~ b, b′ ~ a et a, b ont un voisin commun dans C_e.

**Lecture sur F_λ.**
- Classes (0,1) : {i, i′} ∈ M0 ∩ M1, et le voisin commun dans C2 existe si et seulement si i′ = σ^{±1}(i).
- Classes (1,2) : de même avec M1 ∩ M2.
- Classes (2,0) : {k, k′} ∈ M2 avec σ{k, k′} ∈ M0 et k′ = σ^{±1}k.

> **K ≥ 0 si et seulement si aucune σ-arête (avec σ(i) ≠ i) n'est dans M0∩M1, ni dans M1∩M2, ni dans σ(M2)∩M0.**

**Validation (E).**
- Test (d) : égalité avec la matrice K sur 3 000 tirages.
- Égalité exacte avec les verdicts K<0 de line37 sur les 212 847 classes des trois pilotes.

**Conséquences.**
- λ = (1¹²) est toujours admissible, puisqu'il n'y a aucune σ-arête.
- La fraction admissible dépend surtout du nombre de σ-arêtes : 0,7621 à 0,7622 pour les λ sans part ≤ 2, environ
  0,779 avec un point fixe, etc. (table, annexe).

### 2.4 Comptes admissibles exacts (E)

- **Burnside restreint (`enum37 --burnside --adm`)**, pour z ≤ 20 000 (68 λ). On utilise les trois types de points fixes
  ci-dessus, filtrés par la Proposition 3, et des sommes de sous-ensembles sur les masques de σ-arêtes.
- **Les 9 λ à z > 20 000** : énumération complète, `--fastcount --adm`.
- **Recoupement** : sur 8 λ, Burnside restreint = énumération (`B+E` dans l'annexe). À n = 8 et 10, Burnside restreint
  = énumération pour 21 λ et 40 λ.
- **Total** : 147 579 095 390 admissibles.
- **Cible t ≤ 7.** On retire (1¹²), (2,1¹⁰), (3,1⁹), (2²,1⁸) et (4,1⁸), soit 2 035 646 classes dont 1 881 197
  admissibles. Il reste 187 379 400 048 classes, dont 147 577 214 193 admissibles.

---

## 3. L'énumérateur canonique `enum37.cpp` (P pour l'algorithme)

### 3.1 Forme canonique

**Définition.** T est canonique s'il est le minimum lexicographique, sur l'orbite A_λ·T, du triple d'indices
(idx M0, idx M1, idx M2). L'ordre sur PM est le rang « plus petit point libre, puis rang du partenaire ».

**Calcul.** On a canonA(T) = min_j canonC(V_j). On calcule canonC(X, Y, Z) par la chaîne C ⊇ S(m0) ⊇ S(m0, m1) :
- m0 = min C·X, avec t·X = m0 (table de la racine, par BFS sur les générateurs de C) ;
- m1 = min S(m0)·(tY), avec t1 (table de niveau 1) ;
- troisième coordonnée : min S(m0, m1)·(t1 t Z) (table de niveau 2) ;
- les minimiseurs successifs forment les classes S(m0)t, puis S(m0, m1)t1t.

**Stabilisateurs.**
- On les obtient par les générateurs de Schreier et une clôture explicite. On a |S(m0)| ≤ |Stab_{S12}(M)| = 46 080.
- Contrôle d'orbite-stabilisateur à chaque m0 : |S(m0)|·|C·m0| = z_λ.

### 3.2 Génération et Proposition 4 (exactitude)

**Lemme (conditions nécessaires).** Les premières coordonnées des images couvrent C^±·M0 ∪ C^±·M1 ∪ C^±·M2, où
C^± = C ∪ R. Un triple canonique vérifie donc :
- M0 = min C^±·M0 ;
- min C^±·M1 ≥ M0 et min C^±·M2 ≥ M0 ;
- M1 = min S(M0)·M1, et M2 = min S(M0, M1)·M2 (car T = canonC(V0)).

**Boucles.**
- M0 parcourt les minima de C^±-orbite.
- M1 et M2 parcourent les matchings éligibles (min C^±-orbite ≥ M0) qui sont des minima de S(M0)-orbite et de
  S(M0, M1)-orbite.
- Seules les variantes à égalité de première coordonnée sont comparées par canonC : rootmin(V_j[0]) = M0. Pour les
  autres, canonC(V_j)[0] > M0.
- **Raccourcis** quand S(M0) est trivial :
  - V3 vaut (M0, φM2, φM1), avec φ = t3 r0 σ fixe pour M0 (table) ;
  - V4 vaut (M0, a4, t4 r0σ M2), avec a4 fixe pour M1. Si a4 < M1, tout M1 est rejeté. Si a4 > M1, V4 est sans effet.
    Si a4 = M1, on teste M2 par M2.

> **Proposition 4.** La sortie contient exactement un triple par orbite de A_λ : le minimum lexicographique de l'orbite.
>
> **Preuve.**
> - Un triple accepté vérifie T = canonC(V0) et T ≤ canonC(V_j) pour tout j. C'est donc le minimum de son orbite.
> - Réciproquement, le minimum de toute orbite satisfait les conditions de génération, donc il est visité, et le test
>   l'accepte.
> - `--adm` filtre une propriété invariante.
> - `--slice i/n` partitionne les paires (M0, M1). □

### 3.3 Mise en œuvre et usage

    enum37 <lambda> [--adm] [--slice i/n] [--count | --fastcount] [--triples] [--selftest k] [--burnside] [--random k s]

- **λ** s'écrit « 5,4,2,1 », « 12 » ou « 1^12 ». La notation mixte « 2,1^10 » n'est pas acceptée : écrire la liste
  complète.
- **Sortie** : 36 entiers par ligne, s01 s12 s20, en forme standard. Elle se branche sur `line37 file` ou
  `line37_fast file`.
- **Options.**
  - `--fastcount` : même règle d'acceptation, mais comptage en bloc des M2 qui ne peuvent pas être à égalité ; sert à la
    validation.
  - `--burnside` : Burnside sur le groupe explicite.
  - `--random` : tirages uniformes non canoniques pour un λ.
- **Construction** : `g++ -O2 -std=c++17 [-DNCL=12] enum37.cpp`. NCL est la taille des classes : 4, 6, 8, 10 ou 12.
- **Mémoire.**
  - Racine et niveau 1 : moins de 1 Mo.
  - Tables de niveau 2 : 20 Ko chacune, plafonnées à 6 000, vidées entre deux M1. Le maximum observé est de 771 tables.
- **Vitesse mesurée (n = 12).**
  - Grands groupes (z ≥ 1 000) : 2 à 5·10⁶ classes/s en comptage, par exemple (3,3,3,3) en 25 s et (2⁶) en 2,2 s.
  - (12) en `--fastcount` : 15 602 163 591 classes en 83 s.
  - Sortie texte : environ 1 à 3 µs par ligne. Par exemple, (3,1⁹) donne ses 182 221 lignes en 0,5 s.

---

## 4. Validation (E)

| contrôle | taille | résultat |
|---|---|---|
| `enum37_validate_group.py` 3000 7 : action sur le graphe et formules (a), images de A_λ (b), invariant (c), critère K (d), conversion (e) | 3 000 tirages, 14 types λ | 0 échec |
| distributions en couronne contre énumération de C(σ), R(σ) dans S_n | n = 4, 6, 8 : toutes les partitions | identiques |
| Burnside par λ contre Burnside direct sur H | n = 4, 6, 8, 10, 12 | totaux égaux |
| force brute : orbites de H sur X, sans λ (`enum37_brute.cpp`) | N = 4 : 13 824 triples ; N = 6 : 373 248 000 triples | 24 et 886 orbites, comptes par λ = Burnside |
| sortie de l'énumérateur N = 6 contre force brute (mode check) | 886 lignes | 0 doublon, X entièrement couvert (avant et après la réécriture de la boucle) |
| énumérateur (complet et `--fastcount`) contre Burnside | N = 8 : 22/22 λ ; N = 10 : 42/42 λ | égal |
| énumérateur `--adm` (complet = fast) contre Burnside restreint | N = 8 : 21 λ ; N = 10 : 40 λ (z ≤ 20 000) | égal |
| énumérateur contre Burnside, N = 12 | 21 λ : les 20 plus petits N et (12), soit 16 501 418 242 classes (8,8 %) | égal |
| autotest canonA contre minimum de force brute sur A_λ, N = 12 | 21 λ, 3 000 triples (z ≤ 1 944) ou 150 (z ≥ 4 320), égalités forcées | 0 écart |
| Burnside C++ sur le groupe explicite contre formule Python, N = 12 | 68 λ (z ≤ 20 000) | égal |
| K<0 de line37 contre N − N_adm | 3 pilotes | 0, 1 024, 12 927 : égal |

**Pas vérifié.** Le compte complet de l'énumérateur pour les 56 autres λ à N = 12 (1,709·10¹¹ classes) n'a pas été
fait (§8).
- Le code est le même pour tous les N.
- L'exactitude repose, pour ces λ, sur la Proposition 4, les autotests et la validation complète à N ≤ 10.

---

## 5. Pilote (E)

- **Procédure.** `enum37 λ > reps.txt`, puis `line37 file reps.txt 60`. Une seule tâche à la fois, au plus 4 min par
  passe ; (3,1⁹) est coupé en deux moitiés.
- **λ de plus petit N : (1¹²), 790 classes.**
  - Aucune K<0 (Proposition 3), 210 disconnected, 144 7-torsion et 230 L23.
  - **206 no-x** : chaque sommet de C0 est dans un triangle transversal, donc le moteur n'a pas de x. Ces 206 classes
    ne sont pas décidées.
  - t = 12 > 7 : elles sortent de la cible de THEOREME_REDUCTION_R37 (A), qui ne se sert que de P ≤ 852.
- **(2,1¹⁰), 29 836 classes.**
  - 1 024 K<0, 3 145 disconnected, 5 050 7-torsion et 10 426 L23.
  - **10 191 UNSAT**, 0 SAT, 0 TIMEOUT.
  - Droite testée : 5,7 ms en moyenne, 16 ms au plus, 514 nœuds au plus.
  - Passe complète : 59 s.
- **(3,1⁹), 182 221 classes.**
  - 12 927 K<0, 11 408 disconnected, 25 092 7-torsion et 66 567 L23.
  - **66 227 UNSAT**, 0 SAT, 0 TIMEOUT.
  - Droite testée : 6,5 ms en moyenne, 145 ms au plus, 812 nœuds au plus.
  - Deux passes de 204 s et 234 s.
- **Ce que ce n'est pas.** Les disconnected (c ≥ 2) et les 7-torsion relèvent d'autres moteurs (star_prep_gen, c1t,
  c1tt). Ces trois λ ne sont donc fermés que pour les classes que line37 traite (c = 1, d = 1).

---

## 6. Coût projeté (E)

**Échantillon par λ.**
- Pour chacun des 77 λ : `enum37 λ --random 200`, puis `line37 file`. Fichier `enum37_logs/sample_lambda_200.jsonl`,
  137 s au total.
- Pondéré par les N_λ exacts, cela donne les fractions suivantes :
  - K<0 : 21,0 % (exact : 21,24 %) ;
  - disconnected : 0,04 % ;
  - 7-torsion : 12,2 % ;
  - L23 : 33,6 % ;
  - testées : 33,1 %, soit environ 6,2·10¹⁰ classes, à 31,5 ms en moyenne.

**`line37.exe`.**
- Σ_λ N_λ × (ms par ligne)_λ = 1,96·10⁹ s, soit environ 5,4·10⁵ heures-cœur.
- C'est cohérent avec les 12,4 ms par tirage du recensement rand 100 000 (graine 777001, `runs/line37_rand100k.json`),
  qui donne 6,5·10⁵ heures-cœur, sur un PC chargé.
- Le coût varie selon λ :
  - environ 21 à 31 ms par droite testée pour les λ avec points fixes ;
  - environ 37 à 40 ms sans point fixe.

**`line37_fast`.**
- NOTE_LINE37_FAST (E là-bas) mesure un gain de 10,2 à 10,7.
- On obtient environ 1,9·10⁸ s, soit environ 5·10⁴ heures-cœur. NOTE_BOOST donne 6,5·10⁴ à partir de 1,2 ms par classe
  tirée.
- Ordres de grandeur : 2 à 3 jours sur 1 000 cœurs, environ 6 mois sur les 13 fils du PC du labo. **Ce n'est pas
  faisable en local dans les règles actuelles.**

**Énumération.** Environ 1,9·10¹¹ × 1 à 3 µs, soit moins de 2·10² heures-cœur. C'est moins de 0,5 % du test.

**Non couvert par line37** (moteurs à part, coût non mesuré ici) :
- les droites 7-torsion : environ 2,3·10¹⁰ ;
- les droites disconnected : environ 7,5·10⁷ ;
- les no-x : uniquement λ = (1¹²), t = 12.

**Premier pilote utile pour la cible t ≤ 7.** λ = (2⁶), t = 0, avec 4 157 364 classes dont 3 592 317 admissibles. Coût
estimé : 12,35 ms par ligne avec `line37.exe`, soit environ 14 h, ou environ 1,4 h avec `line37_fast`. Non lancé.

---

## 7. Ce qui pourrait rendre l'énumération (ou le test) plus petit

1. **K ≥ 0 sur couplages partiels** (Proposition 3).
   - Ce qui l'implémente :
     - test des σ-arêtes de M0∩M1 dès la paire (M0, M1) : `kprune1` élimine des M1 entiers avant la boucle M2 ;
     - après M2 : σ-arêtes de M1∩M2 et de σ(M2)∩M0 (`kprune2`).
   - Effet : −21,24 % des classes, exact.
   - Mais les K<0 coûtent environ 0,03 ms dans line37. Le gain porte sur les entrées-sorties, pas sur le test.
2. **t ≤ 7** (A : THEOREME_REDUCTION_R37, à partir de P ≤ 852).
   - Le mécanisme tel que je le relis (P) : Σ_T t(T) = 2P sur les 231 droites. En effet, un triangle transversal U de
     G_T forme avec T un prisme induit, et chaque prisme est compté par ses deux triangles.
   - On retire 5 λ et 2·10⁶ classes.
   - C'est surtout la façon propre d'éviter le trou no-x de λ = (1¹²).
   - Une meilleure borne sur P ne gagnerait presque rien : la masse est à t ∈ {0, 1, 2}.
3. **Ordre et priorités par λ.** La table de l'annexe donne N_λ, N_λ^adm et le coût par ligne. Cela permet de découper
   en tranches (`--slice`) de durée connue, et de commencer par les λ de grand groupe (petits N).
4. **Ce qui ne marche pas.** Il n'y a pas de condition sur couplages partiels pour le test d'étoile :
   - Ω = (3I − G + J)⁻¹ mod 7 et Z sont globaux ;
   - L23 et la 7-torsion dépendent de τ mod 7 (déterminant global) ;
   - les mises à jour de rang 12 quand seul M2 change (Woodbury) ne toucheraient que la préparation, soit 0,15 ms sur
     3,4 ms avec line37_fast.
5. **Le levier réel est le coût par droite testée.**
   - Exemple : choisir le x de plus petit domaine au lieu du premier x hors triangle.
   - Ou une preuve qui remplace l'énumération : SYNTHESE_MECANISMES §3.7 (A) dit qu'aucun lemme court n'est connu.

---

## 8. Ce qui n'a pas été lancé (suspension à 16 h 33)

- **Compte complet de l'énumérateur à N = 12** pour les 56 λ restants.
  - Commande : `enum37 λ --fastcount [--adm]`, à comparer à `enum37_logs/enum37_burnside_m6.json` et
    `burn_n12.jsonl`.
  - Coût estimé : 1 à 5 h pour un cœur, en passes de 5 min (option `--slice`).
  - La passe (11,1) / (10,1,1) en cours a été arrêtée sans résultat.
- **Pilote t ≤ 7** sur (2⁶), et les λ suivants.
- **Certification des UNSAT.** line37 n'exporte pas de certificat (statut E).
- **Seconde voie de certification de l'énumération** : la formule de masse Σ_T 6z_λ/|Stab(T)| = nombre de triples
  étiquetés admissibles (THEOREME_REDUCTION_R37 §7.1). Elle n'est pas implémentée. L'égalité avec Burnside joue ce rôle
  pour les λ vérifiés.

---

## 9. Fichiers

**Dans `merge_2026-10-19/`.**
- `enum37.cpp` / `enum37.exe` : l'énumérateur (build NCL = 12).
- `enum37_burnside.py` : comptes de Burnside par λ et total sur H ; `--check-explicit` pour n ≤ 8.
- `enum37_validate_group.py` : contrôles (a) à (e).
- `enum37_brute.cpp` : force brute N = 4 et 6 (`census`, `check`).
- `enum37_tools/` : pilotes de validation et de pilote (`cmp_fast.py`, `burn_cmp.py`, `fast_all.py`, `sample_lambda.py`,
  `sum37.py`, `cmp_counts_sorted.py`).
- `enum37_logs/` :
  - tables de Burnside : `enum37_burnside_m*.log`, `enum37_burnside_m6.json` ;
  - force brute : `brute4_census.json`, `brute6_census.json`, `brute6_check_v2.json` ;
  - comparaisons : `cmp_fast_n8.json`, `cmp_fast_n10.json`, `cmp_counts_n12_part1.json`, `fast_all_n12.jsonl`,
    `burn_n8/10/12.jsonl`, `selftest_n12.jsonl` ;
  - échantillon : `sample_lambda_200.jsonl` ;
  - pilote (1¹²) complet : `pilot_1x12.txt`, `pilot_1x12.line37.jsonl` ;
  - pilotes (2,1¹⁰) et (3,1⁹) : statistiques de l'énumérateur.

**Dans `scratchpad/boost/runs/`.**
- Les listes complètes et les sorties line37 de (2,1¹⁰) et (3,1⁹) (environ 45 Mo) : `pilot_2x1x10*`, `pilot_3x1x9*`.
- Elles sont reproductibles à l'identique : l'énumérateur est déterministe.

---

## Annexe : table par λ (E)

**Colonnes.**
- **adm** : nombre de classes admissibles.
- **source adm** : B = Burnside restreint, E = énumération complète.
- **enum = B** : compte de l'énumérateur égal à Burnside à N = 12.
- **échantillon** : 200 tirages par λ passés à line37, dans l'ordre K<0 / disconnected / 7-torsion / L23 / UNSAT.
- **ms/ligne** : temps line37.exe moyen par tirage, sur le PC chargé.

| λ | z_λ | N_λ (classes) | adm | adm/N | source adm | enum = B | échantillon | ms/ligne |
|---|---:|---:|---:|---:|---|---|---|---:|
| (11,1) | 11 | 17019245250 | 13257877911 | 0.7790 | B | - | 38 / 0 / 24 / 65 / 73 | 11.30 |
| (12) | 12 | 15602163591 | 11891346490 | 0.7622 | B | oui | 45 / 0 / 22 / 73 / 60 | 11.62 |
| (9,2,1) | 18 | 10408611780 | 8281389796 | 0.7956 | B | - | 38 / 0 / 25 / 70 / 67 | 9.36 |
| (10,2) | 20 | 9368430622 | 7291692522 | 0.7783 | B | - | 45 / 0 / 25 / 70 / 60 | 11.49 |
| (10,1,1) | 20 | 9368430622 | 7459701071 | 0.7963 | B | - | 47 / 0 / 27 / 58 / 68 | 9.38 |
| (8,3,1) | 24 | 7800702687 | 6076396481 | 0.7790 | B | - | 42 / 0 / 28 / 65 / 65 | 10.62 |
| (9,3) | 27 | 6934016421 | 5284509888 | 0.7621 | B | - | 57 / 0 / 21 / 66 / 56 | 10.97 |
| (7,4,1) | 28 | 6686571910 | 5208704403 | 0.7790 | B | - | 46 / 0 / 18 / 69 / 67 | 10.11 |
| (6,5,1) | 30 | 6240648332 | 4861401156 | 0.7790 | B | - | 46 / 0 / 22 / 68 / 64 | 9.96 |
| (8,2,1,1) | 32 | 5859958376 | 4766246695 | 0.8134 | B | - | 35 / 0 / 35 / 58 / 72 | 9.72 |
| (8,4) | 32 | 5851325099 | 4459573266 | 0.7621 | B | - | 46 / 0 / 22 / 59 / 73 | 13.50 |
| (7,5) | 35 | 5349194334 | 4076874195 | 0.7621 | B | - | 51 / 0 / 29 / 60 / 60 | 12.11 |
| (6,3,2,1) | 36 | 5204547972 | 4140654771 | 0.7956 | B | - | 36 / 0 / 19 / 77 / 68 | 10.26 |
| (5,4,2,1) | 40 | 4684274290 | 3726853053 | 0.7956 | B | - | 38 / 0 / 26 / 65 / 71 | 11.31 |
| (7,3,2) | 42 | 4461065280 | 3471967728 | 0.7783 | B | - | 39 / 0 / 26 / 62 / 73 | 13.53 |
| (7,3,1,1) | 42 | 4461065280 | 3551943532 | 0.7962 | B | - | 46 / 0 / 17 / 64 / 73 | 9.77 |
| (6,4,2) | 48 | 3903919414 | 3038442205 | 0.7783 | B | - | 40 / 0 / 24 / 77 / 59 | 11.01 |
| (6,4,1,1) | 48 | 3903919414 | 3108466033 | 0.7962 | B | - | 43 / 1 / 19 / 73 / 64 | 8.24 |
| (9,1,1,1) | 54 | 3474887148 | 2828403774 | 0.8140 | B | - | 50 / 1 / 27 / 62 / 60 | 6.83 |
| (7,2,2,1) | 56 | 3348616400 | 2721422073 | 0.8127 | B | - | 36 / 0 / 25 / 76 / 63 | 9.13 |
| (5,3,2,1,1) | 60 | 3125329515 | 2541855151 | 0.8133 | B | - | 40 / 0 / 25 / 69 / 66 | 8.57 |
| (5,4,3) | 60 | 3120616380 | 2378202272 | 0.7621 | B | - | 56 / 0 / 25 / 61 / 58 | 10.58 |
| (8,2,2) | 64 | 2930605337 | 2329614312 | 0.7949 | B | - | 40 / 0 / 31 / 63 / 66 | 12.62 |
| (6,6) | 72 | 2601204858 | 1982619583 | 0.7622 | B | - | 51 / 0 / 24 / 64 / 61 | 12.16 |
| (7,2,1,1,1) | 84 | 2235820065 | 1859190885 | 0.8315 | B | - | 34 / 1 / 23 / 68 / 74 | 7.76 |
| (5,3,3,1) | 90 | 2080350722 | 1620411546 | 0.7789 | B | - | 35 / 0 / 24 / 69 / 72 | 10.48 |
| (6,2,2,1,1) | 96 | 1955432359 | 1624804196 | 0.8309 | B | - | 43 / 0 / 24 / 66 / 67 | 8.15 |
| (4,3,2,2,1) | 96 | 1953640902 | 1587581591 | 0.8126 | B | - | 32 / 0 / 24 / 86 / 58 | 9.00 |
| (4,4,3,1) | 96 | 1950464802 | 1519264745 | 0.7789 | B | - | 37 / 0 / 34 / 67 / 62 | 9.72 |
| (5,5,2) | 100 | 1874093606 | 1458640006 | 0.7783 | B | - | 38 / 0 / 22 / 73 / 67 | 13.37 |
| (5,5,1,1) | 100 | 1874093606 | 1492288439 | 0.7963 | B | - | 50 / 0 / 23 / 64 / 63 | 8.39 |
| (6,3,1,1,1) | 108 | 1737591285 | 1414235660 | 0.8139 | B | - | 31 / 0 / 38 / 69 / 62 | 6.59 |
| (6,3,3) | 108 | 1733956248 | 1321435209 | 0.7621 | B | - | 45 / 0 / 18 / 60 / 77 | 15.24 |
| (5,4,1,1,1) | 120 | 1563907390 | 1272916042 | 0.8139 | B | - | 38 / 0 / 29 / 68 / 65 | 6.40 |
| (5,3,2,2) | 120 | 1562860320 | 1242258300 | 0.7949 | B | - | 38 / 0 / 23 / 71 / 68 | 12.48 |
| (4,4,2,1,1) | 128 | 1465525286 | 1191933548 | 0.8133 | B | - | 40 / 0 / 26 / 67 / 67 | 7.82 |
| (4,3,2,1,1,1) | 144 | 1304458983 | 1084616393 | 0.8315 | B | - | 28 / 0 / 26 / 65 / 81 | 9.38 |
| (4,3,3,2) | 144 | 1301541193 | 1012881356 | 0.7782 | B | - | 42 / 0 / 29 / 61 / 68 | 12.46 |
| (4,3,3,1,1) | 144 | 1301541193 | 1036240155 | 0.7962 | B | - | 31 / 2 / 21 / 76 / 70 | 7.64 |
| (8,1,1,1,1) | 192 | 979872761 | 815388724 | 0.8321 | B | - | 33 / 1 / 25 / 70 / 71 | 6.22 |
| (5,2,2,1,1,1) | 240 | 783407119 | 665584335 | 0.8496 | B | - | 33 / 0 / 25 / 71 / 71 | 7.47 |
| (5,2,2,2,1) | 240 | 782197116 | 649386434 | 0.8302 | B | - | 43 / 0 / 24 / 83 / 50 | 7.22 |
| (4,4,2,2) | 256 | 733188798 | 582809691 | 0.7949 | B | - | 35 / 0 / 28 / 62 / 75 | 12.48 |
| (6,2,1,1,1,1) | 288 | 653914651 | 555957376 | 0.8502 | B | - | 34 / 1 / 18 / 83 / 64 | 6.07 |
| (6,2,2,2) | 288 | 652097835 | 529447626 | 0.8119 | B | - | 31 / 0 / 30 / 67 / 72 | 12.07 |
| (3,3,2,2,1,1) | 288 | 652078048 | 541753085 | 0.8308 | B | - | 29 / 0 / 10 / 82 / 79 | 9.80 |
| (3,3,3,2,1) | 324 | 578387361 | 460099755 | 0.7955 | B | - | 43 / 0 / 29 / 59 / 69 | 10.91 |
| (5,3,1,1,1,1) | 360 | 522584205 | 434819560 | 0.8321 | B | - | 25 / 0 / 29 / 70 / 76 | 6.68 |
| (4,2,2,2,1,1) | 384 | 489576176 | 415588727 | 0.8489 | B | - | 31 / 0 / 28 / 74 / 67 | 8.10 |
| (4,4,4) | 384 | 488002169 | 371951892 | 0.7622 | B | - | 53 / 0 / 26 / 55 / 66 | 13.04 |
| (4,2,2,1,1,1,1) | 768 | 245647971 | 213402736 | 0.8687 | B | - | 25 / 0 / 26 / 69 / 80 | 6.13 |
| (4,4,1,1,1,1) | 768 | 245179756 | 204023695 | 0.8321 | B | - | 19 / 1 / 22 / 79 / 79 | 6.76 |
| (7,1,1,1,1,1) | 840 | 224729921 | 191189900 | 0.8508 | B | - | 32 / 0 / 19 / 80 / 69 | 5.18 |
| (3,3,2,1,1,1,1) | 864 | 218088766 | 185387952 | 0.8501 | B | - | 28 / 0 / 19 / 85 / 68 | 5.80 |
| (3,2,2,2,1,1,1) | 864 | 217933428 | 189176594 | 0.8680 | B | - | 27 / 1 / 29 / 72 / 71 | 7.67 |
| (3,3,2,2,2) | 864 | 217534574 | 176586213 | 0.8118 | B | - | 28 / 0 / 22 / 74 / 76 | 13.31 |
| (3,3,3,1,1,1) | 972 | 193132116 | 157171561 | 0.8138 | B | - | 33 / 0 / 24 / 77 / 66 | 7.09 |
| (3,2,2,2,2,1) | 1152 | 163196211 | 138404926 | 0.8481 | B | oui | 35 / 0 / 20 / 80 / 65 | 9.80 |
| (5,2,1,1,1,1,1) | 1200 | 157510118 | 136929823 | 0.8693 | B | oui | 30 / 1 / 26 / 73 / 70 | 4.95 |
| (4,3,1,1,1,1,1) | 1440 | 131145468 | 111557400 | 0.8506 | B | oui | 26 / 1 / 19 / 91 / 63 | 4.48 |
| (4,2,2,2,2) | 1536 | 122560378 | 101637681 | 0.8293 | B+E | oui | 33 / 0 / 20 / 71 / 76 | 13.25 |
| (3,3,3,3) | 1944 | 96461652 | 73516417 | 0.7621 | B+E | oui | 51 / 0 / 29 / 60 / 60 | 12.04 |
| (3,2,2,1,1,1,1,1) | 2880 | 65756445 | 58413019 | 0.8883 | B+E | oui | 20 / 4 / 26 / 69 / 81 | 6.13 |
| (6,1,1,1,1,1,1) | 4320 | 43964236 | 38245092 | 0.8699 | B+E | oui | 31 / 2 / 21 / 87 / 59 | 3.26 |
| (4,2,1,1,1,1,1,1) | 5760 | 33033026 | 29360992 | 0.8888 | B+E | oui | 16 / 3 / 32 / 75 / 74 | 4.85 |
| (2,2,2,2,2,1,1) | 7680 | 24645986 | 21832500 | 0.8858 | B+E | oui | 17 / 0 / 23 / 80 / 80 | 10.18 |
| (2,2,2,2,1,1,1,1) | 9216 | 20611995 | 18695487 | 0.9070 | B+E | oui | 12 / 1 / 31 / 82 / 74 | 6.00 |
| (3,3,1,1,1,1,1,1) | 12960 | 14685530 | 12773649 | 0.8698 | B+E | oui | 33 / 2 / 28 / 67 / 70 | 4.37 |
| (5,1,1,1,1,1,1,1) | 25200 | 7590151 | 6750683 | 0.8894 | E | oui | 21 / 2 / 15 / 80 / 82 | 4.01 |
| (3,2,1,1,1,1,1,1,1) | 30240 | 6341589 | 5763241 | 0.9088 | E | oui | 19 / 1 / 29 / 73 / 78 | 4.26 |
| (2,2,2,1,1,1,1,1,1) | 34560 | 5558856 | 5158678 | 0.9280 | E | oui | 7 / 2 / 29 / 84 / 78 | 4.75 |
| (2,2,2,2,2,2) | 46080 | 4157364 | 3592317 | 0.8641 | E | oui | 33 / 0 / 20 / 73 / 74 | 12.35 |
| (4,1,1,1,1,1,1,1,1) | 161280 | 1208078 | 1098783 | 0.9095 | E | oui | 13 / 3 / 23 / 67 / 94 | 4.14 |
| (2,2,1,1,1,1,1,1,1,1) | 322560 | 614721 | 583518 | 0.9492 | E | oui | 9 / 4 / 33 / 76 / 78 | 3.58 |
| (3,1,1,1,1,1,1,1,1,1) | 1088640 | 182221 | 169294 | 0.9291 | E | oui | 13 / 7 / 24 / 78 / 78 | 3.14 |
| (2,1,1,1,1,1,1,1,1,1,1) | 7257600 | 29836 | 28812 | 0.9657 | E | oui | 3 / 9 / 33 / 68 / 87 | 2.52 |
| (1,1,1,1,1,1,1,1,1,1,1,1) | 479001600 | 790 | 790 | 1.0000 | E | oui | 0 / 16 / 39 / 71 / 0 (no-x 74) | 0.03 |
| **total** | | **187381435694** | **147579095390** | 0.7876 | | 21 λ | | Σ = 1,96·10⁹ s |
