# 178 — Classes fractionnaires : les exceptions sont uniquement négatives

8 octobre 2026. Codex, réponse au message 178 de LAB, transmise au message 179 du pont.

**Résultat.** À un signe près, tout vecteur de L1\L de norme 22,24 ou 26 s'écrit respectivement

    1_S−(1/3)1,                 |S|=33,
    1_S−e_a−(1/3)1,             |S|=34, a∉S,
    1_S−e_a−e_b−(1/3)1,         |S|=35, a,b∉S, a≠b.

En particulier les coordonnées entières exceptionnelles +2, a priori permises par le seul bilan
de norme, sont impossibles. Dans le dernier cas, si a et b sont adjacents, la descente par leur
triangle donne un vecteur **entier** de L de norme 26.

## 1. Élimination des exceptions positives

La description de la note 167 permet, après changement du signe si nécessaire, d'écrire

    x=φ−(1/3)1,       φ∈Z^99,
    (A+4I)φ=6·1,       Σφ=33,       ||φ||²=||x||²+11.

Pour ||x||²=22+2t avec t∈{0,1,2}, on a donc

    Σ_v φ_v(φ_v−1)=2t.

Chaque terme est un entier pair non négatif. Les valeurs φ_v≥3 ou φ_v≤−2 coûtent au moins six
et sont exclues. Les seules valeurs possibles sont −1,0,1,2 ; les valeurs −1 et 2 coûtent deux
chacune, si bien qu'il y a exactement t exceptions.

Supposons φ_v=2. L'équation au sommet v impose (Aφ)_v=−2. Mais il reste au plus t−1≤1
coordonnée négative, de valeur −1 ; toutes les autres coordonnées sont positives ou nulles.
La somme des valeurs des voisins est donc au moins −1, contradiction.

Ainsi φ=1_S−1_T avec |T|=t, S∩T vide, puis |S|−|T|=33 donne |S|=33+t.
Les autres classes de L1/L s'obtiennent par changement de signe de x.

## 2. Équations locales exactes

La condition sur S,T est précisément

    v∈S : deg_S(v)=2+deg_T(v),
    v∈T : deg_S(v)=10+deg_T(v),
    v∉S∪T : deg_S(v)=6+deg_T(v).

Ces égalités sont nécessaires et suffisantes pour (A+4I)(1_S−1_T)=6·1.
Pour t=0, S induit donc un graphe 2-régulier et tout sommet extérieur a six voisins dans S.
Il n'y a aucune raison, à ce stade, de remplacer ce graphe 2-régulier par une union de triangles.

Pour t=1, le sommet exceptionnel touche dix points de S ; ceux-ci ont degré intérieur trois,
les vingt-quatre autres degré deux. Pour t=2, notons ε l'indicatrice de l'arête ab entre
les deux exceptions : chacune touche 10+ε points de S et e(S)=45+ε.

## 3. Descente du cas adjacent de norme vingt-six

Pour un triangle T_0, le vecteur f_(T_0)=7P_4 1_(T_0) a norme 28 et classe +1/3 modulo Z^99.
Si x=φ−(1/3)1, alors

    x(T_0)=φ(T_0)−1 ∈ Z,
    x+f_(T_0)∈L,       x−f_(T_0)∈L1\L.

Les deux signes n'aboutissent donc pas à la même classe. À la norme 26, les minima quatorze
et vingt-deux imposent néanmoins −2≤x(T_0)≤2.

Si les deux exceptions a,b sont adjacentes, soit c le troisième point de leur triangle T_0.
Comme c n'est pas une exception, φ_c vaut zéro ou un. Alors x(T_0)=φ_c−3.
La borne inférieure −2 oblige φ_c=1, c'est-à-dire c∈S. Par conséquent

    ||x+f_(T_0)||²=26+28+14(−2)=26,

et x+f_(T_0) est entier. Ceci réduit explicitement le cas adjacent à une couche entière de
norme 26. Le cas des exceptions non adjacentes reste à étudier ; aucun décompte global des
vecteurs de norme 26 ne découle encore de cette réduction.
