# Le test d'étoile par droite : tous les types c ≤ 3 au rang 37, et le rang 39

LAB, 20/10/2026 après-midi. Calcul lancé pendant que le PC était libre, avec l'accord de l'utilisateur.

**Statuts.**
- **P** : preuve écrite ici, non relue.
- **E** : calcul exact sans certificat exporté (verdict d'un moteur de recherche maison).
- **A** : déjà dans l'archive.

---

## 0. Réponse courte

### 0.1 Au rang 37, l'étoile tue tous les types de droites c ≤ 3 testés (E)

| type de droite (c, d) | ρ au rang 37 | droites | runs | verdict | nœuds max | temps moteur max |
|---|---|---:|---:|---|---:|---:|
| c = 1 générique (1, 1) | 0 | 40 | 40 | 40 UNSAT | 5 277 | 0,08 s |
| c = 1 à 7-torsion, `c1t` (1, 2) | 1 | 10 | 20 (δ = 1, 3) | 20 UNSAT | 2 273 | 0,06 s |
| c = 2, composantes 18 + 18 (2, 2) | 1 | 10 | 20 | 20 UNSAT | 95 773 | 1,7 s |
| c = 2, composantes 12 + 24 (2, 2) | 1 | 10 | 20 | 20 UNSAT | 84 874 | 1,3 s |
| c = 2, composantes 6 + 30 (2, 2) | 1 | 10 | 20 | 20 UNSAT | 126 355 | 2,4 s |
| c = 2 à torsion, équilibré (2, 3), les trois découpages | 2 | 18 | 36 | 36 UNSAT | 45 649 | 0,8 s |
| c = 2 à torsion, déséquilibré (2, 3), r(T) = 1 | 0 | 18 | 18 | 18 UNSAT | 332 568 | 6,2 s |
| c = 3, composantes 12 + 12 + 12 (3, 3) | 2 | 6 | 12 | 12 UNSAT | 4 724 521 | 86 s |
| c = 3, composantes 6 + 6 + 24 (3, 3) | 2 | 3 | 6 | 6 UNSAT | 9 375 339 | 153 s |
| c = 3, composantes 6 + 12 + 18 (3, 3) | 2 | 5 | 10 | 10 UNSAT | 4 749 922 | 76 s |
| c = 1 à double torsion, `c1tt` (1, 3) : δ = 1, 3 (ρ = 2) et 8 directions déséquilibrées (ρ = 0) | 2 / 0 | 6 | 60 | 60 UNSAT | 5 743 | 0,1 s |

Total : 118 droites, 262 runs, tous UNSAT.
- c ≤ 2 : 98 droites et 174 runs ;
- c = 3 : 14 droites et 28 runs ;
- c = 1 avec d = 3 : 6 droites et 60 runs.

**Ce qui était déjà connu (A, NOTE_FUSION §3, 19/10).** La mort au rang 37 des droites c = 1 génériques, c = 1 à
torsion et c = 2 (d = 2 et 3) avait déjà été établie (E) avec le moteur de droite complète (oblr2, 60 lointains) :
5 + 42, 8/8 et 18/18 + 27/27 instances. NOTE_FUSION chiffrait la vérification exhaustive à « des milliers
d'années-CPU », environ 1 s par droite c = 1 et 4 à 100 s par droite c = 2. Elle était jugée hors de portée.

**Ce qui est nouveau ici.**
1. Une unité dix fois plus petite suffit : l'étoile d'un seul sommet proche, soit 10 lointains au lieu de 60.
2. Le coût par droite baisse d'un facteur 25 environ : 40 ms mesurés en C++ pour c = 1, au lieu d'environ 1 s, et
   davantage après optimisation.
3. **Les droites c = 3 meurent aussi au rang 37**, en 1 à 2 minutes. C'est un maillon nouveau. Avec m = 4 exclu
   (A), il remplace le registre m ≥ 3 au rang 37 (§7).

- Aucune feuille n'est jamais atteinte : chaque étoile meurt avant d'avoir placé ses 10 sommets lointains.
- Le type de forme δ du résidu n'est fixé par aucune règle prouvée pour ces types de droites. On teste donc les deux,
  et la droite ne meurt que si les deux meurent. C'est le cas partout.

### 0.2 Au rang 39, l'étoile tue aussi les droites testées, en 40 min à 2 h chacune (E)

- **Graine 1** ((τ|7) = −1, x = 0, δ = 3) : UNSAT.
  - δ = 3 est la forme qu'impose la règle de NOTE_RESEAUX_DE_DROITE §2, dérivée à la main et non relue.
  - 254 614 885 nœuds, aucune feuille, 1,28·10¹⁰ coupes réelles, 6 919 s.
  - La même droite meurt au rang 37 en 2 511 nœuds.
  - Le run avec l'autre forme (δ = 1), qui rend le verdict indépendant de la règle, est en cours.
- **Graines 3 et 4** : UNSAT, en 44 et 40 min.
  - La graine 3 est dans le cas anisotrope ((τ|7) = +1, δ = 1).
  - La graine 4 est hyperbolique, avec la forme imposée par la règle.
- **Graines 2, 5, 6 et 7**, ainsi que les formes hors règle des graines 1 et 4 : en cours (§5).
- **Lecture.**
  - L'heuristique de NOTE_OBSTRUCTION §3.2 prévoyait environ 10⁵ solutions de l'étoile au rang 39 avec les seules
    conditions mod 7.
  - Le filtre réel (projecteur lointain, valable à tout rang) coupe énormément : 1,28·10¹⁰ coupes pour la
    graine 1. Aucune configuration n'atteint 10 lointains.
  - **Contrôle sans le filtre réel** (graine 4, STAR_NOREAL=1) : TIMEOUT à 900 s, 98,9 M nœuds, 573 branches de
    profondeur 1 sur 12 647, aucune feuille. Le filtre accélère donc la recherche d'un facteur d'environ 8. Sa
    nécessité n'est pas établie : mod 7 et couplage pourraient suffire, puisque l'heuristique donne une espérance
    d'environ 0,1 à 1 solution sans le filtre.
  - C'est, à ma connaissance, le premier verdict complet par droite au rang 39 : recherche faite dans work/ et dans
    le dépôt. Le moteur de droite complète (oblr2, oblr3) donnait TIMEOUT au rang 39 (NOTE_FUSION R4,
    NOTE_CHATGPT_CORE37_VERIF).

### 0.3 Ce que cela change au plan

- **Au rang 37**, une preuve par ordinateur prend la forme suivante, sans le registre m = 3 :
  - (a) le test d'étoile, droite par droite, sur **tous** les graphes de droite c ≤ 3 ;
  - (b) l'exclusion de m = 4 (A ; verdicts CP-SAT à certifier).
  - Coût mesuré : environ 7 à 9·10⁵ heures-cœur avec le moteur actuel (§7). Une optimisation d'un facteur 5 à 10
    est en cours, ce qui viserait environ 10⁵ heures-cœur. NOTE_FUSION parlait de « milliers d'années-CPU »,
    soit au moins 10⁷.
  - Il faut aussi écrire un générateur ordonné, porter la préparation en C++ et certifier les verdicts.
- **Aux rangs 39 à 43**, le test d'étoile ne passe pas à l'échelle. Il faut une idée nouvelle.
- **Correction** de mon estimation précédente sur la route c (§6) :
  - m = 3 n'est pas « presque fermé » ;
  - m = 2 n'est pas un calcul fini de 3,4 millions de gabarits.

---

## 1. Coût mesuré au rang 37, droites c = 1 génériques (E)

Fichier `boost_logs/cost37.jsonl`. Graines 1 à 40, (τ|7) = −1 (L23 de Codex, A), et premier x hors triangle
transversal.

- 40 étoiles sur 40 sont UNSAT.
- Nœuds : minimum 654, médiane 2 181, maximum 5 277. Aucune feuille.
- Temps du moteur `star39.exe` : 0,03 à 0,08 s, démarrage du processus compris.
- La préparation en Python prend environ 1 s. En C++, ce serait de l'ordre de la milliseconde : 10 × 3 600 triplets,
  avec des opérations de dimension 36.
- **Correction après mesure.** J'avais estimé environ 5 ms par droite en C++. Le temps du moteur mesuré ci-dessus
  inclut le démarrage du processus, et l'estimation était fausse.
- **Mesure réelle** avec `line37.cpp`, test complet en C++, de G_T jusqu'au verdict, validé sur 40 droites (mêmes
  statuts, x, candidats et nœuds que la chaîne Python) :
  - médiane 38 à 42 ms par droite testée : construction 0,04 ms, préparation 3 ms, recherche 35 à 42 ms ;
  - 99ᵉ percentile 103 ms, maximum 385 ms ;
  - sur 3 000 tirages uniformes : 21 % K < 0, 35 % exclus par L23, 12 % à 7-torsion (test séparé), 31 % testés
    (932/932 UNSAT) ;
  - soit environ 14 ms par graphe tiré ;
  - **100 000 tirages** (graine 777001, `boost_logs/line37_rand100k_seed777001.json`) : **33 754 droites testées, toutes
    UNSAT**, aucun SAT, aucun TIMEOUT. Médiane 35,8 ms, 99ᵉ percentile 70 ms, maximum 327 ms, 7 353 nœuds au plus,
    12,4 ms par tirage. À 95 % de confiance, la proportion de droites qui survivent est inférieure à 3/33 754, soit
    environ 9·10⁻⁵.

## 2. Une étoile pour tout type de droite : `star_prep_gen.py`

### 2.1 Formalisme

C'est celui de `oblr_prep.py` (A, NOTE_FUSION) :
- X est le g-inverse réflexif symétrique du bloc proche M[N,N] mod 7, de rang 38 − d ;
- β(a, b) = e_aᵀ X e_b ;
- ρ = r − 38 + d, avec une forme D ;
- condition diagonale : uᵀDu = −3 − β(w, w) ;
- condition sur les paires : R = β + uᵀDu′ ∈ {0, 1} ;
- filtres L2, L4 (|K|/6 noms par composante) et orthogonalité au noyau proche ;
- encodage déséquilibré des droites à torsion (u = (b + c, b − c), D = diag(4, 3)).

Le moteur `star39.cpp` n'est pas modifié. Il calcule R = 4 − Σ_k Y_a[noms_b] + uᵀDu′. Avec Y_a = 3 − X e_a mod 7, la
somme vaut 18 − β ≡ 4 − β, donc R = β + uᵀDu′ exactement.

### 2.2 Validation (E)

- **Rang 37, graines 1, 2 et 4** : mêmes candidats (3 070 / 2 503 / 2 292), mêmes nœuds (2 511 / 1 527 / 838) et mêmes
  coupes réelles (70 539 / 39 907 / 29 791) qu'avec `star39_prep.py`, qui utilise Ω.
- **Rang 39 (ρ = 2, δ = 3), graine 4** : mêmes triplets, mêmes candidats (u et drapeau canonique) et mêmes dd. Sur
  200 000 paires tirées au hasard, les valeurs de Green sont identiques mod 7, sans aucun écart.

### 2.3 Projecteur réel quand c ≥ 2 (P)

**Énoncé.** Pour toute droite, Π_T est le projecteur sur l'espace propre −4 de R dans ker E, et

    rang Π_T = 7 + c        (c = nombre de composantes de G_T).

**Preuve.**
- Par L4, Eᵀκ = 0 pour les c − 1 différences de composantes κ, qui sont dans Z. Donc rang E = 35 − c et
  dim ker E = 25 + c.
- R² + R + EᵀE = 12I + 2J. Sur ker E, qui est orthogonal à 𝟏, R a donc les valeurs propres 3 et −4.
- Trace de R sur l'espace des lignes de E :
  - RE^T y = Eᵀ(−I − G)y pour y ∈ Z ∩ κ^⊥ ;
  - la valeur propre est 8 sur 𝟏 ;
  - tr(G | Z ∩ κ^⊥) = −3 − 3(c − 1) = −3c, sur un espace de dimension 34 − c ;
  - la trace vaut donc 8 − (34 − c) + 3c = 4c − 26.
- Comme tr R = 0, tr(R | ker E) = 26 − 4c.
- Avec a + b = 25 + c et 3a − 4b = 26 − 4c, on obtient a = 18 et b = 7 + c.

**Conséquence.** La formule H = 3I − R − EᵀZE + J/9 = 7Π_T reste vraie si Z est le pseudo-inverse de 3I − G + J :
la dérivation de NOTE_OBSTRUCTION §1.1 passe avec K⁺, et e_w ⊥ κ. Dans le code,
Z = (3I − G + J + P_ker)⁻¹, ce qui revient au même sur les e_w.
- Les coupes réelles (H ⪰ 0 et 7I − H ⪰ 0) valent donc pour tout c.
- Le test de rang « ≤ 8 » sur l'étoile n'a de sens que pour c = 1. Pour c ≥ 2, le rang ≤ 7 + c est automatique sur
  10 vecteurs liés par la relation du tout-un. Les runs c ≥ 2 sont faits avec STAR_NORANK=1.
- Rapprochement possible avec P3 de Codex (rang T_X = 23 − c) : 30 − (23 − c) = 7 + c. Non vérifié.

## 3. Les droites c = 2 et à torsion au rang 37 (E)

Fichiers `boost_logs/gen37_c2.jsonl`, `gen37_c2t.jsonl`, `gen37_c3_*.jsonl` et `gen37_c1tt.jsonl`. Pilote :
`boost_logs/gen_batch.py`.
- Pour c = 2 (d = 2), ρ = 1, et les deux formes δ ∈ {1, 3}. Les 30 droites et les 60 runs sont UNSAT, au plus 2,4 s
  chacun.
- **c1t**, connexe à 7-torsion, d = 2.
  - Au rang 37, seul le cas équilibré est possible : 37 = 38 − d + 2r(T) + ρ force r(T) = 0 et ρ = 1.
  - Les 10 droites et les 20 runs sont UNSAT, au plus 2 273 nœuds.
  - L'orthogonalité au noyau garde environ 2 600 à 3 300 candidats, contre environ 10 000 pour c = 2.
- **c = 2 à torsion**, d = 3. Deux cas au rang 37 :
  - équilibré, avec ρ = 2 ;
  - déséquilibré, avec r(T) = 1 et ρ = 0.

  Les 18 droites (6 par découpage) et les 54 runs sont UNSAT. Dans le cas équilibré, l'orthogonalité vide souvent un
  domaine entier : l'étoile meurt alors dès la racine, en 1 nœud.
- **c = 3**, d = 3 (découpages 12 + 12 + 12, 6 + 6 + 24, 6 + 12 + 18), ρ = 2, δ ∈ {1, 3}.
  - Les 14 droites et les 28 runs sont UNSAT, en 25 à 153 s et 1,8 à 9,4 millions de nœuds.
  - Il y a environ 30 000 à 41 000 candidats par étoile. L4 et le filtre réel suffisent à finir la recherche.
  - Comparaison : une droite c = 1 au rang 39 a aussi ρ = 2, mais environ 150 000 candidats et coûte 2 h.
- **c = 1, d = 3** (`c1tt`, environ 0,35 % des droites connexes). Au rang 37, r(T) = 0 avec ρ = 2, ou r(T) = 1 avec
  ρ = 0.
  - Dans le cas déséquilibré, les e·ker des candidats couvrent deux directions. On découpe donc selon les 8 droites
    F₇g possibles (option `--kappa`) : dans un graphe avec r(T) = 1, tous les lointains ont e·ker sur une même
    droite.
  - Les 6 droites et les 60 runs sont UNSAT, au plus 5 743 nœuds.

## 4. En cours au moment de la note

- Étoiles du rang 39, graines 2 à 7.

## 5. Rang 39, droites c = 1 (E)

| graine | (τ\|7) | δ | candidats | branches de profondeur 1 | verdict | nœuds | temps |
|---|---|---|---:|---:|---|---:|---:|
| 1 | −1 | 3 (règle) | 153 268 | 18 188 | **UNSAT**, aucune feuille | 254 614 885 | 6 919 s |
| 1 | −1 | 1 (hors règle) | | 18 436 | en cours | | |
| 3 | +1 | 1 (règle, plan anisotrope) | 114 505 | 14 736 | **UNSAT**, aucune feuille | 102 079 170 | 2 628 s |
| 4 | −1 | 3 (règle) | 117 942 | 12 647 | **UNSAT**, aucune feuille | 93 242 509 | 2 409 s |
| 4 | −1 | 1 (hors règle) | 119 820 | 12 959 | **UNSAT**, aucune feuille : la droite meurt avec les deux formes, sans dépendre de la règle | 85 040 317 | 2 166 s |
| 6 | −1 | 3 (règle) | 129 241 | 16 354 | **UNSAT**, aucune feuille | 129 035 234 | 3 420 s |
| 2 | −1 | 3 (règle) | 121 735 | 14 124 | **UNSAT**, aucune feuille | 141 014 038 | 3 712 s |

- La graine 3 a (τ|7) = +1. Elle est donc exclue au rang 37 par le seul L23. Au rang 39, elle est permise avec le
  plan anisotrope, et c'est l'étoile qui la tue.

## 6. Correction de mes estimations sur la route c

Ma réponse précédente donnait 85 % de chances pour « c_min ≥ 2 », pour un coût de 10 000 à 100 000 heures-cœur, sur la
base de 3,4 M de gabarits racine. C'était trop optimiste. Ce que dit l'archive :

- **m = 3** (`c3_inventaire_2026-10-19.md` ; NOTE_MANDAT_REPRESENTATION §1.2, A) : 35 gabarits ouverts au 19/10.
  - P3 n'en couvre que 7 : 125 des 128 sous-tranches sont faites, et 3 tournent.
  - Les autres n'ont encore aucune méthode : 20 n'ont pas de paire partagée forcée, et 10 n'ont pas assez de grilles
    pour les familles existantes.
- **m = 2, racine sur une droite c = 2** (`C21_ROOT_CENSUS_PARTIAL`, `C3_COST_PILOT §Taille`, A) :
  - les 3,4 M de gabarits ne couvrent que k ≥ 4 grilles à la racine ;
  - pour k ≤ 3, l'estimateur de Knuth donne environ 2,8·10¹⁰ gabarits étiquetés, soit environ 10⁷ à symétrie près ;
  - le test de Gram n'en coupe qu'environ 93 % ;
  - l'archive concluait : « il faut un argument nouveau pour c ≤ 2 ».
- **m ≤ 2 (II), où tout sommet est sur une droite c ≤ 2** : NOTE_MANDAT note « aucune méthode finie ».

**Ce qui change aujourd'hui.** Le test d'étoile droite par droite tue les droites c ≤ 2 **au rang 37**, de tous les
types testés (§0.1). La branche m ≤ 2 du rang 37 n'a donc plus besoin de la route c qui ne dépend pas du rang. Il
suffit d'énumérer les graphes de droite.

## 7. Plan au rang 37 et son coût

> **Remplacé par THEOREME_REDUCTION_R37.md (Théorème 6.1).** La réduction n'utilise que P ≤ 852 :
> - au moins 18 droites ont t ≤ 7 ;
> - t ≤ 7 entraîne c ≤ 4 et l'existence d'un x hors des triangles transversaux.
>
> Elle ne passe ni par les verdicts CP-SAT de m = 4, ni par le registre, ni par L23, ni par la règle sur δ. La
> formulation « c ≤ 3 + m = 4 exclu » ci-dessous avait aussi un trou : une droite à c ≤ 3 peut avoir t = 12, et
> alors aucun x n'est utilisable. Les comptes de coût restent valables.

**Énoncé de réduction (P, immédiat).**
- m ≤ 4 est prouvé (A, P ≤ 852) et m = 4 est exclu (A, verdicts CP-SAT sans certificat portable). Un graphe de Conway
  a donc une droite T avec c(T) ≤ 3.
- Au 7-rang 37, cette droite doit passer le test d'étoile de rang 37 pour son type (c, d) et pour **toutes** les
  variantes possibles : forme δ, cas équilibré ou déséquilibré, direction de torsion.
- **Donc, si tous les graphes de droite c ≤ 3 meurent au test d'étoile de rang 37, aucun graphe de Conway n'a r = 37.**
- Le registre m = 3 n'intervient plus. NOTE_FUSION §3 passait par lui (maillon 4), avec les gabarits sans méthode du
  §6.

**Coût du test exhaustif**, en estimation grossière :
- **Nombre de classes.** (12!)³ / ((2⁶·6!)³ · 6) ≈ 1,87·10¹¹ classes de triplets de bijections, en supposant l'action
  libre.
- **Proportions sur des tirages uniformes (E)** (`lg_counts.py 20000 2026`, sortie dans `boost_logs/`) :
  - 79,2 % vérifient K ≥ 0 ;
  - 15 838 de ces graphes sont connexes et 8 ont deux composantes, d'où environ 1,48·10¹¹ graphes c = 1
    admissibles ;
  - c = 2 représente environ 7·10⁷ graphes. Le compte par composantes donne aussi environ 6·10⁷ : environ
    8,4·10⁸·p₅/6 pour 6 + 30, avec un seul type de composante à 6 sommets admissible, le prisme (K₃,₃ viole
    K ≥ 0) ; environ 5·10⁶ pour 12 + 24 ; environ 10⁶ pour 18 + 18. Les 10⁹ à 10¹⁰ de NOTE_FUSION étaient donc trop
    hauts ;
  - parmi les connexes : d = 1 pour 85,6 %, d = 2 pour 14,1 %, d = 3 pour 0,35 % ;
  - pour d = 1, (τ|7) = +1 et −1 sont à parts égales (6 800 contre 6 750).
- **c = 1 au rang 37.** Ceux qui ont (τ|7) = +1 sont exclus d'emblée par L23. Il reste environ 6,3·10¹⁰ génériques et
  2,2·10¹⁰ à torsion, soit environ 8,5·10¹⁰ droites.
  - Mesure `line37` : environ 14 ms par classe tirée, tri compris, soit 1,9·10¹¹ × 14 ms ≈ 7·10⁵ heures-cœur ;
  - les droites à torsion se testent en quelques ms ;
  - **moteur optimisé `line37_fast`** (NOTE_LINE37_FAST.md) : 3,4 à 3,6 ms par droite testée, soit environ 10 fois
    plus vite, avec des résultats identiques (0 écart sur 40 + 3 000 + 20 000 tirages ; mêmes nœuds ; candidats et
    valeurs R et h identiques au bit près). On passe à environ 1,2 ms par classe tirée, soit environ 6,5·10⁴
    heures-cœur pour c = 1.
- **c = 2.** Environ 7·10⁷ droites, à 1 à 6 s chacune, soit environ 2·10⁴ à 10⁵ heures-cœur.
- **c = 3.** Par composantes, environ 2·10⁵ droites (6 + 6 + 24 domine), à 1 à 3 min chacune, soit environ
  5·10³ heures-cœur.
- **Total : environ 8·10⁵ heures-cœur aujourd'hui**, et 1,5 à 2·10⁵ après optimisation. Cela représente environ 1 mois
  sur 1 000 cœurs aujourd'hui, ou 1 semaine après optimisation. Ce n'est pas faisable sur le PC du labo.
- **À écrire** :
  - un générateur ordonné (augmentation canonique sur les trois bijections) ;
  - la préparation en C++ ;
  - des certificats ou une double implémentation pour les verdicts UNSAT.

**Types non couverts par le moteur (X).** Ils relèvent tous de la 7-torsion :
- c = 2 avec d = 4 ;
- c = 3 avec d = 4, environ 15 % des droites c = 3 ;
- d ≥ 5.

Au rang 37, ces types demandent un résidu de rang 3, ou un cas déséquilibré avec un résidu de rang 1. Il faut étendre
le moteur à u ∈ F₇³. Le reste est couvert :
- c = 1 avec d = 1, 2, 3 ;
- c = 2 avec d = 2, 3 ;
- c = 3 avec d = 3.

**Rangs 39 à 43.**
- Au rang 39, une droite c = 1 a ρ = 2 et coûte des heures (§5).
- Une droite c = 2 y a ρ = 3, que le moteur ne gère pas et qui coûterait plus encore.
- Aux rangs 41 et 43, l'étoile est heuristiquement satisfaisable (NOTE_OBSTRUCTION §3.2).
- Aucune énumération exhaustive n'est envisageable : il faut une idée nouvelle.

## 8. Fichiers

**Dans le dépôt, `merge_2026-10-19/`** :
- `star_prep_gen.py` : étoile pour tout type de droite (formalisme X, modes `--unbal` et `--kappa`, type `c1tt`) ;
- `lg_counts.py` : recensement par tirage des graphes de droite ;
- cette note.

**Dans le scratchpad, `boost/`** :
- `watchdog.py` : garde « on coupe dès qu'il y a une saisie ou une nouvelle application » ;
- `star_boost.py` et `gen_batch.py` : pilotes ;
- journaux `*.jsonl` et sorties du rang 39.

Tout est recopié dans `merge_2026-10-19/boost_logs/`, avec le second lanceur P3 (`p3local_runner2.py`).
