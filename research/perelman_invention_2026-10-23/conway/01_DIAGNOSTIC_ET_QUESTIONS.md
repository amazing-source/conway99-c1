# 1. Diagnostic : la campagne Conway-99 lue avec les murs de Hamilton, et les cinq questions du mandat

Statuts : **[P]** démontré · **[L]** littérature · **[E]** calcul reproductible · **[S]** verdict de solveur sans
certificat portable · **[A]** analogie · **[C]** conjecture · **[O]** ouvert. Les statuts de la campagne sont repris de
la carte maîtresse (`code/lab_chantier_2026-10-20/CARTE_MAITRESSE.md`, notée CARTE), sans nouvel audit, conformément à la
consigne du 9 octobre.

---

## 1.1 Où en est la campagne (CARTE §2–§3)

**Acquis.** Si un srg(99, 14, 1, 2) existe, il est asymétrique (C1).

| énoncé | statut |
|---|---|
| Pas d'automorphisme d'ordre 3 (C3) | P + Lean |
| Pas d'automorphisme d'ordre 7 (C7) | P + Lean |
| Pas d'automorphisme d'ordre 11 | L (Behbahani–Lam ; Wilbrink 1984) |
| Pas d'automorphisme d'ordre 2 (C2) | S (Théorème R relu ; 25,8 M paires exclues sans certificat) |
| r = rang₇(A − 3I) ∈ {37, 39, 41, 43} | conditionnel (thêta de niveau 7, audité par Codex) |
| P ≤ 852 prismes ; 3P + 4G ≤ 2772 | conditionnels sur un recensement engendré par programme |
| Théorème 6.1 : le rang 37 se réduit à un calcul fini sur les droites à t ≤ 7 | P (relu par un agent) |
| Tout Conway a une droite avec c(L) ≤ 3 | S |
| Γ est tordu (L1) | P (Makhnev 1988 ; preuve indépendante de l'équipe) |
| Pas d'étalement régulier (note 165) | P |

**Non acquis.** Aucune exclusion de C1, ni d'un des rangs 37 à 43. Il reste cinq routes (A à E), toutes ouvertes. La
cible n° 1 est **ODD-PURE** et ses deux compagnons.

**Méta-leçon de l'équipe** (CARTE §4, statut H) : toutes les fermetures combinent arithmétique globale, positivité ou
rang, et intégralité.

---

## 1.2 Correspondance avec le programme de Hamilton [A]

Le premier travail (`../etude_perelman/01_LE_MUR_AVANT_PERELMAN.md`) isole le mur de Hamilton : une estimée a priori
manquante (le non-effondrement), sans laquelle la machinerie existante (compacité, classification, chirurgie) ne démarre
pas.

| Hamilton avant 2002 | campagne Conway |
|---|---|
| un flot canonique, la compacité sous non-effondrement, Harnack, le pincement | la structure locale exacte (cadre, droites, G_T), des contraintes arithmétiques globales (fenêtre 7-adique), des réductions finies (rang 37), des bornes (P ≤ 852) |
| il manque une estimée : le non-effondrement (M1) | il manque un énoncé de capacité locale : ODD-PURE (+ Z), ou ses équivalents Q7, N9-NG, H-MATCH |
| une fois l'estimée acquise, la machinerie conclut | une fois ODD-PURE acquis, P ≤ 852 force une paire sans grille où il s'applique, et c'est fini (L08-027) |
| l'estimée était appuyée par des exemples réels | l'énoncé est appuyé par des blocs qui ne peuvent pas exister dans Conway (CARTE §5 n° 6) |
| marge : une constante κ > 0 | marge : zéro (λ_max jusqu'à 0,99993) |

**Lecture.** Structurellement, la campagne est « Hamilton avant Perelman » : le programme est posé et l'estimée unique
manquante est identifiée. Trois différences pèsent lourd :
1. il n'y a pas de flot (Théorème A.1, démontré) ;
2. les données qui soutiennent l'estimée viennent d'objets qui n'existent pas ;
3. la marge est nulle, si bien que l'estimée est un énoncé de **rigidité** plutôt qu'une inégalité.

Le troisième point oriente vers S3/T4 (classer les cas d'égalité) plutôt que vers S1/S2 (monotonie avec marge).

---

## 1.3 Les cinq questions du mandat

### Q1. Avons-nous choisi les bons objets ?

Le critère tiré de Perelman : un objet est bon s'il porte une quantité monotone ou rigide, et s'il survit aux opérations
que l'argument utilise. On a testé les objets que la lecture perelmanienne suggère.

- **Courbures** (chapitre 2). Elles sont toutes constantes sur Conway (Théorème A.1, A.2) : ce sont de mauvais objets
  pour lui. La seule exception est la parité d'appariement η (A.3), qui n'est pas une grandeur monotone.
- **Complexe triangles-carrés, π₁, H¹** (chapitre 3). Ce sont de bons objets pour la *famille* : ils expliquent L1 (Makhnev),
  BvLS = Golay et la structure des huit graphes connus à 243. Sur ces huit graphes, π₁ ≠ 1 exactement quand il y a un
  étalement régulier. Pour Conway, qui n'en a pas, ils sont conjecturalement vides. Surtout, le type topologique prédit
  (simplement connexe) est réalisé par les quatre srg(243) sans étalement Γ₅ à Γ₈ : la topologie seule ne peut pas
  exclure Conway (§3.7).
- **Blocs locaux de Gram de l'équipe.** Ils portent l'information arithmétique et de rang, d'où sont venues toutes les
  fermetures.

**Verdict.** Les objets de l'équipe sont les bons pour le seul canal qui ait marché. Les objets nouveaux suggérés par
Perelman sont maintenant caractérisés, et ne sont pas meilleurs pour Conway. Un objet nouveau mérite pourtant
l'attention : le **graphe d'appariement B_xy** d'une non-arête. Il porte à la fois la seule courbure libre (η) et toute la
cohomologie (jauge radiale, Théorème 3.6).

### Q2. Avons-nous le bon énoncé intermédiaire ?

Voir §4.3. L'architecture est correcte : un énoncé unique, et un comptage global qui force son applicabilité. Il manque
exactement le trait 3 de Perelman : une quantité monotone à cas d'égalité rigide.

Au niveau de la classe 𝒦₁₄, l'énoncé intermédiaire naturel (non-effondrement à l'échelle 3) est équivalent au problème
(Corollaire 2.2) : il n'y a rien de plus faible à démontrer d'abord.

Sur ODD-PURE lui-même, la transposition de S1 redonne exactement le lemme impair de l'équipe. Le cas ouvert est
précisément là où le mécanisme s'arrête (Proposition 4.3) : la permutation formelle ne préserve pas l'énergie.

### Q3. Cherchons-nous une contradiction statique au lieu d'étudier une transformation des configurations ?

Oui, la campagne est statique. Les transformations disponibles :
- **revêtements et quotients** : chapitre 3, théorie complète, aucune obstruction ;
- **bascules** : note 165, « bascule = rotation d'espaces propres », D = 7(P′₃ − P₃) à 99, avec un critère de rigidité ;
- **mouvements locaux** : recherche locale, recuit (CARTE §4.A).

Le Théorème A.1 montre qu'aucun flot naturel n'existe sur l'objet, et le chapitre 3 que les revêtements structurent la
famille sans rien exclure. Une transformation ne démontre une non-existence que si elle s'accompagne d'une quantité
monotone à égalité rigide. On n'en connaît aucune sur les configurations partielles. **L'approche statique n'est donc pas
une erreur de méthode : elle est forcée, tant que cette quantité manque.** C'est l'ingrédient à chercher (§4.3(e)).

### Q4. Nos relaxations perdent-elles une information globale ?

Oui, et on peut dire laquelle.
- Toute relaxation réelle voit b₁ = 0, des courbures constantes et un spectre fixé (Théorèmes A.1 et 3.3(a)).
- L'information qui distingue les graphes est de **torsion** (H¹(X; 𝔽₃), rang₇), ou de **parité** (η).
- À 243, H¹(𝔽₃) vaut 6, 1 ou 0 selon le graphe ou son revêtement, alors que b₁ = 0 partout.

C'est l'explication précise de la méta-leçon de l'équipe : ce que les paramètres ne fixent pas vit dans des invariants
finis et arithmétiques, invisibles sur ℝ.

### Q5. Quelle quantité ou structure est réellement imposée par les paramètres ?

**Imposé :**
- spectre, marches fermées, fonctionnelles de chaleur, zêta d'Ihara ;
- toutes les courbures 2-locales (A.1, A.2) et le cadre (Aut = 2⁷·7!) ;
- la torsion (L1) et l'absence d'étalement régulier (note 165) ;
- les égalités en k − 14 (variance nulle, §4.2(a)) ;
- r impair dans la fenêtre (équipe) ;
- b₁ = 0 (3.3(a)) et |π₁| ≤ 82 859 (3.3(c)).

**Libre :**
- la distribution de η et la structure des cycles des B_xy. H¹ et π₁ ne sont pas fixés par une preuve, mais ils sont
  conjecturalement triviaux (Conjecture 3.10, appuyée par Γ₅ à Γ₈) ;
- les graphes de droite G_T ;
- r dans {37, …, 43} ;
- P et G (bornés).

Cette liste délimite l'espace des phases où toute obstruction doit vivre.

---

## 1.4 Faut-il abandonner des représentations ?

Le mandat le permettait. Conclusion : **aucune représentation de l'équipe n'est à remplacer** par une représentation
perelmanienne. Deux ajouts sont utiles :
- le langage topologique (π₁, codes parfaits, jauge radiale) donne une forme propre à la « torsion » (L1, note 165) ;
- l'objet B_xy relie la seule courbure libre et la cohomologie.

Ces ajouts organisent ; ils ne ferment rien.
