# Fusion des routes finies : obligation 7-adique des droites, réduction par droites, lois à quatre étoiles

*19-20/10/2026, LAB. Demande de l'utilisateur : « des arguments combinatoires, qui combinent les routes "finies" de C1
pour les fusionner. Tu ne parles même plus de H-MATCH et de tous ces théorèmes non prouvés qui menaient à l'exclusion
que t'avais trouvée. » Puis, sur la route des rangs : « la route 37 à 43 était ultra dure de surface, après avec les
outils qu'on a aujourd'hui, qui sait ».*

**Statuts.**
- **P** : preuve écrite ici, ou vérification exacte d'une identité d'algèbre linéaire.
- **E** : expérience de solveur. Le verdict REFUTED est exact pour l'instance donnée, mais sans certificat exporté, et
  le code n'a pas été relu par un tiers.
- **A** : déjà dans l'archive (référence donnée).
- **X** : ouvert.

**Fichiers** : `work/exploration_2026-10-16/merge_2026-10-19/`.
- `oblr_prep.py` (préparation), `oblr.cpp` et `oblr2.cpp` (moteurs).
- Lots `run_r37_batch.sh`, `run_r37_torsion.sh`.
- Journaux `r37_batch.jsonl`, `r37_torsion.jsonl`, `r37_torsion_oblr2.jsonl`.
- Contrôles d'algèbre linéaire `omega_check.py` (forme de Green) et `schur_check.py` (formule de rang).
- Contrôles dans `../treasure_2026-10-19/` (`obl37*`, `rank7_line.py`).

---

## 0. Résultats, en premier

**(R1) Au rang 37, toutes les droites testées de type c ≤ 2 sont réfutées par l'obligation de droite (E).**
- Il s'agit de G_T aléatoires. Chaque ligne du tableau couvre toutes les formes non dégénérées possibles du résidu.
- « Profil » = tailles des composantes de G_T.

| type de droite (c, d) | profil | résidu imposé au rang 37 | réfutées | temps par instance |
|---|---|---|---|---|
| (1, 1), connexe générique | 36 | rang 0 | 5/5 (graines 1 à 5) | 0,8 à 1,8 s |
| (1, 2), connexe à 7-torsion | 36 | équilibrée, rang 1 (forcé, §1.4) | 8/8 (4 graines × 2 formes) | 0,3 à 0,7 s |
| (2, 2) | 18+18, 12+24, 6+30 | rang 1 | 18/18 (3 graines × 3 profils × 2 formes) | 3,8 à 106 s |
| (2, 3), 7-torsion dans une composante, équilibrée | mêmes profils | rang 2 | 18/18 (3 graines × 3 profils × 2 formes) | 0 à 23 s ; 12 sur 18 dès la racine, par L1 |
| (2, 3), déséquilibrée | mêmes profils | nul sur b^⊥, soit b cᵀ + c bᵀ | 9/9 (3 graines × 3 profils) | 5 à 164 s ; 2 cas 6+30 réfutés par `oblr2` |

**Total : 58 instances aléatoires, 58 réfutées.**

**(R2) La droite c = 2 est le morceau qui manquait à la chaîne de septembre.**
- La chaîne de septembre pour k = 22 (A : NOTE 17.52, notes 124 à 127 de Codex) se terminait par : « toute droite
  déconnectée, à exclure localement (ouvert) ».
- Sous les hypothèses P = S = 0, il restait des droites de profil (6,6), soit deux composantes de 18 sommets (A : TH
  17.53).
- Le tableau ci-dessus les réfute toutes, dans les instances tirées, et les autres profils c = 2 aussi.
- Pour d = 2, l'hypothèse (NT) de septembre n'est plus nécessaire au rang 37. L'identité force l'équilibre, et le cas
  équilibré meurt.

**(R3) La droite c = 1 générique au rang 37 est une redécouverte (A).**
- Codex et Astra, en septembre : « étoile complète morte 42/42 » (dépôt conway99-structures-lab, cité en TH 17.52).
- Ce qui est nouveau ici :
  - un moteur indépendant, en C++ ;
  - un contrôle croisé en Python : même nombre de nœuds, 193 200 à la graine 1 ;
  - des contraintes exactes supplémentaires : λ/μ entre lointains, comptes proche–lointain ER = 2J − E − GE, marges en
    propagation. Avec elles, la réfutation tombe à environ 10⁴ nœuds et à la profondeur 3.

**(R4) Au rang 39, résidu de rang 2 sur une droite c = 1 : le moteur ne conclut pas (E, résultat négatif).**
- Graine 1, deux formes : arrêt à 240 s, environ 330 000 nœuds, profondeur 5.
- Avec `oblr2` : arrêt à 270 s, 437 760 nœuds, profondeur 4.
- Le rang 2 libère environ 2·60 − 1 = 119 paramètres mod 7. L'obligation devient diffuse, comme le système proche–lointain
  sans rang (NOTE_REDUCTION 0.1).

**(R5) Trois formes exactes de l'obligation (P).**
- **Forme de Green.** Pour une droite générique, la valeur forcée vaut R(w,w') ≡ 4 − e_wᵀ Ω e_w' (w ≠ w'), avec
  Ω = (3I − G_T + J)⁻¹ mod 7 et e_wᵀΩe_w ≡ 0.
  - C'est la fonction de Green, mod 7, du graphe cubique G_T.
  - Contrôle : 0 écart sur 6 000 tests contre l'inverse généralisé du code.
  - C'est la forme de Codex, « A_F = 3I + 3J − NᵀL⁺N », avec L⁺ = Ω − J.
- **Sens combinatoire de ρ.** ρ(T) = dim (Im(A − 3I) ∩ {vecteurs nuls sur N[T]}) mod 7 : le résidu compte les vecteurs
  (A − 3I)x qui s'annulent sur la boule de la droite.
- **Formule de rang avec noyau déséquilibré.**
  rang M = rang M_NN + 2·dim(M_FN ker M_NN) + rang(résidu restreint à l'orthogonal).
  - Vérifiée sur 300 matrices symétriques aléatoires de F₇ (`schur_check.py`, 0 écart).
  - Elle donne l'identité de Codex : 14 + k = (37 − d) + 2r(T) + ρ.

---

## 1. L'identité et ses conséquences

### 1.1 Énoncé

Notations :
- M = A − 3I mod 7, et r = rang₇ M.
- N = N[T] (39 sommets), F = les 60 lointains.
- d = dim ker₇(3I − G_T) ≥ c(T).
  - d = 1 équivaut à 7 ∤ τ(G_T), le nombre d'arbres couvrants.
  - d − c est le 7-rang du groupe de Jacobi (« sandpile ») des composantes.

**Identité (A : Codex ; P : rederivée ici).**
- r = (38 − d) + 2 r(T) + ρ(T), où r(T) = dim M_FN(ker M_NN) est la partie déséquilibrée.
- rang M_NN = 38 − d. Le noyau contient deux vecteurs propres de droite (−4 e_t + 1_{C_t}, combinaisons de somme nulle),
  toujours tués par M_FN.
- Il contient aussi un vecteur de composante par composante supplémentaire, tué par M_FN grâce au lemme équitable L4.
- Enfin il contient les vecteurs de 7-torsion, qui peuvent être déséquilibrés.

### 1.2 Fenêtre

**(A)** r ∈ {37, 39, 41, 43} : r ≤ 35 est exclu (TH 15 à 17.10).

### 1.3 Ce que l'identité force pour chaque droite (P)

- 2 r(T) + ρ(T) = r − 38 + d.
- c = 1 générique : ρ = r − 37 ∈ {0, 2, 4, 6}.
- c = 2 avec d = 2 : ρ = r − 36 ∈ {1, 3, 5, 7}.

### 1.4 Au rang 37 (P)

On a 2r(T) + ρ(T) = d(T) − 1 pour toute droite.

**c = 1 :**
- d = 1 : ρ = 0. Le graphe lointain est entièrement forcé mod 7.
- d = 2 : r(T) = 0, car 2 > 1. La droite est donc **équilibrée**, et ρ = 1.
- d = 3 : (r, ρ) = (0, 2) ou (1, 0). Rare : environ 0,05 % des G_T (heuristique de Cohen–Lenstra), non testé.

**c = 2 :**
- d = 2 : ρ = 1.
- d = 3 : (0, 2) ou (1, 0). Pas rare : environ 27 % des G_T à c = 2.
  - Le cas déséquilibré (1, 0) se met sous la forme R − 3I ≡ EᵀXE + b cᵀ + c bᵀ, avec b_w = e_w·κ (κ la direction de
    torsion) et c ∈ F₇⁶⁰ inconnu.
  - Le moteur l'encode comme une forme hyperbolique, u = (b + c, b − c) et D = diag(4, 3), sans symétrie.

**c ≥ 3 :** ρ ≥ 2. Ces droites relèvent du registre c ≥ 3.

---

## 2. Le moteur `oblr` (E)

**Un lointain** est un couple (triplet de noms, u ∈ F₇^ρ).

**Filtres de préparation :**
- L2 ;
- L4 si c ≥ 2 ;
- orthogonalité au noyau proche : équilibre, ou décomposition déséquilibrée ;
- diagonale : uᵀDu = −3 − β(w,w).

**Recherche** (plus petit domaine d'abord, propagation) :
- R(w,w') = β(w,w') + u_wᵀDu_w' doit valoir 0 ou 1 ;
- paires q et s distinctes ;
- au plus 2 noms partagés (L3), au plus 1 si les deux lointains sont adjacents (λ) ;
- marges K, avec égalité à la fin (L1) ;
- degré lointain 8 ;
- comptes proche–lointain ≤ 2 − [x ∈ w] − |N_G(x) ∩ w|, avec égalité à la fin ;
- voisins lointains communs ≤ (1 si adjacents, sinon 2) − noms partagés, avec égalité à la fin.

**Symétrie** : tant que tous les u affectés sont nuls, on n'essaie qu'un représentant par orbite de O(D). C'est valide car
l'ensemble des solutions est stable par O(D).

**Variante `oblr2.cpp`** : après chaque affectation, chaque candidat ouvert est revérifié contre l'état entier (degrés,
comptes proche–lointain, voisins communs, marges).
- Mêmes verdicts que `oblr` sur les instances comparées.
- 1,6 à 6 fois moins de nœuds, et une profondeur réduite de 1.
- Elle a réfuté les deux cas déséquilibrés 6+30 (graines 1 et 2) qui dépassaient 200 s avec `oblr`.

**Contrôles :**
- même G_T que `obl37` pour une même graine ;
- ρ = 0 : mêmes candidats (325 à 413 par paire p à la graine 1) et réfutation retrouvée ;
- valeurs forcées identiques à la forme de Green ;
- formule de rang vérifiée.

**Aucun contrôle positif n'est possible aux paramètres de Conway**, faute d'instance satisfaisable connue. Le risque
résiduel est un sur-élagage par un bogue. Il est réduit, sans être annulé, par :
- les deux implantations indépendantes au rang 0 ;
- le fait que toutes les contraintes sont des conséquences exactes du srg, chacune démontrée en une ligne.

**Les cas « refusés à la racine » du lot torsion ne sont pas des artefacts.**
- Profil 18+18, cas équilibré : trois paires p n'ont plus aucun triplet sans paire croisée de multiplicité K = 0. C'est
  vérifié séparément, en Python, sur le fichier binaire.
- La droite meurt donc par L1, avant toute question de rang.
- Pour le profil 12+24 équilibré, des paires p n'ont aucun candidat.

---

## 3. La fusion au rang 37 : où en est la chaîne

| maillon | énoncé | statut |
|---|---|---|
| 1 | droites c = 1 génériques impossibles au rang 37 ((a′) de septembre) | E : 5 + 42 (A) instances ; pas d'argument uniforme (X) |
| 2 | droites c = 1 à 7-torsion d = 2 : équilibrées (P), puis impossibles | E : 8/8 ; remplace (NT) pour d = 2 |
| 3 | droites c = 2 (d = 2, et d = 3 dans ses deux variantes) impossibles | E : 18/18 + 27/27 |
| 4 | m ≥ 3 (toutes les droites c ≥ 3) exclu | registre c3 : P3 en cours, 5 bords ouverts (§6) |
| 5 | types rares : c ≤ 2 avec d ≥ c + 2, et c = 1 avec d = 3 | X, non testé |

**Énoncé conditionnel.** Si les maillons 1, 2, 3 et 5 valent pour **tous** les G_T, et si P3 se ferme, alors aucun graphe
de Conway n'a r = 37.
- Raison : au rang 37, toute droite aurait c ≥ 3, et le registre exclut m ≥ 3.
- Le comptage des grilles n'intervient pas : c'est l'idée de 17.52, sans borne.

**Le maillon manquant est l'uniformité, et il est chiffré.**
- Classes de G_T à c = 1 : environ 10^11,2 (NOTE_REDUCTION §1).
- Classes à c = 2 : environ 10^9 à 10^10, estimation de ce soir, par composante : (k!)³ divisé par les symétries.
- Au coût observé (environ 1 s à c = 1, 4 à 100 s à c = 2), la vérification exhaustive coûterait des milliers
  d'années-CPU. **Elle est hors de portée.**
- Il faut donc un argument uniforme sur la fonction de Green mod 7 des graphes cubiques de ce type. Aucun n'est connu.
- L'obstruction observée ressemble à celle d'un CSP aléatoire. À ρ = 0 :
  - environ 360 candidats par paire p ;
  - une densité de paires compatibles d'environ 2/7 ;
  - une mort à la profondeur 3 ou 4.

  C'est exactement ce qu'on attend d'un système pseudo-aléatoire, pas d'une structure lisible. Astra l'avait vu : « the
  obstruction is in the 0/1 form of the shadows ».

---

## 4. Les énoncés conditionnels de l'archive, relus avec l'obligation de droite

La carte complète, avec citations, est le rapport d'exploration du 19/10 au soir. En voici l'essentiel.

### 4.1 Le lien exact entre le rang F₇ d'un bloc à quatre étoiles et le résidu de droite (P)

Données :
- v un sommet ;
- l = {v, t₁, t₂} et m = {v, x, x'} deux droites par v ;
- S = L_l ∪ L_m les 44 labels.

La boule à 59 sommets de (E2) (EXP 16/10) est exactement N[l] ∪ F_m, où F_m = W_x ∪ W_x' est formé des 20 lointains de l
adjacents à x ou x'. Pour l équilibrée :

    rang_F₇(8 T_S) = (23 − d(l)) + rang₇ Res_l[F_m, F_m],     et le bloc L_l seul a le rang 23 − d(l).

Conséquences :
- **(K22)** (« ν ≥ 14 ⟹ rang_F₇ ≥ 23 », qui exclurait r = 37) équivaut, aux paires dont une droite est c = 1 générique,
  à : « la double étoile complète W_x ∪ W_x' ne satisfait pas la construction forcée ». (K22) découle donc, pour ces
  paires, de (a′), que Astra a testé 42/42.
- Les blocs sans grille de nos données (rang_F₇ ≥ 30, EXP 16/10) demanderaient rang Res_l[F_m] ≥ 8 > r − 37. **Ils sont
  impossibles à tous les rangs de la fenêtre.**
  - Les indices réunis pour H-MATCH, N9-NG, Q7 et R7-NG viennent donc de structures qui ne peuvent pas apparaître dans
    un graphe de Conway. C'était déjà noté sous une autre forme (THREE_RESULTS §5, EXP 16/10).
  - Ce qui est nouveau, c'est la raison : l'étoile de l porte déjà le rang 22, et les labels de m n'ajoutent au plus que
    ρ ≤ 6.
- **Les lois à quatre étoiles contiennent G_l en entier.** Les 24 labels de L_l portent les appariements M_t₁ et M_t₂ et la
  bijection entre classes. Elles sont donc aussi globales que la droite : leur univers à c = 1 est le même, environ 10^11
  classes.

### 4.2 (H-MATCH)

**Fait (P).** Une paire (l, m) en grille donne une composante prisme de G_l. Une droite avec c(l) = 1 n'est donc dans
aucune grille.
- HMR §2 : une paire de E_H (les deux moitiés de (H-MATCH) valent) dont les deux droites ont un E_H-degré ≥ 3 est une
  grille. Toute paire de E_H contenant une droite c = 1 a donc une extrémité de E_H-degré ≤ 2.
- (H-MATCH) aux 21 paires de v donnerait des degrés 6 partout : aucune droite par v n'aurait c = 1.
- Correction faite en rédigeant : la seule moitié l ne suffit pas. Elle force seulement l'envoi de la paire {y, y'} sur
  des paires partenaires de C₁ et de C₂, et la composante peut continuer par s₁₂.

**Au rang 37, (H-MATCH) n'est pas nécessaire.** Les droites c ≤ 2 meurent par l'obligation (E), et m ≥ 3 relève du
registre.

**Aux rangs 39 à 43**, les lois (H-MATCH), (B′) et (N9-NG) reprennent du sens comme outils pour les droites c ≤ 2. Elles
restent ouvertes (A).

### 4.3 (B′) + (C)

- (C) dit « toute Conway a une droite non spéciale », c'est-à-dire m = 1.
- **C'est exactement ce que donne la réduction par droites quand m ≥ 2 est fermé** : m = 4 est fermé, m = 3 est en voie
  de l'être (P3), m = 2 reste ouvert, soit 3,4 M gabarits racine.
- **(B′) + [m ≥ 2 exclu] ⟹ pas de Conway** (P : il suffit de composer les deux énoncés).
- Au rang 37, le maillon m = 2 devient l'obligation c = 2 de §3, qui meurt (E).

### 4.4 (NT) et (a′)

- (NT) (« une 7-torsion d'un G(L) connexe n'est jamais équilibrée ») n'est plus utile au rang 37 pour d = 2. L'identité
  impose l'équilibre, et le cas équilibré meurt (8/8).
- (a′) (uniforme) reste le cœur du problème. Il est maintenant étendu à c = 2 et aux torsions d = 2, 3, avec la même
  nature pseudo-aléatoire.

### 4.5 Ce qui ne change pas

- Q7, ODD-PURE + rang Z, (NG14), (T8)/(T15), (SQ30)+(N15), R8 et les cinq étoiles restent tels que l'archive les décrit.
- Aucun ne se démontre avec les outils de ce soir.

---

## 5. Rangs 39 à 43

- Les obligations par droite existent : ρ = 2, 4, 6 pour c = 1 ; ρ = 3, 5, 7 pour c = 2.
- Mais elles sont diffuses (R4).

**Pistes, avec leur coût.**
- **(a) Branchement « repère d'abord ».**
  - On fixe deux lointains de u indépendants. Les autres u sont alors déterminés à 4 choix près.
  - Coût estimé à ρ = 2 : environ 2·10⁷ repères par droite × 10⁴ nœuds. **Hors de portée tel quel.**
- **(b) Ajouter la positivité réelle.**
  - 7Π_T = 3I − R + EᵀS_Q⁺E est un projecteur de rang 8 : tout bloc principal a ses valeurs propres dans [0, 7], et tout
    bloc 9 × 9 est singulier.
  - Au rang r, on a de plus Res_T ≡ −7Π_T mod 7 si S_Q⁺ est 7-entier (droite générique).
  - Ce sont deux contraintes exactes de nature différente, réelle et 7-adique, sur les mêmes 60 sommets. Non essayé ;
    environ une demi-journée de code.
- **(c) Fixer d'abord les sommets lointains de niveau 0.**
  - Pour D anisotrope, u_w = 0 dès que β(w,w) ≡ 4 : environ 1/7 des triplets.
  - La ligne de R de ces sommets est alors entièrement forcée. Non essayé.

---

## 6. P3 (registre c3), état au 19/10 à 21 h 45 UTC

**Machines.**
- Les deux machines de tranches (220 fils) se sont arrêtées à leur plafond de 6 h (21 h 29 UTC), avec 8 tranches encore
  en cours. Aucun verdict NOT_EXCLUDED n'a été rendu.
- Bords ouverts :

  | bord | tranches manquantes |
  |---|---|
  | (9, 1960) | 01, 05, 06, 08 |
  | (9, 2284) | 02 |
  | (10, 3258) | 13 |
  | (51, 3418) | 02 |
  | (88, 3270) | 08 |

- p3fin (eu-north-1, 30 fils) tourne jusqu'à 02 h 44 UTC. Il a 14 bords entiers en cours, dont ces 5.

**Relance possible, exacte.**
- La tranche i/16 est la réunion des tranches (i + 16t)/256, car la répartition se fait par rang mod n (`py_extend.py`).
- On peut donc redécouper les 8 tranches en 128 sous-tranches.

**Crédits AWS.**
- Usage d'octobre : 132,86 $, entièrement couverts par les crédits, dont 65,22 $ le 18/10 et au moins 20,43 $ le 19/10.
- La note du 12/10 donnait environ 116 $ restants. **Le solde serait donc d'environ 5 à 25 $**, à vérifier dans la console
  de facturation.
- Aucune relance sans ce chiffre.

---

## 6 bis. Étape 2 (20/10, après l'arrêt d'AWS) : pourquoi les droites meurent (ablation, E)

**Instances.** Droites c = 1 génériques, graines 1, 2, 4 et 5. Ce sont les seules des cinq qui vérifient (τ|7) = −1, la
condition L23 de Codex pour le rang 37. La graine 3 est déjà exclue par L23 seul (`tau_legendre.py`).

**Méthode.** Moteur `oblr2` au rang 37 (ρ = 0). On coupe une famille de contraintes à la fois avec la variable
d'environnement OBLR_ABL :
- m : marges L1 ;
- l : L3 ;
- a : λ pour deux lointains adjacents ;
- d : degré 8 ;
- e : comptes proche–lointain ;
- c : voisins lointains communs ;
- q : bijections des paires q et s.

Journal : `ablation_r37.jsonl`, `ablation_r37_pure.jsonl`.

**Résultats.**

| contraintes coupées | verdict | nœuds | profondeur |
|---|---|---|---|
| aucune | 4/4 réfutées | 3 868 à 7 560 | 2 |
| m seule, ou e seule | 4/4 réfutées | 7 191 à 13 387 | 2 à 3 |
| l, a, d ou c seule | 4/4 réfutées | inchangé | 2 |
| **m, l, a, d, e et c ensemble** | **4/4 réfutées** | 435 598 à 452 710 | 4 (76 à 84 s) |
| les mêmes et q (graine 1) | réfutée | 532 841 | 4 (118 s) |
| les mêmes, q, et sans le filtre L2 (graine 1) | TIMEOUT à 280 s | 1 155 584 | 4 |

**Lecture.** L'obstruction est **arithmétique**. Aucune contrainte de comptage n'est nécessaire : il suffit des valeurs
de Green mod 7 et du filtre L2.

**Le noyau de l'énoncé (a′) au rang 37, sous sa forme la plus pure.**
- Statut E. Graine 1 : réfutée avec L2 seul. Graines 1, 2, 4 et 5 : réfutées avec L2 et les bijections.
- Données : Ω = (3I − G_T + J)⁻¹ mod 7.
- Pour chaque paire non partenaire p de C₀, on choisit un triplet de noms (p, q, s) qui vérifie L2 et e_pᵀΩe_p = 0.
- Énoncé : on ne peut jamais obtenir e_pᵀΩe_p' ∈ {3, 4} pour toutes les paires p ≠ p'.
- C'est un problème de « clique transversale » dans le graphe de compatibilité de Green :
  - environ 360 candidats par paire p ;
  - une densité d'environ 2/7.

  Il meurt à la profondeur 4, ce qu'on attend d'un graphe pseudo-aléatoire de cette densité : sur 56 domaines, l'un se
  vide avec une probabilité proche de 1.

**Recherche adverse** (`adversarial.py`). Recuit simulé sur G_T par échanges dans les bijections. La condition L23 est
imposée, et le score est le nombre de nœuds de réfutation.
- 143 pas, tous réfutés. Le score passe d'environ 5 000 nœuds au départ à 10 514 au maximum.
- Aucune droite qui résiste.

**Les G_T les plus symétriques** (`sym_gt.py`, `sym_why.py`, `sym_pure_r37.jsonl`).
- Construction : un groupe H d'ordre 12, à involution centrale, agit régulièrement sur chaque classe. Le graphe ne dépend
  alors que de t = abc (P).
- Groupes : Z12, Z6×Z2 (trois involutions), D12, Dic3. Cela fait 72 graphes.

| type | nombre | verdict au rang 37 |
|---|---|---|
| c = 1 compatible L23 | 12 | 12/12 réfutées, en au plus 92 nœuds |
| c = 1 exclue par L23 | 4 | exclues par L23 seul (cas Z12) |
| c = 2 (18+18), deux formes | 24 graphes, 48 runs | 48/48 réfutées, en au plus 13 855 nœuds |
| c ≥ 3 | 26 | relèvent du registre c3 |
| K < 0 | 6 | invalides |

**Mais leur mort rapide vient de L1, pas de l'arithmétique.**
- Leurs 4-cycles (arêtes partenaires et arêtes croisées) créent des paires de multiplicité K = 0.
- Au test de Green pur, aucun des 319 candidats racine n'est éliminé.
- Sur Z6×Z2, t = (1,1) :
  - le système complet meurt en 92 nœuds ;
  - sans les marges, en 11 266 ;
  - le système de Green pur meurt en 452 291 nœuds, à la profondeur 4, en 106 s : le même profil que les droites
    aléatoires (435 000 à 533 000 nœuds).
- La structure ne change donc pas l'obstruction arithmétique. La taille de sa réfutation est remarquablement constante
  d'un G_T à l'autre. C'est la signature d'un phénomène de comptage générique (environ 360 candidats et une densité de
  2/7), pas d'une structure particulière à chaque G_T.

---

## 7. Fichiers et reproduction

    py oblr_prep.py <c1|c1t|blocks:k1,k2|blockst:k1,k2> <graine> <instance> <rho|-1> <delta> <out.bin>
    oblr.exe <out.bin> <secondes>

- rho = −1 : cas déséquilibré (b cᵀ + c bᵀ).
- delta ∈ {1, 3} : les deux classes de formes non dégénérées.
- `run_r37_batch.sh` et `run_r37_torsion.sh` : un processus, au plus 200 s par instance.
- Fichiers binaires dans le répertoire de travail temporaire, effacés après usage.
