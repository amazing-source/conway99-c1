# 173 — Unicité des graines de norme 16 et budget commun aux normes 14 et 16

8 octobre 2026. Codex, prolongement des notes 165 et 170 ; transmis pour relecture aux messages 156–157.

**Résultats.** Chaque graine indépendante (p0,U) appartient à au plus un vecteur orienté de norme 16.
Elle ne peut être utilisée à la fois par un vecteur de norme 14 et un vecteur de norme 16. Par conséquent,

    7a_7 + 8a_8 ≤ 55440,

et en particulier **a_8≤6930**, au lieu de 27720 dans la note 170.

Deux vecteurs distincts de norme 16 ne peuvent avoir une différence de norme 14. Il en résulte aussi
que tous les vecteurs de norme 16 de L1 sont orthogonaux aux racines du dual M (réalisé dans le même
espace euclidien). Ces résultats ne constituent pas une nouvelle exclusion de rang à eux seuls.

## 1. Éléments déjà établis

Nous utilisons les faits suivants, indépendants du rang modulo 7 :

- min L≥14 ; les vecteurs de norme 14 et 16 de L1 appartiennent à L et sont binaires (notes 165–167) ;
- leurs deux supports de signe sont indépendants, de tailles sept ou huit, et leurs degrés croisés valent quatre ;
- pour un vecteur g de norme 14, tout sommet extérieur au support touche soit zéro sommet de chaque signe
  (ensemble Z_g), soit un de chaque signe (ensemble X_g), et **Z_g est indépendant** (note 165) ;
- la reconstruction d'une graine de norme 16 de la note 170 : les six seconds voisins communs V induisent
  soit un ensemble indépendant (cas d'une arête double du défaut), soit une arête isolée ou un chemin
  de longueur deux (cas d'un cycle simple du défaut).

Dans ce dernier cas, le sommet x de V extérieur au support est le centre du chemin ou l'un des deux
bouts de l'arête. Une fois x fixé, six sommets R de P sont connus, ainsi que six sommets de Q,
à savoir U et les deux sommets γ,δ reconstruits dans la note 170 §4.

Rappelons pourquoi Z_g est indépendant, car ce fait est essentiel au nouveau raisonnement.
Pour z∈Z_g, la somme des nombres de voisins communs de z avec les sept sommets du support positif
de g vaut 7·2=14. Chaque voisin de z appartenant à X_g y contribue une fois, les voisins dans Z_g
zéro fois, et z ne touche aucun sommet du support. Comme z a exactement quatorze voisins, ils sont
tous dans X_g ; il n'a donc pas de voisin dans Z_g.

## 2. Deux vecteurs portant une même graine ne se croisent pas entre signes

Supposons qu'une graine (p0,U) appartienne à deux vecteurs distincts

    f=1_P1−1_Q1,       h=1_P2−1_Q2,

de norme 16. Le cas d'arête double du défaut est déjà unique et exclusif dans la note 170 §3.
Nous sommes donc dans le cas d'un cycle simple pour les deux vecteurs.

Dans ce cas, chaque sommet de P1 a au moins un voisin dans U : p0 en a quatre, les deux partenaires
dans le défaut en ont un chacun, les cinq autres en ont deux chacun. Or Q2 est indépendant et contient U ;
aucun de ses sommets n'a de voisin dans U. Donc P1∩Q2 est vide. Symétriquement, P2∩Q1 est vide.

Ainsi

    (f,h)=|P1∩P2|+|Q1∩Q2|,
    ||f−h||²=32−2(f,h).

Puisque f−h est un vecteur non nul de L, la borne min L≥14 impose (f,h)≤9.

Si les deux vecteurs utilisaient le même sommet manquant x, ils auraient les six sommets R en commun
dans P et les six sommets U,γ,δ en commun dans Q. On aurait (f,h)≥12, contradiction.
Il y a donc **au plus un vecteur par choix de x**, sans utiliser le comptage de la note 170 §5.

## 3. Les deux choix possibles de x sont également incompatibles

Deux vecteurs distincts devraient donc utiliser les deux bouts de l'arête isolée de V comme choix de x.
Ils partagent au moins cinq sommets positifs — p0 et les quatre autres c_ij — ainsi que les quatre
sommets négatifs U. Donc (f,h)≥9, et la borne précédente force l'égalité :

    R=P1∩P2 a taille 5,         Q1∩Q2=U a taille 4,
    g=f−h a norme 14.

Le sommet p0 est extérieur au support de g. Il n'a aucun voisin dans P1∪P2, puisque p0 appartient
aux deux supports positifs indépendants. Ses quatre voisins dans chacun de Q1 et Q2 sont exactement U ;
il ne touche donc pas non plus Q1\Q2 ou Q2\Q1. Il n'a aucun voisin dans le support de g : **p0∈Z_g**.

Tous les sommets u∈U sont voisins de p0 et extérieurs au support de g. Comme Z_g est indépendant,
ils appartiennent à X_g, et ont exactement un voisin de chaque signe de g.
Ils ne peuvent toucher Q1∪Q2, puisque chacun appartient aux deux ensembles indépendants Q1 et Q2.
Leur voisin dans le signe positif de g est donc dans P1\P2, et leur voisin dans le signe négatif dans
P2\P1. Comme u a quatre voisins dans P1, il lui reste exactement trois voisins dans R. Ainsi

    e(R,U)=4·3=12.

En revanche, pour chaque r∈R, l'indépendance de P1 et P2 interdit tout voisin dans P1∪P2.
Le sommet r est extérieur au support du Fano g, donc il a au plus un voisin de chaque signe de g,
et en particulier au plus un dans Q1\Q2. Sur ses quatre voisins dans Q1, au moins trois sont donc dans U.
On obtient

    e(R,U)≥5·3=15,

contradiction. **Une graine ne porte jamais deux vecteurs distincts de norme 16.**

## 4. Disjonction des graines de norme 14 et 16

Supposons qu'une graine porte à la fois un Fano g=1_Pg−1_Qg et un vecteur h de norme 16.
Les six c_ij sont alors les six autres sommets de Pg ; V est indépendant.
Le vecteur h est donc nécessairement dans le cas d'arête double du défaut. Son support positif est

    Ph=R∪{p*},          R={p0}∪V=Pg.

Dans cette configuration h, les sommets de U ont quatre voisins dans R ; les quatre sommets de Qh\U
en ont exactement trois ; les sommets extérieurs à Ph∪Qh en ont au plus deux ; ceux de Ph n'en ont aucun.
Il y a donc **exactement quatre** sommets du graphe ayant quatre voisins dans R : ceux de U.

Mais le Fano g en exigerait sept, à savoir tous les sommets de Qg. Contradiction.
Les graines utilisées par les vecteurs de norme 14 et 16 sont disjointes.

Il y a 55440 graines indépendantes au total. Chaque vecteur orienté de norme 14 en porte sept,
chaque vecteur orienté de norme 16 en porte huit, et chacune est utilisée au plus une fois.
Cela donne

    7a_7+8a_8≤55440,         a_8≤6930.

Les deux signes des vecteurs sont comptés : une graine utilise un sommet du support positif.

## 5. Deux vecteurs de norme 16 ne peuvent différer d'un Fano

Soient f,h deux vecteurs de norme 16 tels que g=f−h ait norme 14. Le vecteur g est binaire :
les intersections croisées P1∩Q2 et P2∩Q1 doivent être vides, sinon g aurait une coordonnée ±2.
Notons R=P1∩P2 et U=Q1∩Q2, de tailles r et s. Comme (f,h)=9, on a r+s=9.

Chaque sommet de R est extérieur au support du Fano g. Il ne touche pas P1∪P2 et a au plus un
voisin dans Q1\Q2. Il a donc trois ou quatre voisins dans U. De même, chaque sommet de U a
trois ou quatre voisins dans R.

Un sommet de R de degré quatre vers U fournirait une graine commune à f et h, interdite par les
§§2–3. Un sommet de U de degré quatre vers R fournirait une graine commune à −f et −h, également interdite.
Tous ces degrés valent donc trois. Le comptage des arêtes R–U impose 3r=3s, impossible avec r+s=9.

Ainsi il n'existe **aucune différence de norme 14 entre deux vecteurs de norme 16**.

## 6. Orthogonalité aux racines de M

Soit ρ une racine de M, de norme 2. Le vecteur g=√7ρ appartient à L1 et a norme 14, donc est un Fano de L.
Comme M=√7 L1*, on a g∈7L1*, donc (g,h) est divisible par 7 pour tout h∈L1.

Si h a norme 16, les deux vecteurs h±g sont non nuls, et la borne de minimum 14 donne

    30−2|(g,h)|≥14,          |(g,h)|≤8.

Les seules valeurs possibles divisibles par 7 sont 0 et ±7. Si le produit scalaire valait ±7,
l'un des vecteurs h±g aurait norme 16 et différerait de h par un vecteur de norme 14, ce que le §5 interdit.
Donc (g,h)=0 et (ρ,h)=0.

Autrement dit, la coque de norme 16 de L1 est contenue dans l'orthogonal de l'espace engendré par
les racines de M. Cette observation ne donne pas à elle seule une borne numérique supplémentaire
sur a_8 ni sur r : la dimension de cet espace de racines reste à déterminer.

## 7. Portée et contrôle

La preuve est un argument de comparaison de deux vecteurs dans un même graphe. Elle utilise les
lemmes de reconstruction déjà contrôlés sur les 3824 configurations locales marquées dans la note 170,
mais ne prétend pas avoir énuméré des paires de configurations dans un graphe complet inconnu.
Le nouveau pas essentiel est la contradiction 12≥e(R,U)≥15 obtenue dans le cœur Fano de leur différence.

La borne de rang 35 et les certificats de la note 172 restent valables. Une nouvelle optimisation
avec la relation couplée ci-dessus est un travail séparé ; aucun nouveau rang n'est annoncé ici.

Au message 159 du pont, LAB a indiqué avoir redérivé indépendamment l'unicité des graines et le
budget commun, sans trouver de faille, et a confirmé les corollaires. Cette relecture par une autre
session d'IA ne constitue ni une validation humaine ni une formalisation dans un assistant de preuve.
