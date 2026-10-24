# Partie II — Les trois manuscrits : reconstruction des mécanismes décisifs

Conventions : $M$ close de dimension $n$ (sauf mention), $\partial_t g = -2\mathrm{Ric}$, $\tau = T - t$ temps
rétrograde, $\Box = \partial_t - \Delta$, $\Box^* = -\partial_t - \Delta + R$ (opérateur adjoint :
$\frac{d}{dt}\int uv = \int (\Box u)v - u(\Box^* v)$, I.9.6). Les numéros d'équations sont ceux de Perelman.

---

## 1. I.1–I.2 : le flot de Ricci est un flot de gradient (modulo une jauge)

**Définition.** $\mathcal F(g,f) = \int_M (R + |\nabla f|^2)\,e^{-f}dV$.

**Première variation (I.1.1).** Avec $\delta g_{ij} = v_{ij}$, $\delta f = h$, $v = g^{ij}v_{ij}$ :
$$\delta\mathcal F = \int_M e^{-f}\Big[-v_{ij}(R_{ij} + \nabla_i\nabla_j f) + \big(\tfrac v2 - h\big)(2\Delta f - |\nabla f|^2 + R)\Big].$$

**Lecture.** $\tfrac v2 - h = 0$ exactement quand la mesure $dm = e^{-f}dV$ est fixe. À mesure fixée, le gradient
$L^2(dm)$ de $\mathcal F^m$ est $-(R_{ij} + \nabla_i\nabla_j f)$, le *tenseur de Bakry–Émery*. Le flot de gradient
$\partial_t g = -2(\mathrm{Ric} + \nabla^2 f)$, $\partial_t f = -R - \Delta f$ (1.1) n'est autre que le flot de Ricci tiré
en arrière par les difféomorphismes engendrés par $\nabla f$. Après ce changement :
$$\partial_t g = -2\mathrm{Ric}, \qquad \partial_t f = -\Delta f + |\nabla f|^2 - R \quad (1.3), \qquad
\frac{d\mathcal F}{dt} = 2\int |R_{ij} + \nabla_i\nabla_j f|^2 e^{-f}dV \geq 0 \quad (1.4).$$
La seconde équation dit exactement $\Box^*(e^{-f}) = 0$ : **la fonction auxiliaire évolue par l'équation de la chaleur
adjointe**. Perelman : « le choix de $m$ est analogue à un choix de jauge » [D, I.1.1].

**Le premier invariant.** $\lambda(g) = \inf\{\mathcal F(g,f) : \int e^{-f}dV = 1\}$. Avec $e^{-f/2} = \varphi$,
$\mathcal F = \int (4|\nabla\varphi|^2 + R\varphi^2)$ : $\lambda$ est **la plus petite valeur propre de $-4\Delta + R$**
(I.2.2). Par (1.4), $\lambda(g(t))$ ne décroît pas ; il est constant seulement sur un soliton stationnaire de gradient.

**Conséquences démontrées.**
- Prop. I.1.2 : si le flot de gradient de $\mathcal F^m$ existe sur $[0,T]$, alors $\mathcal F^m \leq \frac{n}{2T}\int
  dm$ en $t = 0$. Preuve : $\mathcal F_t \geq \frac2n\int (R+\Delta f)^2 dm \geq \frac 2n\mathcal F^2$ (Cauchy–Schwarz).
- **Pas de « respirateur » stationnaire** (I.2.2) : un $g(t_2)$ difféomorphe à $g(t_1)$ force $\lambda(t_1) =
  \lambda(t_2)$, donc l'égalité dans (1.4) sur $[t_1,t_2]$ : soliton stationnaire.
- **Pas de respirateur dilatant** (I.2.3) : $\bar\lambda = \lambda V^{2/n}$ est croissant lorsqu'il est $\leq 0$.
  Perelman signale qu'une preuve plus simple résulte de [Hamilton 1999, §2] avec $\min R\,V^{2/n}$ (I.2.5*).

**Origine [D, I.1.4*].** $\mathcal F$ et sa variation figurent dans la littérature de théorie des cordes (action
effective de basse énergie, $f$ = dilaton) ; le tenseur $\mathrm{Ric} + \nabla^2 f$ est celui de Bakry–Émery ; DeTurck
avait déjà modifié le flot par des difféomorphismes, mais pour la parabolicité. **Ce qui est nouveau** : lire le flot
comme un flot de gradient dont la jauge est le choix d'une mesure, et coupler la fonction auxiliaire au flot par
l'équation adjointe. L'intuition annoncée est celle du groupe de renormalisation : « Ricci flow must be gradient-like »
[D, I.0.2].

---

## 2. I.3 : l'entropie $\mathcal W$ et l'insertion de l'échelle

Le cas contractant ($\lambda > 0$) résiste à $\mathcal F$, qui n'est pas invariant par changement d'échelle.

**Définition (3.1–3.2).** Pour $\tau > 0$ et $u = (4\pi\tau)^{-n/2}e^{-f}$ avec $\int u\,dV = 1$ :
$$\mathcal W(g,f,\tau) = \int_M \big[\tau(|\nabla f|^2 + R) + f - n\big]\,u\,dV .$$
$\mathcal W$ est invariant par $(g,\tau) \mapsto (c\,g, c\,\tau)$.

**Évolution couplée (3.3)** : $\partial_t g = -2\mathrm{Ric}$, $\tau_t = -1$, $\Box^* u = 0$. **Formule de monotonie
(3.4)** :
$$\frac{d\mathcal W}{dt} = 2\tau\int_M \Big|R_{ij} + \nabla_i\nabla_j f - \frac{1}{2\tau}g_{ij}\Big|^2 u\,dV \;\geq\; 0 .$$
Le défaut est **un seul tenseur**, dont l'annulation est l'équation des solitons contractants de gradient.

**Invariants.** $\mu(g,\tau) = \inf_f \mathcal W$ et $\nu(g) = \inf_{\tau > 0}\mu(g,\tau)$. Pour $T$ fixé,
$t \mapsto \mu(g(t), T - t)$ ne décroît pas (il suffit de résoudre l'équation adjointe en arrière depuis le minimiseur).

**Le rôle de l'inégalité de Sobolev logarithmique.** Sur $\mathbb R^n$ euclidien, $\mathcal W(g_{eucl}, f, \tau) \geq 0$
avec égalité pour $f = |x|^2/4\tau$ (soliton gaussien) : c'est l'inégalité de Gross, après le changement
$f = |x|^2/2 - 2\log\varphi$ (I.3.1). Perelman en tire :
- **Affirmation (I.3.1)** : $\mu(g,\tau) < 0$ pour $\tau$ petit et $\mu(g,\tau) \to 0$ quand $\tau \to 0$ (preuve
  esquissée : les métriques $\frac12\tau^{-1}g$ « tendent » vers l'euclidienne, et un minimiseur limite violerait Gross).
- **Pas de respirateur contractant non trivial** : sur un respirateur, $\nu$ est atteint et constant, donc égalité
  dans (3.4), donc soliton.
- Remarque I.3.2 : (3.4) redonne une inégalité de Sobolev logarithmique avec cas d'égalité sur les solitons.

**Origine [D, I.3.3*].** Le théorème « pas de respirateurs » en dimension 3 était dû à Ivey (par le pincement) ; les
inégalités de Sobolev logarithmiques apparaissent dans les flots géométriques chez Ecker (2000) pour le flot de
courbure moyenne. **Nouveau** : la fonctionnelle elle-même, l'insertion explicite de l'échelle $\tau$ qui évolue avec le
temps, la monotonie (3.4) en dimension quelconque.

---

## 3. I.4 : premier théorème de non-effondrement

**Définition (I.4.2).** $g$ est **$\kappa$-non effondrée à l'échelle $\rho$** si toute boule $B$ de rayon $r < \rho$
avec $|\mathrm{Rm}| \leq r^{-2}$ sur $B$ vérifie $\mathrm{Vol}(B) \geq \kappa r^n$. Cette propriété passe aux limites et
se comporte bien par changement d'échelle.

**Théorème (I.4.1).** Sur $M$ close et $T < \infty$, la solution n'est pas localement effondrée en $T$.

**Preuve complète (R, d'après I.4.1).**
1. Supposons des boules $B_k = B(p_k, r_k)$ aux temps $t_k \to T$, $r_k^2/t_k$ bornés, $|\mathrm{Rm}| \leq r_k^{-2}$ sur
   $B_k$ et $\varepsilon_k := r_k^{-n}\mathrm{Vol}(B_k) \to 0$.
2. *Fonction test.* $f_k = -\log\phi(d_{t_k}(x,p_k)/r_k) + c_k$, avec $\phi = 1$ sur $[0,\frac12]$, décroissante, presque
   nulle sur $[1,\infty)$ ; $c_k$ normalise $\int u = 1$, d'où $c_k \approx \log\varepsilon_k - \frac n2\log 4\pi \to
   -\infty$.
3. *Estimation.* Le terme $\tau|\nabla f|^2$ est $O(1)$ (car $|\nabla\phi| \lesssim r_k^{-1}$ et la masse de $u$ est
   portée par $B_k$), le terme $\tau R$ est $O(1)$ (borne de courbure), le terme $\int fu$ vaut $c_k + O(1)$. Donc
   $\mu(g(t_k), r_k^2) \leq \log\varepsilon_k + C(n) \to -\infty$.
4. *Monotonie.* $\mu(g(0), t_k + r_k^2) \leq \mu(g(t_k), r_k^2) \to -\infty$.
5. *Contradiction.* $t_k + r_k^2$ reste borné, et $\mu(g(0),\cdot)$ est minoré sur tout intervalle borné (par I.3.1 et
   la compacité de $M$). ∎

**Corollaire (I.4.2).** Si $Q_k = |\mathrm{Rm}|(p_k,t_k) \to \infty$ et $|\mathrm{Rm}| \leq CQ_k$ pour $t < t_k$, les
rééchelonnements par $Q_k$ convergent (sous-suite) vers une **solution ancienne complète, $\kappa$-non effondrée à toutes
les échelles**. *C'est la solution de (M1).*

**Structure logique [Int].** L'entropie est une quantité **globale**, **monotone**, et **minorée initialement** (par
une inégalité fonctionnelle, Gross). Évaluée sur une fonction test concentrée dans une boule de rayon $\sqrt\tau$, elle
**majore** $\log$ du rapport de volume de cette boule. La monotonie transporte la minoration initiale vers tous les
temps et toutes les échelles. Une quantité globale contrôle ainsi une non-dégénérescence locale uniforme.

---

## 4. I.5–I.6 : deux heuristiques (non nécessaires à la preuve)

**I.5, analogie statistique.** Avec $\log Z = \int(-f + \frac n2)dm$ :
- $\langle E\rangle = -\tau^2\int(R + |\nabla f|^2 - \frac{n}{2\tau})dm$ ;
- $S = -\int(\tau(R + |\nabla f|^2) + f - n)dm = -\mathcal W$ ;
- $\sigma = 2\tau^4\int|R_{ij} + \nabla_i\nabla_j f - \frac{1}{2\tau}g_{ij}|^2 dm \geq 0$, nulle seulement sur les
  solitons contractants.

$\mathcal W$ est donc *moins une entropie*, et la monotonie (3.4) se lit comme la positivité d'une fluctuation (somme de
carrés). La question finale de I.5.1 (une entropie bornée force-t-elle un soliton ?) reçoit une réponse négative en
II.1.4.

**I.6, espace formel « Ricci-plat ».** $\tilde M = M \times S^N \times \mathbb R^+$, avec $\tilde g_{ij} = g_{ij}(\tau)$,
$\tilde g_{\alpha\beta} = \tau g_{\alpha\beta}$ ($S^N$ de courbure $\frac1{2N}$), $\tilde g_{00} = \frac N{2\tau} + R$, le
flot étant rétrograde.
- Les composantes de la courbure de $\tilde g$ coïncident (mod $N^{-1}$) avec l'expression de Harnack matricielle de
  Hamilton, et sa courbure de Ricci est nulle (mod $N^{-1}$).
- La longueur d'une géodésique issue de $\tau = 0$ vaut
  $\sqrt{2N\tau} + \frac{1}{\sqrt{2N}}\int_0^\tau\sqrt\tau(R + |\dot\gamma|^2)d\tau + O(N^{-3/2})$.
- Bishop–Gromov dans cet espace suggère la monotonie de
  $\tilde V(\tau) = \int_M \tau^{-n/2}\exp(-\frac1{\sqrt{2\tau}}L)\,dx$.

[KL §4] : « Section I.5 and I.6 are not needed in the sequel. » **L'heuristique a produit l'objet ; la preuve (I.7) ne
passe pas par elle** [D].

---

## 5. I.7 : la géométrie $\mathcal L$ et le volume réduit

**Longueur $\mathcal L$.** Pour un chemin $\gamma(\tau)$, $\tau \in [\tau_1, \tau_2]$, dans le flot rétrograde
$\partial_\tau g = 2\mathrm{Ric}$ :
$$\mathcal L(\gamma) = \int_{\tau_1}^{\tau_2}\sqrt\tau\,\big(R(\gamma(\tau),\tau) + |\dot\gamma(\tau)|^2\big)\,d\tau .$$
Avec $s = \sqrt\tau$, $\mathcal L = \int(2s^2R + \frac12|d\gamma/ds|^2)ds$, régulier en $\tau = 0$ [R].

**Géodésiques (7.2).** $\nabla_X X - \frac12\nabla R + \frac1{2\tau}X + 2\mathrm{Ric}(X,\cdot) = 0$, $X = \dot\gamma$.

**Distance réduite.** $p$ fixé, $\tau_1 = 0$ : $L(q,\bar\tau) = \inf\mathcal L$ et $l(q,\bar\tau) =
L/(2\sqrt{\bar\tau})$. Dans $\mathbb R^n$ plat, $l = |q-p|^2/4\bar\tau$.

**Les identités clés.** On note $K = \int_0^{\bar\tau}\tau^{3/2}H(X)\,d\tau$, où $H(X)$ est l'expression de Harnack
tracée de Hamilton (avec $t = -\tau$). Alors :
- (7.5) $L_{\bar\tau} = 2\sqrt{\bar\tau}R - \frac1{2\bar\tau}L + \frac1{\bar\tau}K$ ;
- (7.6) $|\nabla L|^2 = -4\bar\tau R + \frac2{\sqrt{\bar\tau}}L - \frac4{\sqrt{\bar\tau}}K$ ;
- (7.10) $\Delta L \leq -2\sqrt{\bar\tau}R + \frac n{\sqrt{\bar\tau}} - \frac1{\bar\tau}K$.

(7.10) vient de la seconde variation, avec le champ $Y$ solution de $\nabla_X Y = -\mathrm{Ric}(Y,\cdot) + \frac1{2\tau}Y$,
pour lequel $|Y(\tau)|^2 = \tau/\bar\tau$. **L'expression de Harnack matricielle de Hamilton apparaît exactement comme
terme de seconde variation** [D, I.7.1].

**Jacobien.** Pour l'application $\mathcal L\exp$ :
$\frac d{d\tau}\log J \leq \frac{n}{2\bar\tau} - \frac12\bar\tau^{-3/2}K$ (7.12), avec égalité seulement si
$2\mathrm{Ric} + \frac1{\sqrt{\bar\tau}}\mathrm{Hess}_L = \frac1{\bar\tau}g$. Le long d'une $\mathcal L$-géodésique,
$\frac d{d\tau}l = -\frac12\bar\tau^{-3/2}K$. **Les deux termes en $K$ se compensent** :
$\tau^{-n/2}e^{-l}J$ est non croissant.

**Théorème (volume réduit).** $\tilde V(\tau) = \int_M \tau^{-n/2}e^{-l(q,\tau)}dq$ est non croissant en $\tau$, donc
non décroissant en temps réel. Il est **constant seulement sur un soliton contractant de gradient**. Dans $\mathbb R^n$,
$\tilde V \equiv (4\pi)^{n/2}$, et $\tilde V(\tau) \to (4\pi)^{n/2}$ quand $\tau \to 0$.

**Inégalités différentielles utiles.**
- (7.13) $l_{\bar\tau} - \Delta l + |\nabla l|^2 - R + \frac{n}{2\bar\tau} \geq 0$, autrement dit
  $\Box^*(\tau^{-n/2}e^{-l}) \leq 0$ ;
- (7.14) $2\Delta l - |\nabla l|^2 + R + \frac{l-n}{\bar\tau} \leq 0$ ;
- (7.15) $\bar L_{\bar\tau} + \Delta\bar L \leq 2n$ pour $\bar L = 2\sqrt\tau L$. Donc **$\min_q l(q,\bar\tau) \leq
  \frac n2$ pour tout $\bar\tau$** (principe du maximum).
- (7.16) sous un opérateur de courbure $\geq 0$, et pour $\tau$ loin de $\tau_0$ : $|\nabla l|^2 + R \leq Cl/\tau$.

**Non-effondrement par le volume réduit (I.7.3).** Hypothèse plus forte que I.4.1 : borne de courbure sur le *cylindre
parabolique* $B_k \times [t_k - r_k^2, t_k]$.
1. Effondrement à l'échelle $r_k$ : les $\mathcal L$-géodésiques courtes restent dans $B_k$, les longues sont pénalisées
   par la comparaison de jacobien. Donc $\tilde V_k(\varepsilon_k r_k^2) < 3\varepsilon_k^{n/2}$.
2. Au temps 0 ($\tau = t_k$), $\tilde V_k$ reste minoré : $\min l(\cdot, t_k - \frac T2) \leq \frac n2$ fournit un point
   $q_k$ par lequel on borne $l$ au temps 0, la géométrie de $[0, T/2]$ étant bornée.
3. La monotonie impose $\tilde V_k(t_k) \leq \tilde V_k(\varepsilon_k r_k^2)$. Contradiction. ∎

**Origine [D, I.7.4*].** Ce sont « des modifications naturelles » de la théorie classique de la variation des
géodésiques ; la référence la plus proche est **Li–Yau (1986)**, qui emploient une « longueur » associée à une équation
parabolique linéaire. Le volume réduit ressemble à la formule de monotonie de Huisken pour le flot de courbure moyenne,
mais **avec la monotonie dans le sens opposé** (I.6.4*). La première interprétation géométrique de la Harnack de Hamilton
est due à Chow–Chu (1995–96), dont la construction est « en un sens duale » de celle de I.6 (I.6.4*).

**Pourquoi c'est la pièce maîtresse [D, KL §4 ; MT intro].** Le volume réduit est **localisable en espace-temps** : il
n'utilise que la géométrie le long des $\mathcal L$-géodésiques issues du point. Il survit donc à la chirurgie, si l'on
contrôle les courbes qui passent près des régions opérées (II.5). C'est l'outil employé dans toute la suite ; MT y voit
l'une des deux avancées essentielles de Perelman. Selon KL, un lecteur qui ne vise que Poincaré ou la géométrisation
« pourrait en principe commencer en I.7 ».

---

## 6. I.8 : non-effondrement localisé (Théorème I.8.2)

**Énoncé.** Pour tout $A$ il existe $\kappa(A)$ tel que : si $|\mathrm{Rm}| \leq r_0^{-2}$ sur $B_0(x_0,r_0) \times
[0,r_0^2]$ et $\mathrm{Vol}\,B_0(x_0,r_0) \geq A^{-1}r_0^n$, alors la solution n'est pas $\kappa$-effondrée aux échelles
$< r_0$ en tout point $(x, r_0^2)$ avec $d_{r_0^2}(x,x_0) \leq Ar_0$.

**Mécanisme.**
- Le volume réduit issu de $(x, r_0^2)$ doit être grand au temps $\frac12$ si $l$ est borné sur une petite boule autour
  de $x_0$.
- On borne $\bar L$ par un principe du maximum appliqué à $h = \phi(d - A(2t-1))(\bar L + 2n + 1)$. On utilise (7.15)
  et le lemme I.8.3 : $d_t - \Delta d \geq -(n-1)(\frac23Kr_0 + r_0^{-1})$ hors de $B(x_0,r_0)$ si
  $\mathrm{Ric} \leq (n-1)K$ sur cette boule. Ce lemme sert ensuite partout (vitesse de variation des distances).

**Rôle.** Le non-effondrement n'a plus besoin d'une borne globale : il se propage d'une boule « de taille définie » vers
toute région à distance bornée.

---

## 7. I.9 : inégalité de Harnack pour l'équation adjointe

**Proposition (I.9.1).** Si $u = (4\pi(T-t))^{-n/2}e^{-f}$ vérifie $\Box^* u = 0$, alors
$v = [(T-t)(2\Delta f - |\nabla f|^2 + R) + f - n]u$ vérifie
$$\Box^* v = -2(T-t)\Big|R_{ij} + \nabla_i\nabla_j f - \frac{1}{2(T-t)}g_{ij}\Big|^2 u .$$

**Corollaires.**
- C'est la version *ponctuelle* de (3.4).
- Si $u$ tend vers une masse de Dirac quand $t \to T$, alors $v \leq 0$ (I.9.3). Preuve par dualité :
  $\frac d{dt}\int hu = 0$ et $\frac d{dt}\int hv \geq 0$ pour toute solution $h > 0$ de l'équation de la chaleur.
- $f \leq l$ (I.9.5).

**Remarque I.9.6.** Le flot de Ricci est *caractérisé* parmi les évolutions $\partial_t g = A_{ij}$ par le comportement
infinitésimal des solutions fondamentales de l'équation adjointe :
$(\Box\bar f + \bar f/t) = o(1)$, et même $O(|pq|^2 + |t|)$.

**Origine [D, I.9.7*].** Li–Yau, Hamilton (Harnack pour l'équation de la chaleur rétrograde et formules de monotonie),
Ecker (formule de monotonie locale pour le flot de courbure moyenne, 2001).

---

## 8. I.10 : pseudolocalité

**Théorème (I.10.1).** Pour tout $\alpha > 0$, il existe $\delta, \varepsilon > 0$ tels que : si à $t = 0$ on a
$R \geq -r_0^{-2}$ et une isopérimétrie presque euclidienne,
$\mathrm{Vol}(\partial\Omega)^n \geq (1-\delta)c_n\mathrm{Vol}(\Omega)^{n-1}$ pour $\Omega \subset B(x_0,r_0)$, alors
$|\mathrm{Rm}|(x,t) \leq \alpha t^{-1} + (\varepsilon r_0)^{-2}$ pour $0 < t \leq (\varepsilon r_0)^2$ et
$d_t(x,x_0) < \varepsilon r_0$.

« Les régions presque singulières ne peuvent pas influencer instantanément les régions presque euclidiennes » [D].

**Architecture de la preuve.**
1. Par l'absurde, avec des suites $\varepsilon, \delta \to 0$.
2. *Choix du point (Affirmations 1–2)* : on construit $(\bar x, \bar t)$ par une suite finie de points où $|\mathrm{Rm}|$
   au moins quadruple. Le point final a une courbure **contrôlée par 4 fois la sienne dans tout un voisinage
   parabolique**. C'est un lemme de choix du point (*point-picking*).
3. On centre en $(\bar x, \bar t)$ une solution fondamentale de l'équation adjointe ; le $v \leq 0$ associé a une
   intégrale $\int_B v$ minorée en valeur absolue près de $\bar t$ (Affirmation 3). Preuve par éclatement : sinon la
   limite serait un soliton contractant, incompatible avec $|\mathrm{Rm}|(\bar x,\bar t) = 1$.
4. On propage cette minoration jusqu'à $t = 0$ par la monotonie localisée (9.1) et une fonction de coupure.
5. À $t = 0$, sur la région presque euclidienne, on contredit l'inégalité de Sobolev logarithmique gaussienne
   (symétrisation sphérique).

**Corollaires.** Minoration de volume (10.2) ; version pour courbure bornée et volume presque euclidien (10.3) ;
non-effondrement à partir d'une région presque euclidienne (10.4).

**Origine [D, I.10.6*].** Analogue des estimées intérieures d'Ecker–Huisken pour le flot de courbure moyenne.

---

## 9. I.11 et II.1 : les $\kappa$-solutions

**Définition (I.11.1, II.1.1).** Une **$\kappa$-solution** est une solution ancienne ($t \in (-\infty, 0]$), complète,
non plate, à courbure bornée et opérateur de courbure $\geq 0$ (sectionnelle $\geq 0$ en dimension 3), et
$\kappa$-non effondrée à toutes les échelles. Ce sont exactement les limites d'éclatement possibles en dimension 3
(Hamilton–Ivey et I.4.2).

**I.11.2, soliton asymptotique.** Pour $(p,t_0)$, choisissons $q(\tau)$ avec $l(q(\tau),\tau) \leq \frac n2$ (7.15). Les
rééchelonnements de $g(t_0 - \tau)$ en $q(\tau)$ par $\tau^{-1}$ convergent, pour une sous-suite $\tau \to \infty$, vers
un **soliton contractant de gradient non plat**.
- *Compacité* : (7.16) et le non-effondrement.
- *Constance* : $\tilde V$ est monotone et minoré (non-effondrement), donc constant à la limite.
- *Rigidité* : le cas d'égalité de (7.12)–(7.14) donne l'équation du soliton
  $\bar R_{ij} + \bar\nabla_i\bar\nabla_j\bar l - \frac{1}{2\tau}\bar g_{ij} = 0$.
- *Non platitude* : $\bar V < (4\pi)^{n/2}$ parce que $g$ n'est pas plate, alors qu'un soliton plat donnerait exactement
  $(4\pi)^{n/2}$.

**Mécanisme [Int].** C'est un double éclatement [Tao §6] : la limite d'éclatement d'une singularité (une
$\kappa$-solution) a elle-même une limite d'« écrasement » (*blow-down*) qui est un objet rigide, un soliton. **La
monotonie bornée force l'égalité asymptotique, et l'égalité est rigide.**

**I.11.3 (dimension 2).** La seule $\kappa$-solution orientée est la sphère ronde. On combine le soliton asymptotique
(sphère, Hamilton 1988) et le fait que la presque-rondeur s'améliore sous le flot.

**I.11.4.** Le rapport de volume asymptotique $\mathcal V = \lim r^{-n}\mathrm{Vol}\,B(p,r)$ est nul. La preuve est
une induction sur la dimension. Si $\mathcal V > 0$ :
- ou bien le rapport de courbure asymptotique $\mathcal R = \limsup R\,d^2$ est infini : un éclatement scinde une droite
  (concavité d'Alexandrov–Toponogov) et on réduit la dimension ;
- ou bien il est fini et non nul : on obtient un cône non plat, exclu par le principe du maximum fort de Hamilton ;
- ou bien il est nul : la métrique est plate.

**I.11.5–11.6.** Deux énoncés complémentaires, en courbure $\geq 0$ :
- (11.5) une courbure très grande en un point force un rapport de volume **petit** à l'échelle $A$ fois l'échelle de
  courbure (conséquence de $\mathcal V = 0$) ;
- (11.6) par contraposée, un rapport de volume $\geq w$ sur une boule $B(x_0,r_0)$ force la borne
  $R \leq Cr_0^{-2} + B(t - t_0)^{-1}$ sur $B(x_0, r_0/4)$.

« Volume minoré ⇒ courbure majorée » : c'est le schéma qui sert ensuite en I.12.3 et II.6.

**I.11.7, compacité modulo l'échelle** de l'ensemble des $\kappa$-solutions, en dimension 3. L'hypothèse de
non-compacité de l'énoncé initial est superflue (II.1.1).
- Ingrédients : 11.5, comparaison de volume en courbure $\geq 0$, estimées de Shi, Harnack intégrée.
- Un point de courbure infinie à distance finie est impossible : il y aurait des cous de rayon $\to 0$ dans une variété
  ouverte à courbure $\geq 0$.

**I.11.8.** Les points qui ne sont pas des centres de $\varepsilon$-cous forment un compact de diamètre
$\leq CQ^{-1/2}$, sur lequel la courbure est comparable à $Q$.

**II.1.2 (pas de soliton contractant non compact à courbure $> 0$ bornée, en dimension 3).**
1. Le long des géodésiques longues, $f$ croît linéairement et $\nabla f$ est presque radial.
2. Par $\nabla_i R = 2R_{ij}\nabla_j f$, $R$ croît le long des lignes de gradient. Un éclatement à l'infini scinde une
   droite : c'est un cylindre rond, et $R \to 1$.
3. Les surfaces de niveau de $f$ sont convexes, d'aire croissante vers $4\pi\cdot 2$, et pourtant de courbure
   intrinsèque $< 1$.
4. Cela contredit Gauss–Bonnet. ∎

**II.1.3–1.5, classification.**
- Les solitons asymptotiques possibles sont : quotients sphériques ronds, cylindre rond, quotient $\mathbb Z_2$ du
  cylindre.
- Les $\kappa$-solutions sont : sphériques rondes, de soliton asymptotique cylindrique (non compactes, comme le cylindre
  ou le soliton de Bryant, ou **compactes** — cas que I.11.7 avait omis), ou leurs quotients.
- **Exemple II.1.4** : un long cylindre coiffé sur $S^3$ fournit des $\kappa$-solutions compactes de soliton
  asymptotique cylindrique. Il donne aussi une réponse négative à la question de I.5.1.
- **II.1.5** : il existe un $\kappa_0$ universel. Il existe des constantes universelles $\eta, C_1(\varepsilon),
  C_2(\varepsilon)$ : $|\nabla R| < \eta R^{3/2}$ et $|R_t| < \eta R^2$, et tout point a un voisinage de l'un des quatre
  types (a) $\varepsilon$-cou fort, (b) $\varepsilon$-calotte, (c) variété close difféomorphe à $S^3$ ou
  $\mathbb{RP}^3$, (d) variété close à courbure constante.

**Remarque I.11.9.** Perelman *croit* que la seule $\kappa$-solution non compacte à courbure $> 0$ est le soliton de
Bryant. Il le dit plausible mais non rigoureux, et prouve l'unicité parmi les solitons stationnaires de gradient
(résultat établi plus tard par Brendle). **La preuve n'en a pas besoin** : la classification grossière (cous et
calottes) suffit [D, II.1.5 ; Int].

---

## 10. I.12 : le théorème des voisinages canoniques

**Théorème (I.12.1).** Soient $\varepsilon, \kappa > 0$ et $\phi$ (pincement). Il existe $r_0$ tel que, pour une
solution sur une 3-variété close, $\kappa$-non effondrée aux échelles $< r_0$ et $\phi$-presque à courbure $\geq 0$, tout
$(x_0,t_0)$ avec $t_0 \geq 1$ et $Q = R(x_0,t_0) \geq r_0^{-2}$ a un voisinage parabolique
$\{d^2 < (\varepsilon Q)^{-1}, t \in [t_0 - (\varepsilon Q)^{-1}, t_0]\}$ qui est, après rééchelonnement par $Q$,
$\varepsilon$-proche d'un morceau de $\kappa$-solution.

**Preuve, dans son ossature.**
1. **Par l'absurde, avec un choix extrémal** : on prend $r_0 \to 0$ et, parmi les points qui violent la conclusion,
   **un point de courbure presque minimale**. La conclusion est alors vraie en tout point de courbure $> 2Q$ dans une
   fenêtre temporelle $HQ^{-1}$, $H \to \infty$. **L'hypothèse aux échelles plus fines fournit les estimées
   nécessaires à l'échelle courante** : c'est une induction sur les échelles.
2. **Affirmation 1** (bornes de courbure locales) : grâce aux estimées $|R_t| \leq CR^2$ et
   $|\nabla R| \leq CR^{3/2}$, valables aux points déjà « canoniques ».
3. **Affirmation 2 (courbure bornée à distance bornée)** : le long d'une géodésique où la courbure est grande, un point
   de courbure beaucoup plus grande ne peut pas être à distance bornée. Sinon, à la limite :
   - on obtient une métrique à courbure $\geq 0$, lisse sauf en un point singulier $o$ ;
   - près de $o$, elle est cylindrique et de rayon $\leq \varepsilon\,d(\cdot,o)$, donc de courbure $\geq 0$ au sens
     d'Alexandrov en $o$, donc conique ;
   - les rééchelonnements en $x_i \to o$ convergent vers un **cône non plat à courbure $\geq 0$**, qui de plus évolue
     par le flot (Affirmation 1) ;
   - c'est **exclu par le principe du maximum fort** de Hamilton.
4. **Extraction de la limite au temps $t_0$** (non-effondrement), à courbure bornée (sinon il y aurait des cous de
   rayon $\to 0$ dans une variété complète à courbure $\geq 0$), puis sur un intervalle de temps.
5. **Extension à tout le passé**, par la Harnack ($R_t \geq -R/(t - t')$) et par le contrôle de la croissance des
   distances (I.8.3(b)). La limite est une $\kappa$-solution : contradiction.

**Ce qui est nouveau, selon les reconstructions [D, MT intro].** Le point 3 est « l'autre avancée majeure » de
Perelman, à côté du non-effondrement : Hamilton se plaçait aux points de courbure maximale, ce qui ne marche pas ici.
L'argument emploie la géométrie d'Alexandrov (le domaine de Perelman dans les années 1990 : Burago–Gromov–Perelman
1992, théorème de stabilité). *C'est le transfert de compétence le mieux documenté de toute la preuve* [D pour l'usage ;
Int pour l'interprétation biographique].

**I.12.2–12.4 et correction II.6.2.** Ce sont des contrôles de courbure vers l'avant et vers l'arrière à partir du
volume et d'une minoration de courbure dans une boule, en courbure presque positive. L'énoncé I.12.2 était incorrect et
est corrigé en II.6.2 [D].

---

## 11. II.2–II.4 : la solution standard et la chirurgie à deux échelles

**II.2, solution standard.**
- *Donnée initiale* : une métrique de révolution sur $\mathbb R^3$, à courbure $\geq 0$, égale à
  $[0,\infty) \times S^2$ (courbure scalaire 1) hors d'un compact (« calotte standard »).
- *Propriétés* : le flot reste de révolution (Affirmation 1, les champs de Killing sont préservés) ; il converge à
  l'infini vers le cylindre, donc $T \leq 1$ (Affirmation 2) ; il est unique (Affirmation 3, réduction à un système 1D) ;
  il existe sur $[0,1)$ (Affirmation 4, par pseudolocalité et exclusion d'un point conique).
- Il vérifie les conclusions de II.1.5, et $R_{\min}(t) \geq c(1-t)^{-1}$ (Affirmation 5).
- **C'est un modèle universel** : toute région fraîchement opérée ressemble, à l'échelle de chirurgie, à ce flot connu
  [Int].

**II.3, structure au premier temps singulier.**
- $\Omega$ est l'ensemble où la courbure reste bornée, et $\bar g$ la métrique limite ; $\Omega_\rho = \{\bar R \leq
  \rho^{-2}\}$ est compact.
- Chaque $\varepsilon$-cou de $\Omega$ est contenu dans un tube, une calotte, une corne (*horn*), une corne coiffée ou une
  double corne.
- Seul un nombre fini de composantes touchent $\Omega_\rho$.
- La topologie de $M$ est la somme connexe des $\bar\Omega_j$ (cornes compactifiées) avec des $S^2 \times S^1$ et des
  $\mathbb{RP}^3$.

**II.4, flot avec $\delta$-coupure.** On fixe $\varepsilon$ ; le voisinage canonique vaut à l'échelle $r = r(\varepsilon)$
(hypothèse a priori) ; on pose $\rho = \delta r$.
- **Lemme II.4.3** : il existe un rayon $h(\delta,\rho,\phi) < \delta\rho$ tel que, profondément dans une corne
  ($\bar R^{-1/2}(x) \leq h$), le voisinage parabolique $P(x, T, \delta^{-1}h(x), -h(x)^2)$ soit un $\delta$-cou **fort**.
  La preuve est par l'absurde : la limite a deux bouts, se scinde par Toponogov en $S^2 \times \mathbb R$, et l'argument
  se répète sur $[-A, 0]$ pour tout $A$, ce qui donne le cylindre rond.
- **Chirurgie** : dans chaque corne, on coupe un $\delta$-cou de rayon $h$ le long de la 2-sphère médiane et on colle une
  calotte presque standard (la courbure ne fait que s'améliorer, par la technique conforme de Hamilton). On jette les
  composantes sans point de $\Omega_\rho$.
- **Ressource décroissante** : chaque chirurgie retire un volume $\geq h^3$, et le volume est majoré. Les temps de
  chirurgie sont donc discrets.
- **Lemme II.4.5 et Corollaires II.4.6–4.7** : après une chirurgie, la région opérée suit la solution standard pendant un
  temps $\theta h^2$, ou bien disparaît entièrement. Les courbes qui la traversent ont une $\mathcal L$-longueur
  (en fait $\int R + |\dot\gamma|^2$) grande.

**Séparation des échelles [D, II, introduction].** « The point is to make $h$ arbitrarily small while keeping $r$
bounded away from zero. » Les paramètres sont choisis dans l'ordre $\varepsilon \to (r, \kappa) \to \bar\delta \to h$.

---

## 12. II.5 : justification des hypothèses a priori

**Proposition II.5.1.** Il existe des suites décroissantes $r_j, \kappa_j, \bar\delta_j$ telles que, pour toute donnée
initiale normalisée et tout $\delta(t) < \bar\delta_j$ sur $[2^{j-1}\varepsilon, 2^j\varepsilon]$, le flot avec
$\delta(t)$-coupure existe pour tout temps et vérifie, sur cet intervalle, le $\kappa_j$-non-effondrement et le voisinage
canonique de paramètre $r_j$.

**Preuve par récurrence sur $j$.**
- **Non-effondrement (Lemmes II.5.2–5.3).**
  - Seules les courbes **admissibles** (qui évitent les régions opérées) ont une $\mathcal L$-longueur définie.
  - L'argument de I.7.3 marche si toute courbe « tout juste admissible » a une longueur réduite $\geq \frac32 + \kappa'$.
  - Perelman introduit $\mathcal L_+$, avec $R_+ = \max(R,0)$ (car $R \geq -6$), et montre (5.3) qu'une courbe qui passe
    près d'une calotte récente a un $\mathcal L_+$ arbitrairement grand quand $\delta \to 0$, en s'appuyant sur 4.6.
- **Voisinages canoniques (II.5.4).**
  - Par l'absurde, au premier temps de violation (c'est une condition ouverte).
  - L'Affirmation 2 de II.4.2 donne une limite à $t = 0$.
  - Pour l'étendre en arrière, il faut qu'il n'y ait pas de chirurgie proche. S'il y en a une, le point est près d'une
    calotte et suit la solution standard (4.5, 4.7, II.2 Affirmation 5) : il a donc un voisinage canonique,
    contradiction.
  - On obtient une solution ancienne $\kappa$-non effondrée : contradiction avec le choix du point.

**Lecture [Int].** Les hypothèses a priori (pincement, voisinage canonique à l'échelle $r$) sont *supposées* pour
construire le flot avec chirurgie, puis *démontrées* pour le flot ainsi construit, par une récurrence sur des
intervalles de temps dyadiques. **La quantité de non-effondrement est choisie pour survivre à l'opération** : c'est
le volume réduit, intégrale le long des courbes, avec une pénalité infinie pour les courbes qui traversent une zone
opérée.

---

## 13. II.6–II.8 : temps long, effondrement, valeur propre

- **II.6.3–6.8** : versions avec chirurgie de I.12.2–12.3 (contrôle de courbure à partir du volume) ; lemmes
  d'Alexandrov élémentaires (6.6).
- **II.7.1–7.3** :
  - $V(t)(t + \frac14)^{-3/2}$ est non croissant et $\hat R = R_{\min}V^{2/3}$ non décroissant ;
  - les points épais convergent après normalisation vers des variétés hyperboliques de courbure $-\frac14$ (arguments de
    Hamilton 1999, rigidité hyperbolique) ;
  - incompressibilité des tores par surfaces minimales (l'aire du disque minimal ne fait que décroître à la chirurgie).
- **II.7.4** : la partie mince est une variété graphée. C'est un théorème d'effondrement à courbure localement minorée,
  « qui n'a rien à voir avec le flot de Ricci » (outil : points critiques de fonctions distance), renvoyé à un article
  ultérieur. Il a été démontré depuis par Shioya–Yamaguchi, Morgan–Tian, Kleiner–Lott, Cao–Ge, et autrement par
  Bessières et coll. [D ; KL §3].
- **II.8** : $\lambda$ (première valeur propre de $-4\Delta + R$) ne décroît pas à travers les chirurgies pour une
  coupure assez fine (Lemme 8.1). D'où (8.2) :
  - un $\lambda > 0$ possible caractérise les sommes connexes de $S^2 \times S^1$ et de quotients sphériques ;
  - $\bar\lambda = \sup\lambda V^{2/3} = 0$ caractérise les variétés graphées ;
  - si $\bar\lambda < 0$, $\bar V = (-\frac23\bar\lambda)^{3/2}$ est le volume hyperbolique minimal.

  Ce sont les analogues exacts des conjectures d'Anderson sur la constante Sigma.

---

## 14. III : extinction en temps fini

**Théorème (III.1.1).** Si la décomposition en premiers de $M$ ne contient aucun facteur asphérique, le flot avec
chirurgie s'éteint en temps fini pour toute métrique initiale.

**Le min-max.**
- $\Lambda M$ est l'espace des lacets contractiles. Pour un lacet $c$, $A(c,g)$ est l'aire minimale d'un disque de bord
  $c$.
- Pour une famille $\Gamma \subset \Lambda M$, $A(\Gamma, g) = \sup_{c\in\Gamma}A(c,g)$.
- Pour une classe non triviale $\alpha \in \pi_*(\Lambda M, M)$, $A(\alpha, g) = \inf_{\Gamma\in\alpha}A(\Gamma,g)$.
- **Une telle classe existe dès que $M$ n'est pas asphérique (Serre).**

**Lemme III.1.2.** $\frac d{dt}A^t \leq -2\pi - \frac12 R^t_{\min}A^t$, au sens des quotients différentiels supérieurs.

*Idée (exacte quand les lacets sont plongés et réguliers).* On fait évoluer les lacets par raccourcissement de courbe et
le disque minimal $D_c$ par le flot. La variation de l'aire vaut
$\int_{D_c}(-\mathrm{Tr}\,\mathrm{Ric}^T) + \int_c(-k_g)$. En dimension 3,
$-\mathrm{Tr}\,\mathrm{Ric}^T = -\frac12R - (K - \det\mathrm{II})$ avec $\det\mathrm{II} \leq 0$ (disque minimal).
**Gauss–Bonnet** donne $\int_D K + \int_c k_g = 2\pi$, d'où la borne.

*Difficulté technique* : des lacets non immergés. Perelman la règle en ajoutant une dimension : on travaille dans
$M \times S^1_\lambda$, où les relevés sont des « rampes » plongées dont le raccourcissement existe pour tout temps
(Altschuler–Grayson 1992). On contrôle ensuite les familles par des $\mu$-réseaux et par l'aire des anneaux minimaux
(2.4–2.5).

**Conclusion (III.1.3).** Les chirurgies sont topologiquement triviales (cas irréductible) et presque 1-lipschitziennes,
donc le lemme passe au flot avec chirurgie. Avec $R_{\min} \geq -\frac{3}{2(t+c)}$, on obtient
$\frac d{dt}\frac{A}{t+c} \leq -\frac{2\pi}{t+c}$ : le membre de droite n'est pas intégrable, alors que $A \geq 0$,
d'où l'extinction.

**III.1.4.** Avec Kneser (ou même sans), cela donne l'*elliptisation* et Poincaré **sans l'analyse en temps long**
(II.6–8).

**Origine [D, III, introduction].** « It does not require any substantially new ideas » : l'argument d'aire de
[Hamilton 1999, §11] et la régularisation d'Altschuler–Grayson. Colding–Minicozzi ont donné indépendamment une preuve par
la largeur des balayages par 2-sphères (2005, puis 2008) [D, KL introduction]. **Ce qui est propre à Perelman** : faire
d'une estimée de décroissance connue un argument d'extinction, en l'appliquant à un *min-max sur une classe d'homotopie
non triviale de l'espace des lacets*. La topologie garantit que la quantité ne peut pas s'annuler sans extinction ; la
géométrie (Gauss–Bonnet) donne une dérive négative universelle [Int].

---

## 15. Corrections, lacunes, et ce que les reconstructions ont dû compléter

[D] Perelman corrige lui-même, dans [II] :
- l'oubli des $\kappa$-solutions compactes à soliton asymptotique cylindrique (II.1.3–1.4) ;
- l'énoncé de I.12.2 (II.6.2) ;
- l'affirmation de I.13.2 sur la minoration du volume des cornes maximales, « injustifiée » et inutile (II,
  introduction ; II.7) ;
- le report du théorème des variétés graphées (II, introduction).

[D, KL introduction] : « we did not find any serious problems, meaning problems that cannot be corrected using the
methods introduced by Perelman ».

Des points ont été complétés en détail par les reconstructions :
- l'existence et l'unicité de la solution standard ;
- la gestion des courbes admissibles ;
- le choix précis des paramètres de chirurgie ;
- les preuves de la compacité des $\kappa$-solutions.

Ce sont des **arguments techniques indispensables**, mais pas de nouvelles idées.
