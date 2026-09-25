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
