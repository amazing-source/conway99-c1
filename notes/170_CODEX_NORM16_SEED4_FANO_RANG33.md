# 170 — Au plus quatre vecteurs de norme 16 par graine ; le rang 33 force au moins 33 configurations de Fano

8 octobre 2026. Codex, en dialogue avec LAB et LAP (messages 142–146 du pont).

**Résultats.** Pour un srg(99,14,1,2), avec les réseaux et coefficients de la note 167,

    a_7 ≤ 7920,                  a_8 ≤ 27720.

Si r=rang_7(A−3I)=33, on a en outre

    a_7 ≥ 66.

Les coefficients comptent les vecteurs avec leurs deux signes. Ainsi **le rang 33 impose au moins
33 configurations de Fano à un signe près**, et en particulier min L=min L1=14.
La branche r=33 sans vecteur de norme 14 est donc éliminée. La branche r=33 avec de tels vecteurs reste
à étudier ; la présente note ne démontre pas r≥35.

La nouvelle borne sur a_8 vient d'une preuve combinatoire par reconstruction. Les calculs contrôlent les
configurations locales et la conséquence modulaire ; ils ne remplacent pas cette preuve par un décompte
de complétions du graphe inconnu.

## 1. Provenance

LAB a proposé au message 142 la borne a_7≤7920 et le principe de compter les vecteurs de norme 16
contenant une même graine. LAP a transmis au message 143 un argument donnant treize vecteurs par graine,
avec un découpage suivant les voisins dans les quatre sommets de la graine.

Codex obtient d'abord une borne dix au message 144 en identifiant le sommet manquant parmi les six seconds
voisins communs. L'observation nouvelle est que ces six sommets induisent nécessairement un graphe vide,
une seule arête ou un chemin de longueur deux. Il y a donc au plus deux choix du sommet manquant.
Une simplification de l'argument de comparaison de LAP, valable pour tous ses sous-cas, ramène ensuite
la borne à quatre (message 146). La preuve finale ci-dessous utilise cette comparaison et ne dépend
ni de l'ancienne borne dix ni de l'exclusion séparée de sous-cas de LAP.

LAB a refait l'argument de la borne dix, puis la combinaison donnant quatre (message 147), et a
ensuite vérifié explicitement la version simplifiée du §5 sans y trouver de faille (message 148).
Cette seconde lecture est celle d'une autre session d'IA, pas une formalisation ni une expertise humaine.

## 2. Rappels utilisés et définition d'une graine

Par les notes 165–167, tous les vecteurs de norme 16 de L1 appartiennent à L et s'écrivent

    f=1_P−1_Q,         |P|=|Q|=8,

où P et Q sont indépendants, chaque sommet ayant quatre voisins de l'autre côté.
Tout sommet extérieur à P∪Q a au plus deux voisins dans P et autant dans Q.

Si B est l'incidence P–Q, le défaut M=2I+2J−BBᵀ est un multigraphe 2-régulier sans boucle dont tous
les cycles sont pairs. En particulier, deux voisins distincts d'un sommet dans un cycle simple du défaut
ne sont pas adjacents entre eux dans le défaut. Un sommet extérieur ayant deux voisins dans P réalise
une arête de M, avec sa multiplicité.

Une **graine** est un sommet p0 et un ensemble U de quatre voisins indépendants de p0.
Le voisinage de p0 est constitué de sept arêtes disjointes ; il y a donc exactement

    C(7,4)·2^4=560

graines à sommet p0 fixé, et 99·560=55440 dans le graphe.
Un vecteur orienté f=1_P−1_Q de norme 16 contient huit graines, une pour chaque p0∈P, avec
U=N(p0)∩Q. Nous montrons qu'une graine est contenue dans au plus quatre tels vecteurs.

Pour une graine fixée, écrivons U={q1,q2,q3,q4}. Les q_i sont deux à deux non adjacents, donc ont
exactement deux voisins communs. Pour chaque paire {i,j}, notons c_ij celui qui est différent de p0.
Ces six sommets sont fixés par le graphe et la graine, indépendamment du choix éventuel de P et Q.

## 3. Deux cas exclusifs, reconnus dans le graphe sur les six c_ij

### Cas d'une arête double du défaut en p0

Supposons que p0 ait un partenaire p* d'intersection zéro dans Q. Les six autres sommets de P
ont chacun deux voisins dans U. Ils sont exactement les six c_ij, tous distincts : chacun contribue
à une des six paires de U, et aucune paire ne peut avoir deux seconds voisins communs.

Ainsi V={c_ij} est indépendant et R={p0}∪V=P\{p*} est fixé, de taille sept.
Chaque sommet de Q\U est adjacent à p* et à trois sommets de R. Réciproquement, tout sommet hors U
ayant trois voisins dans R appartient à Q\U : les sommets de P n'en ont aucun, les sommets extérieurs
à P∪Q en ont au plus deux, et les sommets de U en ont quatre.

Donc Q\U se reconstruit exactement à partir de R, puis P se reconstruit comme l'ensemble de tous les
sommets ayant quatre voisins dans Q. Il y a **au plus un vecteur** de ce cas pour la graine.

### Cas d'un cycle simple du défaut en p0

Supposons maintenant que p0 ait deux partenaires p′,p″ ayant chacun un seul voisin dans U.
Les cinq autres sommets de P ont chacun deux voisins dans U. Ils donnent cinq des six c_ij,
distincts. Le sixième, noté x, est extérieur à P∪Q et a deux voisins dans U⊂Q ; il appartient donc à D.
Il ne peut être dans Q, qui est indépendant. Les six c_ij sont tous distincts.

Le sommet x n'est pas adjacent à p0 : sinon l'arête xp0 aurait les deux sommets de sa paire de U
comme voisins communs, contrairement à λ=1.

Les deux voisins de x dans P constituent une arête du défaut M. Ils ne peuvent être exactement
p′ et p″, car ces deux voisins de p0 dans un cycle pair de longueur au moins quatre ne sont pas
adjacents dans M. Ils ne contiennent pas p0 non plus. Donc x touche au moins un, et au plus deux,
des cinq autres sommets de P qui sont dans V.

Il s'ensuit que **V induit une arête isolée ou un chemin de longueur deux, avec des sommets isolés**.
Dans le premier cas, x est l'un des deux bouts de l'arête ; dans le second, x est son centre.
Il y a donc au plus deux choix de x. Ce cas est incompatible avec le précédent, où V était indépendant.

Il reste à montrer qu'à x fixé, il y a au plus deux vecteurs.

## 4. Reconstruction à sommet manquant fixé

Réétiquetons U de façon que x=c_12. Les cinq sommets connus de P sont donc

    c_13, c_14, c_23, c_24, c_34.

Avec p0, ils forment un ensemble R fixé de six sommets.
Par les degrés quatre de chaque q_i vers P, les deux partenaires inconnus se répartissent ainsi :
p′ a q1 comme unique voisin dans U, et p″ a q2. En effet, parmi les cinq c connus, q1 et q2
apparaissent deux fois chacun, q3 et q4 trois fois chacun ; l'ajout de p0 laisse précisément
une place pour chacun de q1 et q2.

Posons Q′=Q\U. Les sommets p′ et p″ ont chacun trois voisins dans Q′, et ils ont exactement deux
voisins communs dans Q : leur défaut mutuel est nul. Leurs voisins dans U étant distincts,
on peut donc écrire, avec quatre sommets distincts,

    Q′={α,β,γ,δ},
    N(p′)∩Q′={α,β,γ},       N(p″)∩Q′={α,β,δ}.

### Les sommets γ et δ sont fixés

Les sommets p′ et c_13 ont déjà q1 en commun. Ils ne peuvent avoir plus d'un voisin commun dans Q′.
Or c_13 a deux voisins dans Q′. Comme p′ est adjacent aux trois sommets de Q′ autres que δ,
cela force c_13 à être adjacent à δ. De même c_14 est adjacent à δ.

Ainsi δ est **le second voisin commun de c_13 et c_14, autre que q1**, déterminé par le graphe.
De façon symétrique, γ est le second voisin commun de c_23 et c_24, autre que q2.
Ces sommets ne dépendent plus du choix des deux partenaires inconnus, dès que x est fixé.

Le sommet p′ est donc l'un des deux voisins communs de q1 et γ, deux sommets non adjacents de Q.
Il existe au plus deux choix de p′. Nous prouvons que chaque choix donne au plus un vecteur.

## 5. Unicité à p′ fixé : comparaison de deux vecteurs

Fixons p′ et une première configuration, avec partenaire p″ et sommets α,β,γ,δ comme ci-dessus.
Parmi c_13 et c_14, il existe un sommet c non adjacent à γ : sinon cette paire aurait trois voisins
communs q1,δ,γ, contrairement à μ=2.

Les sommets p′ et c ont q1 en commun et sont non adjacents. Leur unique autre voisin commun ξ
est dans {α,β}. En effet, c a δ et exactement un autre voisin dans Q′ ; ce dernier n'est pas γ,
et p′ est adjacent à α et β. Ainsi ξ est fixé par p′ et c dans le graphe.

Supposons qu'une seconde configuration, avec le même x et le même p′, remplace p″ par u≠p″.
Ses six sommets R, ses quatre sommets U et ses deux sommets γ,δ sont les mêmes. Le sommet u est
adjacent à q2 et δ. Il n'appartient ni au P de la première configuration, dont tous les autres
sommets sont déjà R et p′, ni à son Q, qui est indépendant.

Le lemme « au plus deux voisins dans Q pour un sommet extérieur » s'applique donc à u dans la
**première** configuration : ses deux voisins q2,δ épuisent cette possibilité. Il n'est adjacent
ni à α ni à β, donc pas à ξ.

Mais dans la seconde configuration, l'autre voisin commun de p′ et c est toujours ξ. Le même
argument le place parmi ses deux sommets α̃,β̃. Son partenaire u est adjacent aux deux : il doit
donc être adjacent à ξ. Contradiction.

Cela prouve qu'à p′ fixé, p″ est unique. Une fois P=R∪{p′,p″} connu, Q est exactement l'ensemble
des sommets ayant quatre voisins dans P, puisque tous les sommets extérieurs à P∪Q en ont au plus deux.
La configuration entière est donc unique.

Ainsi il y a au plus deux vecteurs pour chaque choix de x, et au plus deux choix de x.
Le cas de l'arête double était exclusif et donnait au plus un vecteur. **La borne globale est quatre.**

## 6. Comptages globaux et borne de rang 33

Chaque vecteur orienté de norme 16 porte huit graines, et chaque graine porte au plus quatre vecteurs.
Donc

    8a_8 ≤ 4·55440,          a_8 ≤ 27720.

Les deux signes sont bien comptés : les graines d'un vecteur sont prises dans son support positif P ;
son opposé a pour support positif Q et intervient lui aussi dans ce double comptage.

Pour la norme 14, la preuve de LAB est encore plus courte : une graine reconstruit les six autres
sommets de P comme les seconds voisins communs des paires de U, puis reconstruit Q. Chaque vecteur
porte sept graines et chaque graine en porte au plus un, donc 7a_7≤55440, soit a_7≤7920.

Au rang 33, nous reprenons **le certificat rationnel déjà audité de la note 168**, en remplaçant
la contrainte a_8≤0 par a_8≤27720. Avec a_7≤0, ses multiplicateurs positifs donnent la constante

    −4282111190 / 132977991 < 0,

avec annulation exacte de tous les coefficients variables. La branche a_7=0 est contradictoire.
En retirant aussi la contrainte a_7≤0 de cette combinaison, on obtient plus précisément

    a_7 ≥ 305865085 / 4755353 > 64.

Le nombre a_7 est pair, par l'involution f↦−f sur les vecteurs non nuls. Il est donc au moins 66,
soit au moins 33 configurations de Fano à un signe près.

Cette conséquence n'utilise ni le cap de racines b_1≤3784 de LAB, ni l'optimisation nouvelle de son LP,
ni la borne a_7≤7920. Elle utilise uniquement le certificat antérieur et la borne combinatoire sur a_8.

## 7. Vérifications et limites de leur portée

`code/codex/norm16_seed_cap.py` parcourt les 478 représentants de la note 169 et chacun de leurs huit
sommets p0, soit 3824 configurations locales marquées. Pour chacune, il vérifie notamment :

- les six seconds voisins communs, leur distinction et le graphe induit sur V ;
- le cas d'arête double ou de cycle simple et le nombre de choix possibles du sommet manquant ;
- la reconstruction de γ,δ par les deux paires c_13,c_14 et c_23,c_24 ;
- les intersections de voisinages, l'existence de c et ξ utilisées dans la comparaison ;
- le fait que le candidat extérieur pour remplacer p″ a déjà exactement q2,δ comme voisins dans Q.

Les sommets S et Z omis du petit graphe de contrôle ne peuvent être des seconds voisins communs de
paires de P ou de Q : ils n'ont respectivement qu'un voisin ou aucun dans chacun de ces supports.
Les arêtes D–D ne sont utilisées dans aucun de ces contrôles.

| Type de défaut | Configurations locales marquées contrôlées |
|---|---:|
| 8 | 1944 |
| 6+2 | 944 |
| 4+4 | 688 |
| 4+2+2 | 216 |
| 2+2+2+2 | 32 |
| Total | 3824 |

Ce contrôle local ne constitue pas une énumération des configurations possibles dans un graphe complet.
La comparaison de deux configurations du §5 est un argument mathématique, distinct de cette énumération.

Le programme régénère aussi notre base thêta et vérifie le certificat modifié dans les coordonnées
c_1,…,c_7, sans solveur LP. Les multiplicateurs et constantes exactes sont archivés dans
`data/codex_norm16_seed_cap.json`. Commande :

    python code/codex/norm16_seed_cap.py

## 8. Autres éléments du message 142

L'archive quartique corrigée de LAB (`f31263d`, puis `e6ce6ba`) est importée ici par `1beef10` et `4482f44`.
LAB rapporte que la correction de signe ne change pas la liste des bornes de minimum. Il s'agit de son
recalcul, pas d'une nouvelle optimisation indépendante dans cette note. Notre test vérifie séparément
que la correction donne l'égalité sur les 462 contributions de triangles et rejette la somme fictive
trop grande décrite dans la note 169.

Au rang 43, nous vérifions dans notre base l'identité exacte

    a_14−b_2 = −288(a_7−b_1).

Les deux différences sont non négatives par l'inclusion √7 M⊂L1 ; elles sont donc toutes deux nulles.
Cela confirme les deux premières égalités du phénomène de trace modulaire signalé par LAB.
La présente note n'utilise pas son assertion pour tous les indices, ni ses optimisations d'abondance.
