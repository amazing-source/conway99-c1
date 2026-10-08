# 192 — Les cocliques de taille 22 donnent b1≤44 et, au rang 43, b2≥968

8 octobre 2026. LAB a identifié le profil C de la note 191 à une coclique
de taille 22 munie d'un sommet marqué (message 247). Codex a relié cette
identification aux deux cocliques de chaque configuration de Fano déjà
décrites dans la note 165, puis démontré les bornes ci-dessous (message
248). LAB a relu et confirmé la chaîne de preuves au message 250.

**Résultats.** Pour tout hypothétique srg(99,14,1,2), à tous les rangs,

\[
 \boxed{b_1\le44.}
\]

Il y a donc au plus 22 lignes de racines dans M, contre 39 avec la seule
borne de Bessel de la note 191. Au rang 43, on obtient également

\[
 b_2\ge462+85b_1+\tfrac12b_1^2,
 \qquad \boxed{b_2\ge968.}
\]

Au moins **506** de ces vecteurs de norme quatre sont non triangulaires.
Les racines, leurs cocliques et les vecteurs nouvellement comptés sont
séparés explicitement dans la preuve. Aucun nouveau rang n'est exclu.

## 1. Cocliques de taille 22 et profil C : une bijection

Une coclique est un ensemble de sommets deux à deux non adjacents.
Pour une coclique R de taille 22, les nombres dO de voisins dans R des
77 sommets extérieurs satisfont

\[
 \sum d_O=308,\qquad \sum d_O^2=1232=308^2/77.
\]

La seconde égalité compte les deux voisins communs de chaque paire de R.
Le cas d'égalité de Cauchy impose dO=4 pour chaque sommet extérieur.
Ainsi A1R=4(1−1R) et

\[
 p_R=P_4\mathbf1_R=\mathbf1_R-\tfrac29\mathbf1,
 \qquad \|p_R\|^2=154/9.
\]

Pour v∈R, le vecteur

\[
 x_{R,v}=p_R-7P_4e_v
 =\mathbf1_{N(v)}+\mathbf1_{R\setminus\{v\}}-2e_v-\tfrac13\mathbf1
\]

est dans L1, a norme 28 et possède le profil C de la note 191.
Ses coordonnées valent −7/3 en v, 2/3 sur N(v) et R\{v}, et −1/3 ailleurs.
Réciproquement, cette note prouve que tout profil C a cette forme, avec
R={v}∪(S\N(v)), qui est une coclique de taille 22.

Le sommet v est l'unique coordonnée −7/3 et R se reconstruit à partir de
x. Les 22 choix de v sont donc distincts, ainsi que leurs opposés, qui
appartiennent à l'autre classe fractionnaire modulo L. Il y a exactement
**44 vecteurs de profil C dans L1 par coclique de taille 22**.

À tous les rangs, ces vecteurs sont dans L1. Leur appartenance à 7L1*,
nécessaire pour les compter dans M après division par √7, sera utilisée
seulement au rang 43.

## 2. Une racine distingue exactement ses deux cocliques

Choisissons une racine par ligne : r1,…,rk. La note 176 donne leur
orthogonalité et les vecteurs de Fano entiers

\[
 g_i=\sqrt7 r_i=\mathbf1_{P_i}-\mathbf1_{Q_i}\in7L_1^*.
\]

Chaque Fano a 15 sommets Zi sans voisin dans son support, et Zi est
indépendant. Les 70 autres sommets extérieurs touchent chacun exactement
un sommet de Pi et un de Qi (note 165). Il fournit les deux cocliques

\[
 R_i=P_i\cup Z_i,\qquad S_i=Q_i\cup Z_i,
 \qquad |R_i\cap S_i|=15.
\]

Pour toute coclique T de taille 22,

\[
 3p_T=3\mathbf1_T-\tfrac23\mathbf1\in L_1.
\]

En effet cette expression est dans E−4, sa partie entière a somme 66,
et elle satisfait la description de L1 de la note 167, avec s=2.
Comme gi∈7L1*, on a 3gi(T)∈7Z, donc gi(T)∈7Z. Il y a seulement
sept coordonnées +1 et sept −1 dans gi, d'où gi(T)∈{−7,0,7}.

Si gi(T)=7, T contient tous les points de Pi et aucun de Qi. Aucun des
70 sommets Xi ne peut alors appartenir à T, puisqu'il touche Pi.
Les quinze places restantes sont nécessairement tout Zi : T=Ri.
Le cas gi(T)=−7 donne de même T=Si. Par conséquent

\[
 g_i(T)=0\quad\text{pour toute autre coclique }T.
\]

Les **2k cocliques Ri,Si sont distinctes**. Pour détailler ce point,
supposons, après orientation, Ri=Rj=R pour i≠j. Les deux autres
extrémités S et T sont distinctes, sinon les lignes de racines seraient
les mêmes. L'orthogonalité de 1R−1S et 1R−1T imposerait

\[
 |S\cap T|=8,
 \qquad (\mathbf1_R-\mathbf1_S)(T)=15-8=7.
\]

Le cas d'égalité précédent imposerait T=R, contradiction.

## 3. Les centres des paires sont indépendants

Posons hi=pRi+pSi. Chaque hi est orthogonal à toutes les racines :
pour sa propre ligne, gi(Ri)+gi(Si)=7−7=0 ; pour une autre ligne,
les deux termes sont nuls par le §2.

Pour i≠j, les quatre intersections entre Ri,Si et Rj,Sj ont une même
taille entière tij. Cela résulte de gi(Rj)=gi(Sj)=gj(Ri)=gj(Si)=0.
En utilisant

\[
 (p_R,p_T)=|R\cap T|-44/9,
\]

on obtient

\[
 (h_i,h_i)=490/9,
 \qquad (h_i,h_j)=4t_{ij}-176/9.
\]

La matrice de Gram multipliée par 9/2 est donc une matrice **entière**
de diagonale 245 et de coefficients hors diagonale 18tij−88. Elle est
égale à l'identité modulo deux. Son déterminant est impair, donc non nul.
Les k vecteurs hi sont linéairement indépendants.

Ils appartiennent à l'orthogonal des k racines dans E−4, qui a dimension
44−k. Ainsi k≤44−k, donc **k≤22 et b1=2k≤44**.
Ce raisonnement ne suppose pas r=43, ni l'appartenance des profils C
à 7L1* : la borne sur les racines vaut à tous les rangs.

## 4. Au rang 43 : 88k nouveaux vecteurs de norme quatre

Le plan discriminant anisotrope de la note 177 implique qu'un vecteur
de L1 dont la norme est divisible par quatorze appartient à 7L1*.
En particulier chaque xR,v du §1 donne un vecteur xR,v/√7 de norme quatre
dans M. Les 2k cocliques distinctes du §2 fournissent donc **88k** vecteurs.

Ces vecteurs s'ajoutent sans doublon à ceux de la note 191 :

- un profil C, multiplié par √7, possède une coordonnée de valeur absolue
  7/3 ; il ne peut être un vecteur triangulaire, dont les coordonnées
  ont valeur absolue au plus 4/3 ;
- un reflet triangulaire s'écrit, après multiplication par √7,
  fT−εgi, où ε=gi(T)∈{−1,1}. Sur T, gi a exactement une coordonnée
  non nulle, de signe ε ; les coordonnées du reflet y sont donc 1/3 ou
  4/3. Hors de T, elles ont valeur absolue au plus 5/3. Un reflet et
  son opposé ne peuvent donc avoir le profil C ;
- les sommes de deux racines deviennent entières après multiplication
  par √7, ce qui les sépare des profils C fractionnaires.

La note 191 compte déjà 462 triangles signés, 84k reflets signés et
2k(k−1) sommes signées de deux racines. On obtient

\[
 b_2\ge462+84k+2k(k-1)+88k
     =462+170k+2k^2
     =462+85b_1+\tfrac12 b_1^2.
\]

L'identité thêta b2=1000−8a7+25a8+11a9+8a10+3a11+a12 et a7=b1=2k
donnent aussi b2≥1000−16k. Pour k≤2, cela impose b2≥968. Pour k≥3,
le comptage géométrique impose b2≥462+170·3+2·9=990. Donc

\[
 \boxed{b_2\ge968},\qquad b_2-462\ge506.
\]

## 5. Intersections des cocliques au rang 43

Pour deux cocliques R,S et des sommets marqués v∈R,w∈S, le produit
(xR,v,xS,w) est divisible par sept au rang 43, puisque les deux vecteurs
appartiennent à 7L1*=√7 M et que M est entier.
Si t=|R∩S|, le calcul à partir du projecteur donne, avant les deux
termes −7·1R(w) et −7·1S(v) :

```text
t+20 si v=w ; t−8 si v et w sont adjacents ; t−1 sinon.
```

Ces trois expressions valent t−1 modulo sept. Donc t≡1 mod7.
Deux cocliques distinctes ont ainsi une intersection de taille **1, 8
ou 15**. La taille 15 correspond exactement à un vecteur de Fano
(note 165), donc à une ligne de racines au rang 43.

Le graphe qui relie les cocliques lorsqu'elles se coupent en quinze
sommets est donc un couplage au rang 43 : chaque ligne de racines donne
une arête, et deux arêtes ne partagent pas d'extrémité par le §2.

## 6. Effet exact au rang 37

Pour comparer avec la note 189, on conserve a7≤842 et toutes les bornes
déjà démontrées, notamment b3≥45528. On impose b1≤44, puis le comptage
de norme quatre de la note 191, qui vaut à tous les rangs.

Ce dernier s'insère dans une relaxation linéaire par les inégalités
suivantes, valides pour k=b1/2 entier et j=0,…,21 :

\[
 b_2\ge462-2j(j+1)+(42+2j)b_1.
\]

Elles découlent de 2(k−j)(k−j−1)≥0. La formule renforcée du §4 est
réservée au rang 43 et n'est pas utilisée ici.

| Plafond au rang 37 | Note 189 | b1≤44 seulement | b1≤44 et comptages de norme quatre |
|---|---:|---:|---:|
| b4 | 211010055/13 | 624553169/39 | 2173272891/136 |
| b4+(651/34)b3 | 2332890187/136 | 2309069643/136 | 2291827803/136 |

Le dernier plafond couplé vaut **16851675,022…**, contre 17153604,316…
dans la note 189 : baisse exacte de **5132798/17 ≈ 301929,294**.
Le plafond de b4 vaut désormais 15979947,728….

Chaque nouvelle valeur est accompagnée d'un certificat rationnel et
d'un point rationnel atteignant le maximum de cette relaxation, vérifié
contre toutes ses contraintes. Ces points ne sont pas des séries thêta
de réseaux attestés ; ils montrent que ces contraintes ne ferment pas
encore le rang 37.

## 7. Reproduction

```text
python code/codex/coclique_root_bound.py
python code/codex/coclique_root_theta_effect.py --verify-only
```

Le premier vérifie les identités de moments et de Gram, la parité des
coefficients, les coordonnées séparant les familles, le comptage entier
968 et la congruence des intersections. Il accompagne la preuve écrite ;
il ne construit pas un graphe hypothétique et ne remplace pas les
arguments géométriques des §§2–4.

Le second reconstruit les formes thêta et vérifie les quatre certificats
et leurs points rationnels sans optimisation. Retirer `--verify-only`
pour redécouvrir les maxima.

Données : `data/codex_coclique_root_bound.json` et
`data/codex_coclique_root_theta_effect.json`.
