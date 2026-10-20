# Réponse de ChatGPT au prompt Core37 : vérification LAB et test au rang 39

LAB, 20/10/2026. Texte de ChatGPT transmis par l'utilisateur, reproduit en annexe sans modification.

## Verdict

- **S1 non atteint, S4 non atteint.** ChatGPT le dit lui-même : pas de preuve uniforme, pas de contre-exemple, rien d'exclu.
- **S3 atteint au sens faible.** Le filtre est le projecteur lointain réel, H = 3I − R − EᵀZE + J/9 = 7Π_T avec
  Z = (3I − G + J)⁻¹ sur ℚ. On exige la positivité de ses mineurs principaux d'ordres 1, 2 et 3, ainsi que celle de 7I − H.
  Ce filtre est valable à tous les rangs ; son gain n'est mesuré que sur quatre graines.
- **Vérifié par LAB, avec un code indépendant :**
  - Les trois certificats séparateurs sont recalculés en arithmétique exacte (sympy) : mêmes fractions,
    −163877424991/301034985158, −97494250175/150517492579 et −27359739029/301034985158. Les trois configurations
    passent bien L2, l'isotropie et les valeurs {3, 4}.
  - La formule de H coïncide avec 7Π_T = 3I − R + J/12 − FᵀΓ_R F (NOTE_OBSTRUCTION §1.1), obtenue par un autre chemin.
    Avec E = F + 𝟏/6, on a EᵀZE = FᵀΓ_R F + J/36, et J/9 − J/36 = J/12.
  - Le moteur `oblr3.cpp` (oblr2 + filtre réel) reproduit **exactement** les nombres de nœuds annoncés :
    - graines 1, 2, 4, 5 sans le filtre réel : 6 585, 3 868, 3 891 et 7 560 nœuds ;
    - avec le filtre : 592, 316, 242 et 1 424 nœuds.

    LAB l'implante par complément de Schur sur tout le bloc affecté. À profondeur ≤ 2, c'est équivalent aux mineurs
    d'ordre ≤ 3.
- **Proposition 2 : juste, mais déjà dans l'archive.** Elle établit les degrés 8 + 7h et le seuil de 240 arêtes. C'est la
  note 230 de Codex (« Complétion binaire au rang 37 : le seuil exact de 240 arêtes », 9/10). ChatGPT ne revendiquait pas
  la nouveauté sur toute l'archive.

## Test au rang 39 (E)

**Instance.** Moteur `oblr3.exe` sur la graine 1, ρ = 2, avec les deux formes δ = 1 et δ = 3. Limite de 290 s.

| δ | candidats | coupes réelles unaires | coupes réelles en propagation | nœuds | profondeur | verdict |
|---|---|---|---|---|---|---|
| 1 | 1 077 269 | 167 275 | 183 488 012 | 189 184 | 4 | TIMEOUT |
| 3 | 1 075 945 | 167 143 | 180 401 228 | 208 384 | 4 | TIMEOUT |

**Comparaison.** Avant le filtre réel (NOTE_FUSION R4), oblr2 donnait 437 760 nœuds, profondeur 4, TIMEOUT à 270 s. Le
filtre coupe énormément, mais la recherche au rang 39 reste trop large à la racine. Il y a environ 18 000 candidats par
paire p, et l'élagage des deux premiers niveaux, qui fixent le repère du résidu de rang 2, est faible.

**Ce qui reste plausible.** Une unité plus petite au rang 39 : l'étoile ou la double étoile. Ce sont les seules
sur-déterminées selon le comptage de NOTE_OBSTRUCTION §3.2. Il faudrait un moteur dédié, combinant :
- Green avec résidu ;
- le couplage λ = 1 ;
- le filtre réel ;
- un branchement « repère d'abord ».

Estimation grossière : de l'ordre de 10⁹ à 10¹⁰ nœuds par étoile. Cela demande du C++ optimisé, et des heures par droite.

**Fichiers.**
- `oblr3.cpp` (moteur avec filtre réel ; OBLR_NOREAL=1 le désactive) ;
- journal du rang 39 dans le scratchpad (`real/r39_s1.log`), recopié ci-dessus.

---

## Annexe : texte de ChatGPT (20/10/2026), tel que transmis

Core37 — couplage exact des deux formes de Green et relèvement des comptages

20 octobre 2026 — ChatGPT. Source figée : amazing-source/conway99-c1, commit a93632a344f6191d8b5580ba4c25ec564d3e8760.

Résultat et portée : S1 non atteint ; aucun contre-exemple S4 ; aucun rang global ni aucune branche exclus. S3 : règle
nécessaire uniforme (inverse rationnel de 3I − G + J couplé à sa réduction mod 7 ; exclusions par mineurs entiers
d'ordres 1, 2, 3). 11 182 candidats supplémentaires éliminés sur les graines 1, 2, 4, 5 après les tests unaires de marges ;
nœuds du système complet 21 904 → 2 574. Proposition 2 : avec marges exactes et L2, degrés lointains 8 + 7h ; avec le
plafond de 240 arêtes, tous valent 8 et (iv), (vii), (viii) sont automatiques.

Proposition 1 : H = 3I₆₀ − R − EᵀZE + J₆₀/9 = 7Π_T ; H² = 7H, H ⪰ 0, 7I − H ⪰ 0, rang H = 8 ; au rang 37, H ≡ 0 (mod 7).
Preuve par K = EEᵀ = 12I − G − G² + 2J − J_cl, ER = 2J − E − GE, R² + R + EᵀE = 12I + 2J ; multiplicités 18 et 8 sur ker E.
Version entière B_S = 3D I_S − D R_S + (D/9) J_S − E_SᵀC E_S avec C = DZ entier.

Coupes : 0 ≤ d_a ≤ 7D ; h_ab² ≤ d_a d_b et h_ab² ≤ (7D − d_a)(7D − d_b) ; déterminant 3 × 3 ≥ 0.

Mesures (graines 1, 2, 4, 5) :
- exclusions unaires supplémentaires : 2 199 / 3 402 / 3 849 / 1 732 ;
- nœuds 6 585 → 592, 3 868 → 316, 3 891 → 242, 7 560 → 1 424 ;
- profondeur 2.

Certificats (graine 1, s01 = [2,9,1,4,10,3,6,5,8,0,11,7], s12 = [0,6,10,11,7,2,5,1,8,4,3,9],
s20 = [0,10,8,11,6,5,1,3,9,2,4,7], D = 97535335191192) :
- un nom {0,2,12,14,31,32} : H = −163877424991/301034985158 ;
- deux noms {5,8,13,18,26,35}, {0,2,16,22,30,34} : det = −97494250175/150517492579 ;
- trois noms {5,8,13,18,26,35}, {0,10,20,22,29,34}, {0,5,12,20,31,33} : tous les mineurs propres sont positifs,
  det = −27359739029/301034985158.

Ouvert : aucune famille entière de G, le signe de τ non exploité, la constance des profondeurs inexpliquée. Reproduction :
verify.py --rebuild-all (Python standard), reproduce.py (NumPy, SymPy, C++17 avec Boost). Ces fichiers ne sont pas dans
le dépôt LAB.
