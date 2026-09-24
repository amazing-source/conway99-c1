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
