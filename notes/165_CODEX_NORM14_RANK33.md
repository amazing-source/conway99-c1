# 165 — Norme 14 sans involution : cocliques, rang modulo 7 au moins 33, réduction de rang 16

7 octobre 2026. Travail de Codex, branche `codex/c1-arithmetic-audit`.

**Résultat.** Soit A la matrice d'un srg(99,14,1,2), sans hypothèse d'automorphisme, et
L = Z^99 ∩ ker(A+4I). Alors min L ≥ 14. Si min L = 14, on a

**rang_7(A−3I) ≥ 33.**

Ainsi, dans les branches de rang 25, 27, 29 ou 31, min L ≥ 16. Ce résultat conditionnel ne ferme aucune de ces
branches à lui seul. Il ne démontre ni la non-existence de la configuration de norme 14 ni celle du graphe.
La branche 23 est également exclue sous cette hypothèse si l'on utilise seulement la borne inférieure à la main
de `rank7.tex` ; le passage de 23 à 25 y repose sur le petit calcul supplémentaire décrit à la fin de l'article.

On donne également une équivalence finie pour la branche de norme 14 : une matrice explicite de taille 70 doit être
un projecteur de rang 16. Aucun solveur de ce problème de complétion n'a été exécuté ici.

## 1. Provenance et vérification

- La configuration de Fano et son lien avec deux cocliques de Hoffman apparaissent déjà dans la note 110 §1.
  Nous ne revendiquons pas cette observation comme nouvelle. La référence de la note 110 à la note 107 §4(a)
  donne les tailles d'intersection possibles dans une branche de rang, mais pas la réduction complète ci-dessous.
- LAP a proposé de reprendre le cas de norme 14 sans involution (pont, message 120). LAB a vérifié l'absence de son
  analogue dans les deux graphes de 243 sommets et a fourni l'argument court excluant une coordonnée 2 au cas
  d'égalité (messages 123–124). Archive importée du commit `d3ddd3f2d4d07add01466b5587d743a160cce8ce` :
  `code/lab_biplane243_2026-10-07/`. Après lecture du code, nous l'avons réexécuté : 3 592 512 candidats et aucune
  configuration dans chacun des deux 243, neuf vecteurs à signe près dans le contrôle 3×3. Détails, versions,
  durées et empreintes dans `data/codex_biplane_rerun.json`. C'est une réexécution du code de LAB, pas une seconde
  implémentation indépendante. Les fichiers locaux CRLF ont été comparés aux blobs Git LF après normalisation.
- Le déterminant det L = 9·7^(rang_7(A−3I)−1) et la fenêtre de rang sont déjà dans `papers/rank7/rank7.tex`.
  La voie générale par Hermite avait déjà été évaluée dans la note 110. Nous ne la présentons pas comme nouvelle.
- La borne conditionnelle 33, la réduction de rang 16 et leurs contrôles sont développés ici.
- LAB a refait à la main la preuve de la borne 33, notamment les rangs 23 et 5 et le comptage de Z (message 127).
  Il s'agit d'une seconde lecture par une session d'IA, pas d'un arbitrage humain ni d'une preuve formalisée.
- `code/codex/norm14_audit.py` vérifie les matrices en arithmétique exacte et écrit
  `data/codex_norm14_audit.json`. Il vérifie aussi l'unicité du plan de Fano par les 30 systèmes de triples étiquetés,
  un contrôle positif sur le graphe de la grille 3×3, et un contrôle négatif de la condition de projecteur.

## 2. Tous les petits vecteurs entiers sont couverts

Soit φ ∈ L non nul. Puisque 14 ≠ −4, on a Σφ = 0 ; la norme carrée ||φ||² est paire. Posons
h = max |φ_v| et changeons le signe de φ pour avoir φ_v = h. Notons S la masse positive, égale à la masse négative.
L'équation en v impose S ≥ 4h. L'intégralité donne

    ||φ||² ≥ 2S + h(h−1) ≥ h²+7h.

Donc h ≥ 2 impose une norme au moins 18. En particulier tout vecteur de norme au plus 16 prend ses valeurs dans
{0,1,−1}. Même la norme 18 est impossible avec h ≥ 2 : l'égalité impose un seul 2, six 1 et huit −1, ces huit
derniers tous voisins de v, et aucun 1 voisin de v. Un sommet portant 1, non voisin de v, a au plus deux voisins
négatifs (μ = 2), ce qui contredit une somme de voisins égale à −4. Ainsi h ≥ 2 impose en fait une norme au moins 20.

Supposons maintenant φ = 1_P−1_Q, avec |P| = |Q| = m. Pour p ∈ P, notons a_p son degré dans P ; son degré dans Q
vaut a_p+4. Notons de même a_q pour q ∈ Q. À l'extérieur, les degrés vers P et Q sont égaux, notés t_x.
Le comptage des voisins communs des paires de P et des paires de Q donne exactement

    Σ_ext t_x(t_x−1)
      = 2m(m−7) − 7(e(P)+e(Q)) − Σ_{p∈P} a_p² − Σ_{q∈Q} a_q².

En effet, le total des incidences « paire de P ou Q, voisin commun » vaut 2m(m−1)−e(P)−e(Q).
Les contributions d'un sommet de support de degré intérieur a sont
C(a,2)+C(a+4,2)=a²+3a+6. En sommant Σa=2(e(P)+e(Q)), on obtient l'identité.
Son membre de gauche est positif ou nul : m ≥ 7, donc min L ≥ 14.

À m=7, tous les termes soustraits et tous les t_x(t_x−1) sont nuls. P et Q sont indépendants ; chaque sommet
a quatre voisins de l'autre côté ; à l'extérieur t_x vaut 0 ou 1. Chaque paire de P a ses deux voisins communs
dans Q, et réciproquement. La matrice B d'incidence P–Q vérifie

    B1 = B^t1 = 4·1,     BB^t = B^tB = 2I+2J.

C'est le complément de l'incidence du plan de Fano : J−B est un 2-(7,3,1). Son unicité à renommage près permet
de choisir B_{pq} = p·q sur F_2, pour p,q les sept vecteurs non nuls de F_2³ (les valeurs 0/1 étant ensuite entières).
La borne de rang ci-dessous n'a pas besoin de cette unicité, seulement des identités de B.

## 3. Les 15 sommets communs et le plan de triples

Notons X les sommets extérieurs avec un voisin dans P et un dans Q, et Z ceux sans voisin dans P∪Q.
Chaque p a dix voisins dans X. Il y a donc |X|=70 et |Z|=15.

Un x ∈ X est étiqueté (p,q) par ses deux voisins. Puisque tous les voisins communs de p et q sont dans X,
la cellule (p,q) contient exactement 2−B_{pq} sommets : 28 cellules simples et 21 cellules doubles.

Pour z ∈ Z, comptons ses voisins communs avec les sept sommets de P. Le total vaut 14 et compte exactement
ses voisins dans X, chacun une fois. Tous ses 14 voisins sont donc dans X. **Z est indépendant.**
P∪Z et Q∪Z sont ainsi deux cocliques de taille 22, se coupant en 15 sommets.

Pour x étiqueté (p,q), la somme des nombres de voisins communs avec les sept sommets de P vaut 13. Son voisin q
y contribue pour 4, chacun de ses voisins dans X pour 1, les autres pour 0. Il a donc 9 voisins dans X et 3 dans Z.
Les ensembles T_x = N(x)∩Z sont des triples. Ils forment un **2-(15,3,2)** : chaque point appartient à 14 triples
et chaque paire à deux triples. Les triples sont distincts, car deux sommets ne peuvent avoir trois voisins communs.

Les dix triples d'une ligne p de la grille de cellules couvrent chaque z exactement deux fois (μ(p,z)=2).
La même chose vaut pour chaque colonne q. Dans une cellule double, les deux triples sont disjoints, car les deux
sommets ont déjà p et q comme voisins communs.

Réciproquement, la différence de deux cocliques de Hoffman de taille 22 se coupant en 15 est un vecteur de norme 14
de L. Pour justifier cette dernière assertion sans hypothèse supplémentaire, l'égalité dans la borne spectrale
de Hoffman donne A1_C = 4(1−1_C) pour une coclique C de taille 22 ; on soustrait les deux identités.

## 4. Preuve de la borne de rang 33

Tout ce paragraphe est sur F_7. Sur le cœur C=P∪Q∪Z, le bloc de A−3I est

    F = [ −3I   B     0  ]
        [  B^t −3I    0  ].
        [   0    0  −3I15]

Son noyau est formé des (u,v,0) tels que u=Bv/3 et Jv=0, car
B^tB−9I = 2J modulo 7. Il a dimension 6. **rang F = 23.**

Soit D=A_{C,X}. Sur ce noyau, la coordonnée de D^t(u,v,0) à un sommet de cellule (p,q) est u_p+v_q.
Les 49 cellules sont non vides. Cette expression est donc partout nulle si et seulement si u=a1, v=−a1.
Ces vecteurs appartiennent bien à ker F, puisque −3−4=−7=0. Ainsi

    rang(D^t|ker F) = 6−1 = 5.

Pour toute matrice symétrique par blocs M=[F D;D^t H], on a

    rang M ≥ rang F + 2 rang(D^t|ker F).

Preuve : on sépare par congruence une partie inversible de F de son noyau, puis on élimine le couplage de la partie
inversible. Le bloc restant est [0 K;K^t H′]. Si rang K=t, il contient, après changements de bases, un bloc inversible
[0 I_t;I_t *] de taille 2t. Ceci prouve l'inégalité, indépendamment de H.

Application : **rang_7(A−3I) ≥ 23+2·5 = 33.**

Le script vérifie ces trois rangs et construit un prolongement symétrique arbitraire sur F_7 de rang exactement 33.
Ce prolongement n'est pas une matrice d'adjacence. Il montre que la seule inégalité de blocs ne permet pas
d'annoncer une borne plus grande sans utiliser d'autres contraintes.

## 5. Élimination exacte du cœur : un projecteur de rang 16

Dans un vrai graphe, E=(27I−9A+J)/63 est le projecteur orthogonal sur l'espace propre −4.
Sur C, posons G=63E_CC=27I−9A_CC+J. Il est positif, de rang 28, et son noyau est engendré par

    k = (3·1_P, 3·1_Q, −1_Z).

On peut le voir en séparant les espaces de sommes nulles de P,Q et Z : les valeurs propres non nulles sont
27±9√2 (six fois chacune), 27 (quatorze fois), 63 et 47. Sur les vecteurs constants de P∪Q et Z, le bloc est
[5 15;14 42], de valeurs propres 0 et 47.

Supprimons un sommet z_* du cœur, et appelons I les 28 coordonnées restantes. Alors

    det G_II = 3^67·7^7.

Pour un sommet x de cellule (p,q) et de triple T_x, écrivons
g_x = 1_C−9(e_p+e_q+1_{T_x}). On a k^t g_x=0. Le complément de Schur est donc bien défini par

    R_xy = E_xy − (g_x|I)^t (G_II)^−1 (g_y|I) / 63.

Dans un vrai graphe, R est le projecteur orthogonal sur les fonctions propres −4 nulles sur C, restreintes à X.
Son rang est 44−28=16. C'est une propriété générale de l'élimination d'un sous-ensemble de coordonnées d'un
projecteur orthogonal : si E=UU^t, on projette les colonnes sur ker U_C ; sur cet espace U_X est une isométrie.

La formule fermée suivante ne demande aucune inversion lors d'une recherche. Pour x=(p,q,c), y=(p′,q′,c′),
H=A_XX et h_xy=|T_x∩T_y|, posons K=147R. Alors

    K_xy = 63[x=y] + 12 − 21H_xy − 7h_xy
           − 9[p=p′] − 9[q=q′] − 3(B_pq′+B_p′q).

En particulier R_xx=10/49 si B_pq=1, et R_xx=12/49 sinon. Il y a respectivement 28 et 42 sommets, donc tr R=16.
Le script compare tous les coefficients de cette formule avec l'inversion rationnelle du bloc G_II.

## 6. Équivalence finie pour la branche de norme 14

Fixons B comme ci-dessus et les 70 étiquettes (p,q,c), 0≤c<2−B_pq. Choisissons :

1. Un triple T_x dans un ensemble Z de 15 points, pour chaque x, chaque point appartenant à 14 triples.
2. Un graphe simple H, 9-régulier, sur les 70 étiquettes.

Construisons K par la formule du §5. **Il existe un srg(99,14,1,2) de norme minimale 14 si et seulement si un tel
choix vérifie K²=147K.** Les contraintes de plan de triples du §3 peuvent être ajoutées comme filtres nécessaires.

Sens direct : les §§2–5 donnent ces objets et le projecteur R=K/147.

Sens inverse : construisons A avec le cœur Fano et Z indépendant, les attaches de chaque x à p,q,T_x, puis H.
Tous les degrés valent 14. La matrice 27I−9A+J a un bloc de rang 28, les colonnes croisées sont dans son image,
et son complément de Schur est 63R. Si R²=R, sa trace 16 donne rang R=16. La matrice entière a donc rang 44.
Comme A est 14-régulière, cela force exactement 54 valeurs propres égales à 3. Pour les 44 autres valeurs propres
non principales λ_i, les traces de A et A² donnent

    Σλ_i = −176,     Σλ_i² = 704,     Σ(λ_i+4)² = 0.

Toutes valent −4, donc A²+A=12I+2J. C'est le SRG voulu. Enfin 1_P−1_Q est directement un vecteur propre −4
de norme 14, car chaque x rencontre P et Q une fois. L'inégalité du §2 assure que c'est bien le minimum.

La trace seule n'est pas suffisante : notre contrôle synthétique régulier a tr R=16 mais
(R²−R)_00=128/343, et ne vérifie pas l'identité du SRG.

## 7. Ce qui reste ouvert

La borne 33 est une conséquence de l'existence d'un vecteur minimal de norme 14. Elle ne force pas ce vecteur,
et laisse les rangs 33,35,37,39,41,43 possibles dans cette branche. La branche min L≥16 reste entière.

Le projecteur de rang 16 fournit un problème plus petit en dimension, mais comporte encore 70 triples et les arêtes
de H. Aucune estimation de coût, aucun résultat SAT/UNSAT et aucune classification de réseau de rang 16 n'en
découlent automatiquement. Les contrôles exacts valident les formules, pas l'inexistence d'une complétion.
