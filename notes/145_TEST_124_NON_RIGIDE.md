# 145 — Test décisif sur un réseau non rigide : 124 (d₈a₇², voisins D₈³ et A₁₅D₉)

*27/09 nuit. C1. En cours. Question : les lemmes locaux et la contrainte des DEUX voisins tuent-ils un réseau non rigide ?
(notes/144)*

## Données
- r = 224 et Γ = 4 (data/finishC/gamma/gamma_124.json). Aucune paire y n'est calculée.
- Nouvelles racines :
  - 112 signées dans D₈³ : deux blocs D₈ ⊃ A₇, de 28 racines chacun à signe près ; le d₈ de U remplit le 3ᵉ D₈ ;
  - 160 dans A₁₅D₉ : A₁₅ ⊃ A₇+A₇ (64 racines, e_i − e_j avec i ∈ I, j ∈ J) et D₉ ⊃ D₈ (16 racines, ±e_i ± e₉).
- m(x) = 28 − E(x), le même dans les deux voisins. **128/2048 vecteurs de norme 3 ne touchent rien** : c'est le plus contraint
  des 131 réseaux non rigides.
- **Budget de packing** (voisin D₈³, le plus serré) : Σ_u m(u) + hits_y(D₈³) ≤ 56.

## Bloc D₈ ⊃ A₇ (nouvelles racines ±(e_i + e_j) dans le voisin D₈³)
**Vecteurs pairs h.** (h, e_i − e_j) ∈ ℤ, (h, e_i + e_j) ∈ ℤ et |h_i + h_j| ≤ 1. Donc h|_B est l'un des vecteurs suivants :
0, ±e_i, e_i − e_j, (±½)⁸, ±(3/2, (−½)⁷).

**Vecteurs impairs.** Toutes les coordonnées sont ≡ ¼ (mod 1), ou toutes ≡ −¼, avec |v_i + v_j| ≤ 3/2.
- La nouvelle racine e_i + e_j est touchée ⟺ v_i + v_j = ±3/2.

**Identité de bloc** (somme sur les 28 nouvelles racines, w = 3 − 2n) :
- Σ_h [6|h_B|² + (Σ_i h_i)²] = 84 − 2H_B, où H_B = nombre de nouvelles racines du bloc touchées (par u ou y).
- Contributions par forme de h :

| forme de h\|_B | contribution |
|---|---|
| 0 | 0 |
| ±e_i | 7 |
| e_i − e_j | 12 |
| (±½)⁸ avec k signes moins | 12 + (4−k)² |
| ±(3/2, (−½)⁷) | 28 (toute la norme de h est alors dans le bloc) |

## Plan
1. Même inventaire pour A₁₅ ⊃ A₇+A₇ et D₉ ⊃ D₈ (voisin A₁₅D₉).
2. Le plan 2D V ⊥ racines(U) est vu par les DEUX voisins, via des directions différentes : (1_{B₂}, 1_{B₃}) dans D₈³, et
   (u_A, e₉) dans A₁₅D₉. Écrire la projection de (F) sur V, soit Σ_v P_V v P_V vᵀ = 7I₂, dans les deux cadres.
3. Recoller : chaque h a UNE forme par bloc dans chaque voisin, et sa norme totale vaut 4. Il faut en même temps :
   - l'identité de bloc dans les deux voisins ;
   - le packing ;
   - Z⁺.
   Chercher la contradiction sans énumérer les y. Seule l'information des types de y par bloc devrait servir.
