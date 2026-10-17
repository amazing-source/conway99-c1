# 259 — Deux chemins de transport dans les quatre attaches à coupure de poids deux

10 octobre 2026. Suite exploratoire des notes 257–258.

**Portée.** Les quatre attaches cas 3, orbites 0, 1, 21, 22 imposent une
même décomposition : sur 46 simples, les arêtes dont le triangle a son
troisième sommet dans le cœur forment exactement deux chemins, avec
éventuellement des cycles supplémentaires. En ajoutant deux doubles
précis et leurs quatre arêtes de transport, on obtient des cycles pairs
sur 48 sommets. C'est une conséquence structurelle, sans hypothèse de
rang. Elle ne ferme aucune des quatre attaches.

## 1. Deux doubles avec un triangle manquant de chaque côté

On conserve P,Q,D,B,Z des notes précédentes. D est indépendant. La
coupure D=U∪V de la note 257 impose à tout simple au plus un voisin dans
chaque partie. Les quatre attaches ont les caractéristiques suivantes,
obtenues directement de leurs huit ombres de taille quatre :

| Attache | Doubles particuliers | Incidences cœur-double dont le triangle n'est pas déjà dans le cœur+D |
|---|---|---|
| 0, 1 | d1, d2, tous deux dans U | (P3,d1), (Q4,d1), (P2,d2), (Q3,d2) |
| 21, 22 | d2, d3, tous deux dans V | (P1,d2), (Q3,d2), (P3,d3), (Q0,d3) |

Les indices commencent à zéro. Six doubles ont deux arêtes disjointes
dans leur ombre ; les deux doubles du tableau ont une seule arête
dans leur ombre. Dans chacun de ces deux cas, les deux sommets non
couverts par cette arête sont un sommet de P et un sommet de Q,
non adjacents entre eux.

Chaque incidence du tableau exige un troisième sommet de triangle dans
B : il n'est pas dans le cœur par construction, ni dans D puisque D
est indépendant, ni dans Z puisque Z ne touche pas le cœur.

Ces quatre partenaires dans B sont distincts. Un partenaire commun aux
deux incidences d'un même double donnerait deux voisins communs à une
arête D-B. Un partenaire commun aux deux doubles particuliers toucherait
deux doubles du même côté de la coupure, interdit par la note 257.

## 2. Décompte des simples et preuve des deux chemins

Le cœur a 32 arêtes entre P et Q. Les doubles en portent 14 triangles :
six fois deux, plus deux fois un. Chaque autre arête du cœur porte son
triangle avec un simple. Il y a donc 18 simples dont les deux voisins
dans le cœur sont adjacents, et 46 dont les deux voisins ne le sont pas.

Pour un simple b dont les voisins p,q du cœur sont adjacents, le
triangle bpq fournit déjà les partenaires de bp et bq. Il ne participe
à aucune arête B-B dont le troisième sommet du triangle soit dans le
cœur.

Pour chacun des 46 autres simples, l'arête bp a un partenaire unique
dans D ou B ; il en est de même de bq. Ces deux partenaires sont
distincts : un partenaire commun donnerait deux voisins communs à
l'arête qui le joint à b. Le partenaire ne peut appartenir au cœur
(p,q sont non adjacents), ni à Z (qui ne touche pas p ou q).

Les seuls partenaires dans D sont les quatre partenaires particuliers
de la section 1. Ils concernent quatre simples distincts. Ainsi, dans
le graphe T des seules arêtes B-B dont le triangle est centré au cœur :

- quatre sommets ont degré un ;
- les 42 autres sommets ont degré deux ;
- il n'y a aucun sommet isolé, et T a 44 arêtes.

Un graphe fini simple ayant ces degrés est la réunion disjointe de
**deux chemins non triviaux et de cycles éventuels**. Les quatre
extrémités sont précisément les simples des quatre triangles du tableau.
Leurs identités dans B restent à déterminer ; seules les incidences
cœur-double qui les définissent sont fixées.

Colorons une arête de transport par P ou Q selon le côté du cœur qui
contient le troisième sommet de son triangle. À chaque sommet intérieur
de T, les deux couleurs sont différentes. Les cycles de T sont donc
pairs. En ajoutant les deux doubles particuliers et les quatre arêtes
D-B du tableau, chaque sommet a exactement une arête de chaque couleur.
Le graphe ainsi augmenté, sur 48 sommets et 48 arêtes, est une réunion
de cycles pairs.

Cette décomposition ne prétend pas décrire toutes les arêtes induites
sur ces 48 sommets. D'autres arêtes peuvent avoir leur troisième sommet
de triangle hors du cœur. On ne peut donc pas appliquer automatiquement
une exclusion de ruban induit nu à ces cycles.

## 3. Essais et limites

`code/codex/norm16_tight_transport.py` couple les cellules (p,q) des
64 simples, leurs masques sur D, les moments cœur-D, et les appariements
imposés par les triangles au cœur. Les bornes locales de voisins communs
sont imposées aux arêtes obligatoires. Le modèle sans Z est faisable
pour chacune des quatre attaches. Ces témoins ne sont pas des SRG.

Le partenaire d'un simple dans un voisinage du cœur peut être un double.
Une première version l'imposait à tort dans B ; son verdict infaisable
était invalide. La version conservée et les quatre fichiers de résultats
incluent cette possibilité et indiquent tous une faisabilité.

L'option `--forest 7` ajoute les onze Z, leurs incidences avec D et B,
les moments exacts cœur-Z, D-D, D-Z et Z-Z, et des bornes locales entre
simples. Elle laisse libres les arêtes B-B supplémentaires : même une
faisabilité ne vaudrait pas complétion du graphe. Le pilote cas 3/0,
forêt 7, renvoie **UNKNOWN après 45 secondes**, pas une exclusion.

    python code/codex/norm16_tight_transport.py --orbit 0 --forest 7 --seconds 45

Il n'y a pas de nouvelle campagne de supports ni de résultat d'exclusion
à ajouter aux notes 256–258. La piste structurelle ouverte est de
contraindre le raccordement des quatre extrémités, avec les incidences
sur Z ou les obstructions spectrales, plutôt que d'assimiler tous les
simples à des cycles fermés dès le départ.

## 4. Information reçue de LAB au message 551

LAB rapporte au rang 37, après exclusion de la norme 14, l'identité

    350 a8 + 91 a9 + 13 a10
      = 7462 + a12 + 476 (b2−462) + 21 (b3−24948).

Référence : commit `86749e1`, branche `lab/theta-lp-2026-10-08`,
NOTE 17.100. Avec la borne b3≥45898 de la note 196 et les autres
termes non négatifs cités par LAB, le membre de droite vaut au moins
447412. Si les normes 16 et 18 sont exclues au rang 37, cela impose
a10≥34418 (en tenant compte des signes opposés).

La borne de la note 176, a10≤7920 κ20, montre alors que κ20≤4
suffirait à exclure ce rang. Cette dernière borne par graine demeure
une cible ouverte. Ce résultat des pairs est enregistré pour réemploi ;
aucun nouvel audit de son identité n'a été lancé ici.
