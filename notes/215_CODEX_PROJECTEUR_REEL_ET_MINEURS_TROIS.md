# 215 — Projecteur réel de rang huit et filtres sur trois ombres

8 octobre 2026. Identité réelle signalée par LAP via LAB, redérivée
ci-dessous ; ajout par Codex des mineurs d'ordre trois contenant
l'apex commun. **Les 473 branches d'apex de la boule cyclique (2,4,1)
sont désormais rejetées par arithmétique exacte et propagation,
sans LP ni recherche de choix.**

La boule était déjà exclue par étoile unique. L'avancée porte sur
la méthode et la justification du rejet : une contrainte réelle
supplémentaire, applicable dans son principe à tout rang, réduit
ici toute la vérification à des filtres locaux et des traces de
suppression. Aucun rang global supplémentaire n'est exclu.

## 1. Identité du projecteur réel

Fixons une droite du SRG hypothétique. On note G son graphe proche
cubique sur 36 points, N l'incidence proche/lointain (36×60), et A_F
l'adjacence des 60 points lointains. Chaque colonne de N a six uns,
deux dans chacune des trois couches ; chaque ligne en a dix.

Les identités entières sont

    N Nᵀ = K = 12I − G − G² + 2J − B,
    N A_F = 2J − (G+I)N,
    A_F² + A_F + NᵀN = 12I + 2J,

où B indique l'appartenance à la même couche. Supposons G connexe,
ce qui est automatique pour nos boules génériques. Soient
H=3I−G et H⁺ son pseudo-inverse **réel**, ici rationnel, pas sa
réduction modulo sept.

Sur V, l'espace de dimension 33 des vecteurs à somme nulle dans
chaque couche, K=H(4I+G) est définie positive. Sur les deux contrastes
de couches, K est nul ; sur la constante j, Kj=60j. Donc rang N=34
et dim ker N=26.

A_F préserve ker N. L'identité quadratique ci-dessus y donne les
valeurs propres 3 et −4. Sur im N, son action transportée est 8 sur
j et −I−G sur V. Puisque tr(G|V)=−3, la trace sur im N vaut
8−33+3=−22. La trace totale de A_F étant nulle, la trace sur ker N
vaut 22. Les multiplicités dans ker N sont donc 18 pour 3 et
**8 pour −4**.

Soit Π le projecteur orthogonal sur ce dernier sous-espace.
A_F−3I+7Π annule ker N et peut s'écrire NᵀRN. On peut prendre

    R = J_36/432 − H⁺.

En effet, sur im N=V⊕⟨j⟩,

    K R = J_36/3 − G − 4I,

ce qui donne précisément l'identité proche/lointain après
multiplication par N. On obtient ainsi

    A_F = 3I + J_60/12 − NᵀH⁺N − 7Π,
    Π Nᵀ = 0.

Par conséquent

    Q := 3I + J_60/12 − A_F − NᵀH⁺N = 7Π

est semi-définie positive de rang huit. En particulier, pour une
ombre n_i et deux ombres distinctes,

    Q_ii = 37/12 − n_iᵀH⁺n_i,
    Q_ij = 1/12 − a_ij − n_iᵀH⁺n_j.

Ces identités réelles ne supposent pas le rang global 37 modulo
sept. En revanche, les pools et les tables utilisés ci-dessous
gardent le cadre générique au rang 37 des notes 211–214, notamment
pour déduire a_ij du produit de Green modulo sept.

## 2. Trois ombres grâce à l'apex commun

L'apex commun w est isolé dans l'union des deux étoiles : ses
adjacences avec les 18 ombres privées sont connues et nulles. Tous
les coefficients du mineur Q sur {w,i,j} sont donc déterminés par
deux candidats, sans choisir une troisième ombre variable.

On exige successivement :

1. Q_ii≥0, y compris pour w ;
2. Q_ww Q_ii−Q_wi²≥0 pour chaque candidat ;
3. Q_ii Q_jj−Q_ij²≥0 pour chaque couple compatible ;
4. det Q_{w,i,j}≥0 pour chaque tel couple.

Les trois premiers types contrôlent tous les mineurs principaux
d'ordre un et deux du bloc 3×3 ; le quatrième termine exactement
le test de positivité semi-définie de ce bloc.

Si Q_ww>0, le dernier test peut aussi se lire

    (Q_ij Q_ww − Q_iw Q_jw)²
       ≤ (Q_ii Q_ww − Q_iw²)(Q_jj Q_ww − Q_jw²).

C'est le test 2×2 après élimination de l'apex. Le complément de
Schur complet serait PSD de rang au plus sept. Le code utilise
directement le déterminant polynomial, sans division, et traite
donc aussi le cas Q_ww=0.

## 3. Calcul exclusivement rationnel ou entier

`two_star_real_projector.exact_green` calcule

    H⁺ = 36(36H+J)⁻¹ − J/36.

Il vérifie exactement H H⁺=I−J/36, H⁺j=0, la symétrie, la réduction
modulo sept vers le Green déjà employé, et tr(H⁺K)=129.

Sur la boule cyclique (2,4,1), le dénominateur commun réduit est
d=8 128 080. En écrivant H⁺=M/d avec M entière, les coefficients
de 12dQ sont les entiers

    q_ii = 37d − 12 n_iᵀM n_i,
    q_ij = d(1−12a_ij) − 12 n_iᵀM n_j.

Le déterminant utilisé est

    q_ww q_ii q_jj + 2 q_wi q_wj q_ij
    − q_ww q_ij² − q_ii q_wj² − q_jj q_wi².

Tous ces produits sont des entiers Python à précision arbitraire.
Un contrôle séparé sur 120 triplets a reconstruit directement la
matrice rationnelle 3I+J/12−A−NᵀH⁺N, puis comparé sa matrice
entière mise à l'échelle et son déterminant aux formules du filtre.

## 4. Contrôle des deux branches 0 et 33

On repart des pools unaires initiaux de la note 211 et des filtres
entre un candidat et w. Entre les 18 ombres privées, le mode
`green` impose seulement le produit de Green 2 ou 3 avant les
nouveaux tests réels. Il n'incorpore ni intersection, ni capacité,
ni saturation, ni plafond K entre ces 18 ombres.

Les filtres réels sont appliqués **avant** toute propagation. Les
sommes ponctuelles et les tables ainsi obtenues servent ensuite
au propagateur et au replay exact de la note 212.

| Branche | Après les filtres unaires réels | Couples avant/après PSD 2×2/après PSD 3×3 |
|---|---:|---|
| 0 | 639 candidats | 54 717 / 32 922 / 25 370 |
| 33 | 751 candidats | 76 121 / 43 985 / 35 625 |

Les filtres limités aux paires, avec leurs sommes exactes, laissent
la propagation ouverte : 562 candidats pour la branche 0 et 637
pour la branche 33. Ce n'est pas une affirmation de faisabilité
des modèles correspondants.

L'ajout des mineurs 3×3 fait vider un domaine : 248 événements de
suppression pour la branche 0, 359 pour la branche 33. Aucun LP
n'est nécessaire à ces deux contradictions.

## 5. Les 473 apex de la boule cyclique

Le balayage exhaustif donne :

| Étape | Branches exclues |
|---|---:|
| Diagonale réelle négative de l'apex | 14 |
| Tables privées `green` + PSD 3×3 + propagation | 428 |
| Pour les survivants : tables privées `full` + PSD 3×3 + propagation | 31 |
| Total, sans recouvrement des exclusions | **473/473** |

La première passe laisse 31 branches, et la seconde les rejette
toutes. Les tables `full` sont celles de la note 214 ; elles sont
reconstruites depuis les pools initiaux, avec les filtres réels,
puis la propagation est refaite. Il n'y a ni choix d'ombre par
recherche, ni solveur LP/CP dans ces balayages.

À comparer au contrôle de LAB sans les filtres réels : les seules
tables combinatoires complètes et la propagation laissaient 213
branches ouvertes sur cette même boule. La combinaison des deux
familles de contraintes rend ici la propagation suffisante partout.

Chaque trace est rejouée pendant la production. Les traces complètes
et la géométrie de chaque branche sont archivées en JSONL compressé
(environ 685 ko pour les deux archives). Les fichiers de résumé
donnent leurs SHA-256 et les listes exactes de branches :

- `data/codex_real_green_triples_cyclic_sweep.json` et son archive
  `.proofs.jsonl.gz` : les 473 branches de la première passe ;
- `data/codex_real_full_triples_cyclic_survivors.json` et son archive :
  les 31 survivants traités avec les filtres complets ;
- `data/codex_real_cyclic_coverage.json` : contrôle que l'union des
  exclusions est exactement {0,…,472}.

Les deux archives finales ont ensuite été intégralement relues
depuis le disque : 473 enregistrements de première passe et 31
de seconde passe, tous revérifiés, en environ 209 et 19 secondes.

## 6. Reproduction et portée

Les deux replays complets, sans optimisation, sont :

    python code/codex/two_star_real_sweep.py --out data/codex_real_green_triples_cyclic_sweep.json --verify-only
    python code/codex/two_star_real_sweep.py --out data/codex_real_full_triples_cyclic_survivors.json --verify-only

Un contrôle individuel :

    python code/codex/two_star_real_projector.py --out data/codex_real_green_triples_000.json --verify-only

Le premier balayage peut être reproduit avec `--seconds 240`.
`--start`, `--max-apex` ou `--indices` permettent un traitement
borné ; un résultat partiel n'est jamais annoncé comme exclusion
complète. Les deux scripts acceptent aussi un JSON `adjacency`
36×36 et des centres `--u`, `--v`.

La géométrie réelle fournit donc un renforcement exact et efficace
du mécanisme combinatoire. Il reste à établir une obstruction
valable pour toutes les boules admissibles : ce balayage complet
d'un exemple connu ne donne pas une obstruction uniforme pour le cas C1.
