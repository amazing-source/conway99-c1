# line37_fast : le test d'étoile par droite (rang 37), même sémantique, environ 10 fois plus vite

LAB, 20/10/2026 après-midi.

**Statuts** (ceux de NOTE_BOOST) :
- **P** : argument écrit ici, non relu ;
- **E** : calcul exact sans certificat exporté (comparaison de sorties de programmes).

---

## 0. Réponse courte

- `line37_fast.cpp` / `line37_fast.exe` remplacent `line37.cpp` / `line37.exe` à l'identique :
  - même entrée, même ligne de commande, même format de sortie ;
  - même verdict, même x, même liste de candidats (même ordre, dd identiques au bit près) ;
  - **même nombre de nœuds** sur toutes les droites testées (E, §3).
- Aucun élagage nouveau : seul l'ordre d'évaluation de conditions déjà présentes change (P, §2).
- **Gain mesuré : 10,2 à 10,7 fois par droite testée** (36,34 ms contre 3,41 à 3,56 ms), mesure faite dos à dos sur le PC
  chargé (§4). La préparation passe de 2,28 à 0,15 ms, la recherche de 34,0 à 3,2-3,3 ms.
- Validation (E, §3) :
  - lines40 ;
  - rand 3000 (graine 20261020) ligne à ligne ;
  - rand 20000 (graine 20261021) ligne à ligne ;
  - au total 7 608 droites testées et 19 010 073 nœuds, **0 écart** ;
  - R et h identiques au bit près sur 1 677 608 paires tirées au hasard.
- **Limite de la validation : aucune feuille n'est jamais atteinte**, ni par line37 ni par line37_fast (0 sur les 7 608
  droites).
  - `leaf_ok` (avec Jacobi) n'est donc couvert que par l'argument : code recopié tel quel, nourri par les R et h testés
    ci-dessus.

## 1. Point de départ

- `line37.exe` se reconstruit exactement : `g++ -O3 -march=native -std=c++17 line37.cpp` (GCC 16.1, Ryzen 7 7800X3D, Zen 4)
  donne un désassemblage identique (seul l'en-tête PE diffère). Ce sont donc ses options.
  - Elles incluent la contraction FMA : `t -= L*y` devient `vfnmadd231sd`, et `s += y*y` devient `vfmadd231sd`.
- Profil instrumenté de line37 (une droite type) :
  - environ 1,8 million de candidats visités par le filtrage en avant, dont 12 % seulement atteignent `psd_ok` ;
  - l'arbre a 3 niveaux (profondeurs 0 à 2) et tous les fils de profondeur 3 meurent au filtrage ;
  - environ 2 700 des 3 070 candidats sont affectés quelque part.
  - Précalculer des tables de paires ne paierait donc pas. Il faut rendre chaque visite très peu chère.

## 2. Ce qui change, et pourquoi c'est équivalent (P)

1. **Domaines sans allocation.**
   - line37 alloue `vector<vector<int>> nd(NV)` à chaque nœud.
   - line37_fast tient, pour chaque profondeur et chaque lointain, une liste préallouée (identifiant, qi, si) dans l'ordre
     des vecteurs de line37.
   - La liste d'un fils est compressée depuis celle du père (AVX-512 VBMI2, ordre conservé).

2. **R(A, b) par tables, 64 candidats à la fois.**
   - Avec Y_A[z] = Σ_{u∈W_A} Ω[z][u] (même orientation que line37), on a
     s = Σ_{z∈W_b} Y_A[z] ≡ cst_A[w] + rq_A[qi_b] + rs_A[si_b] (mod 7), puis R = (4 − s) mod 7.
   - C'est un calcul en entiers exacts.
   - Pour chaque triple affecté A, on construit une fois par droite deux tables d'octets TQ[qi] et TS[si] et une table cst[w].
   - Les filtres bon marché de line37 s'évaluent alors par `vpermb` (AVX-512 VBMI) :
     - qi_b ≠ qi_A et si_b ≠ si_A (« used ») ;
     - |W ∩ W′| ≤ 2 ;
     - R ∈ {0, 1} ;
     - R = 1 ⇒ partage 1, cap_A = cap_b = 1 et NF ;
     - pas de R = 1 si A est plein ;
     - R(p, b) ≠ 1 pour les partenaires p de A ;
     - marges saturées.
   - Justifications :
     - **cap_b = 1** ⟺ b1 ∉ Q_b et b2 ∉ S_b, car x^1 ∉ W_b.
     - **NF, première moitié** (noms de b) : elle se lit par qi, par si et par lointain.
     - **NF, seconde moitié** (noms de A) : elle est testée directement, sur les seuls candidats R = 1.
     - **Marges** : le long d'un chemin, marg ne fait que croître, et une saturation ancienne a déjà vidé les domaines.
       Seuls les 4 noms de A peuvent donc devenir saturés. À la racine, marg = 0 et K(x, n) ≥ 1 pour tout nom de tout
       candidat.
     - **« Used »** : seuls qi_A et si_A sont nouveaux, et compat les exclut déjà.

3. **Ordre d'évaluation du filtrage en avant.**
   - line37 calcule nd[w] pour w = 0..9. Pour chaque candidat, il applique les filtres bon marché puis `psd_ok`. Il
     s'arrête au premier nd[w] vide.
   - line37_fast applique d'abord les filtres bon marché à tous les w, puis le filtre réel lointain par lointain (le plus
     petit d'abord). Il s'arrête au premier ensemble vide.
   - Pourquoi c'est équivalent :
     - les filtres forment une conjonction de prédicats sans effet de bord (`real_cuts` n'est jamais imprimé) ;
     - chaque ensemble conservé est donc le même ;
     - « mort » ⟺ un ensemble est vide, dans les deux programmes ;
     - un fils vivant reçoit les mêmes domaines complets.
   - Les fils, leur ordre et leurs domaines étant les mêmes, **les nœuds sont les mêmes**.

4. **psd_ok incrémental, au bit près.**
   - line37 recalcule pour b toute la descente y_i = (h_i − Σ_{j<i} Lc[i][j] y_j) / Lc[i][i], ainsi que les sommes s et s7.
   - y_i ne dépend que de b, des i + 1 premiers triples affectés et des lignes 0..i de Lc. Tout cela est inchangé sous le
     niveau i.
   - line37_fast mémorise y_i, y7_i, s et s7 au moment où le (i + 1)-ième triple est affecté, et ne calcule que la nouvelle
     entrée : mêmes opérations, dans le même ordre, donc mêmes doubles.
     - Les opérations sont `t = h ; t −= L·y` (fnmadd), `y = t / L`, `s += y·y` (fma), puis les tests
       `d − s < −1e−9` et `(7 − d) − s7 < −1e−9`.
     - h est obtenu par les mêmes 6 additions dans le même ordre. Les deux premières sont faites une fois par (A, w), avec
       le même arrondi.
     - Quand degenAt ≥ 0, rien n'est calculé ni lu, comme dans line37 où `psd_ok` rend vrai.
   - `chol_push`, `leaf_ok` et `jacobi_eig` sont recopiés tels quels et reçoivent les mêmes R et h.
   - Les options de compilation sont les mêmes. Le désassemblage de line37_fast.exe montre la même suite
     `vfnmadd231sd` / `vdivsd` / `vfmadd231sd` que line37.exe dans psd et dans chol.

5. **Préparation.**
   - Le choix de x, les filtres, l'ordre des candidats (y, qi, si croissants) et le calcul de dd (mêmes 36 additions dans le
     même ordre) ne changent pas.
   - **L2** est testé pour tous les si d'un couple (y, qi) à la fois :
     - un sommet extérieur avec 3 voisins dans W a son jumeau dans W, donc seuls les 6 jumeaux de W sont à tester ;
     - chaque condition qui échoue interdit les paires S contenant un sommet donné, ou toutes les paires ;
     - détail dans `prep_star`.
   - **g(W, W) mod 7** est décomposé par blocs, en entiers exacts.
   - Y, nbc et zq ne sont plus stockés par candidat. zq n'est calculé que pour les triples affectés, avec les mêmes 6
     additions.

6. **Supprimé, car sans effet au rang 37.**
   - Le test de symétrie O(D) (`!anynz && cd.nz && !cd.canon`) : u = 0 pour tout candidat, il ne se déclenche jamais.
   - REAL = RANK = vrai : le `main` de line37 ne lit aucune variable d'environnement.

7. **Différences hors calcul.**
   - Si le fichier d'entrée manque : message et code 1 (line37 plante sur un FILE* nul).
   - Deux modes de validation ajoutés : `filev` et `randv`, qui ajoutent un hachage des candidats.
   - Tout argument en trop est ignoré. On peut donc ajouter une étiquette `scratchpad/boost/runs` pour le watchdog.

## 3. Validation (E)

Comparaison des champs status, x, candidates et nodes, droite par droite. La référence est le `line37.exe` officiel.

| test | droites | testées | écarts | nœuds (réf. = rapide) |
|---|---:|---:|---:|---:|
| lines40 (gen/lines40.txt) | 40 | 40 | 0 | 93 390 |
| lines40, voie scalaire `-DL37_SCALAR` | 40 | 40 | 0 | 93 390 |
| rand 3000, graine 20261020 (mêmes tirages en mode file) | 3 000 | 932 | 0 | 2 360 821 |
| rand 20000, graine 20261021 (2 × 10 000 en mode file) | 20 000 | 6 636 | 0 | 16 555 862 |

- **Mêmes candidats au bit près.**
  - Une copie instrumentée de line37.cpp (`line37_refv_patch.py`, qui ajoute seulement une sortie) imprime un hachage de la
    liste (var, qi, si, bits de dd).
  - Il est identique pour les 932 droites testées de rand 3000, en voie AVX-512 comme en voie scalaire.
  - La copie instrumentée redonne exactement les sorties de line37.exe.
- **R et h au bit près.**
  - Après chaque droite testée de rand 3000, les deux programmes calculent R et h sur les mêmes 1 677 608 paires tirées au
    hasard (`pairv_patch.py`).
  - Les paires sont prises dans toute orientation, compatibles ou non ; 478 686 d'entre elles ont R ∈ {0, 1}.
  - 0 écart, bits de h compris. Ce test couvre aussi les valeurs dont se sert `leaf_ok`.
- **L2 décomposé.**
  - Le build `-DL37_CHECK_PREP` compare, sur chaque triple, trois tests : le test décomposé, le test direct par popcount et
    le test de line37 lui-même.
  - Ils sont d'accord sur 251 066 000 triples (30 959 000 sur rand 3000, 220 107 000 sur rand 20000).
- **Comptes du mode rand :**

| | K<0 | disconnected | 7-torsion | L23 | UNSAT | SAT | TIMEOUT |
|---|---:|---:|---:|---:|---:|---:|---:|
| line37.exe rand 3000 20261020 60 | 640 | 2 | 362 | 1 064 | 932 | 0 | 0 |
| line37_fast rand 3000 20261020 60 | 640 | 2 | 362 | 1 064 | 932 | 0 | 0 |
| line37.exe, 20 000 tirages de la graine 20261021 (somme ligne à ligne) | 4 256 | 6 | 2 316 | 6 786 | 6 636 | 0 | 0 |
| line37_fast rand 20000 20261021 120 | 4 256 | 6 | 2 316 | 6 786 | 6 636 | 0 | 0 |

- nodes_max vaut 6 484 sur rand 3000, des deux côtés.
- **Couverture des chemins rares** (copie à compteurs `coverage_patch.py`, sur les 23 040 droites) :

| chemin | occurrences |
|---|---:|
| commits avec partenaires | 2 265 785 |
| candidats R = 1 conservés | 191 726 851 |
| rejets par la seconde moitié de NF | 53 389 518 |
| exclusions par un partenaire | 132 836 |
| blocs dégénérés (degenAt) | 10 |
| racines sans mode b1 | 0 |
| feuilles | 0 |
| TIMEOUT | 0 |

  - Pour une racine sans mode b1, le branchement sur le plus petit domaine est le même code qu'aux nœuds profonds, où il
    sert sans cesse.

## 4. Vitesse (E)

Mesure dos à dos, 16 h 04-16 h 05. Le PC est chargé (environ 11 fils sur 16 occupés) et les deux programmes tournent en
priorité IDLE. Commande : rand 3000 20261020 60.

| | ms par droite testée | médiane | prépa | recherche | durée totale |
|---|---:|---:|---:|---:|---:|
| line37.exe | 36,34 | 34,96 | 2,28 | 33,99 | 33,9 s |
| line37_fast (avant / après la référence) | 3,56 / 3,41 | 3,41 / 3,20 | 0,155 / 0,151 | 3,33 / 3,19 | 3,31 / 3,18 s |
| facteur | 10,2-10,7 | 10,2-10,9 | 14,7-15,1 | 10,2-10,6 | 10,2-10,7 |

- Sur des mesures non simultanées (lancées à quelques minutes d'écart, charge variable), le facteur va de 8,3 à 10,7 :
  - 8,3 sur les 20 000 tirages en mode file (36,59 contre 4,39 ms) ;
  - 10,7 sur rand 3000 (38,29 contre 3,59 ms).
- La voie scalaire, sans AVX-512, donne 11,65 ms sur lines40 (référence : 30,22 ms), soit environ 2,6 fois.
- **Répartition de la recherche rapide** (profil rdtsc sur les 932 droites) :

| poste | part |
|---|---:|
| filtre réel (environ 177 000 appels par droite, environ 10 ns chacun) | 47 % |
| filtres bon marché (environ 58 000 lots de 64) | 29 % |
| branchement et commit | 10 % |
| compression des listes | 6 % |
| tables par triple | 5 % |
| chol | 3 % |

- **Pistes testées et écartées** :
  - remplacer les divisions du filtre réel ne change rien de mesurable : ce n'est pas le goulot ;
  - une variante qui applique tous les filtres bon marché sans arrêt précoce et spécialise psd par profondeur est plus
    lente de 2 à 3 % ;
  - un psd vectorisé passerait par des gathers : 0,37 ns par élément, contre 0,17 à 0,21 ns pour des chargements
    scalaires. Le gain espéré est d'environ 20 %. Non fait.

## 5. Portabilité et usage

- Sans AVX-512 VBMI et VBMI2, ou avec `-DL37_SCALAR`, le programme compile une voie scalaire de même logique (validée
  ci-dessus).
- L'identité au bit près vaut pour des binaires compilés avec les mêmes options par le même compilateur, sur la même
  machine que la référence. Sur une autre machine, il faut recompiler line37 et line37_fast avec les mêmes options et
  refaire la comparaison (outils au §6).
- Mémoire : quelques Mo.
- Usage identique à line37 :
  - `line37_fast file <lines.txt> [limit]` ;
  - `line37_fast rand <count> <seed> [limit]`.

## 6. Fichiers

**Dans `merge_2026-10-19/`** :
- `line37_fast.cpp` et `line37_fast.exe` (g++ 16.1 -O3 -march=native -std=c++17 ; même code que le binaire de toutes les
  mesures ci-dessus) ;
- `line37_fast_validation/`, qui contient :
  - `gen_lines.cpp` : écrit les tirages du mode rand (même mt19937_64 et même std::shuffle) ;
  - `line37_refv_patch.py` : copie de line37.cpp avec hachage des candidats ;
  - `pairv_patch.py` : test de R et h sur paires tirées, pour les deux programmes ;
  - `coverage_patch.py` : compteurs de couverture ;
  - `cmp_line37.py` : comparaison ligne à ligne ;
  - `validation_summary.json` : tous les comptes et résumés ci-dessus.

**Journaux complets** : scratchpad `boost/runs/fast/`.
