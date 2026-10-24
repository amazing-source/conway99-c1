# Partie I — Le mur : le programme de Hamilton avant novembre 2002

## 0. Méthode, sources et statuts

**Sources primaires, lues intégralement** (sources LaTeX récupérées sur arXiv le 23/10/2026, copies de travail hors
dépôt) :
- [I] G. Perelman, *The entropy formula for the Ricci flow and its geometric applications*, arXiv:math/0211159 (11/2002).
- [II] G. Perelman, *Ricci flow with surgery on three-manifolds*, arXiv:math/0303109 (03/2003).
- [III] G. Perelman, *Finite extinction time for the solutions to the Ricci flow on certain three-manifolds*,
  arXiv:math/0307245 (07/2003).

On cite « I.7.3 » pour la section 7.3 de [I], « II.4.3 » pour [II], « III.1.2 » pour [III], comme Kleiner–Lott.

**Reconstructions consultées pour contrôler les attributions et la logique** (sources arXiv lues aux endroits cités) :
- [KL] B. Kleiner, J. Lott, *Notes on Perelman's papers*, Geom. Topol. 12 (2008), arXiv:math/0605667 (version 2013) :
  introduction, guide de lecture, aperçus §3–§5.
- [MT] J. Morgan, G. Tian, *Ricci flow and the Poincaré conjecture*, Clay Math. Monographs 3 (2007),
  arXiv:math/0607607 : chapitre d'introduction (« Perelman's advances », « Bounded curvature at bounded distance »).
- [Tao] T. Tao, *Perelman's proof of the Poincaré conjecture: a nonlinear PDE perspective*, arXiv:math/0610903.
- [CZ] H.-D. Cao, X.-P. Zhu, *A complete proof of the Poincaré and geometrization conjectures*, Asian J. Math. 10
  (2006), arXiv:math/0612069 (pour la dénomination « Little Loop Lemma »).
- Mentionnés sans relecture de détail : Bessières–Besson–Boileau–Maillot–Porti (*Geometrisation of 3-manifolds*, 2010),
  Colding–Minicozzi (extinction finie, 2005 et 2008), Shioya–Yamaguchi (effondrement, 2005).

**Statuts employés dans cette étude.**
- **[D]** documenté : dit explicitement dans [I], [II], [III] (avec section) ou dans une reconstruction citée.
- **[R]** reconstruction mathématique : conséquence vérifiable des textes, refaite ici.
- **[Int]** interprétation conceptuelle de l'auteur de cette étude. Ce n'est pas un fait historique.
- **[Hyp]** hypothèse sur le processus de découverte. Aucune n'est présentée comme un fait.

Perelman n'a laissé presque aucun témoignage sur sa manière de chercher. Les seuls matériaux « de motivation » sont dans
les textes eux-mêmes : I.0.2 (analogie avec le groupe de renormalisation), I.5 (analogie statistique), I.6 (espace
formel de dimension infinie), et les paragraphes historiques marqués « * » (I.1.4*, I.3.3*, I.5.3*, I.6.4*, I.7.4*,
I.9.7*, I.10.6*, I.11.10*, I.13.3*). Tout ce qui va au-delà relève de [Int] ou [Hyp].

---

## 1. L'équation et l'outillage de base

Le flot de Ricci est l'équation $\partial_t g_{ij} = -2R_{ij}$ (Hamilton 1982).

**Acquis avant Perelman [D, I.0.1 ; MT ch. 3].**
- *Existence et unicité en temps court* sur une variété close (Hamilton 1982, par Nash–Moser) ; simplification par
  l'astuce de DeTurck (1983), qui rend l'équation strictement parabolique modulo difféomorphismes (I.1.4*).
- *Équations d'évolution* : $\partial_t \mathrm{Rm} = \Delta \mathrm{Rm} + Q(\mathrm{Rm})$, $Q$ quadratique ; en
  particulier $\partial_t R = \Delta R + 2|\mathrm{Ric}|^2$, donc $\min R$ ne décroît pas.
- *Principe du maximum pour les tenseurs* (Hamilton 1982, 1986) ; *principe du maximum fort* (Hamilton 1986) : une
  solution à opérateur de courbure $\geq 0$ qui s'annule quelque part se scinde localement.
- *Estimées locales des dérivées* de W.-X. Shi (1989) : une borne de courbure sur un cylindre parabolique contrôle
  toutes les dérivées à l'intérieur.

## 2. Les théorèmes de convergence

- **Hamilton 1982** : une 3-variété close à $\mathrm{Ric} > 0$ converge, après normalisation, vers une métrique de
  courbure constante. Les valeurs propres de Ric sont *pincées* quand la courbure devient grande [D, I.0.1].
- **Hamilton 1986** : même conclusion en dimension 4 pour un opérateur de courbure $> 0$.
- **Surfaces** (Hamilton 1988, complété par Chow 1991) : le flot normalisé converge vers une métrique de courbure
  constante. Hamilton y montre aussi que la sphère ronde est le seul soliton contractant orienté, non plat, de courbure
  $\geq 0$ en dimension 2 (utilisé en I.11.3) et construit le **soliton cigare** $\mathbb{R}^2$,
  $g = (dx^2+dy^2)/(1+x^2+y^2)$, soliton stationnaire asymptote à un cylindre plat $S^1 \times \mathbb{R}$ [Tao §3].

## 3. L'outillage pour les singularités (1993–1995)

1. **Inégalité de Harnack différentielle** (Hamilton 1993), pour un opérateur de courbure $\geq 0$. Sa forme tracée :
   $R_t + 2\langle X, \nabla R\rangle + 2\,\mathrm{Ric}(X,X) + R/t \geq 0$ ; pour une solution ancienne,
   $R_t + 2\langle X, \nabla R\rangle + 2\,\mathrm{Ric}(X,X) \geq 0$ et donc $R_t \geq 0$ (I.11.1). Elle compare la
   courbure en des points et des temps différents. Modèle : l'inégalité de Li–Yau (1986).
2. **Théorème de compacité** (Hamilton 1995, Amer. J. Math.) : une suite de flots pointés converge (modulo
   difféomorphismes) vers un flot complet si (A) les courbures sont uniformément bornées sur des cylindres paraboliques
   et (B) **le rayon d'injectivité au point de base est minoré** [D, I.0.1 ; KL §3.3]. Si l'intervalle de temps
   rééchelonné tend vers l'infini, la limite est *ancienne*, c'est-à-dire définie sur $(-\infty, T)$.
3. **Pincement de Hamilton–Ivey** (Ivey 1993, Hamilton 1995), propre à la dimension 3 :
   $\mathrm{Rm} \geq -\phi(R)\,R$, avec $\phi$ décroissante vers 0 comme $1/\log$. La partie négative de la courbure
   est négligeable devant $R$ là où $R$ est grand. Conséquence : **toute limite d'éclatement a une courbure sectionnelle
   $\geq 0$** [D, I.0.1].
4. **« Formation of singularities »** (Hamilton 1995, Surveys in Diff. Geom. 2) : types de singularités (I, II, III),
   réduction de dimension (scinder une droite dans une limite), solutions anciennes et éternelles, et des **conjectures
   sur la structure des limites d'éclatement en dimension 3 (§26)**, que [I] confirme [D, I.0.1]. On y trouve aussi la
   conjecture d'une estimée locale du rayon d'injectivité que Hamilton appelle **« Little Loop Lemma »** [D, CZ
   introduction : « Perelman removed these two stumbling blocks [...] by establishing a local injectivity radius
   estimate (also called 'Little Loop Lemma' by Hamilton) »].
5. **Formules de monotonie** : Hamilton (1993, CAG 1) étudie des formules de monotonie pour des flots paraboliques
   construites avec des solutions de l'équation de la chaleur rétrograde (I.9.7*). Huisken (1990) a une telle formule
   pour le flot de courbure moyenne [D, I.6.4*]. **Aucune formule de monotonie globale n'était connue pour le flot de
   Ricci en dimension quelconque.** En dimension 2, Chow (1991) avait une entropie ; Perelman note qu'elle semble sans
   rapport avec la sienne [D, I.5.3*].

## 4. La chirurgie

- Hamilton (1997, *Four-manifolds with positive isotropic curvature*) définit la **chirurgie** : couper un cou presque
  rond, coller des calottes, relancer le flot. Il montre qu'on peut la faire en **préservant le pincement**, en
  déformant la métrique par un facteur conforme $e^{-f(z)}$ près du milieu du cou [D, II.4.4 ; MT intro].
- Il espérait la même procédure en dimension 3 sans hypothèse de courbure, avec un nombre fini de chirurgies et une
  solution finalement non singulière [D, I.0.1].
- Perelman relève une affirmation non justifiée dans l'argument de Hamilton (« $R_{MAX} = \Gamma$, page 62 ») qu'il dit
  n'avoir pas su réparer, et adopte une approche différente [D, II, introduction].

## 5. Le comportement en temps long

Hamilton (1999, *Non-singular solutions of the Ricci flow on three-manifolds*) traite les solutions définies pour tout
$t$ **à courbure normalisée bornée** $|\mathrm{Rm}| \leq C/t$ :
- décomposition épaisse/mince ;
- la partie épaisse converge vers des variétés hyperboliques de volume fini ;
- les tores de bord sont incompressibles (argument de surfaces minimales, Meeks–Yau) ;
- c'est suffisant pour exclure un contre-exemple à la géométrisation **parmi ces solutions** [D, I.0.1 ; I.13.1].

Le même article contient l'estimée de décroissance de l'aire des disques minimaux, $\tfrac{d}{dt}A \leq -2\pi - \tfrac12
R_{\min} A$ à une constante près, que Perelman réutilise en III.1.2 [D, III.1.2 « cf. [H, §11] »].

## 6. Les murs, formulés exactement

Le programme de Hamilton s'écrit : lancer le flot, comprendre les singularités, faire des chirurgies, comprendre le
temps long. Voici les obstacles précis, dans l'ordre logique.

**(M1) Non-effondrement aux éclatements.**
- Pour comprendre une singularité, on rééchelonne au voisinage d'un point de courbure $Q_k \to \infty$ par le facteur
  $Q_k$ (en temps et en espace) et on veut une limite.
- Le théorème de compacité exige (B) : un rayon d'injectivité minoré au point de base. Sous une borne de courbure, cela
  équivaut à une minoration du rapport de volume $r^{-n}\mathrm{Vol}\,B(x,r)$ (Cheeger–Gromov–Taylor) [KL §3.3].
- **Sans (B), on n'a pas de limite, et les limites possibles incluent des modèles effondrés**, comme le produit d'un
  cigare et d'une droite : solution ancienne, effondrée aux grandes échelles, qu'**aucune chirurgie ne peut enlever**
  [D, Tao §3, « non-example »].
- C'est le « Little Loop Lemma » conjecturé par Hamilton. Il manquait une **estimée a priori**, pas un calcul.

**(M2) Classification des limites.**
- On savait que les limites (si elles existent) ont une courbure $\geq 0$ (Hamilton–Ivey) et vérifient l'inégalité de
  Harnack.
- Une solution ancienne générale est difficile à analyser [D, I.0.1]. Il n'existait pas de classification, même
  grossière, des solutions anciennes à courbure positive en dimension 3.
- Hamilton éclatait en des **points de courbure (presque) maximale** [D, MT « Bounded curvature at bounded distance » :
  « Hamilton avoided this problem by always focusing on points of maximal curvature. That method will not work in this
  case »]. Cette méthode ne voit pas les singularités *locales*, qui se forment dans une région pendant que la courbure
  reste bornée ailleurs.

**(M3) Contrôle quantitatif de la région de haute courbure.** Pour couper, il faut savoir que *chaque* point de grande
courbure a un voisinage standard (cou, calotte), avec des constantes **uniformes** en temps, et **qui restent vraies
après les chirurgies**.

**(M4) La chirurgie elle-même.**
- Préserver les estimées a priori (pincement, non-effondrement, voisinages canoniques) à travers la chirurgie.
- Éviter l'accumulation des temps de chirurgie.
- Garder une topologie contrôlée : couper le long de 2-sphères seulement, ce qui donne des sommes connexes [MT intro].

**(M5) Temps long sans hypothèse de courbure normalisée bornée.** Perelman écrit qu'il n'a pas su confirmer l'espoir de
Hamilton que la courbure normalisée reste bornée. Il contourne : la région où elle ne l'est pas est localement effondrée
à courbure minorée, et son travail antérieur (en partie non publié) sur les espaces d'Alexandrov suffit pour la topologie
[D, I.0.1, II.7.4].

**(M6) Raccourci pour Poincaré : l'extinction en temps fini** pour les variétés sans facteur asphérique [III].

## 7. Ce qui était presque accessible, et ce qui demandait une idée

Lecture [Int], appuyée sur [KL §3–4] et [MT intro].

| étape | outils disponibles en 2001 | ce qui manquait |
|---|---|---|
| limite d'éclatement, une fois (M1) acquis | compacité de Hamilton, estimées de Shi | **(M1) lui-même** |
| courbure $\geq 0$ des limites | Hamilton–Ivey | rien |
| comparaison de courbure dans les limites | Harnack de Hamilton | rien |
| solitons contractants en dimension 2 | Hamilton 1988 | rien |
| scindage et réduction de dimension | principe du maximum fort, Toponogov | rien |
| classification grossière des solutions anciennes non effondrées | — | **un mécanisme qui force une structure asymptotique** |
| bornes de courbure « à distance bornée » autour d'un point non maximal | — | **un argument nouveau** (cônes exclus) |
| voisinages canoniques uniformes, et après chirurgie | — | **une induction sur les échelles** |
| non-effondrement à travers les chirurgies | — | **une quantité qui survit aux chirurgies** |
| décroissance d'aire de disques minimaux | Hamilton 1999 §11 | l'idée de l'appliquer à un min-max topologique |
| effondrement à courbure minorée | théorie d'Alexandrov (Perelman et coll.) | sa mise en forme pour ce contexte |

**La colonne de droite est le mur.** Elle contient une seule estimée a priori (M1), dont dépend presque tout le reste,
puis trois mécanismes nouveaux (classification asymptotique, bornes à distance bornée, induction sur les échelles), et
la survie de ces estimées à la chirurgie.
