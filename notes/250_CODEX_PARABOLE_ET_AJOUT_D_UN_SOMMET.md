# 250 — Transformer la parabole entière en filtre d'extensions

9 octobre 2026. Exploitation du lemme A de LAP, reçu au message522.

**Résultat Codex.** L'inégalité de LAP sur un support augmenté d'un sommet
se calcule à partir du support initial par une formule quadratique simple.
Le coefficient entier du nouveau sommet s'optimise exactement en deux
essais. Sur le support4, un petit ensemble de poids élimine **1689 des
24602 voisinages candidats**, laissant22913, sans solveur. Le support4
lui-même n'est pas déclaré exclu.

## 1. Réduction de supports annoncée par LAP

LAP rapporte941 supports exclus parmi les4581 ouverts par ses lemmes A
(parabole entière) et B (plafond de voisins communs). Source annoncée :
`conway99-c2-aws`, commit `a7667ddbb`, dossier
`c1_mandat_c_transformations/p3n25_search/`, section17 de sa note.
Les fichiers sont `lemma_witnesses.jsonl`, `check_witnesses.py`,
`parabola.py`, `caplemma.py`. Ce calcul n'est pas reproduit ici.

| delta | Supports initiaux | Exclus par A ou B | Restants |
|---|---:|---:|---:|
| 3 | 209 | 82 | 127 |
| 4 | 496 | 155 | 341 |
| 5 | 914 | 229 | 685 |
| 6 | 1155 | 206 | 949 |
| 7 | 1054 | 180 | 874 |
| 8 | 596 | 73 | 523 |
| 9 | 157 | 16 | 141 |
| Total | 4581 | 941 | 3640 |

LAP donne687 supports avec témoin A et413 avec témoin B ; leur union
est941, donc159 appartiennent aux deux listes. Il annonce1100 témoins
contrôlés par les formules entières. Parmi les301 exclusions de son
balayage LP à cette date,300 figurent dans cette union ; l'exception est
4656. Les anciennes exclusions LP ne doivent donc pas être additionnées
aux941 comme si elles étaient disjointes. Le tableau porte uniquement
sur l'union des deux lemmes, pas sur le bilan final du balayage.

## 2. Parabole entière de LAP

Pour un support induit S, écrire A pour son adjacency, w un vecteur
entier sur S et a un entier. Pour y hors S, poser t_y=sum_{s~y}w_s.
L'identité du SRG donne

    Phi_S(w,a) = w^T(12I+2J-A-A^2)w
                -(2a+1)(14 sum(w)-1^T A w)
                +(99-|S|)a(a+1)
              = sum_{y hors S}(t_y-a)(t_y-a-1) >=0.        (1)

La positivité vient de l'intégralité de t_y. Le lemme vaut pour tout
support induit, pas seulement P3/N25. Il fournit l'entrée mathématique
de la nouvelle déduction ci-dessous.

## 3. Formule pour ajouter un sommet

Considérer un sommet extérieur z dont le voisinage dans S serait B,
et b=1_B. Définir

    d=14-|B|,
    r=2*1-b-A b,
    t=w^T b,       s=w^T r.

Le nombre d est le nombre de voisins de z hors S union {z}, et r_i
le nombre de voisins communs de i et z hors de ce support augmenté.
Pour tout entier h placé en coordonnée z,

    Phi_(S+z)((w,h),a)
      = Phi_S(w,a)-(t-a)(t-a-1)
        +2h*s+d*h*(h-2a-1).                              (2)

Preuve : retirer de (1) le terme du sommet z. Pour chaque autre sommet
extérieur y adjacent à z, remplacer t_y par t_y+h. La somme de ces
t_y vaut s, et leur nombre est d. Développer la parabole donne (2).
Cette démonstration ne dépend pas du pilote informatique.

Pour d>0, le membre droit est une parabole convexe en h. Son minimum
sur tous les entiers est atteint en l'un des deux entiers

    h0=floor(((2a+1)d-2s)/(2d)),       h0+1.               (3)

Si ce minimum est négatif, le bloc B est interdit. Cela évite une
recherche supplémentaire sur le poids du sommet ajouté. Dans P3/N25,
les blocs ont4,6,8 ou10 sommets, donc d>0 est toujours satisfait.

Le seul choix h=0 donne déjà le budget nécessaire

    (w^T b-a)(w^T b-a-1) <= Phi_S(w,a).                   (4)

Plus généralement, pour plusieurs sommets extérieurs distincts aux
blocs B_i, la somme des termes de gauche de (4) est au plus Phi_S.
C'est une conséquence directe de (1), à utiliser sans compter plusieurs
fois un même sommet. Si Phi_S=0, chaque bloc réalisé doit donc vérifier
w^T b dans {a,a+1}.

## 4. Petit pilote sur le support4

Le programme `code/codex/p3_n25_parabola_extension.py` reprend ce support
du registre existant et ses24602 colonnes satisfaisant les déficits de
paires, les plafonds lambda/mu et la capacité triangulaire de note248.
Il ne lance aucun LP et ne régénère aucun support.

L'ensemble de76 poids contient les vecteurs unité, les indicatrices de
voisinages ouverts et fermés dans S, ainsi que les sommes et différences
de deux Q_p={p} union N_N(p). Pour chaque poids, trois valeurs de a sont
testées autour de la moyenne (14 sum(w)-1^T A w)/71. Ce choix de poids
et de a est exploratoire, pas exhaustif. Pour chaque couple retenu,
l'optimisation (3) parcourt implicitement TOUS les entiers h.

Le calcul entier supprime1689 colonnes et en conserve22913. Les
premières exclusions proviennent de seulement six couples de poids :

- w=1_Qp,a=1 pour chacun des trois p :542 nouvelles colonnes chacun ;
- w=1_Qp+1_Qq,a=2 pour chacune des trois paires :21 nouvelles chacune.

Exemple : B={0,5,8,11,12,14}, w=1_Q0, a=1, Phi_S=4. Le choix h=1
donne Phi_(S+z)=-4, donc ce bloc est impossible.

Un témoin de chaque famille a été évalué directement par (1) sur la
matrice augmentée de taille29, avec accord exact avec (2). La liste des
blocs supprimés et les familles de témoins sont sauvegardées dans
`data/codex_p3_n25_parabola_extension.json`. La commande a pris0,84s
dans l'environnement local ; ce temps n'est pas extrapolé aux4581 cas.

Ce sont des exclusions de colonnes supplémentaires, pas de nouveaux
supports ni de rangs. Le filtre et sa formule ont été transmis au pont
(message523). Le calcul LP/entier des supports reste à LAP et n'est pas
dupliqué dans cette note.
