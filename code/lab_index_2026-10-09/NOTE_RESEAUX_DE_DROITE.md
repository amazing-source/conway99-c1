# Réseaux propres portés loin d'une droite : déterminants exacts et conditions locales (session PC labo, 09/10/2026)

Statut : dérivé à la main dans cette session, contrôles numériques de cohérence seulement (scripts de ce dossier).
Non relu par un tiers. **Rien ici n'exclut un rang.**

## Cadre

Γ un srg(99,14,1,2), r = rang modulo 7 de A - 3I, r = 37 + 2k. E₋ = Z^99 ∩ V₋ (rang 44), E₃ = Z^99 ∩ V₃ (rang 54) :
réseaux pairs, det E₋ = 9 · 7^(r-1), det E₃ = 11 · 7^(r-1) (colle 7-élémentaire de rang r - 1 entre E₋ et E₃, colle
cyclique d'ordre 9 entre E₋ et Z·1, d'ordre 11 entre E₃ et Z·1).
T une droite dont le graphe G = G(T) (cubique, 36 points) est connexe ; H = 3I - G, τ = nombre d'arbres couvrants,
Θ = det(4I + G)/7 = produit des (4 + θ) sur les 35 valeurs propres θ ≠ 3 de G.

* Λ₋(T) = vecteurs propres entiers de valeur -4 nuls sur T ∪ N(T) : réseau pair de rang 8 (7Π = Gram des résidus).
* Λ₃(T) = même chose pour la valeur 3 : réseau pair de rang 18.

## Énoncés

**1. Déterminants.** Il existe des entiers j, j' ≥ 1 tels que

    det Λ₋(T) = 4 · 7^(2k) · τ / (9 j²),        det Λ₃(T) = 5 · 7^(2k) · Θ / (256 j'²).

Preuve (esquisse). Les projections E₋e_p des 36 points proches ont pour Gram (1/7)(H + J/9), de déterminant
144 τ / 7^36 ; les trois sommets de T sont dans leur enveloppe, x_t = -(5/18) L_t + (1/18)(L_t' + L_t''), et engendrent
avec elles un sur-réseau d'indice 54. Le réseau dual E₋^# = E₋(Z^99) a pour déterminant 1/(9 · 7^(r-1)) ; W étant
l'enveloppe des points proches, det E₋^# = det(E₋^# ∩ W) / det Λ₋(T). Même calcul pour la valeur 3 : Gram
(1/7)(4I + G - (2/11)J), déterminant (5/11) Θ / 7^36, y_t = (1/2) L_t + (1/4)(L_t' + L_t''), indice 16.

**2. Structure en 7 (τ premier à 7).** Λ₋(T) ⊗ Z₇ ≅ U_(8-2k) ⊥ 7 U''_(2k) : la matrice des résidus 7Π modulo 7 est de
rang 2k (c'est le modèle à vecteurs libres de la session portable), et la classe de la forme libre est fixée :
χ(det U'') = (-1)^(k+1) (τ | 7). Au rang 39 : plan anisotrope si (τ|7) = +1, hyperbolique si (τ|7) = -1 ; au rang 43 :
forme de dimension 6 hyperbolique si (τ|7) = -1, elliptique sinon. Au rang 37 : Λ₋(T) est 7-unimodulaire et
E₋ = Λ₋(T) + (E₋ ∩ 7E₋^#) : toute classe de vecteurs propres entiers modulo le réseau « trivial » a un représentant
nul sur T ∪ N(T), pour chaque droite T ; même chose pour Λ₃(T) (rang 18).

**3. Conditions locales (invariants de Hasse).** V₋ ⊗ Q : discriminant 1, c₂ = c₇ = -1 ; V₃ ⊗ Q : discriminant 11,
c₇ = c₁₁ = -1 (les mêmes à tous les rangs). Le complément X₋ de l'enveloppe des points proches a pour discriminant τ
et X₃ pour discriminant 5Θ. L'existence d'un réseau pair du bon déterminant dans X impose :
  - en 7, au rang 37 : (τ | 7) = -1. C'est le lemme L23 de Codex, retrouvé par cette voie ;
  - en 3 (v₃(τ) = 2), en 11 (11 ne divise pas Θ), en 2 (v₂(Θ) = 8) : des conditions qui se trouvent **toujours
    satisfaites** par les boules (153/153, 275/275, 109/109 sur des boules aléatoires). Donc 7 est le seul nombre
    premier qui filtre les boules ; pas de nouveau filtre.
Faits automatiques observés : 9 divise τ ; 256 divise Θ ; si v₂(Θ) = 8, la partie impaire de Θ est 3 mod 4.

**4. Vecteurs courts (Hermite, constante de Blichfeldt).** Pour toute droite à graphe connexe :

    min Λ₃(T) ≤ 3,41 · (5 · 7^(2k) Θ / 256)^(1/18),        min Λ₋(T) ≤ 2 · (4 · 7^(2k) τ / 9)^(1/8).

Pour les boules typiques (Θ ≈ 1,1e19, τ ≈ 2e12) et au rang 37 : il existe un vecteur propre entier de valeur 3, non nul,
de norme ≤ 30, nul sur T ∪ N(T), pour chaque droite T (et un de valeur -4 de norme ≤ 62). Aux rangs 39, 41, 43 les
bornes deviennent 38, 48, 60 (valeur 3). Non exploité : je n'ai pas de borne inférieure sur ces normes.

**5. Identité d'indices.** Avec m = indice de N^T Z^36 dans sa saturation dans Z^60 et g = indice de colle entre
Λ₋(T) et Λ₃(T) : m · 7^(2k) = 2 g j j'.

## Contrôles

`tau_theta_valuations.py`, `theta_mod4.py`, `local_conditions.py` (boules aléatoires, déterminants exacts par Bareiss,
symboles de Hilbert) : la condition en 7 coïncide avec « τ non résidu » sur 264 boules sur 264 ; contrôle en p = 13
(250/250 triviaux) ; conditions en 2, 3, 11 toujours satisfaites. Ces coïncidences ne prouvent pas les formules
mais une erreur d'indice ou de constante les aurait très probablement brisées.
Cohérence avec la session portable : au rang 43 la partie unimodulaire U₂ de E₋ est le plan anisotrope.
