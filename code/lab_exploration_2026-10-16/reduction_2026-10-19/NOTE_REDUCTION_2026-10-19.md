# Pourquoi on ne peut pas tout balayer, et ce qu'une réduction de la route finie doit fournir

*19/10/2026, LAB. Mandat de l'utilisateur, 19/10 : un prompt ChatGPT transmis, et sa propre remarque : « un tout nouveau
cadre, de la novelty, expliquer pourquoi on peut pas juste tout balayer … admettre que Conway n'existe pas, que C1
n'existe [pas], et que notre route finie mène à la résolution, seul but étant de la réduire pour avoir quand même une
preuve ».*

**Statuts.**
- **P** : preuve écrite ici.
- **C** : calcul exact.
- **E** : expérience de solveur (verdict sans certificat, durée bornée).
- **H** : heuristique (pas une preuve).
- **A** : déjà dans l'archive (référence donnée).
- **X** : ouvert.

**Cadre.**
- Fichiers : `work/exploration_2026-10-16/reduction_2026-10-19/`.
- Une seule machine locale. Chaque test tient en moins de 5 minutes.
- Pendant les tests, 12 fils au plus, avec l'accord de l'utilisateur (80 %). À partir de 17 h 10 UTC, 1 fil (20 % demandés).

---

## 0. Résultat, en premier

**Aucune réduction de la branche m = 1 n'est obtenue aujourd'hui.** P3 (registre c3) tourne toujours et sera rapporté à
part. Ce qui est nouveau :

### 0.1 Un mur de dureté mesuré exactement à la taille de Conway (E, nouveau)

On considère le système proche–lointain d'**une seule droite** (§2) :
- 7 200 inconnues binaires, qui codent le choix des noms des 60 sommets lointains ;
- les contraintes L1–L3, plus L4 quand c ≥ 2.

Aucun des deux solveurs ne le décide, quel que soit c. L'archive notait « never tried on a connected generic ball »
(17.53) : c'est le premier essai pour c = 1.

| G_T | contraintes | solveur | limite | verdict |
|---|---|---|---|---|
| c = 1, aléatoire (graine 1, t = 1) | L1–L3 | CP-SAT 9.15, 12 fils | 280 s | UNKNOWN |
| le même G_T | L1–L3 | CaDiCaL 1.9.5 (pysat), 1 fil | 270 s | UNKNOWN |
| c = 3, blocs (2,2,2), aléatoire | L1–L4 | CP-SAT, 12 fils | 280 s | UNKNOWN |
| c = 6 (six grilles), aléatoire | L1–L4 | CP-SAT, 12 fils | 240 s | UNKNOWN |

**Contrôle positif planté.** On tire un appariement 3D aléatoire, puis on demande au solveur de retrouver un appariement
qui a les mêmes marges de lettres. L'instance est donc SAT par construction.

| n (= k − 2) | lointains | CP-SAT, 12 fils | CaDiCaL |
|---|---|---|---|
| 6 | 12 | 0,0 s (2 graines) | — |
| 8 | 24 | 0,0 et 0,2 s | 0,0 s |
| 10 | 40 | 0,5 et 0,5 s | 0,4 et 0,9 s |
| **12 (Conway)** | **60** | **UNKNOWN 280 s** (et 2 × 120 s à 1 fil) | **UNKNOWN 270 s** (et 20 s) |

- **Le mur se situe entre n = 10 et n = 12**, c'est-à-dire au paramètre même de Conway.
- Toute solution trouvée est revérifiée hors du solveur : `verify` dans `ll_test.py`, et `recheck_margins_equal` pour
  le planté (vrai à chaque fois).
- Une piste fausse a été écartée : la première interruption de CaDiCaL dans pysat n'était pas honorée (le processus
  ne s'arrêtait pas). Le solveur tourne désormais dans un processus fils, tué à l'échéance.

### 0.2 Un budget d'entropie du système d'une droite (H, nouveau comme quantification)

Quantité mesurée : log10 du nombre attendu de solutions du système proche–lointain, par G_T étiqueté (`budget.py`).
Le calcul repose sur trois hypothèses (§4) :
- approximation gaussienne locale ;
- covariance **exacte** de Hoeffding pour une bijection aléatoire ;
- indépendance entre les trois paires de classes.

| | L1 seul | L1–L3 |
|---|---|---|
| Conway, c = 1 : 300 G_T aléatoires, médiane [min ; max] | −27,4 [−33,0 ; −23,3] | −47,6 [−53,5 ; −42,9] |
| Conway, somme sur les ≈ 10^11,2 classes de G_T à c = 1 | −16 | −36 |
| srg(243,22,1,2), 3 droites réelles (c = 5) | +68 à +70 | +32 à +35 |
| srg(243,22,1,2), 20 G_T aléatoires | — | +45 à +50 |

**Lecture.**
- À 243, le système d'une droite est sous-contraint : environ 10^32 à 10^35 solutions attendues par droite. Il ne dit donc rien, ce qui
  est cohérent avec l'existence de ces graphes.
- À 99, le nombre attendu de solutions pour une droite vaut environ 10^−48 : chaque droite est heuristiquement
  impossible. Pourtant aucun solveur ne le montre pour une seule droite.
- Explication proposée (H) : la surcontrainte est **diffuse**. Elle est répartie sur les 432 marges et les 1 728 triplets.
- Un sous-système (une partie des lointains seulement) change les égalités de marges en inégalités. Il redevient alors
  sous-contraint (H).
- C'est le régime des CSP aléatoires surcontraints. Pour eux, les réfutations par résolution sont de taille
  exponentielle : Chvátal–Szemerédi 1988, Ben-Sasson–Wigderson 2001 (mécanisme de largeur). C'est cohérent avec le mur
  de 0.1.
- À l'inverse, tout ce qui a fermé quelque chose dans le projet était **concentré** : C2, C3, C7, et le registre c ≥ 3
  par les filtres de Gram. Ce sont des identités exactes, de l'intégralité, de l'arithmétique.

### 0.3 À c = 1, aucune identité linéaire locale au-delà des marges (P, §3)

- Supposons EEᵀ = K. Les relations lointaines n'imposent alors **rien de plus** sur E au niveau linéaire :
  - ER = 2J − E − GE ;
  - R² + R + EᵀE = 12I + 2J.
- Raison : la compatibilité se réduit à KE = 12E + 10J − GE − G²E, qui est une identité. De plus, EREᵀ est
  automatiquement symétrique.
- La seule identité exacte « gratuite » sur E est le lemme équitable (variance nulle). Elle n'existe que pour c ≥ 2.
  Elle vaut, en ordres de grandeur de contraintes exactes et concentrées (H pour les chiffres, `budget_extra.json` ;
  P/A pour le lemme) :
  - c = 2 : −21 (blocs 1,5) à −27 (blocs 3,3) ;
  - c = 3 (2,2,2) : −48 ;
  - c = 6 : −94.
- Cela s'accorde avec la ligne de partage du projet : c ≥ 3 s'est fermé, c ≤ 2 explose. Mais **L4 seul ne suffit pas** :
  avec L4, le système d'une droite reste UNKNOWN à c = 3 et à c = 6 (0.1). Les fermetures c ≥ 3 sont venues des
  gabarits racine (sept droites à la fois) et du Gram entier, pas du système d'une droite.

---

## 1. Pourquoi on ne peut pas tout balayer (chiffré)

| Branche | Objets à tuer | Nombre | Coût unitaire observé | État le 19/10 |
|---|---|---|---|---|
| m = 4 | gabarits racine (racine minimisant 9s + 8g) | 79 | CP-SAT | fermé (verdicts sans certificat portable) |
| m = 3 | gabarits c ≥ 3, k ≤ 12, Gram entier | 10 052 | secondes à heures ; les 37 derniers bords sur 256 vCPU Spot | 35 ouverts, P3 en cours (20 bords ouverts à 17 h 20 UTC) |
| m = 2 | gabarits racine c_min = 2, k = 4 à 11 (filtres P, O', S', K, Z ; `cpp_census`) | **3 443 556** (2 002 986 avec `--la`) ; k ≤ 3 non disponible | non mesuré, au moins celui de c3 | jamais lancé |
| m = 1 | types de droite c = 1 (classes de G_T) | **≈ 1,5 × 10^11** (`budget.py`) | > 5 min × 12 fils pour **une** droite (0.1) | hors de portée |
| A : co-Heawood sans rang | secondes lignes par base | ≈ 3 × 10^22 (NOTE 17.101) | — | hors de portée |

**Comptage des G_T à c = 1.**
- G_T étiquetés : (12!)³ ≈ 10^26,04. La fraction qui vérifie K ≥ 0 vaut 0,787 sur 300 tirages, et tous les tirages
  admissibles sont connexes.
- On divise par le groupe (6!·2⁶)³·3! ≈ 10^14,77.
- Il reste ≈ 10^11,17 classes, presque toutes sans automorphisme.

**Coûts.**
- Branche m = 1 : le balayage coûterait (nombre de classes) × (coût d'une droite). Ce coût est d'au moins
  10^11 × 300 s ≈ 10^6 années-CPU, et il est minoré seulement : chaque droite est restée UNKNOWN.
- Branche m = 2 : à 1 minute par gabarit (valeur non mesurée, probablement optimiste), le coût est d'environ 6
  années-CPU, plus k ≤ 3.

---

## 2. Le système proche–lointain d'une droite

### 2.1 Notations

- Le graphe est Γ = srg(v, k, 1, 2), avec n = k − 2 (n = 12 pour Conway, n = 20 pour 243).
- On fixe une droite T = {p, q, s}.
- Les trois classes sont C_0 = N(p) − T, C_1 = N(q) − T et C_2 = N(s) − T. On renumérote pour que le partenaire de i
  soit i ⊕ 1 : la paire {2j, 2j+1} est une droite passant par le point de T.
- G_T est formé des arêtes partenaires et de trois bijections s01, s12, s20 entre les classes.
- F désigne l'ensemble des sommets lointains.
- Un sommet lointain a exactement 2 voisins dans chaque classe, non partenaires (μ = 2 avec chaque point de T).
- Il en résulte des bijections : F ↔ {paires non partenaires de C_0} (ses « p-noms »), puis F → paires de C_1 et
  F → paires de C_2.
- L'incidence E (proche × lointain) se réduit donc à deux bijections.

### 2.2 Conditions nécessaires (P)

Les quatre conditions sont déjà dans l'archive pour les composantes (6,6) (NOTE 17.53 et son addendum, avec le filtre de
Codex). Elles sont rederivées ici dans le cas général.

**(L1)** EEᵀ = K := (k − 2) I − G − G² + 2J − J_cl.
- *Preuve.* A² = (k − 2)I − A + 2J. Pour u, u' ∈ N(T), les voisins communs se trouvent dans T (une fois si u, u' sont
  de même classe), dans N(T) ((G²)_{uu'}) et dans F ((EEᵀ)_{uu'}).
- Les blocs de même classe sont automatiques, par bijectivité des noms.

**(L2)** Pour x ∈ N(T) et w ∈ F : |N_G(x) ∩ noms(w)| ≤ 2 − [x ∈ noms(w)].
- *Preuve.* x et w ont au plus 2 voisins communs, et au plus 1 s'ils sont adjacents (λ = 1).

**(L3)** Un 3-ensemble transversal (un sommet par classe) est contenu dans les noms d'au plus un lointain.
- *Preuve.* Deux lointains qui partageraient 3 voisins violeraient μ (ou λ).
- Réciproquement, deux lointains ne partagent au plus qu'une lettre par classe : ce sont deux arêtes distinctes de CP(6).
  L3 est donc exactement « au plus 2 voisins proches communs ».

**(L4)** Conway seulement : chaque lointain a exactement |K|/6 noms dans chaque composante K de G_T.
- C'est le lemme équitable, archivé comme « équilibre » (17.53).
- *Preuve.* Pour la composante K, EEᵀ 1_K = 10k·1. La variance sur F de |N(f) ∩ K| est donc nulle.
- Ce lemme est propre à r = 3 = degré de G_T. À 243, EEᵀ1_K = 8·1_K + 10k·1, et rien de tel n'existe.

### 2.3 Contrôle (C)

- Sur 9 droites réelles de trois srg(243,22,1,2) (`check_243.log`), L1 à L3 donnent **0 violation**.
- Graphes : new243_trade_aut162, new243_trade_aut108 et BvLS, droites 0, 57 et 200.
- Valeurs de c observées : 4, 5 et 10.

### 2.4 Rappel (A)

Dans les srg(243) connus, toute droite est dans une grille et c = 1 n'arrive jamais : `EXPLORATION.md`, l. 394. Recontrôlé
ici sur quatre graphes et toutes leurs droites (`c_dist_243.log`) :

| graphe | profils de composantes (nombre de droites) |
|---|---|
| aut162, aut108 | (6,6,6,6,36) : 405 ; (6,6,6,42) : 324 ; (6,24,30) : 162 |
| BvLS | (6¹⁰) : 891 |
| tricayley | (6⁵,30) : 486 ; (6⁴,36) : 405 |

La famille connue n'offre donc **aucun étalonnage** pour c ≤ 2.

### 2.5 Identité de coupe (A : `c1_balcut.py`, 17/10)

- Soit S ⊂ N(T) avec q sommets dans chaque classe. Alors
  Σ_{f ∈ F} (|noms(f) ∩ S| − q/2)² + Σ_u d_∂(u)² = 7 e(S, S̄).
- Cela vient de y = (A − 3I)(1_S − (q/12)1_{N(T)}), qui est un vecteur propre −4 de norme 7|cut|.
- **Complément du jour (P, mineur).** Pour q impair, chaque terme lointain vaut au moins 1/4. On en tire
  7e − Σd_∂² ≥ 15, puis e(S, S̄) ≥ 3, car d_∂² ≥ d_∂ donne Σd_∂² ≥ 2e.

---

## 3. Preuve de 0.3 : l'information de Gram est épuisée par K

On suppose EEᵀ = K et on cherche R (symétrique, R1 = 8·1) avec :
- (a) ER = D := 2J − E − GE ;
- (b) R² + R = 12I + 2J − EᵀE.

**Symétrie.** (a) donne EREᵀ = DEᵀ = 20J − K − GK, car JEᵀ = 10J. Ce terme est symétrique, car G commute avec K. En
effet, GJ_cl = J_cl G = J : chaque sommet a exactement un voisin dans chaque classe.

**Compatibilité de (a) et (b).**
- En multipliant (b) à gauche par E et en utilisant (a) : DR + D = 12E + 20J − KE.
- D'un autre côté, avec JR = 8J : DR = 2JR − ER − GER = 16J − D − GD.
- L'égalité équivaut donc à KE = 12E + 4J + GD = 12E + 10J − GE − G²E.
- Or KE = 12E − GE − G²E + 12J − 2J, car J_cl E = 2J.
- C'est donc une **identité** : aucune condition nouvelle sur E.

**Ce qu'il reste.**
- R est déterminé sur l'image de Eᵀ.
- Sur ker E (de dimension 25 + c), R vaut 3P_3 − 4P_W, où P_W est le projecteur lointain de rang 7 + c (Théorème 1 de
  la note du mandat de représentation).
- Les seules contraintes restantes sur R sont combinatoires : entrées 0/1 et diagonale nulle.
- Pour c = 1, l'information exacte sur (G_T, E) se réduit donc aux marges K. Tout le reste est combinatoire (0/1),
  c'est-à-dire diffus. ∎

---

## 4. Le budget d'entropie : définition, hypothèses, limites (H)

### 4.1 Définition

Pour une paire de classes (a, b), on pose X_uv = #{f : u ∈ a-nom(f), v ∈ b-nom(f)}.
- Pour une bijection uniforme, X est une statistique de permutation.
- Covariance exacte (Hoeffding) : Σ = (A ⊗ A)/(m − 1), où A est la Gram centrée de l'incidence de CP(n/2).
  - Valeurs propres de A : n − 4, avec multiplicité n/2 − 1 ;
  - n − 2, avec multiplicité n/2 ;
  - 0, sur le vecteur 1.
- On pose P(X = K) ≈ (2π)^{−d/2} det Σ^{−1/2} exp(−(K − μ)ᵀΣ⁺(K − μ)/2), avec d = (n − 1)².
- Budget L1 : 2 log10 m! + Σ_{3 paires} log10 P.
- Facteur L3 : (1 − 2(n − 3)/(m − 1))^{Σ C(K_pq, 2)}.
- Facteur L2 : (1 − 4/n²)^{6m}.

### 4.2 Calibration

| | lointains m | log10 (m!)² | budget L1–L3 par droite |
|---|---|---|---|
| Conway | 60 | 163,8 | −48 (médiane) |
| srg(243) | 180 | 660,6 | +32 à +50 |

**Ce que le budget explique.**
- Les gabarits survivent à tous les tests locaux, parce qu'ils sont sous-contraints.
- Une seule droite est difficile pour les solveurs. La surcontrainte n'est atteinte qu'à l'échelle de la droite
  entière, sans noyau local.
- Les droites c ≥ 2 sont plus contraintes. Le facteur L4 est calculé exactement par lointain (énumération des 60³
  triplets de noms) :
  - c = 2 : 0,444 (blocs 1,5) et 0,36 (3,3) par lointain, soit 10^−21,1 et 10^−26,6 pour les 60 lointains ;
  - c = 3 (2,2,2) : 0,158, soit 10^−48,0 ;
  - c = 6 : 0,0267, soit 10^−94,4.

**Ce qu'il n'explique pas.**
- Le mur de dureté de 0.1. Le budget L1 des instances plantées (solutions autres que la plantée, 5 graines) vaut :
  - n = 8 : −40 à −49 ;
  - n = 10 : −57 à −71 ;
  - n = 12 : −81 à −95.

  Elles sont toutes fortement surcontraintes, et pourtant n ≤ 10 est trivial. Le mur dépend donc aussi de la taille de
  l'espace (40! contre 60!) et de la propagation. Il est empirique.
- Ce n'est pas une preuve. Les corrélations (structure) peuvent créer des solutions que le premier moment ne voit pas.
  Le premier moment global naïf (14-régulier ou 22-régulier aléatoire, λ et μ poissonniens) prédit d'ailleurs aussi la
  non-existence des srg(243) : environ 10^−12 990 graphes étiquetés, calcul à la main dans la session. C'est l'échelle
  locale qui sépare 99 de 243, pas l'échelle globale.

---

## 5. Ce qu'une réduction doit fournir, et les pistes pour m ≤ 2

### 5.1 Critère

Une réduction utile exhibe un objet **forcé** dont les contraintes sont **exactes et concentrées** (égalités, intégralité,
arithmétique). Elle doit vérifier deux conditions :
- (i) chaque cas est réfuté en quelques minutes, par un solveur ou par un certificat ;
- (ii) le nombre de cas est au plus de l'ordre de 10^6.

La surcontrainte diffuse ne suffit pas : on l'a à −48 par droite, et elle ne se laisse pas exploiter.

### 5.2 Pistes, avec leur coût et le maillon qui manque

**(a) m = 2.**
- Toutes les droites ont c ≥ 2. Le lemme équitable fournit 60 égalités exactes par droite à c = 2 (facteur 10^−21 à
  10^−27, §4.2).
- Le recensement racine existe : 3,4 M survivants pour k ≥ 4, k ≤ 3 manquant.
- Maillon : réduire ces 3,4 M par une identité supplémentaire avant tout solveur. C'est la même méthode que le registre
  c3 (Gram entier), à mesurer sur un échantillon.
- Coût d'un échantillon de 1 000 : moins d'une heure à 1 fil.

**(b) m = 1, par le côté lointain.**
- Le projecteur lointain est de rang 8 : 7Π_T = 3I − R_T + J/12 − EᵀL_T⁺E (note du mandat de représentation,
  Théorème 1). C'est une contrainte exacte, mais elle ne porte sur R qu'**après** E.
- Test à faire : le système complet (G_T, E, R_T) devient-il décidable en 5 minutes sur un G_T aléatoire à c = 1 ?
- Même dans ce cas, le compte de 10^11 reste. Il faudrait regrouper les G_T, ce qui n'a pas de mécanisme connu.

**(c) m = 1, par un objet forcé par l'arithmétique plutôt que par le choix d'une droite.**
- C'est l'échelle des rangs de l'archive : à r = 37, 39, 41, un vecteur propre −4 entier de norme 18 ou 26 est forcé
  (NOTE 17.101, NOTE_COCLIQUE_FRAME §3).
- Ce sont des objets à contraintes exactes : le support à 18 est biparti 4-régulier (26 cœurs), et chaque sommet
  extérieur est équilibré.
- Maillon : l'archive bloque sur norme 18 sans hypothèse de rang (la positivité ne tue pas les sommets triples).

**(d) Certificat uniforme.**
- Il s'agirait d'une réfutation algébrique (Nullstellensatz, SOS) du système d'une droite, paramétrée par G_T.
- Risque connu : sur les CSP aléatoires à densité constante, SOS échoue aussi (Grigoriev, Schoenebeck).
- Le seul espoir est la structure spectrale propre à r = 3 (lemme 0.3). Ouvert (X).

### 5.3 Recommandation (risque assumé)

- **Tant que m = 1 n'a pas de méthode finie, la route finie ne mène pas à une preuve.** C'est la seule branche de coût
  non borné.
- Le choix de la droite minimale produit justement l'objet le plus diffus du problème : à c = 1, aucune identité exacte
  au-delà des marges (0.3). Il faut arrêter de chercher une réduction de m = 1 par le choix d'une droite.
- Pour m = 1, mettre l'effort sur un objet forcé arithmétiquement (piste (c)) ou sur un certificat uniforme (piste (d)).
  Ce sont des recherches, pas des calculs.
- Pas mesurables tout de suite :
  - (a), un échantillon de 1 000 gabarits c_min = 2 (1 h à 1 fil). Il chiffre la branche finie m = 2.
  - (b), un test de 5 minutes. Il dit si R_T rend une droite décidable.

---

## 6. Fichiers et reproduction

**Scripts.**
- `ll_test.py` : modèle CP-SAT et vérificateur exact. Modes `check`, `solve-real`, `random`, `randomc`, `blocks`,
  `planted`, option `--workers`.
- `ll_sat.py` : le même système en CNF (pysat). CaDiCaL tourne dans un processus fils tué à l'échéance (variable
  `LL_SOLVER`).
- `budget.py` : budget d'entropie. `c_dist.py` : profils de composantes d'un srg(243) réel.

**Journaux.**
- `check_243.log`, `c_dist_243.log`.
- `planted.log`, `planted_scaling.log`, `planted_sat.log`.
- `random_c1.log`, `random_c1_sat.log`, `blocks.log`, `budget.json`.

**Commande type.**
`py ll_test.py random 1 280 L123 --workers=12` ; `LL_SOLVER=cadical195 py ll_sat.py planted 1 270 12`.

Code personnel, non audité par un tiers. Les verdicts UNKNOWN ne sont pas des résultats mathématiques : ce sont des
mesures de dureté.
