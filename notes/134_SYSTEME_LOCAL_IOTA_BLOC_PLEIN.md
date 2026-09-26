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
