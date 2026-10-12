# Annexe mathématique — modèles, couverture et certificats

## A. Reconstruction avec un bord fixé

Soit une partition \(V=S\sqcup F\), et écrivons
\[
A=\begin{pmatrix}C&Y\\Y^{\mathsf T}&D\end{pmatrix}.
\]
Les blocs \(C,Y\) sont connus. Les équations d’un SRG \((v,k,\lambda,\mu)\) sont
\[
A^2=(k-\mu)I+(\lambda-\mu)A+\mu J,\qquad A\mathbf1=k\mathbf1.
\]

Le bloc \(S\times S\), indépendant de \(D\), doit d’abord satisfaire
\[
C^2+YY^{\mathsf T}=(k-\mu)I_S+(\lambda-\mu)C+\mu J_S.
\]
Dans notre expérience, il provient d’un vrai Paley et est donc correct, de même que les degrés de \(S\).
Les conditions restantes sont exactement
\[
YD=(\lambda-\mu)Y+\mu J_{S,F}-CY,\tag{A1}
\]
\[
D^2=(k-\mu)I_F+(\lambda-\mu)D+\mu J_F-Y^{\mathsf T}Y,\tag{A2}
\]
\[
D\mathbf1=k\mathbf1-Y^{\mathsf T}\mathbf1,\tag{A3}
\]
avec \(D=D^{\mathsf T}\), diagonale nulle et entrées binaires.

Pour une colonne/ligne \(d_i\), A1 et A3 donnent un domaine fini de masques.
Pour deux lignes \(d_i,d_j\), il suffit d’imposer
\[
(d_i)_j=(d_j)_i,\qquad
d_i\cdot d_j+(Y^{\mathsf T}Y)_{ij}
=\mu+(\lambda-\mu)(d_i)_j. \tag{A4}
\]
Les degrés fixent les diagonales de A2 ; A4 fixe toutes les autres entrées.
Le problème de compatibilité de lignes est donc **équivalent**, pas seulement nécessaire,
au problème de complétion graphique.

## B. Pourquoi le bord \(K_5\) est canonique à 25

Dans tout SRG(25,12,5,6) possédant une clique \(S\) de taille cinq, poser
\(t_w=|N(w)\cap S|\) pour les vingt sommets extérieurs.

Les degrés donnent \(\sum t_w=5(12-4)=40\).
Chaque paire de \(S\) a cinq voisins communs, dont trois dans \(S\) ; ainsi
\[
\sum_w \binom{t_w}{2}=\binom52(5-3)=20.
\]
Donc \(\sum t_w^2=80\) et
\[
\sum_w(t_w-2)^2=80-160+80=0.
\]
Tous les \(t_w\) valent deux. Chaque paire de \(S\) possède exactement deux voisins extérieurs ;
ces vingt sommets s’identifient aux dix paires, chacune doublée.

Cela fixe \(Y\) à renommage près, sans utiliser les arêtes extérieures ni une symétrie.
On a \(C=J_5-I_5\), \(Y^{\mathsf T}\mathbf1=2\mathbf1\),
\(Y\mathbf1=8\mathbf1\) et \(YY^{\mathsf T}=6I_5+2J_5\).
A1–A3 deviennent les équations de `RESULTATS.md`.

Ainsi, notre modèle englobe **tous les SRG(25,12,5,6) contenant un \(K_5\)**.
La conclusion qu’il retrouve aussi toutes les classes connues s’appuie en plus sur la
classification historique et sur les quinze correspondances vérifiées. Nous ne prétendons
pas déduire l’existence d’un \(K_5\) de ce seul argument local.

## C. Réduction des échanges et poids exacts

Dans le bord fixé, deux sommets extérieurs de même paire ont les mêmes incidences vers \(S\).
Leur échange est une symétrie du problème partiel, sans être une symétrie exigée de la solution.

Au moment de choisir la ligne \(i\), prenons une paire \(u,v\) encore non choisie, différente de \(i\),
que toutes les lignes déjà choisies voient de la même façon. Échanger \(u,v\) préserve le bord et
toutes les décisions antérieures, donc met en bijection les prolongements des deux choix
\((d_i(u),d_i(v))=(0,1)\) et \((1,0)\).
On garde le second et multiplie le poids par deux.
Les paires étant disjointes, \(s\) paires nouvellement distinguées donnent un facteur \(2^s\).

Si la ligne distingue déjà les deux sommets dans l’historique, l’échange n’est plus utilisé.
Si l’un des deux sommets est la ligne en cours, il n’est pas utilisé non plus.
Les échanges non supprimés continuent d’être parcourus explicitement.

C’est pourquoi les 3 983 feuilles ne sont pas des orbites complètes : il s’agit d’une
réduction partielle accompagnée de poids, dont la somme est le nombre exact de matrices étiquetées.
La règle ne suppose pas que le graphe terminé possède le moindre automorphisme.

### Contrôle indépendant du total

Pour un graphe \(G\) du catalogue, choisir une de ses \(K_5\), la bijecter sur \(S\) et bijecter
les deux sommets de chaque profil sur les deux étiquettes extérieures. Cela donne
\[
\#K_5(G)\,5!\,2^{10}
\]
bijections vers notre ensemble étiqueté. Chaque matrice obtenue est comptée \(|Aut(G)|\) fois.
On obtient la formule du rapport, vérifiée séparément pour les quinze graphes.

Trois répétitions sans aucune suppression d’échanges donnent les mêmes totaux que les
recherches pondérées : 4, 408 et 6 pour les trois contrôles documentés.

## D. Certificat général d’asymétrie par attaches

**Proposition.** Soit \(U\subseteq V(G)\) préservé par tout automorphisme de \(G\).
Supposons que les profils \(N(w)\cap U\), \(w\notin U\), soient deux à deux distincts.
Si l’identité est le seul automorphisme de \(G[U]\) préservant l’ensemble de ces profils,
alors \(Aut(G)\) est trivial.

**Preuve.** Un automorphisme de \(G\) induit un automorphisme de \(G[U]\) qui permute les profils.
Il fixe donc \(U\) point par point. L’injectivité des profils le force à fixer chaque sommet
extérieur. Il est l’identité. ∎

L’hypothèse sur les profils suffit ; on n’a même pas besoin d’utiliser les arêtes entre
sommets extérieurs pour rejeter un automorphisme du noyau.

Pour le témoin livré, \(U\) est la réunion de **toutes** les \(K_5\), donc intrinsèque.
Le graphe \(G[U]\) possède deux automorphismes ; l’unique involution transforme un profil
présent en un profil absent. Le vérificateur redémontre le nombre deux par une énumération
de 240 candidats, à partir de la seule matrice, et contrôle les dix profils.

### Autre certificat, sans utiliser le noyau

Associer à chaque sommet le couple (nombre de \(K_4\) incidents, nombre de \(K_5\) incidents).
Raffiner sa couleur par le multiensemble des couleurs de ses voisins.
Par récurrence, tous ces invariants sont préservés par chaque automorphisme.
Dès que les vingt-cinq couleurs sont distinctes, tous les sommets sont fixes.

Les comptes \(5,16,22,25\) sont les nombres de classes de couleurs successives pour le
témoin livré. Ce certificat ne repose pas sur un principe faux du type
« tout SRG asymétrique est distinguable par des petits motifs ».
Il est vérifié sur cette matrice précise. Le raffinement exploite les incidences entre
classes, et ne se réduit pas aux statistiques brutes de motifs de taille cinq.

## E. Matrice de différence et espaces propres

Pour le Paley initial \(A\) et la nouvelle matrice \(A'=A+E\), les identités exactes impliquent
\[
E\mathbf1=0,\quad YE_F=0,\quad
D E_F+E_F D+E_F^2+E_F=0.
\]
Le test entier livré vérifie ces deux dernières égalités sur les blocs libres.

Les projecteurs sont
\[
P_2=(A+3I)/5-3J/25,\qquad P_{-3}=(-A+2I)/5+2J/25.
\]
Les sous-espaces propres supportés dans le complément du \(K_5\) ont dimensions 7 et 8.
Pour les deux cliques précises du rapport, ces dimensions deviennent 2 et 4.
Elles sont calculées exactement par
\[
\dim E_\theta(F)=12-\operatorname{rang}P_\theta[S,S].
\]
Cette formule résulte de l’application de restriction à \(S\) depuis l’espace propre,
dont la matrice de Gram est le bloc principal du projecteur.

Pour le témoin à 74 changements, \(\operatorname{rang}E=10\) et
\[
\chi_E(t)=t^{15}
(t^{10}-74t^8+2041t^6-25636t^4+141060t^2-252000).
\]
Ce calcul est une description supplémentaire du témoin, pas une obstruction nouvelle à C1.
La relation \(E=5(P'_2-P_2)\) est la spécialisation de l’identité générale de chirurgie
spectrale déjà présente dans la note 165 du dépôt.

## F. Portée des certificats

- La validité SRG et l’asymétrie du témoin sont vérifiées par Python standard en entiers.
- Chaque représentant du recensement et chaque isomorphisme vers le catalogue sont vérifiés
  séparément, sans besoin de refaire la recherche.
- La couverture du recensement dépend de la validité de l’énumération des domaines et de la
  recherche exhaustive décrite ci-dessus. Les codes courts et leurs entrées sont fournis,
  ainsi qu’une répétition complète et des contrôles de suppression de symétrie.
- Aucun certificat DRAT ou développement Lean n’est revendiqué pour ce dossier.
- Les temps de calcul sont des mesures ; ils ne participent pas aux preuves.
