# 218 — Un motif forcé par les coordonnées unitaires d'une étoile

8 octobre 2026. Suite à l'observation O3 de LAB, message 394,
note 17.62. **Résultat général : en l'absence de cycle de longueur
quatre passant par le centre proche, une étoile complète impose
un couple (apex, autre ombre) qui utilise au moins deux coordonnées
unitaires résiduelles.** Le comptage ne fait pas intervenir Green.
LAB a relu et confirmé sa preuve dans le message 396.

Ce résultat isole un motif à exclure dans la piste C1. Il ne prouve
pas encore cette exclusion. Le présent travail ne concerne pas le
lemme T20 de C2.

## 1. Les vraies multiplicités hors de la couche du centre

Conservons le graphe proche G sur 36 points, trois couches de 12,
avec exactement un voisin dans chaque couche, et

    K = 12I − G − G² + 2J − B.

Soit v un point proche et O l'ensemble des 24 points hors de sa
couche. On suppose G sans triangle et (G²)_pv≤2 pour p∈O, condition
nécessaire à une complétion : K_pv est une multiplicité non négative.
Posons

    z = #{p∈O : (G²)_pv=2}.

Les deux voisins transversaux de v ont K_pv=1. Les six chemins
de longueur deux qui ne reviennent pas à v finissent dans O ;
ils donnent 6−2z extrémités simples et z extrémités doubles.
Les voisins directs ne peuvent être parmi ces extrémités, par
l'absence de triangle. Par conséquent

    #{K_pv=0}=z,    #{K_pv=1}=8−2z,    #{K_pv=2}=16+z.     (1)

En particulier, le profil 8/16 exige **z=0**, c'est-à-dire aucun
cycle de longueur quatre passant par v. L'absence de tels cycles
sur une seule arête incidente à v ne suffit pas.

### Correction des exemples utilisés

| Graphe | Centre | K=0 | K=1 | K=2 |
|---|---:|---:|---:|---:|
| Boule 5 | 0 ou 12 | 1 | 6 | 17 |
| Boule 9 | 0 ou 12 | 1 | 6 | 17 |
| Boule 12 | 0 | 0 | 8 | 16 |
| Boule 12 | 12 | 1 | 6 | 17 |
| Cyclique (2,4,1) | 0 ou 12 | 0 | 8 | 16 |

Ainsi, les deux centres de la boule 12 n'ont pas le même profil.
L'affirmation « huit points simples, déduits des sommes seules donc
général » du message 394 était trop large. LAB l'a corrigée après
le contrôle ci-dessus.

## 2. Une étoile comme système d'incidences

Une étoile S_v contient dix ombres n. Chacune contient v, un autre
point de sa couche, et quatre points dans O. Ses sommes sont

    Σ_{n∈S_v} n = K e_v.

Écrivons

    P = {p∈O : K_pv=1},    Q = {p∈O : K_pv=2},
    a(n) = |n∩P|.

Les points de P sont couverts une seule fois ; les ensembles
n∩P sont donc disjoints et Σa(n)=8−2z. Les points de Q sont
couverts deux fois. Les points de multiplicité zéro sont absents.

Les deux voisins transversaux u₁,u₂ de v appartiennent à P.
Chacun est contenu dans une unique ombre w_i de S_v. Ces deux
ombres sont distinctes : la contrainte unaire

    (G n)_v ≤ 2−n(v)=1

interdit à une ombre de contenir u₁ et u₂ simultanément. Ce sont
les deux apices, et a(w_i)≥1. Aucun argument modulo sept n'est
utilisé pour les identifier.

Pour un apex w, la cible résiduelle est t_w=K e_v−w. Posons

    P_w = {p∈O : t_w(p)=1},
    d_w(n)=|n∩P_w|   pour n≠w.

Les identités exactes sont

    |P_w| = (8−2z−a(w)) + (4−a(w))
          = 12−2z−2a(w),                              (2)
    Σ_{n≠w} d_w(n) = |P_w|,                          (3)
    d_w(n) = a(n) + |n∩w∩Q| ≥ a(n).                 (4)

Dans (4), aucun point de n∩P ne peut appartenir à w, car P est
couvert une seule fois.

## 3. Lemme général du couple forcé, z=0

**Lemme.** Toute étoile complète avec z=0 contient un de ses deux
apices w et une autre ombre n tels que d_w(n)≥2.

**Preuve.** Supposons d_w(n)≤1 pour chaque apex w et chaque n≠w.
L'application de (4) à w₁,w₂ dans les deux ordres donne
a(w₁)=a(w₂)=1. Mais (2) donne alors |P_w|=10 et (3) demande de
couvrir ces dix incidences unitaires par neuf ombres, chacune
en portant au plus une. Contradiction. ∎

Une formulation constructive du même argument distingue seulement
trois cas : si a(w₁)=1, le couple existe en conditionnant par w₁ ;
sinon, si a(w₂)=1, il existe en conditionnant par w₂ ; sinon,
d_w₁(w₂)≥a(w₂)≥2. Les seize possibilités a(w_i)∈{1,2,3,4}
sont couvertes par ces trois cas. Des contraintes unaires plus
fortes peuvent restreindre ces valeurs ; elles ne sont pas requises.

### Deux motifs concrets à exclure

Un apex w est isolé dans l'étoile. Pour une autre ombre n, w et n
sont non adjacents dans le graphe lointain et ont au plus deux
points proches communs. L'un est déjà v ; ainsi

    |n∩w∩Q|≤1.

Le couple forcé appartient donc à l'un des deux types :

- **A :** n contient au moins deux points de P ;
- **B :** n contient un point de P et partage avec w un point x∈Q.

Le partage de deux points de Q avec w est impossible. Dans B,
n∩w={v,x} et K_vx=2 : w et n sont exactement les deux ombres
communes aux étoiles de v et de x. En outre G_vx=(G²)_vx=0,
puisque x est hors couche et K_vx=2.

On peut voir directement pourquoi A ou B est inévitable. Si A
est absent, huit ombres ont a=1 et deux ont a=0. Un apex a=1
porte trois points de Q. Chacun doit être couvert par une autre
ombre, et ces trois autres ombres sont distinctes, par la borne
d'intersection avec l'apex. Il n'existe que deux ombres avec a=0 :
au moins l'une des trois a=1, donnant B.

**Conséquence conditionnelle précise.** Prouver l'impossibilité
des motifs A et B dans toutes les étoiles admissibles du secteur
C1 considéré suffirait à exclure ce secteur sous z=0. Le lemme
présent prouve leur apparition forcée, pas leur impossibilité.
Les tables de Green au rang 37 sont une contrainte disponible
pour cette seconde étape, mais ne sont pas employées ici.

## 4. Pourquoi les deux restrictions du lemme comptent

Le script joint construit deux matrices d'incidence **abstraites**
10×24, chaque ligne de poids quatre. Elles ne satisfont pas un
graphe G ou des contraintes de Green imposés et ne sont pas des
exemples de graphes C1.

1. Avec z=1, six colonnes ont somme un, dix-sept somme deux et
   une somme zéro. Les deux lignes distinguées portent chacune
   un point de multiplicité un, mais d_w(n)≤1 dans les deux sens
   et pour toutes les autres lignes. Le seul comptage ne force
   donc plus le motif lorsque z=1.
2. Avec z=0, huit colonnes ont somme un et seize somme deux. Une
   ligne distinguée a=2 vérifie d_w(n)≤1 pour toutes les autres,
   tandis que l'autre, avec a=1, impose d_w(n)≥2 pour au moins
   une ligne. Le comptage n'impose donc pas le motif après le
   choix arbitraire d'un seul apex fixé d'avance.

Les matrices complètes et leurs cibles résiduelles sont archivées.

## 5. Ce que l'observation numérique ne prouve pas

Les 38518 feuilles de la note 216 sont toutes réfutées. Les
reclasser par d_w(n) ne fournit aucun groupe de survivants auquel
les comparer.

Un exemple de LAB montre de plus que d_w(n)≥2 n'impose pas une
contradiction par la propagation simple. Sur la boule 12, centre 0 :

    apex 187 : w = {0,7,12,16,32,34},
    variable 0, candidat 17 : n = {0,1,15,18,26,29},
    n∩P_w = {18,29}.

En mode Green interne sans aucune table entre étoiles, fixer n
laisse un point fixe non vide. Les neuf domaines de l'étoile de 0
ont les tailles

    1, 8, 10, 6, 10, 10, 6, 8, 9.

Cette survie n'est pas une solution entière. En fixant ensuite
la variable 3, ses six candidats sont tous réfutés par propagation.
Les six traces sont archivées et vérifiées sur les indices
originaux ; leurs suppressions et contradictions restent toutes
dans l'étoile de 0. Cela invalide la règle algorithmique en un
choix, sans invalider la cible mathématique d'impossibilité.

## 6. Un contrôle exact à trois ombres

LAB a proposé un triplet qui passe ses tests flottants. Son
contrôle rationnel exact donne :

    w₁ = {0,1,12,13,26,35},
    w₂ = {0,2,18,21,24,25},
    n  = {0,7,22,23,29,32}.

Sur la boule 12, centre 0, ces ombres appartiennent aux pools
unaires, ont norme de Green 6, produits mutuels 3 et respectent
les sommes partielles ainsi que N_partiel N_partielᵀ≤K. Les
premières sont les deux apices et n porte le motif forcé.

Avec les trois adjacences nulles, le Gram réel de la note 215 est

    Σ₃ = 3I₃ + J₃/12 − N₃ᵀ H⁺ N₃.

Ses sept mineurs principaux sont strictement positifs en
arithmétique rationnelle ; notamment

    det Σ₃ = 3511203878 / 216957183411 > 0.

Les valeurs exactes sont archivées. Cela montre qu'on ne peut pas
exclure le motif à partir de ces seuls filtres sur trois ombres.
Aucune complétion en étoile entière n'est affirmée.

## 7. Artefacts et prochaine cible

- `code/codex/star_singleton_counting.py` : profils exacts, deux
  exemples abstraits, contrôle du cas 187, et triplet rationnel ;
- `data/codex_star_singleton_counting.json` : résultats et matrices ;
- `data/codex_singleton_hard_leaf187.json` : graphe, choix et traces
  de la réfutation en six feuilles après le premier point fixe.

Rejeu :

    python code/codex/star_singleton_counting.py --out data/codex_star_singleton_counting.json --verify-only

Le programme vérifie les identités de cible sur tous les apex des
quatre graphes de contrôle, puis les contrôles positifs explicites.
Il ne prétend pas vérifier par énumération tous les graphes G :
la preuve générale est le comptage des §§1–3.

La cible suivante est l'incompatibilité des motifs A et B avec
l'étoile complète, sous les hypothèses appropriées de C1. Le motif
B désigne notamment un couplage à deux ombres communes entre les
étoiles de v et x, différent du couplage à un apex des notes 209–216.
Ce lien mérite d'être étudié ; son impossibilité reste à démontrer.
