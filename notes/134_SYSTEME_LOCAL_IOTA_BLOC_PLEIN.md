# 134 — Système local (i)–(iii) et ι = ΦσΦ⁻¹ au bloc plein : lemme mono-bloc, quasi-2-facteurs

*27/09, nuit. C1, en appui de la piste de « structures » (involution/iota_*.py, 8d1988c) : le système local (i)+(ii)+(iii)
serait infaisable en tout type de bloc à m = 7 (≈ 10⁻¹⁰ solution attendue par type, contre 10⁴⁸ à m = 11). DÉRIVÉ = preuve
écrite.*

## 0. Énoncés
| énoncé | statut |
|---|---|
| **Lemme mono-bloc** (bloc plein, p sur un D-cycle de longueur ≥ 3) : au plus un quadruplet e ∪ ι(e) contient 3 des 4 étiquettes spéciales Sp_p = {p±, m(p±)}, aucun ne les contient toutes | DÉRIVÉ |
| Moments d'ordre 2 (niveau blocs et niveau étiquettes) : PSD, noyau = équilibre par D-cycle (blocs), trivial (étiquettes) | calcul exact |
| Reformulation de (i)+(ii) en quasi-2-facteurs G_a et R_b | DÉRIVÉ |
| Farkas globaux (ι #0, #1, #3 du 6-cycle) : pas de motif uniforme | calcul |
| **Extension (§6)** : en tout type, pour p ancré en c et non frère, a₃ + 3a₄ + Σ_{S_p}(k − 1)⁺ + #{Q ∉ S_p : k = 0} = 1 − [dg]. Digone ancré ⟹ équilibre (v) ; bloc chemin ⟹ exactement un excès | DÉRIVÉ, coupes relues et codées |

## 1. Cadre (« structures »)
- Bloc plein c : μ = τ = m, un couplage des 12 étiquettes entre blocs voisins du graphe D.
- ι := Φ σ Φ⁻¹ est un couplage des 60 paires non-μ. Les 30 quadruplets Q = e ⊔ ι(e) (sans annulation au bloc plein) forment
  un quasi-2-design : λ = 3 pour une paire générique, 2 pour une paire π, 1 pour une paire m.
- Étape 2 : on affecte les quadruplets aux 30 σ-paires, 2 par paire de blocs, en respectant (ii).
- (ii) sommée sur un bloc p donne la couverture c_p(b) = K2[p+,b] + K2[p−,b] = 4 − 2[b ∈ p±] − 2[b ∈ m(p±)].

## 2. Lemme mono-bloc
Soit S_p les 10 quadruplets sur les paires de blocs passant par p, et k_Q = |Q ∩ Sp_p|.
- On a Σ_{Q∈S_p} k_Q = Σ_{b∈Sp_p} c_p(b) = 8, donc **Σ_{Q∈S_p}(1 − k_Q) = 2**.
- Donc #{Q ∈ S_p : k_Q = 0} = 2 + Σ_{Q∈S_p}(k_Q − 1)⁺ ≥ 2.
- C'est exactement le certificat de Farkas de l'IIS à 12 lignes de ι #2 : y = −1 sur Sp_p, +1/3 ailleurs.
- **Inclusion–exclusion sur le quasi-design.** Soit a_k = #{Q : k_Q = k}. Alors a₀ = 30 − 40 + Σλ(Sp_p) − a₃ − 3a₄.
  - Si p est sur un D-cycle de longueur ≥ 3, m(p+) et m(p−) sont dans deux blocs différents. On a alors
    Σλ = 2 + 1 + 1 + 3 + 3 + 3 = 13, donc a₀ = 3 − a₃ − 3a₄, et **a₃ + 3a₄ ≤ 1**.
  - Pour un digone {p, q} : Σλ = 12, donc a₃ = a₄ = 0 et a₀ = 2. C'est l'équilibre par D-cycle, déjà connu : les deux quadruplets
    qui évitent Sp_p sont forcés sur la paire de blocs {p, q}.
- ι #2 (6-cycle) meurt ainsi au bloc 0 : un seul quadruplet évite {0, 1, 3, 10}.
- **Usage** : ce sont des contraintes linéaires sur les indicatrices de ι-paires. On les ajoute à l'étape 1 (construction de ι) ;
  voir « structures », partie (a).
- Hors bloc plein (ÉTL), le même certificat donne un surplus nul : 6 étiquettes à 4, 4 à 3, 2 à 2. Aucun évitement n'est forcé.

## 3. Moments d'ordre 2 : pas d'obstruction uniforme
- **Niveau blocs.** Le Gram des lignes [1_Q | 1_{β(Q)}] est forcé : [[Λ, C], [Cᵀ, 8I + 2J]].
  - Il est PSD pour 6cyc, 24, 33 et 222, de rangs 17, 16, 16, 15.
  - Son noyau est l'équilibre par D-cycle, n_K(Q) = 2 − |β(Q) ∩ K|, plus le vecteur trivial.
  - Toute agrégation à poids constants par type (propre, m, reste) est automatiquement satisfaite.
- **Niveau étiquettes.** Le Gram de [1_{r(e)} | 1_e] vaut [[9I + J − P_σ, K2], [K2ᵀ, 9I + J − P_m]]. Il est PSD, de noyau trivial.
- « structures » : le tenseur à 3 indices est PL-faisable sur 3 000 types, et les moments M± sont PSD sur 110 359 types.
- **Tout certificat uniforme doit donc dépendre de ι.**

## 4. (ii) en quasi-2-facteurs
- Au bloc plein, K2[a,b] = 2 − [b ∈ Sp(a)], avec Sp(a) = {a, σa, m a, m σa}.
- **Côté étiquettes.** Pour chaque étiquette a, les 10 moitiés {Φ(z) : z ∋ a} forment un graphe G_a sur les 12 étiquettes,
  de degré 1 sur Sp(a) et 2 ailleurs.
  - G_a est donc la réunion de **2 chemins** d'extrémités Sp(a) et de cycles, sans arête μ.
  - G_{σa} (les autres moitiés des mêmes quadruplets) a les **mêmes** extrémités. G_a ∩ G_{σa} = ∅, et ι échange G_a et G_{σa}.
- **Côté racines (dual).** Pour chaque étiquette b, les racines r(e) = Φ⁻¹(e) des 10 arêtes non-μ en b forment R_b, de degré 1
  sur block(b) ∪ block(m b) et 2 ailleurs : 2 chemins plus des cycles, sans arête σ.
  - R_b ne contient aucune σ-paire de racines, car il n'y a pas de ι-paire sécante au bloc plein.
- **Donc (i)+(ii)** ⟺ r : E(K₁₂ − μ) → E(K₁₂ − σ) est une bijection telle que :
  - r⁻¹(étoile de a) soit un quasi-2-facteur d'extrémités Sp(a) ;
  - r(étoile de b) soit un quasi-2-facteur d'extrémités block(b) ∪ block(m b).
- **(iii)** : ι = r⁻¹σr a les comptes croisés K₃.
- **Bloc général** : G_a a pour extrémités {a, σa, μa, τσa}, et R_b a pour extrémités {b, σb, μb, στb}.
- Piste : une contrainte de graphe (chemins imposés) propage mieux qu'une égalité de comptes. Une obstruction uniforme pourrait
  venir d'un comptage des chemins de G_a contre ceux de R_b, via σ(r(e)) = r(ι(e)).

## 5. IIS de l'étape 2 au niveau blocs (6-cycle, 4 ι de « structures »)
- ι #2 : 12 contraintes à un seul bloc (§2).
- ι #0, #1, #3 : IIS de 81 à 84 contraintes sur les 6 blocs (12 propres, 12 m, 42 à 47 reste, 11 à 13 lignes Q, 1 à 3 lignes bp).
- Leurs poids de Farkas, classés par relation (propre / m / reste à distance cyclique 1, 2, 3), sont dispersés dans [−1, 1] :
  aucun motif uniforme.

## 6. Extension à tout type : blocs ancrés non frères (27/09 matin)
*Avec « structures » : l'énoncé en coupe est dans NOTE_S29 §9, relu par C1. L'égalité et ses deux conséquences sont de C1 ;
« structures » a refait la preuve du digone (lab 59c3449).*
- **Cadre.** Un bloc c de type quelconque. Un bloc p est ancré en c si p± sont des pivots (μp± = τp±). On le suppose **non
  frère** : μp+ ≠ p−. On pose Sp = {p±, μp±}.
  - Les μp± sont aussi des pivots, car τμp+ = ττp+ = p+ = μμp+.
  - Donc K3[b,b] = 2 − 2[μb = τb] = 0 sur Sp : aucun quadruplet sécant n'est centré dans Sp, et k compte les étiquettes avec
    leur multiplicité.
  - Pour un bloc frère, Sp = {p±} et la couverture est nulle : l'énoncé est vide.
- **Couverture.** c_p(b) = 4 − 2[b ∈ p±] − [b ∈ μp±] − [b ∈ τp±], ce qui vaut 2 sur Sp et 4 ailleurs. Donc
  #{Q ∈ S_p : k = 0} = 2 + Σ_{S_p}(k − 1)⁺.
- **Inclusion–exclusion.** Σλ(Sp) = 2 + 1 + 1 + 3 + 3 + 3 − [dg], avec [dg] = 1 si μp+ et μp− sont dans un même bloc q (digone
  {p, q}). Donc a₀ = 3 − [dg] − a₃ − 3a₄.
- **Égalité** (on combine les deux) : **a₃ + 3a₄ + Σ_{Q∈S_p}(k_Q − 1)⁺ + #{Q ∉ S_p : k_Q = 0} = 1 − [dg].**
  - Elle n'utilise que (i), (ii) sommée sur p et (iii) sur Sp × Sp.
  - La coupe codée par « structures » (--cuts) en retient a₄ = 0 et a₃ ≤ 1 − [dg].
- **Digone ancré {p, q}, dans tout type : k_Q = 2 − |β(Q) ∩ {p, q}| pour chaque σ-paire.** C'est l'équilibre (v) du bloc plein,
  étendu.
  - Preuve : Sp_q = Sp_p, et le membre de droite vaut 0 pour p comme pour q. Donc k ≤ 1 sur S_p ∪ S_q, et k ≥ 1 hors de S_p
    comme hors de S_q.
  - Σ_{S_p} k = 8 force k = 1 sur S_p \ S_q (qui est hors de S_q), puis k = 0 sur les 2 σ-paires de {p, q}.
  - Σ_Q k = 40, avec a₃ = a₄ = 0, force k = 2 sur les 12 σ-paires restantes.
  - Codé par « structures » : --digon, dans les deux encodages.
- **Bloc chemin ([dg] = 0) : il y a exactement UN excès.** Exactement un des trois événements suivants a lieu, une seule fois :
  - une σ-paire hors de S_p à k = 3 ;
  - une σ-paire de S_p à k = 2 ;
  - une σ-paire hors de S_p à k = 0.
  - Jamais k = 4, jamais k ≥ 3 sur S_p.
- **Contrôles.**
  - Les hypothèses tiennent sur les 1 521 classes à pivots : 405 blocs ancrés non frères (243 chemins, 162 digones) et 501 frères.
  - lemma_cuts coïncide avec une génération indépendante faite depuis l'énoncé (0 écart).
  - L'identité a₀ = 3 − [dg] − a₃ − 3a₄ tient sur des ι de l'étape 1 (tier8_rel 0, 1, 3, 5 et 6). L'ι du type 5 meurt par la coupe.
  - L'égalité n'est testée ni en calcul ni en SAT : aucune solution complète n'est connue à m = 7.
- **Portée.** Le digone touche 21 des 79 types pertinents (25 paires digones), dont tier8_0, la sonde restée inconnue après 1 h
  chez C2.

## 7. Blocs tordus : l'identité à trois excès (27/09 matin, pour les 7 types (0,6))
- **Cadre.** Un bloc p est tordu en c : une seule étiquette pivot p*, avec μp* = τp* = q* dans un autre bloc, et p° non pivot.
  On pose S = {p*, p°, q*}. k_Q compte les places de Q dans S **avec multiplicité** : K3[b,b] = 2 − 2[b pivot], donc p° est le
  centre sécant d'exactement un quadruplet, et p*, q* d'aucun.
- **Couverture.** c_p vaut 2 sur S, 3 sur μp° et τp°, 4 ailleurs. Donc #{Q ∈ S_p : k = 0} = 4 + Σ_{S_p}(k − 1)⁺.
- **Inclusion–exclusion.** Σλ(S) = λ(p*,p°) + λ(p*,q*) + λ(p°,q*) + λ(p°,p°) = 2 + 1 + 3 + 1 = 7, avec k ≤ 4, donc
  a₀ = 7 − a₃ − 3a₄.
- **Égalité : a₃ + 3a₄ + Σ_{Q∈S_p}(k_Q − 1)⁺ + #{Q ∉ S_p : k_Q = 0} = 3.** Un type (0,6) en porte 6.
- **Bonus (0,6)**, de (i) et (iii) seuls : Σ_Q (k_P(Q) − 2)² = 18, où k_P est le nombre d'étiquettes pivots de Q.
- **Contrôles.**
  - La couverture et Σλ = 7 tiennent sur les 2 812 blocs tordus des 1 521 classes à pivots (iota_design.K2K3), avec 0 écart.
  - a₀ = 7 − a₃ − 3a₄ et le bonus tiennent exactement sur des ι de l'étape 1 de deux types (0,6), soit 12 blocs, avec a₀ = 6 ou 7.
- Proposé à « structures » et C2 comme option --twist des encodages ; relu et codé par « structures ». Sur une sonde à deux
  blocs de T = K₇, twist + CROSS donne UNSAT en 0,4 s.

## 8. L'identité générale et son balayage (`code/ident_scan.py`, `data/ident_tight.json`)
- **Énoncé.** Pour tout ensemble d'étiquettes S, places comptées avec multiplicité, et tout bloc p :
  **a₃ + 3a₄ + Σ_{Q∈S_p}(k_Q − 1)⁺ + #{Q ∉ S_p : k_Q = 0} = 20 − 10|S| + Λ(S) + C_p(S)**, avec
  Λ(S) = Σ_{b<d∈S}([non-μ] + K3[b,d]) + Σ_{b∈S} K3[b,b]/2 et C_p(S) = Σ_{b∈S}(K2[p+,b] + K2[p−,b]).
- **Preuve.** Pour k ≤ 4 : 1 − k + C(k,2) = [k=0] + [k=3] + 3[k=4]. On l'utilise avec Σk = 10|S|, ΣC(k,2) = Λ(S) et la
  couverture en p.
- §2, §6 et §7 en sont des cas particuliers : Sp ancré donne 1 − [dg] ; S₃ tordu donne 3.
- **Balayage des 3 308 classes, tous S et tous p.**
  - Aucun second membre négatif : aucune identité mono-bloc ne tue un type à elle seule.
  - 971 classes ont une identité de second membre ≤ 1.
  - Pour (0,6), le minimum vaut 3 : c'est S₃.
- **Famille nouvelle : le carré π.** C'est le cas d'un bloc p non pivot où μ(p+) = p− et où les τ-images t± forment une
  μ-arête : un 4-cycle de μ ∪ τ. Avec S = p± ∪ τ(p±), le second membre vaut 4 − 3[μt+ = t−] − [t− = πt+]. Il vaut donc 0 si
  les deux μ-arêtes sont des arêtes π. On a la même chose en échangeant μ et τ.
  - Dans les 79 types pertinents : 8 identités à 0 et 6 à 1.
  - Dans les étoiles libres : 243 types sur 1 787.
  - Aucune dans les 441 types P = 0 de Sol, où le minimum est ≥ 3.
