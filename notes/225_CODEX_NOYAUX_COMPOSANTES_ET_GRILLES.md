# 225 — Relier les 174 noyaux aux composantes et aux grilles

9 octobre 2026. Exploration issue du message LAB 422. Aucune hypothèse
de rang modulo sept ; utilisation du catalogue et des résultats disponibles.

**Nouvelle réduction conditionnelle.** Si chaque triangle d'un candidat C1
appartient à au moins une grille, les 174 types de noyaux se réduisent à
**115**. Si chaque triangle appartient à au moins deux, trois ou quatre
grilles, il reste respectivement **52, 11 ou 2 types**.

Le mécanisme est un lemme de regroupement des composantes : une petite
partie visible du graphe proche impose la taille de ses composantes
complètes. Les comptes ci-dessous portent sur les deux lectures possibles
du motif, car les symétries du catalogue peuvent échanger ses triangles.
Ils n'excluent aucun noyau supplémentaire sans l'hypothèse indiquée.

## 1. Équilibre des composantes, utilisé comme acquis

Soit T un triangle, G=G(T) le graphe cubique sur ses 36 voisins proches,
et N la matrice d'incidence des 60 sommets lointains sur ces points.
Chaque sommet lointain a exactement six voisins proches, deux par couche.
On utilise l'identité réelle déjà disponible dans le corpus :

    NNᵀ=K=12I−G−G²+2J−diag(J₁₂,J₁₂,J₁₂).

Chaque composante C de G rencontre également les trois couches, car
les arêtes transversales entre deux couches sont des couplages parfaits.
Le vecteur z=1_C−(|C|/36)1 vérifie Kz=0 : les termes 12I−G−G²
annulent les constantes par composante, et les deux termes en J se
compensent. La positivité réelle donne Nᵀz=0. Ainsi, pour tout lointain f,

    |N(f)∩C| = |C|/6.                                  (1)

En particulier chaque composante rencontre l'ombre N(f)∩N(T), et sa
taille vaut six fois le nombre de points de cette ombre qu'elle contient.
Cette identité ne dépend pas du rang modulo sept.

## 2. Lemme de regroupement des composantes visibles

Prenons un motif S de la note 221 : T=012, second triangle 345,
arêtes transversales 03 et 14. Le point f=5 est lointain de T.
Dans le noyau H de 14 sommets, les dix points proches sont

    J : 3,4,6,7,8,9,10,11,12,13.

Ils contiennent **toute l'ombre de f**, soit

    Ω={3,4,10,11,12,13}.

Notons J₁,…,J_s les composantes du sous-graphe induit sur ces dix
points, et q_i=|J_i∩Ω|. Les quatre points hors de Ω sont déjà reliés
à 3 ou 4 par les arêtes imposées du noyau. Chaque q_i est donc positif,
et leur somme vaut six.

**Lemme.** Le profil des tailles des composantes complètes de G(T)
est obtenu en regroupant les q_i, puis en multipliant chaque somme
par six.

**Preuve.** Une composante visible J_i ne peut se scinder dans G(T).
Plusieurs J_i peuvent se rejoindre via les sommets encore inconnus.
Réciproquement aucune composante complète n'est invisible : par (1)
elle rencontre Ω, entièrement contenu dans J. Les composantes complètes
correspondent donc à une partition de {J₁,…,J_s}. La formule (1) donne
leur taille. ∎

Exemples :

| Poids visibles q_i | Tailles de composantes encore possibles |
|---|---|
| (6) | (36) : connexité forcée |
| (5,1) | (36) ou (30,6) |
| (4,2) | (36) ou (24,12) |
| (2,2,2) | (36), (24,12) ou (12,12,12) |

Ces profils sont des conditions nécessaires. Leur présence dans la
liste ne prouve pas qu'ils admettent un prolongement.

## 3. Borne sur les grilles passant par T

Une grille passant par T fournit une composante prisme de six points
dans G(T) : ses six autres sommets y ont déjà leur degré cubique complet.
Réciproquement une composante de six points est un prisme : les deux
formes cubiques possibles avec deux points par couche sont le prisme
et K₃,₃ ; la seconde contredit μ=2. Ajouter T au prisme donne la grille.

Le nombre g(T) de grilles passant par T est donc exactement le nombre
de composantes de taille six de G(T). D'après le lemme, chacune provient
d'un q_i=1 laissé seul dans le regroupement. Ainsi

    g(T) ≤ #{i : q_i=1}.                                (2)

Ici ces composantes visibles de poids un sont des sommets isolés parmi
les quatre points de Ω autres que 3 et 4. Une grille peut être en
grande partie hors de H : c'est (1)–(2) qui l'interdit lorsque la borne
est zéro, pas la simple absence d'un prisme visible dans H.

On applique le même lemme à T′=345 et f′=2. Il faut conserver les deux
lectures, puisque la normalisation des 174 types autorise T↔T′.

## 4. Réductions obtenues sur le catalogue

Les deux bornes (2), considérées comme une paire non ordonnée, donnent :

| Bornes sur g(T),g(T′), à échange près | Types |
|---|---:|
| (0,0) | 20 |
| (0,1) | 33 |
| (0,2) | 6 |
| (1,1) | 33 |
| (1,2) | 24 |
| (1,3) | 6 |
| (2,2) | 27 |
| (2,3) | 11 |
| (2,4) | 3 |
| (3,3) | 8 |
| (3,4) | 1 |
| (4,4) | 2 |

Donc 20 types imposent l'absence de grille sur les deux triangles,
et 59 sur au moins l'un. Par ailleurs, 19 types imposent la connexité
du graphe proche d'au moins l'un des deux triangles, dont deux pour
les deux triangles.

**Corollaire de réduction.** Sous l'hypothèse que chaque triangle du
graphe appartient à au moins q grilles, chaque motif obligatoire S
doit avoir ses deux bornes au moins égales à q. La couverture devient :

| Hypothèse globale | Types possibles |
|---|---:|
| Aucune borne inférieure sur g(T) | 174 |
| g(T)≥1 pour tout triangle T | 115 |
| g(T)≥2 pour tout triangle T | 52 |
| g(T)≥3 pour tout triangle T | 11 |
| g(T)≥4 pour tout triangle T | 2 |
| g(T)≥5 pour tout triangle T | 0 |

La dernière ligne, jointe à l'existence d'un motif S, implique qu'un
candidat possède un triangle dans au plus quatre grilles. Les autres
lignes réduisent des sous-cas ; elles ne supposent pas que l'une de
ces hypothèses globales soit vraie dans tout candidat.

Les deux types du sous-cas q=4 ont pour identifiants `bits=0` et
`bits=1` : respectivement aucune arête dans D, ou la seule arête
optionnelle (6,7). Ce sont deux cibles concrètes pour chercher une
obstruction supplémentaire ; aucun de leurs prolongements n'est exclu ici.

## 5. Exploitation et fichiers

Le lien avec LAP est désormais explicite : son résultat sur la connexité
et les profils déconnectés peut être appliqué aux profils nécessaires
produits par le lemme, en conservant ses hypothèses de rang et de cycles.
Les restrictions sur les grilles obtenues ici sont, elles, sans rang.
Pour une étude où les triangles sont tous couverts par des grilles, les
59 types interdits par cette hypothèse ne doivent plus être explorés.

- Programme : `code/codex/core_component_profiles.py`.
- Profils, bornes pour les deux triangles et listes des types de chaque
  sous-cas : `data/codex_core_component_profiles.json`.
- Calcul direct :

      python code/codex/core_component_profiles.py --out data/codex_core_component_profiles.json

Il s'agit d'une lecture combinatoire des noyaux avec un lemme de
réduction nouveau appliqué à ces données, sans nouvelle campagne de
vérification ni recherche de prolongements. L'équilibre réel (1) est
un acquis utilisé, pas un résultat annoncé comme redémontré pour la
première fois.
