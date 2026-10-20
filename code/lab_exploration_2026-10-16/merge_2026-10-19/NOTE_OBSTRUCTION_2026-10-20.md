# D'où vient l'obstruction au rang 37 ? Valeurs de Green, étoile, alternatives

LAB, 20/10/2026.

**Question de l'utilisateur.** « Est-ce que les valeurs de Green sont le seul moyen de trouver l'obstruction ? Si oui,
cherchez-la ; si non, cherchez-la quand même et cherchez des alternatives. »

**Statuts.**
- **P** : preuve écrite ici, non relue.
- **E** : calcul exact, mais sans certificat exporté.
- **A** : déjà dans l'archive.

---

## 0. Réponse courte

### 0.1 Pour une droite générique, Green est toute l'information 7-adique

La condition de rang 37 équivaut aux valeurs de Green (Prop. 1 du prompt Core37). Elle équivaut aussi à :
- **le projecteur lointain réel Π_T est 7-entier** (§1, P) ;
- L23 (A) est la seule condition 7-adique qui porte sur G_T seul. Les traces et les polynômes caractéristiques sont automatiquement compatibles (§1, P).

### 0.2 Green ne suffit pas seul

Au niveau de l'étoile d'un sommet proche x :

| contraintes conservées | verdict |
|---|---|
| Green et couplage λ = 1 en x | l'étoile meurt |
| Green sans couplage | non conclu en 60 s (pas de verdict) |
| combinatoire sans les valeurs de Green | satisfaisable en 128 nœuds |

L'obstruction est donc **Green × couplage**.

### 0.3 La mort est statistique, pas structurelle (E)

- Sur l'étoile, les valeurs de Green sont uniformément réparties sur F₇ (1/7 chacune, à 10⁻³ près).
- Les comptes exacts de 3-uplets et de 4-uplets compatibles valent le modèle « événements indépendants » à 1 % près.
- Les noyaux minimaux ont 7 lointains. C'est exactement le seuil où l'espérance heuristique du nombre de solutions passe sous 1.

**Conséquence.** On ne doit pas s'attendre à un petit lemme structurel. Une preuve uniforme de (a′) demanderait un
énoncé de pseudo-aléa des fonctions de Green mod 7 valable pour **tout** G. Hors de portée aujourd'hui.

### 0.4 Alternatives examinées

- **Projecteur réel 7Π_T** (indépendant du rang) :
  - filtre très fort sur les configurations partielles ;
  - équivalent aux comptes locaux exacts sur une droite complète ;
  - pas d'obstruction bon marché indépendante du rang (§3).
- **Ordre 2 en 7** (Π mod 7 idempotent de rang 8, de type moins) et **couplage par les droites latérales** (L23 pour
  G_{T_x}) : filtres nouveaux, non testés (§4).
- **Traces, autres premiers, séries thêta** : automatiques, sans effet, ou épuisés (§1, A).

---

## 1. Faits exacts (P)

### 1.1 Forme unifiée réel / 7-adique

Notations :
- Z = {vecteurs de somme nulle dans chaque classe} (dimension 33) ;
- f_W = e_W − (1/6)𝟏 ∈ Z ;
- Γ_R = ((3I − G)|_Z)⁻¹ sur ℝ, c'est la fonction de Green réelle.

**Calcul de K⁺.** K = EEᵀ vaut 60 sur 𝟏, 0 sur les différences de classes, et (3I − G)(4I + G) sur Z. Donc :

    7Π_T(W, W') = 3δ − R(W, W') + 1/12 − f_Wᵀ Γ_R f_W'          (toute droite, tout rang ; Théorème 1 réécrit).

**Réduction mod 7.** Si 7 ∤ τ, alors Γ_R est 7-entier, et Γ_R mod 7 = Ω|_Z. Comme 12⁻¹ ≡ 3 (mod 7), on obtient
7Π_T ≡ 3δ − R + 3 − f_WᵀΩf_W' (mod 7). L'égalité 7Π_T ≡ 0 est exactement la forme de Green.

**Conséquences, pour une droite générique :**
- rang 37 ⟺ Π_T est 7-entier ;
- en général, rang₇(7Π_T mod 7) = ρ(T) = r − 37 (déjà énoncé sous forme de congruence, NOTE_FUSION §5(b)).

*Statut : reformulation propre, pas un fait nouveau sur Conway.*

### 1.2 Invariants automatiques

On écrit B = EᵀΩE.
- **Polynôme caractéristique.** charpoly(B) = (x − 4) x²⁶ charpoly((G − 3I)|_Z). C'est exactement ce qu'impose le spectre
  du graphe lointain (note 114). Toutes les traces tr(Bᵏ) sont donc compatibles d'office.
- **Moments.** Les moments d'ordre 1 et 2 (prompt Core37, §5.1) sont automatiques.
- **Ce qui reste.** Parmi les invariants de G seul, le discriminant (L23) est le seul qui ait donné un filtre. Les
  invariants spectraux sont compatibles d'office.

### 1.3 L'étoile au rang 37 est une condition de non-augmentation du rang

Le rang 37 impose rang₇ M[N[T] ∪ étoile(x)] = 37, comme pour N[T] seul. Ajouter les 10 lointains de x ne doit donc pas
augmenter le rang.

---

## 2. Expériences sur l'étoile (E)

Scripts `star_csp.py`, `star_stats.py`, `star_real.py`. Un processus, priorité IDLE.

### 2.1 Ablation

Graine 1, x = 0, `star_ablation_s1x0.jsonl`.

| retiré | verdict | nœuds |
|---|---|---|
| rien | réfutée | 12 817 |
| marges (k) | réfutée | 18 273 |
| comptes proche–lointain (n) | réfutée | 16 299 |
| k et n | réfutée | 26 498 |
| couplage (m), et m avec k ou n | non conclu à 60 s | 22 531 à 183 805 |
| valeurs de Green (g, diagonale conservée) | **satisfaisable** | 128 |

### 2.2 Noyaux minimaux

Fichier `star_cores.jsonl`.
- Graines 1, 2, 4 : toujours 7 lointains.
- Graine 1 : chacune des 7 sous-étoiles de 6 est satisfaisable (contrôle explicite, sans timeout).

### 2.3 Test statistique

Fichier `star_stats_s1x0.json`.
- Fréquences des valeurs g sur les paires de candidats : 0,1428 à 0,1430 pour chaque résidu.
- Quatre tirages de 4 lointains. Le rapport « comptes exacts / modèle indépendant » vaut 1,002 à 1,007 pour les 3-uplets
  et 0,998 à 1,010 pour les 4-uplets. Le modèle corrigé des degrés donne 0,993 à 1,002.

### 2.4 Espérance heuristique

On compte les solutions pour k lointains, avec un couplage partiel et des valeurs épinglées : 360ᵏ · T(k) · 7^(−k(k−1)/2),
où T(k) est le nombre de couplages partiels.

| k | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|
| espérance | 6·10⁵ | 3·10⁴ | 3·10² | 0,5 | 10⁻⁴ | 3·10⁻⁹ |

Le seuil se situe entre 7 et 8, ce qui colle avec les noyaux de 7.

### 2.5 Projecteur réel, sans rang

Fichier `star_real.py`. Échantillons qui ne respectent que la combinatoire.
- 300 étoiles et 415 couplages : aucun bloc 7Π n'est semi-défini positif. La plus petite valeur propre a pour médiane −1,78.
- Probabilité qu'un bloc k × k de triplets aléatoires soit semi-défini positif : 0,67 / 0,29 / 0,08 / 0,014 / 0,0012 /
  10⁻⁴ / 0 pour k = 2…8 (20 000 tirages).
- Extrapolation : environ 10⁻¹¹ pour k = 10, contre environ 10²⁵ configurations combinatoires.
- La positivité seule laisse donc probablement beaucoup d'étoiles. Le rang ≤ 8 (une équation réelle de plus) ne se teste
  pas par échantillonnage.

---

## 3. Ce que cela implique

### 3.1 Coût d'une preuve uniforme par ordinateur

Avec un test d'étoile optimisé en C++, estimé (non mesuré) à environ 10 à 25 ms par G_T, Green compris :
- environ 10¹¹ classes donnent 30 à 80 années-CPU ;
- il faut en plus une génération ordonnée des classes ;
- il faut aussi les maillons 2, 3 et 5.

NOTE_FUSION disait « des milliers d'années-CPU » avec le moteur de droite complète, à environ 1 s par G_T. Le bon ordre
de grandeur est donc la dizaine d'années-CPU. Cela reste hors de portée sans calcul payant.

### 3.2 Rangs 39 à 43

Même décompte, avec u ∈ F₇^ρ :
- l'étoile seule redevient satisfaisable heuristiquement, environ 10⁵ solutions au rang 39 ;
- la **double étoile** de x et x̄ (20 lointains, couplage croisé épinglé) reste sur-déterminée à tous les rangs. Les
  espérances, très grossières et symétrie O(D) comprise, sont d'environ 10⁻⁷⁰, 10⁻⁴⁰ et 10⁻¹⁰ à 10⁻¹⁷ aux rangs 39, 41,
  43 ;
- c'est l'unité naturelle de ces rangs, mais sa recherche exacte demande un moteur dédié, avec un repère d'abord. Non
  écrit.

---

## 4. Alternatives non encore testées

1. **Ordre 2 en 7.** Au rang 37, Π_T = (3I − R + J/12 − FᵀΓ_RF)/7 est 7-entier, et Π_T mod 7 doit être un idempotent de
   rang 8, de type moins.
   - Sur une étoile : une condition mod 7, faible.
   - Sur une double étoile : rang ≤ 8 sur 18 directions utiles, donc très fort.
   - Inutile au rang 37, puisque l'étoile meurt déjà.
2. **Droites latérales.**
   - La double étoile de (x, x̄) détermine entièrement G_{T_x}, pour la droite latérale T_x = {t₀, x, x̄}.
   - Si T_x est générique, L23 impose (τ(G_{T_x}) | 7) = −1.
   - C'est un filtre gratuit, qui divise par 2 environ, sur les doubles étoiles, à tous les rangs.
3. **Projecteur réel aux rangs 39 à 43.**
   - Semi-défini positif et rang ≤ 8 sur toute famille de 9 lointains.
   - Combiné au résidu de rang ρ, c'est le seul filtre réel qui coupe les configurations partielles là où Green est
     diffus.

**Fichiers.** `star_csp.py`, `star_stats.py`, `star_real.py` ; journaux `star_ablation_s1x0.jsonl`, `star_cores.jsonl`,
`star_stats_s1x0.json`.
