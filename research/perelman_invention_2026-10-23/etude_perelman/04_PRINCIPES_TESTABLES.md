# Partie IV — Mécanismes généraux : dix schémas testables

Chaque schéma est tiré d'un argument précis de Perelman. Il est formulé avec ses hypothèses structurelles, pour qu'on
puisse vérifier sur un autre problème si elles sont satisfaites. La rubrique « propre au flot » dit ce qui n'est **pas**
transférable sans un équivalent. La rubrique « déjà transféré » donne les domaines où le schéma a effectivement marché
hors du flot de Ricci : c'est la justification de sa généralité.

Notations abstraites :
- $\mathcal X$ : espace de configurations ;
- $\Phi_t$ : une évolution sur $\mathcal X$ ;
- $G$ : un groupe de symétries (jauge, échelle) qui commute avec $\Phi$ ;
- $\mathcal Y$ : un espace de variables auxiliaires.

---

## S1. Dissipation égale au carré du défaut de modèle (I.2, I.3, I.7)

**Hypothèses.**
- (H1) Une évolution canonique $\Phi_t$, définie au moins en temps court à partir de n'importe quelle configuration.
- (H2) Une fonctionnelle $E : \mathcal X \times \mathcal Y \to \mathbb R$, $G$-invariante, et une évolution couplée
  $y(t)$ des variables auxiliaires, telles que
  $$\frac d{dt}E(x(t),y(t)) = \|D(x(t),y(t))\|^2 \geq 0,$$
  où $D = 0$ caractérise exactement les orbites **auto-similaires** (contenues dans une $G$-orbite).
- (H3) $\mu(x) := \inf_y E(x,y)$ est atteint et minoré sur les configurations de départ.

**Conclusions.**
- (C1) Toute orbite périodique de $\Phi$ dans $\mathcal X/G$ est un point fixe : pas de respirateur.
- (C2) Toute limite (rééchelonnée) le long de laquelle $\mu$ se stabilise est auto-similaire.

**Instance.** $D = \mathrm{Ric} + \nabla^2 f - g/2\tau$, avec $\mathcal Y = \{(f,\tau)\}$ et $G$ = difféomorphismes et
homothéties.

**Ce qu'il faut construire pour tester.** Une évolution canonique, sa jauge, et une fonctionnelle dont la dérivée est
**exactement** un carré. C'est la partie la plus rare : en général on obtient seulement une inégalité, et le cas
d'égalité n'est pas rigide.

**Propre au flot.** L'existence de $\Phi$ (EDP parabolique), le fait que le flot de Ricci soit un gradient modulo
difféomorphismes, et l'échelle parabolique.

**Déjà transféré.** Formule de monotonie de Huisken (flot de courbure moyenne, antérieure) ; entropie de
Colding–Minicozzi pour le flot de courbure moyenne (2012) ; flot de Kähler–Ricci (estimées de Perelman, publiées par
Sesum–Tian).

## S2. Une quantité globale sondée localement contrôle une non-dégénérescence (I.4.1)

**Hypothèses.**
- S1 ;
- (H4) une mesure locale de dégénérescence $\varepsilon(x,B)$ pour des « boules » $B$ d'échelle $s$ ;
- (H5) pour toute boule à courbure contrôlée, une variable test $y_B$ (concentrée sur $B$) avec
  $E(x, y_B) \leq \log\varepsilon(x,B) + C$ ;
- (H6) une minoration initiale de $\mu$ aux petites échelles, qui vient d'une **inégalité fonctionnelle rigide** (ici
  Sobolev logarithmique).

**Conclusion.** $\varepsilon(x(t),B) \geq \kappa := e^{\mu_0 - C}$ pour tout $t$ et toute boule : non-dégénérescence
uniforme, d'où la compacité des limites.

**Lecture.** Le point remarquable est (H5) : la quantité globale est un **inf sur des sondes**, et une sonde bien
placée lit la géométrie locale. La monotonie fait le reste.

**Déjà transféré.** Le non-effondrement d'Andrews (2012) pour le flot de courbure moyenne à courbure moyenne positive,
puis Haslhofer–Kleiner (2017) : même rôle (compacité des limites), mécanisme différent (principe du maximum sur un
rayon de boules tangentes).

## S3. Monotonie bornée et rigidité de l'égalité : structure asymptotique (I.11.2)

**Hypothèses.** Une classe $\mathcal K$ d'objets « extrêmes » (solutions anciennes) fermée par limites, une quantité
$\tilde V$ monotone et bornée sur chaque objet, et une **rigidité** : $\tilde V$ constant implique un modèle
auto-similaire.

**Conclusion.** Le comportement asymptotique (écrasement) de tout objet de $\mathcal K$ est un modèle rigide. C'est un
**double éclatement** : singularité → objet extrême → modèle auto-similaire.

**Test.** Une version discrète doit remplacer « asymptotique » par une notion de limite. Dans un problème **fini**, le
schéma se dégrade en : *une quantité entière monotone de variation totale bornée, sur une chaîne longue, a beaucoup de
pas d'égalité*, et un pas d'égalité est rigide. L'intégralité joue le rôle de la limite : un défaut entier petit est nul.

## S4. Voisinages canoniques par contradiction, choix extrémal et induction sur les échelles (I.12.1, II.5.4)

**Hypothèses.**
- (a) Une notion d'échelle locale $Q(x)$.
- (b) Un théorème de compacité sous non-dégénérescence (S2) et bornes locales.
- (c) Une classe de modèles compacte, avec des estimées de dérivées universelles ($|\nabla R| \leq \eta R^{3/2}$).
- (d) Un **théorème de rigidité qui interdit les singularités ponctuelles à distance finie** (cônes exclus par le
  principe du maximum fort).

**Schéma de preuve.**
1. Par l'absurde, on choisit un contre-exemple d'échelle presque minimale ; la conclusion vaut alors à toutes les échelles
   plus fines (hypothèse de récurrence).
2. On en tire des bornes locales.
3. Par (d), on a des bornes « à distance bornée ».
4. On extrait une limite, qui est un modèle : contradiction.

**Lecture.** Ce n'est pas un simple éclatement : **l'ordre des quantificateurs est inversé par le choix extrémal**, ce
qui transforme une conclusion en hypothèse aux échelles plus fines.

**Déjà transféré.** Chirurgie du flot de courbure moyenne (Huisken–Sinestrari 2009 ; Brendle–Huisken ;
Haslhofer–Kleiner) ; c'est devenu la méthode standard pour les flots géométriques en dimension basse.

## S5. Classification grossière suffisante (II.1.5, I.11.9)

**Principe.** Classer les modèles seulement à la résolution que consomme la suite : un type topologique et des
constantes universelles, pas l'unicité. Perelman laisse l'unicité de Bryant comme croyance (I.11.9).

**Test.** Énumérer ce que l'argument aval utilise réellement des modèles, et classer seulement l'image des modèles par
cette fonction. Dans un problème fini, cela revient à **quotienter l'énumération par l'invariant que le test aval lit**.

## S6. Opération contrôlée par une ressource, à une échelle séparée (II.4)

**Hypothèses.** Une opération locale qui :
- (i) remplace une région par un **modèle standard universel**, dont l'évolution est connue ;
- (ii) consomme au moins une quantité fixe $h^3$ d'une ressource bornée (le volume) ;
- (iii) se fait à une échelle $h$ choisie **après** l'échelle de contrôle $r$, et très petite devant elle.

**Conclusion.** Nombre fini d'opérations sur tout intervalle borné ; les estimées a priori, démontrées par récurrence
dyadique, survivent.

**Déjà transféré.** Chirurgie du flot de courbure moyenne (mêmes références qu'en S4).

## S7. Min-max topologique à dérive négative (III)

**Hypothèses.**
- (a) Un invariant topologique non trivial (classe $\alpha$) qui rend une quantité min-max $W(t)$ positive tant que
  l'objet existe.
- (b) Une identité locale (Gauss–Bonnet) donnant $\frac{d}{dt}W \leq -c + a(t)W$ avec
  $\int c\,e^{-\int a} = \infty$.

**Conclusion.** Le processus s'arrête en temps fini.

**Déjà transféré.** Colding–Minicozzi (largeur des balayages par 2-sphères, 2005 et 2008) ; méthode d'Almgren–Pitts
pour les surfaces minimales, plus ancienne et dans l'autre sens (existence).

## S8. Espace formel plat comme générateur de monotonies (I.6)

**Principe heuristique.** Plonger l'objet en évolution dans un espace formel plus grand, de dimension $N \to \infty$, où
l'évolution devient un équilibre (Ricci-plat). Les théorèmes de comparaison classiques (Bishop–Gromov) y suggèrent des
quantités monotones, qu'on démontre ensuite directement.

**Statut.** Heuristique. [KL] note que I.6 n'est pas nécessaire à la preuve. Utile pour *trouver*, pas pour *prouver*.

## S9. Dualité direct–adjoint (I.9)

**Principe.** Pour une évolution linéaire $L$ et son adjoint $L^*$ : $\int hu$ est conservé si $Lh = 0$ et $L^*u = 0$ ;
une sous-solution adjointe $v$ ($L^*v \leq 0$) donne une quantité $\int hv$ monotone. En centrant $u$ en un point
(solution fondamentale), on **localise** une monotonie globale.

**Déjà transféré.** C'est un outil standard (Li–Yau, Hamilton, Ecker) ; Perelman l'applique à la densité de
$\mathcal W$.

## S10. L'énoncé intermédiaire unique (méta-principe ; I.0, I.4, II.5)

**Principe.** Identifier **une** estimée a priori dont la vérité fait fonctionner la machinerie existante (compacité,
classification, chirurgie), et organiser l'attaque autour de cette estimée, dans sa forme la plus robuste : toutes
dimensions, localisée, survivant aux opérations.

Chez Perelman, cette estimée était le non-effondrement : conjecturé par Hamilton, démontré deux fois en [I] ($\mathcal
W$, puis $\tilde V$), puis rendu local (I.8), puis robuste à la chirurgie (II.5).

**Test.** Sur un problème bloqué, écrire la liste des estimées manquantes, et vérifier s'il en existe une **dont toutes
les autres découlent** par les outils disponibles. S'il n'en existe pas, le problème n'a pas la structure qui a permis la
percée.

---

## Partie V — Ce qui est propre au flot de Ricci, et ce qui pourrait être transférable

**Ingrédients propres au flot de Ricci, ou à la géométrie riemannienne de dimension 3.**
1. **Une déformation canonique** existe à partir de n'importe quelle donnée : le problème *produit* sa propre dynamique.
2. **Principes du maximum** (scalaire, tensoriel, fort) : ils donnent des inégalités ponctuelles qui se propagent.
3. **Symétries continues** : difféomorphismes (jauge) et homothéties paraboliques (échelle). L'éclatement n'a de sens
   que grâce à l'échelle.
4. **Compacité** à la Cheeger–Gromov–Hamilton : une limite existe sous des bornes uniformes.
5. **Dimension 3** : pincement de Hamilton–Ivey ; liste des solitons contractants ; topologie des cous (2-sphères, somme
   connexe) ; décomposition en premiers ; géométrisation.
6. **Géométrie d'Alexandrov et théorie de l'effondrement**, pour reconnaître les variétés graphées.

**Transférable au niveau de l'architecture logique** (avec les hypothèses de S1–S10) :
- (i) une fonctionnelle dont la dissipation est un carré de défaut, si l'on dispose d'une évolution canonique ;
- (ii) le passage « quantité globale + sonde locale ⇒ non-dégénérescence uniforme » ;
- (iii) « monotonie bornée + rigidité de l'égalité ⇒ modèle » ;
- (iv) l'induction sur les échelles par choix extrémal ;
- (v) la classification réduite à ce que consomme l'aval ;
- (vi) la séparation hiérarchique des paramètres ;
- (vii) le min-max topologique ;
- (viii) le méta-principe de l'énoncé intermédiaire unique.

**Conditions de transfert vers un problème fini** (déduites de I–IV, à tester dans le second travail) :
- **T1** : une évolution canonique non triviale sur un espace qui contient l'objet cherché. Sans elle, S1, S3, S6 et S7
  n'ont pas de support.
- **T2** : une notion d'échelle (S2, S4).
- **T3** : un substitut de la compacité. En fini, c'est la finitude elle-même, ou l'intégralité qui transforme un défaut
  petit en défaut nul (S3).
- **T4** : un théorème de rigidité pour les cas d'égalité (S1, S3, S4(d)).
- **T5** : un invariant topologique non trivial (S7).

Le second travail examine ces conditions une à une pour Conway-99.
