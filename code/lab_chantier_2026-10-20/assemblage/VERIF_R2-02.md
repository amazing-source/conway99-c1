# VERIF R2-02 — sous-cas de la note 225 : « chaque triangle dans ≥ q grilles »

Vérificateur adverse, contexte neuf, 20/10/2026. Lecture seule. Script : `check_misc.py` (scratchpad de la session),
arithmétique exacte.

## Verdict : DÉJÀ CONNUE (en substance) ; les définitions et l'arithmétique tiennent

- **Le sous-cas q = 4 est vide.** C'était écrit le 15/10, dans les mêmes termes (P ≥ 924 > 852 et ρ ≥ 154 > 126).
- **Le sous-cas q = 3 donne G ≥ 121.** C'était écrit le 14/10.
- **Le sous-cas q = 2 a les mêmes chiffres que la branche c ≥ 4** du 18/10.
- **Ce qui est nouveau :**
  - la fenêtre en P du sous-cas q = 3, soit P ∈ [726, 762], qui découle en une ligne de faits du 18/10 ;
  - le lien explicite avec les 2 et 11 types du catalogue de la note 225.
- **Ce n'est pas une exclusion.** Les hypothèses « g(T) ≥ q pour tout T » sont des sous-cas globaux, pas des faits.

## 1. Définitions (contrôle demandé)

- **G** : nombre de grilles 3×3 induites. C'est écrit explicitement dans
  `origin/codex/coheawood-hoffman-20261012:notes/RACINE_PONDEREE_2026_10_18.txt:5-7` : « P designe le nombre de prismes
  triangulaires induits et G le nombre de grilles3x3 induites [...] 3P+4G <=2772 ».
- **ρ (note 182)** : `origin/codex/c1-arithmetic-audit:notes/182_CODEX_RECENSEMENTS_HUIT_NEUF_SOMMETS.md`.
  - l. 5 : « P≤852 et ρ≤126 [...] resserre les bornes sur les prismes et les grilles ».
  - l. 148-149 : « Le code du graphe grille est 13262907120. Son majorant 126 possède également un certificat rationnel
    exact ».
  - l. 169 : le coin « P=1386, ρ=231 ». C'est le cas où toute paire de droites engendre une grille : 99·21/9 = 231.
  - **Décodage du code 13262907120** (bits de poids faible d'abord, sur les C(9,2) = 36 paires) : un graphe 4-régulier
    à 9 sommets, 18 arêtes et 6 triangles. C'est la grille K₃□K₃.
  - **Donc ρ = G.**
- **Grille induite.** Une grille de graphe est automatiquement induite : e(S) ≤ 18 pour |S| = 9, avec égalité si et
  seulement si S est une grille (NOTE_NIGHT 17.1, `work/c1_night_2026-10-14/NOTE_NIGHT.md:261-266`).
- **Faux amis à ne pas confondre avec G :**
  - « ρ(R) < 10 » de PRISM-SPECTRAL (L05-127) est un rayon spectral ;
  - « rho = k1 − b » de V13 §66 est un vecteur ;
  - « ρ ≤ 191 » (14/10) est une borne sur G, plus faible.
- **g(T)** : nombre de grilles contenant la droite T. C'est exactement le nombre de composantes à 6 sommets de G(T)
  (note 225:86). C'est bien la quantité de l'hypothèse « chaque triangle appartient à au moins q grilles » (225:124-134).
- **g(x)** : nombre de grilles passant par le sommet x.

## 2. Doubles comptages (vérifiés)

- **Comptages de base.**
  - Σ_T g(T) = 6G, car une grille contient 6 droites.
  - Σ_x g(x) = 9G (RACINE_PONDEREE:36).
  - Σ_{ℓ∋x} g(ℓ) = 2g(x), car une grille passant par x contient exactement 2 des 7 droites par x : sa ligne et sa
    colonne.
  - Ce dernier comptage est exact. Il n'a pas besoin du fait qu'une paire de droites soit dans au plus une grille, que
    R2 voulait vérifier. Ce fait est d'ailleurs vrai : le quatrième coin est l'unique second voisin commun, par μ = 2.
- **Sous l'hypothèse g(T) ≥ q pour tout T :**
  - g(x) ≥ ⌈7q/2⌉ ;
  - G ≥ ⌈99·⌈7q/2⌉/9⌉ = 11·⌈7q/2⌉.
- **Prismes.**
  - t(T) ≥ 2g(T) : chaque grille passant par T donne 2 prismes sur T, et deux grilles distinctes donnent des prismes
    distincts. Comme Σ_T t(T) = 2P, on obtient P ≥ 231·q.
  - P ≥ 6G : une grille contient 6 prismes, et un prisme est dans au plus une grille, par λ = 1
    (RACINE_PONDEREE:60-62 ; déjà dans 100_SYNTHESE C4, l. 201).
- **Majorations** (C relativement au recensement d'ordre 9, lui-même E en double implantation) :
  - G ≤ 126 (note 182) ;
  - 3P + 4G ≤ 2772 (RACINE_PONDEREE:7) ;
  - P ≤ 852.
  - Remarque : 3P + 4G ≤ 2772 et P ≥ 6G donnent déjà 22G ≤ 2772, donc G ≤ 126 (RACINE_PONDEREE:62).

## 3. Arithmétique refaite

| q | g(x) ≥ | G ≥ (par les sommets) | G ≥ (par les droites seules) | P ≥ max(231q, 6G) | P ≤ (2772 − 4G)/3 | état |
|---|---|---|---|---|---|---|
| 1 | 4 | 44 | 39 | 264 | 865 (852 par P ≤ 852) | ouvert |
| 2 | 7 | 77 | 77 | 462 | 821 | ouvert ; mêmes chiffres que c ≥ 4 |
| 3 | 11 | **121** | 116 | **726** | **762** | fenêtre G ∈ [121, 126], P ∈ [726, 762] |
| 4 | 14 | 154 > 126 | 154 | 924 > 852 | 718 < 924 | **vide**, par trois contradictions indépendantes |
| 5 | 18 | 198 | 193 | 1188 | 660 | vide (déjà vide dans le catalogue de 225) |

- **Sous-cas q = 3.**
  - Les couples entiers (G, P) avec 121 ≤ G ≤ 126 et 6G ≤ P ≤ ⌊(2772 − 4G)/3⌋ sont au nombre de 114.
  - P varie entre 726 et 762.
  - À G = 126, on a exactement **P = 756**. Les chiffres de R2 sont exacts.
- **Plus simple encore pour q ≥ 4.** La moyenne des g(T) vaut 6G/231 ≤ 36/11 ≈ 3,27. Une droite au moins est donc dans
  au plus 3 grilles.
  - Tout candidat a donc une droite dans ≤ 3 grilles. C'est plus fort que le « ≤ 4 » de la note 225:137-138.
- **Lecture correcte des « types sans objet ».**
  - Les types `bits=0` et `bits=1` (note 225:142-145) sont sans objet **comme cibles du sous-cas q = 4**.
  - Ils restent parmi les 174 types en général : aucune exclusion de type n'en découle.

## 4. Chaîne réécrite

1. **(P)** Doubles comptages du §2, valables dans tout srg(99,14,1,2).
2. **(C/recensement)** G ≤ 126, 3P + 4G ≤ 2772 et P ≤ 852.
3. **Conséquences sous l'hypothèse globale « g(T) ≥ q pour tout T » (statut C) :**
   - q ≥ 4 est impossible ;
   - q = 3 impose G ∈ [121, 126] et P ∈ [726, 762] ;
   - q = 2 impose G ≥ 77 et P ≤ 821.

## 5. Redécouverte

- **q = 4.** `work/stars_rank_2026-10-14/THREE_RESULTS_2026-10-15.md:97-103` (15/10) : « g(l) >= 4 [...] so t(l) >= 8
  for every line: P = sum t / 2 >= 924 > 852 (and rho = sum g / 6 >= 154 > 126) ».
- **q = 3.** `work/stars_rank_2026-10-14/NOTE_PROOFS_1410.md:216-218` (14/10) : « a stronger form ('at least three grids
  per line') would give at least 11 grids per vertex by parity [...] hence rho >= 121: not yet a contradiction ».
- **q = 2.** RACINE_PONDEREE:59 (18/10) : « Sous c>=4, somme g>=99*7 donne G>=77 et le certificat donne P<=821 ».
- **Recherche faite :** « 121 », « [121, 126] », « 726 », « 762 » et « g(x) ≥ 11 » dans `work/`. Hors des fichiers R2,
  le seul résultat est NOTE_PROOFS_1410. La fenêtre en P n'apparaît nulle part.

## 6. Ce qui manquerait

- **Pour fermer le sous-cas q = 3**, il faudrait l'une des trois choses :
  - G ≤ 120 ;
  - P ≥ 763 ;
  - un argument local contre les 11 types de la note 225 compatibles avec q = 3.
  Rien de tel n'est connu.
- **Même fermé, ce sous-cas n'exclurait pas le graphe.** L'hypothèse « toute droite dans ≥ 3 grilles » n'est pas forcée.
- **Statut.** Il reste celui du recensement d'ordre 9 : C relativement au recensement, recensement E. Pour passer à P,
  il faudrait dériver à la main les identités de G ≤ 126 et de 3P + 4G ≤ 2772 (CARTE §8.1).
