# 136 — L'échelle des pivots : le cas involution ramené à des systèmes locaux par type de bloc

*27/09, nuit. C1, avec C2 (décompte des 42 pivots en « tout un bloc ») et « structures » (système local, SAT). DÉRIVÉ = preuve
écrite ; les listes sont des calculs exacts. Les conclusions sont CONDITIONNELLES aux verdicts SAT (campagne cloud en cours).*

**Relu et VÉRIFIÉ par « structures »** : formule, parité, impossibilité de 10 pivots, « arête π ⟺ paire frère » dans les deux
sens. **Recompte indépendant** (involution/recount_pivots.py) : 0 : 1787, 2 : 958, 4 : 407, 6 : 106, 8 : 39, 12 : 11 ; pertinentes
pour Σ = ∅ : 2 : 759, 4 : 278, 6 : 56, 8 : 19, 12 : 4, soit 79 à ≥ 6. Identique aux listes de C1. Énoncé et preuve modulo les 79 :
notes/45 du labo de C2. Indice : 3 des 9 types (2,4) pertinents, chaque ι trouvé meurt en étape 2 (2 au PL, 1 en PLNE).

## 0. Énoncés
| énoncé | statut |
|---|---|
| Pivots en c ⟺ arêtes communes de τ_c (compagnons) et η_c (holonomie) | DÉRIVÉ |
| Arête commune qui est une arête π (τ(x+) = η(x+) = x−) ⟺ paire frère {c, x} | DÉRIVÉ |
| Nombre de pivots en un bloc = 2 × #arêtes communes, donc pair ; 10 pivots impossible | DÉRIVÉ + recensement |
| **Total des pivots = 42 + 2\|Σ\| − 2n_dis** | DÉRIVÉ |
| Système local UNSAT sur les 156 types à ≥ 6 pivots ⟹ **n_dis ≥ \|Σ\| + 7** dans toute configuration | conditionnel |
| En particulier : famille Σ = ∅ « tout un bloc » morte si les **79** types pertinents sont UNSAT | conditionnel |
| UNSAT aussi sur les 407 types à 4 pivots ⟹ n_dis ≥ \|Σ\| + 14 ; sur les 958 à 2 pivots ⟹ seul « tout dis » survit | conditionnel |

## 1. Pivots et types de bloc
- Une orbite o_l de l'étoile de c (étiquette l) a son partenaire D dans l'étoile de c ssi τ(l) = η(l).
  - Le partenaire D est N(u) ∩ N(σu) avec u = (c+, l).
  - Le compagnon (c+, τl) est voisin de σu = (c−, σl) ssi ητl = l, c'est-à-dire τl = ηl.
  - On appelle **pivot en c** une telle étiquette.
- Si τ(l) = η(l) = σl (arête π), le partenaire D de o_l est sa sœur : {c, bloc de l} est une **paire frère**. Sinon, c'est un
  carré « un bloc » pivotant en c.
- Les pivots en c sont les sommets des arêtes communes des couplages τ et η. **Leur nombre est pair.**
  - 10 pivots est impossible : les deux étiquettes restantes seraient appariées à la fois par τ et par η.
  - Donc #pivots ∈ {0, 2, 4, 6, 8, 12}.
- **Profil en c** (notation de C2) : par bloc x, le nombre de pivots vaut 2 (paire ancrée en c, ou frère), 1 (paire tordue) ou
  0 (ancrée en x), soit (|anch|, |tw|).

## 2. Le décompte global
- Chaque orbite contribue au nombre de pivots selon son carré D :
  - frère : 2 (une fois en chacun de ses deux blocs) ;
  - un bloc : 1 (en son pivot) ;
  - dis : 0.
- Avec 2|Σ| orbites frères et 2n_dis orbites dis sur 42 : **Σ_c #pivots(c) = 42 + 2|Σ| − 2n_dis.**
- Moyenne sur les 7 blocs : si 42 + 2|Σ| − 2n_dis > 28, elle dépasse 4, et par parité **un bloc au moins a ≥ 6 pivots**.
  - Seuils analogues : > 14 ⟹ un bloc ≥ 4 ; > 0 ⟹ un bloc non libre.

## 3. Couverture (le point à relire)
Soit un bloc c de profil donné dans une configuration (Γ, σ). Sa structure locale (τ_c, η_c) est :
- un couple d'involutions sans point fixe ;
- valide (K2, K3 ≥ 0, qui sont des comptes) ;
- dont le motif de pivots par bloc est une permutation du profil.
`classes_t_ge` énumère tous ces couples à B₆ près (recompte direct contrôlé), et B₆ préserve le motif à permutation près. Le
système local (i)–(iii) + L1/S1/S2 est nécessaire en tout bloc et B₆-invariant. La nécessité repose sur la dérivation de K2 et
K3, refaite à la main deux fois (C1 et « structures », c'est bien τπ). Le contrôle BvLS n'est que partiel : il est dégénéré,
avec μ = τ = π en tout bloc, donc tous les blocs frères et P_τπ = P_τμ = P_μτ = I. Donc :
**si tous les types d'un profil sont UNSAT, aucun bloc de ce profil n'existe, quelle que soit la structure D.**

## 4. Les listes (`data/`, `code/pivot_types.py`)
- 1 521 classes à pivots :
  - 156 à ≥ 6 pivots (`all_ge6.json`) ;
  - 407 à 4 pivots ;
  - 958 à 2 pivots.
- **Σ = ∅** (pas d'arête π parmi les pivots) : **79 classes à ≥ 6 pivots** (`allonblock_ge6_rel.json`).
  - (2,2) 24, (1,4) 18, (2,4) 9, (3,0) 7, (0,6) 7, (3,2) 6, (4,0) 4, (6,0) 4.
  - Les 4 dernières sont les blocs pleins de fb/sat.
- Grands T de C2 : 1 030 des 1 104 orientations ont un bloc (2,4), 13 un bloc plein, et les 61 autres un bloc à 6 pivots.
- Campagne cloud (c2-compute, tâche « tier ») : `code/sat_local_batch.py`, soit sat_local plus lex-leader sous Stab_B₆(μ, τ).
  CaDiCaL, puis DRAT et drat-trim sur les UNSAT. Un SAT serait la première solution locale complète à m = 7, et serait testé
  aussitôt au q:7 (`code/q7_far_from_satsol.py`).

## 5. Ce qui reste si l'échelle passe
- Configurations à n_dis ≥ |Σ| + 7 : familles dis lourdes, et à l'extrême « tout dis » (n_dis = 21, 7 étoiles libres).
- Là, le système local est probablement satisfiable (« structures » : l'étape 2 est PL-faisable aux ÉTL), et c'est le q:7 qui
  prend le relais :
  - det Q_c carré ⟹ K anisotrope, lignes rigides ;
  - côté pair, boule scindée ⟹ résidu pair anisotrope à g⁺ = 20 (notes/135 §4) ;
  - test lointain complet sur toute solution locale trouvée.
