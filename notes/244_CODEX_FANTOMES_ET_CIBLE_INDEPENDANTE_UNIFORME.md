# 244 — Avec ou sans fantômes : une même cible de 2 289 configurations

9 octobre 2026. Codex, exploitation des messages LAP relayés par LAB
491, 492 et 493. Résultats transmis au pont aux messages 494 et 495.

**Théorème de réduction.** Dans S0 (rang 43, sans racines et sans normes
16 à 24), il existe au moins **2 289 configurations distinctes**

    y=(2/9)1+1_P-1_Q, |P|=7, |Q|=29, P et Q disjoints,
    (A+4I)(1_P-1_Q)=-4*1, P indépendant.                    (1)

Si g est le nombre de sommets fantômes, le seuil est au moins
**2 289+15g**. La réduction couvre donc aussi les cas 1<=g<=22 laissés
ouverts par la réduction binaire de LAP, et renforce son seuil 2 001
dans le cas g=0. Une borne supérieure uniforme de 2 288 sur (1)
suffirait à exclure tout S0. Cette borne supérieure n'est pas obtenue.

La note 242 a déjà éliminé les racines dans la branche sans normes
16 à 24. Le présent résultat ramène donc toute cette branche à la
même cible combinatoire ; il ne ferme pas encore la branche.

## 1. Données de pair, conventions et quatre profils

On utilise les données du programme neuf classes de LAP sans le
reproduire : `conway99-c2-aws/c1_mandat_c_transformations/`, section 13,
commits 62af6b1a0, b0634aa5f, df7372aa3. Le minimum 5 672 et les autres
bornes ci-dessous sont des résultats de son programme linéaire exact.

Écrire E pour le projecteur sur V_-4 et v_a=7Ee_a. Ainsi

    v_a(a)=28/9, v_a(b)=-8/9 si a~b, 1/9 sinon.

On emploie ici les vecteurs redimensionnés dans L_9, c'est-à-dire
sqrt(7) fois les vecteurs de O cités par LAP. Introduire :

- F : nombre de vecteurs de classe deux, norme 280/9 dans L_9 ;
  F>=5672. Les 693 arêtes donnent v_a+v_b, a~b.
- g : nombre de vecteurs de classe un, norme 196/9, autres que les
  99 vecteurs v_a. Ce sont les sommets fantômes ; 0<=g<=22.
- I : nombre de vecteurs **entiers**, norme 28 dans L1, deux signes
  compris ; 346<=I<=538.
- t : nombre de vecteurs de norme 28 dans une classe fractionnaire
  fixée de L1/L ; 231<=t<=327 et I+2t=1000.

Pour ces derniers, la note 191 distingue A,B,C. Écrire alpha,beta,gamma
pour les nombres de vecteurs non triangulaires de chacun de ces types,
dans la classe -1/3. Ainsi t=231+alpha+beta+gamma. Un A a trois
coordonnées entières -1, un B en a deux, un C aucune, dans l'écriture
x=phi-(1/3)1.

Les F-693 vecteurs supplémentaires de norme 280/9 ont, d'après LAP,
y=(2/9)1+m, sum m=-22, sum m²=36, (A+4I)m=-4*1, et exactement l'un
des quatre profils suivants. Les zéros sont omis :

| Type | Coordonnées de m | Nombre |
|---|---|---:|
| A | 2, trois 1, -2, vingt-cinq -1 | n_A |
| B | 2, quatre 1, vingt-huit -1 | n_B |
| C | six 1, -2, vingt-six -1 | n_C |
| D | sept 1, vingt-neuf -1 | n_D |

Les lettres de ce tableau ne désignent pas les mêmes profils que
alpha,beta,gamma, qui concernent la norme 28.

## 2. Les sommets fantômes ont deux formes combinatoires

**Lemme.** Tout sommet fantôme s'écrit

    z=(1/9)1+1_U-1_V, |U|=6, |V|=17.                       (2)

Le graphe sur U est vide ou contient une seule arête. Le graphe sur V
est un appariement contenant respectivement une ou deux arêtes.

Écrire z=(1/9)1+n. Alors sum n=-11, sum n²=23 et
(A+4I)n=-2*1. Par Cauchy avec E_aa=4/9, -3<=n_a<=3.
Si n_a=3, ||z-v_a||²=0 et z est un sommet connu. Si n_a=2,
||z-v_a||²=14, donnant une racine, exclue dans S0. Dans un fantôme,
les coordonnées positives de n valent donc un.

L'identité sum n_a(n_a+1)/2=6 borne leur nombre par six. Une valeur
-3 exigerait une somme de voisins dix, impossible. Une valeur -2
exigerait six voisins positifs, alors qu'elle consomme une unité du
budget et ne laisse que cinq coordonnées positives. Donc seules
les valeurs -1,0,1 restent, et les sommes donnent (2).

Les équations de voisinage sont

    u dans U : d_V(u)=6+d_U(u),
    v dans V : d_U(v)=2+d_V(v).

Ainsi e(V)=e(U)+1. Poser s_U=sum_(u in U)binom(d_U(u),2),
s_V=sum_(v in V)binom(d_V(v),2). Le comptage des voisins communs
des quinze paires de U donne

    5e(U)+s_U+s_V+sum_(x hors U union V)binom(d_U(x),2)=9.   (3)

Donc e(U)<=1. Enfin V ne peut avoir un sommet v de degré au moins
trois : v aurait au moins cinq voisins dans U, et un voisin w dans V
en exigerait au moins trois ; lambda=1 n'en permettrait qu'un dans
N(v) et au plus un hors N(v).

Si d_V(v)=2, v touche quatre points de U. Chacun de ses deux voisins
dans V doit toucher les deux points de U hors N(v), plus un dans
N(v). Ces deux voisins auraient alors au moins trois voisins communs :
v et ces deux points de U. C'est impossible. V est donc un appariement.

Noter g0,g1 les nombres de fantômes selon e(U)=0,1 ; g=g0+g1.

## 3. Comptages exacts par descente

Le principe de la première descente apparaît déjà dans le message 492
de LAP. La forme précise de (2) permet le comptage suivant :

    n_A=2g0+4g1,    n_B=15g0+13g1.                         (4)

En effet, un y de type A ou B a une unique coordonnée m_a=2.
Alors z=y-v_a est de norme 196/9, classe un. Il ne peut être un sommet
connu, sans quoi y serait une arête. Inversement chaque z de (2) et
chaque a dans V donne y=z+v_a. Le profil est A si a appartient à une
arête de V, B sinon. La position de l'unique 2 rend la correspondance
bijective. D'où (4), et en particulier n_B<=330.

La seconde descente est également présente dans le message 493, sous
forme de borne. Ici elle s'écrit exactement

    n_A+n_C=3alpha+2beta.                                  (5)

Pour la coordonnée m_c=-2, poser x=y+v_c, de norme 28 et classe +1/3.
Le vecteur -x est un A ou B de norme 28, et c est l'une de ses
coordonnées entières -1. Il est non triangulaire : si x=v_a+v_b+v_c
était un triangle, y=v_a+v_b serait une arête.
Inversement, chacune des trois/deux positions -1 d'un A/B extra
produit une telle descente. Les 231 triangles produisent exactement
les 693 arêtes et ont été retirés des deux côtés.

Il en résulte déjà

    n_D = F-693-(15g0+13g1)-(3alpha+2beta) >= 4361.          (6)

On a utilisé n_B<=330, alpha+beta+gamma<=96 et F>=5672.

Autre conséquence : le triplet négatif d'un A extra de norme 28 ne
peut être un chemin de deux arêtes dans S0. La descente au sommet
central donnerait deux coordonnées 2 non adjacentes, cas exclu par
la réduction de LAP. Les triplets négatifs extra sont donc indépendants
ou formés d'une arête et d'un sommet isolé.

## 4. Compter les D dont le support positif contient une arête

Soit y de type D, et ab une arête de son support positif. Alors

    w=y-v_a-v_b

est un vecteur entier de norme 28. Ses coordonnées négatives valent
uniquement -1 : aux deux extrémités elles valent -1 ; ailleurs
soustraire v_a+v_b ajoute zéro, un ou deux aux coordonnées de m.

### Combien de vecteurs entiers sont admissibles ?

Tout vecteur entier w de norme 28 a ses coordonnées entre -2 et 2.
En effet, si w_a=c, les sommes des coordonnées sur N(a) et sur le
reste sont -4c et 3c. Donc ||w||²>=c²+7|c|, qui dépasse 28 pour |c|>=3.

Pour toute coordonnée w_a=-2, z=w+v_a a norme 196/9 et z_a=10/9 ;
c'est donc un sommet fantôme, et a est l'un de ses six points positifs U.
Inversement chaque paire (z,a),
a dans U, donne un w avec -2 en a. La forme (2) montre que ce -2
est unique. Il y a donc exactement **6g vecteurs entiers de norme 28
ayant une coordonnée -2**. Seuls I-6g peuvent provenir d'un D.

### Au plus cinq arêtes utiles par vecteur, même non binaire

Pour un w binaire, la borne de LAP (message 493) donne au plus cinq
arêtes dans son support négatif. Sa preuve utilise les deux supports
de taille quatorze et le comptage de leurs voisins communs ; elle
s'applique à tous les rangs et n'est pas recalculée ici.

Supposons w non binaire, mais sans -2. Il possède un unique +2 en a
et w=v_a-z, où z est de la forme (2). Le sommet a est isolé dans U,
sinon une autre coordonnée de w vaudrait -2.

Les treize coordonnées -1 de w sont

    Y=(U sans a) union R, R=N(a) hors V, |R|=8.

Noter h2 et h1 les nombres d'arêtes de l'appariement sur V ayant
respectivement deux et un seuls bouts dans N(a). Le voisinage de a
est un appariement de sept arêtes, réparti sur six points de V et
huit points de R. Il donne

    e(R)=1+h2.

Les cinq paires non adjacentes (a,u), u dans U sans a, ont dix voisins
communs au total. Ceux dans V sont au nombre de 6+2h2+h1. Donc

    e(R,U sans a)=4-2h2-h1.

Si une arête de Y ne touche pas R, ajouter son vecteur v_p+v_q à w
laisse la coordonnée +2 en a ; le résultat ne peut être de type D.
Il reste donc au plus

    e(R)+e(R,U sans a)=5-h2-h1<=5

arêtes utiles. Certaines peuvent encore donner un autre type ; il
suffit ici d'une majoration.

Chaque D non indépendant a au moins une arête positive, et chaque
descente est déterminée par le couple (w,arête). Ainsi

    n_D_nonindep <= 5(I-6g).                               (7)

C'est l'extension nécessaire pour couvrir les cas avec sommets fantômes.

## 5. Le seuil uniforme

Soustraire (7) de (6), utiliser I+2t=1000 et
t=231+alpha+beta+gamma. On obtient

    n_D_indep >= F-5000+7t+15g+2g1+beta+3gamma
              >= 2289+15g.                                (8)

La dernière étape n'utilise que F>=5672, t>=231 et la positivité des
autres termes. Les configurations sont des couples ordonnés (P,Q),
uniquement déterminés par y ; aucun quotient par automorphismes n'est
pris dans ce comptage.

## 6. Structure de tous les D : un budget de défaut dix-sept

Ce complément concerne aussi les D dont P n'est pas indépendant.
Poser e=e(P), s_P=sum_(p in P)binom(d_P(p),2), Z=V(Gamma) hors P union Q.
Les équations donnent

    d_Q(p)=8+d_P(p) sur P,
    d_Q(q)=d_P(q) sur Q,
    d_Q(z)=4+d_P(z) sur Z,
    e(Q)=28+e.

Compter les voisins communs des paires de P donne l'identité exacte

    5e+s_P+sum_(q in Q) ((d_Q(q)-2)(d_Q(q)-3)/2)
        +sum_(z in Z) binom(d_P(z),2) = 17.                (9)

Tous les termes sont non négatifs. Donc e<=3, et si e=3, s_P<=2.
À des sommets isolés près, le graphe positif a l'un des sept types

    vide, K2, 2K2, P3, 3K2, P3+K2, P4.

Si P contient un P4, (9) est saturée : les 29 points de Q ont
exactement 25 degrés deux et quatre degrés trois ; chaque point
de Z touche au plus un point de P.

Enfin tout triangle T de Q vérifie

    6+e(T,Q sans T)=e(T,P)<=7.

Il a donc au plus une arête sortante dans Q, et deux triangles de Q
ne partagent aucun sommet. Pour la cible indépendante, e(Q)=28 et
chaque point de P a exactement huit voisins dans Q.

## 7. Portée et suite

Les bornes radiales et la classification initiale des quatre profils
sont attribuées à LAP ; le lemme binaire à cinq arêtes est également
le sien. Les nouveaux apports ici sont la structure des sommets
fantômes, les bijections affinées, le traitement des vecteurs entiers
non binaires, la réduction uniforme (8), et le budget (9).

Aucun calcul par classes n'a été reproduit. Les arguments nouveaux
sont des preuves par coordonnées, incidences et comptages de paires.
Le seuil 2 289 est une **obligation d'existence**, pas un nombre de
configurations déjà réalisées ou éliminées. S0 et C1 restent ouverts.
