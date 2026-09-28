# 149 — Couplage des sept étoiles (proposition Sol / utilisateur, 28/09) : évaluation, et la vraie cible (B)

*28/09, matin. C1. Directive de l'utilisateur : arrêter la machinerie des 1 272 paires, attaquer le couplage spectral des sept
étoiles, viser un invariant (ou un objet arithmétique impossible) indépendant de V. DÉRIVÉ = preuve écrite ; CALCUL = exact.*

## 0. Énoncés
| énoncé | statut |
|---|---|
| L'identité (2) Σ tr A_c² + 2Σ tr A_cA_d = 47 040 équivaut à « 10 non-zéros par ligne » + tr(NR) = 0 : automatique | DÉRIVÉ |
| Tout moment de Σ_c A_c découle de N² = N + 12I − R et NR = 0 : aucune congruence n'en sortira | DÉRIVÉ |
| Q_c (compagnons en c⁰) et P_c (croisées) sont TOUJOURS des couplages parfaits ; Q_c ∩ P_c = arêtes D internes à l'étoile c | DÉRIVÉ |
| Sept étoiles libres (P_c ∩ Q_c = ∅ pour tout c) ⟺ tout-dis ⟺ famille (B) de notes/137 | DÉRIVÉ |
| « 11 types spectraux » est faux : 66 440 couples libres (11 classes de Q) donnent 1 856 spectres de D_c | CALCUL |
| Chaque étoile engendre exactement 11 dimensions du repère w (spectre de D_c sur 1⊥ dans [2, 20]) | CALCUL |
| BvLS (m = 11) est tout-frère : 110/110 orbites ont D(U) = sœur ; Paley(9) aussi (forcé) | CALCUL |
| Sonde SAT de (B) (modèle d'orbite exact + tout-dis) : inconnu à 300 s | CALCUL |

## 1. (2) est vide
- Σ_{c,d} tr(A_cA_d) = Σ_{u∈⋆c, v∈⋆d} (w_u,w_v)² = 4‖W‖² (chaque u est dans deux étoiles), et ‖W‖² = tr W² = 28 tr W = 28·420.
  D'où 47 040 = 15·56² (et non 7·56²).
- Développement : tr W² = 42·100 + Σ_{u≠v}(4N_uv − R_uv)² = 4200 + 16·#nz(N) − 8 tr(NR) + 840.
  Avec #nz = 420 (diagonale de N²) : tr W² = 11 760 − 8 tr(NR). Donc (2) ⟺ tr(NR) = 0, conséquence de NR = 0.
- Plus généralement, tr((Σ A_c)^k) = 15·56^k est une conséquence de W² = 28W, donc de N² = N + 12I − R. Une identité
  spectrale entre étoiles ne peut donner de contradiction que si elle utilise l'intégralité (entrées de N dans {0, ±1}) et la
  combinatoire. La tenue de livres spectrale seule est toujours cohérente.

## 2. Le théorème d'étoile, énoncé exact
- Au sommet intérieur a = c⁰ : ses 12 voisins extérieurs O_a forment un couplage parfait (λ = 1) : c'est Q_c.
- Tout u ∋ c⁰ a exactement un voisin contenant c¹ (règle (I)) : ces arêtes croisées, vues en orbites, forment P_c. P_c est
  un couplage parfait sans point fixe (u ≁ σu).
- Q_c(U) = P_c(U) ⟺ u est adjacent à v et à σv ⟺ D(U) = V ∈ étoile(c). La ligne de U dans l'étoile c est alors nulle.
- Donc D_c = 11I + Π_c − J + 4(Q_c − P_c) vaut TOUJOURS, avec P_c, Q_c couplages parfaits, les arêtes communes s'annulant.
  « Sept étoiles libres » (P_c ∩ Q_c = ∅ partout) ⟺ aucune orbite n'a son partenaire D dans une de ses deux étoiles ⟺ tout-dis.
- Arête interne à une cellule (c,d) : elle est dans Q_c ⟺ dans P_d (et dans P_c ⟺ dans Q_d).

## 3. Les deux repères d'étoile (CALCUL, `code/star7_types.py`, ~1 min)
- Repère impair w (15 dimensions) : Gram d'étoile D_c = 11I + Π − J + 4(τ − μ). Sur les 66 440 étoiles libres (μ à Aut(Π) près,
  τ quelconque disjoint) : 1 856 spectres distincts, valeurs propres sur 1⊥ dans [2, 20]. Chaque étoile est donc de rang 11.
- Repère pair β (L_β de « structures », 15 dimensions) : Gram d'étoile 5I − Π − 2(μ + τ). Son rang vaut 12 − #amas
  (composantes de μ ∪ τ ∪ Π). Répartition : rang 11 pour 61 464 couples, 10 pour 4 816, 9 pour 160. Il y a 848 spectres distincts.
- Repère des sommets (30 dimensions = β ⊕ w) : l'étoile X_c (24 sommets) a un rang de 23 − #amas.
- Deux étoiles de rang 11 dans ℝ¹⁵ se coupent en dimension ≥ 7, alors que la cellule commune n'en fournit que 2. Mais c'est
  automatique en dimension 15 (27 + 22 − 42 = 7). C'est un élagage pour une recherche, pas une obstruction.

## 4. Méta-fait : où un argument uniforme en m est permis (CALCUL, `code/bvls_dtypes.py`)
- Les seuls graphes connus de la famille (λ, μ) = (1, 2) avec une involution à un point fixe sont Paley(9) (m = 2) et BvLS
  (m = 11). Les deux sont tout-frère : D(U) = orbite sœur pour les 110 orbites de BvLS.
- Tout-frère est mort à m = 7 (S39 §4, trois preuves ; Th. D de C2).
- Donc (A) (types à pivots) et (B) (tout-dis) ne sont protégés par aucun exemple connu, à aucun m. Un argument uniforme en m
  qui utilise la présence d'une orbite non frère n'est pas interdit par BvLS. La remarque de S40 (« une preuve doit utiliser un
  objet qui n'existe qu'à m = 7 ») ne vaut que pour la branche tout-frère, déjà close.

## 5. (B) : état et suite
- (B) = tout-dis : sept étoiles libres, D = 2-facteur de KG(7,2), SEC-dis partout. En chaque bloc c : 12 quadruplets ι sécants,
  un par étiquette x, dont la σ-paire est D(O_x). Les 18 autres ι-paires sont disjointes et correspondent aux 9 paires D
  internes à F_c.
- Sonde (`code/alldis_sat_probe.py`) : orbit_sat.build(7) (R, D, I, P exacts), plus 441 clauses tout-dis, plus D(U0) = (3,4,0)
  (Stab(U0) est transitif sur les 20 orbites disjointes). 666 183 variables, 1 510 889 clauses. CaDiCaL 1.9.5 : inconnu à 300 s
  (tué à 480 s par le plafond). Le modèle monolithique ne tranchera pas vite.
- « structures » fait tourner un CP-SAT du couplage (S1–S3, conway99-rank17/n5_signed.py). Signes vérifiés ; sans N² c'est une
  relaxation faible, donc seul un UNSAT aurait du sens.
- Pistes :
  - un invariant tout-dis (comptage, parité, q:7 par bloc) qui distingue les étoiles libres des étoiles frères ;
  - à défaut, une recherche exacte structurée par étoiles, élaguée par les rangs d'étoile dans les deux repères (§3).
