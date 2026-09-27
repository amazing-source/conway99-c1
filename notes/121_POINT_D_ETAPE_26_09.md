# 121 — Point d'étape du 26/09 : ce que l'analyse locale en torsion maximale a donné, et ce qui reste

*26/09, fin d'après-midi. Synthèse des notes/114 à 120, écrite pour qu'une reprise sache exactement où l'on en est.
DÉRIVÉ = preuve écrite ; OBSERVÉ = calcul (contrôle exact ou PL certifié). Pas de nouveau calcul ici.*

## 1. Le cadre
- En un sommet x : 7 classes, 14 étiquettes, 84 paires Δ_x. Les données locales (τ, σ) fixent les 4 voisins spéciaux
  de chaque paire ; les 8 voisins génériques, pris entre blocs disjoints, sont inconnus.
- Toute l'information srg en x tient en une identité : A_Δ² + A_Δ − 12I = 2J − ∂ᵀ∂, avec les fentes. Sur ker ∂, A_Δ
  n'a que les valeurs propres 3 (×40) et −4 (×30). Le problème en x **est** le problème entier.
- Le profil de torsion maximale (P = 0, notes/100 §4) satisfait tous les lemmes L1 à L23 : c'est le cœur à attaquer.

## 2. Ce qui est démontré à la main
| énoncé | note | relecture |
|---|---|---|
| lemme du triangle : T ⪯ 3I − P_∂ ; e ≤ 12 ; au cas tendu, vecteur propre et comptes exacts | 115 | « structures » |
| identités (P2) par blocs = repère ajusté de constante 196 dans E₋₂ ; forme « 4-cycle alterné » | 116, 117 | « structures » |
| identités de cellules (35 dimensions) et paire × bloc ; cellcross = ⟨(A+I)ε_R, A1_R′⟩ = 0 | 117, 118 | « structures » |
| Fano tendu : fonctionnelle universelle Ψ_R ; condition par bloc I_R = 0 | 118 | « structures » (S21) |
| **Fano tendu : lemme P-Ψ**, condition exacte par paire, systèmes affines F₂ par droite | 119 | « structures » |
| Fano tendu : cycles τ de chaque droite = C6+C6 ou C12 ; classe doublée ⟹ p_Z = 2 | 119, 120 | « structures » (partiel) |
| Fano tendu : triades de doubles, règles cerise/antipode (cas A et B) | 120 | « structures » (types, R1) |
| **en tout sommet : ≥ 5 vecteurs propres cellulaires pour 3 (Q), ≥ 35 − k (mod 7)** | 120 | « structures » |
| à P = 0 : torsion aux voisins = droites internes sans « boucle » = K sans triangle (carrés d'Astra) | JOURNAL, 26/09 | « structures » |

## 3. Ce qui est observé (PL certifiés, énoncés d'échantillon)
- Sur des configurations locales aléatoires admissibles en torsion maximale (S = 0), 45 au total :
  - environ 55 % meurent au niveau bloc ;
  - environ 90 % des survivantes meurent au niveau cellules ;
  - **les 3 dernières meurent au niveau paire × bloc**.
  - Chaque mort a un certificat de Farkas exact. « Structures » en a revérifié 21 avec son propre code.
- Strate des σ internes (m = 1, 2) : 1 survivant « blocs + cellules » sur 24, indéterminé en paire × bloc sous 5 minutes.
- Fano tendu : 9 σ sur 9 tués par P-Ψ, pour tout τ de type Fano. Heuristique : environ 0,2 % des solutions de KBLDP
  pourraient passer P-Ψ. Ce n'est donc probablement pas un lemme complet.

## 4. Portes fermées (avec la raison)
- **Relaxations symétriques** (moyennées sous 2⁷:S₇). Elles perdent la cohérence des spéciaux entre paires ; notes/91
  les donnait déjà faisables à l'ordre 8. Tout certificat uniforme serait symétrique : il n'en existe pas à ces niveaux.
- **Certificats par configuration → preuve.** Il y a environ 10¹⁰⁰ configurations admissibles ; aucune réduction finie
  n'est connue. Une vraie preuve exigerait une strate rigide, ou un invariant uniforme.
- **7-adique par sous-matrices déterminées.** L21 donne k ≥ 22 au mieux. Contredire k ≤ 28 exigerait un support
  déterminé de rang₇ ≥ 45, et les plus grands connus ont 39 points.
- **Fano tendu par budget de doubles (Théorème F de C2).** Le budget vaut 8 et il est saturé par les blocs parallèles :
  pas de dépassement. Le dérangement cerise/σ : T ≡ 1 est faux au témoin, mais ce témoin est une configuration partielle déjà morte ; la route reste OUVERTE (re-scopé 27/09).
- **Dimension forcée au Fano tendu.** La tension crée elle-même 6 vecteurs propres par blocs : le test est vide.

## 5. Portes ouvertes (avec l'obstacle)
- **Fano tendu complet.** P-Ψ, triades et KBLDP ensemble : fini, mais demande de coupler globalement σ, τ et les
  atterrissages. À la main, c'est long ; par machine, ce serait un PLNE, que l'utilisateur ne veut pas pour l'instant.
  Voie symétrique possible : configurations invariantes sous Z₇ (Singer), une droite suffit.
- **Géométrie interne I_x à P = 0.** 140 droites internes et la torsion aux voisins (K sans triangle). Aucun de nos
  modèles ne voit les droites internes. Obstacle : il faut un modèle au niveau des paires.
- **Composantes de K (Astra).** À P = 0, au plus 3 composantes, chacune de taille multiple de 7 et ≥ 175. Une
  structure « arc-en-ciel » (chaque droite porte une arête de chaque composante) est compatible avec ces comptes. Si
  elle était forcée, elle donnerait en x une 3-coloration des étiquettes avec c(u) ≠ c(ū) et c(u) ≠ c(τ_v(u)).
- **Dimension forcée (général).** Elle est non linéaire, donc hors des PL. Elle ne mordrait qu'avec des comptes
  cellulaires connus, c'est-à-dire sur des strates rigides.

## 6. Lecture d'ensemble
- Les outils locaux sont désormais très forts **configuration par configuration** : aucune configuration aléatoire
  n'a survécu au niveau paire × bloc.
- Mais toute preuve uniforme doit, soit réduire à des strates rigides (seul le Fano tendu en est une, et il n'est pas
  clos), soit trouver un invariant qui ne se moyenne pas.
- Le verrou de notes/100 (« il manque un plafond ») est reformulé, pas levé. Le plafond local existe config par
  config, mais pas uniformément.
