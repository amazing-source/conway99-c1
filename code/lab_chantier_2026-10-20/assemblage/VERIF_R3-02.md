# VERIF R3-02 — V15 §79 × N14 au rang 37

Vérificateur adverse, contexte neuf, 20/10/2026. Lecture seule. Petits scripts dans le scratchpad de la session
(`check_misc.py`), un processus, quelques secondes.

## Verdict : TIENT AVEC RÉSERVES

La chaîne est correcte. Le vecteur co-Heawood de §79 est exactement l'objet de N14, avec la même normalisation. §79
n'utilise aucune hypothèse cachée qui contredirait la portée « rang 37 ».

Réserves :

1. **Statut E.** N14 est un calcul exhaustif sans certificat, jamais audité par une autre session (NOTE.md:3742,
   3816-3818 ; relecture 07 du 16/10, R10). La combinaison a ce statut.
2. **En substance déjà connue.** Que la famille co-Heawood soit vide au rang 37, c'est N14 lui-même (10/10). La
   branche co-Heawood de Codex a été identifiée au monde de N14 le 12/10 (NOTE.md:4133-4135 ; fiche L06-100). Seul le
   corollaire écrit pour la dichotomie de V15 est nouveau : je ne l'ai trouvé nulle part avant le chantier.
3. **Gain mince.**
   - Dans la branche co-Heawood, §79 donne déjà **au plus une** complétion, avec au plus 2¹³ = 8192 tests linéaires
     (unicité : l. 3574-3575 ; borne 8192 : (76d), l. 3433).
   - N14 permet seulement de rejeter ces facteurs sans les tester, et seulement pour une recherche restreinte au
     rang 37.
   - La vraie difficulté reste entière : énumérer les bords (B, D), ce qui n'est pas borné (§77, l. 3502-3508).
     **Pas d'exclusion.**
4. **Le volet « S₀ du rang 43 » est trivial et plus général qu'annoncé.**
   - Au rang 43, a₇ = b₁. Toute la branche sans racine (b₁ = 0) est donc sans co-Heawood, pas seulement S₀.
   - Statut : P (Codex et LAP), pas E.

## 1. Énoncés exacts aux sources d'origine

Dépôt `C:/home/researcher/cw/conway99-c1`, branche `origin/codex/coheawood-hoffman-20261012`, fichier
`notes/NOTE_COEXISTENCE_DEFAUTS_COCLIQUES_2026_10_12.md`. La copie `Desktop/Recherche_Conway/c1-main-codex/...` est
identique sur l. 3543-3599 (contrôlé par `diff`).

- **§66 (l. 2906-3004), cadre.**
  - C = [D ; 1ᵗ], E0 = C⁺R, P = I − C⁺C, avec E0P = 0 (66c).
  - Toute complétion s'écrit E = E0 + 3P − 7Q, avec Q un projecteur et PQ = Q (66d, l. 2941).
- **§76 (l. 3401-3447), cas q = 1.**
  - « E=M-vv^t, Cv=0, v^t v=7 » (76a, l. 3405), avec M = E0 + 3P.
  - « a_i=-eta M_ii=v_i², a_i>=0, sum a_i=7 » (76b, l. 3410).
  - « Si c<=2, il n'y en a qu'une ou deux. Si c>=3 [...] a_i=1/2 pour TOUTES les coordonnées actives [...] EXACTEMENT
    14 coordonnées actives » (l. 3427-3432). On a au plus 2¹³ = 8192 affectations (76d, l. 3433).
- **§77 (l. 3448-3508).**
  - « q = 44-rang H_-(B) » (77b, l. 3460).
  - « Si n=43 et H_-(B) est définie positive, q=1 » (l. 3468).
- **§79 (l. 3543-3599).**
  - « f=sqrt(2)*v est un vecteur propre ENTIER de norme14, à coefficients±1 » (l. 3549).
  - « soit il reste au plus DEUX affectations de signes, soit toute complétion contient un co-Heawood disjoint du bord »
    (l. 3569-3571).
  - « une complétion éventuelle est UNIQUE » (l. 3574).
  - « La famille co-Heawood demeure ouverte » (l. 3579-3580).
- **N14** (`work/c1_theta_lp_2026-10-07/NOTE.md:3739-3825`, 10/10 00:02 UTC). « **Lemma N14.** A srg(99,14,1,2) with
  rank_7(A - 3I) = 37 has no integral (-4)-eigenvector of norm 14. » (l. 3745).
  - Statut écrit par l'auteur : « computer-assisted lemma, exhaustive [...] NOT audited by another session »
    (l. 3741-3742).
  - « What is not done. No audit by another session of points 1 to 7 and of the program » (l. 3816).
- **Rang 43** : « b_1 = a_7 and a_7k = b_k » (NOTE.md:1032) ; « Au rang 43, le quotient discriminant anisotrope donne
  a7k=bk » (note 191:109, branche `origin/codex/c1-arithmetic-audit`).

## 2. Définitions et normalisations

- **Le vecteur de §79.**
  - v ∈ ker C, donc Dv = 0 et 1ᵗv = 0, et ‖v‖² = 7, parce que 7Q = vvᵗ est un projecteur de rang 1.
  - Ev = (E0 + 3P − vvᵗ)v = 0 + 3v − 7v = −4v, puisque E0P = 0 et Pv = v.
  - Donc (0, v) est un vecteur propre −4 de la matrice complète A (99 × 99).
  - Dans le cas « 14 a_i = 1/2 », f = √2·v ∈ {0, ±1}⁹⁹ et fᵗf = 2·7 = 14.
- **L'objet de N14.**
  - C'est un vecteur f ∈ ℤ⁹⁹ avec Af = −4f et fᵗf = 14.
  - Le point 1 de 17.95 (l. 3749-3751) montre |f_v| ≤ (2/3)|f| < 3, puis f = 1_X − 1_Y avec |X| = |Y| = 7.
  - C'est la norme euclidienne de L = ℤ⁹⁹ ∩ ker(A + 4I) (§1 de NOTE.md, où a₇ compte ces vecteurs avec les deux signes).
  - **Même objet, même normalisation.**
- **Le rang.**
  - N14 emploie r = rang₇(A − 3I), la convention de l'équipe (CARTE §1.6).
  - V15 n'emploie aucun rang.
  - Pas de conflit de dictionnaire r / r_ext.
- **La structure.**
  - §79 (l. 3553-3566) et N14, point 2 (l. 3752-3755), obtiennent la même chose : le biplan 2-(7,4,2), c'est-à-dire le
    complément de l'incidence de Fano.
  - Contrôle : il y a 30 biplans étiquetés sur 7 points, tous compléments d'un plan de Fano (30 = 7!/168).
  - On a 7·C(4,2) = 42 = 2·C(7,2).

## 3. Hypothèses

- **§79 suppose :**
  - un facteur (B, D) vérifiant (66a), ce qui est nécessaire pour tout bord induit ;
  - |B| = 43 et 3I − B + J/9 > 0, d'où q = 1 ;
  - λ = 1 et μ = 2 dans le comptage co-Heawood.
- **§79 ne suppose pas :** de symétrie, de borne sur α, de rang.
- **N14 suppose :** r = 37 seulement. Le lemme L23 n'est pas utilisé (l. 3746).
- **Portée de la combinaison :** les graphes hypothétiques de rang 37 et ceux du rang 43 sans racine. Aucune hypothèse
  ne manque dans cette portée.

## 4. Chaîne réécrite

1. **(§77, P, Codex, non relu par un humain.)** Si B a 43 sommets et 3I − B + J/9 > 0, alors q = 1. Toute complétion
   s'écrit E = M − vvᵗ, avec Cv = 0 et ‖v‖² = 7.
2. **(§76, P.)** Si le graphe des signes forcés a c ≤ 2 composantes, il y a au plus 2 affectations. Si c ≥ 3, on est
   dans le cas CH : exactement 14 coordonnées actives, toutes égales à 1/2.
   - Le cas CH se lit sur la diagonale de M avant toute recherche (l. 3572-3573).
3. **(§79, P.)** Dans le cas CH, toute complétion contient f = √2 v, vecteur propre −4 entier de norme 14, supporté hors
   du bord. Elle a au plus une complétion.
4. **(N14, E.)** Au rang 37, un tel f n'existe pas.
5. **Conclusion (E).** Au rang 37, pour tout facteur d'un bord positif de 43 sommets :
   - ou bien au plus 2 affectations de signes ;
   - ou bien aucune complétion de rang 37, ce qui permet un rejet immédiat.
6. **Variante au rang 43 (P).**
   - L1/7L1* ≅ F₇² est anisotrope (notes 176-177).
   - Je l'ai redérivé par la formule de Milgram :
     - la somme de Gauss vaut −7²¹, donc la partie de rang 42 a un discriminant carré ;
     - donc det U est un carré ;
     - −1 n'est pas un carré modulo 7, donc −det U non plus.
   - D'où a₇ = b₁ = 2k. Sans racine, il n'y a pas de f et la même conclusion vaut.

## 5. Redécouverte

- **10/10, NOTE 17.95.** Le « monde d'un vecteur de norme 14 », c'est-à-dire le biplan, est vide au rang 37.
- **12/10, NOTE 17.101, l. 4133-4135.** « two Hoffman cocliques meeting in 15 points (= an integral (-4)-eigenvector of
  norm 14, the world of 17.95) ». La fiche L06-100 note : « Même objet que le monde de norme 14 de N14 ».
- **14/10, V15 §79 et pont #621.** Codex écrit « famille co-Heawood toujours ouverte », sans citer N14. C'est juste dans
  sa portée, qui ne fixe pas de rang.
- **Recherches sans résultat avant le chantier :** « N14 » avec « V15 », « Heawood » ou « bord43 », et « co-Heawood »
  avec « rang 37 », dans :
  - `work/` ;
  - les notes et `AGENTS.md` de `c1-asymmetry-audit` ;
  - le pont copié (`par_jour/2026-10-14.md`).

  On ne trouve, dans le chantier, que R1 (R45) et R2 (l. 215), écrits dans la même phase.

## 6. Ce qui manquerait

- **Pour que la combinaison soit prouvée (P/C).** Il faut certifier N14 (L06 OUVERT-24), au choix :
  - un audit indépendant des points 1 à 7 de 17.95 et de `fano37.c` ;
  - le run étiqueté complet d'environ 6 h ;
  - un certificat par orbite.
- **Pour qu'elle serve.** Il faut une méthode qui énumère ou coupe les bords (B, D). Le corollaire ne change pas ce coût.
- **Formulation proposée pour la carte :**

  > « Au rang 37 (E, via N14) et au rang 43 sans racine (P), tout facteur d'un bord positif de 43 sommets demande au plus
  > deux affectations de signes, ou bien il est rejeté avant toute recherche. »
