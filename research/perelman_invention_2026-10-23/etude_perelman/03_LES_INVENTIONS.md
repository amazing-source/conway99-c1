# Partie III — Les inventions : obstacle → idée → définition → propriété → conséquence → rôle

Chaque fiche suit la chaîne demandée. La ligne **origine** distingue ce qui est documenté [D] de l'interprétation
[Int]. La ligne **nature** classe l'apport :
- **N** : idée véritablement nouvelle ;
- **P** : perfectionnement d'un outil existant ;
- **A** : application ingénieuse d'un théorème connu ;
- **T** : argument technique indispensable.

---

## Fiche 1. L'entropie $\mathcal W$ et l'insertion de l'échelle

- **Obstacle.** Aucune quantité monotone globale pour le flot de Ricci en dimension quelconque. $\mathcal F$ (et
  $\lambda$) ne voit pas les solitons contractants, qui sont précisément les modèles de singularités à courbure
  positive.
- **Idée.** Ajouter à la métrique une *fonction* (mesure) et une *échelle* $\tau$, qui évoluent toutes deux : la mesure
  par l'équation de la chaleur adjointe, l'échelle par $\tau_t = -1$. Rendre la fonctionnelle invariante par changement
  d'échelle.
- **Définition.** $\mathcal W(g,f,\tau) = \int[\tau(|\nabla f|^2 + R) + f - n](4\pi\tau)^{-n/2}e^{-f}$ ;
  $\mu = \inf_f\mathcal W$ ; $\nu = \inf_\tau\mu$.
- **Propriété.** $\frac d{dt}\mathcal W = 2\tau\int|\mathrm{Ric} + \nabla^2 f - \frac{g}{2\tau}|^2u \geq 0$. Égalité
  si et seulement si soliton contractant de gradient. $\mu(g,\tau) \to 0$ quand $\tau \to 0$ (Gross).
- **Conséquences.** Pas de respirateur (I.2–3) ; non-effondrement I.4.1 ; inégalité de Harnack adjointe (I.9) ;
  pseudolocalité (I.10).
- **Rôle.** Première solution de (M1). Logiquement remplaçable, pour Poincaré et la géométrisation, par le volume
  réduit (fiche 3) [D, KL §2 et §4]. Indispensable pour la pseudolocalité, qui sert dans la solution standard (II.2,
  Affirmation 4).
- **Origine.** $\mathcal F$ : théorie des cordes et Bakry–Émery [D, I.1.4*]. Sobolev logarithmique : Gross ; usage dans
  un flot géométrique chez Ecker [D, I.3.3*]. L'heuristique annoncée est le groupe de renormalisation : « Ricci flow must
  be gradient-like » [D, I.0.2].
- **Nature.** **N** (la fonctionnelle, l'échelle couplée, la monotonie) ; **A** (Gross).

## Fiche 2. Le non-effondrement (« Little Loop Lemma »)

- **Obstacle.** (M1) : le théorème de compacité de Hamilton exige un rayon d'injectivité minoré au point de base. Sans
  lui, il n'y a pas de limites d'éclatement et rien n'exclut les modèles effondrés (cigare $\times\mathbb R$).
- **Idée.** Transformer l'énoncé géométrique « volume relatif minoré » en un énoncé *intégral* sur une quantité monotone,
  en évaluant cette quantité sur une fonction test concentrée dans la boule.
- **Définition.** $\kappa$-non-effondrement à l'échelle $\rho$ (I.4.2, I.8.1).
- **Propriété.** Sur un intervalle de temps fini, il existe $\kappa > 0$ (I.4.1) ; versions localisées (I.8.2, I.10.4) ;
  version avec chirurgie (II.5.2, II.6.3(a)).
- **Conséquences.** Limites d'éclatement (I.4.2) ; les $\kappa$-solutions comme classe de modèles ; exclusion du
  cigare.
- **Rôle.** Pierre angulaire : « One of the outstanding achievements of [I] » [D, KL §3.3].
- **Origine.** L'énoncé est la conjecture de Hamilton [D, CZ] ; la méthode est nouvelle.
- **Nature.** **N** (théorème et mécanisme).

## Fiche 3. Longueur $\mathcal L$, distance réduite, volume réduit

- **Obstacle.** $\mathcal W$ est global : il ne se localise pas bien près des chirurgies, et il ne donne pas
  directement une structure asymptotique pour les solutions anciennes.
- **Idée.** Une géométrie de comparaison *en espace-temps* : des chemins rétrogrades pondérés par
  $\sqrt\tau(R + |\dot\gamma|^2)$, comme une distance riemannienne. Le flot y joue le rôle d'un espace « Ricci-plat »,
  ce qui suggère un Bishop–Gromov. L'heuristique vient de la limite $N \to \infty$ de I.6.
- **Définition.** $\mathcal L$, $l = L/2\sqrt\tau$, $\tilde V(\tau) = \int\tau^{-n/2}e^{-l}$.
- **Propriété.** $\tilde V$ monotone. Égalité si et seulement si soliton contractant, de potentiel $l$. Inégalités
  (7.13)–(7.16). $\min l \leq n/2$. Sous courbure $\geq 0$ : $|\nabla l|^2 + R \leq Cl/\tau$.
- **Conséquences.** Non-effondrement localisé (I.7.3, I.8.2) ; soliton asymptotique des $\kappa$-solutions (I.11.2) ;
  non-effondrement à travers les chirurgies (II.5.2–5.3).
- **Rôle.** Outil central de toute la suite [D, MT intro : « the tool by which he establishes the needed non-collapsing
  results »].
- **Origine.** Li–Yau (longueur d'une équation parabolique) [D, I.7.4*] ; Huisken, avec monotonie inversée [D, I.6.4*] ;
  Chow–Chu (interprétation géométrique de la Harnack) [D, I.6.4*] ; Harnack de Hamilton, qui apparaît comme terme de
  seconde variation [D, I.7.1].
- **Nature.** **N**. La compensation des termes en $K$ (Harnack de Hamilton) entre la dérivée de $l$ et le jacobien
  est le cœur technique.

## Fiche 4. Harnack différentielle pour la solution fondamentale adjointe

- **Obstacle.** Localiser la monotonie de $\mathcal W$ autour d'un point.
- **Idée.** Une version ponctuelle de (3.4) : la densité $v$ de $\mathcal W$ est une sous-solution de l'équation
  adjointe.
- **Définition et propriété.** $\Box^*v = -2\tau|\mathrm{Ric} + \nabla^2 f - g/2\tau|^2u \leq 0$ ; $v \leq 0$ pour une
  solution fondamentale ; $f \leq l$.
- **Conséquences.** Pseudolocalité ; comparaison de $f$ et $l$.
- **Origine.** Li–Yau, Hamilton, Ecker [D, I.9.7*].
- **Nature.** **N** (énoncé), **P** (technique).

## Fiche 5. Pseudolocalité

- **Obstacle.** Montrer qu'une région presque euclidienne ne devient pas singulière instantanément, quoi qu'il se passe
  ailleurs. C'est nécessaire pour la solution standard (II.2, Affirmation 4) et pour la robustesse locale.
- **Idée.** Choix d'un point extrémal + solution fondamentale adjointe centrée en ce point + monotonie localisée par
  coupure. La contradiction vient de l'inégalité de Sobolev logarithmique gaussienne, qui est rigide.
- **Propriété.** I.10.1, I.10.3.
- **Rôle.** Contrôle local dans la solution standard et dans les régions presque plates.
- **Origine.** Ecker–Huisken pour le flot de courbure moyenne [D, I.10.6*].
- **Nature.** **N**.

## Fiche 6. Les $\kappa$-solutions et leur soliton asymptotique

- **Obstacle.** (M2) : les solutions anciennes générales sont trop générales.
- **Idée.** (a) Imposer le non-effondrement à toutes les échelles, puisque les limites d'éclatement en héritent.
  (b) Étudier l'écrasement (*blow-down*) d'une solution ancienne par le volume réduit : monotone et borné, il devient
  constant à la limite, et l'égalité est rigide.
- **Définitions.** $\kappa$-solution ; soliton asymptotique.
- **Propriétés.** Soliton asymptotique non plat (I.11.2). $\mathcal V = 0$ (I.11.4). Compacité modulo l'échelle
  (I.11.7). Liste des solitons asymptotiques possibles en dimension 3 (II.1.2–1.3). Constantes universelles et quatre
  types de voisinages (II.1.5).
- **Conséquences.** Une description grossière mais *uniforme* de toutes les limites d'éclatement.
- **Rôle.** C'est la liste des modèles de singularités. **Elle ne demande pas la classification fine** (l'unicité de
  Bryant, I.11.9, n'est pas nécessaire).
- **Origine.** Solutions anciennes et réduction de dimension : Hamilton [D, I.11.10*]. Exclusion des cônes : principe
  du maximum fort de Hamilton. Solitons en dimension 2 : Hamilton. **Nouveau** : la classe des $\kappa$-solutions, le
  soliton asymptotique, la compacité, II.1.2 (Gauss–Bonnet sur les niveaux de $f$).
- **Nature.** **N** (structure), **A** (Hamilton, Toponogov, Gauss–Bonnet).

## Fiche 7. Voisinages canoniques et « courbure bornée à distance bornée »

- **Obstacle.** (M3) : passer des modèles (limites) à un énoncé uniforme sur le flot réel, en tout point de grande
  courbure, sans se placer au maximum de courbure.
- **Idée.** (a) Par l'absurde, choisir le contre-exemple de courbure presque minimale. La conclusion vaut alors à toutes
  les échelles plus fines, d'où des estimées de dérivées locales : c'est une **induction sur les échelles**.
  (b) Montrer qu'une courbure beaucoup plus grande ne peut pas se trouver à distance bornée, car la limite contiendrait
  un **cône** à courbure $\geq 0$ évoluant par le flot, ce que le principe du maximum fort interdit. L'argument passe par
  la géométrie d'Alexandrov.
- **Propriété.** I.12.1 ; II.4.2 (Affirmation 2) ; II.5.4 (avec chirurgie).
- **Conséquences.** Structure de la région de haute courbure (II.3) ; possibilité de couper ; constantes uniformes.
- **Rôle.** L'autre avancée majeure, selon [D, MT intro].
- **Origine.** Le choix d'un point et les éclatements sont classiques en analyse géométrique [D, KL §3.3]. La méthode
  du maximum de Hamilton ne suffit pas [D, MT]. L'argument conique avec Alexandrov est propre à Perelman.
- **Nature.** **N**.

## Fiche 8. La solution standard

- **Obstacle.** (M4) : après une chirurgie, la région opérée doit être contrôlée sans connaître le passé.
- **Idée.** Toutes les chirurgies collent à l'échelle $h$ la même calotte, dont le flot est connu une fois pour toutes.
- **Définition.** Calotte standard sur $\mathbb R^3$ ; solution standard (II.2).
- **Propriétés.** Symétrie, unicité, existence sur $[0,1)$, voisinages canoniques sauf pour les cous non forts.
- **Rôle.** Rend les hypothèses a priori vérifiables près des zones opérées (II.4.5–4.7, II.5.4).
- **Origine.** La technique de collage préservant le pincement est due à Hamilton [D, II.4.4 ; MT].
- **Nature.** **N** (le rôle du modèle universel), **T** (existence et unicité).

## Fiche 9. Chirurgie à $\delta$-coupure et séparation des échelles

- **Obstacle.** (M4) : couper assez profondément (cous forts, presque cylindriques) sans perdre les estimées, et sans
  accumulation.
- **Idée.** Deux échelles très séparées : $h \ll r$. Le voisinage canonique est contrôlé à l'échelle $r$, et on coupe à
  l'échelle $h$, où les cous sont *forts* par le Lemme II.4.3 (cous profonds dans les cornes). Chaque chirurgie consomme
  au moins $h^3$ de volume.
- **Propriétés.** Discrétude des chirurgies ; l'ordre de choix des paramètres.
- **Rôle.** Existence du flot avec chirurgie pour tout temps (II.6.1).
- **Origine.** La chirurgie est de Hamilton (1997) ; Perelman signale une lacune dans son argument [D, II intro].
  Nouveau : les deux échelles, le choix des cous forts, l'induction en temps.
- **Nature.** **P** (sur Hamilton) + **N** (structure inductive).

## Fiche 10. Non-effondrement et voisinages canoniques *à travers* la chirurgie

- **Obstacle.** La chirurgie détruit la régularité du flot. Les estimées a priori doivent être *démontrées* pour le flot
  que l'on construit en les supposant.
- **Idée.** Une récurrence sur des intervalles dyadiques $[2^{j-1}\varepsilon, 2^j\varepsilon]$, avec des paramètres
  décroissants. Le non-effondrement passe par des courbes admissibles et par $\mathcal L_+$ (avec $R_+$) : les courbes
  qui frôlent une calotte récente ont une longueur énorme (II.5.3).
- **Propriétés.** II.5.1 et II.6.3.
- **Rôle.** Fermer le cercle « supposer, construire, démontrer ».
- **Nature.** **N** (architecture), **T** (estimées).

## Fiche 11. Temps long sans courbure normalisée bornée

- **Obstacle.** (M5).
- **Idée.** Ne pas borner la courbure normalisée, mais décrire la partie où elle n'est pas bornée : elle est
  *localement effondrée à courbure minorée*, et la géométrie d'Alexandrov la reconnaît comme variété graphée.
- **Propriétés.** I.13.1 ; II.6–7 ; théorème d'effondrement (II.7.4).
- **Rôle.** La géométrisation complète.
- **Origine.** Hamilton 1999 pour la partie épaisse (hyperbolique, tores incompressibles) [D] ; Perelman pour
  l'effondrement (« our earlier (partly unpublished) work ») [D, I.0.1].
- **Nature.** **P** (Hamilton), **A** (théorie d'Alexandrov).

## Fiche 12. Valeur propre $\lambda$ et constante Sigma (II.8)

- **Idée.** Le flot de Ricci est le flot de gradient de $\lambda$ ; $\lambda$ survit aux chirurgies fines. On obtient une
  caractérisation topologique par $\sup\lambda V^{2/3}$.
- **Rôle.** Une seconde voie vers l'incompressibilité et la description (II.8.2), qui évite rigidité hyperbolique et
  surfaces minimales.
- **Origine.** Conjectures d'Anderson [D, II.8.2].
- **Nature.** **A/N**.

## Fiche 13. Extinction en temps fini par un min-max topologique

- **Obstacle.** (M6), pour un raccourci vers Poincaré.
- **Idée.** Utiliser une classe d'homotopie non triviale de l'espace des lacets (Serre) pour définir une aire min-max,
  strictement positive tant que la variété existe. La géométrie (Gauss–Bonnet sur les disques minimaux) donne une
  dérive négative universelle.
- **Définition.** $A(\alpha, g) = \inf_{\Gamma\in\alpha}\sup_{c\in\Gamma}A(c,g)$.
- **Propriété.** $\frac{d}{dt}A \leq -2\pi - \frac12R_{\min}A$.
- **Rôle.** Poincaré et l'elliptisation sans l'analyse en temps long.
- **Origine.** Estimée de Hamilton 1999 §11 ; régularisation d'Altschuler–Grayson ; preuve indépendante de
  Colding–Minicozzi [D, III intro ; KL intro].
- **Nature.** **A** (« pas d'idée substantiellement nouvelle », dit Perelman), mais le passage à un min-max sur une
  classe d'homotopie est l'idée qui fait marcher l'argument.

---

## Synthèse 1 : ce qui est devenu démontrable

| nouvel objet | devenu démontrable | inaccessible avant parce que |
|---|---|---|
| $\mathcal W$, $\mu$ | non-effondrement aux temps finis ; pas de respirateurs en toute dimension | aucune quantité monotone ne contrôlait le volume local |
| volume réduit | non-effondrement local et robuste ; soliton asymptotique ; non-effondrement avec chirurgie | $\mathcal W$ est global ; aucune structure asymptotique des solutions anciennes |
| Harnack adjointe | localisation de $\mathcal W$ ; pseudolocalité | pas de densité monotone |
| $\kappa$-solutions et compacité | constantes universelles ; liste des voisinages | les solutions anciennes générales ne sont pas compactes |
| courbure bornée à distance bornée | éclatements en des points *non maximaux* | Hamilton n'éclatait qu'aux maxima |
| solution standard et $\delta$-coupure | chirurgies infinies en nombre, discrètes, contrôlées | pas de modèle post-chirurgie, ni d'estimées qui survivent |
| min-max sur $\pi_*(\Lambda M, M)$ | extinction en temps fini | l'estimée d'aire existait, sans quantité à laquelle l'appliquer globalement |

## Synthèse 2 : classement des apports

- **N** (vraiment nouveau) : fiches 1, 2, 3, 6, 7, 10 ; le rôle du modèle standard (8) ; l'architecture à deux
  échelles (9).
- **P** (perfectionnement) : chirurgie (Hamilton) ; temps long (Hamilton 1999) ; Harnack (Li–Yau, Hamilton).
- **A** (application ingénieuse) : Gross ; Gauss–Bonnet en II.1.2 et III.1.2 ; Serre ; Toponogov et Alexandrov ;
  Altschuler–Grayson ; Meeks–Yau.
- **T** (technique indispensable) : existence et unicité de la solution standard ; courbes admissibles et
  $\mathcal L_+$ ; choix des paramètres ; régularisation par rampes.

## Synthèse 3 : pourquoi ces objets ? Ce que disent les textes, ce qu'on peut en conclure

**Documenté [D].**
1. Le flot devait être « gradient-like » à cause de l'analogie avec le groupe de renormalisation (I.0.2).
2. $\mathcal F$ vient de l'action effective des cordes (I.1.4*).
3. $\mathcal W$ est « moins une entropie » d'un ensemble canonique (I.5).
4. Le volume réduit est issu de Bishop–Gromov dans un espace formel Ricci-plat (I.6).
5. $\mathcal L$ est la « longueur » de Li–Yau (I.7.4*).
6. Le cas d'égalité des monotonies est toujours un soliton (I.2, I.3, I.7).
7. La géométrie d'Alexandrov est son outil de base (I.12.1 Affirmation 2, II.6.6, II.7.4).

**Interprétation [Int].**
1. **Chercher la monotonie là où la physique la promet.** L'analogie avec le groupe de renormalisation prédit qu'une
   « entropie » doit décroître quand on passe à des échelles plus grossières. Perelman a cherché la fonctionnelle dont la
   dissipation est le carré du défaut de soliton.
2. **Ajouter des variables pour rendre le problème variationnel** : la fonction $f$ (mesure, dilaton), puis l'échelle
   $\tau$.
3. **Faire de chaque monotonie un instrument de mesure local**, par une fonction test ou une solution fondamentale
   centrée au point.
4. **N'exiger des modèles que ce que la suite consomme** : une classification grossière, des constantes universelles.
5. **Organiser la preuve comme une induction sur les échelles** (voisinages canoniques, puis chirurgie dyadique), où
   l'hypothèse aux échelles fines fournit les estimées à l'échelle courante.

**Hypothèses [Hyp], non vérifiables** : que l'ordre de découverte ait suivi l'ordre de l'article ($\mathcal F$, puis
$\mathcal W$, puis $\tilde V$). Les remarques I.6 et I.7.4* suggèrent que $\tilde V$ est venu de l'heuristique de
dimension infinie et de Li–Yau, mais le texte ne date rien.
