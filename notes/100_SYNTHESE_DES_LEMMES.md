# 100 — Synthèse des 21 lemmes : ce qu'ils donnent ensemble

*25/09, 06 h. Question de l'utilisateur : « T'as 21 lemmes, tu les as jamais mis ensemble pour arriver à une
conclusion ? » Réponse honnête : ils avaient été combinés au coup par coup (L15 + L16, L20 + L20 bis/ter, L21 ⊃ L20),
jamais systématiquement. Voici la synthèse complète. Conclusion en §4 : **aucune combinaison des 21 lemmes ne peut
donner de contradiction, et cela se démontre** ; la raison est précise, et elle dit quel lemme manque.*

> **Mise à jour (08 h, notes/101) : L22 exclut k = 30, donc k ≤ 28.** La proposition de cohérence du §4 reste vraie
> avec **k = 28** à la place de k = 30 (L22 n'est pas contredit : 28 ≤ 28 et les signes 7-adiques associés sont
> satisfiables). Mais le corpus contient désormais un **plafond** (sur k), et le profil 7-générique est interdit.
>
> **Mise à jour (fin de matinée, notes/102) : L23.** Le signe mod 7 des blocs extrêmes s'ajoute au rang. Une droite
> dont τ(G(L)) est un carré non nul mod 7 force k ≥ 24. Fenêtre heuristique : k ∈ {24, 26, 28}. Le profil de la
> proposition (torsion maximale, k = 28) reste cohérent.

> **Mise à jour (après-midi, notes/105) : L8 est démontré** (un point de Hamming impose un plan de Fano sur les
> classes, puis une contradiction ; aucune exécution SAT). Cela ne change pas la conclusion du §4 : L8 est un
> plancher, et le profil de torsion maximale le satisfait. La méthode (droites au-dessus des triangles de Kneser)
> est en revanche la première qui contrôle les arêtes génériques de Γ₂(x).

> **Mise à jour (soir, notes/108–109).** L11 démontré et g(x) ≤ 17 (comptage des fentes). Le côté peu tordu est
> désormais fermé à la main jusqu'à L14 exclu. Le profil de torsion maximale du §4 reste cohérent : en torsion maximale,
> les comptages du premier et du second ordre sont des tautologies, et l'objet d'holonomie de L8 ne se transporte pas
> (2 doubles par sommet en moyenne, notes/109). Le verrou est inchangé : il manque un plafond (P ≥ 1152).

> **Mise à jour (soir du 25/09, notes/110–111).**
> - **L14 pour |C| = 2 est démontré à la main** (relu indépendamment par la session « structures »). C'est le premier
>   contrôle manuel de « doubles » (arêtes génériques non bijectives) : trois doubles sont forcés par μ, et un bloc
>   tordu × tordu reçoit 4 voisins communs pour une demande ≥ 5.
> - Pour tout |C|, les deux torsions ont le même graphe de classes. |C| = 3, 4 restent au SAT ; |C| = 5 est ouvert,
>   avec des bilans exacts sans jeu, mais cohérents.
> - **Deux routes de plafond fermées** : Minkowski sur Λ₃, Λ₋₄ (la paire de Petersen passe tout) et Akiyama sur le
>   réseau des droites (rang 48, S₂₆ ≠ 0).
> - Nouveau lemme sans contradiction : les codes p-aires des droites contiennent leur dual (p = 2, 3, 5).
> - Contrôle : Gewirtz, qui existe et est tordu au maximum dans la famille (0, 2), est lui aussi sous la borne de
>   p-rang. La 7-spécialité exigée par L22 n'est donc pas anormale.
> - Le verrou reste le même : aucun mécanisme de plafond.

> **Mise à jour (nuit du 25/09, notes/112–114).**
> - **notes/112 : vers g(x) ≤ 16.** 𝒩 est un 4-cycle (lemme du degré minimal), plus les lemmes A et B et le contrôle de
>   blocs du second ordre. Il reste 20 configurations, qui demandent le troisième ordre.
> - **notes/113 (« structures ») : le contenu de C3 ne se transpose pas** (no-go : il faut une symétrie d'ordre impair).
>   Genre local et global cohérent en 7 et en 11 ; la somme de Gauss de l'Arf retombe sur L17.
> - **notes/114 : labo expérimental** (méthode C3, `Desktop/c1_experimental`).
>   - Le graphe lointain d'une droite a un spectre fixé par G(L) ; ses réseaux sont de rang 18 et 8. Nikulin ne mord
>     jamais.
>   - Les graphes réels de valeurs propres {3, −4} (Paley(49), réseaux d'AG(2,7), srg(50,21,8,9)) confirment que L22
>     est sain.
>   - Équilibre d'une droite (C2) et lemme E : le modèle de Fano est exclu si σ respecte l'appariement.
>   - Droites équiangulaires : fermé (borne 540).
>   - **Tout cela est côté plancher ou cohérent : le plafond manque toujours.** Cadre utile (« structures ») : une
>     contradiction en torsion maximale exigerait un sous-graphe induit forcé de spectre local hors de [−4, 3], ou
>     une égalité de Rayleigh forcée.
> - **notes/115 : lemme du triangle (première contrainte exacte active en torsion maximale).** Pour tout sommet et
>   toutes trois classes, T ⪯ 3I − P_∂ (T : transitions internes aux 12 paires ; recalcul indépendant par
>   « structures »). D'où e ≤ 12 ; au cas tendu, un vecteur propre de valeur 3 et des comptes exacts.
>   - En torsion maximale, il tue 22 % des configurations localement admissibles.
>   - Il force le modèle de Fano au régime tendu : toute σ-arête interne le tue.
>   - Pas encore un plafond : les configurations aux transitions étalées passent.
> - **notes/116 : second ordre exact ; le Fano tendu survit au niveau des blocs.**
>   - Outils généraux : A_Δ² + A_Δ − 12I = 2J − ∂ᵀ∂ ; identités de second ordre par blocs, avec
>     Σ_z cnt(z,R)(cnt(z,R) − 1) = 16 − 2e(R) ; critère lointain (U)/(L) en formes closes. Recalcul indépendant par
>     « structures » (contrôles Paley 9 et BvLS).
>   - Au Fano tendu : comptes exacts et variance nulle (F5). Pourtant un témoin passe tous les tests de niveau bloc
>     (admissibilité, 231 identités, toutes les compressions de Rayleigh). Route de plafond fermée.
> - **notes/117 : (P2) linéarisé par types (méthode de C2).** En torsion maximale générique, 19 configurations locales
>   admissibles sur 31 sont impossibles, chacune avec un certificat de Farkas exact ; l'un d'eux a été revérifié par
>   « structures ». Premier outil qui mord massivement sur le cœur. Énoncé d'échantillon : environ 40 % survivent,
>   et il reste à les caractériser.
> - **notes/118 : niveau paire × bloc et obstruction Ψ au Fano tendu.**
>   - Les 3 survivants « blocs + cellules » de l'échantillon S = 0 meurent au niveau paire × bloc (2 certificats
>     revérifiés par « structures », le 3ᵉ en flottants) ; 19 certificats de cellules sur 19 revérifiés.
>   - La famille qui tue est cellcross : Σ_z δ_R(z)c_R′(z) = −Σ_{y∈R} ε(y)c_R′(y).
>   - Au Fano tendu, fonctionnelle universelle explicite Ψ_R et forme close (reproduites par « structures »). Mais
>     des retournements bien choisis l'annulent. Les 21 systèmes « cellules par bloc » échouent dans 16 à 19 blocs de
>     chaque configuration testée ; le lemme uniforme n'est pas fait.
>   - Strate des σ internes : 1 survivant « blocs + cellules » sur 24, indéterminé en paire × bloc sous 5 minutes.
>
> - **notes/119 : lemme P-Ψ (mathématiques pures).** Au Fano tendu, pairblk combiné à Ψ donne une condition par paire :
>   θ(z_X(y)) + θ(z_Y(y)) = 0. Démontré, et relu à la main par « structures ».
>   - Droite par droite, c'est un système affine sur F₂ en les retournements.
>   - Chacun des 9 σ tendus testés a des droites sans aucune solution : ils sont morts pour tout τ Fano.
>   - Le lemme « aucun sommet de Fano tendu » reste à conclure par un argument global.
>
> - **notes/120 : vecteurs propres cellulaires forcés ; triades au Fano tendu.**
>   - En tout sommet, au moins 5 fonctions constantes sur les cellules sont vecteurs propres de A_Δ pour 3 (dimension :
>     35 + 40 > 70) ; mod 7, au moins 35 − k ≥ 7 (L19, L22). C'est une contrainte non linéaire, invisible aux PL.
>   - Au Fano tendu (transposition du Théorème F de C2), les doubles d'un bloc viennent de ses deux parallèles, avec des
>     règles rigides cerise/antipode (deux cas par triade). Le budget vaut 8 et il est saturé : pas de contradiction
>     directe.
>
> - **notes/121 : point d'étape du 26/09.** Tableau de ce qui est démontré, observé, fermé et ouvert. Les outils locaux
>   tuent chaque configuration testée, mais aucun argument uniforme n'est encore trouvé. Le verrou est reformulé, pas
>   levé.
>
> - **notes/122 : Fano tendu, différences de retournement.**
>   - Lemme démontré, relu par « structures » : T(L) est sans triangle ssi poids(d(L)) ≠ 1, et T(L) = C6+C6 ssi
>     d(L) = (1,1,1).
>   - Identité des parités de branche.
>   - Forme réduite de P-Ψ : les droites tout-CM sont toujours résolubles, et τ y est déterminé par σ.
>   - Cadre commun avec la contrainte τ–σ d'Astra.
>   - *Suite (Astra, dossier n° 3) : P-Ψ + admissibilité a une solution, donc P-Ψ n'est pas un lemme de Fano complet.
>     Le témoin meurt au niveau paire × bloc par des bornes ordonnées. Le Fano tendu est désormais le chantier d'Astra.*
>
> - **notes/123 : porte I_x en torsion maximale (P = 0).**
>   - Surtout une relecture : holonomie et prismes (F1, notes/99), ombres (notes/114) et schéma des droites
>     (notes/99, 109) étaient déjà connus.
>   - **H + 3P = 213 444** est la formule de Reimbayev, retrouvée et contrôlée sur BvLS. Le plafond P ≥ 1152 équivaut
>     à H ≤ 209 988.
>   - Nouveau : à P = 0 et S = 0, H(x) = 12 936 en tout sommet. Le troisième ordre est localement constant en torsion
>     maximale ; le plafond doit venir des arêtes génériques effectives.
>
> - **notes/124 : le lointain d'une droite, complément de Schur exact.**
>   - Sur Q, Φ_F = −7·Π_{K₋₄(L)} (contrôle BvLS : −9Π). Le graphe lointain est donc fixé par les ombres et par un
>     sous-espace de dimension 7 + c.
>   - Mod 7, rang R_L = k − 22 ≤ 6 (formule de notes/102 §8, revérifiée exactement).
>   - C'est la cible du dossier n° 5 d'Astra.
>
> - **notes/125 : cycles courts des graphes de droites.**
>   - Σ_L c₄(G(L)) = S + 3P et Σ_L c₃ = 2P. À P = 0, S compte les 4-cycles des 231 graphes de droites.
>   - À P = S = 0 : maille ≥ 5 partout. Les profils (4,4,4) et (4,8) sont exclus (lemme de Klein) ; reste (6,6).
>
> - **notes/126 : L21 raffiné.** k ≥ 23 − d(L) + 2r(L), où r(L) est le rang de Mᵀ sur le noyau local supplémentaire.
>   - Une droite dégénérée ne fait baisser la borne que par ses vecteurs propres mod 7 **équilibrés** portés par N(L).
>   - Donc k ≤ 20 impose à chaque droite au moins deux tels vecteurs.

## 1. Les quantités en jeu
- **Torsion** : |W(x)| = nombre de paires (étiquette, classe) tordues en x ; m(e) = 6 − d(e) = prismes de barreau e ;
  P = nombre de prismes = 1386 − Σ_x|W(x)|/6 (L15) ; g(x) = grilles par x.
- **Arithmétique** : k = rank₇(A − 3I) − 15 (même en tout sommet), signes 7-adiques.
- **Statistiques d'ordre 7** : P et S (L18).

## 2. Le tableau : chaque lemme, ce qu'il contraint, dans quel sens
| lemme | contrainte | sens | statut |
|---|---|---|---|
| L1 (Makhnev 1988) | Γ n'est pas grid-full : Σ|W| > 0 | **plancher de torsion** | preuve |
| L7 | un point de Hamming n'est pas fixé par une involution | plancher (branche C2) | preuve |
| L8 | aucun point de Hamming : |W(x)| > 0 en tout x | **plancher** | **preuve (notes/105, squelette de Fano)** |
| L9, L9' | torsion + transitions mates ⟹ une grille manque | règle locale (plancher) | preuve |
| L10 | g(x) ≤ 18 | **plancher** (g = 21 via L8) | preuve (g = 21 : L8 démontré) |
| L11 | les torsions touchent ≥ 4 classes | **plancher** | preuve (notes/108, lemme D1) |
| L12 | propagation : une étiquette ou une classe tordue seule est impossible | **plancher** | preuve |
| L13 | une classe est tordue par 0 ou ≥ 2 étiquettes | règle locale | preuve |
| L14 | deux étiquettes tordues ne suffisent pas (|C| ≤ 4) | **plancher** | \|C\| = 2 : preuve (notes/111) ; \|C\| = 3, 4 : SAT non certifié |
| L15 | P = 1386 − Σ|W|/6 ; Σ|W| = 6048 + Σν³ | identité | preuve |
| L16 | P ≤ 1151, c'est-à-dire Σ|W| ≥ 1410 | **plancher** (global) | preuve |
| L18 | 0 ≤ S ≤ n₃, dictionnaire d'ordre 7 | identité + encadrement | preuve |
| L5, L6 | grilles serrées ; comptages enracinés ; surface Σ, χ = 3P − 4158 | identités (Σ a un bord : aucune borne) | preuve |
| L2, L4 | k pair, le même en tout sommet, k ≤ 30 | arithmétique | preuve |
| L3, L17 | signes 7-adiques fixés par k (oddité) | arithmétique, compatible pour tout k pair | preuve |
| L19 | U_x : diviseurs 1^k 7^{70−2k} 49^k, déficit ≤ k | lien k–torsion, vide si k grand | preuve |
| L20 | k ≥ 11 − 2e(τ_a) : peu de torsion en une étiquette ⟹ k grand | **plancher de k** | preuve |
| L20 bis/ter, L19 bis | k ≥ 10 | **plancher de k** | preuve + calcul exact |
| L21 | k ≥ 23 − d(L) ; droite générique ⟹ k ≥ 22 | **plancher de k** | preuve |
| L22 | k ≤ 28 (genre de Λ₋₄) | **plafond de k** | preuve (notes/101) |
| L23 | τ(G(L)) carré non nul mod 7 ⟹ k ≥ 24 (signe des blocs extrêmes) | plancher de k, **par la torsion** | preuve (notes/102) |

**Aucune ligne n'est un plafond de torsion** (une borne inférieure sur P) **ni un plafond de k** (autre que k ≤ 30).

## 3. Ce que les combinaisons donnent réellement (corollaires nouveaux)
**C1 (L20 + L20 ter + L15). Si k = 10, alors pour toute arête e : m(e) ∈ {0, 2}.** Donc |W(x)| ≥ 56 en tout sommet,
et P est pair avec P ≤ 462.
*Preuve.* À k = 10, chaque étoile a un rang 11 − 2e ≤ 10, donc e(τ_a) ≥ 1 (L20). Le calcul exact de L20 ter pour
k = 10 (refait ce jour, `kbound_exact.py 10`) exclut (1;2,3) et (4;2). Il laisse (0;2,2,2), (0;2,4), (0;6), (2;2,2)
et (2;4), qui ont 0 ou 2 classes non tordues. Or m(e) est le nombre de classes non tordues. Donc m(e) ∈ {0, 2},
d(e) ≥ 4, |W(x)| ≥ 14·4, et 3P = Σ_e m(e) ≤ 693·2, pair. ∎
**C2 (L21). Si k ≤ 20, toutes les droites sont 7-dégénérées** (G(L) non connexe, ou 7 divise le nombre d'arbres
couvrants de G(L)). **Si k = 10, chaque droite a d(L) ≥ 13**, alors que le maximum trouvé numériquement est 9 :
k = 10 est exclu numériquement, pas encore démontré (il manque la preuve de d ≤ 12).
**C3 (L12 + L13 + L14 + L11). Plancher local** : en tout sommet, au moins 3 étiquettes tordues (ou 2 avec |C| = 5,
non traité), au moins 4 classes touchées, donc |W(x)| ≥ 6. Plus faible que la moyenne imposée par L16 (14,2).
**C4 (L5 + L10 + L16).** g_tot ≤ P/6 ≤ 191 (chaque grille contient 6 prismes, chaque prisme est dans au plus une
grille), donc la moyenne de g(x) est ≤ 17,4. C'est à peine mieux que L10.
**C5 (L3 + L17 + L2).** Compatibles pour tout k pair (déjà noté en L3 et L17) : pas de contradiction de genre.
**C6 (L6).** χ(Σ) = 3P − 4158 ≤ −705 : Σ est une surface à bord très négative, ce qui ne contraint rien.

## 4. La conclusion : les 21 lemmes ne peuvent pas se contredire
**Proposition (cohérence).** Le profil suivant satisfait simultanément les énoncés de L1 à L21 :
- toutes les transitions τ_a sans boucle en tout sommet (« torsion maximale »), donc m(e) = 0, P = 0, |W(x)| = 84 ;
- aucune grille (g ≡ 0) ;
- k = 28 (et les signes 7-adiques associés ; k = 30 est exclu par L22, notes/101) ;
- S quelconque dans [0, 4158].
*Vérification, lemme par lemme.*
- **Planchers de torsion.** L1, L7, L8, L10, L11, L12, L14, L16 excluent seulement la torsion faible, et le profil est
  à torsion maximale.
- **Règles locales.** L9 et L9' ont pour hypothèse une transition non tordue τ_{c̄}(a) = ā : elles sont vides ici.
  L12 est satisfait, car toute étiquette tord toute classe. L13 aussi : chaque classe est tordue par 12 étiquettes.
- **Identités.** L5, L6, L15, L18 sont satisfaites (P = 0, g = 0, S ≤ n₃ = 4158).
- **Arithmétique de k.** L2 et L4 : k pair. L3 et L17 sont des conditions de signe compatibles pour tout k pair. L19 :
  70 − 2k = 14 ≥ 0. L20, L20 bis/ter, L21, L22 : 28 ≥ 11 − 2e, 28 ≥ 10, 28 ≥ 23 − d(L), 28 ≤ 28.

Tout raisonnement qui combine ces énoncés, et seulement eux, reste vrai dans ce profil. **Aucune contradiction ne peut
donc sortir de L1–L21.** Ce n'est pas une preuve d'existence de Γ : c'est une limite de ce corpus de lemmes.

*Remarque (corrigée à 08 h).* Le profil « tordu générique » (τ comme des couplages aléatoires : P ≈ 126) passe les
relâchements calculés (ordre ≤ 8, triplets de droites), **mais pas L22** : une structure 7-générique aurait k = 30,
exclu. Un Γ doit donc être 7-spécial en chaque sommet (rank₇ M_x ≤ 28).

## 5. Ce que cela dit du programme
1. **Le corpus est unilatéral.** Tous les lemmes locaux excluent la torsion faible (le côté Hamming). L16, seul lemme
   global sur P, pousse dans le même sens. Les lemmes arithmétiques minorent k. Le côté « torsion forte », là où vivrait
   un Γ générique, n'est touché par **aucun** lemme.
2. **La pièce manquante est un plafond.** Une contradiction exige au moins un énoncé qui exclut la torsion forte. Soit
   un plafond local (un sommet ne peut pas être trop tordu), soit une borne inférieure globale sur P, soit une
   majoration globale de k. Rien de ce qui a été essayé n'en fournit un ; toutes les méthodes par moyennes ou par
   positivité sont faisables à P ≈ 0–126.
3. **Candidats, par coût.**
   - (a) *Frontière miroir (gelée : plus de solveurs, décision du 25/09).* Tester par SAT si un sommet entièrement tordu est possible (les 14 τ sans boucle en x).
     C'est le symétrique de L8. Le test « tous de type (2,2,2) » a été tué à 4 Go sur le portable. PC du labo
     seulement ; et même un succès ne donnerait qu'un plafond faible (au moins un prisme par sommet).
   - (b) *Plafond arithmétique.* Une majoration de k par un argument global. **Obtenu à 08 h : L22, k ≤ 28, par le
     genre de Λ₋₄ (notes/101).** Reste à le relier à la torsion.
   - (c) *Méthode globale nouvelle* (réseau des droites et formes modulaires, notes/96) : plusieurs jours, issue
     incertaine.
   - (d) *Resserrer k par combinaison* (C2 : prouver d ≤ 12, d'où k ≥ 12) : faisable, mais ce n'est encore qu'un
     plancher de k, sans effet sur le verrou.

## 6. Réponse courte
Mis ensemble, les 21 lemmes donnent un portrait cohérent : Γ serait **fortement tordu** (torsion moyenne ≥ 14,2 et
torsion en tout sommet), avec **k ≥ 10 pair** (et k = 10 imposerait m(e) ∈ {0, 2} partout et P ≤ 462). Ils ne peuvent
pas se contredire, parce que tous poussent dans la même direction et que le régime de torsion maximale les satisfait
tous. Pour conclure, il faut un résultat d'un autre type, un plafond, qu'aucun des 21 n'est.
