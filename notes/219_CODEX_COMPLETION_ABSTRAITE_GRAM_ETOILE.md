# 219 — Une étoile de Green abstraite peut prolonger trois ombres fixées

8 octobre 2026. Suite aux notes 207, 209 et 218, et aux messages LAB
398 / Codex 399. Cette note concerne **C1, dans le cadre générique
de rang global 37**. Elle ne concerne pas T20 de C2.

**Résultat.** Deux apices et une troisième ombre non apex, compatibles
au niveau de Green, admettent toujours un prolongement en dix vecteurs
entiers qui respecte tout le Gram modulo sept d'une étoile, sa somme
entière, les sommes de couches et la coordonnée centrale. Les sept
nouveaux vecteurs ne sont pas imposés binaires ou positifs.

Cela précise une limite de la relaxation algébrique : ces seules
identités ne peuvent interdire le prolongement. Cela ne démontre
ni l'existence d'une vraie étoile, ni la nécessité d'une énumération
exhaustive des graphes proches.

## 1. Hypothèses et énoncé précis

G est un graphe simple sans triangle sur 36 points, répartis en
trois couches de 12, avec exactement un voisin par couche. Posons

    H = 3I − G,    K = 12I − G − G² + 2J − B,
    B = diag(J₁₂,J₁₂,J₁₂).

On suppose rang₇ H=35. L'espace V des vecteurs de somme nulle dans
chaque couche a dimension 33 ; la forme de Green

    ⟨x,y⟩ = xᵀH⁺y,    H⁺=(H+J)⁻¹−J,

y est non dégénérée (note 209). Toutes les égalités de formes
bilinéaires dans les §§1–4 sont dans F₇.

Fixons un centre v et trois ombres binaires w₁,w₂,n, chacune de
poids deux par couche et contenant v. Nous supposons

    (Gw₁)_v=(Gw₂)_v=1,    (Gn)_v=0,
    ⟨w₁,w₁⟩=⟨w₂,w₂⟩=⟨n,n⟩=6,
    ⟨w₁,w₂⟩=⟨w₁,n⟩=⟨w₂,n⟩=3.

Les deux premières jouent le rôle des apices ; n est non apex.
Les conditions unaires supplémentaires des vrais pools peuvent
être imposées aux trois ombres fixées, mais ne sont pas nécessaires
à la preuve.

**Proposition.** Il existe dix vecteurs entiers m₀,…,m₉, dont
m₀=w₁, m₁=w₂, m₂=n, tels que :

1. chaque mᵢ a somme exactement deux sur chaque couche et mᵢ(v)=1 ;
2. Σmᵢ=Ke_v exactement en entiers ;
3. leur Gram de Green modulo sept vaut

       C = 3I₁₀ + 3J₁₀ − A_(4K₂+2K₁),

   avec isolés 0,1 et paires (2,3),(4,5),(6,7),(8,9).

La matrice C est celle imposée par le résidu nul au rang global 37.
Les hypothèses de cette proposition ne comprennent ni la binarité
des sept nouveaux vecteurs, ni leur positivité, ni les autres
contraintes combinatoires d'une étoile. Aucun z=0 n'est requis ici.

## 2. Fixer aussi la somme et la coordonnée centrale

Notons j le vecteur constant sur 36 points et Π=I−3B la projection
sur V modulo sept. Pour une ombre m de sommes de couches deux,
x_m=m−6j appartient à V et a le même Green que m.

Introduisons les vecteurs déjà déterminés

    s=Ke_v−60j,    h=ΠHe_v.

Le vecteur h est le dual de la coordonnée v sur V :
⟨h,x⟩=x(v). En effet H⁺H agit comme l'identité sur V et Π est une
projection orthogonale commutant avec H. On obtient

    ⟨h,h⟩=3−2/12=17/6=4,
    ⟨h,s⟩=10−60=6,
    ⟨h,x_m⟩=1−6=2.

Sur V, K=−H². Par suite

    ⟨s,x_m⟩=−(Hx_m)_v=(Gm)_v−3,

soit 5 pour les deux apices, 4 pour n. De plus ⟨s,s⟩=0.
Pour vérifier cette dernière identité sans supposer une étoile
complète, écrire s=−H²Πe_v, puis

    ⟨s,s⟩=(H³Π)_vv.

G est cubique sans triangle, donc (H³)_vv=54 ; HB=3B−J implique
H³B=27B−9J, d'où (H³Π)_vv=54−3(27−9)=0.

Ainsi le Gram des cinq vecteurs fixés
(s,x_w₁,x_w₂,x_n,h) est

    F = [ 0  5  5  4  6 ]
        [ 5  6  3  3  2 ]
        [ 5  3  6  3  2 ]
        [ 4  3  3  6  2 ]
        [ 6  2  2  2  4 ],       det F=2 dans F₇.

Leur espace est donc non dégénéré de dimension cinq, avec
complément orthogonal non dégénéré de dimension 28 dans V.

## 3. Réaliser le Gram cible avec les cinq vecteurs prescrits

La matrice C est non dégénérée : det C=2. En outre C⁻¹1 a
coordonnées 5 sur les deux apices et 4 sur les huit autres ombres,
donc 1ᵀC⁻¹1=2·5+8·4=0 dans F₇.

Adjoignons le vecteur dual h au modèle cible :

    C̃ = [ C     2·1 ]
         [ 2·1ᵀ    4 ],       det C̃=det C·4=1.

Dans cet espace abstrait de dimension onze, remplaçons la base
par (somme des dix ombres, ombre 0, ombre 1, ombre 2, h,
ombres 3,…,8). Le Gram des cinq premiers vecteurs est exactement F.
Le complément orthogonal cible a dimension six et est non dégénéré.

**Lemme élémentaire.** Tout espace symétrique non dégénéré sur F₇
de dimension au moins 2k représente toute forme symétrique non
dégénérée de dimension k.

**Preuve.** Diagonaliser les deux formes, ce qui est possible en
caractéristique impaire. Pour chaque coefficient cible c≠0,
utiliser deux coordonnées ambiantes de coefficients a,b≠0. Les
ensembles {at²:t∈F₇} et {c−bu²:u∈F₇} ont chacun quatre éléments ;
ils se rencontrent dans F₇. On obtient at²+bu²=c. Des paires de
coordonnées disjointes réalisent les k vecteurs orthogonaux. ∎

Appliquer ce lemme à la dimension ambiante 28 et à k=6. Prolonger
par l'identité sur les cinq vecteurs fixés donne une réalisation
de C̃ dans V. Les dix vecteurs xᵢ obtenus ont pour somme s et
vérifient ⟨h,xᵢ⟩=2, donc xᵢ(v)=2. Poser mᵢ=xᵢ+6j fournit
le Gram C, la coordonnée centrale un, les sommes de couches deux
et la somme Ke_v, pour l'instant modulo sept.

Les trois premières colonnes coïncident modulo sept avec les
trois ombres binaires fixées.

## 4. Rétablir toutes les sommes en entiers

Prendre pour chaque coordonnée son représentant dans {0,…,6}.
Les trois premières colonnes sont alors exactement w₁,w₂,n.

Corriger d'abord chaque somme de ligne en ajoutant son écart à
la dernière colonne m₉. Tous les écarts sont multiples de sept.
La ligne v est déjà composée de dix uns et sa cible K_vv vaut dix,
donc elle reste inchangée.

Dans chaque couche, choisir une ligne autre que v. Pour chaque
colonne libre m₃,…,m₈, y ajouter l'écart entre sa somme de couche
et la cible deux, et soustraire la même quantité de m₉. Ces écarts
sont encore multiples de sept. Les sommes de lignes restent donc
exactes et le Gram modulo sept est conservé.

Enfin chaque somme de couche de Ke_v vaut vingt. Les neuf
premières colonnes ayant chacune somme deux, la dixième a elle
aussi somme deux. Les trois colonnes fixées et la coordonnée
centrale n'ont pas été modifiées. La proposition est démontrée.

Cette étape peut produire des valeurs négatives ou supérieures
à un : c'est précisément la restriction omise par la relaxation.

## 5. Témoin explicite sur le triplet de la note 218

Le programme applique cette construction au graphe de la boule 12,
centre 0, avec

    w₁={0,1,12,13,26,35},
    w₂={0,2,18,21,24,25},
    n ={0,7,22,23,29,32}.

Ces trois ombres passent les contrôles binaires et rationnels de
la note 218. Le fichier joint archive les dix colonnes construites.
La relecture vérifie directement toutes les identités annoncées,
sans refaire la construction par plongement.

Les trois premières colonnes restent binaires. Les sept suivantes
ont respectivement 17,29,28,31,25,30,34 coordonnées non binaires ;
les valeurs vont de −42 à 238. Ce témoin est une solution de la
relaxation, **pas une étoile du SRG**. Il ne prétend notamment pas
satisfaire les bornes d'incidence, les pools unaires, la positivité
du projecteur réel, ni les contraintes de voisinages couplés.

Une corruption ajoutant sept à une seule coordonnée conserve le
Gram modulo sept mais brise les sommes exactes ; le vérificateur
la rejette.

    python code/codex/abstract_green_star_completion.py --out data/codex_abstract_green_star_completion.json --verify-only --negative-control

## 6. Conséquence pour la stratégie C1

Le message LAB 398 allait trop loin en proposant de conclure que
l'énumération exhaustive était la seule voie restante. Les témoins
précédents ne justifient pas cette nécessité : celui de la note 207
ne satisfait qu'une liste restreinte de contraintes sur une boule,
et les matrices abstraites de la note 218 n'imposent aucun Green.
Les contraintes individuelles de Green ne sont pas automatiques
sur les ombres binaires. Les tests réels ne le sont pas non plus :
la note 215 exclut déjà quatorze apices par leur seule norme réelle.

La présente proposition établit une limite plus précise : après
trois ombres compatibles, **le Gram modulo sept et les identités
linéaires énumérées ci-dessus admettent toujours une complétion
entière signée**. Une contradiction doit donc utiliser d'autres
restrictions, notamment les supports binaires, ou davantage de
relations globales. Une inégalité uniforme exploitant ces
restrictions reste une possibilité mathématique ouverte.

Le rang global intervient aussi dans les espaces de réseau et
leurs discriminants (note 205). Au rang 37, l'espace centré de
cette autre construction a dimension 18 ; ce n'est pas l'espace
de Green V de dimension 33. Aucune traduction utile des motifs
A/B de la note 218 dans l'espace de dimension 18 n'est démontrée ici.

Enfin, une masse combinatoire divisée par un facteur empirique
et multipliée par un coût supposé par boule n'est ni un décompte
certifié des orbites, ni une borne inférieure de calcul. L'estimation
de seize années-cœur du message 398 reste un scénario conditionnel,
pas une impossibilité prouvée de la voie exhaustive ou théorique.
LAB a accepté et consigné ces quatre corrections dans son message
400 (note 17.64, commit c7d99f4).

**Bilan de portée :** le lemme de comptage 218 est indépendant du
rang sous ses hypothèses géométriques ; le Gram précis utilisé ici
est celui du cadre générique de rang 37. Aucun nouveau rang de C1
n'est exclu par cette note.
