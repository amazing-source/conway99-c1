# Journal C1

## 2026-09-24 (session 1)
- 09:30 Lecture du contexte (mémoire, repos C2/C3). Création du dossier, venv.
- Témoins construits et vérifiés : srg(9,4,1,2), BvLS srg(243,22,1,2), Clebsch, **Gewirtz srg(56,10,0,2)**
  (analogue q = 2, tordu et existant), GQ(2,2), GQ(2,4).
- Fondations redérivées (notes/00). Constat : les deux témoins de la famille sont grid-full (τ = mate), donc aveugles
  à la torsion.
- 13 idées F (notes/10).
- F2 attaquée par SAT (`twist_search.py`) : contrôle positif H(3,3) retrouvé à n = 27 ; **graphe tordu à 20 sommets
  (t = 2)**, puis **à 39 sommets (t = 3)** (UNSAT pour 33 ≤ n ≤ 38). F2 locale tuée.
- F3 (étoiles), F1/F13 (droites) : entrelacement, 0 violation. Tuées.
- F2' (revêtement universel) : H₁ = 0 des exemples tordus. Tuée.
- F4 (Fano) : l'exemple t = 3 n'est pas cohérent par classes. Tuée localement.
- F11 : fermetures en 3-cubes absentes des exemples tordus. Tuée.
- F5 : lemmes L2 (rank₇(A − 3I) impair), L3 (recollement non scindé).
- F5 × C : lemme L4 (k' = 15, k(x) = α − 14 pair, indépendant de x).
- Consigne utilisateur : ne pas s'appuyer sur conway-99-research (amateur). Utilisé seulement comme index de noms.
- Recherche par mécanisme : unicité de BvLS **ouverte** (donc « tout PQ(2,t,2) est grid-full » est au moins aussi dur) ;
  unicité de Gewirtz par forçage spectral (Brouwer–Haemers) ; codes parfaits dans les graphes de Doob (Lloyd via
  l'hôte distance-régulier ; pas d'analogue q = 3 par Egawa).
- Correction : le serrage des grilles (L5) est propre à 99 (9(k−4) = n−9), pas vrai dans BvLS — la validation du
  modèle « point de Hamming » ne peut pas utiliser BvLS.
- Lancé : modèle exact « point de Hamming » t = 6 (Cadical, 30 min, plafond 4 Go).
- 13:57 Mémoire du portable critique pendant une pause : Claude Code a coupé les boucles d'attente. Les 4 modèles
  « familles » (confined 0123, sources 00,10 / 00,10,20 / 00,01,10,11 ; ~650 Mo chacun, 73–81 min sans verdict)
  ont été arrêtés volontairement pour libérer la RAM (5,6 Go libres ensuite). À relancer sur le PC du labo.
  Les 3 recherches tri-circulantes t = 6 (N = 34…45, ~80 Mo chacune) continuent (arrêt automatique à 3 h).
- 16:05 Erreur d'ordonnancement : lancer 2 tests Fano en même temps a fait passer la RAM machine sous 2 Go ; le garde-fou a tué le cas deux étiquettes |C| = 5 (18 min perdues). Famille Fano arrêtée, |C| = 5 relancé (twolabel_dom23456_b). Règle : un seul lancement à la fois, RAM libre vérifiée avant.
- 16:15 L'utilisateur signale que le portable rame (et une question sur les ventilateurs) : j'avais 4-5 calculs en parallèle. Tout arrêté (0 processus, 6,9 Go libres). État sauvegardé : k=3 24/128 UNSAT ; interrompus : deux étiquettes |C|=5, Fano « first », énumération k=4, spectre de Hodge de BvLS. Règle désormais : un seul calcul lourd à la fois sur le portable ; le volume va au PC du labo.
- Piste Σν³ poursuivie : spectres rotationnels de Q calculés sur toutes les géométries ; non tordu ⇒ spectre entier = valeurs du gradient ; tordu ⇒ irrationnel, Σν³ > 0. Borner Σν³ ⟺ spectre rotationnel = {3, −4} ⟺ (vraisemblablement) grid-full : c'est la conjecture F2-SRG sous forme spectrale (« laplacien de Hodge à deux valeurs propres »), pas un raccourci.
- 16:40 (après auto-compaction) L'utilisateur demande de poursuivre la route Σν³, recherches autorisées.
  Vérification préalable de ma propre affirmation (« confiner le spectre rotationnel dans [−4, 3] par Garland ») :
  **fausse**. Théorème H0 : confinement ⟹ M = 0 ⟹ grid-full ⟹ M ≠ 0 pour t ≥ 2. `hodge_blocks.py` : identités par
  blocs H1–H3 exactes sur 6 géométries ; BvLS (24 s, 557 Mo, un seul calcul) : rotationnel
  {−20^11, −5^660, −2^660, 4^880, 7^220}, exactement la prédiction par théorie des représentations.
- 17:00 Recherche ciblée : Reimbayev arXiv:2608.19410 (fréquences d'ordre 7, variables libres n₃, z₁₁) ;
  n₃ = 3(P_max − P) = ½Σ|W| (confirme L15). `reimbayev7.py` : règle de somme OK sur n₃ et z₁₁, échec sur les
  constantes (z₁₇₆ probablement 1/8 et non 1/84, plus un écart B(k+6)) ; à (99,14) la non-négativité ne donne que
  0 ≤ n₃ ≤ 4158. Lou–Murin 2014 (PRIMES) : faits locaux (π(L) ≠ 11). Thakkar–Severini 2026 : CP-SAT, rien de neuf.
- 17:08 Route Hodge / Σν³ close (notes/60_HODGE.md). Rapport, README, notes 10/20/30 mis à jour.
- 17:20 L'utilisateur (frustré par le faux espoir, et sans moyens de calcul) demande une voie mathématique, pas du
  SAT. Nouvelle idée : conditions de Krein pour des configurations dérivées. **L16 : P ≤ 1151** (droites dans E₋₄ ;
  la somme des cubes des produits scalaires est une norme au carré). Contrôle BvLS exact. Tentatives de
  renforcement (drapeaux, graphe des droites, Krein locales sur H, degrés ≤ 16) : rien de plus, et aucune borne
  inférieure sur P. notes/70_KREIN_DROITES.md.
- Incident mineur : TaskStop n'a pas tué le processus python enfant du venv (il a tourné ~12 min, un cœur) ; tué à
  la main. Tous les calculs de cette heure sont instantanés (formules), aucun calcul lourd.
- Nuit. L'utilisateur : chercher une « étincelle » à la C3 sans copier C3, et raisonner en supposant que Γ n'existe
  pas. Posture adoptée : une preuve doit tuer le désordre (torsion forte), or tous nos outils tuent l'ordre.
  Nouveau : Σ|W| = 1386 + 32‖Σ u_L^{⊗3}‖² (torsion = moment cubique des droites) ; L17 (le 70-espace local se
  scinde en 2, 3, 5, K₃ pair 2-unimodulaire, formes 3/5-adiques déterminées ; mécanisme vérifié sur BvLS mod 5) ;
  structure d'Eisenstein des droites orientées (graphe à gains Z/3). Tout est cohérent : pas de contradiction.
  notes/80_ETINCELLE_ARITHMETIQUE.md.
- Nuit (suite). Lecture de Bondarenko–Radchenko (famille λ = 1, g = k) : leur représentation euclidienne force les
  réflexions σ_v à être des automorphismes, d'où une structure de F₃-espace (n = 3^m). Pour 99, g = 44 ≠ k : il
  reste 30 dimensions libres par sommet (W_x^⊥), c'est là que vit la torsion. Lou–Murin : lemme de variance de
  Wilbrink–Brouwer (local). Thakkar–Severini : constructions partielles, rien d'exploitable.
- **L18** : identification de la seconde variable libre de Reimbayev (z₁₁) : z₁₁ = 4n₃ − 2S, S = nombre de paires
  σ-adjacentes (= coïncidences τ_a(c) = τ_c(a)) ; le polygone d'ordre 7 est exactement 0 ≤ S ≤ n₃. Vérifié par
  comptage direct des sous-graphes induits sur 4 géométries (`code/z11_identity.py`). Grilles avortées :
  Σ(18 − e(G)) = 2n₃ − S/2, défaut euclidien |Σ_G p|² = 18(18 − e) ; opérateur de défaut Δ ⪰ 0 sur E₋₄.
  Matrice des réflexions Z (= J − I − A si non tordu ; masse à distance 3 sur les géométries tordues).
  Pas de contradiction. notes/90_SECONDE_VARIABLE.md.
- Suite : borne de Delsarte locale sur le schéma des étiquettes (B₇, 6 relations) : traces exactes de H par
  composante irréductible de K, toutes les contraintes automatiquement satisfaites (résultat négatif, vérifié :
  comptages par relation exacts en chaque sommet des 5 géométries). Piste U_x = (2H+1)σ_x (similitude de norme 49
  sur K, valeurs propres entières algébriques de norme 49 créées par la torsion) notée, sans contradiction.
  Lecture du dépôt C3 (étincelle = décomposition Z[C₃] → Z × Z[ω] et matrice d'Eisenstein M² + M = 12I, puis
  calcul) : repose sur la symétrie, pas transposable tel quel à C1.
- Nuit (fin). L'utilisateur : « décortique le problème, pose-toi des questions, tu peux utiliser du calcul ».
  Construit une hiérarchie exacte : équations de comptage des sous-graphes induits (validées sur 4 SRG), résolution
  exacte (ordre 7 : 208 types, variables libres 3P et S/2 = Reimbayev ; HiGHS flottant disait « infaisable » à
  tort, artefact d'échelle), ordre 8 (916 types) ; positivité euclidienne (degrés 1–4, témoins, E₋₄/E₃,
  harmonique, enracinée ; validée à 1e-15 contre les vrais vecteurs propres de srg(9) et Petersen) ; positivité de
  drapeaux (erreur 0 sur srg(9), Petersen). Contrôle BvLS cohérent (P = 8910 admis). Résultat : tout bute sur
  P ≤ 1151,08 (L16) ou ne contraint rien ; aucune borne inférieure sur P. notes/91_HIERARCHIE_ORDRE8.md.
  Tous les calculs sous plafond mémoire (max ~3,2 Go), un à la fois.
- Nuit (tard). L'utilisateur : « prouve qu'il existe » (tentative de construction, C1). Méthode RRR d'Elser
  (projections : 0/1 ∩ spectre), trois formulations (générique, enracinée avec structure forcée, par droites) ;
  étalonnage : trouve Hoffman–Singleton et Gewirtz, pas srg(81,20,1,6) en 10 min. Littérature vérifiée après coup
  (question de l'utilisateur) : SAT (Keramatipour 2026) et heuristiques (Thakkar–Severini 2026) échouent ; RRR
  jamais appliqué aux SRG à notre connaissance. Message de la session C2 : corrections de rigueur faites (|Aut|,
  L8, L11, deux étiquettes), réponse envoyée. notes/92_CONSTRUCTION.md. Étalonnage long (1 h) en cours.
- Plafond « 70 % » : score de Thakkar–Severini (4950 contraintes) ; expérience témoin par recuit simulé, 8 min par
  graphe : 99 → 59 % ; SRG existants : Hoffman–Singleton 83 %, Gewirtz 64 %, BvLS 49 %, M22 42 %, Brouwer–Haemers
  35 %, Higman–Sims 31 % ; aucun retrouvé. Le plateau est algorithmique, pas un signe de non-existence. Session C2
  informée (un échec heuristique sur C2 ne serait pas informatif). notes/92 §4.
- Nouvelle posture (non-existence, prompt ChatGPT lu avec recul, sans agents). Cadrage « six unités » réfuté (il
  faut une borne supérieure sur la torsion, qui n'existe pas). Programme B (tr Δ²) : échec expliqué (trace linéaire,
  Frobenius quadratique). F17 naïve réfutée par les produits cartésiens (géométries tordues t = 6 sans plan d'ordre 6).
  Hypothèse « la géométrie à 42 sommets vient du plan de Fano » testée : fausse (non isomorphe). **L19** : forme de
  Smith 7-adique de U_x = (1^k, 7^{70−2k}, 49^k) avec k global ; valeurs propres = 7·racines de l'unité sauf un déficit
  ≤ k ; si k = 0, congruences s(x) ≡ 0 (7), e_σ(x) ≡ 14 (49). Direction retenue : comprendre k. notes/93.
- Nuit (8 h autonomes demandées). **L19 bis : k ≥ 2** (à la main : sur Γ₂(x) les combinaisons des lignes de B₁(x) sont
  additives en étiquettes ; les paires où elles doivent s'annuler contiennent des triangles, d'où tout nul). Programme D
  (parités d'holonomie des droites, `parity_probe.py`) : pas de loi. Littérature en texte intégral : Makhnev 1988
  (mathnet, PDF via getFT + cookies) = **notre L1 (déjà connu)** ; Wilbrink–Brouwer 57 (rapport CWI) : la méthode ne
  passe pas (prisme non tendu à 99, c = 30 ; coclique de Hoffman non forcée ; design local trivial pour μ = 2) ;
  Reimbayev srg(19) : saturation à t = 2, marge énorme à t = 6 ; livre BvM 2022 : état de l'art (Wilbrink 1984 ordre
  11, Behbahani–Lam, Crnković–Maksimović 2020 ordres 6 et 9 ; la preuve de Makhnev pour Moore 3250 est fausse).
  notes/94_NUIT_LITTERATURE.md.
- Nuit (suite). Littérature complète en texte intégral (Wilbrink 1984 via le navigateur, Cesarz–Woldar 2025, Ishida
  2026, Shpectorov–Zhao 2025, etc.) : rien pour C1 (notes/94 §3.5–3.9). **Preuve humaine de L7** (point de Hamming +
  σ_x ∈ Aut impossible) : décalage diagonal δ additif, le fait C impose une parité impaire sur chacun des 105
  triplets, la somme totale compte chaque δ 12 fois, donc 0 ≡ 1. Vérifié (`hamming_diag.py` : système réduit UNSAT,
  parité incompatible sur F₂). notes/95. L8 général : l'invariant naturel (signature) n'est pas forcé par C.
- Nuit (01:30). **Akiyama (arXiv:2609.08319, 8 sept. 2026)** : non-existence de srg(266,45,0,9), cas ouvert, par
  réseaux entiers (repère local serré de rang 11, complétion unimodulaire paire de rang 24, identité de Venkov, racines
  A₁₁D₇E₆, moments), formalisée en Lean. Lu en entier. Pour 99, repères serrés entiers exacts calculés :
  L₋₄ = 24I + 2J − 8H − 3S − P' (84 vecteurs de norme 20 en rang 30, constante 56) et L₃ = 60I − 2J + 15H − 4S + P'
  (norme 50 en rang 40, constante 105). La transposition n'est pas immédiate (repère peu dense, constante paire 56
  avec la partie 7 = k de L19, complétion en rang ≥ 32 où S₁₈ ≠ 0). Plan écrit. notes/96.
- Nuit (03:00). Noyaux UNSAT minimaux (`core_extract.py`, `core_family.py`, sélecteurs par équation) : les trois cas
  g19 ont le **même noyau de 7 contraintes**, d'où un lemme local nouveau **L9'** (τ_a(c) ≠ c̄ et τ_{c̄}(a) = ā ⇒ une
  grille G_{[c],m} manque) et une **preuve humaine complète de L10** (g(x) ≤ 18). L11 : noyau minimal de 112 équations,
  trop gros pour la main.
- Nuit (03:30). **Audit indépendant de L16** (P ≤ 1151), tout refait à la main : Gram E₋₄ des droites (4, 0, 1 − e),
  comptes n₀…n₃ en fonction de π(L) (216 arêtes vers les droites disjointes, 36 quadrangles par droite), Σ K = 0,
  Σ K³ = 60 − 6π, ‖T_L‖² = (13860 − 12P)/64 ; raffinement points-droites : ‖T_P‖² = 99·14868/21952 ≈ 67,05,
  ⟨T_P,T_L⟩ = −231·4,5/(28√28), d'où ‖T_L‖² ≥ 0,734 et P ≤ 1151,08. **Correct.** Filtre des 728 motifs confinés à
  3 classes par les règles humaines L9', L12, L13 : 560 survivent (la propagation n'en laissait que 28) ; L11 à la main
  hors de portée cette nuit.
- Nuit (04:00). **L20** : sous-matrices principales de A − 3I sur B₁(x) ∪ étoile(a) (déterminées par τ_a), bloc du
  moulin inversible mod 7, d'où k ≥ rang₇ du complément de Schur. Calcul exhaustif sur les 10 395 τ_a :
  **rang = 11 − 2·(nombre de cycles pairs du graphe de classes de τ_a)**. Donc **k ≥ 6** (au lieu de 2) ; k = 6 ⟹
  P = 0 ; P ≥ 1 ⟹ k ≥ 8 ; une étiquette non tordue ⟹ k ≥ 12. Premier lien démontré entre k et la torsion
  (notes/97). Pas de borne supérieure sur k : pas de contradiction.
- Nuit (02:10). **L20 bis : k ≥ 8.** Formule locale exacte k = rank₇(H + 4I + 3S + P' + 5J) ; si k = 6, les étoiles
  (type (2,2,2), rang 5 = k − 1) engendrent des hyperplans non dégénérés, donc leurs vecteurs de noyau sont des
  relations entre lignes complètes : ligne({a,ℓ₁}) = ligne({a,ℓ₃}), et la colonne {ℓ₁,q} donne H − H' ≡ 4 ou 5 mod 7,
  absurde. Formules de Schur vérifiées exactement (G = −(3/8)I − P/8 + J/16). Crédit du principe : van Eijl 1991.
- Nuit (02:40). **L20 ter : k ≥ 10.** Généralisation de L20 bis par énumération exacte des annulateurs possibles des
  relations d'étoile, plus un modèle SAT petit (degrés, contrainte d'étiquette τ_ℓ(a) unique) : k = 8 exclu (32 cas
  UNSAT par propagation, contrôles SAT sans la condition linéaire ou sans la contrainte d'étiquette). Bogue
  d'énumération (colonnes à fonctionnelle nulle) trouvé et corrigé ; résultat inchangé. Pour k = 10, la méthode à une
  étoile n'exclut plus rien de décisif.
- 25/09, 03 h – 05 h 30. **Verrou principal** (consigne « continue sur le verrou principal »), notes/99.
  - **L21 (nouveau, à la main)** : rang₇(A − 3I) sur la boule d'une droite = 2 + rang₇(A_{G(L)} − 3I), G(L) cubique
    sur les 36 voisins de L ; d'où k ≥ 23 − d(L), d = composantes + 7-rang du tas de sable. Une droite générique donne
    k ≥ 22 ; L20 = cas « deux points de L » ; le rang « deux étoiles » de notes/97 = 23 − d(L). Identité vérifiée sur
    700 configurations, critère d = 1 ⟺ 7 ∤ τ(G) sur 317 (0 exception). Recuit : max d = 9 (conjecture k ≥ 14).
  - **Triplets de droites (ordre 9)** : quatre repères de l'espace des droites (dim 1, 54, 44, 132 ; le dernier est
    invisible depuis les points), comptages exacts de triplets (validés sur BvLS : 0 écart, 0 équation violée, Gram
    positives). Relâchement jusqu'au degré 4 de Hadamard : P ∈ [0, 1155]. Négatif. Incident : un premier calcul mal
    mis à l'échelle annonçait P ≤ 178 ; artefact, corrigé par remise à l'échelle.
  - Fonctions F₃ de somme nulle sur les droites : 2 à 7 dimensions dans les géométries tordues. Négatif.
  - Enraciné en une droite (même modèle vu d'une droite, structure locale exacte, validé sur BvLS) : π(L) = 0
    faisable avec μ_L ∈ [0, 18] ; une droite entièrement tordue n'est exclue par rien. Négatif.
  - Bilan : la voie 7-adique ne fait que minorer k (heuristiquement k ≈ 30) ; la positivité s'étend aux 9 points des
    triplets de droites sans rien donner. Verrou entier.
- 25/09, 06 h. **Synthèse des 21 lemmes** (question de l'utilisateur), notes/100. Tableau quantité/sens/statut ;
  tous sont des planchers (torsion faible exclue, k minoré), aucun plafond ; le profil de torsion maximale (P = 0,
  g = 0, k = 30) satisfait tous les énoncés, donc aucune contradiction possible à partir d'eux seuls. Corollaires :
  k = 10 ⟹ m(e) ∈ {0, 2}, |W(x)| ≥ 56, P ≤ 462 pair (L20 + L20 ter refait pour k = 10 + L15) ; k ≤ 20 ⟹ droites
  7-dégénérées ; g_tot ≤ 191. La pièce manquante est un plafond.
- 25/09, 06 h 15. **Décision de l'utilisateur : plus de solveurs** (« ça n'en vaut jamais la peine »), après la
  branche C2 (SAT de 8 h, cassage de symétrie, cube-and-conquer, générateur : rien). LAB_INSTRUCTIONS et §6 du
  rapport gelés. La suite se fait en mathématiques pures (notes/100 : il manque un plafond de torsion).
- 25/09, 08 h. **L22 : k ≤ 28** (notes/101). Route A, argument de genre : Λ₋₄ pair, rang 44, det 9·7^{14+k},
  partie 3 = Z/9 ; à k = 30, U = 0 force ε₇ = (9|7) = +1 alors que l'oddité exige −1. Conventions testées (A₂…E₈,
  2300 réseaux aléatoires, 0 échec) ; schéma validé sur Petersen, T(7), T(8), srg(9). Brouwer–van Eijl 1992 lu :
  seulement ≤ 45, pas de genre. notes/100 corrigée (profil de cohérence à k = 28). Premier plafond du corpus.
- 25/09, 09 h. **L23 et structure 7-adique complète** (notes/102). Recherches : Ducey et al. (groupe critique du 99,
  7-rang pour srg(28,9,0,4)), Brouwer–van Eijl, Chvátal, familles 2025, Akiyama : personne n'utilise genre, oddité ou
  signe des réseaux propres. Maths : N² ≡ 2J ⟹ N de carré nul sur 1^⊥ ; β non scindée (signe de L22) ; M_x² ≡ 0 et
  forme de M_x hyperbolique (moulin : rang 14, disc 1). Outil : un bloc extrême (rang Q = 14 + k) est non scindé.
  Boule de droite : disc = τ(G(L)) si d = 1, d'où **(τ | 7) = +1 ⟹ k ≥ 24**. Contrôles : 5 SRG (beta_form_check,
  gq33_check), 300 boules (ball_sign_check), 0 échec. Négatif : blocs d'arête de rang Q impair (edge_block_sign, 10 395 τ).
- 25/09, 11 h. **Structure de Kneser en un point de Hamming** (notes/103, consigne : attaquer la structure générique
  en maths pures, en lisant le Théorème D de C2). Réduction exacte de L8 à une S₄-connexion sur K(7,2) ; régime « tout
  A » réfuté (triangles équilibrés + couples complémentaires) ; classification des holonomies autour d'une arête
  (énumération exhaustive) ; point de Hamming ⟹ 18 ≤ k ≤ 26 (grilles complètes dans U′). Régime mixte ouvert.
- 25/09, midi. **L8 : les deux régimes extrêmes sont exclus à la main** (notes/103 §6-7).
  - Aucune arête isométrique : les images antipodales forment 21 tournois à degrés entrants pairs (μ avec les
    étiquettes). Le fait C impose un accord pair sur chaque K₄ commun, et la parité donne 0 ≡ 1 sur tout triangle de
    classes. Version locale : trois paires par une même classe ne peuvent pas être entièrement non isométriques.
  - L7 local : les 18 arêtes autour d'un triangle de classes ne sont pas toutes isométriques.
  - Correction de notes/95 : une arête non isométrique a 0 ou 2 transports isométriques, pas 0 ou 1.
  - Reste le cas mixte : une coupe (paires de {1,2,3,4} contre le reste) passe toutes les contraintes locales. Il
    faudra les parties de translation.
- 25/09, après-midi. **L8, cas mixte : recherche annexe et nouvelles planches** (notes/103 §8-11).
  - Littérature : rien sur cette configuration. Les outils classiques repérés sont le code de Golay (BvLS, m = 11),
    les totaux de Sylvester, les plans de Fano, et H¹ = 0 pour les signatures de K(7,2).
  - Parité S₃ du fait C : tous les types ont la même parité, et μ avec les étiquettes devient linéaire.
  - Relations à constante impaire : L8 se ramène à la parité de 21 quantités locales Q_R, de somme 105. BvLS montre
    qu'elles ne sont pas paires en général : il faudrait la rigidité propre à m = 7.
  - Livres et carrés : jamais de carré 3-cycle.
  - Le modèle local exact autour d'un triangle de classes a 1 522 solutions : la contradiction est globale.
  - L7 local généralisé (pages à images antipodales uniformes : impossible).
  - Pas de δ étendu à défaut linéaire ; pas de certificat de parité de degré 2 (fait C + μ + signes).
- 25/09, 12 h 30. **F10 attaquée : tissu de 11 grilles** (notes/104, session « approche par les structures »).
  - Réduction exacte à 55 permutations M_ij (équation (E), analogue de (K) de notes/103).
  - Couplages tous anti ⟹ Σ_k M_ik M_kj = J ⟹ **plan projectif d'ordre 10** avec polarité (droite absolue, Baer) :
    exclu par Lam. Contrôle inverse à l'ordre 4 : PG(2,4) + polarité + K₃ donne srg(15,6,1,3) (weave_pg4_control.py).
  - Tous iso : 7 ∤ 220 (congruence des sous-espaces invariants). Pur mixte : deux classes, mod 7 ⟹ {2,9}, puis
    β − α/2 ≤ 2 (weave_grid_traces.py, 72 automorphismes) ⟹ contradiction. **L25.**
  - Régime général (bijections ni iso ni anti) : identités Π, Y² + 3Y + X² = 10 avec [X,Y] = 0 ; spectralement
    invisible. Ouvert. Annexe : spectre du sous-graphe à 77 sommets hors d'une coclique de Hoffman.
- 25/09, après-midi. **L8 démontré** (notes/105 ; aucun solveur, quatre vérifications finies de quelques secondes).
  - Intégralité d'ordre 8 (p-adique, 6 032 équations) : aucune condition. En un point de Hamming, k = rang₇(N − 3I)
    sur Z^⊥ exactement.
  - Cas coupe impossible : seules 28 coupes passent μ avec les étiquettes ; une seule orbite reste après notes/103 §6,
    et un tournoi y force toutes les classes à être des sources.
  - **Squelette de Fano.** Chaque point de Q_P est sur 5 droites formant un couplage parfait de Petersen. Le nombre de
    droites au-dessus d'un triangle de Kneser est pair (pas de 3-cycle). Les seules fonctions cohérentes sont les 30
    plans de Fano sur les classes : ℓ = 4 sur les faisceaux, 2 sans droite, 0 avec une droite.
  - Section X parallèle hors faisceaux ; C = {X ≠ A} indépendant ; C = ∅ ramène à L7. Il reste 35 configurations :
    14 étoiles, exclues par notes/103 §6, et 21 quadrilatères, tués par deux μ-parités en chemin P₃ et la règle (i).
  - En chemin : lemme spectral (S_I − 5)(S_I + 2) = −KKᵀ (quatrième preuve de L7) et lemme des composantes.
    Correction de l'affirmation « NNN = 2-cycle ».
- 25/09, fin d'après-midi. **Comptage des fentes (notes/108) : L11 démontré, g(x) ≤ 17.**
  - Autour des grilles complètes, μ avec les étiquettes force des couplages parfaits (unicité des fentes sur K₅ tant
    que les défauts voisins sont sécants).
  - Un sommet tordu n'a alors plus de place pour ses ombres. Lemme D1 : les grilles incomplètes ne sont jamais deux à
    deux sécantes. Lemme D2 : la configuration chemin est impossible.
  - Donc L11 (sans SAT), le cas g = 19 de L10 redémontré, et g(x) ≤ 17 (ancienne frontière de L10).
  - Recontrôle indépendant des énumérations de L8 : identique.
- 25/09, soir. **Routes closes, codes des droites, L14 (|C| = 2) à la main** (notes/110, 111).
  - Minkowski sur Λ₃, Λ₋₄ : vecteurs courts forcés (≤ 36, ≤ 44), mais la paire de Petersen passe tous les comptages ;
    classification infaisable, route close. Akiyama sur Λ_L : ni Venkov (rang 48, S₂₆ ≠ 0), ni isolement des racines,
    ni repère dense de rang ≤ 24 ; route close.
  - Les codes p-aires des droites contiennent leur dual (p = 2, 3, 5) : rang₂ N = 72 + ½ rang₂(NᵀAN) ≥ 72,
    77 ≤ rang₃ N ≤ 98. Contrôle BvLS. Invariants nouveaux, sans contradiction.
  - **L14 pour |C| = 2 démontré à la main** : fentes, trois doubles forcés par μ, puis 4 voisins communs disponibles
    contre 5 exigés dans le bloc tordu × tordu. |C| ≥ 3 reste au SAT.
  - Correction de notes/102 §9 (les arêtes d'ombre sont sur des droites intérieures non pures).
- 25/09, nuit. **Démarche expérimentale de C3, labo séparé** (notes/113, 114 ; `Desktop/c1_experimental`).
  - Demande de l'utilisateur : faire travailler les trois sessions avec la méthode de C3, pas avec son contenu.
    Registre de pistes noté P/C ; énoncés généraux testés sur de vrais graphes avec contrôles négatifs.
  - Contenu de C3 : clos par « structures » (notes/113), avec C2.
  - Outillage : Go 1.27 et GCC 16.1 installés à la demande de l'utilisateur. `code/padic.c` : Smith et noyaux sur Z_q
    en C. Le calcul X1 sur BvLS passe de plus de 20 min à 4,5 s.
  - Résultats :
    - graphe lointain d'une droite (spectre fixé par G(L), réseaux de rang 18 et 8, Nikulin sans prise) ;
    - graphes réels de valeurs propres {3, −4}, jamais utilisés : srg(49,24,11,12) et srg(50,21,8,9), ce dernier par
      commutation trouvée à la main. L22 y est sain ;
    - équilibre de C2 re-dérivé, principe de variance nulle (égalité de Rayleigh), lemme E, exclusion de Fano si σ
      respecte l'appariement ;
    - droites équiangulaires fermées (borne 540).
  - En parallèle : « structures » démontre S5 (critère mod 4 sur det Λ_θ ; 35 ensembles ouverts exclus, 0 faux positif
    sur 1183 graphes connus), puis rejoue L21 et L23 sur de vrais graphes (ils tiennent). C2 ferme ses
    configurations ancrées.
  - Aucun plafond pour l'instant.
- 25/09, nuit (suite). **Lemme du triangle (notes/115).**
  - Principe de Rayleigh (A ⪯ 3I + (11/99)J) sur le support entièrement déterminé x + étiquettes + 12 paires de trois
    classes. Complément de Schur sur le moulin : T ⪯ 3I − P_∂ exactement. Recalcul indépendant par « structures ».
  - Corollaires : e ≤ 12 ; au cas tendu, Aq = 3q avec des comptes exacts 1 et 3.
  - Premier outil exact actif en torsion maximale : 22 % des configurations admissibles tuées ; le modèle de Fano est
    forcé au cas tendu.
  - Aussi dans le labo : projecteur caché d'une droite (A_F = B₀ − 7Π₋₄, rang 8) et outil de certificats de Rayleigh
    pour les branches à M partiel (`code/hidden_projector.py`, validé sur BvLS).
- 25/09, nuit (suite). **Second ordre exact et Fano tendu (notes/116).**
  - Le point 3 du lemme du triangle est recalculé par « structures » : CONFIRMÉ (commit 6119697).
  - Outils généraux : A_Δ² + A_Δ − 12I = 2J − ∂ᵀ∂ (sur ker ∂, seules les valeurs propres 3 et −4) ; identités (P2) de
    second ordre par blocs ; critère lointain (U)/(L), formes closes du projecteur caché pour 99.
  - Au Fano tendu : comptes génériques exacts, κ, équilibre étiquette, (F5) par variance nulle. Tous les systèmes
    dérivés sont faisables (HiGHS, au plus 37 s, avec contrôles). Un témoin passe tous les tests de niveau bloc.
  - Le Fano tendu n'est donc pas une route de plafond. Deux fausses violations venaient d'identités non imposées.
- 26/09. **(P2) par types en torsion maximale (notes/117).** Méthode de C2 (H-β tué) transposée au cœur C1 : types de
  paires (multigraphes de classes de G_z), lignes linéaires, dont les 231 identités (P2).
  - 19 configurations locales admissibles aléatoires sur 31 sont infaisables, chacune certifiée par un Farkas exact ;
    un certificat a été revérifié par « structures ».
  - Environ 40 % survivent, dont le témoin de Fano.
  - Aussi : aide à C2, qui a tué H-β ; le certificat se lit comme une seule identité circulante demi-entière sur son
    squelette le plus symétrique.
- 26/09, matin. **Niveau paire × bloc et obstruction Ψ (notes/118).**
  - Les 3 survivants de l'échantillon S = 0 meurent au niveau paire × bloc. « Structures » a revérifié les
    2 certificats exacts et les 19 certificats de cellules.
  - L'ablation désigne cellcross comme la famille qui tue.
  - Au Fano tendu, cellcross se découple par bloc. Il en sort une fonctionnelle universelle Ψ_R, reproduite par
    « structures ». Mais 480 choix de retournements l'annulent pour σ du témoin. Les systèmes « cellules par bloc »
    échouent dans 16 à 19 blocs sur 21.
  - Strate des σ internes : un survivant indéterminé.
  - Auto-attaques : un statut « limite de temps » n'est pas une mort ; les spéciaux sont dédoublonnés quand une arête
    σ est interne ; les morts d'un tirage aléatoire ne valent pas pour un choix adverse.
- 26/09, fin de matinée. **Retour aux mathématiques pures (demande de l'utilisateur) ; lemme P-Ψ (notes/119).**
  - pairblk combiné à Ψ donne, au Fano tendu, une condition exacte par paire, relue à la main par « structures ».
  - Elle se lit comme un système F₂ par droite en les retournements. Les 9 σ testés sont morts pour tout τ.
  - Il reste l'argument global.
- 26/09, après-midi. **Vecteurs propres cellulaires forcés, triades (notes/120).**
  - Dimension forcée ≥ 5 (Q) et ≥ 7 (mod 7) de fonctions cellulaires propres pour 3 ; refaite à la main par
    « structures ».
  - C2 a transmis son Théorème F. Sa transposition en C1 donne des règles de triades rigides, mais pas de contradiction :
    le budget vaut 8 et il est saturé.
  - P-Ψ reste un filtre exact, pas un lemme.
- 26/09, après-midi (suite). **Portes relues, Fano tendu mis en pause.**
  - Le dérangement cerise/σ, idée de « structures », est clos : le compte T ≡ 1 est faux au témoin (14 cas sur 42 seulement).
  - La voie 7-adique par sous-matrices déterminées est close : il faudrait un support déterminé de rang₇ ≥ 45, et le
    maximum connu est de 39 points (L21 donne au mieux k ≥ 22).
  - Porte proposée : la géométrie interne I_x (140 droites internes) à P = 0. La torsion maximale aux étiquettes
    u ∈ N(x) s'y lit comme une contrainte exacte sur les droites internes : pour y = {u,v} et une droite interne
    {y, p, p′}, τ_u(w_p) ≠ w_{p′}, où {u, w_p} est le second u-voisin de p.
  - Au passage, la torsion en u pour l'étiquette ū équivaut à « ρ_α sans point fixe », et un point fixe est un prisme
    par l'arête uū (cohérent avec L13 et P = 0).
  - Aucun de nos PL ne modélise les droites internes.

- 26/09, soir. **Différences de retournement, parités de branche, P-Ψ réduite (notes/122).**
  - Lemme des différences de retournement (refait à la main par « structures ») : T(L) est sans triangle ssi
    poids(d(L)) ≠ 1, et T(L) = C6+C6 ssi d(L) = (1,1,1).
  - Identité des parités de branche. P-Ψ se réduit à trois inconnues par droite ; sur une droite tout-CM, τ est
    déterminé par σ.
- 26/09, soir (suite). **Rapport d'Astra sur le dossier n° 2** (transmis par l'utilisateur via « structures » ; résultats
  d'Astra, non refaits par C1) :
  - il y a exactement un revêtement de degré 4 de K₇ à λ = 1 (non régulier, 28 sommets, monodromie S₄, 8 prismes).
    Construction et prismes prouvés à la main par Astra ; unicité par deux énumérations exactes indépendantes ;
  - d'où la branche « factorisation de Heawood » du Fano tendu force P ≥ 24 : **exclue à P = 0** ;
  - le σ du témoin meurt par P-Ψ pour tout τ, avec un certificat sur une seule paire (revérifié par « structures ») ;
  - la contrainte τ–σ d'Astra est **redondante** : elle découle de P-Ψ, de la réciprocité de σ et de la symétrie des
    comptes de blocs. Elle ne compte donc plus parmi les ingrédients de notes/122 §4 ;
  - définitions de β, e, d, r et identités r₀ = r₁ = r₂, e_i = d_j + d_k (non refaites ici).
- 26/09, soir (suite). **Dossier n° 3 (demande de l'utilisateur), partage sans recouvrement** :
  - Astra : Fano tendu général (tâche principale), généralisation de sa classification en contrainte (tâche secondaire) ;
  - C1 : cas général, porte I_x à P = 0 ; C1 ne touche plus au Fano tendu ;
  - « structures » : vérifications, pont entre les conditions locales de C1 et les comptes d'Astra, soutien à C2.
  - Transmis à Astra par C1 :
    - la reformulation par droite (les 24 atterrissages dans C4(L) ≅ vecteurs pairs de F₂^L ; F5 et P-Ψ sont des
      conditions « ≠ » sur deux coordonnées différentes ; le seul couplage entre droites passe par les bijections σ_U
      et par B, L, P2) ;
    - l'identité (A + I)Aψ_R = 12ψ_R − 30ζ_R (pairblk dans la direction Ψ_R, utilisable pour les paires hors de R) ;
    - la question décisive : F5 + KBLDP + P-Ψ + admissibilité a-t-il une solution ?
- 26/09, nuit. **Rapport d'Astra sur le dossier n° 3** (via l'utilisateur et « structures » ; résultats d'Astra, vérifiés
  par « structures », non refaits par C1) :
  - **Q2 : P-Ψ + admissibilité + identités de bloc ont une solution.** Témoin explicite dans la branche « rang 8 » :
    tous les retournements valent 1, T = C12 sur chaque droite, rang M_β = 8. P-Ψ n'est donc pas un lemme de Fano
    complet.
  - Ce témoin meurt au niveau paire × bloc par une **borne ordonnée** (6 > 5 pour y = {0.0, 2.0}, R = {0,1}), pour
    tout τ admissible. Toute la famille « deux factorisations de Heawood affectées par parité » est exclue
    (PGL(3,2) doublement transitif sur les 8 factorisations).
  - Outil général (bornes ordonnées) : si y a g_y(B) voisins génériques dans le bloc B, et si les comptes c_z(R)
    des z ∈ B sont triés a_{B,1} ≤ … ≤ a_{B,4}, alors
    Σ_B Σ_{i≤g_y(B)} a_{B,i} ≤ t_y(R) ≤ Σ_B Σ_{i>4−g_y(B)} a_{B,i}.
    Utilisable dès que les comptes sont fixés, hors du Fano aussi.
  - Pour I_x : un revêtement de K₇ avec λ = 1, μ ≤ 2 et sans prisme est de degré ≥ 5. Au Fano tendu, le graphe
    auxiliaire H (6-régulier, λ_H = 1) a au plus 2 composantes à P = 0.
  - Q3 : les parités r_i et e_i sont redondantes.
- 26/09, nuit. **C1, porte I_x à P = 0 : premières explorations** (DÉRIVÉ, contrôles exacts sur BvLS). Rien de tout
  ceci n'est un plafond, ce sont des conséquences automatiques de A² = 12I − A + 2J :
  - holonomie d'un triangle T : les prismes sur T sont les points fixes de σ_T (composée des trois couplages
    croisés). On a P(x) = Σ_{T∋x} fix(σ_T), et F_T contient 32 − fix(σ_T) triangles (recoupe notes/114) ;
  - **hexagones induits : H + 3P = 213444** (formule de Reimbayev 2024, retrouvée par classement des 6-cycles selon
    leurs cordes ; contrôle exact sur BvLS : 4 980 690). Le plafond P ≥ 1152 équivaut à H ≤ 209988 ;
  - graphe signé des triangles A_Σ = N₀ − N₂ − 2N₃ : **A_Σ² = 13A_Σ + 68I** (BᵀE₋₄B est un multiple d'un projecteur
    de rang 44 ; contrôle BvLS : BᵀE₋₅B a pour valeurs propres {0, 6}). À P = 0 : graphe signé {0, ±1}, 68-régulier,
    de valeurs propres 17 (×44) et −4 (×187) ;
  - ombres : pour toute étiquette u, q ↦ (ses deux voisins contenant u) est une bijection des 60 paires évitant U
    sur les arêtes de K₁₂ − τ_u. P(u) = 0 dit que l'appariement des droites internes en {u,v} évite τ_u. À P = 0
    (et S = 0), par classe U : 12 droites uūQ, 48 uQQ, 48 ūQQ, 32 QQQ ;
  - fixées localement : les 21 identités de troisième ordre (X²)_{T_U T_U′} = 0 en x (nouvelles coupes possibles pour
    les modèles de paires, sans contradiction à la main).
- 26/09, nuit (correction). notes/123 réécrite après relecture du corpus. Holonomie et prismes (F1, notes/99),
  bijection d'ombre (notes/114 §1) et schéma des droites (Y − 4)(Y + 17) = 0 avec sa forme locale (notes/99 §4,
  notes/109 §4) étaient **déjà connus**. H + 3P = 213 444 est le théorème de Reimbayev. Seul apport nouveau : à P = 0,
  S = 0, H(x) = 12 936 en tout sommet. Leçon : relire 99/109/114 avant d'annoncer une identité sur les droites.
- 26/09, nuit (suite). **Porte I_x à P = 0 : où chercher la prise** (bilan de C1, mathématiques pures).
  - **La fermeture est essentielle.** Les géométries locales « tordues au maximum » existent hors SRG : le graphe des
    arcs de K₅ (t = 2, 20 sommets) et la géométrie t = 3 à 42 sommets ont P(x) = 0 en tout sommet et aucun prisme
    (contrôle exact sur data/). Tout plafond doit donc utiliser que Δ_x est fermé (99 = 1 + 14 + 84).
  - Les relaxations symétriques jusqu'à l'ordre 8 sont faisables à P = 0 (notes/91). Il n'existe donc pas de certificat
    linéaire uniforme à ces niveaux : il faut du non convexe (intégralité au niveau paire, rang 7-adique, dimension
    forcée des supports).
  - **Strates rigides à P = 0, S = 0.**
    - G(L) = M_T est cubique, et ses composantes sont fermées par les appariements internes. Une composante qui ne
      contiendrait qu'une classe par couche forcerait une boucle de τ_u. Chaque composante a donc au moins 12 sommets.
      *(Correction : une version précédente de cette ligne invoquait une « maille ≥ 5 ». C'est faux. À P = 0 et S = 0,
      M_T peut encore avoir des 4-cycles d'holonomie dont l'arête interne est dans la couche de u ou de ū, soit
      σ_U(τ_u(v)) = v ou τ_ū(v) = σ_U(v). Ces coïncidences sont permises : c'est le cas où le second voisin commun de
      {u,v} et {ū,v} est une u-paire ou une ū-paire.)*
    - Profils possibles : connexe, (6,6), (4,8) ou (4,4,4) étiquettes par couche.
    - Cas (4,4,4) : τ_u, τ_ū sont de type D³ à couplage commun des 6 classes, et σ_U préserve chaque paire de classes.
    - Cas (6,6) : type C₃C₃.
    - Dans les trois cas non connexes, l'équilibre (notes/114 §3) fixe la répartition des ombres de chaque lointain :
      les bornes ordonnées d'Astra y deviennent applicables.
  - **Contrainte 7-adique par droite** (rappel, notes/114 §1) : pour d(L) = 1, le rang de recollement de F_L vaut k − 22 ≤ 6
    < 8. Chaque graphe lointain doit donc être 7-spécial. C'est la contrainte connue la plus forte sur les arêtes
    génériques, et elle n'est pas exploitée.
- 26/09, nuit (suite). **Contrôle exact de la formule de notes/102 §8** (demandé avant l'envoi du dossier n° 5 à Astra) :
  rang₇ Q = rang₇ Q_BB + rang₇ R_L, avec R_L[w,w′] = Q_ww′ − 6 + 1_{N_w}ᵀL_G⁺1_{N_w′} et L_G⁺ le pseudo-inverse de
  3I − M_T mod 7 sur 1^⊥.
  - Le test : boule construite à partir d'une donnée locale aléatoire (C, τ_u, τ_ū, σ_U), partie lointaine
    entièrement aléatoire (ombres à 2 points par couche, adjacence lointaine quelconque). 6 tirages sur 6 vérifient
    l'égalité, avec rang Q_BB = 36 = 37 − d(L).
  - Dans un vrai srg(99,14,1,2), cela donne rang R_L = 14 + k − 36 = k − 22 pour d(L) = 1.
  - Script : code/x29e_schur_line_check.py.
- 26/09, nuit (fin). **Strate (4,4,4) de G(L) à P = 0, S = 0** (pas de contradiction pour l'instant).
  - Par partie X_j, il y a 8 configurations locales admissibles pour (τ_u, τ_ū, σ_U) (énumération, code/x29g).
  - Dans toutes, pour tout v ∉ U, le second voisin commun r_v de {u,v} et {ū,v} est une u-paire ou une ū-paire,
    jamais un lointain. σ_U coïncide partiellement avec τ_u ou τ_ū sur chaque partie.
  - Par l'équilibre (2 points d'ombre par composante) :
    - pour s ∈ X_j, τ_s(u^±) ∉ X_j et σ_S(u^±) ∉ X_j ;
    - chaque u-paire {u,v} a 4 voisins lointains de type 1 (une étiquette dans X_j) et 6 de type 0 ;
    - les incidences d'ombre se bouclent exactement (80 = 32 × 1 + 24 × 2).
  - La strate est donc très rigide, mais cohérente aux niveaux 1 et 2. Il faudrait le niveau paire × bloc (doubles,
    bornes ordonnées) pour conclure. Mise en attente.
- 26/09, nuit (suite). **Cycles courts des graphes de droites (notes/125).**
  - Les 4-cycles de G(L) sont de deux types : un Z₂ centré en un point de L (deux événements S), ou le carré d'un
    prisme dont un barreau est une arête de L. D'où **Σ_L c₄(G(L)) = S + 3P**, et Σ_L c₃(G(L)) = 2P.
  - Contrôle exact sur les 3 géométries tordues : 120 = 120, 117 = 3·39 et 336 = 336.
  - À P = 0, S est donc le nombre total de 4-cycles des 231 graphes de droites. Avec S ≤ n₃ (L18) : Σ_L c₄ ≤ 4158.
  - Critère exact de maille ≥ 5 par composante : σ_U évite id, mate, τ_u et τ_ū, plus la condition (c). Énumération :
    96/96 et 46 080/46 080.
  - **Lemme de Klein** : une composante à 4 étiquettes par couche a toujours un cycle de longueur ≤ 4.
  - À P = S = 0 : maille ≥ 5 partout, **profils (4,4,4) et (4,8) exclus**. Reste (6,6), avec 15 types de composantes
    à maille ≥ 5.
  - **Corrections.**
    - La correction b231c36 était elle-même fausse. S est global (L18), et les 4-cycles d'holonomie invoqués sont des
      événements S en u ou en ū. À P = S = 0, la maille ≥ 5 est vraie.
    - La strate (4,4,4) de d7cd060 est vide à S = 0 global. Chaque r_v ∈ P_u ∪ P_ū est un événement S.
    - notes/124 §1 : l'explication de rang₇ Q_BB = 37 − d(L) était fausse. Le quotient donne un bloc de Jordan, et
      c'est 1_L − 1_{N(L)} qui entre dans ker₇ Q_BB. Les nombres étaient justes (contrôle sur 8 boules).
- 26/09, nuit (suite). **(6,6) à P = S = 0 : exploration, non tranché** (mathématiques pures).
  - Équilibre : chaque lointain voit 3 points de chaque composante. Types de colonnes pour C₁ : (1,1,1), au nombre de 24,
    et les 6 permutations de (2,1,0).
  - Lemme E (version |O| = 6) : un lointain intra-couche p a exactement un voisin « de plus » dans la composante.
  - **Orientation.** On compte les « plus » situés dans la couche suivante du cycle x → u → ū → x. Ils sont en même
    nombre t dans chaque couche (a = d = e = t, b = c = f = 12 − t). Pour les deux composantes, **t₁ + t₂ = 12**.
  - Par u-sommet z de C₁ : a_z + f_z + g_z = 6, c_z = 2 − a_z + f_z, d_z = 2 + a_z − f_z, avec |a_z − f_z| ≤ 2.
  - Le type de maille 6 (τ_ū = τ_u, σ involutif, mate ∪ τ ∪ σ = 1-factorisation de K₃,₃) est biparti.
    Mᵀh (h = ±1 par bipartition) est un vecteur propre 2 de A_F, de norme 108. Exactement 6 lointains ont leurs
    3 points de C₁ du même côté.
  - Tous ces comptes sont cohérents. Conclure demande le graphe générique, niveau paire × bloc. **Laissé ouvert.** Même
    tranché, le résultat ne toucherait que la strate P = S = 0.
  - Piste notée : les vecteurs 1_{C_i} − 1_{C_j} sont des vecteurs courts de Λ₃ (normes 24 et 36, contre 42 pour
    (A + 4I)(e_p − e_q)). Un minorant combinatoire de min Λ₃ exclurait les profils non connexes sans hypothèse sur S.
- 26/09, nuit (suite). **L21 raffiné (notes/126), tâche (c′).**
  - 14 + k = (37 − d(L)) + 2r(L) + ρ(L), où r(L) = rang₇ de Mᵀ sur E_L = {φ : couches nulles, L_G φ = 0}. D'où
    **k ≥ 23 − d + 2r = 22 + r − r₀**.
  - Preuve par congruence par blocs : un vecteur du radical de Q_BB qui se couple au lointain apporte un plan
    hyperbolique. Le radical trivial (quotient et 1_L − 1_{N(L)}) est tué par Q_FB.
  - r₀(L) est la dimension des vecteurs propres 3 mod 7 de Γ portés par N(L). Sur Q, ce sont les différences de
    composantes (équilibre par positivité). Mod 7, un vecteur de torsion doit de plus vérifier Mᵀφ = 0.
  - Conséquence : k ≤ 20 impose r₀ ≥ 2 + r sur chaque droite. À P = S = 0, chaque droite doit porter une torsion mod 7
    équilibrée.
  - Contrôle exact : 10 boules dégénérées aléatoires. On trouve r = 1 à chaque fois : la torsion aléatoire n'est jamais
    équilibrée.
  - Tables de τ des composantes (6,6) à maille ≥ 5 (notes/125 §5) : 7 | τ pour σ de type [2,2,2] non biparti et [2,4],
    avec une nullité jusqu'à 4. Le graphe de Pappus en fait partie (τ ≡ 6).
- 26/09, nuit (suite). **À P = S = 0, une droite (6,6) force k ≥ 22** (notes/126 §3 bis).
  - Lemme : aucune torsion mod 7 portée par une seule composante (6,6) n'est équilibrée. Chaque lointain rencontre la
    composante en un triplet admissible, et les paires y sont couvertes exactement λ fois. Test exact : pour chaque
    φ ≠ 0, au moins 20 (dim 1) ou 12 (dim 3) paires sont en défaut, sur les 168 composantes étiquetées avec torsion.
  - Les équilibrés mixtes forment le graphe d'une injection E_{C₁} ⊇ D → E_{C₂}, donc r₀ ≤ 1 + min(t₁, t₂). D'où
    k ≥ 21 + |t₁ − t₂|, donc k ≥ 22.
  - Bilan : P = S = 0 et k ≤ 20 imposent que toutes les droites soient connexes, avec une torsion en majorité
    équilibrée (r₀ ≥ 1 + t/2).
  - Coquille de notes/126 §3 corrigée (signalée par « structures ») : pour une droite connexe, k ≥ 22 + t − 2r₀.
- 26/09, nuit (suite). **Théorème conditionnel (notes/126 §3 quater) : sans torsion équilibrée (NT), k ≥ 18.**
  - Les composantes à 2 étiquettes sont des prismes, car σ(v) = v̄ donnerait K₃,₃. D'où c(L) ≤ 6, et sous NT
    k ≥ 23 − c(L).
  - k = 18 force, en tout sommet, un motif de torsion (2,…,2) sur une réunion de cycles de classes, avec |T_x| ≥ 4
    (L11). Toutes les autres droites sont non tordues (6 prismes). P ∈ [924, 1122] et g(x) ∈ [14, 17].
  - |T_x| = 4, c'est le motif (2,2,2,2) de notes/112 (12 survivants à l'ordre deux). C'est le côté Hamming, où le
    corpus mord : piste pour tuer k = 18.
  - k = 20 force c(L) ≥ 3 sur toute droite. À P = 0, c'est « (4,4,4) partout ».
- 26/09, nuit (suite). **Pistes négatives pour (NT) et (c′)** (exploration, pas une preuve).
  - Sur 3000 boules connexes aléatoires à maille ≥ 5 (P = S = 0), 7 | τ(G(L)) dans 14,9 % des cas. Ce taux est le même
    pour tous les types de cycles de σ (12 à 22 %), c'est-à-dire le taux de Cohen–Lenstra. La 7-dégénérescence d'une
    droite ne se lit donc pas sur l'holonomie : « toutes les droites dégénérées » ne se ramène pas à une statistique
    de σ (`code/x35_tau_vs_holonomy.py`).
  - Reformulations de (NT), sans prise. Une torsion équilibrée φ équivaut à un couple (z₃ ∈ Λ₃, V ∈ Λ₋₄) de vecteurs
    entiers qui coïncident hors de N(L). Explicitement, V = (0, −L_Gφ̃/7, Mᵀφ̃/7) après normalisation. On a aussi
    rang₇ M = 34 − r₀ pour une droite connexe.
  - Tous les tests locaux par paires sont trop faibles pour des ombres de 6 points : (NT) connexe demande un argument
    global.
- 26/09, nuit (suite). **k = 22 sans droite générique** (tâche proposée par « structures », complément de (a′)).
  - Réduction : à k = 22, on a ρ(L) = r₀ − r ≥ 0 sur toute droite. Une droite connexe dégénérée exige donc de la
    torsion équilibrée ; une droite non connexe exige t ≤ c − 1 + 2b.
  - **Sous NT, k = 22 sans générique ⟹ toute droite est non connexe.** À P = 0, chaque droite est (4,4,4), (6,6) avec
    t₁ + t₂ ≤ 1, ou (4,8) avec t ≤ 1. À P = S = 0, c'est (6,6) partout.
  - Piste « trame dans V₃ » : chaque droite non connexe donne ses différences de composantes dans V₃. En (6,6)
    partout, F = Σ f_L f_Lᵀ = 154·E₃ + T, avec F[v,w] = 18 forcé sur les arêtes (6 + 12 droites).
    **Mais c'est automatique** : chaque W_L ⊆ V₃ par l'équilibre, donc F·V₋₄ = 0 et Σ_{arêtes} F = 3·tr F valent
    droite par droite. Pas de contrainte globale de ce côté.
  - « Toute droite non connexe » est donc une question locale : compatibilité, en chaque sommet, des 7 partitions P_U
    avec les τ (τ_a préserve P_A) et les lemmes E de chaque droite. Au niveau des classes, les contraintes laissent de
    la place, car les évènements génériques comblent les « plus ». Il faut le niveau paire × bloc. Non tranché.
- 26/09, fin de nuit. **Rigidité (4,4,4) (notes/128).** À P = 0, si les 7 droites par x sont (4,4,4), alors pour
  c ∈ C et d ∈ D, W = Π_C(D) : {c, τ_c d} est une W-paire dans la composante de c de G(L_W). L'équilibre (2 points par
  composante) interdit alors que le partenaire σ_C de {c, d} soit une W-paire, d'où σ_C(d) = d̄.
  - Tous les σ en x sont donc des réflexions de mates, et S(x) = 84.
  - Deux tels sommets voisins se contredisent : aucun événement S en u n'est porté par L_U, alors que tous le seraient.
  - Conséquences : V₄₄₄ est indépendant (au plus 22 sommets) ; « (4,4,4) partout » est impossible ; **sous NT, k ≥ 22
    à P = 0** ; sans NT, k ≤ 20 à P = 0 impose au moins 26 droites à torsion équilibrée.
  - notes/127 (carte du programme 7-adique) est aussi au corpus.
- 26/09, fin de nuit (suite). **k = 18 exclu sous NT (notes/128 §3 bis), pour tout P.**
  - Dans le motif (2,…,2) de k = 18, c tord D vers W ; la composante à 4 étiquettes {C, W*} de L_W sature y = {c, d}.
  - Un 3-cycle est exclu (d serait un 3ᵉ point).
  - Sinon σ_C = mate sur π(C) en tout sommet. En un voisin u, cela contredit les événements S que la même droite y
    impose (même mécanisme que le corollaire 1).
  - **Bilan sous NT : k ≥ 20 en général, k ≥ 22 à P = 0.** k = 20 à P > 0 reste ouvert : c(L) ≥ 3 partout.
  - « structures » a relu notes/128 (lemme R et corollaires) et notes/126 §3 quater : tout tient. Complément
    ajouté : τ(prisme) = 75 ≢ 0 mod 7.
- 26/09, fin de nuit (suite). **État du cas k = 20 sous NT, P > 0 (ouvert), et réponse à « structures » sur (a′).**
  - k = 20 sous NT impose c(L) ≥ 3 partout, avec ρ(L) = c − 3 − t exactement.
    - Les droites à c = 3, de profils (4,4,4), (2,4,6) ou (2,2,8), ont donc ρ = 0 : leur graphe lointain est fixé mod 7
      par les ombres, comme R_L = 0 pour une droite générique à k = 22.
  - Outils disponibles :
    - composantes prismes = grilles complètes (symétrique), donc 𝒩(x) = graphe de torsion ;
    - saturation des composantes à 4 étiquettes (notes/128) ;
    - lemmes du côté Hamming (D1, lemme 0 de notes/112).
    L'analyse par profils est longue ; laissée ouverte.
  - (a′), réponse à « structures ». Ils ont montré que l'échec de l'étoile tient à une surdétermination (espérance
    ≈ 10⁻¹⁵ solution par boule) plutôt qu'à une identité. J'ai estimé le nombre de boules génériques à τ non carré à
    P = S = 0 : environ 10⁸ classes à symétrie près. Mes lemmes ne contraignent que les droites non connexes ou
    dégénérées, et ne réduisent pas cet espace. Un examen exhaustif n'est donc pas envisageable.
- 26/09, fin de nuit. **Pause du programme 7-adique** (décision de l'utilisateur, relayée par « structures ») : C1 et
  « structures » passent à fond sur la branche de C2 (involution), pour obtenir avec C3 le théorème Aut(Γ) = 1.
  - **État à la reprise** (carte : notes/127) :
    - sous NT, k ≥ 20, et k ≥ 22 à P = 0 (notes/128) ;
    - dernier cas sous 22 : **k = 20 à P > 0** ;
    - verrous : NT pour les droites connexes, (a′) (surdétermination), k = 24 à 28, et « k = 22 sans générique ».
  - **k = 20 à P > 0 (sous NT).**
    - Toute droite a c(L) ≥ 3, avec un profil parmi (2,2,8), (2,4,6), (4,4,4), (2,2,2,6), (2,2,4,4), (2,2,2,2,4)
      et (2⁶). On a ρ = c − 3 − t, donc les droites à c = 3 sont construction-complètes mod 7.
    - Les structures dont toutes les droites sont (2,2,2,2,4) ou (2⁶) tombent déjà : c'est l'argument de k = 18.
    - Outils : relation prisme symétrique (composantes prismes = grilles complètes, 𝒩(x) = graphe de torsion),
      règle 1 (propagation), saturation des composantes à 4 étiquettes, mécanisme « événements S en u », lemmes du côté
      Hamming.
    - Σ_L p_L = (2/3)Σ_x g(x) ≤ P ≤ 1151.
    - À faire : combiner les profils à c ∈ {3, 4}.
- 26/09, soir. **q:7 dans le cadre de C2 (tâche principale, décision de l'utilisateur relayée par « structures » :
  « fini la vérification, place aux paris et aux percées »).** Note : notes/129.
  - Partage : « structures » fait le genre (NOTE_S27) ; C1 fait les minorants de g et les signes locaux.
  - **Côté « structures » (relu et rederivé)** :
    - g = rang₇(S − 3I) est pair et vaut au plus 20 ; g = 22 est exclu par le signe (déterminant exact 7²²) ;
    - g⁺ est pair et au moins 2, et g⁺ + g⁻ = 14 + k.
    - Mon E₋ vaut 42 + M dans leur jauge. Contrôle Paley(9).
    - C2 avait déjà « g pair, forme hyperbolique » (Th. B, B′).
  - **Côté C1 (nouveau)** :
    - g = rang₇(T − 3I), où T est le seul bloc racines × racines.
    - Boule impaire d'une droite-bloc : rang = 6 + rang Q_c, avec Q_c = P_τ − P_η − 2P_π − I ; disc ≡ det Q_c ≡ det L_G⁻.
      Kirchhoff du revêtement double : τ(G) = τ(H)·det L_G⁻/2.
    - L23 dédoublé : g⁻ = 18 ⟹ det Q_c non carré ; g⁺ = 18 ⟹ τ(H_c) carré.
    - Résidu lointain impair : R² = 0, XR = 0 ; structure W_c ⊥ K_c à g = 20.
    - Critère : l'involution meurt ssi Λ_{T,−4} est 7-isotrope.
    - Contrôles exacts sur 3000 boules abstraites (c1_experimental/q7/).
  - **Suite** :
    - C1, à la main : l'étoile complète impaire à g = 18, puis K_c à g = 20.
    - « structures » et C2 : le filtre N_II sur les squelettes à Q entier.
- 26/09, soir (suite). **q:7 : g⁻ ≥ 14 par énumération locale exhaustive ; retour d'Astra (dossier 6).**
  - Astra (relu par « structures ») :
    - min Λ₋₄⁻ ≥ 8 et det L_T = 2¹²·7^{g⁻−7} ;
    - Blichfeldt exclut g⁻ = 8 et 10 ;
    - réserve : exclure 18 et 20 ne suffit que si un Q_c est inversible.
  - C1 : dim ker Q_c ≤ 4 sur TOUS les (τ, η) (11 classes de τ × 10 395 η, code/x36c). Avec g ≥ 18 − t_c, on obtient
    **g⁻ ∈ {14, 16, 18, 20}**.
    - t_c = 4 exige au moins 2 digones de π ∪ τ_c (arêtes sœurs de type m en c).
    - Cas de réserve : à g = 16, au moins 2 vecteurs de torsion impaire équilibrés en chaque bloc ; à g = 14,
      t_c = r₀_c = 4 partout.
  - Envoyé à « structures » (avant cela : filtre des mineurs, L21 impair raffiné, ker T = ⟨b_c⟩, identités impaires
    autour des paires frères, recollement local surdéterminé de 22 à 112). « structures » note que les identités (sint) de
    C2 (note 19) couvrent déjà une partie des identités impaires pour les paires frères partageantes.
  - Le recollement (7 étoiles dans un espace quadratique de dim ≤ 13) est heuristiquement surdéterminé, mais n'est pas
    certifiable à la main : aucun mineur 14 × 14 n'est entièrement connu, et les seuls zéros connus sont des sœurs à
    n_s ∈ {0, 2}.
- 26/09, soir (suite). **g⁻ = 14 exclu** (notes/129 §5 bis).
  - t_c = 4 force η_c sans digone (exhaustif, code/x36d).
  - La cohérence entre étoiles (h(c,d) = m(d,c)) interdit alors t_c = 4 dans les 7 blocs.
  - Donc g⁻ ∈ {16, 18, 20}. g = 16 demande de la torsion impaire équilibrée dans les 7 blocs ; elle n'y est jamais
    rationnelle.
