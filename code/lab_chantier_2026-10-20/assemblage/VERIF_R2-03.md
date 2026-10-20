# VERIF R2-03 — rang 43 : b₂ ≥ 1000 pour tout k, et b₂ ≥ 1264 s'il existe une racine (avec R2-21)

Vérificateur adverse, contexte neuf, 20/10/2026. Lecture seule. Scripts du scratchpad de la session : `check_r2_03.py`
et `check_r2_03_fricke24.py`. Bibliothèque standard, fractions exactes, un processus, environ 1 min chacun, moins de
200 Mo.

## Verdict : TIENT

Les deux bornes sont justes. Le statut est P : preuves d'IA (Codex, avec la confirmation de LAP), qu'aucun humain n'a
relues.

Contrôles faits ici :
- **Identité thêta du rang 43.** Je l'ai refaite indépendamment en arithmétique exacte, avec deux contrôles positifs.
- **Identité harmonique (3) de la note 242.** Refaite de même, avec un contrôle positif du signe de Fricke.
- **Arithmétique de la combinaison.** Refaite par script.

**R2-21 est juste aussi.** L'enchaînement « 462 + 85b₁ + b₁²/2 ≥ 968 » est faux pour b₁ ∈ {0, 2, 4}. L'erreur est dans
la fiche du chantier (L05_Codex.md:1617, B09), pas dans la note 192, qui distingue correctement les cas.

**Ce n'est pas une exclusion.** Aucune borne supérieure de b₂ n'est connue au rang 43.

## 1. Énoncés exacts

Dépôt `C:/home/researcher/cw/conway99-c1`, branche `origin/codex/c1-arithmetic-audit`. Toutes les couches comptent les deux
signes (note 242:29 et 242:149).

- **Note 191:109** : « Au rang 43, le quotient discriminant anisotrope donne a7k=bk pour tout k, en particulier a7=b1 ».
- **Note 191:115** : « b2 = 1000 − 8a7 + 25a8 + 11a9 + 8a10 + 3a11 + a12 = a14 ». La même formule est en NOTE.md:1035.
- **Note 242:8, (1)** : « Au rang 43, s'il existe une racine dans M, [...] 10 a8 + 2 a9 + 5 a10 + 2 a11 + a12 >= 328 ».
- **Note 242:42, (2)** : « b2 = 1000-16k+25a8+11a9+8a10+3a11+a12 », avec b1 = 2k.
- **Note 192:172-173** : « b_2 ≥ 462+84k+2k(k−1)+88k = 462+170k+2k^2 » au rang 43.
- **Note 192:178-182** : « b2≥1000−16k. Pour k≤2, cela impose b2≥968. Pour k≥3, [...] b2≥990 ».

## 2. Définitions et hypothèses

- **Réseaux** (NOTE.md §1 ; notes 167 et 242 §1).
  - L1 est pair, de rang 44, de déterminant 7^(r−1). M = √7·L1*.
  - a_n est le nombre de vecteurs de norme 2n de L1. b_n est le nombre de vecteurs de norme 2n de M.
  - Une racine est un vecteur de norme 2 de M, et k est le nombre de lignes ±r.
  - Les mêmes objets servent dans 191, 192 et 242. Pas de faux ami.
- **Rang 43, donc d = 42.**
  - L1/7L1* ≅ F₇², avec la forme x·x/2 mod 7.
  - Redérivation de l'anisotropie (note 177) par la formule de Milgram :
    - la somme de Gauss vaut 7²¹·e(44/8) = −7²¹ ;
    - la partie de rang 42 a donc un discriminant carré dans F₇ ;
    - comme det L1 = 7⁴², la partie unimodulaire U de rang 2 a det U carré ;
    - −1 n'est pas un carré modulo 7, donc −det U non plus, et le plan est anisotrope.
  - D'où L1[14j] = √7·M[2j] (242:36), a₇ = b₁ = 2k et a₁₄ = b₂.
- **Hypothèse de (1)** : k ≥ 1. Elle sert dans la direction e = r/√2 d'une racine.
- **Ingrédients de (1) non redérivés ici** :
  - l'orthogonalité des racines (note 176), qui donne V1[e,e] = 4 ;
  - la distinction des 84 reflets et des sommes ±r ± s (note 191 §2), qui donne V2[e,e] ≥ 84 + 8(k−1).
- **Ce que j'ai recompté** : les 42 triangles non orthogonaux à r. Chacun des 14 sommets du cœur porte 3 triangles
  n'ayant qu'un sommet dans P ∪ Q, et Σ_T g(T)² = 42.

## 3. Contrôles numériques (exacts)

1. **Base de poids 22 sur Γ₀(7).**
   - On prend F_j = q^(14−j)·θ_A·E1^(4j−7)·E7^(49−4j), pour j = 0..14, avec A = x² + xy + 2y² (NOTE.md §1).
   - Fricke : θ_M = Σ c_j 7^(d/2+2j−25) F_(14−j).
   - Contrôles positifs, avec θ_M prédit égal au θ_M réel sur 60 coefficients :
     - E8⁵ ⊕ A ⊕ A (d = 2) : **égal** ;
     - (√7E8)⁵ ⊕ A ⊕ A (d = 42) : **égal**.
2. **Identités du rang 43.**
   - Je n'impose que a₀ = 1, a₁..a₆ = 0, b₀ = 1 et b₁ = a₇. J'obtiens exactement :
     - a13 = 2632 + 56a7 − 2a8 − 16a9 + 7a10 + 2a11 + a12 ;
     - b2 = 1000 − 8a7 + 25a8 + 11a9 + 8a10 + 3a11 + a12.
   - a14 = b2 sort automatiquement.
   - C'est conforme aux notes 191:114-115 et 242:41-42.
3. **Identité harmonique (3) de la note 242, base de poids 24.**
   - On prend F'_j = η^(4j)·η7^(48−4j), pour j = −1..13.
   - Élimination triangulaire : c0 = 52h7 + 48h8 + 24h9 + 28h10 + 16h11 + 12h12 + 4h13 + h14, avec h7 = 7R et h14 = 7D.
     C'est le c0 de 242:94, soit 364R + 48h8 + … + 4X + 7D.
   - F'_13 = q − 52q² + …
   - Fricke (4), Θ_M,P = −7¹⁰(Θ_L1,P | W7), avec le **signe** :
     - contrôle positif sur L = (√7E8)⁵ ⊕ A ⊕ A (det 7⁴²), avec P = |x_E1|² − 4|x_A1|² (harmonique : 8 − 2·4 = 0) ;
     - Θ_M,P prédit égal au réel sur 50 coefficients (464, 452064, …).
   - On obtient c−1 = −2401R et c0 = −2548R − 49D, puis 728R + 12h8 + 6h9 + 7h10 + 4h11 + 3h12 + h13 + 14D = 0. **C'est
     (3).**
4. **Trace de (5).**
   - On recalcule trace/44 à partir de (2) et de a13.
   - On trouve C = 2828 + 112k + 35a8 + 7a9 + (35/2)a10 + 7a11 + (7/2)a12. Conforme à 242:114.
   - 728·4 + 14(84 + 8(k−1)) = 3976 + 112k, d'où 35a8 + … ≥ 1148, et 1148/3,5 = 328. **C'est (1).**
5. **Combinaison.**
   - Pour k = 0 : b₂ = 1000 + (25a8 + 11a9 + 8a10 + 3a11 + a12) ≥ 1000.
   - Pour k ≥ 1 :
     - les coefficients de (2) dominent ceux de (1) un à un (25 ≥ 10, 11 ≥ 2, 8 ≥ 5, 3 ≥ 2, 1 ≥ 1), d'où
       b₂ ≥ 1328 − 16k ;
     - le minimum de 25a8 + … + a12 sous (1) vaut exactement 328, atteint en a12 = 328. Ce couple d'inégalités ne donne
       donc pas mieux.

| k | max(1000−16k, 462+170k+2k²) (ancien) | max(1328−16k, 462+170k+2k²) (k ≥ 1) |
|---|---|---|
| 0 | 1000 | — |
| 1 | 984 | 1312 |
| 2 | **968** | 1296 |
| 3 | 990 | 1280 |
| 4 | 1174 | **1264** |
| 5 | 1362 | 1362 |
| 6 | 1554 | 1554 |

L'ancien minimum vaut 968, en k = 2. Le nouveau vaut **1000** pour tout k (en k = 0), et **1264** s'il existe une racine
(en k = 4).

## 4. Chaîne réécrite

1. **(Note 177, P, Codex ; redérivé ici.)** Au rang 43, le plan discriminant est anisotrope, donc a₇ⱼ = bⱼ et
   a₇ = b₁ = 2k.
2. **(Notes 191 et 242, P/C ; redérivé ici, exact.)** b₂ = 1000 − 16k + 25a8 + 11a9 + 8a10 + 3a11 + a12.
3. **(Note 242 §2-4, P, Codex ; (3) confirmé par LAP au message 487 ; (3), (4) et (5) redérivés ici.)** Si k ≥ 1, alors
   10a8 + 2a9 + 5a10 + 2a11 + a12 ≥ 328.
4. **(Note 192 §4, P, Codex ; relu par LAB au message 250.)** b₂ ≥ 462 + 170k + 2k².
5. **Conclusion (P).**
   - Au rang 43, b₂ ≥ 1000.
   - L'égalité exige k = 0 et a8 = … = a12 = 0 : c'est la branche S₀.
   - S'il existe une racine, b₂ ≥ 1264.
   - Les cibles deviennent :
     - « b₂ ≤ 999 ⇒ r ≠ 43 », au lieu de « ≤ 967 » (L06 COND-05) ;
     - « b₂ ≤ 1263 ⇒ pas de racine ».

## 5. R2-21, refait

- Les valeurs de 462 + 85b₁ + b₁²/2 sont :
  - 462 pour b₁ = 0 ;
  - 634 pour b₁ = 2 ;
  - 810 pour b₁ = 4 ;
  - 990 pour b₁ = 6.
- L'inégalité « ≥ 968 » n'est donc vraie qu'à partir de b₁ = 6.
- **Où se trouve l'énoncé enchaîné faux.**
  - Il est dans `fiches/L05_Codex.md:1617` (B09 : « b_2 ≥ 462 + 85b_1 + b_1²/2 ≥ 968 »).
  - R1 (I10) le cite sous le nom L05-029.
  - La ligne L05-029 elle-même (L05_Codex.md:109) dit seulement « b_2 ≥ 968 », ce qui est juste.
- **Les sources d'origine sont correctes :**
  - note 192, l. 178-182 : cas k ≤ 2 et k ≥ 3 ;
  - NOTE.md:1079 : « with b_2 >= 1000 - 16 k: b_2 >= 968 ».
- **Correction proposée.** Il faut remplacer B09 par « b₂ ≥ max(462 + 85b₁ + b₁²/2, 1000 − 8b₁) ≥ 968 ». C'est désormais
  dépassé par b₂ ≥ 1000.

## 6. Redécouverte

« 968 » apparaît partout :
- note 192 ;
- NOTE.md:1079 ;
- fiches L05-029 et B09, L06 COND-05 et BORNE-08 ;
- pont du 08/10.

NOTE.md:61 donne « b_2 >= 1000 », mais seulement sous a₇ = 0, c'est-à-dire le cas k = 0. La note 242 (09/10) contient (1)
et (2) sur la même page, mais n'écrit pas la borne universelle.

J'ai cherché `b_?2 ?(>=|≥) ?(1000|1264)`, `1328 ?- ?16k` et `b2>=1000` dans :
- `work/` ;
- `Desktop/Recherche_Conway` ;
- les branches de `conway99-c1` (`git grep`) ;
- le pont du 09 au 10/10.

Je n'ai rien trouvé. **Le corollaire est nouveau tel qu'écrit, mais il ne demande qu'une ligne.**

## 7. Ce qui manquerait

- **Pour le statut.** Une relecture humaine des ingrédients qui ne sont pas redérivés ici :
  - note 176 (racines deux à deux orthogonales) ;
  - note 191 §2 (distinction des reflets et des sommes de racines) ;
  - note 192 §4 (88k vecteurs de profil C distincts des précédents) ;
  - l'identité det L1 = 7^(r−1) (rank7.tex).
- **Pour une exclusion du rang 43.** Il faudrait une borne supérieure b₂ ≤ 999. Aucun mécanisme n'est connu. Selon
  NOTE.md:1039-1040, le comptage dual ne peut pas la donner.
