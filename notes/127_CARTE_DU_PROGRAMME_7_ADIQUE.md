# 127 — Carte du programme 7-adique (état du 26/09, fin de nuit)

*Synthèse de coordination, sans résultat nouveau. Elle indique ce qui ferme quel cas et où sont les verrous. Sources :
notes/99 et 101-102 (L21, L22, L23), 114, 124-126, rapports d'Astra sur le dossier n° 5 (relus par « structures »),
NOTE_S24 et S26.*

## 1. Le cadre
- k = rang₇(A − 3I) − 15 est pair et le même en tout sommet (L2, L4). On a 10 ≤ k ≤ 28 (L20 bis/ter et L22).
- Pour une droite L :
  - d(L) = dim ker₇ L_{G(L)} ;
  - E_L est le noyau local supplémentaire, de dimension d − 1 ;
  - r(L) = rang₇(Mᵀ|_{E_L}) et r₀ = d − 1 − r.
- **Identité exacte (notes/126)** : 14 + k = (37 − d) + 2r + ρ, avec ρ ≥ 0. D'où **k ≥ 22 + r − r₀**.
- r₀ est la dimension des vecteurs propres 3 mod 7 de Γ portés par N(L). Sur Q, ce sont les différences de
  composantes.

## 2. Les cas de k, et ce qui les ferme
| k | droites génériques (d = 1) | droites dégénérées | état |
|---|---|---|---|
| ≤ 16 | impossibles (L21) | r₀ ≥ 6 + r partout ; sous NT, impossible (c(L) ≤ 6) | **fermé sous NT** |
| 18 | impossibles | sous NT : motif (2,…,2) sur des cycles de classes en tout sommet, P ∈ [924, 1122] | sous NT, côté Hamming (notes/112) |
| 20 | impossibles | sous NT : c(L) ≥ 3 partout ; à P = 0, (4,4,4) partout | ouvert |
| 22 | R_L = 0, construction complète (Astra §2) ; τ non carré (L23) ; **étoile complète morte 42/42** | ρ = r₀ − r : torsion équilibrée ou non connexe | (a′) chez Astra ; « sans générique » chez C1 |
| 24 | rang R_L = 2, construction complète (Astra §3 + MR = 0) ; τ carré ⟺ R anisotrope ; ≥ 8 mauvaises ombres | ρ = 2 + r₀ − r | (b′) chez Astra |
| 26, 28 | rang 4, 6 ; signe χ(disc R) = (−1)^{k/2} χ(τ) | — | ouverts |

## 3. Résultats inconditionnels sur les droites dégénérées (notes/125-126)
- **P = 0 :**
  - une droite (4,4,4) donne exactement k ≥ 20 : pas de torsion, r₀ = 2 ;
  - une droite **(6,6) force k ≥ 22** (aucune torsion équilibrée sur une composante à 6 étiquettes, test exact) ;
  - une droite **(4,8) force k ≥ 22**, sauf torsion équilibrée sur sa composante à 8 étiquettes (non testé).
- **P = S = 0** : toutes les G(L) sont de maille ≥ 5, et seuls restent les profils connexe et (6,6).
- Composantes à 4 étiquettes : 7-torsion seulement avec triangles (P > 0), et jamais équilibrée sur une seule
  composante.

## 4. Les verrous
1. **(NT) pour les droites connexes** : une torsion 7 de G(L) n'est jamais équilibrée (Mᵀφ ≠ 0).
   - Heuristique : la torsion aléatoire n'est jamais équilibrée (environ 20 conditions indépendantes).
   - Aucun test local n'est assez fort (ombres de 6 points). Reformulation : un couple (z₃ ∈ Λ₃, V ∈ Λ₋₄) entier qui
     coïncide hors de N(L).
   - NT ferme k ≤ 16, et réduit k = 18 et k = 20 à des motifs rigides.
2. **(a′) uniforme** : l'étoile complète est impossible pour toute boule générique à k = 22. Obstruction purement
   algébrique (ablation de « structures »), qui demande tout le couplage 4K₂ + 2K₁.
3. **k = 22 sans droite générique** : sous NT, toutes les droites sont non connexes. La question est locale :
   partitions P_U et lemmes E au niveau paire × bloc. La « trame dans V₃ » est automatique.
4. **k = 24 à 28** : moins rigide (résidu de rang 2 à 6). Heuristique de comptage : environ 10^(−676) solution par
   système d'ombres à k = 28, mais pas de preuve.

## 5. Chaîne possible vers k ≠ 22
(a′) uniforme ⟹ pas de droite générique à k = 22. Avec NT, toute droite est alors non connexe. Exclure « toute droite
non connexe » (question locale) ferme k = 22.
