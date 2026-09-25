# 106 — La voie 7-adique se ramène entièrement à la matrice générique G (résultat négatif, démontré)

*25/09, après-midi (session « structures », celle de notes/104). On a tenté de retourner le critère de notes/102 : au lieu
de forcer un bloc de rang ≥ 43, utiliser le plafond de L22 (rang₇ Q ≤ 42) pour forcer des relations linéaires. Le
premier geste est vide, et la raison est générale. Cette note l'enregistre pour qu'on ne refasse pas ce chemin.*

## Énoncé
Toute preuve de non-existence par le rang modulo 7 (de Q = A − 3I + 3J, ou de A − 3I), dans un sens comme dans l'autre,
doit contrôler **G**, la matrice des arêtes génériques de Γ₂(x). Ces arêtes relient des paires dont les classes sont
disjointes. Rien d'autre n'est disponible, et changer de sommet de base n'apporte rien de plus.

## (a) Colonnes connues : rang 14, déjà atteint par la boule du sommet (calcul exact)
Dans les coordonnées de x, les seules colonnes connues pour toutes les lignes sont celles de B₁(x) (15 colonnes) : un
sommet {c, d} de Γ₂(x) y est adjacent exactement à c et d. Sur ces 15 colonnes :
- rang₇ de Q sur B₁(x) × B₁(x) (moulin à 7 pales) = **14** ;
- rang₇ des 99 lignes restreintes à ces colonnes = **14**.
Toute relation « lignes extérieures dans l'espace des lignes d'une boule », restreinte là, est donc automatiquement
satisfaite. Script : `code/g_reduction_known_columns.py`.

## (b) Un bloc sans entrée inconnue a au plus 39 sommets (preuve)
Deux sommets de Γ₂(x) ne peuvent porter une arête générique que si leurs paires de classes sont disjointes (00_FONDATIONS F3 ;
notes/40). Un bloc sans entrée inconnue correspond donc à une famille de paires de classes (parmi 7) deux à deux
sécantes. Une telle famille est une étoile ou un triangle (EKR pour k = 2). L'étoile d'une classe donne au plus 6 × 4 = 24
sommets de Γ₂(x), plus les 15 de B₁(x), soit 39 : c'est la boule de droite de notes/99, de rang Q ≤ 37. Aucun bloc
connu ne peut atteindre 42 ou 43, et aucun bloc connu n'a assez de colonnes pour contraindre le reste.

## (c) Changer de carte n'ajoute pas d'information au-delà de (τ, G) (preuve)
Pour a ∈ N(x), les coordonnées dans la carte de a d'un sommet v ∈ Γ₂(x) ∩ Γ₂(a) sont ses deux voisins dans N(a) =
{x, ā} ∪ étoile(a). Ses voisins dans étoile(a) sont soit étiquetés (donnés par τ), soit génériques (entrées de G). Le
passage d'une carte à l'autre est donc fonction de τ et de G : un argument « à deux cartes » est un argument sur G.

## Conséquence
Avec notes/102 §9 (tout est cohérent localement pour chaque k pair ≤ 28), une contradiction 7-adique demande une
propriété **globale** de G. Les seules contraintes connues sur G sont : ses degrés par étiquette (fixés par la torsion),
le spectre réel de H = T + G (12, (−2)⁶, 0⁷, 3⁴⁰, (−4)³⁰), et rang₇ M_x = k ≤ 28. Aucune n'est encore exploitée
globalement. Le « retournement » du critère de notes/102 est **vide sans G**.
