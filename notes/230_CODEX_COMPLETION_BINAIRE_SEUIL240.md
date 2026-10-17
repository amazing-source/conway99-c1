# 230 — Complétion binaire au rang 37 : le seuil exact de 240 arêtes

9 octobre 2026. Exploration issue du cas connexe sans torsion signalé
par LAB 443 ; résultat transmis au pont par Codex 444.

**Théorème de réduction.** Pour un graphe proche connexe sans torsion
modulo sept, soixante ombres binaires de moments exacts K et de produits
de Green admissibles déterminent déjà toutes les arêtes lointaines.
Le nombre de ces arêtes est nécessairement

    240 + 7q,       q entier ≥0.

Il vaut 240 **si et seulement si** ces données se prolongent en un
SRG(99,14,1,2) de rang modulo sept égal à 37. Au seuil, les équations
restantes de voisins communs sont automatiques sur les entiers.

Cela donne une formulation suffisante du problème de complétion, au-delà
des conditions nécessaires d'une ou deux étoiles. **Ce n'est pas une
nouvelle exclusion.** Le critère ancien L23 impose déjà q≥1 lorsque
le nombre d'arbres couvrants est un carré non nul modulo sept (§7) ;
la borne reste à trouver pour les autres classes sans torsion. Aucun balayage de graphes
proches ni nouvelle vérification des recherches LAP n'est lancé ici.

## 1. Données et hypothèses

Soit G un graphe simple sur X=X₀⊔X₁⊔X₂, avec douze sommets par couche
et exactement un voisin dans chacune des trois couches pour tout sommet.
Posons, sur les entiers,

    H=3I−G,
    B=diag(J₁₂,J₁₂,J₁₂),
    K=12I−G−G²+2J−B.

On suppose rang₇ H=35. En particulier G est connexe, puisque les
indicatrices de ses composantes seraient sinon plusieurs directions
indépendantes du noyau. Dans F₇, définissons

    H⁺=(H+J)⁻¹−J,       H⁺1=0,
    M=3J−H,             M⁻¹=−H⁺+5J.                    (1)

Le fait que |X|=36≡1 modulo sept explique ces normalisations.

Cherchons N=(n₁,…,n₆₀), matrice **binaire** de 36 lignes, telle que :

1. chaque colonne a exactement deux uns dans chaque couche ;
2. NNᵀ=K sur les entiers ;
3. n_fᵀH⁺n_f=6 dans F₇ ;
4. pour f≠g, n_fᵀH⁺n_g∈{2,3} dans F₇.

La diagonale de K vaut dix, donc chaque ligne de N contient dix uns.
Les colonnes sont automatiquement distinctes par les conditions 3–4.

Définissons le graphe simple F sur les soixante colonnes par

    F_fg = 1 si n_fᵀH⁺n_g=2,
           0 si n_fᵀH⁺n_g=3,           f≠g.            (2)

Ces valeurs sont des entiers zéro ou un, pas des variables encore libres.

## 2. Les degrés lointains sont congrus à un

Puisque Σ_g n_g=10·1 et H⁺1=0, pour chaque f,

    0 = Σ_g n_fᵀH⁺n_g
      = 6 + 2d_F(f) + 3(59−d_F(f))
      = 183−d_F(f),                          dans F₇.

Ainsi d_F(f)≡1 modulo sept. Cette congruence seule permettrait encore
le degré un ; le §4 montrera que le degré est au moins huit.

## 3. Le Gram impose l'identité SRG modulo sept

Adjoignons un triangle T={t₀,t₁,t₂}, où t_i est adjacent à toute la
couche X_i. Joignons X à F selon N. Avec R la matrice 3×36 des couches,
la matrice d'adjacence obtenue sur 99 sommets est

        [ J₃−I₃     R      0 ]
    A = [ Rᵀ        G      N ].
        [ 0         Nᵀ     F ]

Les points de T et de X ont degré exactement quatorze. Un point f a
degré 6+d_F(f), donc lui aussi degré nul modulo sept, par le §2.
Dans F₇, posons Q=A−3I+3J. Son bloc sur X est M, inversible.

Le vecteur de produits d'un point f avec X est r_f=3·1+n_f. Par (1),

    r_fᵀM⁻¹r_g = 6−n_fᵀH⁺n_g.

Les conditions 3–4 et (2) donnent donc exactement les blocs diagonaux
et hors diagonale requis pour Q sur F. Pour t_i, si b_i=1_{X_i},
sa coordonnée dans la base X est

    M⁻¹(3·1+b_i)=2b_i+2·1.

Les sommes de couches des n_f donnent les produits Q_{t_i,f}=3.
Les produits entre les t_i valent zéro sur la diagonale et quatre
hors diagonale, comme requis. Il existe donc une matrice C, avec
C_X=I₃₆, telle que

    Q=CᵀMC,        rang₇ Q=36.                          (3)

Par NNᵀ=K, le bloc proche vérifie déjà, en entiers,

    (A²+A)_{XX}=B+G²+NNᵀ+G=12I+2J.

Comme tous les degrés de A sont nuls modulo sept et 99≡1, le
développement de Q² donne

    Q²=A²+A+2I+5J,                         dans F₇.

Ainsi (Q²)_{XX}=0. Or, par (3), ce bloc est M(CCᵀ)M. L'inversibilité
de M force CCᵀ=0, puis Q²=0 sur tous les sommets. Finalement

    A²+A ≡ 12I+2J  (mod 7).                             (4)

Cette étape utilise les moments globaux des soixante ombres ; elle ne
s'applique pas à une simple étoile isolée ni à une complétion signée
comme celle de la note 219.

## 4. Le seuil est 240, avec un écart multiple de sept

Pour deux sommets distincts de A, leur nombre de voisins communs est
un entier non négatif. Par (4), il est congru à un s'ils sont adjacents,
et à deux sinon. Il est donc **au moins** respectivement un et deux.

Fixons un point lointain f et sommons cette borne sur les 36 points
proches. Il est adjacent à six d'entre eux :

    Σ_{x∈X}(A²)_{xf} ≥ 6·1+30·2=66.

Le membre gauche vaut, directement dans les blocs de A,

    Σ_x (GN+NF)_{xf}=18+6d_F(f).

Ainsi d_F(f)≥8. Avec le §2,

    d_F(f)=8+7a_f,       a_f entier ≥0.

La somme des degrés étant paire, Σ_f a_f est pair. Donc

    e(F)=240+7q,         q=(Σ_f a_f)/2 entier ≥0.         (5)

## 5. Au seuil, toutes les équations entières se ferment

Si e(F)≤240, (5) impose q=0 et tous les degrés lointains valent huit.
Le graphe A est donc quatorze-régulier.

**Lemme de relèvement.** Un graphe simple quatorze-régulier sur 99
sommets satisfaisant (4) est un SRG(99,14,1,2).

En effet, pour un sommet a, chaque compte de voisins communs avec un
autre sommet dépasse sa cible, un sur les arêtes et deux ailleurs,
d'un multiple de sept non négatif. Or la somme réelle des comptes est

    14²−14=182,

exactement la somme des cibles 14·1+84·2=182. Tous les excès sont donc
nuls. Les égalités SRG valent en entiers pour chaque paire.

Enfin rang₇(A−3I)=37 : Q a rang 36 par (3), annule 1 et coïncide
avec A−3I sur 1⊥ ; sur la droite ⟨1⟩, A−3I agit par 14−3≡4≠0.
La décomposition ⟨1⟩⊕1⊥ est directe car 1ᵀ1=99≡1.

Réciproquement, un SRG de rang 37 possédant un triangle dont H a
rang 35 fournit ces données. Son Gram Q a rang 36 et son bloc M est
inversible, d'où les produits de Green prescrits. Il a soixante points
lointains, chacun de degré lointain huit, donc e(F)=240.

## 6. Nouvelle formulation de la cible, et sa limite

Pour G fixé, former les ombres binaires de poids deux par couche et
de norme de Green six. Deux ombres sont compatibles si leur produit
de Green est deux ou trois ; affecter un coût un à la première valeur,
zéro à la seconde.

Il suffit alors de chercher une **clique de soixante ombres compatibles**
avec moments entiers Σ_f n_f n_fᵀ=K et coût total au plus 240. Les
contraintes nécessaires déjà connues peuvent affiner le pool : elles
ne sont pas remplacées par des vecteurs arbitraires ou signés.

Une sélection au coût 240 serait une construction complète de C1 au
rang 37. À l'inverse, une borne uniforme coût≥247 sur toutes les
sélections admissibles exclurait le cas connexe sans torsion, sans
traiter séparément chaque graphe G. **Cette borne reste à trouver pour
les classes non carrées de τ, après application de L23 au §7.**
La formulation ne résout pas le choix des soixante ombres ni celui de G.

La note ne suppose pas P=0. Dans une recherche limitée à P=0, il faut
en plus conserver les contraintes nécessaires d'absence de prismes.
Elle ne traite pas les droites connexes avec torsion, les autres rangs,
ni directement les 174 noyaux de la route sans rang. Sa contribution
est la suffisance du seuil, et la suppression des équations quadratiques
supplémentaires en F une fois les hypothèses ci-dessus satisfaites.

## 7. Appliquer L23 avant toute recherche de sélection

Le message LAB 445 retrouve un filtre déjà établi le 25 septembre
dans `notes/102_FORME_BETA_SIGNE.md`, sections 1 et 4, sous le nom
**L23**. On l'utilise comme acquis, sans refaire la preuve d'oddité
ni ses tests sur des graphes exemples. Ce n'est pas une découverte
supplémentaire de la présente campagne.

Notons τ(G) le nombre d'arbres couvrants de G. Le discriminant de la
forme globale non dégénérée Q est non carré au rang 37. Or, dans le
cas de la présente note, les 36 vecteurs proches sont une base, de
matrice M. Le théorème des arbres couvrants donne

    det M = −3888 τ(G) ≡ 4 τ(G)  (mod 7).

Donc toute vraie complétion au rang 37 impose

    τ(G) mod 7 ∈ {3,5,6}.                               (6)

Si τ(G)∈{1,2,4} modulo sept, le cas q=0 du théorème produirait un
SRG contredisant L23. Pour toute sélection satisfaisant les hypothèses
des §§1–2, on a donc déjà

    q≥1,       e(F)≥247.

Cette borne est une application du filtre ancien à la nouvelle fonction
de coût ; elle ne constitue pas une nouvelle famille de graphes exclus.
Si τ≡0, H n'a pas rang 35 et le modèle sans torsion ne s'applique pas.

**Consigne de recherche.** Écarter les classes {1,2,4} avant de construire
les pools de sélection de la note 230 ; rechercher une obstruction
nouvelle uniquement dans {3,5,6}. Une proportion d'environ moitié sur
des échantillons aléatoires n'est pas une proportion démontrée du
catalogue complet. Aucun échantillonnage supplémentaire n'est nécessaire
pour utiliser le critère exact.

Le même type global précise la forme résiduelle dans le cas de deux
composantes sans torsion, comme l'indique LAB 445 : leur sous-espace
proche a discriminant de classe 3τ₁τ₂. Le complément de dimension un
au rang 37 a donc norme de classe τ₁τ₂. Une seule des deux classes de
normes scalaires est pertinente pour chaque paire. Les balayages déjà
réalisés sur les deux classes restent des recherches sur un sur-ensemble ;
ce constat n'invalide pas leurs exclusions et ne demande pas de les rejouer.
