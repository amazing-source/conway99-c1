# 141 — Ligne (C) : lemme Z, étages h / y / u, famille rigide

*27/09, fin d'après-midi. C1. Suite de notes/140. Tout ce qui est marqué DÉMONTRÉ est une condition nécessaire sur tout repère
(F) dans une enveloppe U. Les outils sont h_stage2.py, frame_pipeline.py, rigid_h.py et y_first.py (ce dernier réservé au PC du
labo).*

## 1. Lemme Z (DÉMONTRÉ)
**Énoncé.** Σ_{c=1..7} h_c ∈ 2U. Donc z := ½Σ_c h_c ∈ U, de norme 7, et z ∈ N (quels que soient les signes ε_c).

**Preuve.**
1. **(L5)** Pour χ caractéristique, (F) s'écrit 7χ = Σ(χ,v)v. Or (χ,u) et (χ,y) sont impairs, et (χ,h) est pair. Donc
   c := Σ_u u + Σ_y y ≡ χ mod 2U : c est caractéristique.
2. (F) en x ∈ U, réduit mod 2 (avec a² ≡ a), donne Σ(u,x) + Σ(h,x) + Σ(y,x) ≡ |x|². Par ailleurs (c,x) ≡ |x|². D'où
   (Σ_h h, x) ≡ 0 mod 2 pour tout x ∈ U, c'est-à-dire Σh ∈ 2U* = 2U.
3. De plus z ∈ N_max, et comme [N_max : N] ∈ {1, 7} est impair, z ∈ N. ∎

**Contrôle côté graphe.** 1_blocs ∈ ker(I + B) mod 2, car B·1_blocs ≡ 1_blocs : le lemme est cohérent, pas vide.
- Plus généralement, les 49 vecteurs (u, h) mod 2U satisfont exactement les relations de K̄⁺ = ker(I + B) mod 2, un espace de
  dimension 27.

**Usage dans O₂₄.** a = ΣM_c est un vecteur de O₂₄ de forme (±3⁴, ±1²⁰). Chez C2 le filtre passe 298 fois sur 298 : il est
presque automatique. Les sommes d'étoiles (§3), elles, tuent 298 sur 298.

## 2. Étages de recherche (conditions DÉMONTRÉES)
**Étage h.**
- (O) Les 7 h sont orthogonaux deux à deux.
- (H2) |(h,β)| ≤ 1 pour toute nouvelle racine β, et w(β) := Σ_c(h_c,β)² ∈ {1, 3}.
- (Z) Le lemme Z ci-dessus.
- (CELL) Pour chaque paire {c,d} et chaque t = ±1, il existe un x de norme 3 avec (x,h_c)(x,h_d) = t, les deux produits valant
  ±1, et (x,h_e) = 0 pour e ∉ {c,d}.
  - Raison : les deux orbites de la paire ont C_coC_do = +1 et −1.
  - La condition est monotone sur les configurations partielles.

**Étage y.** Soit B₁ := {β : w(β) = 1}. Ce sont EXACTEMENT les nouvelles racines touchées à 3/2 par un vecteur impair du repère.
- y ∈ H⊥, |y|² = 7, |(y,β)| ≤ 3/2.
- hits(y) ⊂ B₁.
- (α,y₁)² + (α,y₂)² ≤ 6 pour toute racine α.
- Les hits des deux y sont disjoints.
- Le piège : min (y⊥)* ≥ 8/7.

**Étage u (L7, DÉMONTRÉ).** Pour chaque bloc c : Σ_{cellules de c} (x,h_c)·x = 3h_c, avec un x par cellule (12 cellules).
- C'est linéaire une fois les h fixés.

**Résultat sur 132 (d₆⁴).**
- L'étage h seul trouve facilement des configurations.
- Mais les 10 premières configurations testées meurent toutes à l'étage y : aucun des 19 264 vecteurs de norme 7 de H⊥ n'a ses
  hits dans B₁. Tous touchent une racine de B₃.

## 3. Famille RIGIDE : 10 (a₁²⁴), 44 (a₃⁸), 87 (d₄⁶), 115 (a₇²d₅²), 132 (d₆⁴)
Ce sont les réseaux de rang plein à Coxeter égaux h. Le voisin nb₁ a le même système de racines que U, et nb₂ a h' = 2h + 2.
**Conséquences :**
- E(x) = h|x|² pour tout x ;
- tout x de norme 3 a m(x) = 0 (aucun hit à 3/2) et |P_C x|² = rang(C)/8 pour chaque composante C de nb₂ ;
- chaque y a exactement m(y) = 4h + 8 hits ;
- B₁ = hits(y₁) ⊔ hits(y₂) EXACTEMENT ;
- w vaut 3 partout ailleurs.

**Analyse locale, sous-famille D₂ₘ ⊃ D_m² (10, 44, 87, 132).**
- u a un spinor sur une moitié de chaque bloc.
- h est de type I (entier, sur une moitié, coefficients 0/±1) ou S (tout ±½).
- y est de cas 1 (demi-I : ±1 sur n₁ places ; demi-H : ±½) ou de cas 2 (demi-I nulle ; un ±3/2 sur la demi-H).
- **Identité clé :** t_y(a,b) = y_a² + y_b² − ¼, où t_y compte les items touchés par y parmi les P^±_{ab}.
- Les conditions diagonales (la diagonale de la partie h,y est constante par moitié, égale à 7 − n_i/4) et les conditions de
  couverture sont alors compatibles bloc par bloc. La contradiction, s'il y en a une, est globale.
- La partie croisée est Σ_{h de type S} σ⁽¹⁾σ⁽²⁾ᵀ/4 + Σ_y (P₁y)(P₂y)ᵀ = 0. C'est la matrice M déjà rencontrée.

**Outil : rigid_h.py.**
- Il énumère les h par dominance itérée (h_{k+1} dominant pour W(R ∩ {h₁..h_k}⊥), ce qui est complet par Steinberg).
- Il applique ensuite (O), (H2), (Z), (CELL) et les sommes d'étoiles par bloc (CP-SAT exact, 60 s maximum).
- Il tourne sous run_capped (2,5 Go).

## 4. Critère d'énergie des y (données de racines)
- **Énoncé.** Le packing, en comptant aussi les y, donne E(y₁) + E(y₂) ≥ 1,25r − 16h_min. On le compare au sac à dos sur les
  poids de niveau ≤ 2.
- **Résultat.** Aucune exclusion nouvelle. Dans la famille rigide, c'est une égalité : les y y sont saturés (E = 7h).
