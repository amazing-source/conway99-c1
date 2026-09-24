# 70 — Condition de Krein pour les droites : P ≤ 1151 (2026-09-24, soir)

*Mathématiques pures, sans SAT. Calculs de contrôle : `code/krein_lines.py` (BvLS + formule 99),
`code/krein_flags.py`, `code/krein_linegraph.py`, `code/krein_local.py` (tentatives de renforcement).*

## Énoncé
**Théorème K1.** Dans un srg(99,14,1,2), soit P le nombre de prismes (paires de droites disjointes reliées par un
couplage parfait ; P = nombre de triangles du graphe O des arêtes opposées). Alors
  **12 P = 13860 − 64·‖Σ_L u_L^{⊗3}‖²**, donc **P ≤ 1155**, et même **P ≤ 1151** (en ajoutant les points),
où u_L est le vecteur unitaire de la projection de 1_L sur l'espace propre E₋₄ (dimension 44).

**Corollaires** (avec L15 : P = 1386 − ⅙Σ_x|W(x)|, et n₃ = 4158 − 3P) :
- Σ_x |W(x)| ≥ 1410 : **en moyenne, chaque sommet a au moins 14,2 paires (étiquette, classe) tordues** ;
- au moins 705 paires de droites reliées par exactement 2 arêtes (n₃ ≥ 705) ;
- en moyenne, une droite est dans au plus 10 prismes (le cas « grid-full » en demande 12). **Nouvelle preuve,
  spectrale, que Γ est tordu** (L1 l'obtenait par 99 ∤ 3⁷) ;
- la condition est propre à 99 : dans la famille srg(2t²+4t+3, 2t+2, 1, 2) elle n'exclut « grid-full » que pour
  t = 6 (BvLS, t = 10 : borne 40 contre 20 requis ; 6273 et 494019 : sans effet).

## Preuve (à la main)
1. E = E₋₄ = (3I − A + J/9)/7, projecteur orthogonal sur l'espace propre de −4 (dim 44). Pour une droite L,
   w_L = E·1_L, et 7⟨w_L, w_M⟩ = 3|L∩M| − 1_Lᵀ A 1_M + |L||M|/9.
   - L = M : 9 − 6 + 1 = 4.
   - L, M sécantes en x : 3 − 4 + 1 = **0** (les 4 arêtes vont de x aux deux autres points de chaque droite ; les
     autres points de L et de M ne sont pas adjacents, sinon triangle hors droite). *Les 7 droites par un point sont
     deux à deux orthogonales dans E₋₄* (spécifique à 99 : r = 3 et 9(k − r) = n).
   - L, M disjointes reliées par e arêtes : 1 − e.
   On pose K = 7·Gram : K_LL = 4, 0 pour des droites sécantes, 1 − e pour des droites disjointes.
2. **Comptes par droite.** Un point hors de L a au plus un voisin sur L ; 36 points sont adjacents à L, chacun sur
   6 droites disjointes de L, donc Σ_{M disjointe} e(L,M) = 216. Les paires d'arêtes entre L et M correspondent aux
   quadrangles ayant un côté sur L : Σ_M C(e,2) = 3·12 = 36. On a e ≤ 3, e = 2 ⟺ un seul quadrangle, e = 3 ⟺ prisme.
   Avec π(L) = nombre de prismes contenant L et 212 droites disjointes :
   n₃ = π, n₂ = 36 − 3π, n₁ = 144 + 3π, n₀ = 32 − π (Lou–Murin trouvent les mêmes, sous la forme α, β, γ).
3. Σ_M K_LM = 4 + n₀ − n₂ − 2n₃ = 0 ; Σ_M K_LM³ = 64 + n₀ − n₂ − 8n₃ = **60 − 6π(L)**.
4. Pour des vecteurs unitaires, Σ_{L,M} ⟨u_L,u_M⟩³ = ‖Σ_L u_L^{⊗3}‖² ≥ 0 (produit scalaire des puissances
   tensorielles). Ici ⟨u_L,u_M⟩ = K_LM/4, donc Σ_L (60 − 6π(L)) = 64‖Σ u_L^{⊗3}‖², soit
   13860 − 12P = 64‖Σ u_L^{⊗3}‖² (Σ_L π(L) = 2P). ∎
5. *Raffinement (P ≤ 1151).* Avec aussi les points (u_x = E e_x normalisé : produits 1, −2/7, 1/28) et les
   produits point-droite (2/√28 si x ∈ L, −1/√28 si x a un voisin sur L, 1/(2√28) sinon ; par droite : 3, 36, 60
   points), l'inégalité de Cauchy–Schwarz ⟨T_P, T_L⟩² ≤ ‖T_P‖²‖T_L‖² pour T = Σ u^{⊗3} donne
   ‖T_P‖² = 99·14868/21952, ⟨T_P,T_L⟩ = −231·4,5/(28√28), d'où 13860 − 12P ≥ 46,98, **P ≤ 1151**.

## Contrôles
- BvLS (`krein_lines.py`) : les formules de Gram, les comptes n_e(π) et la somme des cubes calculée directement
  (360,855) coïncident exactement avec la prédiction.
- Cohérence : n₃ = 4158 − 3P est exactement la variable libre de Reimbayev (notes/60).
- Autres formes équivalentes : S = K − 4I (entrées 1, −1, −2 pour e = 0, 2, 3) vérifie **S² = 13 S + 68 I**
  (graphe signé à deux valeurs propres, 17 et −4) ; les 99 sous-espaces V_x = vect(droites par x) forment un
  « tight fusion frame » : Σ_x P_{V_x} = (63/4)·I₄₄.

## Ce qui a été essayé pour renforcer, sans succès (tout est linéaire en P, calculs instantanés)
- Tous les degrés de Gegenbauer jusqu'à 16 pour les droites : seul le degré 3 contraint.
- Familles de drapeaux (point, droite) avec 25 pondérations, dans E₋₄, E₃ et leurs mélanges (dim 98) : P ≤ 1151,
  pas mieux.
- Les 20 conditions de Krein des idempotents du graphe des droites (y compris l'espace des cycles ker N, 132) :
  seule (0,0,0) contraint.
- Conditions de Krein **locales** (idempotents de H = Γ[Γ₂(x)], qui ne dépendent que de |W(x)| et de D₂(x)) :
  aucune ne contraint.
- **Aucune borne inférieure sur P** n'apparaît : toutes ces inégalités vont dans le même sens (torsion forte),
  comme la frontière SAT. Pour une contradiction, il manque une inégalité en sens inverse.

## Pistes ouvertes à partir d'ici
1. Objets plus riches dont les statistiques de paires voient 3 droites (cycles des permutations σ_L autour d'une
   droite : π(L) = points fixes de σ_L, et le 2-facteur autour de L a des cycles de longueur 3 × les cycles de σ_L).
   Ils introduisent de nouvelles inconnues (comme z₁₁ chez Reimbayev), à combiner avec les identités de comptage.
2. Le réseau pair Λ_L engendré par les droites (normes 4, produits 0, ±1, −2 ; 21Λ* ⊂ Λ) : structure 3-adique
   (C'^⊥ ⊆ C', 3-rang pair) et 7-adique (celle de L2–L4).
