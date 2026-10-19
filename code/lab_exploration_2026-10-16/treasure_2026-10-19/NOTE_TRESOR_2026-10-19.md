# Chasse au trésor : lois de famille, symétrie forcée, contraintes de variance (flag algebras)

*19/10/2026, LAB. Suite à la remarque de l'utilisateur : « il n'est pas symétrique ce qui est ultra louche, et en plus
aucun autre graphe de sa famille ne PEUT être asymétrique jusqu'à preuve du contraire. Quelque chose se cache … tu
devrais [l'atteindre] » ; puis « okay vasy », « utilise aws s'il faut pour ces tests, ils sont importants ».*

**Statuts.**
- **C** : calcul exact sur des graphes réels.
- **E** : calcul flottant (programme linéaire ou SDP), exploration.
- **H** : heuristique.
- **A** : déjà dans l'archive.
- **X** : ouvert.

**Fichiers** : `work/exploration_2026-10-16/treasure_2026-10-19/`.

---

## 1. Ce que les graphes connus disent (C)

### 1.1 Symétrie

Les groupes d'automorphismes de tous les srg à λ = 1 que nous connaissons ont un ordre divisible par 6 :

| graphe | ordre de Aut | source |
|---|---|---|
| Paley 9 | 72 | A |
| GQ(2,2) | 720 | A |
| GQ(2,4) | 51 840 | A |
| les 8 srg(243,22,1,2) | 3 849 120 ; 4 320 ; 864 ; 3 888 ; 2 916 ; 108 ; 162 ; 108 | A : `spreadfree_243_2026-10-12/NEW_GRAPHS_2026-10-13.md` |
| srg(378,52,1,8), le moins symétrique connu | 6 | A : `lambda1_construction_2026-10-14` |

Conway est le seul cas λ = 1 où les ordres 2 et 3 sont exclus (C2 et C3). D'où l'énoncé net de l'intuition de
l'utilisateur :

**Conjecture (S3).** Tout srg à λ = 1 possède un automorphisme d'ordre 3.

À 99, cette conjecture fermerait le problème. Aucun mécanisme n'est connu (X).

### 1.2 Deux lois locales candidates, testées

**(a) Réflexion en un point** (`third_point.py`, `third_point_243.log`).
- Définition : σ_x fixe x, échange les deux autres points de chaque droite par x et envoie l'étiquette {a, b} sur
  {a', b'}.
- BvLS : σ_x est un automorphisme pour les 243 sommets, et le « troisième point » d'une paire non adjacente est canonique
  (26 730 paires sur 26 730).
- Les trois autres graphes à 243 sommets : aucune réflexion n'est un automorphisme, et le troisième point n'est canonique
  que pour 31 à 45 % des paires.
- **Ce n'est donc pas une loi de famille.**

**(b) Fonctions additives sur les droites dans F₃** (`line_modrank.py`). On regarde dim Z₃, où
Z₃ = {y : la somme de y sur chaque droite est nulle mod 3} :

| graphe | dim Z₃ |
|---|---|
| Paley 9 | 4 |
| GQ(2,2) | 5 |
| GQ(2,4) | 6 |
| srg(243) : BvLS | 12 |
| srg(243) : les quatre autres testés | 6 |
| srg(378), quatre graphes | 1 (constantes seules) |

Pour p = 2 et p = 7, Z est nul partout. La loi tient dans la famille μ = 2, mais pas pour λ = 1 en général.
- À 99 : dim Z₃ est un paramètre libre entre 1 et 44. La borne vient de Z₃ ⊂ ker₃(A + I), et
  rank₃(A + I) = 55 exactement, car A + I ≡ E_r + J mod 3 (P).

**Conclusion.** La symétrie de la famille ne vient d'aucune loi locale simple. Une « symétrie forcée » serait un théorème
global.

---

## 2. Contraintes de variance (flag algebras de Razborov) sur le recensement exact

### 2.1 Principe (P)

- **Le recensement.** Pour tout type admissible H d'au plus 10 sommets, le nombre x_H de plongements induits est une forme
  affine explicite en 549 paramètres (57 à l'ordre 9). Le paramètre 1 est P, le nombre de prismes induits.
- **L'archive** n'utilisait que x_H ≥ 0, c'est-à-dire un programme linéaire.
- **Le bloc d'un type.** On fixe un type étiqueté σ (k sommets) et des flags F (extensions étiquetées de σ). Pour chaque
  plongement θ de σ, on note v_θ(F) le nombre de plongements de F qui prolongent θ. Alors M_σ = Σ_θ v_θ v_θᵀ est
  semi-défini positif.
- **Calcul des entrées.** Chaque entrée M_σ[F₁, F₂] est une somme, sur les amalgames de F₁ et F₂ au-dessus de σ, de
  comptes x_H du recensement. C'est donc une forme affine en les paramètres.
- La règle est exacte pour un seul graphe fini : pas de limite, pas d'approximation.

### 2.2 Résolution et validation

- **Méthode.** Les bornes viennent de plans coupants : programme linéaire HiGHS, puis vecteurs propres négatifs des
  blocs. Chaque itéré est une borne extérieure valide.
- **SCS rejeté.** SCS donnait un faux max P = 1 363 au-dessus de la borne du programme linéaire seul ; ses solutions ne
  sont pas assez précises.
- **Validation.** L'implantation dense (`flag_sdp.py`) et l'implantation creuse (`flag_engine.py` + `flag_cut_loop.py`)
  donnent les mêmes résultats.

### 2.3 Résultats en local, recensement d'ordre 9 (E)

| contraintes ajoutées au programme linéaire | P min | P max | grilles max |
|---|---|---|---|
| rien | 0 | 852,923 | 126 |
| blocs (7,8) sur 3 types, 112 à 128 flags | 0 | 852,923 | — |
| bloc (5,7), σ = 5 sommets indépendants, 794 flags | 0 | 852,923 | 126 |
| bloc « droite » avec flags de 4, 5 et 6 sommets (124 flags) | 0 | 852,923 | 126 |
| E3 (lemme de l'archive) | 0 | 852,923 | — |

Le bloc (5,7) coupe les deux sommets du programme linéaire, mais d'autres points de même valeur de P restent admissibles.
Les blocs (7,8) et le bloc « droite » sont déjà semi-définis positifs aux sommets du programme linéaire.

### 2.4 Campagne AWS, recensement d'ordre 10 (E)

- **Machine** : une Spot c7a.32xlarge à Londres, environ 2,1 $/h, coupée d'office après 3 h.
- **Blocs** : 21 blocs (5,7), 208 blocs (7,8) et 916 blocs (8,9), tous construits en 2 minutes.
- **Lemme E3** : 9 identifiants de types forcés à 0.

**Résultats (journaux dans `aws_logs/`).**

| contraintes ajoutées au programme linéaire d'ordre 10 | P max | P min |
|---|---|---|
| rien | 852,923 | 0 |
| E3 | 852,923 | 0 |
| E3 + 21 blocs (5,7) | 852,923 (9 itérations) | 0 (400 itérations) |
| E3 + blocs (7,8) et (8,9), boucle « AWS » | 726,5 après 11 itérations | 0,000001 |
| E3 + tous les blocs, boucle « AWS » | 692,39 après 12 itérations | 0,0001 |

**La baisse à 692 n'est PAS établie.**
- Dans la boucle « AWS », la normalisation par la diagonale n'a pas de plancher : on voit des valeurs propres normalisées
  jusqu'à −10²³, donc des diagonales quasi nulles, et des coupes calculées sur des vecteurs dont les composantes
  s'étalent sur 10¹⁵. La baisse arrive d'un coup (852,92 → 693,29) juste après de telles coupes.
- La variante robuste (`flag_cut_exact.py` : plancher de normalisation, coupes à vecteurs entiers, HiGHS réchauffé)
  donne max P = 852,9223 après 6 itérations, sur les mêmes blocs. Aucune baisse.

**Contrôle positif sur srg(243,22,1,2), même chaîne de calcul (E).** De vrais graphes y existent : BvLS a P = 8 910.
- Recensement d'ordre 10 pour (243, 22) : test de cohérence complet passé (`census243_10_check.log`). Ce n'est donc pas
  une erreur du recensement.
- Programme linéaire seul :
  - à l'ordre 9, max P = 8 910,000, exact ;
  - à l'ordre 10, max P = **8 905,82 < 8 910**, avec le simplexe dual comme avec le point intérieur de HiGHS ;
  - P = 8 910 y est déclaré infaisable.
- Le dual rationalisé laisse des résidus positifs d'environ 8,7·10⁻⁶ sur un paramètre d'ordre 10, qu'aucune borne a
  priori n'absorbe. Les échelles des lignes vont jusqu'à 7·10²¹.
- **Conclusion : en flottant, le programme linéaire d'ordre 10 exclut à tort un vrai graphe.** Avec les blocs, la borne
  descend à 8 898, puis HiGHS échoue (statut Unknown).

**Conséquence.** À l'ordre 10, aucune borne obtenue en flottant n'est fiable sans certificat exact. Cela vaut aussi pour
les « explorations flottantes sur le polytope d'ordre 10 » de l'archive, qui sont d'ailleurs étiquetées comme telles.

---

## 3. Lecture

- **Réponse à la question de l'utilisateur (« si tout respecte 852 ? »).**
  - Les contraintes de variance testées ne changent rien sur les configurations d'au plus 9 sommets : bloc (5,7) de
    l'ensemble indépendant, blocs (7,8), droite, arête, non-arête, avec ou sans E3. À cet ordre, les calculs sont sûrs ;
    le certificat exact P ≤ 852,92 existe.
  - À 10 sommets, le seul effet observé n'est pas fiable. Le contrôle 243 montre que la chaîne flottante y produit de
    fausses bornes.
- **Ce que ça établit.** Une obstruction à Conway, si elle existe, n'est pas une inégalité de variance sur de petites
  configurations, au moins jusqu'à 9 sommets. Cela s'accorde avec le budget d'entropie (`../reduction_2026-10-19`) : la
  surcontrainte est diffuse, à l'échelle d'une droite entière (environ 99 sommets).
- **Pour aller à l'ordre 10 de façon fiable** (X, coût) :
  - un programme linéaire certifié : variables remises à l'échelle, certificat dual rationnel, réparation exacte des
    résidus ;
  - c'est de l'ingénierie (environ une journée), avec un gain attendu faible au vu de l'ordre 9 et de la variante
    robuste.
- **La conjecture (S3)** (tout srg à λ = 1 a un automorphisme d'ordre 3) reste la formulation nette de l'intuition de
  l'utilisateur. Elle s'accorde avec toutes les données, mais aucun mécanisme n'est connu. Toutes les constructions
  connues à λ = 1 sont algébriques, et la rigidité (pas d'échange local, archive) empêche de s'en écarter : cela
  explique les données sans les démontrer.

**Coût AWS de la campagne** : environ 2,1 $/h × 1 h 10 (Londres) + environ 0,9 $/h × 0,5 h (Ohio), soit environ 3 $.
Les deux machines ont été arrêtées dès que le contrôle a tranché.
