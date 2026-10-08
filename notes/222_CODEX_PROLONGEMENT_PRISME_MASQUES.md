# 222 — Les incidences extérieures réduisent la couverture à 174 noyaux

9 octobre 2026. Suite des notes 220–221, sans hypothèse de rang modulo sept.

**Résultat.** Parmi les 310 noyaux de 14 sommets conservés par la note 221,
136 ne peuvent recevoir les incidences nécessaires de leurs 85 sommets
extérieurs. Chaque exclusion possède un certificat entier vérifié.
Il reste donc **174 noyaux** dont les prolongements couvrent tout C1.
Ces noyaux ne sont ni 174 graphes complets, ni 174 calculs de difficulté
connue. La faisabilité d'une relaxation ne construit aucun graphe.

## 1. Masques admissibles d'un sommet extérieur

On conserve la notation H=S∪D de la note 221, avec |S|=6 et |D|=8,
et A la matrice d'adjacence de H. Tous les sommets ayant deux voisins
dans S sont déjà dans D. Un sommet extérieur à H a donc un masque
b∈{0,1}¹⁴ avec zéro ou un voisin dans S. Il existe au plus 7·2⁸=1792
masques candidats.

Trois conditions nécessaires filtrent ces masques :

1. Pour tout u∈H, (Ab)_u≤2−b_u : les voisins communs déjà présents
   entre u et le sommet extérieur respectent λ=1 et μ=2.
2. Si δ_uv=2−A_uv−(A²)_uv=0, alors b_u b_v=0 : une paire déjà
   saturée ne peut recevoir un voisin commun supplémentaire.
3. Les deux matrices de projecteur sur H plus ce sommet sont
   positives semi-définies. Leurs blocs sont

       [ Q₋       1−9b ]            [ Q₊       11b−2 ]
       [ (1−9b)ᵀ    28 ],           [ (11b−2)ᵀ     42 ],

   où Q₋=27I−9A+J et Q₊=44I+11A−2J, déjà positifs par la note 221.

Le troisième test utilise un complément de Schur exact. Pour une matrice
Q singulière, on choisit une sous-matrice principale inversible B=Q[I,I]
de taille rang(Q). Pour le vecteur transversal c et la diagonale d,
les conditions sont

    Q[:,I] B⁻¹ c[I] = c,       c[I]ᵀ B⁻¹ c[I] ≤ d.

La première impose c∈image(Q). Les inverses sont rationnelles ; multiplier
par un dénominateur commun positif transforme ces tests en égalités et
inégalités entières. Aucune tolérance numérique n'élimine un masque.
Après ces filtres, le nombre de masques varie de 2 à 310 selon le noyau.

## 2. Compatibilité simultanée des 85 sommets

À chaque masque conservé b_j on associe une multiplicité x_j. Un vrai
prolongement fournit nécessairement des entiers non négatifs vérifiant

    Σ_j x_j = 85,
    Σ_j x_j (b_j)_u = 14−deg_H(u),                         u∈H,
    Σ_j x_j (b_j)_u (b_j)_v = 2−A_uv−(A²)_uv,             u<v dans H.

Cela donne un système Mx=r de 106 lignes (1+14+91). On impose aussi
0≤x_j≤U_j, où U_j est l'effectif total de sa classe relative à S :
33 pour un masque vide sur S, et 9,9,8,9,9,8 pour un masque simple.
La note 221 prouve ces effectifs. Plusieurs masques appartenant à une
même classe n'autorisent donc pas une borne supérieure plus grande.

Le pilote teste la relaxation réelle de ce système. Son impossibilité
exclut tout prolongement du noyau, tandis que sa faisabilité laisse
notamment ouverts l'intégralité des multiplicités et le placement des
arêtes entre les 85 sommets extérieurs.

## 3. Certificats d'impossibilité en entiers

Un solveur flottant propose un vecteur de multiplicateurs y. Seule la
vérification entière suivante est utilisée pour prononcer l'exclusion.
Avec c=yᵀM, toute solution respectant les bornes devrait satisfaire

    yᵀr = c x ≥ L := Σ_j min(0,c_j U_j).

Un vecteur **entier** y tel que L>yᵀr est donc un certificat de
contradiction. Le fichier de résultats contient y, L et yᵀr pour chaque
noyau exclu ; le vérificateur reconstruit M, r et U et recalcule tout en
entiers Python. L'inégalité stricte est obligatoire. Le résultat du
solveur seul ne vaut pas certificat.

Exemple archivé : noyau de code 649, 131 masques avant le test spectral,
109 après. Son certificat donne L=0 et yᵀr=−3. Les 106 multiplicateurs
complets figurent dans le fichier JSON.

## 4. Résultats et contrôles

| Étape | Types exclus à cette étape | Types conservés |
|---|---:|---:|
| Catalogue obligatoire de la note 221 | — | 373 |
| Projecteurs réels sur H | 63 | 310 |
| Incidences simultanées des sommets extérieurs | 136 | 174 |

Le pilote a parcouru les 310 entrées en environ 22,4 secondes sur la
machine de travail. Aucun statut inconnu ni impossibilité numérique
sans certificat n'est compté comme exclusion. Les 174 autres entrées
sont déclarées « LP feasible, unresolved » ; aucune existence exacte
de leur relaxation n'est nécessaire à l'argument de couverture.

Le contrôle positif utilise le vrai graphe tordu à 243 sommets de la
note 221 et son noyau témoin. Avec k=22, les projecteurs à employer sont

    Q₋=108I−27A+2J,    c=2−27b,    d=110,
    Q₊=45I+9A−J,       c=9b−1,     d=44.

Le filtre conserve 310 masques, dont 71 sont utilisés par les **229 vrais
sommets extérieurs**. Aucun de ces sommets n'est rejeté et leurs
multiplicités entières satisfont exactement toutes les équations et
bornes du modèle. Ce contrôle ne demande pas au graphe à 243 sommets de
satisfaire les contraintes spectrales spécifiques à 99.

La relecture des 136 certificats, de la couverture des 310 entrées et
du contrôle positif a réussi. Un certificat dont les multiplicateurs
ont été remplacés par zéro est rejeté.

## 5. Reproduction et portée

- Programme : `code/codex/twisted_prism_extension.py`.
- Entrées : `data/codex_twisted_prism_core.json`.
- Sortie et certificats : `data/codex_twisted_prism_extension.json`.
- Relecture exacte :

      python code/codex/twisted_prism_extension.py --out data/codex_twisted_prism_extension.json --verify-only

- Régénération du pilote, borné à 180 secondes entre noyaux :

      python code/codex/twisted_prism_extension.py --out data/codex_twisted_prism_extension.json --seconds 180

La borne de temps n'interrompt pas un noyau en cours. La couverture du
calcul est explicitement enregistrée dans le résultat ; une exécution
partielle ne doit pas être présentée comme le traitement des 310 noyaux.

L'implication acquise est : **tout SRG(99,14,1,2) contient, autour d'un
motif obligatoire S, l'un des 174 noyaux conservés**. Exclure tous leurs
prolongements suffirait donc pour C1, tous rangs confondus. Le gain
373→174 mesure une réduction de cette couverture, pas un pourcentage de
preuve et pas un coût prévisible pour la suite. Le prochain obstacle est
la réalisation compatible des incidences et des voisins communs entre
les sommets extérieurs. LAB examine un pilote de fermeture bornée sur
ces survivants ; aucune fermeture non encore obtenue n'est revendiquée.
