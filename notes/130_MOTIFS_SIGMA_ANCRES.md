# 130 — Motifs Σ ≠ ∅ de C2 : la famille « ancrée » (lemme de la queue en présence de paires frères)

*26/09, nuit. C1, pièce « motifs Σ ≠ ∅ » (note 42 de C2). Mathématiques ; l'énumération finie des orientations est un
contrôle exhaustif d'un lemme démontré à la main (`c1_experimental/motifs/`).*

## 0. Énoncés
| énoncé | statut |
|---|---|
| Lemme de la queue de C2 (25.1) et T⁺ (« structures ») valent tels quels en présence de paires frères | DÉRIVÉ |
| Famille ancrée d'un motif : blocs non puits de degré sortant ≥ 3, puits deux à deux frères | DÉRIVÉ |
| **Ancrés P₅ et 2P₃ : impossibles** (règle de la queue seule ; preuve à la main pour P₅) | DÉRIVÉ + exhaustif |
| **Ancrés P₃ et P₄ : impossibles** (T⁺ avec graphes D et partitions de Out) | exhaustif, un cas refait à la main |
| Ancrés restants : P₃+K₂ (4 orientations), K₃ (8), 3K₂ (44), 2K₂ (72), K₂ (144) ; ils passent les tests à une racine | exhaustif ; ouvert |

## 1. Cadre
- Motif Σ = ensemble exact des paires frères, σ_k = degré de k dans Σ (≤ 2, lemme des étoiles de C2).
- **Famille ancrée** : chaque paire non frère ij a ses deux orbites appariées « un bloc » par le même bloc (son ancre).
  On oriente j → k si jk est ancrée en k. On note d_k le degré entrant, o_k le degré sortant et w_k = d_k + σ_k,
  de sorte que o_k = 6 − w_k.
- Composantes de G_k : les classes ancrées en k (composantes du graphe D sur In(k)), les partenaires frères (prismes, un
  bloc chacun), et Out(k), qui est une réunion de composantes d'au moins 2 blocs chacune. Une composante réduite à un
  bloc m non frère voudrait dire μ_k = τ_k = σ sur m, donc une paire frère.

## 2. Lemme de la queue, forme « motif »
- **d_k ≠ 1.** Une seule paire ancrée en k serait appariée à elle-même, donc frère.
- Soit X ⊂ ij appariée par le pivot i avec D(X) ⊂ ik (arcs j → i et k → i). L'équilibre de C1 (C2 note 23 §8) en k,
  sur la réunion de composantes Out(k), donne (C2 25.1) : **o_k ≥ 3 + [k → j]**.
  - Out(k) est bien une réunion de composantes : In(k) est stable (classes ancrées) et les partenaires frères sont des
    prismes.
  - Parmi les o_k voisins de x dans C_{Out(k)} figurent l'intérieur de x en i, les deux racines de D(X), et
    l'intérieur en j si k → j.
  - Si jk est frère, [k → j] = 0.
- **Conséquences.**
  - Tout bloc qui a un arc sortant est un bras, donc o ≥ 3.
  - Un puits (o = 0) a toutes ses paires non frères ancrées en lui. Deux puits sont donc frères : **les puits forment une
    clique de Σ**.
  - Un bloc de o = 3 n'est jamais la queue d'une arête D orientée.
  - Valeurs permises de w : σ = 0 → w ∈ {0, 2, 3, 6} ; σ = 1 → {1, 3, 6} ; σ = 2 → {2, 6} ; et Σ_k w_k = 21 + |Σ|.
- **T⁺** (« structures », NOTE_S28) vaut aussi : |S| ≥ 3 + [j ∈ S] + |Π|, où S est la composante de i en k et Π
  l'ensemble des p ∈ S ∖ {i, j} en lesquels {i, k} est une composante de G_p.

## 3. P₅ ancré est impossible (à la main)
Σ = {12, 23, 34, 45}, σ = (1, 2, 2, 2, 1, 0, 0) et Σw = 25.
- Sans puits, Σw ≤ 18. Avec un seul puits, Σw ≤ 22. **Les puits sont donc une paire frère.**
- **Puits {1,2}.** Le compte est exact : w₆ = w₇ = w₅ = 3 et w₃ = w₄ = 2.
  - Donc o₅ = o₆ = o₇ = 3 : aucune arête D entre 5, 6 et 7 au pivot 1, car la queue aurait o = 3.
  - Le graphe D en 1 est 2-régulier sur {3, 4, 5, 6, 7}, avec {5, 6, 7} indépendant. Il faudrait 6 demi-arêtes vers
    {3, 4}, qui n'en prennent que 4. Contradiction.
  - {4,5} est symétrique.
- **Puits {2,3}.** On a w₁ = w₅ = 3, {w₆, w₇} = {3, 2} et w₄ = 2.
  - Au pivot 3 (In = {1, 5, 6, 7}), seul le bloc q ∈ {6, 7} avec w = 2 a o ≥ 4.
  - Toute arête D doit donc avoir q pour queue. Or un 2-facteur (C₄ ou deux digones) sur 4 sommets a une arête sans q.
    Contradiction.
  - {3,4} est symétrique. ∎

## 4. Contrôle exhaustif (`c1_experimental/motifs/anchored_*.py`, `motiflib.py`)
Ordre des tests : orientations de K₇ ∖ Σ ; règle de la queue (§2) avec existence d'un graphe D (2-facteur des paires
permises) en chaque pivot ; puis T⁺ sur tous les choix de graphes D et de partitions de Out(k) ; puis un test à une racine
au niveau paires (zéros de pivot, zéros ancrés, F1, équilibre sur chaque composante), sans couplage entre racines.

| motif | règle de la queue | + T⁺ | + test à une racine |
|---|---|---|---|
| Σ = ∅ (contrôle, C2 Th. 25.3) | **0** | — | — |
| P₅ | **0** | | |
| 2P₃ | **0** | | |
| P₄ | 24 | **0** | |
| P₃ | 48 | **0** | |
| P₃+K₂ | 12 | 4 | 4 |
| K₃ | 80 | 8 | 8 |
| 3K₂ | 44 | 44 | |
| 2K₂ | 84 | 72 | |
| K₂ | 144 | 144 | |

- Les survivants de P₃+K₂ et de K₃ ont leurs puits sur une clique de Σ : {6, 7} pour P₃+K₂, le triangle {1, 3, 5} pour K₃.
- Ils demandent les contraintes couplées de « structures » (dichotomie par paire, symétrie e(P,P′)).
- Un cas de P₃ a été refait à la main : le digone {1,6} forcé en 3 met 3 dans Π pour l'arête D {5,6} au pivot 1,
  d'où 4 ≥ 5, absurde.

## 5. Portée et suite
- Ce n'est que la famille ancrée. Il reste, dans chaque motif, les paires tordues (chaînes, mélanges) et les carrés dis,
  comme pour Σ = ∅.
- Suite proposée à « structures » : le modèle par paires avec couplage sur les survivants ancrés, puis l'extension aux
  paires tordues et dis. La règle de la queue et T⁺ valent pour tout carré « un bloc », tordu compris.
