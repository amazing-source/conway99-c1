# 167 — Mécanismes de construction, de rigidité et de brisure de symétrie dans la famille λ = 1, μ = 2 (11/10)

*But (demande de Dilan) : comprendre les mécanismes, séparer ce qui est **nécessaire** de ce qui vient seulement du
**procédé de construction**, et dégager un mécanisme **transférable** entre 243 et 99. Ce n'est pas un nouveau sous-cas
SAT. Code : `code/asym243/`. Suite des notes 165 et 166.*

## 1. Le cadre commun : revêtements à fibres
Soit Γ un srg(v,k,1,2) muni d'une partition équitable en cellules isomorphes F. On suppose que deux cellules
adjacentes sont reliées par un couplage parfait. Alors Γ est un revêtement de son quotient Q, avec des « voltages »
σ_AB ∈ Bij(A, B).

**Principe de monodromie** (démontré, élémentaire). Le groupe des automorphismes qui préservent chaque cellule et
commutent à la structure est le centralisateur C(Mon) du groupe de monodromie Mon ⊆ Sym(F). De plus, Aut(Γ)_Π /
C(Mon) s'injecte dans le stabilisateur, dans Aut(Q), de la classe de voltage. On a donc

  |Aut(Γ)_Π| = |C(Mon)| · |Stab_{Aut Q}([σ])|.

La symétrie *imposée par une construction de type revêtement* est C(Mon). Une monodromie abélienne et transitive
impose C(Mon) = Mon, c'est-à-dire une symétrie résiduelle obligatoire.

Deux types de fibres apparaissent dans la famille :

| fibre | quotient (243) | quotient (99) | monodromie observée | plancher |
|---|---|---|---|---|
| ligne (3 points) | BH = srg(81,20,1,6) | **impossible** (note 165, lemme 1) | toujours Z₃ | Z₃, sauf S₃ (ouvert, note 165 §6) |
| grille 3×3 (9 points) | K_{9,9,9} | **K₁₁** (seule forme, note 166) | de Z₃² (BvLS) jusqu'à **S₉** (Γ₃) | **aucun** : deck = 1 réalisé par Γ₃ |

**Conséquence.** Le « plancher Z₃ » de la note 165 est un **artefact de la fibre-ligne**. La même géométrie, lue avec
des fibres-grilles, n'a plus de symétrie de revêtement obligatoire : Γ₃ admet 4 partitions en grilles avec Mon = S₉
(ou A₉) et deck = 1 (`gridcover_anatomy.py`). Toute sa symétrie (864) vient alors du **quotient**.

## 2. La loi locale de recollement (identique à 99 et à 243)
Soient A, B deux grilles adjacentes et σ = σ_AB. Pour chaque grille C adjacente aux deux, on pose
ρ_C = σ⁻¹ σ_BC⁻¹ σ_AC ∈ Sym(A). En écrivant λ = 1 pour les arêtes x–σ(x) et μ = 2 pour les paires x ∈ A, y ∈ B non
adjacentes, on obtient l'équivalence exacte

  **Σ_C P(ρ_C) = 2J − I − Adj(A) − Adj(σ*B)**   (9 termes),

où σ*B est la structure de grille de B transportée sur A.

- **Nombre de termes.** Il y a exactement **9** grilles tierces à 243 (la troisième partie de K_{9,9,9}) comme à 99
  (K₁₁ moins A et B). La loi locale est donc la même pour les deux paramètres.
- **Ce qu'ajoute 243.** Pour deux grilles de la même partie (non adjacentes), Σ_{18 termes} = 2J. Cette loi n'existe
  pas à 99.
- **Points fixes.** Le nombre de points fixes de ρ_C est le nombre de droites transverses au-dessus du triangle
  (A, B, C).
- **Vérification.** La loi est vérifiée sur toutes les paires de grilles adjacentes de toutes les partitions des
  4 graphes (`twist_types.py`).
- **Parenté.** C'est la même algèbre (« 2J − I − permutations ») que l'étage colonnes de la route Ω pour C1 (note 163).

## 3. Lois observées (nécessaires ou artefacts ?)
Données : 99 partitions en grilles (BvLS 55, jumeau 10, Γ₃ 15, Γ₄ 19).

1. **Loi des motifs.** Pour toute paire de grilles adjacentes, les 9 droites transverses se répartissent soit en
   **un bloc de 9** au-dessus d'une seule troisième grille, soit en **3 + 3 + 3** au-dessus de trois grilles. Aucune
   exception (`skeleton.py`). L'ensemble de clôture (les points de A qui se referment) est soit A entier, soit une
   **diagonale** (3 points indépendants), soit un **chemin coudé** (3 points, 2 arêtes), jamais une droite
   (`closure_check.py`).
   - *Statut* : observé partout, non démontré.
   - *Conséquence à 99 si la loi est nécessaire* : les triangles « pleins » forment un système partiel de triples
     sur 11 points, et toute paire non couverte l'est par exactement trois triangles « à 3 droites ». Comme STS(11)
     n'existe pas, des triangles à 3 droites sont **obligatoires**.
2. **Types de vrillage.** Ce sont les positions relatives de la grille A et de σ*B. Seuls **5 types** apparaissent :
   - aligné : 18 arêtes communes, 6 droites communes ;
   - (12, 3) et (12, 0) ;
   - (9, 3) ;
   - (8, 0).

   BvLS n'utilise que l'aligné ; le jumeau, aligné et (12,3) ; Γ₄, 4 types ; Γ₃, les 5.
3. **Le vrillage est obligatoire à 99** (démontré, par le lemme 1 de la note 165). Si toutes les bijections étaient
   alignées avec une holonomie d'échange de règles triviale, en prenant une règle par grille on obtiendrait un
   étalement régulier, ce qui est impossible à 99. À 243 au contraire, l'alignement total existe (c'est BvLS).
4. **Rigidité du recollement.** Pour la représentation de Γ₃ à deck trivial, recoller 1, 2 (dans une même partie ou
   non), 3 (triangle ou coclique) ou 4 grilles, ou même une **partie entière de 9 grilles** (153 bijections libres),
   ne redonne que Γ₃ (`regluing.py`, `reglue_drive.py`). Les représentations en grilles sont **localement rigides** :
   la liberté est globale, pas locale.

## 4. Nécessaire contre artefact (bilan provisoire)
| structure | statut |
|---|---|
| structure 2-locale (moulin + Γ₂ ↔ paires de voisins) | **nécessaire**, identique pour tous les graphes, donc sans information |
| critère spectral de rigidité (note 165 §1) | **nécessaire** (identité) |
| formes possibles de partitions équitables | **nécessaire** (spectre) : 2 formes à 99, 11 à 243 |
| loi locale de recollement | **nécessaire** dès qu'il existe une partition en grilles |
| structure affine AG(5,3) | **artefact probable** (les 4 graphes ont été construits ainsi) |
| étalement de lignes régulier | **artefact** du re-voltage ; impossible à 99 |
| plancher Z₃ | **artefact de la fibre-ligne** (disparaît en fibre-grille, Γ₃) |
| partitions en grilles | **intrinsèque probable** : présentes dans les 4 graphes sans avoir été imposées, y compris hors des étalements de lignes |
| loi des motifs 9 \| 3+3+3 | **observée partout**, à démontrer |

## 5. Expériences en cours
- **243 « à partir de zéro ».** Revêtements de K_{9,9,9} à fibres grilles, sans structure affine ni étalement imposé
  (`grid243_scratch.py`). Test décisif : les solutions ont-elles toujours un étalement de lignes régulier (donc le
  plancher Z₃) ?
- **99, sous-cas (A).** Revêtements de K₁₁ (`conway_grids.py`).
