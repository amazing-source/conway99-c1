# 231 — Fixer le signe résiduel ; fermer la liste des identités de traces

9 octobre 2026. Conséquences du message LAB 447, transmises par Codex 448.

**Réduction utilisable.** Le discriminant résiduel proposé par LAB se
déduit de la complétion de Witt. Il dépend du graphe proche et de la
dimension des relations vraies, pas du sous-espace de relations choisi
à dimension fixée. Un mauvais signe en dimension résiduelle zéro
interdit donc toutes les branches de cette dimension. En dimension
résiduelle positive, une seule classe de forme quadratique est possible.

**Deuxième conséquence.** Dans le modèle sans torsion de la note 230,
les identités de traces de tous les ordres découlent déjà des moments
NNᵀ=K. Cela généralise l'observation de LAB sur les ordres deux et trois
et évite de chercher séparément les identités suivantes.

Aucun nouveau décompte de boules exclues n'est annoncé. Aucune recherche
d'étoiles, aucun échantillonnage et aucun ancien audit ne sont rejoués.
La forme globale utilisée est l'acquis de la note 102, pas un nouveau lemme.

## 1. Notations et décomposition

Toutes les formes de cette section sont sur F₇. Soit r le rang global
de A−3I, et V le quotient non dégénéré de la forme Q=A−3I+3J. On a

    dim V=r−1,
    χ(disc V)=−1 pour r=37,41 ; +1 pour r=39,43.

Pour les 36 points proches d'un triangle, le Gram est M₀=3J−H,
avec H=3I−G. Notons p:F₇³⁶→V l'application envoyant les coordonnées
sur leurs vecteurs proches, et

    R₀=ker M₀,       d=dim R₀,
    Tr=ker p,        b=dim Tr,
    d₀=disc de la partie non dégénérée de M₀.

On a Tr⊆R₀. Le sous-espace W=im p possède donc

    dim W=36−b,       dim rad W=d−b=:a,
    W/rad W ≃ (F₇³⁶/R₀, M₀), de dimension 36−d.

Prenons un complément non dégénéré W₀ du radical dans W. Puisque V
est non dégénéré et de caractéristique impaire, chaque direction du
radical peut être complétée par une direction duale isotrope. Les a
plans ainsi obtenus sont hyperboliques. Par orthogonalisation,

    V ≃ W₀ ⊥ H_hyp^a ⊥ R.

Chaque plan hyperbolique a discriminant −1. Il vient

    D := dim R = r−37+2b−d,
    disc R = disc(V) d₀ (−1)^(d−b) modulo les carrés.    (1)

Le quotient et le produit ont ici la même classe, car une classe de
F₇*/(F₇*)² est son propre inverse. Ceci prouve la formule B′ de LAB
au rang 37 et la donne aux autres rangs de la fenêtre.

## 2. Éliminer des branches avant la recherche

La dimension D<0 est impossible. Pour D=0, le discriminant de l'espace
nul vaut un : le membre droit de (1) doit être un carré. S'il ne l'est
pas, **tous** les sous-espaces Tr de dimension b sont impossibles. Ce
test ne requiert pas d'énumérer leurs orientations dans R₀.

Si b était la dimension minimale autorisée par D≥0, il doit donc
augmenter d'au moins un, ce qui augmente D de deux. À ce premier
relèvement, la classe de (1) change de signe : sur F₇, le plan résiduel
obtenu a discriminant carré, donc il est anisotrope. Si une autre borne
prouvée interdit d'augmenter b, toute la boule est alors exclue.

Pour D=1, une seule classe de norme scalaire c₀ est permise : celle
du membre droit de (1). Pour D=2, une seule des classes représentées
par diag(1,1) et diag(1,3) est permise. Plus généralement, la dimension
et le discriminant fixent la classe d'isométrie d'une forme non dégénérée
sur F₇ : il n'y a jamais deux signes résiduels à essayer pour le même
couple (d,b).

Au rang 37, pour la plus petite dimension b permise par D≥0 :

| d | b minimal | D | Restriction |
|---:|---:|---:|---|
| 0 | 0 | 0 | d₀ doit être non carré : L23 |
| 1 | 1 | 1 | c₀ a la classe de 3d₀ |
| 2 | 1 | 0 | d₀ doit être carré ; sinon b≥2 |
| 3 | 2 | 1 | c₀ a la classe de d₀ |
| 4 | 2 | 0 | d₀ doit être non carré ; sinon b≥3 |

Ici trois représente la classe non carrée globale. Dans un cas avec
deux composantes sans torsion, d=1, b=1 et d₀ a la classe de 3τ₁τ₂ ;
on retrouve c₀ de classe τ₁τ₂ (note 230, §7).

Les anciens balayages qui essayaient les deux classes traitaient un
sur-ensemble. Le filtre ne les invalide pas et n'impose pas de les
rejouer. Aucun effectif de branches supprimées n'a été calculé ici.

## 3. Une identité pour tous les moments dans le cas sans torsion

Reprenons exactement les hypothèses de la note 230, en particulier
rang₇ H=35 et NNᵀ=K. Posons

    W=M⁻¹=5J−H⁺,       γ=NᵀWN.

Avec les produits de Green prescrits, γ a diagonale six et entrées
hors diagonale 2+F_fg ; donc γ=4I+2J+F dans F₇. Il s'agit de la
convention utilisée pour γ dans le message LAB 447, distincte du
Gram NᵀH⁺N de diagonale six et hors diagonale 3−F_fg.

Soit E l'espace des vecteurs de somme nulle dans chacune des trois
couches, de dimension 33. Son complément est l'espace S des trois
indicatrices de couches ; S est non dégénéré pour le produit standard
car chaque couche a taille 12≠0 modulo sept.

Sur E, J et B s'annulent. On a donc

    K|E=−H²|E,       W|E=−(H|E)⁻¹,       WK|E=H|E.

Sur S, WK a valeur propre six sur la constante totale, et zéro sur
les deux différences de couches. L'identité de déterminants pour les
produits de matrices rectangulaires donne alors

    χ_γ(x)=x²⁴ χ_WK(x)
          =x²⁶(x−6) χ_(H|E)(x).                         (2)

En particulier, pour **tout** k≥1,

    tr(γ^k)=6^k+tr((H|E)^k),                 dans F₇.    (3)

Ces relations ne demandent pas une nouvelle preuve ordre par ordre.
Les identités des ordres deux et trois rapportées par LAB — congruence
du nombre d'arêtes lointaines, puis du nombre de triangles — en sont
des cas particuliers. Toute sélection complète qui satisfait déjà
NNᵀ=K satisfait automatiquement (2)–(3).

Cela ne rend pas ces identités inutiles dans une relaxation qui omet
une partie des contraintes d'incidence. En revanche, les réintroduire
dans la sélection complète de la note 230 ne la resserre pas. Une
borne nouvelle sur son coût doit exploiter une autre restriction,
par exemple la binarité ou une impossibilité de coexistence de supports.

## 4. Portée et état transmis

LAB rapporte 150 exemples connexes éliminés chez LAP, dont 120 sans
torsion et 30 de torsion un. Il s'agit d'un échantillon ; le cas connexe
n'est pas clos. Une partie des 120 était déjà exclue par L23.

Les progrès partiels rapportés sur (2,3) et sur les reprises de torsion
trois et quatre ne sont pas des clôtures de leurs séries. Les résultats
retirés au message 443 ne sont pas rétablis par l'absence de survivant
dans les premières parties relancées.
