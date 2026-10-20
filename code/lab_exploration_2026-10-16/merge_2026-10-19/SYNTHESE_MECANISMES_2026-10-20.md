# Pourquoi le graphe de Conway semble impossible : les mécanismes, leur profondeur, leurs limites, et les routes finies

LAB, 20/10/2026, soir. Demande de l'utilisateur : « collecte toutes les heuristiques menant vers l'impossible, pourquoi
elles sont là en profondeur, pourquoi ça meurt, pourquoi ça ne marche pas, pourquoi parfois ça ne marche pas, comment
rendre le mécanisme global, comment exclure ce graphe au final ».

**Sources.**
- Trois collectes systématiques de l'archive, faites par des agents en lecture seule, avec fichiers et lignes. Les clés
  de sources sont au §10.
- Les calculs du jour (NOTE_BOOST_2026-10-20.md).
- Les notes du dossier `merge_2026-10-19`.

**Statuts.**
- **P** : preuve écrite, non relue par un humain.
- **C** : calcul exact avec certificat vérifié.
- **E** : calcul exact sans certificat exporté (moteur maison).
- **S** : verdict de solveur sans certificat.
- **O** : ouvert.
- **R** : réfuté.

Tout ce qui suit est dérivé par des IA. Aucune relecture humaine, aucune vérification Lean, sauf C3 (Lean 4).

---

## 0. L'essentiel

### 0.1 Ce qui est établi

- **Groupe d'automorphismes.**
  - Aut(Γ) ⊆ {1, Z₂, Z₃} : littérature, recopié et non reprouvé.
  - Z₃ est exclu (C3 : P + Lean).
  - Z₂ est exclu (C2 : P + C + S). Seules des sessions IA l'ont vérifié ; l'énumération des paires n'est recoupée que
    sur 4 réseaux sur 156.
  - **Il reste C1 : Γ sans aucune symétrie.**
- **Fenêtre de rang.**
  - Le 7-rang r de A − 3I est impair et vaut au plus 43 (L22 de Codex, P).
  - r ≤ 35 est exclu par séries thêta et identités exactes (C, vérificateur autonome, audit par IA seulement).
  - Donc **r ∈ {37, 39, 41, 43}**.
- **Droites.**
  - m ≤ 4 : toute Conway a une droite dont le graphe local a au plus 4 composantes (certificat rationnel P ≤ 852, C).
  - L23 : au rang 37, toute droite générique a (τ|7) = −1 (P).

### 0.2 Le mécanisme qui tue : un seul fil rouge, la surdétermination

Partout où l'on a vu mourir quelque chose, trois familles de contraintes agissent **ensemble** sur les mêmes sommets :
- arithmétique, mod 7 ;
- réelle, la positivité ;
- combinatoire : λ = 1, μ = 2.

Le nombre de contraintes croît comme le **carré** de la taille de la configuration, puisqu'il vient des paires. La
liberté, elle, ne croît que **linéairement**. Au-delà d'un seuil, plus rien ne survit. Prise seule, chaque famille est
toujours satisfaisable (§7.2).

Le seuil dépend de la **quantité d'information 7-adique** (le filtre réel ne dépend pas du rang, mais il ne suffit
pas seul) :
- elle est maximale au rang 37, où le graphe lointain d'une droite est une *fonction* du graphe proche mod 7 ;
- elle décroît aux rangs 39 à 43, où des vecteurs résiduels cachés absorbent les contraintes.

### 0.3 Pourquoi ça ne meurt pas toujours

- **Sous le seuil, les configurations existent** :
  - lois à quatre étoiles satisfaisables ;
  - R7 SAT ;
  - étoile d'une droite au rang 41 ou 43, heuristiquement satisfaisable ;
  - positivité continue, toujours faisable : le centre fractionnaire donne T = 3P, U = 4P.
- **La mort, quand elle arrive, est statistique.**
  - Les valeurs de Green sont pseudo-aléatoires.
  - Les noyaux minimaux n'ont pas de motif local (noyau HB : 30 labels sur 44 ; R8 : 39 ou 40 labels sur 44 ; étoiles :
    7 lointains).
  - On n'en tire donc pas de lemme court. Seule une énumération exhaustive rend la mort « globale ».

### 0.4 Les routes finies vers l'exclusion

| route | énoncé | rangs | état | coût |
|---|---|---|---|---|
| **A : R8 (+ CEGAR)** | une instance SAT (52 labels, 1 326 arêtes autour d'un sommet), UNSAT ⇒ pas de Conway (modèle audité, sain) | **tous** | indécidée | R8 seul : 5·10⁷ à 10¹² heures-cœur, pas réaliste ; variante CEGAR à piloter localement |
| **B : droites au rang 37** | théorème de réduction (seule entrée : P ≤ 852) : toute droite à t ≤ 7 doit passer le test d'étoile | 37 | moteur validé, 100 % des droites testées meurent (33 754/33 754) | environ 6,5·10⁴ heures-cœur avec `line37_fast` |
| **C : dichotomie c** | m = 3 (registre), branche (II) (≥ 33 droites c ≤ 2) | tous | 35 + 14 gabarits ouverts, (II) sans méthode | — |
| **D : lois locales avec pont prouvé** | (N9-NG)/NG5, (T8)/(T15), (H-MATCH) ⇒ pas de Conway | tous | lois ouvertes | — |
| **Rangs 39 à 43** | aucune route finie faisable | 39–43 | il faut un théorème | 3 agents en cours |

---

## 1. Le cadre en dix lignes

- Γ = srg(99, 14, 1, 2), A sa matrice d'adjacence, M = A − 3I. Sur ℤ, M(M + 7I) = 2J ; donc M² ≡ 2J (mod 7).
- Valeurs propres : 14 (×1), 3 (×54), −4 (×44). Mod 7, 3 ≡ −4, et r = rang₇ M.
- Réseaux de vecteurs propres entiers :
  - E₋ (valeur −4), de rang 44 et de déterminant 9·7^(r−1) ;
  - E₃ (valeur 3), de rang 54 et de déterminant 11·7^(r−1).
- **Droite** : un triangle T. Son voisinage N(T) compte 36 sommets proches, répartis en classes C₀, C₁, C₂ de 12. Il y a
  60 sommets lointains.
- Le graphe local G_T est cubique sur les 36 sommets : partenaires et trois bijections entre classes. On note c(T) son
  nombre de composantes, τ son nombre d'arbres couvrants et d = dim ker₇(3I − G_T).
- Un lointain w a exactement 6 voisins proches, ses « noms », 2 par classe. E est l'incidence noms × lointains, et R le
  graphe lointain, 8-régulier sur 60 sommets.
- **Étoile** d'un proche x : les 10 lointains adjacents à x. λ = 1 force sur N(x) un couplage parfait. Sur l'étoile, cela
  donne 4K₂ + 2K₁.
- **Sommet et labels** : les 84 non-voisins d'un sommet v sont étiquetés par les paires non appariées de ses 14 voisins.
  L'étoile L_r est formée des 12 labels contenant r.

---

## 2. Couche I : l'arithmétique globale (réseaux, séries thêta, fenêtre de rang)

| mécanisme | énoncé | statut | ce qu'il tue | pourquoi | où il s'arrête, et pourquoi |
|---|---|---|---|---|---|
| formule d'oddité / Milgram sur E₋ | r impair, r ≤ 43 | P [CX101, rank7.tex] | r pair, r = 45 | 44 + 6α + 4δ ≡ 0 (8) avec α = r − 1 ; à r = 45 la partie unimodulaire est nulle, det V ≡ 9 est un carré, contradiction | « aucune contradiction ne peut venir du genre » (seule k = 30, c'est-à-dire L22) [CX102:150] |
| programme linéaire thêta (M₂₂(Γ₀(7)), 7 paramètres, simplexe exact + Farkas) | r ≤ 27 impossible ; 29 et 31 demandent des vecteurs de Fano ; une norme 14 force r ≥ 33 ; 33 et 35 meurent par identités entières | C, audit IA [TL:8-74, 236-242, 633-655] | r ≤ 35 | les séries thêta de E₋ et de son dual sont modulaires (niveau 7) ; positivité des coefficients + bornes combinatoires sur les vecteurs courts (a₇ ≤ 990 via le lemme F, b₄ ≥ 2 729 034) | **à r = 37 le LP est faisable** avec a₇ = 0 et 22 vecteurs de norme 16 à 20 [TL:4074-4104] ; les rangs 39 à 43 « sont satisfaits par de petits nombres » [TL:397-400] |
| chemin critique | 2a₈ + 16a₉ + a₁₃ = 329(7^m + 1) + … (m = (45 − r)/2) | C [TL:358, 4229-4234] | — | toute exclusion par « mondes » passe par la norme 18 et une borne sur la norme 26 | norme 18 non tuée par la positivité (plus de 10¹³ nœuds par cœur), norme 20 sans borne de graine [TL:4209-4227] |
| mondes de vecteurs courts | N14 : pas de norme 14 au rang 37 (33 508 orbites) ; norme 16 : 3 mondes morts | C pour N14 (non audité par un pair) ; catalogue de la norme 16 incomplet | des sous-cas | énumération exhaustive des cœurs | normes 18, 20, 26 |
| réseaux de droite (NOTE_RESEAUX_DE_DROITE) | det Λ₋(T) = 4·7^(2k)τ/(9j²) ; Λ₋(T)⊗ℤ₇ ≅ U ⊥ 7U″ ; χ(det U″) = (−1)^(k+1)(τ\|7) | P, non relu [RD:19-34] | au rang 37 : (τ\|7) = −1 (L23 retrouvé) | invariants de Hasse en 7 | en 2, 3 et 11, les conditions sont toujours satisfaites ; Hermite ne donne pas de borne inférieure [RD:36-51] |
| L23 (Codex note 102) | rang 37 ⇒ (τ\|7) = −1 pour toute droite générique | P [CX102:52-75] | la moitié des droites génériques au rang 37 | le bloc de boule a le rang 37 − d et le discriminant ≡ τ ; il est extrémal donc non scindé | le signe n'agit que sur les blocs extrémaux (≤ 39 points) : au mieux k ≥ 24 [CX102:151-153] |
| mod 49 | — | — | rien | L19 : les congruences disparaissent pour k ≥ 2 ; formes de Smith imposées par les paramètres [CX93, CX102:119-121] | l'ordre 2 du rang 37 (Σ/7 mod 7) est dérivé, non audité, non implanté [TL:3604-3608] |
| attaque globale du 12/10 | — | O | rien | environ 3·10²² secondes lignes par base | SAT indécis à 240 s [TL:4128-4240] |

**Lecture.** La couche arithmétique est **globale par nature** : réseaux de vecteurs propres, séries thêta. Elle tue tous
les rangs ≤ 35, mais elle s'arrête net à 37. À ce rang, le genre et les formes modulaires sont compatibles, et seuls des
vecteurs de norme 18 ou 26 pourraient encore faire mourir le LP. C'est pourquoi tout le travail récent est descendu à
l'échelle d'une droite (couche II).

---

## 3. Couche II : la rigidité d'une droite (Green, résidu, couplage, projecteur réel)

### 3.1 L'identité clé (A, Codex 124-127)

    rang₇ M = (38 − d) + 2 r(T) + ρ(T)

- 38 − d est le rang du bloc proche M[N, N].
- r(T) est la torsion déséquilibrée et ρ(T) le rang du résidu lointain.

Pour une droite générique (c = 1, 7 ∤ τ), ρ = r − 37.

**Au rang 37, ρ = 0.** Le graphe lointain est alors entièrement déterminé mod 7 par le graphe proche :
R(w, w′) ≡ β(w, w′), une forme de Green.

C'est la raison profonde de tout ce qui suit : au rang minimal, la moitié lointaine du graphe n'a plus aucune liberté
arithmétique.

### 3.2 Pourquoi ça tue au rang 37 (E, NOTE_OBSTRUCTION §2)

- **Contraintes.** Sur l'étoile de x (10 lointains, 45 paires), le couplage λ = 1 épingle R sur chaque paire. Chaque paire
  impose alors une égalité mod 7 : il faut que la valeur de Green tombe sur une valeur précise, avec une probabilité de
  1/7.
- **Liberté.** Il y a environ 360 triplets candidats par lointain.
- **Bilan heuristique.** L'espérance vaut environ 360¹⁰ · 7⁻⁴⁵ · T, soit environ 3·10⁻⁹. Le seuil où l'espérance passe sous
  1 se situe entre 7 et 8 lointains, et les noyaux minimaux observés en ont exactement 7.
- **Pseudo-aléa.** Les valeurs de Green sont uniformes à 10⁻³ près, et les comptes exacts de 3-uplets et de 4-uplets
  suivent le modèle indépendant à 1 % près. **C'est un CSP aléatoire au-delà de son seuil.**

### 3.3 Pourquoi il faut les trois ingrédients ensemble (E)

| retiré | verdict de l'étoile |
|---|---|
| rien | meurt en environ 10³ nœuds |
| couplage λ = 1 (R libre dans {0, 1}, probabilité 2/7 par paire au lieu de 1/7) | non conclu à 60 s |
| valeurs de Green | **SAT en 128 nœuds** |
| projecteur réel | meurt quand même au rang 37 ; c'est lui qui tue au rang 39 (§3.5) |

### 3.4 Le projecteur réel : la contrainte qui ne dépend pas du rang (P)

- **Formule.** H = 3I − R − EᵀZE + J/9 = 7Π_T = (3I − R)·P_{ker E}.
- **Propriétés.**
  - Il est semi-défini positif, de valeurs propres {0, 7}.
  - Son rang vaut **7 + c** (NOTE_BOOST §2.3, calcul de traces).
  - H² = 7H est automatique dès que R vérifie les équations srg : c'est **la condition srg elle-même** vue sur le bloc
    lointain.
- **Force sur les configurations partielles.** Un bloc k × k de triplets aléatoires est semi-défini positif avec une
  probabilité de 0,67, 0,29, 0,08, 0,014, … pour k = 2, 3, 4, 5. Pour k = 10, on extrapole environ 10⁻¹¹.

### 3.5 Ce que ça donne rang par rang

Le résidu ajoute à chaque lointain un vecteur caché u ∈ F₇^ρ. La condition de l'étoile devient : « la matrice de Gram
10 × 10 (β + R) est de rang ≤ ρ sur F₇ ». La codimension de cette condition vaut (10 − ρ)(11 − ρ)/2.

| rang | ρ | codimension mod 7 | espérance mod 7 seul (heuristique) | avec le filtre réel | observé |
|---|---|---|---|---|---|
| 37 | 0 | 55 conditions (épinglées) | environ 3·10⁻⁹ | encore moins | **toutes les droites testées meurent** (E) |
| 39 | 2 | 36 | environ 0,1 à 1 | environ 10⁻¹¹ | **5 étoiles sur 5 meurent**, graines 1, 2, 3, 4, 6, dans les deux types de forme ; 1·10⁸ à 2,5·10⁸ nœuds, 40 min à 2 h ; le filtre réel coupe énormément (12,8·10⁹ coupes) et accélère d'un facteur d'environ 8. Sans lui, la graine 4 n'a aucune feuille sur les 4,5 % de l'arbre explorés en 15 min. Sa nécessité n'est pas établie |
| 41 | 4 | 21 | environ 10¹⁰ | environ 0,1 à 1 | à la limite ; recherche impossible (environ 10¹⁵ nœuds par droite, §8) |
| 43 | 6 | 10 | environ 10¹⁹ | environ 10⁸ | l'étoile survit ; il faut la double étoile, sur-déterminée mais impossible à parcourir |

### 3.6 Résultats exacts du jour (E, NOTE_BOOST)

- **Rang 37, droites c ≤ 3 de tous types**, torsions comprises, découpées en équilibré, déséquilibré et 8 directions : 122
  droites et plus de 280 runs, tous UNSAT, sans aucune feuille.
- **Rang 37, droites c = 1 tirées uniformément** : avec `line37`, le test complet en C++ validé ligne à ligne contre
  Python, **33 754 droites testées sur 100 000 tirages, toutes UNSAT**. À 95 % de confiance, la proportion de
  survivantes est inférieure à 9·10⁻⁵.
- **Coût mesuré** : 38 à 42 ms par droite testée, et environ 14 ms par graphe tiré.
- **Rang 39** : 5 droites sur 5 meurent, à 40 min à 2 h par droite. La graine 4 meurt aussi avec l'autre forme du
  résidu (δ = 1, hors règle), donc sans dépendre de la règle non relue.

### 3.7 Pourquoi il n'y a pas de lemme court

- La mort est celle d'un CSP pseudo-aléatoire. Aucun petit sous-ensemble de contraintes n'en est responsable de façon
  stable.
- Une preuve uniforme pour les environ 10¹¹ graphes de droite serait un théorème de pseudo-aléa des fonctions de Green mod
  7 des graphes cubiques de ce type. Personne ne sait faire cela.
- **Le seul moyen connu de rendre global ce mécanisme est l'énumération exhaustive.** Elle est finie au rang 37 (route B).

---

## 4. Couche III : les lois locales autour d'un sommet (étoiles de labels)

### 4.1 Les plafonds à quatre étoiles sont tous réfutés (R) [AUD15:21-39 ; NP:265-331]

- (A4), les plafonds de relations mixtes, (N9), (NOGRID) + (LOW) et (R7, version rang₇ ≥ 29) sont tous tombés devant
  des témoins exacts.
- **Pourquoi.** Chaque plafond avait été lu sur des marches issues de la famille symétrique G1. Les premières familles
  indépendantes (⟨h⟩, Z5h) l'ont cassé en quelques minutes.
- **Pourquoi c'était inévitable.** À quatre étoiles, positivité, rang 30 et rang₇ ≤ 28 sont **simultanément
  satisfaisables** [NP:242-246]. La positivité continue n'est jamais infaisable : le centre fractionnaire de Codex le
  montre [RG:350-352].

### 4.2 Les morts par arithmétique et par extension (P, C)

- **(SQ3), prouvé.** Classe carrée du déterminant des sous-graphes induits à 45 et 55 sommets
  [NP:332-349 ; EXT:10-17].
- **Les germes semi-définis positifs de rang 30** (645) meurent tous :
  - par DISC (classes 2·3·5 ou 2·3·5·7) ;
  - et par extension : chaque label extérieur a une colonne vide, car la norme de Schur 5/2 n'est jamais atteinte.
  - Le mécanisme de grille est prouvé [EXT:20-50].
- **(SQ30)** était un artefact de symétrie h [AUD15:214-230].
- **(N15)**, « pas de bloc semi-défini positif avec ν ≥ 15 », reste ouvert : environ 288 000 visites montent à ν = 14,
  aucune à 15.

### 4.3 La grappe (H-MATCH)

- **Pont prouvé.** (H-MATCH) ⇒ pas de Conway (P, relu par un agent adverse, modulo L8) [HMR:28-64]. G18 et G21 sont
  prouvés.
- **(H-MATCH) elle-même : ouverte.** La route locale a été déclarée épuisée :
  - environ 1,14 M de structures, sans aucune structure cassée de ν ≥ 14 ;
  - c'est le « mur 13 » : les meilleures structures cassées ont ν = 13 [HMN:73-82, 152-161].
- **Pourquoi les blocs cassés meurent.**
  - Type II : la torsion détruit deux relations h-homogènes, ce qui plafonne ν à 13.
  - Type I : il est tué par U seul, une mort spectrale globale sans certificat induit en dessous de 33 sommets
    [MA:46-51, 175-191].

### 4.4 Les lois de gain de rang et de transversalité

- **ODD9 : réfuté.** (B′) : ouvert, avec une preuve faible.
- **(N9-NG) + P ≤ 852 ⇒ pas de Conway** (P, vérifié par Codex). NG5 suffit ; NG7 : au moins 254 blocs non-grille avec
  t ≤ 7 [3R:92-130]. La loi elle-même est ouverte, sans écart uniforme (0,0071, puis 3,1·10⁻⁶).
- **(T8) ou (T15) + P ≤ 852 ⇒ pas de Conway.** Les deux sont ouverts et fragiles.
- **Bornes vérifiées exactement** : P ≤ 852 et 3P + 4G ≤ 2 772 [AUD18].

### 4.5 La cinquième étoile : la barrière propre à Conway [EXT:75-144 ; RG:141-151, 293-397]

- **Aucune base à quatre étoiles ne prend de cinquième étoile** (34 bases variées et 8 aléatoires).
  - CP-SAT, cryptominisat et cadical concluent tous à l'infaisabilité.
  - La base HB a une preuve DRAT vérifiée (1 576 lemmes).
  - Le lemme h5 est prouvé.
- **C'est propre à Conway.** Pour srg(243), K = 22, les bases aléatoires s'étendent 5 fois sur 5, en 17 à 90 s ; pour
  Conway, 0 fois sur 8.
- **Noyaux minimaux** : 30 ou 31 labels de base sur 44. Il n'y a pas de motif local.
- **Le seuil exact.**
  - R7 (quatre étoiles exactes + 7 labels {4,t}) est **SAT**.
  - Aucun témoin de R7 n'accepte le 8ᵉ label.
  - R8 (les 8 labels) est **indécis** :
    - TIMEOUT à 1 800 s, puis à 3 600 s avec cassage de symétrie (3 071 éléments du groupe, 11,9 M clauses) ;
    - découpage selon M₀ : TIMEOUT à 600 s ;
    - runs de 2 h avec cadical et kissat.
  - **R8 infaisable exclurait Conway, à tous les rangs.**
- **Comptages prouvés autour de R8** [RG:370-386] :
  - la capacité est exactement serrée (Σκ = 8) ;
  - le graphe Ω compte 36 arêtes sur 12 labels, soit 60 % des paires (38 % pour k = 22) ;
  - borne X-paires : n₁ + n₂ ≥ 8 + a, positive seulement pour k = 14.

### 4.6 Pourquoi les lois locales échouent

1. Elles sont lues sur des populations issues de peu de lignées et tombent à la première famille indépendante.
2. **Jusqu'à quatre étoiles, tout est simultanément satisfaisable** : on est sous le seuil de surdétermination.
3. L'étalonnage sur srg(243) était souvent vide. Les analogues y sont automatiques, ou le c spectral n'est pas le nombre de
   composantes [AUD15:317-327].
4. **La frontière est exactement entre R7, qui est SAT, et R8, qui est indécis.** C'est l'endroit où le comptage
   (capacité serrée, débordement 8 + a) devient positif pour k = 14 et seulement pour k = 14.

---

## 5. Couche IV : la symétrie

### 5.1 Exclusions acquises

- **C2** : réduction à 156 réseaux unimodulaires impairs de rang 24 (liste de Borcherds), avec E(v) ≥ 8 [FS-C2].
  - Le moteur tue toutes les paires.
  - Points faibles : l'énumération des paires n'est recoupée que sur 4 réseaux sur 156, et elle dépend d'un seul moteur.
  - La règle des jumeaux n'est pas recertifiée (2,48 M de paires dépendent d'un type en flottant).
- **C3** : Q² + Q = 12I + 6J sur ℤ et M² + M = 12I sur ℤ[ω] sont congrues mod 1 − ω. Les déterminants donnent
  d ≡ −1 (mod 3) contre d′ ≡ 1 (mod 3) (P + Lean). La relecture LAB a trouvé environ 15 trous, mais aucune étape fausse.

### 5.2 Pourquoi la symétrie aidait, et pourquoi C1 est tout le problème

- Un automorphisme réduit énormément l'entropie : il impose des points fixes et des orbites. Le système devient
  sur-déterminé à petite taille.
- Le cas asymétrique a l'entropie maximale.
- **Principe de symétrie forcée** (P) : pour Γ asymétrique, toute structure partielle H a au moins |Aut(H)|
  complétions.
  - Il ne devient global que si l'on dispose d'un problème hôte symétrique dont le nombre de solutions est prouvablement
    inférieur à son ordre de groupe.
  - Conway n'a pas d'hôte connu : pas de two-graph, pas de 3-ovoïde, pas de spread régulier, pas de switching GM pour
    k ≥ 14.
  - Le seul morceau symétrique forcé, le cadre de sommet, est à 30 dimensions de la rigidité [WIN:32-160].
- **On ne connaît aucun srg asymétrique avec λ = 1.** Le moins symétrique connu est un srg(378) avec |Aut| = 6. Cela
  s'explique (« la rareté force la symétrie ») mais ne se prouve pas.
- **Le cadre des cocliques** fermerait C1 seulement avec α ≥ 21, que personne ne sait prouver.

---

## 6. La route c : dichotomie par droites

- **m ≤ 4 : P**, par le certificat exact P ≤ 852.
- **m = 4 exclu : S.** Verdicts CP-SAT de Codex, sans certificat portable : 79 gabarits sur 79 à la racine de budget.
- **Registre m = 3** : 10 052 gabarits après le Gram.
  - 35 restaient ouverts au 19/10. P3 en couvre 7 : 125 sous-tranches sur 128 faites, 3 en cours.
  - Il en reste une vingtaine sans méthode.
  - 23 exclusions reposent sur un seul verdict de solveur.
- **m ≤ 2.**
  - (I) Une racine a ses sept droites à c ≥ 3. Le registre s'applique sans le budget : 14 gabarits ouverts de plus, et un
    audit est à faire.
  - (II) Tout sommet est sur une droite c ≤ 2, donc il y a au moins 33 telles droites. **Aucune méthode finie.**
  - Le recensement m = 2 compte environ 10⁷ gabarits à symétrie près.
- **Pourquoi les gabarits calent.** Ils oublient l'adjacence entre labels, le cadre lointain de chaque droite (rang 7 + c,
  dénominateurs du laplacien) et l'arithmétique des classes carrées [MAND:16-24].

---

## 7. La vue d'ensemble : pourquoi ça meurt, pourquoi parfois non, où est la frontière

### 7.1 Le seuil de surdétermination, unité par unité

| unité | taille | état | lecture |
|---|---|---|---|
| base à quatre étoiles | 44 labels | **SAT** | sous le seuil |
| R7 | 44 + 7 labels | **SAT** | sous le seuil |
| **R8** | 44 + 8 labels (1 326 arêtes) | **indécis** | **frontière, sans dépendance au rang** |
| cinquième étoile sur base | 56 labels | aucune base ne s'étend (S ; DRAT pour HB) | au-dessus |
| étoile d'une droite, rang 37 | 10 lointains | **meurt** (E, toutes les droites testées) | au-dessus |
| étoile, rang 39 | 10 lointains, ρ = 2 | **meurt** (E, 5/5), grâce au filtre réel | au-dessus, de justesse et cher |
| étoile, rangs 41-43 | ρ = 4, 6 | heuristiquement SAT | sous le seuil |
| double étoile | 20 lointains | heuristiquement sur-déterminée à tous les rangs | au-dessus, mais impossible à parcourir |
| droite complète | 60 lointains | meurt au rang 37 ; TIMEOUT au rang 39 | — |

### 7.2 Chaque famille seule est satisfaisable, l'intersection meurt

| mort observée | ingrédients nécessaires |
|---|---|
| étoile au rang 37 | Green (mod 7) × couplage λ = 1 (sans l'un ou l'autre, pas de conclusion) |
| étoile au rang 39 | résidu (mod 7) × couplage. La positivité réelle accélère d'un facteur d'environ 8 ; on ne sait pas encore si elle est nécessaire |
| germes de rang 30 | DISC (arithmétique) × extension (combinatoire) |
| cinquième étoile | C1/C2 (comptages λ, μ) × capacité serrée (comptage propre à k = 14) |

Prises une à une, chaque famille de contraintes est satisfaisable :
- l'arithmétique du genre (aucune contradiction possible) ;
- la positivité (centre fractionnaire) ;
- la combinatoire (SAT en 128 nœuds) ;
- les lois locales jusqu'à quatre étoiles.

### 7.3 Pourquoi parfois ça ne marche pas

1. **Trop local** : sous le seuil, des configurations existent vraiment.
2. **Trop peu d'information arithmétique** : aux rangs 41 et 43, les vecteurs résiduels absorbent les contraintes mod 7.
3. **Échantillons biaisés** : les lois lues sur une seule lignée sont réfutées par la suivante.
4. **Relaxations continues** : elles sont toujours faisables au niveau des paramètres. Le « LP de types » tue 60 à 93 %,
   jamais 100 %.
5. **Pas de motif** : les noyaux minimaux couvrent presque toute la configuration, et l'on n'en tire pas de lemme lisible.

### 7.4 Où est la frontière aujourd'hui

Il y en a deux.
- **R8**, autour d'un sommet, sans dépendance au rang.
- **L'étoile au rang 39**, sur une droite. Les rangs 41 et 43 sont encore au-delà.

---

## 8. Comment rendre le mécanisme global et exclure le graphe : les routes finies

### Route A : R8, une instance SAT pour tous les rangs

- **Énoncé.** Toute Conway porte autour de chaque sommet une configuration R8. Donc R8 UNSAT ⇒ pas de Conway (A, avec
  audit du modèle à refaire).
- **Pourquoi c'est la meilleure candidate.**
  - C'est **un seul** problème fini, de 1 326 variables d'arête.
  - Il ne dépend ni du rang ni de la symétrie.
  - Il est exactement à la frontière : R7 est SAT.
  - L'étalonnage existe : le cas k = 22 est SAT en moins de 90 s.
- **Ce qui manque.**
  1. Un audit du modèle (chaque contrainte nécessaire).
  2. Un encodage renforcé, uniquement par des lemmes prouvés : capacité serrée, graphe Ω, borne X-paires, cassage de
     symétrie.
  3. **Une estimation de Knuth de l'arbre**, jamais faite.
  4. Un cube-and-conquer avec preuves DRAT/LRAT.
- **Résultat de l'audit** (r8_route/NOTE_R8_ROUTE.md, agent, 20/10).
  - **Le modèle est sain** : chaque contrainte est prouvée nécessaire. Un encodeur et un vérificateur indépendants
    concordent avec la CNF de l'archive sur 4 610 affectations. « R8 UNSAT ⇒ pas de Conway » tient donc à tous les
    rangs.
  - Le contrôle positif sur srg(243,22,1,2) passe : 108 structures locales réelles acceptées, et l'analogue de R8
    est SAT en environ 6 s.
  - Deux lemmes de comptage prouvés et encodés accélèrent d'un facteur 10 ou plus.
  - **Coût de R8 seul : pas réaliste.** L'extrapolation (balayage par libération, arbres de lookahead) va de 5·10⁷
    à 10¹² heures-cœur, ou de 2·10⁴ à 4·10⁸ avec un cassage de symétrie idéal. L'incertitude couvre 8 ordres de
    grandeur.
  - La variante CEGAR (A′) est le meilleur pari, mais une seule itération a tourné : 5 coupes exactes sur la base à
    quatre étoiles.
  - **Recommandation : un pilote local CEGAR de 1 à 2 jours**, en tranches de 5 min :
    1. contrôle k = 22 ;
    2. convergence à quatre étoiles ;
    3. quatre étoiles + k labels {4,t}, pour k = 1 à 8 ;
    4. R8.
  - Le pipeline de preuve est décrit : deux encodeurs, LRAT vérifié par cake_lpr, coupes vérifiées en entiers.
  - Réserve : rang₇ ≤ 28 dépend de la fenêtre r ≤ 43 (audit IA seulement).
- **Variante A′ : un sommet, tous les rangs, avec contraintes réelles** (recommandation de NOTE_BORNE_RANG).
  - Les témoins SAT de R7 violent massivement des conditions vraies à tout rang. Sur leurs 51 labels, le bloc réel
    7P_v a le rang 47 au lieu de 30 au plus, 8 valeurs propres négatives, et un 7-rang de 47 au lieu de 28 au plus.
    Le modèle purement combinatoire est donc très faible.
  - L'instance finie naturelle est « R7/R8 + coupes de positivité + rang ≤ 30 + 7-rang ≤ 28 + DISC », par une boucle
    CEGAR : SAT, puis contrôle spectral, puis coupe.
  - Les 645 germes à quatre étoiles réellement cohérents de l'archive échouent tous à DISC, et aucun n'accepte un
    label extérieur. **Ce qui manque, c'est l'exhaustivité**, et c'est exactement ce que donne la boucle CEGAR.
- **Ordres de grandeur.** Les problèmes de ce type résolus en grand :
  - triplets de Pythagore : environ 35 000 heures-CPU ;
  - Keller en dimension 7 ;
  - nombre de Schur 5 : environ 14 années-CPU.

  Ils sont de l'échelle « cluster ».

### Route B : le rang 37 droite par droite, entièrement finie et chiffrée

- **Énoncé (THEOREME_REDUCTION_R37.md, Théorème 6.1, P relu par un agent adverse).** Supposons que tout graphe de
  droite admissible à t ≤ 7 triangles transversaux ait un sommet x hors triangle dont l'étoile est insatisfaisable
  dans toutes les variantes du rang 37. Alors aucun graphe n'a r = 37.
  - La seule entrée est P ≤ 852, d'où au moins 18 droites avec t ≤ 7. t ≤ 7 entraîne c ≤ 4.
  - Il n'utilise ni CP-SAT, ni le registre m = 3, ni L23, ni la règle sur δ.
- **Coût.**
  - Mesure aujourd'hui : environ 7 à 9·10⁵ heures-cœur pour environ 1,9·10¹¹ classes de c = 1, plus environ 7·10⁷ de
    c = 2 et environ 2·10⁵ de c = 3.
  - **Avec `line37_fast`** (10 fois plus rapide, résultats identiques) : environ 6,5·10⁴ heures-cœur pour c = 1,
    soit environ 3 jours sur 1 000 cœurs. Il reste à porter en C++ la préparation des droites à torsion (11,5 % des
    tirages).
- **Ce qui manque.**
  - L'énumération exacte des classes (agent : type cyclique de σ = s₂₀s₁₂s₀₁, couplages modulo un petit groupe, comptage
    de Burnside).
  - La certification des UNSAT, par réimplantation indépendante ou certificats.
  - Le cas des rangs 39 à 43.

### Les rangs 39 à 43 : ce qui pourrait les rendre finis (3 agents en cours)

1. **Un théorème r = 37 : hors de portée des outils actuels** (NOTE_BORNE_RANG.md, agent, 20/10).
   - Toutes les conséquences linéaires des équations srg ne bornent r que par en bas. Cela vaut sur une droite, un
     sommet, quatre étoiles, les réseaux de droite et le genre.
   - Une borne par en haut exige des vecteurs propres entiers −4 de Gram inversible mod 7, et rien de local ne les
     force.
   - Un modèle en position générale reproduit toutes les dimensions forcées à tous les rangs. Le comptage de
     dimensions ne peut donc exclure aucun rang : l'obstruction doit venir de la combinatoire 0/1.
   - L'heuristique de Cohen–Lenstra de Codex attend même r = 43.
   - Résultats prouvés au passage (P) :
     - dim C(T) = ρ(T) + r(T) pour les mots du code portés par le lointain ;
     - scindage orthogonal 7-adique Λ₋(T) ⊥ complément, à tout rang ;
     - dim D_v = r − 15 en chaque sommet.
2. **La globalité du type de résidu et les droites latérales : écartées** (NOTE_RESIDU_GLOBAL.md, agent, 20/10).
   - La règle de classe est prouvée de trois façons pour toute droite équilibrée, d'où une seule forme δ par droite.
   - Mais la classe n'est pas globale : elle vaut (τ(T)|7).
   - Théorème B (P) : sur tout ensemble U ⊇ N[T], tout le contenu mod 7 se réduit à « rang₇ M_UU ≤ r, avec la classe
     fixée en cas d'égalité ». Il ne dépend pas de la droite de base.
   - Conséquences : les droites latérales n'ajoutent rien, et le « filtre gratuit ÷ 2 » de NOTE_OBSTRUCTION §4.2 est
     vide.
   - **Aucune condition reliant les résidus de différentes droites ne peut exclure 39, 41 ou 43.** Il faut la
     structure 0/1 et la positivité.
   - Un test au rang 43 est une relaxation valable pour les quatre rangs.
3. **Des conditions 7-adiques d'ordre 2 locales.** H² = 7H donne déjà UᵀU ≡ 0 (mod 7), mais c'est global sur la droite.
   Une version restreinte à l'étoile ferait bouger les rangs 41 et 43 (NOTE_ORDRE2_7ADIQUE.md).
4. **Ce qui est hors de portée.**
   - Le test par droite au rang 39 : environ 1 h × 10¹¹ droites.
   - Au rang 41 : environ 10¹⁵ nœuds par droite, car les 5 premiers lointains n'ont aucune contrainte mod 7.

### Route C : la dichotomie c

- Certifier m = 4.
- Fermer les 35 + 14 gabarits m = 3 et auditer le budget.
- Pour la branche (II), il faudrait un comptage global (au moins 33 droites c ≤ 2), à confronter à P ≤ 852 et
  3P + 4G ≤ 2 772.

### Route D : les lois locales à pont prouvé

(N9-NG)/NG5, (T8)/(T15) et (H-MATCH) excluent Conway si la loi est vraie. Il faudrait :
- les tester seulement sur des blocs qui passent DISC et acceptent une colonne extérieure ;
- ou suivre la globalisation de Codex : un seul Γ sur 84 labels, et l'extension des vecteurs du noyau par zéro
  [HMN:96-100].

---

## 9. Plan ordonné

1. **R8** (route A) : audit, estimation de Knuth, encodage renforcé. Si le coût est d'environ 10⁵ heures-cœur ou moins,
   c'est le meilleur dossier à présenter à un centre de calcul : un problème fini, qui ne dépend pas du rang, avec
   certificat DRAT.
2. **Dossier du rang 37** (route B) :
   - le théorème de réduction rédigé ;
   - l'énumérateur exact ;
   - le moteur accéléré ;
   - un pilote complet sur un type cyclique ;
   - le coût final.
3. **Rangs 39 à 43** : borne de rang, résidus globaux, ordre 2 en 7. On cherche le théorème qui manque.
4. **Certificats** : m = 4, les 23 exclusions du registre c = 3 à verdict unique, et C2 au-delà de 4/156.

## 10. Sources

Chemins relatifs à `work/` :
- AUD15 = `stars_rank_2026-10-14/AUDIT_EXCLUSIONS_2026-10-15.md` ;
- NP = `stars_rank_2026-10-14/NOTE_PROOFS_1410.md` ;
- 3R = `stars_rank_2026-10-14/THREE_RESULTS_2026-10-15.md` ;
- HMR = `stars_rank_2026-10-14/H_MATCH_REDUCTION_2026-10-15.md` ;
- MA = `stars_rank_2026-10-14/MECHANISM_A_2026-10-15.md` ;
- HMN = `stars_rank_2026-10-14/HMATCH_NIGHT_2026-10-16.md` ;
- EXT = `stars_rank_2026-10-14/EXT84_2026-10-16.md` ;
- RG = `REVUE_GLOBALE_2026-10-16.md` ;
- AUD18 = `exploration_2026-10-16/audit_2026-10-18/AUDIT_EXCLUSIONS_2026-10-18.md` ;
- TL = `c1_theta_lp_2026-10-07/NOTE.md` ;
- RD = `c1_index_2026-10-09/NOTE_RESEAUX_DE_DROITE.md` ;
- MAND = `exploration_2026-10-16/representation_2026-10-19/NOTE_MANDAT_REPRESENTATION_2026-10-19.md` ;
- WIN = `asym_window_2026-10-14/NOTE_ASYM_WINDOW.md` ;
- FS-C2 = `FINAL_STATEMENT_C2_DRAFT_2026-10-07.md`.

Les notes de Codex, sur la branche `origin/codex/c1-arithmetic-audit` du clone `c1merge`, sont notées CX (numéro de
note : ligne).
