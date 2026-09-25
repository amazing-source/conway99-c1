# 114 — Labo expérimental C1 (démarche C3) : graphe lointain d'une droite, graphes réels de valeurs propres {3, −4}, équilibre

*25/09, soir. Sur demande de l'utilisateur, les trois sessions reprennent la **méthode expérimentale** du labo C3, et non
son contenu (clos : notes/113). Labo séparé : `Desktop/c1_experimental`, avec README, registre IDEES (pistes notées
P/C), JOURNAL, `notes/E1_EQUILIBRE_ET_FANO.md` et les scripts ; copies des scripts dans `code/`. Outillage : Go 1.27 et
GCC 16.1 installés à la demande de l'utilisateur ; `code/padic.c` calcule les formes de Smith et les noyaux saturés sur
Z_q (mod q^E, entiers 64 bits). Un calcul qui prenait plus de 20 min en Python exact prend 4,5 s.*

## 0. Résumé
| résultat | statut | portée |
|---|---|---|
| spectre du graphe lointain F_L (60 points) fixé par G(L) | DÉRIVÉ, OBSERVÉ sur BvLS (10⁻¹⁴) | structural, nouveau |
| réseaux lointains K₃(L) de rang 18, K₋₄(L) de rang 8 ; D(K₋₄(L))_q ≅ groupe critique de G(L) (q ∤ 2·3·7) | DÉRIVÉ | Nikulin ne mord jamais (q-rang ≤ 1 sur 312 boules) |
| graphes réels de valeurs propres {3, −4} : Paley(49), réseaux d'AG(2,7), srg(50,21,8,9) | OBSERVÉ | L22 sain ; très 7-spéciaux (géométrie sur F₇) |
| équilibre d'une droite (C2), re-dérivé ; principe « variance nulle » = égalité de Rayleigh | DÉRIVÉ | côté plancher |
| lemme E et Fano : exclu si σ_i respecte l'appariement de Fano | DÉRIVÉ | côté plancher |
| droites équiangulaires (99 droites de R⁴⁵, angle arccos 1/7) | fermé | borne SDP 540 (Barg–Yu) |

## 1. Le graphe lointain d'une droite
Soit L = {x, a, ā}, N(L) = X_x ∪ X_a ∪ X_ā, et F les 60 points à distance 2 de toute la droite.
- **Chaque lointain a exactement 2 voisins dans chaque X_p.** Les lointains sont donc en bijection avec les 60 paires
  non partenaires de X_p, pour chaque p ∈ L (sinon μ ≥ 3 pour une paire). Conséquence : le second voisin commun de
  deux points non partenaires de X_p est toujours lointain, jamais dans X_a ∪ X_ā. C'est cohérent avec le fait que
  chaque point de X_a a exactement un voisin dans X_p (μ avec p, puisque G(L) est cubique).
- **Contrôle aux petits premiers** (`code/x1c_small_primes.py` dans le labo) : 315 boules connexes. Les 2-rangs et
  3-rangs de K(G(L)) valent au plus 3 et 5 ; ceux de coker(A_G + 4I), au plus 6 et 3 ; ceux de la torsion de
  coker(MMᵀ), au plus 8 et 5. La borne de rang 8 de K₋₄(L) ne mord pas non plus en 2 ni en 3.
- Avec M = A[N(L), F] : A_F Mᵀ = Mᵀ(J/3 − A_G − I), et (A_F − 3)(A_F + 4) = 0 sur ker M. D'où
  **spec(F_L) = {8} ∪ {−α − 1 : α ∈ spec(A_G) ∖ {3, 0, 0}} ∪ {3¹⁸, (−4)⁸}** pour G(L) connexe. Le nombre de droites
  contenues dans F_L vaut 32 − t_G, ce qui recoupe n₀ = 32 − π de L16.
- **Réseaux lointains** (vecteurs propres de A portés par F) : K₃(L), de rang 18, et K₋₄(L), de rang 8 = 44 − 36.
  - Pour q ∤ 2·3·7 : D(K₋₄(L))_q ≅ −K(G(L))_q, où K est le groupe critique (car r = 3 est le degré de G(L)), et
    D(K₃(L))_q ≅ −coker(A_G + 4I)_q.
  - À 7 : le rang de recollement du graphe lointain vaut k − 22 (pour d(L) = 1), ce qui recoupe notes/102 §8.
- **Contrôles.** Sur BvLS, le spectre, les multiplicités (72 et 50) et les identités générales de recollement sont
  vérifiés. La prédiction fine n'y est pas testable : G(L) = 10 prismes, donc seuls 2, 3 et 5 interviennent.
  Pour 99, sur 312 boules admissibles aléatoires, les q-rangs aux premiers propres valent au plus 1.
  **Nikulin (l ≤ 8) ne mord pas. Route close.**

## 2. Graphes réels de mêmes valeurs propres {3, −4} (jamais utilisés auparavant)
Les ensembles de paramètres faisables avec r = 3, s = −4 sont (49,24,11,12), (50,21,8,9), (99,14,1,2) et leurs
compléments.
- **srg(49,24,11,12)** (Paley(49) et 4 réseaux d'AG(2,7)) : rank₇(A − 3I) = 16 ; Λ₃ et Λ₋₄ de det 7¹⁶ ; Jordan en
  7 : 1⁹ 7¹⁴ 49¹.
- **srg(50,21,8,9)** (Brouwer : « switch OA(7,4) »). Ensemble de commutation trouvé à la main : M = trois droites
  parallèles d'une 5ᵉ pente. C'est un ensemble (−4)-serré de 21 points ((A + 4I)1_M = 12·1), puisqu'il rencontre
  chaque droite du réseau en 3 points.
  - Données : rank₇ = 17 ; α = 16 ; Jordan de Λ₋₄ : 1⁸ 7¹⁶ ; det Λ₋₄ = 5²·7¹⁶, det Λ₃ = 2·7¹⁶. Oddité vérifiée.
  - Pour ces paramètres, le plafond de type L22 n'exclut pas α maximal : **le mécanisme de L22 est propre aux nombres
    de 99, et il est sain sur graphes réels.**
- Ces graphes sont fortement 7-spéciaux (déficit 8 ou 9) à cause de la géométrie sur F₇. 99 ne peut pas en avoir.
  Observation de calibrage, pas une loi.

## 3. Équilibre, variance nulle, lemme E
- **Équilibre** (C2, labo C2 note 23 §8, sans involution ; relu par « structures »). Soit C une réunion de composantes
  de G(L).
  - Calcul : ‖Mᵀ1_C‖² = 2|C|² − Σ_i |C ∩ X_i|² et Σ_w (Mᵀ1_C)_w = 10|C|. La variance sur F vaut
    |C|²/3 − Σ_i |C ∩ X_i|² ≤ 0, d'où l'égalité.
  - Conclusion : chaque composante rencontre les parties également, et chaque lointain en voit |C|/6 points. Les
    composantes sont les orbites de ⟨m, τ_a, τ_ā, σ⟩ sur les 12 étiquettes, prises dans les trois copies.
- **Principe.** Si A_B f = θ f avec θ ∈ {3, −4}, alors ‖A_{V∖B,B} f‖² = 2(1·f)².
  - « structures » l'identifie comme un cas d'égalité de Rayleigh : pour tout W induit et tout g de somme nulle,
    −4‖g‖² ≤ gᵀA_W g ≤ 3‖g‖². En particulier, λ₂(A_W) ≤ 3 et λ_min(A_W) ≥ −4.
  - G1 (grille = code parfait) relève du même mécanisme.
- **Lemme E.** Soit y = {c, d} un lointain avec c, d dans la même orbite O. Alors
  |O|/2 ≥ 2 + [τ_c(d) ∈ α] + [τ_d(c) ∈ α]. Une orbite de 4 étiquettes interdit donc les coïncidences τ_c(d) ∈ α.
- **Fano** (notes/109 §3). Si σ_i respecte l'appariement de Fano P_i, les orbites sont les 3 blocs. Pour y = {c,d}
  dans un bloc, τ_c(d) et τ_d(c) tombent dans la classe i, et y a au moins 4 voisins dans son bloc, contre 2 exigés.
  **Donc tout σ_i mélange les blocs.**
- **Portée.** Tout cela mord quand G(L) n'est pas connexe, c'est-à-dire en torsion faible ou structurée. **Ce n'est
  pas le plafond.** Les structures forcées en torsion maximale (boules à G(L) connexe, graphes lointains, Δ_x) ont
  un spectre local dans [−4, 3] par construction : pas de violation d'entrelacement à attendre.

## 4. Routes fermées ce jour
- **Contenu de C3** (notes/113, « structures », avec C2) : no-go, la démarche exige une symétrie d'ordre impair.
- **Droites équiangulaires.** Γ équivaut à 99 droites de R⁴⁵ d'angle arccos(1/7). La meilleure borne connue en
  n = 45 est 540 (SDP de Barg–Yu, arXiv:1311.3219, table 3, égale à la borne relative) : aucune prise.
- **Genre local à une droite** : Nikulin (§1).

## 5. Pour mémoire : résultats des sessions partenaires ce jour
- **« structures », théorème S5** (note hors dépôt : `Desktop/c99_structures_lab/NOTE_S5_DISCRIMINANT_MOD4.md`).
  - Critère mod 4 sur det Λ_θ, pour d = r − s impair et E_θ 2-entier : si tous les premiers de d sont ≡ 1 (mod 4),
    alors (−1)^{m/2} P_θ ≡ 1 (mod 4).
  - Il exclut 35 ensembles « ? » des tables de Brouwer et la famille NL_e(n) (e impair, premiers de n ≡ 1 mod 4). Il
    redonne srg(289,54,1,12) en 5 lignes. 0 graphe connu exclu sur 1183.
  - Pour 99 (d = 7 ≡ 3 mod 4), il redonne seulement k pair. Audit indépendant recommandé avant toute annonce.
- **« structures », S3 (D11)** : L21 et L23, en forme générale, tiennent sur les vrais graphes (891 droites de BvLS,
  T(7) à T(15)), avec contrôles négatifs.
- **C2** : toutes les configurations ancrées sont fermées en C2 (queue + équilibre). Le labo C2 existait depuis le
  23/09 (`c2_experimental`).
