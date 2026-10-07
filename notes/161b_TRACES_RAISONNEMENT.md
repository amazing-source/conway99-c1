# 161b — Traces de raisonnement du dépôt openai/math : analyse (07/10)

*Rapport d’un agent de lecture qui a lu les 11 fichiers de `reasoning_traces/` en entier. Il est versé tel quel, avec une
correction en fin de note. Voir aussi la note 161.*


## 0. Sources et limites

J'ai lu en entier les 10 fichiers `.txt` et le `.tex` de Mézard–Parisi, dont le contenu est le même que celui du `.txt`. Il faut garder en tête trois limites :

- **Ce ne sont pas les pensées brutes du modèle.** Chaque fichier est un résumé rédigé par un tiers, avec quelques « VERBATIM EXCERPT ». Seuls ces extraits montrent la réflexion directe, et ils ont été choisis par le rédacteur.
- **Aucune trace ne montre de code ni de calcul machine.**
- **Le dépôt fait état d'une vérification formelle, que je n'ai pas contrôlée.** Le fichier `lean/formalization.yaml` liste des formalisations Lean pour Mahler symétrique et son cas d'égalité, pour Vlasov–Maxwell et pour un contre-exemple de Kaplansky « finitely presented ». Je n'ai ouvert aucun de ces fichiers Lean.

Abréviations utilisées : [kap] kaplansky-direct-finiteness-characteristic-two, [pi] irrationality-exponent-of-pi, [mahler] symmetric-and-general-mahler-conjectures, [ap] quasipolynomial-arithmetic-progressions, [sdp] basic-semidefinite-threshold-np-hardness, [ffac] free-group-factor-isomorphism, [mp] mezard-parisi-formula, [chowla] ordinary-two-point-correlations, [vm] relativistic-vlasov-maxwell, [heis] spontaneous-magnetization-quantum-heisenberg-ferromagnet.

## 1. Trace par trace

**[kap]**
- **Problème.** Est-ce que ab=1 entraîne ba=1 dans K[G], en caractéristique p et pour tout groupe G ?
- **Issue.** Un contre-exemple candidat en caractéristique 2. La Partie I se termine en plein audit (« had not identified a flaw »). La Partie II en tire un automate cellulaire injectif non surjectif, T_b(x)(g)=Σ b_u x(gu), avec pour témoin la configuration δ_h hors de l'image.
- **Tournant.** Pendant une dizaine de sections, le modèle tente des preuves : relèvements de Witt, entropie, spectre à la Thom, canaux gaussiens, lemme de Siegel. En parallèle, la construction progresse par relaxations successives :
  1. des sommes de sous-groupes d'ordre impair qui couvrent chaque élément non trivial un nombre pair de fois ;
  2. puis des poids matriciels de rang 1, de somme nulle sur chaque hyperarête mais de somme globale de rang m ;
  3. puis une interpolation polynomiale sur un espace affine troué sur F_{2^h}, idée explicitement empruntée aux codes LDPC quantiques (Golowich–Lin, Dinur–Liu–Zhang) ;
  4. enfin une maille ≥12 obtenue par lemme local de Lovász et théorème de Linnik, et un plongement des groupes locaux certifié par la formule d'Euler.
- **Impasses.** Le relèvement de signes en caractéristique 0 échoue (des diagrammes sphériques impairs tuent l'involution centrale). L'argument d'entropie échoue à cause de la non-moyennabilité. L'argument d'information gaussienne donne une inégalité « in the wrong direction ».

**[mp]**
- **Problème.** La borne inférieure de la formule de Mézard–Parisi.
- **Issue.** Une preuve est revendiquée.
- **Démarche.** Le modèle commence par chercher un contre-exemple dans les hypothèses, sans succès. Les interactions constantes lui servent ensuite de test de normalisation.
- **Tournant.** Des perturbations de Poisson marquées, combinées au décalage d'un niveau de toutes les profondeurs de branchement : chaque nouveau sommet de branchement « paie » alors un facteur de divergence frais.
- **Abandonné.** Le pinning (mauvais poids). Une affirmation de pureté exacte (« proves too strong »). Le transfert depuis le cadre bayésien (les lois diffèrent).

**[ffac]**
- **Problème.** L(F₂) est-il isomorphe à L(F₃) ?
- **Issue.** Un isomorphisme est revendiqué, conditionnel à un flot et à une étape de « génération limite ».
- **Tournant.** Tous les invariants essayés (largeur de micro-états, L²-homologie, dérivées de Fox, entropie) échouent sur le même écueil, les changements de générateurs incontrôlés (« Same old. »). Le modèle bascule alors vers la construction :
  - reformulation N₂≅N₃ ⟺ 1/√2 ∈ F(N₂) ;
  - analogie classique de la « racine manquante » (« Aha! For classical vertex labels… non-uniform distribution… ») ;
  - flot qui absorbe un générateur libre ;
  - transfert des rangs 3/4 vers 2/3 par les formules d'interpolation de Dykema.

**[pi]**
- **Problème.** μ(π)<5/2 (série de Flint–Hills), puis μ(π)=2.
- **Issue.** μ(π)≤62/25 est revendiqué, puis μ(π)=2 « with no effective denominator threshold ».
- **Démarche.** Une réduction propre en premier : Σ1/(k³‖kπ‖²)<∞ ⟺ Σq_{j+1}²/q_j³<∞. Ensuite une trentaine de sections où Padé, multiplication complexe, formes modulaires, thêta, BBP et grilles gamma meurent tous sur la même « volume obstruction ».
- **Tournant.** Un déterminant d'interpolation à poids simpliciaux, une troncature unitriangulaire du logarithme et un argument d'amplitude sur un éclaté. Le modèle remarque lui-même que l'optimisation des paramètres semble autoriser tout μ>2. Il cherche une contradiction (tests de Liouville), n'en trouve pas, et escalade jusqu'à μ=2.

**[ap]**
- **Problème.** La conjecture d'Erdős sur la somme des inverses, puis des bornes quasipolynomiales pour r_k(N).
- **Issue.** Des preuves proposées de r_k(N)≪N/(log N)³ puis d'une borne quasipolynomiale. Une inquiétude de circularité reste explicitement ouverte (§26).
- **Tournant.** Un diagnostic chiffré : la croissance d↦d^C et les récurrences H_{j+1}=κH_j², P_{j+1}=P_j+(2+P_j)^E condamnent l'itération naïve. Le modèle en déduit des « paquets » d'incréments à gain multiplicatif K, un rang additif d+d₀ et des budgets de largeur par couche.
- **Impasses.** Compter des progressions à partir de bornes supérieures seules (« can't rule holes »). La transférence de Conlon–Fox–Zhao, qui serait circulaire. Les contre-exemples de Rankin et Keleti, quantitativement trop éloignés.

**[chowla]**
- **Problème.** Elliott binaire corrigé en moyenne ordinaire, puis Chowla affine avec un gain (log X)^{−c}.
- **Issue.** Les deux résultats sont revendiqués, en listant explicitement les estimées dont ils dépendent.
- **Tournant.** Des graphes de diviseurs pondérés à la Pilatte, avec deux bandes de premiers : D(n)=β^{−ω_C(n)}2^{ω_Z(n)}.
- **Auto-correction.** Borner ponctuellement un facteur de retour avant l'intégration signée détruisait l'annulation.

**[vm]**
- **Problème.** Existence globale pour Vlasov–Maxwell relativiste en 3D.
- **Issue.** La continuation globale est affirmée, en s'appuyant sur trois estimées listées comme encore à établir.
- **Tournant.** Un bootstrap signé |ΔV|≤MP√I+AIP²log(e+P)/w, avec intégration par parties le long des étiquettes sources, puis une contradiction d'exposants (H<0,41z contre H>0,496z).
- **Rattrapages.** Un décalage d'hypothèses (le critère de Luk–Strain exige H⁵) et la normalisation f/(4π).

**[heis]**
- **Problème.** Aimantation spontanée du ferromagnétique de Heisenberg quantique, d≥3.
- **Issue.** Un état KMS aimanté est revendiqué.
- **Tournant.** Le passage symbolique à F(X,Y)=E∏(X_i+Y_{π(i)}), dont la stabilité donne une dépendance négative, puis une induction sur des « tests d'épingles ».
- **Impasse.** L'identité de connectivité moyenne : « self-consistency with arbitrary phase fraction! ».

**[sdp]**
- **Problème.** NP-dureté au seuil BasicSDP sans supposer UGC.
- **Issue.** Un argument affirmatif proposé.
- **Tournant.** Le modèle remarque que l'énoncé implique déjà UGC (« Wait insight: … already enough for UGC via parallel repetition! »). Il réoriente donc la cible vers la dureté de Unique Games. Il construit un gadget explicite Q(x)=(x₂x₃,x₁x₃,x₁x₂) sur F_{2^d} et des projections creuses β=k^{−2/3}.
- **Impasses.** Des prouveurs tricheurs qui exploitent les projections (« cheater chooses arbitrary g… independent of actual satisfiability! »).

**[mahler]**
- **Problème et issue, Parties I et II.** Mahler symétrique et son cas d'égalité sont revendiqués. La clé est une fonction f(ζ)=(8/π²)Σ_{k impair}ζ^k/k², dont la partie réelle au bord est uniforme sur [−1,1] ; les probabilités de faisabilité de bases donnent la borne. L'égalité passe par des médianes métriques et le théorème de Hansen–Lima.
- **Partie III (cas général).** Une exploration très longue, avec de nombreuses reformulations que le modèle reconnaît lui-même comme équivalentes au problème de départ. Il obtient une constante plus faible, p^{1/n}≥e^{−1/2}. La fin reste conditionnelle à des inégalités scalaires, ramenées à la positivité des coefficients de Bernstein de polynômes de degré 30 et 32.

## 2. Habitudes récurrentes

**a. Reformuler, puis vérifier l'équivalence et repérer les reformulations stériles.**
- Équivalences explicites : critère par fractions continues ([pi]) ; 1/√2 ∈ F(N₂) ([ffac]).
- Contrôle qu'une réduction ne renforce pas le problème : « Cone Laplace inequality exactly equivalent for hyperplane sections, not all log-concave. » [mahler].
- Reconnaissance d'un tour en rond : « So tangent inequality for simple B exactly Mahler… Not progress unless geometry helps. » ; « So pure union Mahler as hard as symmetric general! » [mahler].

**b. Le « test de Liouville » : un argument qui prouverait trop est faux.**
- « Then Roth would give exponent2 all numbers. » ; « Wait this would work for any transcend, contradiction with Liouville. Examine. » [pi].
- « That would even stronger than Mahler (contradiction extremal). » [mahler].
- [heis] « tests whether the construction would inadvertently prove more than intended ».

**c. Les objets extrémaux comme banc d'essai.**
- Orthant, simplexe, polytopes de Hanner, cross-polytope, cônes semi-définis positifs, 24-cell : « Ball violates desired geometric mean inequality! » ; « Thus direct criterion fails globally for PSD cones! » ; « If global min proof must compare all stationary including Hanner. » [mahler].
- [kap] : deux copies de S₃ pour exclure une petite construction de coin.

**d. Tout chiffrer, sous forme de budgets.**
- 0,20008 contre 0,213 ([pi]) ; H<0,41z contre H>0,496z ([vm]).
- « Need b<a−1 for rare. Generic LLL wanted b>a+4. Conflict! » [kap].
- « At depth log p yields p^{C log p}… rank growth must be additive/hierarchical » [ap].

**e. Fixer l'ordre des paramètres et des quantificateurs.**
- « We cannot choose m after post-b because b may be (p+m)^D… Need m fixed function p before defining b. » [ap].
- [heis] : constantes fixées avant de choisir p.
- [sdp] : choix circulaires entre la répétition parallèle de Raz (dépendante de l'alphabet) et celle de Rao.

**f. L'obstruction qui revient sert de signal de bifurcation.**
- « Difference P(V)-U small but derivative of difference can be huge; no closability. Same old. » [ffac].
- « This is same volume obstruction yet again. » ; « Filtration cannot contradict pure volume. Must exploit link across levels… » [pi].

**g. Alterner preuve et réfutation.**
- [kap] « moved between proving direct finiteness… and constructing a counterexample ».
- Chasses au contre-exemple dans [mp] (hypothèses), [chowla] (phases sur les premiers), [ap] (Rankin, Keleti), [sdp] (algorithme pour Unique Games affine).
- [ffac] passe de l'obstruction à la construction.

**h. Distinguer existence et abondance.**
- « Existence tiny row fiber via theorem not enough because advice U gets random… Need positive probability… of hitting a whole fiber. » [sdp].

**i. Vérifier ses propres affirmations.**
- Orientation : « Correct order?… T_bT_a = T_{ba}. So yes. » [kap].
- Spécialisation : « Matrix rank cannot rise under specialization because all larger minors zero *as polynomials*… Good. » [sdp].
- Erreurs de comptage rattrapées : « Without direct for all six G, E labels may not repeat!… k=6 not covered by Vandermonde in n=10b. » [kap], d'où le passage de 10b à 12b.
- Circularité : « Complete solution cannot assume irrationality; period exists nonzero. » [pi].
- Audits par chaîne de dépendances : [ap] §22, « the audit follows a dependency chain ».
- Listes explicites d'obligations restantes : [chowla], [vm].
- Certificats finis : la positivité de Bernstein, « all b_r>0 ensures » [mahler].

**j. L'enthousiasme précède souvent un renversement.**
- « Fractional denomin constants independent w! This is huge. » puis « So any small f with reciprocal gap must λ=0! » [pi].
- « This would be a full proof if derivative identity… works. » puis « wrong direction » [kap].

**k. Calcul : absent des traces.**
- Les constantes numériques semblent calculées, mais aucun outil n'apparaît.
- Les énoncés de problème découragent la force brute : « Brute-force enumerations and computer-assisted proofs are strongly discouraged » [mp] ; « unproved word equalities… is not a certificate » [kap].
- Le modèle privilégie des certificats lisibles : identités, formule d'Euler, coefficients de Bernstein.

## 3. Problèmes d'existence discrète : comment [kap] a trouvé l'objet

1. **Changement d'objet cible.** Le modèle passe par les présentations universelles de Dykema–Heister–Juschenko pour se ramener à des motifs d'annulation finis. Il vise ensuite une **identité locale/globale** : des vecteurs x_v ∈ K^m vérifiant Σ_{v∈ℓ} x_v x_vᵀ = 0 sur chaque droite ℓ, mais Σ_v x_v x_vᵀ = −I_m globalement.
2. **Construction algébrique, sans recherche.** Les droites affines complètes de F_q^n, avec q=2^h, annulent les polynômes de degré ≤q−2. En retirant des points d'interpolation (les « trous »), on obtient une somme globale non nulle. Un conflit de paramètres du lemme local est résolu par une partition des fibres par droites relevées (x, ℓ(Jx)), où J n'a pas de vecteur propre. Le théorème de Linnik contrôle ℓ ≡ −1 (mod q¹⁰⁰). Le modèle désigne les objets par des « canonical least choices » : le certificat est une preuve, pas une donnée.
3. **Pourquoi la caractéristique p est indispensable.** Une identité de double comptage : D·Σ_v W_v = 0 avec D=0 dans K. « Our mod2 D divisible q ensures. Thus no lift. Positive characteristic essential. »
4. **Certificats de non-dégénérescence.**
   - Plongement des groupes locaux : un graphe planaire équilibré minimal, avec B≤E/3, W≤E/2+1/2 et F≤E/6+1, contredit B+W+F=E+2.
   - Le fait que ba≠1 est prouvé par une contradiction de rang (t>m) après augmentation, sans calculer aucun coefficient.
5. **Exclusions en chemin.**
   - Le théorème de de Bruijn–Erdős élimine des configurations (« Excellent. This kills path/star if neighbors always leaves. »).
   - Un argument de rang interdit les couplages parfaits.
   - Une analyse de doubles classes sur S₃×S₃ exclut une petite construction.
6. **Tests contre les théorèmes connus.** Le candidat est confronté aux résultats sur les groupes sofiques et surjonctifs, à Farrell–Jones (« FJ computes K0 as abelian group with action but not monoid positivity. »), aux théorèmes de finitude résiduelle de Wise et au critère de Berlai.
7. **Transport du certificat.** La Partie II convertit le contre-exemple en automate cellulaire, en vérifiant le côté de la multiplication puis en exhibant un témoin explicite.

## 4. Critique

- **Surrevendication systématique.** Huit problèmes ouverts majeurs sont déclarés résolus. Les conclusions reposent souvent sur des étapes que les résumés qualifient eux-mêmes de « proposed » ou « conditional ».
- **L'escalade de [pi] est le cas le plus risqué.** Le modèle remarque des bornes « unexpectedly strong » qui mènent jusqu'à l'exposant 2. Il traite cela comme un test qu'il ne parvient pas à mettre en défaut, au lieu d'y voir un signal d'alarme, et revendique μ(π)=2 sans seuil effectif.
- **Des audits par le même esprit, répétés en boucle.** [pi] §35–44 et [kap] §13–22 recommencent les mêmes vérifications « without identifying a flaw ». Une erreur réelle (le comptage 10b/12b) n'est apparue que tardivement.
- **Des dépendances non établies au moment de conclure.** Les hypothèses de Lampert–Ziegler sont « still to be checked » ([ap]). Les hypothèses tirées de Hartshorne ou Lazarsfeld « still had to be established » ([pi]). Les polynômes de degré 30 et 32 de [mahler] restent à certifier. [kap] n'est jamais instancié sur un exemple concret.
- **Des souvenirs bibliographiques incertains** (« tentative G-function recollections », Gordon–Meyer–Reisner « uncertain about its method »), même s'ils sont parfois testés.
- **Aucune expérimentation numérique visible**, et les traces sont abrégées avec un biais de sélection.

## 5. Habitudes à adopter pour srg(99,14,1,2)

1. **Mettre en place un « test de Liouville » systématique.** Faire passer tout lemme de non-existence par les membres connus de la famille λ=1, μ=2 : srg(9,4,1,2) et vos deux srg(243,22,1,2). Un lemme qui tue l'un d'eux est faux. Votre second graphe à 243 sommets joue désormais le rôle des nombres de Liouville et des polytopes de Hanner.
2. **Vérifier chaque réduction dans les deux sens.** Pour les sous-problèmes issus des star complements et des boules de triangles, contrôler explicitement l'équivalence, comme le fait [mahler] (« exactly equivalent… not all log-concave »). Si une réduction exclut un graphe à 243 sommets alors qu'elle ne devrait pas, elle est trop forte.
3. **Formaliser la question « pourquoi seulement mod p ? ».** Rappel élémentaire : (A−3I)(A+4I)=2J et −4≡3 (mod 7), donc (A−3I)²≡2J (mod 7) et rang₇(A−3I)≤50. Pour chaque identité locale de votre décomposition en triangles, déterminer si elle se relève à ℤ (et tombe alors sous les contraintes de réseau) ou si elle n'existe que mod 7. C'est précisément l'identité de double comptage de [kap].
4. **Chercher la construction sous forme d'identité locale/globale.** Les 231 triangles forment un espace linéaire partiel (droites de taille 3, 7 droites par point). Chercher des poids ou des vecteurs sur F₇ ou F_q qui s'annulent sur chaque droite et dont la somme globale est imposée. Importer des constructions de codes (évaluations polynomiales, droites affines), comme [kap] l'a fait avec les codes LDPC.
5. **Tenir un registre des obstructions, avec une règle de bascule.** Quand la même configuration bloque trois routes indépendantes (des cœurs UNSAT identiques, par exemple), changer de côté : construire en exploitant cette configuration, ou changer d'énoncé cible, comme [ffac] et [sdp].
6. **Écrire des budgets explicites avant d'investir.** Par exemple, le nombre de structures partielles attendues à chaque profondeur comparé au taux d'élagage. N'abandonner une route que si l'obstruction est structurelle et pas seulement une affaire de constantes (« Filtration cannot contradict pure volume »).
7. **Fixer l'ordre des paramètres dans la chaîne SAT.** Choisir la brisure de symétrie et les représentants d'orbites avant de découper en cas, et vérifier que les deux restent compatibles d'une branche à l'autre. Exiger des preuves DRAT ou LRAT validées par un vérificateur certifié, plus un ré-encodage indépendant.
8. **Associer à chaque enthousiasme un contre-test désigné.** Un « this is huge » doit déclencher le test 1, une vérification exhaustive sur un petit cas et une relecture par une autre personne ou un autre outil. Les audits répétés par le même agent n'ont pas suffi dans [pi].
9. **Confronter tout candidat aux théorèmes connus utilisés comme contraintes.** Une structure partielle de srg(99) doit être vérifiée contre l'entrelacement des valeurs propres (multiplicités 54 et 44 pour 3 et −4), les conditions de Krein et les restrictions publiées sur les automorphismes, comme [kap] s'est mesuré aux résultats sofiques et surjonctifs.
10. **Viser l'abondance, pas seulement l'existence** (l'habitude h de [sdp]). Pour les recherches par switching depuis des configurations partielles, mesurer la fréquence des voisinages favorables plutôt que de se contenter d'un exemple, et préférer les invariants qui restent stables sous switching.

## Correction
- **Point 5.3 : la borne énoncée est juste, mais elle est faible.** (A − 3I)(A + 4I) = 2J et −4 ≡ 3 (mod 7) donnent bien
  rang₇(A − 3I) ≤ 50.
- **On a mieux sans calcul.** Le rang sur ℚ vaut 45, puisque 3 a la multiplicité 54, et le rang mod p ne dépasse jamais le rang
  sur ℚ, d’où rang₇(A − 3I) ≤ 45 (déjà dans structures/REVUE).
- **Le reste de cette piste est déjà exploré.** Le côté mod 7 l’est dans les notes 155–156 (invariant de classe φ mod 7).
