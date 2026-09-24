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
