# Audit Codex — campagne asymétrie / Conway, 12 octobre 2026

**Périmètre figé :** `claude/v7-simultaneous`, commit
`640ffe11182aed996b9f5a70514f38c4d0f77fc9`, et dépôt public
`amazing-source/strongly-regular-graphs-research`, commit `a4237a9`.
Examen des résultats principaux des notes 159 et 165–178 ; ce document
ne certifie pas tous les programmes et toutes les recherches historiques.
Les conclusions ci-dessous ont été rédigées avant de lire les conclusions
de l'examen indépendant de LAB. Aucun ancien calcul de rang n'a été relancé.

**Verdict : les trois graphes supplémentaires sont des objets mathématiques
effectifs, deux à deux non isomorphes et distincts de BvLS.** Les quatre
graphes déposés ont encore des automorphismes non triviaux. Plusieurs
réductions théoriques sont exploitables à 99, sous leurs hypothèses ; les
passages « parité ⇒ revêtement complet ⇒ asymétrie » ne sont pas établis.

## 1. Les quatre graphes : résultat indépendant achevé

Le programme `code/codex/audit_asymmetry_20261012.py` ne dépend pas de la
bibliothèque de graphes de la campagne. Il lit les listes d'arêtes et contrôle
les 29 403 paires de sommets de chaque graphe, ainsi que l'identité entière

\[
A^2+A=20I+2J.
\]

Pour les automorphismes, il utilise **BLISS** via igraph, puis Schreier–Sims
sur les générateurs retournés, chacun contrôlé sur la matrice. Il s'agit
donc d'un calcul du groupe complet par un moteur différent du nauty de la
campagne, pas seulement du groupe engendré par les générateurs déposés.
Le décompte des grilles construit explicitement leurs neuf positions et
contrôle leurs 36 paires.

| Graphe | Paramètres | Ordre du groupe complet | Orbites sur les sommets | Grilles 3×3 | Paires de triangles à deux arêtes | Prismes |
|---|---|---:|---|---:|---:|---:|
| BvLS | (243,22,1,2) | 3 849 120 | 243 | 1 485 | 0 | 8 910 |
| Jumeau Γ′ | (243,22,1,2) | 4 320 | 3, 60, 180 | 405 | 19 440 | 2 430 |
| Γ₃ | (243,22,1,2) | 864 | 27, 108, 108 | 621 | 14 256 | 4 158 |
| Γ₄ | (243,22,1,2) | 3 888 | 81, 162 | 837 | 9 720 | 5 670 |

Les quatre nombres de grilles distincts suffisent à prouver les six
non-isomorphismes. Les trois graphes supplémentaires ne sont pas transitifs
sur les sommets. Aucun n'est asymétrique. Les empreintes des fichiers et les
résultats détaillés sont dans `data/codex_asymmetry_audit_20261012.json`.

**Situation bibliographique au 12 octobre.** La
[table de Brouwer](https://aeb.win.tue.nl/graphs/srg/srgtab201-250.html)
mentionne désormais la non-unicité pour (243,22,1,2), avec l'attribution
« Djematene + AI ». Sa
[bibliographie](https://aeb.win.tue.nl/graphs/srg/srgtabrefs.html)
renvoie au préprint d'octobre 2026 de Dilan Djematene. La phrase historique
de la note 159 indiquant que la table ne connaît que BvLS est donc dépassée.
Cette référence extérieure documente la réception du résultat ; elle ne
vaut pas audit de toutes les autres affirmations du dossier ni recherche
exhaustive de priorité.

## 2. Réductions théoriques utilisables

Les statuts de ce tableau portent sur les arguments indiqués, pas sur une
nouvelle exclusion globale de C1.

| Énoncé | Appréciation et portée |
|---|---|
| Chirurgie spectrale et critère de rigidité, note 165 §1 | Argument valable. À paramètres fixés, une modification dans F×F ne peut agir que dans les espaces propres supportés par F. Si l'un des deux espaces propres non principaux supportés est nul, la complétion est unique. |
| Aucun étalement régulier en triangles à 99, note 165 §3 | Valable. Le quotient devrait être (33,12,1,6), avec une multiplicité 180/7. Cela exclut cette structure dans tout graphe de Conway. |
| Partitions équitables à cellules de même taille et même degré interne | À 99, seules restent les formes 3×33 de degré interne 2 et 11×9 de degré interne 4. L'existence d'une telle partition n'est pas forcée. Les partitions de tailles ou degrés différents ne sont pas couvertes. |
| Alignement total des grilles impossible à 99, note 168 | Valable dans le sous-cas 11×9 : si tous les couplages sont des isomorphismes de grilles, une multiplicité devrait valoir 88/7. Les couplages vrillés restent possibles. |
| Reformulation avec une coclique de Hoffman de taille 22, note 171 §5 | Les équations de design et de complétion sont exactes. Elles concernent le sous-cas α=22 et ne prouvent pas l'existence obligatoire d'une telle coclique. |
| Connexité du graphe auxiliaire G∪M, note 173 | L'argument de Laplacien positif puis de parité est valable, sous l'hypothèse de la coclique de Hoffman. La conjecture K₇ plus forte reste ouverte. |
| Mots binaires de ker₇(A+4I), note 178 | La réduction aux poids 0, 63 et 77 est valable ; les petites contraintes de moments ont été recalculées exactement. Rien ici ne force un mot binaire non nul. |
| Lois empiriques de motifs, balance, conjectures G/E/L/P | Points de départ pour l'exploration, pas théorèmes couvrants. Les quatre exemples à 243 sont apparentés. |

Deux précisions simplifient la réutilisation de ces résultats.

**Partition 11×9.** Un sous-graphe induit 4-régulier sur neuf sommets est
nécessairement une grille. Pour un sommet fixé, les chemins de longueur deux
vers les huit autres sommets sont au nombre de 4·3=12. Les quatre voisins
en autorisent au plus 4·1 et les quatre non-voisins au plus 4·2. Toutes ces
bornes sont donc saturées : le sous-graphe est lui-même un SRG(9,4,1,2),
c'est-à-dire la grille. Toute paire de ses sommets a déjà tous ses voisins
communs internes ; un sommet extérieur ne peut en toucher deux. Dans une
partition en onze telles cellules, les liaisons sont donc des couplages
parfaits. La classification par trace peut ainsi être suivie directement
d'un modèle en permutations, sans énumérer des graphes internes.

**Poids binaires.** Si w=7t, les deux identités de moments de la note 178
imposent

\[
v_7=2t(11-t),\qquad u+2v_{14}=t(2t-11).
\]

Avec les bornes de population, les seules possibilités sont
`(w,u,v7,v14)=(0,0,0,0),(63,63,36,0),(77,77,0,22)`.
Le poids 77 équivaut à une coclique de Hoffman de taille 22 par complément.
Le poids 63 donne une autre partition équitable. Pour utiliser cette route
comme exclusion de C1, il reste notamment à forcer un mot binaire non nul,
ou à exploiter autrement l'absence des deux types. Un énumérateur de poids
ordinaire d'un code sur F₇ ne voit pas la restriction aux coordonnées 0 et 1.

## 3. Parité, relèvement et asymétrie : deux implications manquantes

La **note 175** donne une formulation exacte du revêtement : pour la
représentation standard de S₃,

\[
A_\rho^2=A_\rho+20I.
\]

Elle distingue correctement la condition nécessaire obtenue sur les signes.
Il faut reporter cette distinction dans la conclusion de la note 165 §6 et
dans « SAT ⇒ un S₃-revêtement existe » de la note 167 §6.

Pour une paire non adjacente de BH, les six permutations de chemins doivent
avoir pour somme de matrices **2J**. Il existe exactement trois multisets
possibles : chaque élément de A₃ deux fois, chaque permutation impaire deux
fois, ou chaque élément de S₃ une fois. Le test de parité ne conserve que le
nombre de chemins impairs, qui doit être 0, 3 ou 6.

Ce test perd de l'information : six permutations identité ont zéro chemin
impair, mais leur somme est 6I, pas 2J. Cet exemple local montre que le test
de signes n'est pas l'équation complète ; il ne constitue pas un
contre-exemple global à un éventuel théorème de relèvement des signings de BH.
**Un tel théorème manque dans les notes examinées.** Un UNSAT d'une relaxation
nécessaire peut exclure les revêtements ; un SAT de cette relaxation demande
encore un relèvement.

On peut formuler précisément l'étape suivante. Écrire les gains

\[
g_{xy}(t)=s_{xy}t+b_{xy},\quad s_{xy}\in\{1,-1\},\quad b_{xy}\in\mathbf F_3.
\]

Après avoir fixé les signes, il reste à trouver les translations b, avec
holonomie identité sur les triangles. Pour les six chemins d'une paire non
adjacente :

- si les six signes sont égaux, les translations 0,1,2 doivent apparaître
  chacune deux fois ;
- si les signes se répartissent en 3+3, les translations 0,1,2 doivent
  apparaître chacune une fois **dans chacune des deux classes de signe**.

Ces contraintes constituent un objectif de relèvement concret, plus précis
que « trouver un signing non trivial ». Le petit contrôle exact des trois
multisets est archivé dans `data/codex_asymmetry_local_checks_20261012.json`.

**Deuxième implication.** Même un revêtement de monodromie S₃ ne serait pas,
par ce seul fait, asymétrique. Son groupe d'automorphismes fixant chaque
fibre est trivial. Un stabilisateur d'étalement qui est un 2-groupe peut
encore être non trivial ; des automorphismes peuvent aussi déplacer
l'étalement. « Génériquement asymétrique » est ici une intuition de recherche,
pas un théorème. Les exclusions informatiques de symétries impaires de la
note 165 sont conservées comme résultats rapportés, sans répétition de leur
campagne SAT dans cet audit.

Le modèle de translations `t↦t+b` impose au contraire l'automorphisme global
`t↦t+1`. Le programme `stabcover.py` garde explicitement cette translation
dans K. Ce modèle peut produire de nouvelles classes, mais ne peut jamais
atteindre |Aut|=1. C'est une limite structurelle, indépendante du temps CPU.

## 4. Extension de la formule des grilles aux gains S₃

La preuve de la note 165 §5 utilise explicitement des gains dans Z₃. Son
énoncé doit porter cette hypothèse, ou être remplacé par la formule suivante.

**Proposition.** Pour tout SRG(243,22,1,2) muni d'un étalement régulier et
représenté sur BH, notons Mon(H) la monodromie restreinte à une grille H de
BH, agissant sur les trois points d'une fibre. Alors

\[
\#\mathrm{grilles}(\Gamma)
=270+\sum_{H\text{ grille de BH}}|\mathrm{Fix}(\mathrm{Mon}(H))|
=270+3n_1+n_{C_2}.
\]

Ici n₁ compte les grilles de monodromie triviale et n_C₂ celles dont la
monodromie est engendrée par une transposition. A₃ et S₃ ne contribuent pas.

*Preuve.* Une grille contenant deux sommets d'une fibre contient aussi le
troisième, puisque leur arête a son triangle unique. Prenons cette fibre
pour une ligne de la grille. Les trois sommets d'une ligne parallèle sont
soit dans une seule fibre, soit dans trois fibres distinctes : le cas deux
plus un contredirait encore l'unicité du triangle. Trois fibres distinctes
donneraient un triangle de BH dont les trois sommets sont voisins de la
première fibre, donc un K₄ dans BH, impossible puisque λ=1. Les deux lignes
parallèles sont donc elles aussi des fibres. Chaque triangle de BH fournit
une telle grille, soit 81·20/6=270.

Toute autre grille se projette injectivement. Son image ne peut avoir de
corde : une paire non adjacente de la grille a deux voisins communs internes
distincts, dont les images contrediraient λ=1 si la paire devenait adjacente.
L'image est donc une grille induite de BH. Ses sections sont en bijection
avec les points de la fibre de départ fixés par toutes les holonomies. Les
sous-groupes de S₃ ont respectivement 3,1,0,0 points fixes pour 1,C₂,A₃,S₃,
ce qui donne la formule. ∎

Elle retrouve `270+3n₁` pour les revêtements Z₃ existants. Pour un éventuel
revêtement S₃, les grilles de monodromie C₂ apportent **une** section, pas
trois. Ce terme ne doit pas être perdu dans les futurs invariants.

## 5. Deux autres corrections de portée

**Monodromie avec des fibres portant une structure interne (note 167 §1).**
Le centralisateur seul décrit les automorphismes au-dessus de l'identité du
quotient si toute permutation de fibre est autorisée, notamment pour K₃.
Avec des fibres-grilles et des couplages non alignés, il faut également
préserver chaque graphe interne transporté. Pour des transports d'arbre T_v
depuis une fibre de référence, le groupe exact est

\[
C_{\mathrm{Sym}(F)}(\mathrm{Mon})\ \cap\
\bigcap_v T_v^{-1}\mathrm{Aut}(F_v)T_v.
\]

Un centralisateur trivial suffit toujours à prouver ce groupe trivial.
Cela ne calcule toujours pas le groupe complet du graphe.

**Balance et spectre (notes 168–170).** La symétrie du spectre apparié autour
de son centre implique l'annulation de la somme des cosinus ; la réciproque
ne découle pas d'une simple somme nulle. Le « de façon équivalente » de la
note 169 §1 nécessite donc une hypothèse supplémentaire. La note 170 apporte
une structure plus précise, attachée au quotient triparti K₉,₉,₉. Elle laisse
explicitement ouvert le lemme qui placerait tout le spectre d'α sur le bord
du triangle. On ne peut transférer sa graduation tripartie au quotient K₁₁.

La symétrie ± du spectre de M sur Z, note 168 §3, se répare simplement :
les plans appariés contribuent déjà par paires opposées. Poser d₂ et d₅ les
différences de multiplicités aux extrémités ±2 et ±5. L'égalité dim R=dim S
donne d₂=d₅, et tr(M|Z)=0 donne 2d₂+5d₅=0. Donc d₂=d₅=0. La trace carrée
sur Z est **880**, tandis que 990 est celle de M sur les 99 sommets ; le
quotient apporte 10²+10=110. Le résultat reste valable, avec cette preuve.

## 6. Hoffman, Paley et dossiers absents

La recherche a trouvé le dépôt public
[strongly-regular-graphs-research](https://github.com/amazing-source/strongly-regular-graphs-research),
ses manuscrits, les quatre graphes et une coclique de Hoffman explicite de
BvLS. Elle a aussi examiné les branches récentes du dépôt C1 et les arbres
des dépôts connexes `conway99-structures-lab`, `conway99-c2-researcher2` et
`conway99-c2-aws`. Les dossiers complets Paley(25), reconstruction BvLS et
`HOFFMAN_UPDATE` cités comme externes n'ont pas été localisés. La branche
Astra `astra/bvls-boundary-release-20261011` apporte surtout un fichier de
coordination ; elle ne fournit pas ces dossiers.

Il faut distinguer trois niveaux :

- L'existence classique de quinze SRG(25,12,5,6), dont deux asymétriques,
  est documentée par [Cohn et al., *Point configurations that are asymmetric
  yet balanced*](https://arxiv.org/abs/0812.2579). La nouveauté possible de
  l'expérience Paley porte sur la reconstruction par un bord fixé, pas
  sur la première existence de ces graphes.
- Les comptes annoncés de complétions Paley, les 27 648 matrices du bord
  BvLS élargi et les exclusions de designs à actions Z/22 ou d'ordre 21
  restent des **résultats rapportés**, faute de dossiers complets examinés.
- Pour le bord de Hoffman de BvLS effectivement disponible, la coclique de
  taille 45 et l'identité `YYᵀ=20I+2J` ont été contrôlées. Le modèle de
  domaines puis d'assemblage de la note 171 est cohérent avec les équations.
  L'unicité annoncée de la complétion n'a pas été reproduite ici.

Un pilote borné de cette dernière reproduction a atteint sa limite de
45 secondes sur le premier représentant de ligne. Il a été arrêté, sans
relance. Aucun domaine complet ni compte de complétions n'en résulte. Le
statut est conservé dans
`data/codex_hoffman_boundary_audit_20261012/run_status.json`. Les 38 826
candidats de la note 171 sont des **lignes candidates**, pas 38 826 graphes.

L'erratum de cette même note est essentiel : l'unicité pour **un** design de
BvLS ne prouve pas que toute coclique de Hoffman impose la symétrie. Le
lemme d'extension des automorphismes du design aux complétions est valable ;
il relie symétrie et multiplicité des complétions sans les confondre.

## 7. Conséquences pour la suite

Le gain acquis de cette campagne est une famille effective d'au moins quatre
classes à 243, avec une description de plusieurs mécanismes de recollement
et de rigidité. Le travail à 99 reçoit des contraintes uniformes : absence
d'étalement régulier, vrillage obligatoire dans le sous-cas des grilles,
structure du sous-cas α=22 et restriction des mots binaires modulo 7.

Les prochains obstacles doivent être nommés avant de lancer un calcul :

1. Pour S₃, démontrer une obstruction aux signings admissibles, ou résoudre
   leur relèvement en translations ; puis traiter séparément le groupe
   complet du graphe obtenu. La parité seule ne clôt pas la construction.
2. Pour les grilles à 99, obtenir une contrainte nouvelle au-delà des
   identités de blocs, ou un théorème forçant la partition. Une exclusion
   du sous-cas 11×9 resterait conditionnelle à cette structure.
3. Pour Hoffman, exploiter les designs et leur géométrie couplée aux
   complétions, sans supposer α=22 forcé ni symétrie du design obligatoire.

Ces distinctions évitent de transformer une limite du procédé de
construction en propriété de tous les SRG. Aucun calcul supplémentaire de
validation des quatre graphes n'est nécessaire pour partir de leurs
conséquences. Cet audit ne prouve ni l'inexistence de C1, ni la classification
complète à 243, ni l'existence d'un graphe asymétrique à 243.

## 8. Reproduction des contrôles achevés

Depuis la racine du dépôt, avec Python, numpy, sympy et igraph :

```text
python code/codex/audit_asymmetry_20261012.py
python code/codex/audit_asymmetry_local_identities.py
```

Le second programme utilise seulement la bibliothèque standard. Le premier
accepte `--deps CHEMIN` si igraph est installé dans un dossier isolé. Les
sorties JSON sont déposées avec ce rapport. Le pilote Hoffman, distinct,
est fourni pour traçabilité et porte explicitement le statut incomplet ;
il ne fait pas partie des vérifications déclarées achevées.
