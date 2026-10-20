# VERIF_C4_FERMETURE : la fermeture « minimum global c(L) ≥ 4 » et le bug OR-Tools 9.15

Vérification adverse en contexte neuf, faite le 20/10/2026. Lecture seule : dépôt `C:/home/researcher/cw/conway99-c1` (toutes
branches), clone `C:/home/researcher/Desktop/Recherche_Conway/c1-asymmetry-audit` et copie du pont `pont_codex/`.

Question : la fermeture de la branche c ≥ 4 (commit ecb50673, 18/10 14:36 UTC, pont:#1050) dépend-elle de verdicts calculés
avec le code fautif (OR-Tools 9.15 : `list(d) == [-2,3]` mais `d[-1] == 0` sur un champ répété du proto) ?

Toutes les heures sont en UTC. Les dates git sont en +0200 : on retranche 2 h.

## Verdict : SAINE, avec réserves

**Aucun maillon de la chaîne #1050 ne dépend d'une version fautive du code** (preuves aux §1 à §4).
- Dans le code commité, le seul code fautif est `code/codex/root_component_rotated_gram.py` avant ac8921c3. Ce module est né
  en 7da4d547, le 18/10 à 01:54:47. Les autres occurrences, hors chaîne, sont décrites au §1.3.
- Les 76 anciennes fermetures datent du 16/10 (19:48-22:05). Le front 0306 est figé en d93c1b0, le 18/10 à 01:05:34, 49 min
  avant la naissance du module. AWS v1 a tourné avec 5694bb5 (17/10, 23:16).
- Aucun de ces codes ne contient de lecture fautive. Les maillons postérieurs au correctif utilisent la version corrigée,
  avec le tampon `python_list_endpoints_v2`.

**Statut de la fermeture : S.** C'est un verdict CP-SAT sans certificat portable
(`c4_selected_root_closed.json` : `"portable_unsat_proof": false`, `"global_conway_exclusion": false`).

Réserves, qui ne relèvent pas du bug mais ne doivent pas se perdre :
1. **Pas de certificat.** Seuls ces éléments sont de statut C :
   - le certificat 3P + 4G ≤ 2772 (exact, revérifié par LAB, pont:#1020) ;
   - l'arithmétique de la chaîne (refaite ici, §5) ;
   - les 8 certificats linéaires rationnels parmi les 76 (statut déclaré `EXACT_LINEAR_LOWER_BOUND`, multiplicateurs
     rationnels ; non recalculés ici) ;
   - les DRAT des 19 retraits de Gram du gabarit 19 (pont:#1030, #1034).
2. **Verdicts antérieurs au correctif, non refaits.** La chaîne repose sur :
   - les 76 fermetures du 16/10 ;
   - 4 467 retraits de Gram du front 0306, venant de 87 sources. Parmi elles, 68 rapports AWS v1, et 3 pilotes locaux qui
     reprennent 97 verdicts de branche AWS v1.

   La règle 4 de `CONSIGNES_VERIF_ADVERSE.md` (« retiré sauf s'il a été refait ») les retirerait **par la date**. La présente
   archéologie établit qu'ils **ne passent pas par le code fautif**. Les requalifier en « S, non touché par le bug » est une
   décision à prendre et à consigner explicitement.
3. **Traçabilité.** Deux sources du front 0306 ne sont pas dans le dépôt public. Elles n'existent que dans le clone local de
   Codex (§2.4) :
   - `root_component_signature_pool_7_coupled3.json` (970 Gram de 7) ;
   - `root_component_signature_pool_corners0.json` (514 Gram de 19).
4. **#1009 contre #1011.** La consigne « ne pas réutiliser les sorties AWS v1 » vise, selon toute vraisemblance, la campagne
   **c3star v1** (§2.5). Codex ne l'a jamais écrit en toutes lettres. Sur le fond, la question est réglée : AWS 7/9/19 v1 ne
   pouvait pas utiliser le module.

---

## 1. Le bug, son correctif, le recensement des lectures `domain[...]`

### 1.1 Module fautif et correctif

- **Création.** `git log --all --follow -- code/codex/root_component_rotated_gram.py` donne 7da4d547 comme premier commit
  (18/10 01:54:47, « Diagnose pre-search stalls and add exact residual Gram and row-profile cuts »).
- **Lignes fautives** à 7da4d547 :
  - l. 49-50 : `da=model.proto.variables[a.index].domain` … `da[-1]`, `db[-1]` (bornes des produits) ;
  - l. 76-77 : `domain[-1]` (produits arête × valeur).
- **Correctif ac8921c3** (18/10 09:45:40) : conversion `list(...)` ; ajout de `PRODUCT_DOMAIN_ENCODING =
  'python_list_endpoints_v2'` et de `unsafe_product_reports()`. À ecb50673, les l. 54 et 83 lisent des listes Python.
- **Premières références au module** : `git grep rotated_gram` est vide à b41a4f1, d93c1b0 et 1f6bfd25. La première
  référence est à 7da4d547 (`root_component_local_branch.py:271-284`, `root_component_prism_residual.py:70-78`).
- **Agrégateurs c4 post-correctif.** Ils refusent les rapports sans tampon :
  - `root_component_global_matching_summary.py:67` ;
  - `root_component_selected_c4_summary.py:42` ;
  - `root_component_recovery_summary.py:35` ;
  - reprise interdite dans `root_component_local_branch.py:169-179` (état ecb50673).

### 1.2 Le recensement annoncé par Codex

`notes/CORRECTION_DOMAIN_ORTOOLS_2026_10_18.txt`, l. 32-34 (commit ac8921c3) :

> « Recherche des lectures .domain dans code/codex : les autres lectures de dernière borne concernaient déjà des listes
> Python, ou utilisaient explicitement l'indice positif 1. Aucun autre cas trouvé dans ce dossier. »

C'est une phrase, sans liste de fichiers. Sa portée est limitée à `code/codex` dans l'état du correctif, et aux seuls accès
`.domain`. Le scan AST de LAB (pont:#1010) porte sur 435 fichiers, lui aussi dans l'état courant ; il couvre aussi les
indices négatifs, `==`/`!=` et `reversed` sur tous les champs répétés. **Aucun des deux ne couvre l'historique.**

### 1.3 Mon recensement historique

Il s'agit d'un scan AST avec suivi de valeurs dans chaque fonction. Il signale tout indice négatif, toute tranche, toute
comparaison `==`/`!=` et tout `reversed` sur une valeur issue de `.proto` ou `Proto()`, avec une alerte heuristique sur tout
`domain[-k]`.

**Contrôle positif** : à 7da4d547, le scan trouve bien `da[-1]`, `db[-1]` (l. 50) et `domain[-1]` (l. 77).

| Code examiné | Résultat |
|---|---|
| 5694bb5 (runtime AWS v1), tout `code/` (805 fichiers) | aucune lecture fautive |
| clôture d'imports de `root_component_local_branch.py` à 5694bb5 | 24 modules, exactement les 24 `code_sha256` du métadata AWS v1 (`aws_7_9_19_20261018_v1.metadata.json`) ; seuls accès au proto : `len(...)` |
| 41d23bb9, d07ac4a8, b6a15767, 10b03e99, 21fbb74b (commits des 76 fermetures), tout `code/` | aucune lecture fautive |
| b41a4f1, d93c1b0 (front 0306 et pilotes locaux), `code/codex` | aucune lecture fautive ; clôture d93c1b0 de `local_branch`, `filtered_cover` et `campaign` = 29 modules, seuls des `len(...)` |
| **chaque** fichier .py modifié par **chaque** commit touchant `code/`, du 15/10 00:00 au correctif (149 commits, 628 couples) | seules lectures fautives : `root_component_rotated_gram.py:50` et `:77`, de 7da4d547 à 50494050 |
| ecb50673 | le module lit des listes |

Les autres signalements sont sans danger :
- `root_component_domain_regression.py:43` est le test de régression lui-même ;
- `conway_linear_explanation.py:23/86` lit `list(map(int, …domain))` dès sa naissance (ca3dab5a, 16/10 10:21) ;
- `root_component_boundary_sat.py:104` porte sur une liste Python (`Encoder.clauses = []`) ;
- `coclique_partition_verify.py` utilise `cp_model_pb2` (protobuf pur), hors c4 ;
- 4 erreurs d'analyse concernent du code LAB, hors chaîne c4.

**Occurrences antérieures du même piège** (hors chaîne c4) :
- `root_component_signature_benders.py`, le 17/10. Un essai non commité a lu `domain[-1]` sur [0,7] ; il a été déclaré
  « inutilisable » et corrigé avant le commit c7e2daaa (`notes/MOMENTS_SIGNATURES_C1_2026_10_16.txt` l. 634-635). Aucune
  source de la chaîne ne vient de ce script.
- `gram_free_moment.py` de LAB, le 18/10 à 16:25 (pont:#1076). L'occurrence est postérieure à la fermeture ; ses verdicts, y
  compris les « c4 9 et 19 en local » de LAB, n'ont jamais été comptés.

---

## 2. Le front 0306 reprend-il AWS v1 ou d'autres verdicts d'avant le correctif ?

### 2.1 Oui : il retire des Gram sur la foi d'AWS v1

`root_component_gram_filtered_20261018_0306.json`, commité en d93c1b0, porte le champ `excluded_gram_sources`. On y lit
quel rapport a retiré chaque orbite de Gram.

| Gabarit | Orbites de Gram source | Retirées | Restantes | Dont retirées par `aws_v1_*` |
|---|---|---|---|---|
| 7 | 1 851 | 1 402 | 449 | 5 (1244, 1377, 1479, 1529, 1530) |
| 9 | 240 | 228 | 12 | 4 (183, 233, 234, 236) |
| 19 | 3 285 | 2 837 | 448 | 59 |
| **total** | | **4 467** | **909** | **68** |

- Les **87 sources** distinctes de 7, 9 et 19 se décomposent en 68 rapports AWS v1 et 19 autres. C'est exactement le compte
  « 87 sources » de #1011.
- L'écart entre le snapshot 0110 (entrée d'AWS v1 : 456/16/508) et 0306 se compose de ces 68 retraits et des 3 pilotes
  locaux 7#1245, 7#1307 et 19#837.
- **Ces 3 pilotes réutilisent AWS v1** : 75/77, 7/10 et 15/16 de leurs branches INFEASIBLE ont pour `source` le rapport
  `aws_v1_*` du même Gram. Au total, **71 Gram du front dépendent d'AWS v1** : 68 en entier, 3 en partie (97 verdicts de
  branche sur 103).
- **Les rapports AWS v1 sont importés tels quels.** Le JSON de `aws_v1_9_183` est identique entre e441413 (dépôt de LAB) et
  d93c1b0 : simple re-sérialisation. Les 68 rapports sont tous INFEASIBLE, avec `all_component_branches_processed = true`
  et aucune métadonnée de produits.

### 2.2 Mais aucune de ces sources ne passe par le code fautif

- **Dates.** Toutes les sources commitées le sont au plus tard en d93c1b0 (01:05:34). Les 2 sources non commitées datent du
  16/10, vers 22:21 et 22:37 (§2.4). Le module fautif naît à 01:54:47.
- **Code d'AWS v1.**
  - Les 28 empreintes du métadata (24 fichiers de code, 4 entrées) coïncident avec les blobs de 5694bb5 et 315ed4e, que j'ai
    recalculés en LF.
  - LAB les avait vérifiées sur les machines (pont:#978).
  - Ce code est propre (§1.3). Les bornes de produits de `root_component_projector.py:52-61` viennent d'intervalles Python.
- **Règle même de l'agrégateur**, `unsafe_product_reports` recopiée telle quelle depuis ac8921c3 :
  - sur les 95 sources du 0306 (20 gabarits), à d93c1b0 comme sur origin/main : **0 signalée**, et aucun marqueur
    (`integer_gram`, « Necessary integer Gram », `edge_integer_products`) ;
  - **contrôle positif** sur le snapshot 0421 (e4c8aa39) : **19 sources signalées**, exactement les 7 Gram de 7 et les
    12 Gram de 9 que #1011 déclare retirés par les produits fautifs.
- **Les 3 pilotes locaux** ont tourné avec `rotated_residuals` et `rotated_templates` (bornes constantes `(-4,7)`, `(0,49)`,
  `(-cap,cap)` dans `root_component_rotated_residual.py` et `root_component_rotated_templates.py` à d93c1b0), sans
  `rotated_gram`.

### 2.3 Les tables gelées

- **`root_component_low_budget_frontier_d93c1b0.json`** a été créée en 1f6bfd25 (01:19) par
  `root_component_low_budget_transport.py`.
  - Son `source_sha256_lf` pour `root_component_cover79.json` (2ad430f7…) est celui du registre à 21fbb74b, 5694bb5 et
    d93c1b0 : 76 EXCLUDED, 3 OPEN.
  - Ce n'est pas celui des états fautifs e4c8aa39 (77/79) et 311152b6 (79/79).
- **`root_component_low_budget_row_profiles_0306_d93c1b0.json`** est née **dans le même commit que le module fautif**
  (7da4d547), via `root_component_rotated_gram_profiles.py`. Le « antérieures au bug » de #1009 est donc inexact pour ce
  fichier. Son contenu est pourtant sain :
  - sa source déclarée est le 0306 (sha df2225fb…) ;
  - je l'ai **recalculée indépendamment** à partir des 909 Gram du 0306, avec R = L·A·Lᵀ en fractions exactes et le profil
    trié 2048·R_ii + Σ_j R_ij² ;
  - résultat : **909/909 profils identiques, 907 distincts**. C'est une fonction pure du front 0306.

### 2.4 Deux sources non commitées

`find` sur `c1-asymmetry-audit/data/codex_line_resonance_20261016/` donne :

| Fichier | Taille | Date locale | Options | Rôle |
|---|---|---|---|---|
| `root_component_signature_pool_7_coupled3.json` | 198 801 o | 17/10 00:21 | `layer 3, eigen` | retire 970 Gram de 7 |
| `root_component_signature_pool_corners0.json` | 2 080 762 o | 17/10 00:37 | `layer 0` | retire 514 Gram de 19 |

- Les dates locales correspondent au 16/10 vers 22:21 et 22:37 UTC.
- Ces deux fichiers sont cités par les snapshots depuis ed242eaf (16/10 22:55).
- Règle de l'agrégateur : 0 signalement, aucun marqueur.
- Ils sont absents de tout arbre git (`git log --all` vide). La provenance est vérifiable, mais pas reproductible depuis le
  dépôt public.

### 2.5 La contradiction #1009 / #1011

#1009 dit : « Ne pas réutiliser les sorties AWS v1 comme exclusions ». Pourtant le front 0306, déclaré valide en #1011, compte
68 INF d'AWS v1. Lecture la plus probable : « AWS v1 » désigne ici **c3star v1**.
- Cette campagne utilisait les préfixes S3 `c3star-v1a/b` (pont:#1004) et le code 2c7bdd0b, qui **importe** le module fautif
  (`root_component_complete_star.py:147`).
- #1008 demande d'arrêter c3star, et #1010 (LAB) en accuse réception : « aucune de ces sorties ne sera comptée ».
- La note officielle du correctif (`CORRECTION_DOMAIN_ORTOOLS…`, l. 30-31) ne retire que « la campagne AWS c3star fondée sur
  2c7bdd0b ». Elle ne dit rien d'AWS 7/9/19 v1. Ses l. 68-78 (ajoutées en 8ce2e720 ; numéros dans l'état ecb50673) valident
  le 0306 et ses 87 sources.

Quelle que soit la lecture retenue, les faits du §2.2 tiennent : le runtime 5694bb5 ne pouvait pas déclencher le bug.

---

## 3. Les 76 anciennes fermetures

**Dates.** Historique de `root_component_cover79.json` :

| Commit | Date (16/10, UTC) | EXCLUDED |
|---|---|---|
| 72d47c35 | 19:48 | 0 |
| 41d23bb9 | 20:11 | 59 |
| d07ac4a8 | 20:28 | 64 |
| b6a15767 | 21:17 | 74 |
| 10b03e99 | 21:44 | 75 |
| 21fbb74b | 22:05 | 76 |

- Les 76 enregistrements sont **identiques** de 21fbb74b à ecb50673 ; seuls 7, 9 et 19 ont changé.
- La frontière d93c1b0 gèle exactement cet état (§2.3).

**Méthodes** :

| Méthode | Fermetures |
|---|---|
| CP_SAT_RELAXATION | 54 |
| COMPLETE_GRAM_SIGNATURE_COVER | 12 |
| RATIONAL_LINEAR_CERTIFICATE (`root_component_prism_dual.json`, 41d23bb9 : statut `EXACT_LINEAR_LOWER_BOUND`, borne 56 > 51, identité de preuve avec multiplicateurs rationnels ; non recalculés ici) | 8 |
| CP_SAT_FULL | 2 |

`portable_unsat_proof` vaut `false` pour les 76.

**Sources.**
- Les 48 fichiers `.json` cités dans les 76 enregistrements sont tous présents à 21fbb74b.
- Ils ont été commités pour la première fois le 16/10, entre 19 h et 22 h environ.
- 0 signalement par la règle de l'agrégateur, aucun marqueur.

**Code.** Propre aux 5 commits concernés (§1.3).

**Portée.** Plusieurs exclusions utilisent c ≥ 4 sur des droites non racines (pont:#971). Elles valent donc sous l'hypothèse
globale de la branche, mais ne sont pas transportables à c ≤ 3 (pont:#998).

Ces 76 fermetures n'ont **jamais été revérifiées indépendamment** ; Codex le dit lui-même en #1023.

---

## 4. Les fermetures postérieures au correctif utilisent-elles le front 0306 ?

| Gabarit | Rapport (commit, heure) | Entrées | Le 0306 entre-t-il ? |
|---|---|---|---|
| 7 | `c4_selected_root_closed.json` → `seven_exclusion` | g = 12, s ≥ 48, donc score ≥ 528 > 504 ; borne 45 < 48 | **non** (arithmétique et données du gabarit) |
| 9 | `c4_9_all_variable_base.json` (7b6642f3, 14:15), INF en 264,98 s | couverture `selected_weighted_gram_cover.json` (12 Gram), dont `source_gram_cover` = 0306 (df2225fb…) ; `--no-transport` | **oui** (couverture). La frontière et les profils sont lus et contrôlés par empreinte, mais `rotation.transport = false` |
| 19 | m0 (8541c695, 11:47), m1-3 (cd22fdaf, 13:11), m4 (ecb50673, 14:36), puis flips {0},{1,2},{3,6},{4,5,7,8} | 429 Gram = les 448 du 0306 moins 19 retirés par projection pondérée (`weighted_projection_19_complete.json`, source 0306, DRAT d'après #1030) ; couverture factorisée de même source ; transport **actif** | **oui, deux fois** : couverture, et profils transportés (`profiles.roots[0].allowed_profiles = 907`, issus des 909 Gram, gabarit 7 compris). Dépend aussi des 76 via la frontière transportée, appliquée sous condition s ≤ 51 à la nouvelle racine |

Contrôles complémentaires :
- Les tampons `python_list_endpoints_v2` sont présents dans les 3 rapports de 19 (2, 8 et 2). Le rapport de 9 n'a aucun
  produit tamponnable. 0 signalement de l'agrégateur sur les 4 rapports.
- Empreintes de frontière, de profils et de couverture vérifiées dans les 4 rapports ; la couverture factorisée de m4 l'a été
  aussi.
- Le snapshot 0421, contaminé, n'apparaît dans aucun d'eux.
- Pas de circularité : la frontière et les profils sont gelés en d93c1b0 et 7da4d547, avant les preuves de racine pondérée
  (à partir de 8d45031f, 11:21).

---

## 5. La chaîne réécrite, maillon par maillon

| # | Maillon | Source exacte | Statut | Bug |
|---|---|---|---|---|
| 1 | 3P + 4G ≤ 2772 (12 comptes d'ordre 9 à poids positifs : 924 − P − (4/3)G ≥ 0) | `data/codex_domain_recovery_20261018/c4_prism_grid_bound.json`, `weighted_root_certificate.json` (8d45031f) ; vérifié par LAB sur census2 (pont:#1020) | C | sans objet |
| 2 | Σ_x (9s + 8g) = 18(3P + 4G) ≤ 99·504, donc la racine x qui minimise le score vérifie 9s + 8g ≤ 504 | idem ; recalculé ici : 18·2772 = 49 896 = 99·504 | C | sans objet |
| 3 | sous c ≥ 4 : au plus 14 non-grilles, donc g ≥ 7, donc s ≤ ⌊448/9⌋ = 49 ≤ 51 | pont:#1017, #1018 ; recalculé | C | sans objet |
| 4 | couverture des 79 gabarits pour toute racine de budget ≤ 51 | `root_component_templates.json` (72d47c35, 16/10) : 2^21 masques énumérés, filtres d'algèbre linéaire, 200 gabarits à permutation près | énumération exacte, pas CP-SAT ; non revérifiée indépendamment | code propre |
| 5 | 76 gabarits exclus à toute racine de budget ≤ 51 | `root_component_cover79.json` @21fbb74b ; gelé dans `…frontier_d93c1b0.json` | S (8 en C déclaré, non recalculé) | **sain** (§3) |
| 6 | gabarit 7 exclu à la racine choisie : 9·48 + 8·12 = 528 > 504 | `c4_selected_root_closed.json` | C | sans objet |
| 7 | front des Gram de 9 et 19 à budget ≤ 51 : 12 et 448 Gram | `root_component_gram_filtered_20261018_0306.json` @d93c1b0, 87 sources (68 AWS v1) | S | **sain** (§2) |
| 8 | 19 Gram de 19 retirés sous 9s + 8g ≤ 504 | `weighted_projection_19_complete.json` + DRAT (`proof19_checked.tar.gz`, cd22fdaf) | C si les CNF sont fidèles, sinon S | post-correctif |
| 9 | gabarit 9 : INF, tous Gram et couplages libres, sans transport | `c4_9_all_variable_base.json` (7b6642f3) | S | post-correctif |
| 10 | gabarit 19 : 9/9 couplages INF, 429 Gram libres, transport des maillons 5 et 7 | `c4_19_matching_summary_closed.json` (ecb50673) | S | post-correctif, v2 |
| ⇒ | tout srg(99,14,1,2) a une droite L avec c(L) ≤ 3 | `c4_selected_root_closed.json` | **S** | **sain** |

Le statut de l'ensemble est celui du maillon le plus faible : **S**.

**Autre entrée de la chaîne : P ≤ 852.** LAB note en #1012 que la couverture c4 dépend de P ≤ 852 (« m ≥ 9 et coupes 51 »).
P ≤ 852 est un certificat exact, vérifié par LAB avec un census re-dérivé indépendamment (pont:#1016, #1020) : statut C.
Je ne l'ai pas re-vérifié ici, car il est hors de la question du bug.

---

## 6. Ce qui reste à faire, et le coût d'un recalcul

**Si l'on applique la règle 4 à la lettre**, c'est-à-dire si l'on refait tout verdict CP-SAT antérieur au correctif, il faut
relancer les maillons 5 et 7. Le maillon 4 est une énumération exacte, hors du champ de la règle. Ordre de grandeur, d'après
le CPU enregistré dans les rapports (construction des modèles non comptée) :

| Élément à refaire | CPU estimé |
|---|---|
| 68 Gram AWS v1 | ≈ 39 800 s de solveur, soit ≈ 11 h·CPU |
| 3 pilotes locaux | ≈ 0,5 h, plus les 97 branches AWS reprises |
| 16 rapports anciens | ≈ 2 h |
| 76 fermetures (non mesuré ici) | quelques h·CPU |
| **total** | **≈ 15 à 30 h·cœur** |

Cela reste faisable sur le PC à 1 cœur en 1 à 2 jours, mais on ne ferait que **reproduire des verdicts S**.

**Variante ciblée, moins chère**, pour retirer la seule dépendance à AWS v1 et aux 3 pilotes :
1. repartir du snapshot 0110 (980 Gram, antérieur à l'import AWS) ;
2. relancer les modèles post-correctif de 9 (16 Gram au lieu de 12) et de 19 (passage par le filtre de projection pondérée
   avant la couverture) ;
3. régénérer les profils depuis 0110.

Estimation : ≈ 1 à 5 h·CPU, avec une forte incertitude. Une couverture plus grande peut rester UNKNOWN.

**Pour une preuve complète**, il manquerait :
1. des certificats portables (DRAT ou VeriPB) pour les 68 fermetures CP-SAT parmi les 76, pour les 4 467 retraits du
   front 0306, et pour les modèles finaux de 9 et 19 ;
2. une re-dérivation indépendante de la couverture des 79 gabarits et de l'énumération des Gram
   (`root_component_gram_budget51.json`) ;
3. l'archivage public de `pool_7_coupled3.json` et de `pool_corners0.json` ;
4. une phrase explicite de Codex sur le statut d'AWS 7/9/19 v1 après le correctif, pour lever l'ambiguïté de #1009.

---

## 7. Redécouverte et reproductibilité

**Antériorité.**
- Codex avait affirmé la validité du 0306 (#1011 ; `CORRECTION_DOMAIN_ORTOOLS…`, l. 68-78), sans détailler le contenu des
  87 sources.
- La fiche `fiches/L11f_pont.md` (l. 27, 255, 324, 442) signale la contradiction comme « non résolue ».
- Je n'ai trouvé aucune vérification source par source antérieure dans `fiches/`, `assemblage/` ou le dépôt.

**Commandes clés, à relancer en lecture seule.**
- `git -C C:/home/researcher/cw/conway99-c1 log --all --follow --format='%h %ci' -- code/codex/root_component_rotated_gram.py`
  : naissance du module en 7da4d547.
- `git grep -n rotated_gram d93c1b0 -- code/` : résultat vide.
- `git show 315ed4e:data/codex_line_resonance_20261016/aws_7_9_19_20261018_v1.metadata.json` : `code_commit` 5694bb5,
  24 fichiers de code.
- `git show d93c1b0:data/codex_line_resonance_20261016/root_component_gram_filtered_20261018_0306.json` : champ
  `excluded_gram_sources`.
- `git show ecb50673:data/codex_domain_recovery_20261018/selected_weighted_gram_cover.json` : `source_gram_cover` = 0306.

**Scripts de lecture utilisés.** Ils ont tourné en un seul processus, moins de 5 min chacun, et sont restés dans le
scratchpad de session, hors dépôt : `scan_proto_neg.py`, `scan_window.py`, `import_closure.py`, `unsafe_check.py`,
`snap_sources.py`, `closures76.py`, `sha_checks.py`, `recompute_profiles.py`, `closure_reports.py`, `cpu_cost.py`. Leur
logique est décrite aux §1.3, §2 et §4.
