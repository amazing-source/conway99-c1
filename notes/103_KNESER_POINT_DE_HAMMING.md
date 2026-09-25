# 103 — Structure de Kneser en un point de Hamming : vers une preuve humaine de L8

*25/09, fin de matinée. Consigne de l'utilisateur : attaquer en maths pures la structure générique (graphe de Kneser),
en s'inspirant du Théorème D de la branche C2 (`conway99-involution/notes/MATH_C2_PROGRAMME.md`, autre machine ; lu,
aucun message envoyé à C2). Cible naturelle : **L8 (aucun point de Hamming)**, aujourd'hui établi seulement par SAT
non certifié. **Antériorité interne (corrigé à 11 h 15)** : le modèle en bijections φ, la règle de transport et le cas
isométrique (= L7, deux preuves à la main) sont déjà dans notes/20 et notes/95. Ce qui est nouveau ici : la forme
compacte (§1.5), une troisième preuve du cas isométrique par le graphe de Kneser signé (argument de C2, §2), les classes
d'holonomie des triangles (§3) et l'encadrement 7-adique 18 ≤ k ≤ 26 (§4). Le régime mixte (= L8) reste ouvert.*

## 0. Résumé
| résultat | énoncé | statut |
|---|---|---|
| réduction | en un point de Hamming x, H = ⊕_P C₄ + (couplages parfaits entre paires de classes disjointes) : une **S₄-connexion sur K(7,2)** soumise aux équations (K), (T) | preuve (déjà notes/20, 95 ; forme compacte nouvelle) |
| régime « tout A » | si tous les couplages préservent les paires antipodales : contradiction | = L7 (notes/95) ; 3ᵉ preuve par le Kneser signé de C2 |
| classification locale | autour d'une arête de Kneser, les 3 holonomies de triangle sont {id, dt, dt}, {tr, tr, dt} ou {id, 4c, 4c} | preuve + énumération exhaustive |
| encadrement 7-adique | **un point de Hamming force 18 ≤ k ≤ 26** | preuve + calcul exact |
| **régime « aucune arête isométrique »** | impossible ; version locale : pour toute classe i, au plus 2 des 6 paires ∋ i ont leurs 10 arêtes de Kneser non isométriques | **preuve (nouvelle)** + 2 énumérations exactes |
| régime mixte | ouvert | — |

## 1. Réduction (preuve)
*Notations.* Étiquettes = les 14 voisins de x, 7 classes {a, ā}. Paire de classes P = {i, j} : ses 4 sommets
{a_i^ε, a_j^η} ∈ Γ₂(x) ; siblings = deux sommets de P qui partagent une étiquette ; antipodes = {a,b} et {ā,b̄}.
*Point de Hamming* : τ_a(b) = b̄ pour toutes les étiquettes (les 21 grilles par x sont complètes).
1. Chaque y = {a,b} a pour τ-partenaires ses deux siblings {a,b̄}, {ā,b}, qui sont aussi ses partenaires d'holonomie. Il
   lui reste 10 voisins génériques, dans les 10 paires de classes disjointes de P(y).
2. **Au plus un voisin par paire disjointe P′.** Deux voisins siblings dans P′ seraient adjacents, avec deux voisins
   communs (l'étiquette partagée et y) : contradiction avec λ = 1. Deux voisins antipodaux auraient trois voisins
   communs (leurs deux siblings et y) : contradiction avec μ = 2. (C'est l'étape (2) du Théorème D de C2 ; ici sans
   involution.)
3. 10 voisins pour 10 paires : **exactement un par paire disjointe** (la coïncidence 2m − 4 = C(m−2, 2) ⟺ m = 7 de
   C2). Donc, entre deux paires disjointes, H est un couplage parfait φ_{PQ}.
4. Les conditions λ, μ sur Γ₂(x) s'écrivent, par blocs 4 × 4 (Π = matrice de φ, Sib = 4-cycle des siblings) :
   - (K) pour P, P′ disjointes : Σ_R Π_{PR}Π_{RP′} = 2J − Π_{PP′} − Sib_P Π_{PP′} − Π_{PP′} Sib_{P′}. Ici R parcourt
     les 3 paires de classes disjointes de P ∪ P′.
   - (T) pour P, P′ partageant la classe i : Σ_R Π_{PR}Π_{RP′} = 2J − E_i. Ici R parcourt les 6 paires disjointes des
     deux, et E_i[y,z] = [même étiquette de classe i].
5. *Décomposition en caractères.* L'espace des fonctions de somme nulle sur P (dimension 3) a une base naturelle : les
   caractères des 3 partitions de P en deux paires, π_i, π_j (par étiquette) et A (antipodale). Toute bijection φ y agit
   par une matrice de permutation signée, de produit des signes +1 (représentation standard de S₄). Sib|_W = −2·E_A.
   Sur les 63 dimensions orthogonales aux constantes par paire : **(M − 2E_A)² + (M − 2E_A) = 12(I − Proj_Z)**, où Z est
   engendré par les 7 vecteurs « étiquette m » Z_m (et M Z_m = 0). M est l'adjacence d'un revêtement triple signé de
   K(7,2).

## 2. Régime « tout A » (= cas isométrique de L7) : troisième preuve, par le Kneser signé de C2
Supposons que chaque φ_{PQ} envoie les paires antipodales de P sur celles de Q. Alors l'espace A des caractères
antipodaux (21 dimensions) est M-invariant, et M|_A = A_χ est une signature de K(7,2). Comme S_lab et J s'annulent sur A,
on a (A_χ − 2)² + (A_χ − 2) = 12, donc **A_χ² = 3A_χ + 10I**.
- *Arêtes de Kneser P, P′* : (A_χ²)_{PP′} = Σ_{R (3)} χ_{PR}χ_{RP′} = 3χ_{PP′}, donc tous les triangles sont équilibrés.
- *Paires partageant une classe* : (A_χ²)_{PP′} = Σ_{R (6)} χ_{PR}χ_{RP′} doit valoir 0.
- *Couples complémentaires.* Les 6 paires R vivent sur 4 classes et se groupent en 3 couples {R, R̄}. Les triangles
  (P, R, R̄) et (P′, R, R̄) sont équilibrés, donc χ_{PR}χ_{RP′} = χ_{PR̄}χ_{R̄P′}. La somme vaut 2(t₁ + t₂ + t₃), avec
  tᵢ = ±1 : c'est ±2 ou ±6, jamais 0. **Contradiction.** ∎

*Mise en garde.* J'avais d'abord cru que les arêtes A se propagent (« une arête A ⟹ toutes les arêtes A ») ; c'est
faux. Dans (K), une route P → R → P′ peut envoyer A sur A en passant par une partition-étiquette de R. Les régimes
mixtes existent donc a priori. (notes/95 le disait déjà : un triangle de Kneser contient 0, 2 ou 3 arêtes non
isométriques, jamais 1.)

## 3. Classification locale autour d'une arête (preuve + `code/kneser_edge_holonomy.py`)
θ_R = holonomie du triangle P → R → P′ → P. En composant (K) avec Π_{P′P} :
Σ_R Perm(θ_R) = 2J − I − Sib_P − Sib′ (Sib′ = 4-cycle de P′ ramené sur P).
- Arête A : cible I + 2ι, soit {id, dt, dt} ou {tr, tr, dt}.
- Arête non-A : cible I + M_c + M_A (chaque point reste une fois, va une fois vers son partenaire π_c, une fois vers
  son antipode ; jamais vers le partenaire π_{c′}). Solutions : {id, dt, dt}, {tr, tr, dt} (deux façons) ou
  {id, 4c, 4c}.
Jamais de 3-cycle. (Raffinement des « 9 / 18 / 6 arrangements » de notes/95.) |Fix θ_T| = ℓ(T) = nombre de droites de Γ de triple de paires T : 4 (id), 2 (tr), 0 (dt, 4c).
Contraintes de comptage : pour chaque arête, et pour chaque (P, classe m ∉ P), les trois triangles concernés ont des ℓ
de profil {4, 0, 0} ou {2, 2, 0} ; Σ ℓ = 140. Les contrôles de trace (tr M³ = 210, tr M⁴) sont automatiquement
satisfaits : **la contradiction, si elle existe, est combinatoire et non spectrale.** En effet, le régime « aucune
arête A » passe même le test des multiplicités (3²⁶, (−4)³⁰, 0⁷ se réalisent bloc par bloc).

## 4. Encadrement 7-adique : un point de Hamming force 18 ≤ k ≤ 26
- *k ≥ 18.* Chaque droite L par x est en « configuration grille » (σ = id, τ = mates) : d(L) = 6 (notes/99), donc
  k ≥ 23 − 6 = 17 (L21), puis k ≥ 18 par parité.
- *k ≤ 26.* Les 21 grilles G_P par x sont complètes. Pour une grille complète, tout sommet extérieur a exactement
  un voisin dans G : au plus un par ligne, et deux voisins non alignés auraient trois voisins communs. Donc
  (A − 3I)1_G = 1, et η_P = 11·1_{G_P} − 1 ∈ Λ₃. Gram exact : 990, 264 (P, Q partagent une classe), 22 (disjointes).
  Mod 7, c'est 3I + 5A_{T(7)} + A_{K(7,2)} : **rang 14, discriminant non carré** (`code/hamming_grid_gram.py`).
  Son radical est engendré par les ζ_m = Σ_{P ∋ m} η_P = 60·1_{L_m} + 5·1_{N(L_m)} − 6·1_{loin}, le vecteur propre
  canonique de la droite L_m. Or **ζ_m ≡ 5·Σ_{v ∈ L_m} f_v (mod 7) ∈ G**. Les η_P étant indépendants mod 7 (supports
  disjoints sur Γ₂(x)), leur image dans U′ = ρ₃/G est non dégénérée de dimension 14 (et scindée). Donc
  14 ≤ dim U′ = 40 − k, soit **k ≤ 26**. ∎
Ce n'est pas une contradiction (18 ≤ 26), mais c'est le premier plafond de k tiré d'une structure de torsion locale.

## 5. Suite (régime mixte)
- Le problème restant est fini et purement combinatoire : une S₄-connexion sur K(7,2), dont les holonomies de
  triangles suivent les profils du §3, et qui satisfait les équations (T) sur les 105 paires partageant une classe.
  Pour ces paires, la somme porte sur 3 couples complémentaires ; modulo 2 elle doit valoir le motif « même étiquette
  de classe i », non nul. Donc aucune paire (T) n'a ses 6 triangles concernés tous d'holonomie triviale.
- Piste : généraliser l'argument des couples complémentaires. Remplacer la signature (représentation de signe sur A)
  par l'holonomie complète dans S₄, en utilisant les deux triangles (P, R, R̄) et (P′, R, R̄) de chaque couple.

## 6. Le régime « aucune arête isométrique » est impossible (nouveau, 25/09 midi)
*Données.* Pour une arête de Kneser non isométrique (P, R), φ_{PR} envoie la partition antipodale A(P) sur une
partition-étiquette π_κ(R), avec κ = κ(P→R) ∈ R. Si toutes les arêtes issues de P sont non isométriques, orienter
chaque arête R de K₅([7] ∖ P) vers κ(P→R) définit un **tournoi T_P** sur les 5 classes hors de P.
*Deux ingrédients, tous deux vérifiés.*
- **(Z_A) Degrés entrants pairs.** μ(y, a_m) = 2 pour y ∈ Q_P et une étiquette a_m (m ∉ P) : parmi les 4 paires
  {m, n} disjointes de P, exactement 2 voisins de y contiennent a_m. En caractères, c'est M Z_m = 0 ; sa composante
  antipodale en P dit que le nombre de Q ∋ m avec κ(P→Q) = m est pair. **Dans T_P, chaque sommet a un degré entrant
  pair.**
- **(C′) Nombre pair d'isométries.** Soient P = {i,j}, P′ = {i,k}. Parmi les 6 transports ψ_R = φ_{P′R}⁻¹∘φ_{PR}, pour
  R ⊂ F = [7] ∖ {i,j,k}, le fait C impose un nombre **pair** d'isométries. (Énumération exhaustive : 58
  multi-ensembles compatibles, avec 0, 2, 4 ou 6 isométries, `code/factC_parity_check.py`. Même résultat que notes/95.)
  Si les deux arêtes sont non isométriques, ψ_R est une isométrie ssi κ(P→R) = κ(P′→R), c'est-à-dire si T_P et T_{P′}
  orientent R de la même façon. **T_P et T_{P′} s'accordent donc sur un nombre pair des 6 arêtes de K₄(F).**
*Preuve.* Soit D_P l'ensemble des arêtes que T_P oriente vers leur plus petite extrémité, et n(P) = |D_P| mod 2. Un
calcul de degré donne deg_{D_P}(v) ≡ in_{T_P}(v) + rang_P(v). Ici rang_P(v) est le nombre de classes de [7] ∖ P
inférieures à v. Avec (Z_A), cela donne deg_{D_P}(v) ≡ rang_P(v). Or |D_P ∩ E(F)| = |D_P| − deg_{D_P}(k), puisque
F = ([7] ∖ P) ∖ {k}. Par (C′), |D_P ∩ E(F)| ≡ |D_{P′} ∩ E(F)|, d'où
  **n({i,j}) + n({i,k}) ≡ rang_{ij}(k) + rang_{ik}(j) ≡ (j + [i<j]) + (k + [i<k]) + 1 (mod 2).**
Pour i fixé et trois classes j, k, l, on somme les trois relations (paires jk, kl, jl). À gauche, 0 ; à droite,
2(…) + 3 ≡ 1. **Contradiction.** ∎
*Version locale (même preuve).* L'argument n'utilise que les trois paires {i,j}, {i,k}, {i,l} et leurs 30 arêtes de
Kneser. **Pour toute classe i, au plus deux des six paires contenant i ont toutes leurs arêtes non isométriques.**
*Bilan pour L8.* Les deux régimes extrêmes sont exclus : tout isométrique (L7) et rien d'isométrique (ci-dessus).
Il reste les mélanges, qui sont contraints par :
- la règle des triangles : 0, 2 ou 3 arêtes non isométriques par triangle ;
- la version locale ci-dessus.
*Correction de notes/95.* En une arête non isométrique, le nombre de transports isométriques vaut **0 ou 2**, et non
« 0 ou 1 (6 arrangements) » (`code/transport_rule_check.py` : trois triplets sans isométrie, un avec deux). La
conséquence qu'en tirait notes/95 (un triangle n'a jamais exactement une arête non isométrique) reste vraie : elle
découle déjà du cas isométrique.
*Profil fin du fait C* (58 solutions) : autant d'isométries de décalage 0 que de décalage 1 ; les quatre types
non isométriques N(x, y) (A(P) ↦ π_x, π_y ↦ A(P′)) ont tous la même parité.

## 7. Version locale du cas isométrique, et ce qui manque pour le cas mixte
- **L7 local (nouveau).** Pour tout triplet de classes {i, j, k}, les 18 arêtes de Kneser entre {ij, ik, jk} et les
  6 paires de F = [7] ∖ {i, j, k} ne sont pas toutes isométriques. *Preuve.* Les trois équations de décalage de L7
  (triplets (i ; j, k), (j ; i, k), (k ; i, j)) portent sur les mêmes 6 paires R ⊂ F. Chacune donne
  Σ_R (δ(P, R) + δ(P′, R)) ≡ 1. Leur somme vaut 2Σ_R (δ(ij, R) + δ(ik, R) + δ(jk, R)) ≡ 0 à gauche et 3 ≡ 1 à droite. ∎
- **Décalage étendu** (`code/shift_extension.py`). Pour une application non isométrique d'image antipodale a, on pose
  δ = la coordonnée de translation complémentaire de a. Dans une arête non isométrique, deux transports concordants
  (N, N) composent alors en une isométrie de décalage δ(P, R) + δ(Q, R). La règle de transport donne, uniformément :
  **Σ_R δ(ψ_R) ≡ δ(φ_{PQ}) + [φ_{PQ} non isométrique]**. Mais δ étendu **n'est pas additif** : le défaut de
  composition dépend de la partie linéaire complète, et aucune extension à défaut « linéaire » n'existe (δ n'est pas
  S₃-invariant sur les translations). Les deux arguments (décalage de L7, tournois du §6) ne s'unifient donc pas
  directement.
- **Le cas mixte n'est pas exclu par les contraintes combinatoires seules.** Exemple de coupe : V₀ = les 6 paires
  incluses dans {1, 2, 3, 4}, V₁ = les 15 autres ; arêtes isométriques = arêtes internes à V₀ ou à V₁. Il vérifie :
  - la règle des triangles ;
  - L7 local ;
  - la version locale du §6 ;
  - le calcul de parité du §6 (le terme correctif ζ des arêtes isométriques le rend cohérent, vérifié à la main pour
    i = 1 et i = 5).

  Pour conclure, il faudra les parties de translation : les relations (Cδ), et la règle de transport aux arêtes
  traversant la coupe (3 transports non isométriques de Σδ ≡ 1 + δ). Pas de recherche par solveur : ce sera une
  analyse du cas « coupe », puis du cas avec triangles entièrement non isométriques.

## 8. Recherches annexes (25/09, après-midi), nouvelle planche, et le pont
**Littérature (rien sur cette configuration précise).**
- La famille srg(1 + 2m², 2m, 1, 2) n'existe que pour m = 2 (réseau 3 × 3), m = 11 (BvLS = graphe des classes du code
  de Golay ternaire) et éventuellement m = 7, 56, 497
  ([Makhnev, automorphismes λ = 1, μ = 2](https://www.degruyterbrill.com/document/doi/10.1515/156939204872374/html?lang=en)).
  **Un point de Hamming est une image locale « Golay factice » de H(7,3)** (notes/95). Globalement, cela demanderait un
  code parfait de longueur 7, qui n'existe pas (Tietäväinen–van Lint ; 3⁷/99 non entier : L1). L8 en est la version
  locale.
- [Brouwer–Neumaier 1988](https://link.springer.com/article/10.1007/BF02122552) (espaces linéaires partiels de
  maille 5, μ = 2) passe par le premier sous-constituant ; ici il vaut 7K₂, donc c'est sans prise.
- Pas de recouvrement avec [Keramatipour 2026 (SAT)](https://arxiv.org/pdf/2604.23037) ni avec
  [Lou–Murin 2014](https://math.mit.edu/research/highschool/primes/materials/2014/Lou-Murin.pdf).
- **Outils classiques repérés.**
  - En un point de Hamming, les 5 droites par un sommet de Q_P forment une quasi-1-factorisation de K₅, c'est-à-dire
    un « total » de Sylvester de K₆ (6 possibilités, automorphisme extérieur de S₆,
    [réf.](https://en.wikipedia.org/wiki/Automorphisms_of_the_symmetric_and_alternating_groups)).
  - Le sous-cas « holonomies sans transposition » mène à des familles de 1-factorisations, voisines des grands
    ensembles de plans de Fano (qui n'existent pas sur 7 points ; [STS](https://www.win.tue.nl/~aeb/graphs/STS.html)).
  - Pour les signatures à deux valeurs propres
    ([problème ouvert en général](https://arxiv.org/pdf/1907.04349)), notre cas se règle par H¹ = 0 : une signature de
    K(7,2) équilibrée sur tous les triangles est commutable en la signature triviale, de spectre {10, 1, −4} ≠ {5, −2}.
    C'est une preuve en une ligne de l'étape de C2.

**Nouvelle planche : la parité S₃ du fait C** (`code/factC_s3_types.py`).
- *Énoncé.* Lus dans S₃ (action sur les trois partitions), les 6 transports ont tous leurs types de même parité : ou
  bien chacun des 6 éléments de S₃ exactement une fois, ou bien tous les nombres pairs.
- *Conséquence (T).* Pour toutes partitions X de P et Y de P′, #{R : γ_R(X) = Y} est pair. En identifiant les
  partitions aux vecteurs non nuls de F₂² (A ↔ 11), γ_R devient L_{P′R}⁻¹L_{PR} ∈ GL(2,2), et
  **Σ_{R ⊂ F} L_{P′R}⁻¹ L_{PR} = 0** dans M₂(F₂).
- *Conséquence (Z), linéaire.* Avec [u = v] = 1 + ω(u, v) (ω symplectique), la condition « μ avec les étiquettes »
  devient **Σ_{R ∋ m} L_{PR}ᵀ Ω e_m(R) = 0**. Elle est linéaire en les parties linéaires, que l'arête soit
  isométrique ou non. Le cas « aucune isométrie » du §6 en est le cas particulier X = A.
- La seule non-linéarité restante est (T). C'est elle que les parties de translation doivent régler.

**Le pont.**
- *Planches posées.*
  - Cas tout isométrique et cas rien d'isométrique, avec versions locales.
  - Parité S₃.
  - Encadrement 18 ≤ k ≤ 26.
- *Planches suivantes (dans l'ordre).*
  1. Les parties de translation. Pour les isométries, le décalage additif δ ; pour le reste, les relations de
     transport Σδ(ψ_R) ≡ δ(φ) + [φ ∈ N].
  2. Le cas coupe.
  3. Les triangles entièrement non isométriques. Ils forment un 2-cycle mod 2, car une arête non isométrique est dans
     0 ou 2 d'entre eux.
- *La rive d'en face.* Chaque ingrédient utilisé (μ avec les étiquettes, fait C, règle de transport) est une condition
  SRG **universelle**. Le point de Hamming sert seulement à rendre les blocs calculables (des bijections). La
  contradiction de L7 vient d'une arithmétique propre à m = 7 : 3 = C(4,2)/2 est impair, et 105 = 7·15 triplets
  aussi. Pour m = 11, on a C(8,2)/2 = 14, pair, et BvLS survit : c'est la règle de cohérence de C2.
  La fin du pont, pour C1 tout entier, est donc **un comptage modulo 2 sur les 105 triplets (i ; j, k) d'un sommet
  quelconque**. Sa partie constante vaudrait 105·3 ≡ 1, et ses parties variables (blocs génériques 4 × 4 quelconques)
  s'annuleraient par double comptage. Il reste à établir que les corrections dues à la torsion (arêtes τ et
  d'holonomie) sont paires. **Discipline adoptée** : tout lemme général est testé sur BvLS (m = 11), où il doit
  rester vrai.

## 9. Relations à constante impaire, et réduction à une parité locale (`code/factC_affine_relations.py`)
- **Fonctions à parité constante.** Considérons les f : AGL(2,2) → F₂ dont la somme Σ_R f(ψ_R) a la même parité dans
  les 58 solutions du fait C. Elles forment un espace de dimension 10. **Certaines ont la constante 1** : par exemple
  f = [ψ(u) = z] pour u, z de même étiquette en i. C'est le fait C lui-même (exactement un R), valable pour **tous**
  les mélanges.
- **Somme globale.** Dans une jauge donnée (une étiquette « 0 » par classe), on prend u = 0_P et z = 0_{P′} pour chaque
  triplet. On somme sur les 105 triplets et on regroupe par l'intermédiaire R. On obtient **Σ_R Q_R = 105 (impair)**,
  avec Q_R = Σ_{m ∉ R} #{paires d'arêtes {e, e′} ∋ m de K₅([7] ∖ R) telles que t_{eR} = t_{e′R}}. Ici t_{eR} est la
  partie de translation de φ_{eR} ; de façon équivalente, 0_e et 0_{e′} ont un voisin commun dans Q_R.
  **Si chaque Q_R était pair, L8 serait démontré** (21 nombres pairs de somme 105).
- **Structure de Q_R.** Pour chaque arête e, w ↦ φ_{Re}(w) est une bijection. Les ensembles N_w = {e : w voisin de 0_e}
  (w ∈ Q_R) partitionnent donc les 10 arêtes de K₅. En chaque sommet m, μ(w, a_m⁰) = 2 fait des 4 arêtes en m un graphe
  2-régulier sur Q_R (un 4-cycle ou deux digones). On a alors Q_R ≡ #{m : répartition (2, 1, 1, 0)} (mod 2).
- **Limites.**
  1. Q_R dépend de la jauge : changer l'étiquette « 0 » d'une classe n modifie Q_R, et sa parité change d'une façon
     qui dépend de la configuration.
  2. Pour m = 11 (BvLS, où tout sommet est un point de Hamming), la même somme vaut 11·C(10,2) = 495, impaire, et BvLS
     existe. La parité de Q_R n'est donc **pas** un lemme général : elle devrait venir de la rigidité propre à m = 7 (un
     voisin par paire disjointe, qui fait des N_w une partition). C'est la règle de cohérence de C2.
  3. Aucune f de constante 1 n'est additive (f(φ′⁻¹φ) = g(φ) + g(φ′)) : le seul homomorphisme S₄ → F₂ est la
     signature, et elle n'est pas à parité constante (notes/95). Dans L7, c'est l'additivité de δ sur les isométries
     qui rendait Q_R automatiquement pair.
- **Prochaine planche.** Trouver une combinaison des relations du fait C (dans l'espace de dimension 10), éventuellement
  moyennée sur les jauges, dont la partie locale en R soit additive modulo les contraintes en R. Contraintes en R :
  μ exact avec les étiquettes, règle de transport sur les triangles (R, e, e′), classes d'holonomie.
