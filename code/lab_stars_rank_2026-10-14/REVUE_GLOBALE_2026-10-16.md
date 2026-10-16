# Revue globale du projet « graphe de Conway à 99 sommets » : état au 16/10/2026 (LAB)

Sources : les neuf rapports de relecture `C:\Users\RESEARCHER\cw\review\01..09` (tous partiels, agents arrêtés par la limite de
débit), mes notes du 14 au 16/10 (`work/stars_rank_2026-10-14/`), le journal et les fichiers de Codex jusqu'au 16/10 13:19.
Je n'ai rien re-prouvé, sauf ce qui est marqué « re-prouvé ici ».

Statuts :
- PROUVÉ : preuve écrite ;
- RELU : preuve relue par une deuxième session (IA, sauf mention contraire) ;
- EXACT : calcul exact et complet ;
- SAT/CP : verdict de solveur complet, sans certificat ;
- DRAT : preuve d'insatisfiabilité vérifiée par drat-trim ;
- INDICE : données seulement ;
- OUVERT.

Aucun résultat de C1 n'a été relu par un humain.

## 0. En bref

1. Le graphe n'est ni construit ni exclu.
2. Les cas symétriques sont fermés dans les dossiers, avec des statuts inégaux (§1). S'il existe, le graphe est donc
   asymétrique (cas C1).
3. Pour C1, une dizaine de réductions sont prouvées pour tout graphe (§2). Aucune ne ferme C1. La plus forte : si la loi
   (H-MATCH) valait aux 21 paires de droites d'un sommet, le graphe n'existerait pas. Donc chaque sommet a au moins 4
   paires « cassées » (G18).
4. Fait nouveau du 16/10 (§3) : aucun des mondes « quatre étoiles » étudiés ne s'étend.
   - 645 germes de rang 30 : tous tués par l'invariant arithmétique DISC, et aucun ne reçoit une seule colonne extérieure.
   - 34 bases variées : aucune ne reçoit une cinquième étoile ; le cas HB est certifié par DRAT.
   - Le modèle est validé sur un vrai srg(243,22,1,2) : SAT à 4, 5 et 6 étoiles.
5. Conséquence (§4) : les quelque 1,1 million de structures qui soutenaient le « mur 13 » ne sont pas des blocs de Conway.
   Les implications prouvées restent vraies. En revanche, (H-MATCH) n'a plus d'appui expérimental.
6. La question ouverte la plus nette est : existe-t-il UNE structure admissible à cinq étoiles (52 labels) ?
   - Si la réponse est non, il n'y a pas de graphe de Conway.
   - Aujourd'hui la réponse est INCONNUE : sur 34 cas, 18 ont été lancés et tous les 18 sont en TIMEOUT à 90 min.
   - J'ai tout arrêté à 12:50 UTC (Valorant ouvert sur le PC du labo).
   - Étalonnage (§8, corrigé en fin d'après-midi) : sur srg(243), où la réponse est oui, cadical trouve une structure à
     cinq étoiles en 17 s, et CP-SAT en 76-87 s une fois mon encodage corrigé. Pour Conway (modèle 3 fois plus petit),
     cadical reste indécis plus de 23 min et CP-SAT corrigé 7 fois 20 min. C'est un indice étalonné, pas une preuve.
7. Codex a construit 15 lignes complètes et exactes sur les 84 labels (λ, μ et comptes de racines exacts, sans condition
   PSD). Des cadres partiels existent donc, et la non-extension n'est pas immédiate.
8. Anciens outils à brancher tout de suite (§5) :
   - le lemme d'équilibre (re-prouvé ici en cinq lignes) ;
   - le théorème N9 ;
   - les coupes PSD linéaires ;
   - le modèle de couplage exact ;
   - l'encodeur srg_sat avec DRAT ;
   - les huit srg(243) comme contrôles positifs.
   Le plan chiffré est au §7.

## 1. Cas symétriques (d'après le rapport 02 et le rapport 04)

| Cas | Ce qui l'exclut | Statut enregistré |
|---|---|---|
| ordre 11 | Behbahani-Lam (calcul) ; Lou-Murin 2014 « non vérifié » | littérature |
| ordre 3 (C3) | argument de discriminant mod 3 « P1 », dépôt conway99-c3-experimental, 23/09, plus Lean 4 (26 552 déclarations, run GitHub Actions sandboxé) | dérivé et vérifié par machine, aucune relecture humaine |
| ordre 7 (C7) | preuve sans ordinateur, dépôt conway-C7, 02/10, plus Lean | article complet, audité, non arbitré ; Lean accepté en local sans sandbox |
| ordre 2 (C2) | Route C : 156/156 réseaux unimodulaires impairs de rang 24 exclus, 07/10 17:47 UTC | assisté par ordinateur, contrôlé seulement par des IA ; recertification des raccourcis « transfer » (≤ 2 479 669 paires) parquée le 07/10 |

La chaîne de littérature citée dans les dossiers est la suivante :
- Makhnev-Minakova : |Aut| divise 2·3³·7·11 ;
- Cesarz-Woldar ;
- Behbahani-Lam : seuls 2 et 3 peuvent diviser |Aut|.

Avec C3 et C7, il ne reste que |Aut| ∈ {1, 2}. Avec C2, il ne reste que C1.

## 2. Ce qui est prouvé pour tout graphe de Conway (sans symétrie)

Notations :
- v est un sommet ;
- les 14 voisins de v sont les lettres 0..13, et les droites par v sont {v, 2i, 2i+1} ;
- les 84 non-voisins de v sont les labels (paires non appariées de lettres) ;
- L_r est l'ensemble des 12 labels contenant r ;
- B est l'incidence lettres/labels et Γ le graphe sur les 84 labels ;
- T = 3I − Γ − K et U = 7Π − T.

1. **Critère global sur 84 labels** (Codex P4, 16/10 ; PROUVÉ, lu par Codex seul).
   - Pour tout Γ binaire symétrique, T + U = 7Π.
   - Si T et U sont PSD avec rang T ≤ 30, la trace (tr T = 210) force T² = 7T, rang 30, U de rang 40 et TU = 0.
   - On en déduit A99² = 12I − A99 + 2J.
   - Réciproquement, tout srg(99) donne ces conditions.
   Le problème entier équivaut donc à trouver Γ sur 84 labels.
2. **Blocs à quatre étoiles.** Pour deux droites l, m par v (44 labels) :
   - T et U sont PSD et nullité(T) ≥ 14 (PROUVÉ, standard) ;
   - DISC : pour tout ensemble I de 30 labels avec T_I non singulière, la classe carrée de det(8T_I) vaut 2 ou 14 (PROUVÉ et
     re-dérivé par moi le 16/10 ; partie robuste : seuls 2 et 7 peuvent avoir un exposant impair).
3. **(H-MATCH aux 21 paires d'un sommet) ⇒ pas de graphe.**
   - Le sommet serait un point de Hamming, contredisant L8 (Codex, note 105) ou Makhnev 1988.
   - Statut : PROUVÉ, relu de façon adversariale le 15/10.
   - Contraposée G18 (modulo L10) : chaque sommet a au moins 4 paires de droites dont le bloc est PSD, de nullité ≥ 14,
     avec des appariements d'étoiles non reliés par h.
4. **Théorème N9** (moi, nuit du 14/10 ; PROUVÉ à la main) : aucun ensemble de 9 sommets n'induit exactement 17 arêtes.
   Conséquences :
   - lemme des tuiles (jamais exactement 3 des 4 appariements de coins de deux droites en un sommet) ;
   - fermeture des prismes ;
   - autour d'une droite, un compte ≠ 5 ;
   - e(S) ≤ 3, 5, 7, 9, 12, 14, 18, 19 pour |S| = 3..10.
   Les solveurs CDCL ne retrouvent pas ces faits.
5. **Lemme d'équilibre** (cahier C2, lemme 24.0, A6 ; PROUVÉ et RELU dans C2 ; re-prouvé ici, voir §5.1).
   - Le voisinage N(l) d'une droite induit un graphe cubique sur 36 sommets.
   - Chaque composante C a une taille multiple de 6 et rencontre chaque sommet de l en |C|/3 voisins.
   - Chaque sommet lointain (les 60 labels qui évitent les lettres de l) a exactement |C|/6 voisins dans C.
6. **Cinq étoiles, défauts de h** (Codex F1/F2 ; ma vérification pas à pas, message 897 ; PROUVÉ). Sur les étoiles
   0,1,2,3,4, sans aucune symétrie supposée :
   - D ≥ 12 ;
   - au moins 4 des 8 lignes {4,y} cassent h = (01)(23) ;
   - aucune structure à cinq étoiles n'est invariante par h (lemme h5, moi).
   Version φ : au moins 3 lignes cassent tout appariement croisé réel (Codex F5, accepté par moi sans re-vérification).
7. **Fenêtre de rang** (07-08/10, audit IA) : r = rang_7(A − 3I) ∈ {37, 39, 41, 43} ; r ≤ 35 est exclu.
   - La route F7 exclut b = 26..32.
   - b = 34 demanderait a_4 ≈ 1,4·10⁷ supports garantis : bloqué.
8. **Planchers de comptage** (Codex, notes 100-105 et 14/10 ; PROUVÉS, plusieurs avec certificats) :
   - P ≤ 1151 prismes à la main, P ≤ 852 avec certificat ;
   - au plus 126 grilles ;
   - au plus 396 co-Heawood ;
   - 10 ≤ k ≤ 28, k pair ;
   - pas de point de Hamming (L8) ;
   - pas de sommet à 21 grilles (N2).
   Ce sont tous des planchers moyennés. La note 100 le dit : un plafond exact non moyenné manque. Une impossibilité à cinq
   étoiles serait exactement ce plafond.
9. **Inégalité signée à 15** (Codex P9 ; PROUVÉ, conséquence de T ⪰ 0) : pour 7 labels P et 8 labels N,
   e(P) + e(N) − e(P,N) ≤ 14.
10. **Rigidité de complétion** (Codex R1-R5, 14/10 ; PROUVÉ, contrôles exacts) :
    - deux graphes de Conway diffèrent toujours d'une matrice de rang pair, et de rang 2 seulement par une transposition
      impossible ;
    - tout graphe contient des bords B de 43 ou 44 sommets à partir desquels la complétion est décidée par une inversion
      43×43 et au plus 8192 signes, avec au plus 2 complétions isomorphes.

Le résidu de C1 est donc simplement : existe-t-il Γ sur 84 labels qui vérifie les comptes C1 exacts (14 lettres) et C2
exacts (λ, μ) ? Toutes les conditions spectrales en découlent par le point 1.

## 3. Le fait du 16/10 : le monde à quatre étoiles ne s'étend pas

Détails dans `work/stars_rank_2026-10-14/EXT84_2026-10-16.md`.

- **DISC** (EXACT, 645 germes PSD de rang 30, y compris HB et urep100 de Codex) : tous échouent, avec la classe 2·3·5 ou
  2·3·5·7.
  - Mécanisme de grille (PROUVÉ) : les vecteurs κ, v_l et v_m engendrent un sous-réseau de classe 10. Un germe de grille
    ne passe DISC que si son orthogonal a la classe 5 ou 35.
- **Colonnes** (EXACT, outil de Codex) : pour les 645 germes, les domaines des 40 labels extérieurs sont tous vides. Aucun
  germe ne reçoit un seul sommet extérieur.
- **Cinquième étoile, combinatoire seule** (λ, μ, sans PSD) :
  - INFAISABLE pour HB (DRAT vérifié, 1 576 lemmes), pour urep100, pour une base aléatoire et pour 31 bases variées ;
  - la sixième étoile est infaisable pour les 5 choix de droite ;
  - mêmes verdicts avec deux modèles indépendants (CP-SAT, cryptominisat/cadical) ;
  - contrôle positif : le même encodage donne SAT sur le vrai srg(243,22,1,2) new243_trade_aut108 à 4, 5 et 6 étoiles.
- **Cinq étoiles sans base** (la vraie question) : INCONNU.
  - CP-SAT : 1 500 s.
  - cadical : 23 min.
  - Découpage en 34 orbites selon M_4 (groupe d'ordre 3072) : 18 cas terminés, tous en TIMEOUT à 90 min ; cas 0 brisé par
    symétrie : indécis après plus d'1 h.
  - Arrêté à 12:50 UTC. Résultats dans `scratchpad/split5p/results.jsonl`.
- **Familles symétriques à cinq étoiles** (CP complet) : INFAISABLES sous Z4 extérieur, h, (02)(13), h×Z4 et
  ⟨(68)(79),(10 12)(11 13)⟩. Aucune structure à cinq étoiles n'a jamais été trouvée.
- **Côté Codex, le même jour :**
  - 15 lignes complètes sur 84 labels (toute L_4, plus (0,2), (0,3), (0,10)), toutes exactes ; c'est un cadre et non une
    structure à cinq étoiles, car les lignes de L_0..L_3 ne sont pas complètes ;
  - un bloc gris à 15 lignes non extensible (obstruction à cinq lignes) ;
  - core30 exclu par les comptes globaux sur 84 labels (CP-SAT en 26 s, sans certificat) ;
  - modèle exact du graphe entier en 19 types pointés : tous les pilotes sont INCONNUS.

## 4. Ce que cela change pour les conclusions des 14-16/10

- **Restent vraies** (preuves) : tout le §2, le lemme h5, la réduction (H-MATCH ⇒ pas de graphe) et G18.
- **Perdent leur appui** (données) : le « mur 13 » et toute statistique sur les blocs à quatre étoiles. Cela concerne :
  - 414/416 classes complètes, environ 1,14 M structures, aucune cassée PSD de nullité ≥ 14 ;
  - les marches PSD (environ 10⁵ visites) ;
  - les comptes non-grille (≥ 396 blocs) dans leur usage comme indice.
  Ces populations ne contiennent aucun bloc qui reçoive une cinquième étoile. Les conjectures (H-MATCH), N9-NG, NG5 et
  NG7 restent OUVERTES, sans indice pour ni contre.
- **Leçon de méthode** : pour juger une loi locale, il faut désormais filtrer par l'extension (5ᵉ étoile ou colonne
  extérieure), pas seulement par T, U PSD et le rang.

## 5. Anciens travaux utiles aujourd'hui

### 5.1 Lemme d'équilibre (pour exclure)

Origine : cahier C2 (lemme 24.0, A6, R36 ; prouvé et relu ; il a fermé toutes les configurations ancrées de C2).

Preuve, re-faite ici pour tout srg(99,14,1,2), sans symétrie :
- Soit l = {a1, a2, a3} une droite, N_i les 12 voisins de a_i hors de l (disjoints, car λ = 1), et N = N_1 ∪ N_2 ∪ N_3.
- Un sommet w de N_1 a un voisin dans N_1 (le troisième sommet de la droite {a1, w, ·}) et, par μ = 2, un voisin dans N_2
  et un dans N_3. Donc G[N] est cubique.
- Soit y un vecteur porté par N, constant sur chaque composante, avec 1ᵀy = 0. Alors yᵀAy = 3‖y‖². Comme A n'a que les
  valeurs propres 3 et −4 sur 1^⊥, on a Ay = 3y.
- Avec y = 1_C − (|C|/36)·1_N :
  - un sommet lointain z a exactement |C|/6 voisins dans C ;
  - a_i a exactement |C|/3 voisins dans C.
- Les tailles de composantes sont donc des multiples de 6, et il y a au plus 6 composantes.

Lien avec notre modèle :
- Dans le modèle à cinq étoiles, les graphes cubiques des droites l0 = {v,0,1} et l1 = {v,2,3} sont entièrement présents,
  avec 28 labels lointains chacun.
- Le lemme ne dit rien si G[N(l)] est connexe. Il impose des égalités exactes, que le modèle n'a pas aujourd'hui, si c(l) ≥ 2.
- Dans les blocs PSD, il est déjà impliqué : les c − 1 vecteurs y_C donnent des vecteurs du noyau de T_S, et T_S ⪰ 0 force
  alors les égalités sur les labels lointains du bloc.

Usage : couper le modèle en c(l0), c(l1) ∈ {1, ≥ 2} et ajouter les égalités dans la branche ≥ 2. Coût : une heure.

### 5.2 Coupes PSD linéaires (pour exclure)

- Origine : Codex (O5 `psd_exact_cuts.py` ; P7, bibliothèque de 398 coupes ; P9 signée à 15).
- 8T = 24I − 8Γ − 3BᵀB − BᵀMB + 2J est affine en Γ. Pour chaque vecteur entier q, qᵀ8Tq ≥ 0 est donc une inégalité
  linéaire valide sur les arêtes, et de même pour 15U et pour 7I − T (valeurs propres de T dans [0, 7]).
- Sur 52 labels, rang T ≤ 30 doit rester vrai (sous-matrice principale) : la nullité de T_52 est ≥ 22.
- Usage : boucle paresseuse (solution trouvée → test PSD/rang → coupe → on relance).

### 5.3 Théorème N9 et lemme des tuiles (pour exclure)

- Origine : moi, nuit du 14/10, à la main.
- Ce sont des clauses courtes que CDCL ne retrouve pas.
- Les clauses de tuiles et de prismes de Codex (N4, N5 : 8 316 clauses, `prism12_no_double_cut.cnf`) sont du même type.

### 5.4 Modèle de couplage exact à deux blocs (pour exclure ou construire)

- Origine : structures lab, NOTE_S33, `sat_twoblock.py`, équations CROSS.
- Il couple un bloc avec les labels extérieurs. C'est exactement l'étape qui échoue aujourd'hui (la coexistence des étoiles).

### 5.5 Encodeur indépendant et DRAT (pour certifier)

- `srg_sat.py` et `kk5_certify.py` (`work/c1_night_2026-10-14`).
- drat-trim fonctionne (HB certifié aujourd'hui).
- Tout verdict UNSAT à cinq étoiles devra passer par deux modèles et un DRAT par cas.

### 5.6 Contrôles positifs (pour ne pas se tromper)

- Les huit srg(243,22,1,2) : BvLS, twin, Γ3..Γ8 ; les tordus sont meilleurs que BvLS.
- `validate243.py` est déjà prêt.
- Calibration par solution plantée du structures lab : un INCONNU ne porte aucune information.

### 5.7 Relèvement d'Astra et principe d'extension (pour certifier)

- `verify_astra_certificate.py` : un vecteur négatif de 8T sur un bloc partiel se relève en un vecteur du graphe.
- Lemme A7 de C2 : les vecteurs propres de A_UU de valeur 3 ou −4 s'étendent par zéro, avec ‖Bᵀw‖² = (3−α)(4+α)‖w‖².
- Ce sont les outils pour rendre lisible une obstruction trouvée par solveur.

### 5.8 Assembleur 44 → 84 → 99 et critère P4 (pour construire)

- Origine : Codex, commit 4e3ac85.
- `four_star_complete.py` et `schur_domain_join.py` vérifient A99² exactement avant de dire SRG99_CONSTRUCTED.
- Contrôle positif : le graphe de rook 3×3 est reconstruit.
- C'est la porte de sortie si une structure à cinq étoiles apparaît.

### 5.9 Cadres de Codex et échanges équilibrés (pour construire)

- Fichiers : `global_star15_balanced_search_20261016.json`, `conway_star_trades.py`.
- Ce sont les seuls objets exacts, construits sans graine, qui portent 15 lignes complètes.
- Les échanges gardent toujours le même type de M_4 (un 10-cycle et une arête commune) : les autres types de M_4 n'ont
  jamais été essayés.
- La recherche à 23 lignes (L_0 ∪ L_4) est incomplète : 100 cadres testés, 175 en attente.

### 5.10 Littérature sur le problème à 84 sommets (rapport 01)

- Thakkar-Severini : réduction enracinée à 84 sommets, épuisement circulant à 68 %.
- Gray-Taylor 2020 : onze types de voisinage d'arête.
- Keramatipour : pas de Paley(9) partout.
- Lou-Murin 2014 : graphe des triangles.
- À relire seulement si un de ces faits se branche sur le modèle à cinq étoiles.

## 6. Jamais lancé (relevé dans les rapports)

- Le test « une seule grille en x ».
- Cube-and-conquer avec estimation de Knuth de la taille de l'arbre (aucun coût n'existe pour les 34 cas).
- Un contrôle SAT à l'échelle BvLS du modèle à cinq étoiles avec contraintes renforcées.
- DRAT pour T1/kk6 (45 min et 2,5 h).
- Le programme thêta de niveau 63 et l'isotropie des accidents 7-adiques.
- Les autres types de M_4 dans les cadres de Codex.
- La version par paires de l'« LP de types » (note 117 de Codex, 26/09). La version symétrique tue 60 à 93 % des
  configurations et jamais tout : les relaxations linéaires symétriques sont faisables au niveau des paramètres.

## 7. Plan proposé (ordre, coût, critère de réussite)

1. **Renforcer le modèle à cinq étoiles** avec les §5.1-5.3 (équilibre en deux branches, coupes PSD paresseuses sur T_52
   et 7I − T_52, clauses N9 et tuiles) et la brisure de symétrie lex-leader déjà écrite (`five_symbreak.py`).
   - Contrôle : les srg(243) doivent rester SAT.
   - Mesure : le temps jusqu'à UNSAT sur les sous-cas connus (base HB, familles symétriques) doit baisser.
   - Coût : une demi-journée de code, puis des essais de 5 min maximum.
   - Réussite : un des 34 cas décidé (UNSAT ou SAT) en moins de 90 min.
2. **Estimation de Knuth** sur les 34 cas avant toute longue campagne, pour donner un coût chiffré honnête. Coût :
   quelques minutes par cas. Si le total est acceptable, la campagne passe par toi (PC du labo ou AWS, sur ton accord).
3. **Lire l'obstruction de HB** (DRAT de 1 576 lemmes, noyau minimal par suppression `ext5_core.py`) pour en tirer un lemme
   lisible du type h5, valable pour une famille entière de bases (par exemple toutes les grilles de rang 30). Coût : une
   demi-journée. Réussite : un énoncé prouvé à la main qui explique au moins une des 34 non-extensions.
4. **Cadres de Codex** : tester les 15 lignes avec les coupes PSD et le rang (mort spectrale déjà ?), puis les autres types
   de M_4. Ce travail est partagé avec Codex.
5. **Répondre à Codex** sur ce qu'il demande : la liste du §2 (réductions prouvées pour tout graphe) et le résidu exact (Γ
   sur 84 labels ; la question des cinq étoiles en est la plus petite relaxation non décidée).

Pas de longue campagne et pas de cloud sans ton accord. Tant qu'un jeu est ouvert sur le PC, je reste en basse
consommation.

## 8. Ajouts du 16/10 après-midi (après l'envoi du bilan)

- **CORRECTION (fin d'après-midi, à la demande de Dilan : « pourquoi le solveur bloque-t-il sur srg(243) ? »).** Le
  blocage venait de mon encodage CP-SAT, pas du problème.
  - Le journal CP-SAT montre 346 000 booléens dont seulement 4 186 arêtes. Les produits p ≥ e_it + e_jt − 1 n'étaient
    liés que dans un sens : le solveur décidait sur ces variables libres et entretenait un programme linéaire à 280 000
    colonnes. Résultat : 7,2 M décisions pour seulement 4 400 conflits en 400 s.
  - Corrigé (`cp_probe.py --reify --order all --vsel min` : p = e_it ∧ e_jt, branchement sur les arêtes seulement, base
    d'abord, valeur 0 d'abord) : K = 22 cinq étoiles trouvé en 87, 76, 76, 82 s (graines 1-4) ; quatre étoiles en 45 s.
    Avec --reify seul (recherche par défaut), le temps est erratique : 152 et 214 s pour les graines 1-2, INCONNU à 1 200 s
    pour les graines 3-4.
  - Remarque de Codex (juste) : avec des sommes seulement majorées, p ≥ x + y − 1 est déjà une projection exacte. Le
    lien dans les deux sens ne change pas la satisfiabilité, il aide seulement la propagation et le branchement. Les
    anciens UNSAT restent valables.
  - cadical, encodage stars_rank : K = 22 cinq étoiles SAT en 17 s (20 s avec l'encodage corrigé).
  - Conway (52 labels), mêmes méthodes : 7 essais CP-SAT corrigés (graines, ordres, sans LP, 4 workers) tous INCONNUS à
    1 200 s, avec 127 000 à 2,4 M conflits ; cadical indécis à 23 min ce matin, et 90 min par cas M_4.
  - Les lignes ci-dessous (« un INCONNU n'est pas un indice ») reposaient sur l'encodage défectueux et sont remplacées
    par : quand des structures à cinq étoiles existent de façon générique, les deux solveurs les trouvent en 17-90 s ;
    pour Conway rien en plus de 20 min. Indice étalonné de rareté ou de non-existence, pas une preuve.
- **Étalonnage sur srg(243), première version, encodage défectueux** (`cp_generic.py`, CP-SAT, un seul worker, aucune
  arête fixée ; mêmes contraintes C1, C1' et C2 avec 22 lettres) :
  - 4 étoiles (76 labels) : trouvé en 34 s ;
  - 5 étoiles (92 labels) : INCONNU à 240 s, alors que de vraies structures existent (les huit srg(243)).
  Le même saut 4 → 5 étoiles bloque donc le solveur là où la réponse est oui. Un INCONNU à cinq étoiles pour Conway n'est
  pas un indice de non-existence (rejoint la calibration par solution plantée du structures lab). Avec 20 min, le cas
  K = 22 trouve une solution en 351 s ; celui de Conway (52 labels seulement) reste INCONNU à 1 500 s.
- **Taux d'extension de bases aléatoires** (`ext_rate.py` : base à quatre étoiles tirée par objectif aléatoire, puis
  test de la cinquième étoile) :
  - K = 22 : 5 bases obtenues sur 8 tirages, et les 5 s'étendent (solutions en 41-54 s) ;
  - K = 14 (Conway) : 8 bases sur 8 ne s'étendent pas (INFAISABLE en 6-24 s), en plus des 34 bases variées du matin.
  La barrière de la cinquième étoile est donc propre à Conway. C'est une motivation, pas une preuve.
- **Où ça casse** (`ext_rows.py`) : on accroche seulement les labels {4,6}, {4,7}, ..., avec la lettre 4 en simple borne
  (étoile 4 non exacte). Jusqu'à 6 labels passent, le 7ᵉ est INFAISABLE (8 bases sur 8 ; une base casse déjà au 6ᵉ).
  - Noyau (`ext_rows_core.py`, échantillon 1) : les 6 labels {4,6..11} sont tous nécessaires, plus 31 labels de base sur
    44, sans aucun coin {02,03,12,13}. Pas de motif local.
  - Problème sans base « 4 étoiles exactes + 7 labels {4,t} » (`plain_rows.py`) : INCONNU à 240 s avec l'ancien
    encodage. **CORRIGÉ :** avec l'encodage et les solveurs étalonnés, il a des solutions :
    - cadical en 62 s (encodage corrigé) et 81 s (stars_rank) ;
    - CP-SAT corrigé en 88 s (sans LP) et 224 s ;
    - avec 6 labels, cadical en 11 s.
    Le blocage au 7ᵉ label des bases aléatoires n'est donc PAS universel, et cette piste d'exclusion tombe.
  - **Le vrai seuil est le 8ᵉ label** (`five_cnf.py`, `r7_batch.py`, cadical) :
    - témoins à 7 labels trouvés pour 6 graines sur 7 (34 à 396 s), tous vérifiés indépendamment (`check_struct.py`) ;
    - aucun des 6 n'accepte le 8ᵉ label {4,13} (UNSAT en 1,7 à 4,2 s) ni l'étoile 4 exacte (UNSAT en 0,7 à 2,9 s) ;
    - problème sans base « 4 étoiles exactes + les 8 labels {4,t}, lettre 4 bornée » (appelé R8) : TIMEOUT à 1 800 s
      dans les deux encodages. Cinq étoiles complètes (encodage corrigé) : TIMEOUT à 1 800 s.
    - R8 est une relaxation de la cinquième étoile. **R8 INFAISABLE exclurait Conway** (après DRAT, modèle indépendant et
      relecture). C'est la relaxation la plus faible encore indécise ce soir : 52 labels, 1 326 arêtes, la lettre 4 en simple
      borne ; avec un label de moins (R7), la réponse est oui.
- **Coût du découpage brut** (`five_cubes.py`) : avec M_4 et M_0 fixés au hasard (environ 3,5·10⁴ cubes à symétrie près),
  2 cubes sur 2 sont INCONNUS à 100 s. Le coût dépasse donc 1 000 heures CPU sans borne haute connue. Ce n'est pas un coût
  défendable avec le modèle actuel.
- **Cadres de Codex vus à cinq étoiles** (`five_from_frame.py`) :
  - 15 lignes fixées : INFAISABLE en 9 s (cohérent avec son bloc gris, obstruction par quotas C1/C2 seuls) ;
  - 12 lignes de L_4 seules : INCONNU à 240 s.
- **Noyau minimal de HB** (`ext5_core.py`, minimal à 20 s près) : 30 des 44 labels, aucun coin. Il contient les
  appariements croisés « alignés » {0,t}~{1,t} et {2,t}~{3,t}. L'obstruction n'est pas un petit motif local : pas de
  lemme court à en tirer.
- **Identité de trace de Codex** vérifiée indépendamment : sous C1 exact et binarité, tr T = 210 et tr T² = 1470 sur ker B.
  Donc C1 + binaire + T, U ⪰ 0 ⟺ srg(99). Codex note que le centre fractionnaire Γ0 = (2J − Bᵀ(I+M)B)/10 vérifie C1 avec
  T = 3P et U = 4P : la positivité continue seule n'est jamais infaisable.
- **Littérature** : la prépublication arXiv 2610.16266 (Natal, Al-saadi, 12/10/2026) annonce la non-existence par un
  programme SOS. La borne T(99) ≤ 55 est seulement numérique (flottants, pas de certificat exact), et fausse telle
  qu'énoncée :
  - 11 grilles 3×3 disjointes ont 66 triangles, sans diamant ni K_{2,3} (contre-exemple de Codex, vérifié) ;
  - si les densités interdites sont induites, K_99 suffit.
  Aucun changement de statut.

## 9. Le phénomène derrière les indices (16/10 soir, en cours)

Question de Dilan : pourquoi des réponses si rapides pour srg(243) et les graphes existants, et rien ici ?

Notations :
- B est la base à quatre étoiles (L_0 ∪ ... ∪ L_3, 44 labels) ;
- B' est l'ensemble des 36 labels de B qui évitent 4 et 5 ;
- X = {4,t : t = 6..13} (8 labels), C4 = {r,4} (4 coins), C5 = {r,5}, K = {02, 03, 12, 13} ;
- κ_y est le nombre de voisins de y dans K.

1. **Comptage exact, PROUVÉ pour tout k** (λ = 1, μ = 2). Avec tous les labels {4,t} accrochés :
   - Σ_{x ∈ X} |N(x) ∩ B| = 8(k − 6) − Σκ_x ;
   - la capacité de B vaut Σ_y c(y,4) − Σ_{c ∈ C4} |N(c) ∩ B| = 8k − 56 + Σκ_c ;
   - donc Σκ_x + Σκ_c ≥ 8, et ≤ 8 (chaque coin de K a au plus 2 voisins dans L_4).
   Tout est donc serré : chaque label de B a exactement c(y,4) voisins dans L_4. Avec un label de moins, il reste 8 unités de
   marge. C'est vrai aussi pour k = 22 : ce n'est pas encore le phénomène.
2. **Le graphe Ω, PROUVÉ.** Les 36 labels de B' deviennent 36 arêtes distinctes d'un graphe Ω sur les 12 labels de L_4,
   disjoint de M_4. Les 24 labels extérieurs qui évitent 5 prennent exactement les 24 paires restantes. Par étoile r,
   Ω_r (10 arêtes) a des degrés imposés (2 pour chaque x, sauf corrections), donc c'est une union de chemins et de cycles.
   - Densité : 36 sur 60 paires disponibles chez Conway (60 %), 68 sur 180 pour k = 22 (38 %).
3. **Borne qui dépend de k, PROUVÉE.** Deux labels de X non adjacents ont exactement un voisin commun (μ = 2, lettre 4
   commune). Le nombre de labels de B' dont les deux voisins de L_4 sont dans X est donc au plus 28 − a (a = arêtes de M_4
   dans X).
   - Chez Conway : 36 labels contre au plus 28 − a paires. Il faut n_1 + n_2 ≥ 8 + a, où n_i est le nombre de labels de
     B' ayant i voisins dans C4.
   - Pour k = 22 : 68 labels contre 120 paires, aucune contrainte.
   Toutes les égalités de comptage restent compatibles (vérifié) : il faut encore la structure C2 de la base.
4. **Mesures** (pas des preuves) :
   - en forçant les 8 labels sur un témoin à 7 labels (`r8_soft.py`, minimum de contraintes violées), le meilleur
     compromis laisse 3-4 labels {4,t} à court d'un voisin dans une étoile L_r : c'est un manque de capacité ;
   - noyaux minimaux au niveau des arêtes (`r8_core.py`, python-sat, 3 témoins) : 79 à 81 faits, portant sur 39 ou 40
     des 44 labels de base. Presque chaque test de suppression a atteint sa limite de 100 000 conflits : ces noyaux ne
     sont minimaux qu'en apparence. Aucun petit motif local ; l'obstruction porte sur toute la base.
   - R8 et la cinquième étoile avec cassage de symétrie lex-leader (3 071 éléments du groupe, 11,9 M clauses ; contrôle :
     quatre étoiles reste SAT en 52 s) : TIMEOUT à 3 600 s (4 essais). Découpage par M_0 (52 classes) : 4 cas sur 4 en
     TIMEOUT à 600 s.
   - Lancés pour 2 h (16/10, 17:05 UTC) : cadical `--unsat` sur R8 avec et sans cassage de symétrie, et kissat 4.0.4
     (python-sat) sur R8 avec cassage.
5. **Prudence** : la rigidité observée est aussi ce qu'on attendrait d'un graphe asymétrique qui existerait. L'indice
   « srg(243) va vite » parle des structures locales génériques, pas d'une preuve de non-existence.

## 10. Hygiène

- Le travail EXT84 du 16/10 n'est pas encore commité. À faire sur la branche privée habituelle (lab/theta-lp-2026-10-08).
- Les documents de l'espace de travail postérieurs au 01/10 ne sont pas suivis par git (rapport 04) : risque de perte.
- Personne n'a relu à la main C2, C3 ni les résultats de C1. Les preuves de Codex du 14-16/10 n'ont presque toutes qu'un
  seul lecteur : ton instruction du 14/10 16:08 a arrêté les contre-vérifications croisées.
