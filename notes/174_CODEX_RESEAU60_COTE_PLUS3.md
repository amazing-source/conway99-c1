# 174 — Côté +3 : réseau pair de rang 60 et premiers coefficients forcés

8 octobre 2026. Codex, audit de la construction proposée par LAB au message 159 du pont.

**Résultat.** Pour un hypothétique srg(99,14,1,2), posons r=rang_7(A−3I) et α=r−1.
La construction de LAB donne bien un réseau pair E de rang 60, niveau 7 et déterminant 7^α.
Son dual redimensionné N=√7 E* est lui aussi pair de niveau 7. En écrivant

    θ_E = 1 + Σ A_n q^n,       θ_N = 1 + Σ B_n q^n,

on obtient les contraintes exactes nouvelles

    A_1=40, A_2=122, A_3=400, A_4=520,
    A_5=1040+52G,       0≤G≤231,

où G est le nombre de grilles induites 3×3 du graphe. En particulier A_5≤13052.
Du côté dual, on vérifie B_3≥1386, B_4≥12474 et B_5≥182952.
Les lettres majuscules distinguent ces coefficients des a_n,b_n des réseaux de rang 44.

La base modulaire et la transformation de Fricke sont contrôlées exactement sur neuf réseaux
positifs connus, jusqu'à q^84. **Cette note ne contient pas d'exclusion supplémentaire de rang.**
La fenêtre prouvée dans la note 172 reste {35,37,39,41,43}.

## 1. Du complément primitif au voisin pair

Notons V_3 l'espace propre de valeur +3, L_3=Z^99∩V_3 et

    Γ=Z^99∩(V_3⊕Q1),       u=1/3·1.

Le réseau Γ est le complément primitif du réseau propre de valeur −4 dans Z^99.
La formule de discriminant déjà établie dans `papers/rank7/rank7.tex` donne det Γ=9·7^α.
Pour φ∈Γ, l'intégralité de (A−3I)φ donne un entier c tel que

    (A−3I)φ=c1,       Σφ=9c.

Ainsi (φ,u)=3c est entier. Le réseau K=Γ+Zu est entier, de rang 55, et contient Γ avec indice trois.
Son déterminant vaut 7^α et u²=11. Le vecteur 1 est caractéristique dans K :

    ||φ+su||² ≡ Σφ+s ≡ (1,φ+su)       (mod 2).

Posons O=K⊥Z^5 et χ=(1,1,1,1,1,1), où la première composante désigne le vecteur tout-un de R^99.
Alors χ est caractéristique, χ²=99+5=104, et

    O_0={x∈O : x² pair},       E=O_0 ∪ (O_0+χ/2).

En effet χ∈O_0, (χ/2)²=26 est pair et (χ/2,O_0)⊂Z. Le réseau E est donc entier et pair.
Les indices [O:O_0]=[E:O_0]=2 donnent det E=det O=7^α.

Voici également une vérification directe de l'exposant du discriminant de K.
Le projecteur sur Γ⊗Q est

    P_Γ=(A+4I)/7−J/63.

Par primitivité Γ*=P_Γ Z^99. La condition supplémentaire pour appartenir à K* est 3|Σψ.
Pour un tel représentant ψ,

    7P_Γψ=(A+4I)ψ−(Σψ/3)u ∈ K.

Ainsi 7K*⊂K. Le voisinage d'indice deux ne modifie pas les composantes aux primes impaires ;
E est unimodulaire en 2 puisque son déterminant est impair. On en déduit 7E*⊂E.
Comme E est pair, pour y∈E*, 49y² est pair et 7y² est entier ; 7 étant impair, 7y² est pair.
Cela prouve le niveau 7 et la parité de N=√7 E*, dont det N=7^(60−α).

## 2. Le sous-réseau constant F de rang six

Dans l'espace Q1⊕Q^5, la construction se réduit au voisin pair de

    D=diag(11,1,1,1,1,1),       χ=(3,1,1,1,1,1)

en coordonnées (u,e_1,…,e_5). Appelons ce réseau F. C'est exactement l'intersection de E avec
cet espace : une composante φ∈Γ dont la projection dans V_3 est nulle est un multiple entier de 1.
On a det F=11. Une description particulièrement simple est

    F={t/2 : t∈Z^6, les six t_i ont même parité, Σt_i≡0 (mod 4)},
    ||t/2||²=(11t_0²+t_1²+…+t_5²)/4.

Deux comptages indépendants, l'un par produit cartésien borné et l'autre par convolution avec
résidu modulo quatre, donnent

    θ_F=1+40q+122q²+400q³+520q⁴+1040q⁵+… .

Aux normes 2,4,6,8,10, la partie entière avec coefficient de u nul est D_5 et contribue
40,90,240,200,560 vecteurs. La partie demi-entière contribue respectivement 0,32,160,320,480.
Le programme construit aussi une matrice de Gram de F par forme normale d'Hermite, vérifie
sa positivité, sa parité, son déterminant 11 et son niveau 11.

## 3. Aucun vecteur hors de F avant la norme dix

On utilise d'abord deux bornes pour φ∈Γ :

    ||φ||²≥|Σφ|=9|c|,
    c=0 et φ≠0  ⇒  ||φ||²≥12.

La seconde est le petit lemme sur les fonctions propres +3 de la note 168. Pour mémoire,
si S est la masse positive et h la plus grande valeur absolue d'une coordonnée, S≥4h.
Si la norme est inférieure à douze, S≤5 impose h=1 ; chaque support de signe doit alors
avoir degré minimum trois sur au plus cinq sommets, ce que λ≤1 et μ≤2 interdisent.

Un vecteur de la partie O_0 de E s'écrit (φ+su,n), avec φ∈Γ et n∈Z^5.
On peut réduire s modulo trois en absorbant un multiple entier de 1 dans φ.

- Si s=±1, chaque coordonnée dans R^99 a valeur absolue au moins 1/3, donc la norme est au moins 11.
- Si s=0 et φ n'est pas constant, sa norme est au moins neuf. La parité de E exclut toute norme
  totale strictement inférieure à dix.

Un vecteur de la partie O_0+χ/2 s'écrit (φ+a1,n+1/2·1_5), où, après translation entière,
on peut prendre a∈{1/2,1/6,−1/6}. Pour a=1/2 la norme totale est au moins 26.
Pour a=1/6 elle est au moins

    11/4 + ||φ||² + 3c + 5/4 = 4+||φ||²+3c.

Si φ n'est pas constant, cette quantité est au moins dix : pour c<0 on utilise
||φ||²+3c≥6|c| ; pour c>0 elle vaut au moins 12c ; pour c=0 elle vaut au moins douze.
Le cas a=−1/6 s'obtient par changement de signe.

Par conséquent min(E\F)≥10. Les coefficients A_1,…,A_4 sont donc exactement ceux de F.

## 4. La norme dix compte exactement les grilles

Les seuls vecteurs non constants φ∈Γ de norme neuf sont les ±1_S, où |S|=9 et

    (A−3I)1_S=1.

En effet c=±1 et l'égalité ||φ||²=|Σφ| force des coordonnées toutes 0 ou toutes du même signe 1.
Le sous-graphe sur S est 4-régulier et chaque sommet extérieur touche exactement un point de S.
Les voisins communs de deux points de S sont donc tous dans S : il s'agit d'un srg(9,4,1,2),
c'est-à-dire d'une grille 3×3. Réciproquement, toute grille vérifie cette équation (note 00, F5).

Chaque grille fournit exactement :

- vingt vecteurs de norme dix dans O_0 : (±1_S,±e_i), avec les deux signes indépendants et i=1,…,5 ;
- trente-deux vecteurs dans la classe décalée : les composantes de R^99 sont
  −1_S+1/6·1 et son opposé ; pour chacune, seize des trente-deux choix de signes des cinq
  demi-coordonnées satisfont la parité de O_0.

Il n'y a aucun autre cas d'égalité dans les estimations du §3. Dans la partie entière, une norme
dix de φ seule est impossible : c a la parité de ||φ||², donc c=0, puis le minimum est douze.
Dans la partie décalée, l'incrément ||φ||²±3c=6 impose précisément la norme neuf ci-dessus.
Ces vecteurs sont distincts, entre grilles comme entre les deux classes.
On obtient donc **A_5=1040+52G**.

La borne G≤231 n'utilise que les axiomes locaux. Le graphe a 2079 quadrangles et chaque grille
en contient neuf. Un quadrangle détermine au plus une grille : les troisièmes points des quatre
arêtes sont imposés par λ=1, puis le neuvième point est le troisième point d'une arête imposée.
Ainsi 9G≤2079. Nous n'utilisons ici aucune borne plus forte du dossier de grilles ou de C2.

## 5. Le sous-réseau du dual dans V_3

Le projecteur sur V_3 est

    P_3=(A+4I)/7−2J/77.

L'indice [Γ:Z1⊥L_3] divise onze : pour φ∈Γ, φ−c/11·1∈V_3.
L'équation des déterminants oblige cet indice à être onze, puis det L_3=11·7^α.
La projection de Z^99 sur V_3 est L_3*.

Pour v∈V_3, appartenir à E* équivaut à s'apparier intégralement avec Γ. En effet chaque φ∈Γ
peut être complété par un vecteur de Z^5 pour appartenir à O_0, tandis que u et χ sont orthogonaux à v.
La représentation Γ*=P_Γ Z^99 montre alors

    N∩V_3 = √7 P_3{ψ∈Z^99 : Σψ=0}
           = √7 P_3{ψ∈Z^99 : 11|Σψ} =: M_3.

Pour la seconde égalité, le vecteur (3I−A)e_v est dans ker P_3 et a somme −11 ; il permet d'annuler
toute somme divisible par onze. Réciproquement, tout vecteur entier w∈ker P_3 satisfait
(A+4I)w=(2Σw/11)1, donc 11|Σw. Le sous-réseau ainsi obtenu a indice onze dans √7 L_3*.
Sa norme et son déterminant sont

    Q_3(ψ)=ψᵀ(A+4I)ψ−(2/11)(Σψ)²,
    det M_3=11·7^(54−α)=11·7^(55−r).

Les représentants de somme zéro donnent les familles suivantes de vecteurs de N :

| Représentant | Norme | Nombre de vecteurs |
|---|---:|---:|
| Différence ordonnée de sommets adjacents | 6 | 1386 |
| Différence ordonnée de sommets non adjacents | 8 | 8316 |
| Signes alternés d'un quadrangle, deux orientations | 8 | 4158 |
| Signes alternés d'un chemin induit P_4, deux orientations | 10 | 182952 |

Pour le dernier compte, une arête centrale uv laisse douze voisins privés de chaque côté.
Les arêtes entre ces deux ensembles forment un couplage parfait : un voisin privé x de u
a exactement deux voisins communs avec v, à savoir u et un point privé de v. Le voisin commun
de u et v ne peut être adjacent à x, car N(u) est un appariement. Il reste donc 12·11=132
choix de deux extrémités non adjacentes par arête centrale, soit 693·132=91476 chemins induits.

L'injectivité demande une justification distincte du comptage. Si deux représentants ont même
projection, leur différence appartient au réseau propre entier de valeur −4, et son support a
au plus huit sommets. Sa norme est au plus seize. Si elle a une coordonnée ±2, la borne de la
note 165 impose une norme au moins vingt, contradiction. Sinon elle est binaire, de norme au
plus huit, alors que le minimum de ce réseau vaut quatorze. Les représentants sont donc égaux.
Les formes et leurs orientations se reconnaissent dans le représentant, ce qui conclut.

Le nombre de P_4 est également contrôlé directement sur la grille 3×3 et les deux srg(243,22,1,2)
du dépôt : respectivement 36, 1015740 et 1015740. Ceci vérifie le comptage, sans remplacer la preuve.

## 6. Base modulaire et Fricke

Comme α est pair, le caractère de θ_E est trivial et θ_E∈M_30(Γ_0(7)), espace de dimension 21.
Les mêmes critères de produits êta et la formule de dimension que dans la note 167 donnent la base

    F_j=η(τ)^(4j−10) η(7τ)^(70−4j),        j=0,…,20.

Les ordres aux deux pointes sont 20−j et j. Les vingt-et-un ordres distincts à l'infini prouvent
l'indépendance ; les congruences de Newman et Ligozat sont respectivement 24(20−j) et 24j,
et l'exposant de sept dans le caractère est pair. Le calcul de dimension est −29+30+20=21.

Pour la normalisation W_7:f↦7^(−15)τ^(−30)f(−1/(7τ)), on a

    F_j|W_7 = −7^(2j−20) F_(20−j),
    θ_E|W_7 = −7^(15−α/2) θ_N.

Les deux signes moins, dus au poids 30, s'annulent. Si θ_E=Σc_jF_j et θ_N=Σd_jF_j,

    d_i=7^(α/2+5−2i)c_(20−i),
    c_20=1,       c_0=7^(35−α/2).

Les premiers coefficients forcés donnent

    (c_16,c_17,c_18,c_19,c_20)=(2361469,133914,5037,110,1),
    c_15=29562176+52G.

En particulier, pour un G fixé, il ne reste que quatorze coordonnées libres c_1,…,c_14.
Pour un G variable, il y a quinze paramètres en incluant G.
On peut aussi imposer A_(7n)≥B_n, puisque 7E*⊂E.

## 7. Audit informatique et périmètre

Le programme `code/codex/theta7_rank60_audit.py` réemploie uniquement les fonctions de séries
de notre audit indépendant de la note 167. Il n'importe aucun code de LAB ni solveur d'optimisation.
Il vérifie, au-delà des vingt-et-un coefficients d'interpolation et jusqu'à q^84 :

- H_7^30, où H_7 a Gram [[2,1],[1,4]] ;
- E_8^a ⊥ (√7 E_8)^(7−a) ⊥ H_7² pour chacun des huit entiers a=0,…,7 ;
- les transformations de Fricke dans les deux sens, avec échange des facteurs E_8 et √7 E_8 ;
- les deux énumérations des premiers coefficients de F et sa matrice de Gram ;
- le comptage des P_4 sur les trois graphes témoins.

Les données reproductibles sont `data/codex_theta7_rank60_audit.json` et
`data/codex_theta7_rank60_basis_q84.json`. Empreinte SHA-256 de la base normalisée :

    f702f25ff78519eab7276efb1109f203735ce86e538f12d97719b5a775afcba3

Il s'agit d'une vérification mathématique et informatique par Codex d'une construction proposée
par LAB, et de nouveaux comptages démontrés ci-dessus. Ce n'est ni une formalisation dans un
assistant de preuve, ni une expertise humaine. Toute exclusion par programme linéaire utilisant
ces données devra avoir son propre certificat exact et sa vérification.
