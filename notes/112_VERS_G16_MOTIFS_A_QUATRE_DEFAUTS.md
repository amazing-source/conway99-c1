# 112 — Vers g(x) ≤ 16 : les motifs à quatre grilles incomplètes (réduits à 20 configurations)

*25/09, soir. Plancher suivant après g(x) ≤ 17 (notes/108) et L14 pour |C| = 2 (notes/111). Deux lemmes à la main
réduisent les motifs de torsion à quatre défauts, puis un contrôle du second ordre (les « doubles » de notes/111)
en élimine presque toutes les configurations. Il en reste 20, très symétriques, pour lesquelles il faut un ordre de
plus. Scripts : `code/g16_cycles.py` (ordre un), `code/g16_c2222.py`, `code/g16_blocks.py` (ordre deux).*

## 0. Résumé
| énoncé | statut |
|---|---|
| Lemme 0 : le graphe 𝒩 des paires incomplètes est de degré minimal ≥ 2 sur les classes qu'il touche | preuve (R0, L12, L13) |
| donc \|𝒩\| = 4 impose que 𝒩 soit un 4-cycle de classes ; le « chemin » de D2 et les étoiles de D1 tombent en une ligne | preuve |
| Lemme A : deux classes voisines du cycle qui tordent toutes les deux ont chacune leurs deux étiquettes tordantes, et les ombres sont des échanges | preuve |
| Lemme B : entre deux classes muettes, les deux autres classes du cycle ont autant d'étiquettes tordantes | preuve |
| des 10 motifs du 4-cycle, il reste (0,1,0,1) = L14, (0,2,0,2), (0,2,2,2), (2,2,2,2) | preuve |
| ordre deux (blocs de Kneser opposés) : (0,2,2,2) meurt ; (0,2,0,2) et (2,2,2,2) laissent 8 et 12 configurations | contrôle fini exact |
| **g(x) ≤ 16** | **ouvert : 20 configurations** |

## 1. Lemme 0 (degré minimal)
*Énoncé.* Toute classe touchée par 𝒩 appartient à au moins deux paires incomplètes.
*Preuve.* Soit γ dans une seule paire incomplète {α, γ}.
- Si γ est tordue, ses tordeuses sont des étiquettes de α (sinon une autre paire serait incomplète). Par L13, il y en a
  deux, donc a et ā.
- Aucune étiquette hors de α ∪ γ ne tord γ, donc L12 (pour a et chaque c ∈ γ) impose que chaque c ∈ γ torde α.
- Par R0, c tord une deuxième classe, d'où une deuxième paire incomplète en γ : contradiction.
- Si γ n'est pas tordue, {α, γ} est incomplète parce qu'une étiquette c ∈ γ tord α. Par R0 elle tord une autre classe :
  même contradiction. ∎

*Conséquences.*
- Une étoile (cas étoile de D1) ou le chemin {αy, αδ, δw} de D2 ont des classes de degré 1 : ils tombent en une ligne.
- Un graphe à 4 arêtes, de degré minimal ≥ 2 sur son support, est un 4-cycle. Donc **|𝒩| = 4 ⟹ 𝒩 = 4-cycle 0–1–2–3**,
  les classes 4, 5, 6 étant libres.
- Une étiquette de la classe v tord alors ∅ ou les deux voisines de v. On note T_v ses étiquettes tordantes. À
  symétrie près, on a **10 motifs** (|T₀|, |T₁|, |T₂|, |T₃|) permis par L12 et L13.

## 2. Lemme A (classes voisines tordantes)
*Énoncé.* Si T₀ ≠ ∅ et T₁ ≠ ∅, alors |T₀| = |T₁| = 2. De plus, ρ₀ échange les deux étiquettes de 1, et ρ₁ celles de 0.
*Preuve.* Soit y = {a, b}, avec a ∈ T₀ et b ∈ T₁.
1. Les classes libres 4, 5, 6 donnent n_{md}(y) = 1 pour m ∈ {2, 3} et d ∈ {4, 5, 6} : leurs quatre paires sont toutes
   complètes et leurs fentes valent 4.
2. Les fentes de m ∈ {2, 3} donnent donc n₂₃(y) = 1 − s_m(y), d'où s₂(y) = s₃(y) ≤ 1.
3. Comme a tord 1, τ_a(b) est dans la classe 3, donc s₃ ≥ 1, et l'ombre ρ₀(b) n'est pas dans la classe 3.
4. Donc ρ₀(b) = b̄ : b̄ ∈ T₁, et S₀(y) = {ā, b̄}. Ce sommet contient b̄, donc il vaut aussi S₁(y) = {b̄, ρ₁(a)}.
5. D'où ρ₁(a) = ā, et ā ∈ T₀. ∎

## 3. Lemme B (classe muette)
*Énoncé.* Si T₀ = ∅ et b ∈ T₁, alors ρ₀(b) est dans la classe 3. Si de plus T₂ = ∅, alors ρ₀ envoie T₁ dans T₃ et T₃
dans T₁, injectivement, et donc |T₁| = |T₃|.
*Preuve.* Soit y = {a, b} avec a ∈ 0. ρ₁ ne déplace que des étiquettes de 2, puisque Z₁ = T₀ ∪ T₂. Si ρ₀(b) = b̄, alors
S₀(y) = {ā, b̄} contient b̄ et vaut S₁(y) = {b̄, a}, ce qui est absurde. ∎

**Bilan.** Le lemme A tue (1,1,1,1), (1,1,1,2), (1,1,2,2), (1,2,1,2) et (1,2,2,2). Le lemme B tue (0,1,0,2). Le calcul
du premier ordre (fentes, `g16_cycles.py`) confirme : toutes les configurations de ces six motifs sont réfutées par
propagation. Il reste :
- (0,1,0,1), c'est-à-dire L14 avec |C| = 2 : réglé à la main (notes/111) ;
- (0,2,0,2), (0,2,2,2) et (2,2,2,2), avec les ombres forcées par A et B : 256 configurations chacun, toutes compatibles
  avec l'ordre un.

## 4. Ordre deux : les blocs de Kneser opposés (même méthode que notes/111)
Pour ces trois motifs, à la main :
- Les sommets de Q₀₁ et de Q₂₃ n'ont aucun voisin dans le quadrangle opposé (fentes, comme au lemme A). Donc
  e(Q₀₁, Q₂₃) = 0, et de même e(Q₀₃, Q₁₂) = 0.
- Leurs voisins communs génériques sont tous dans Q₄₅ ∪ Q₄₆ ∪ Q₅₆. Un sommet z de ces quadrangles vérifie
  n₀₁ = n₂₃ = q_z et n₀₃ = n₁₂ = 2 − q_z. Ici q_z ∈ {0, 2} : les sommets q = 2 sont exactement les six « doubles » qui
  comblent les déficits de Q₀₁ (paires non adjacentes à qui il manque du μ, et arêtes antipodales dont la droite a son
  troisième point là), et ceux de Q₂₃.
- Dans un quadrangle, les deux sommets q = 2 couvrent des paires complémentaires.
- La matrice D(y, w) = 2 − #(voisins communs décidés par τ, ρ) sur Q₀₁ × Q₂₃ doit valoir Σ_z N₀₁(z) ⊗ N₂₃(z). Même chose
  pour le bloc Q₀₃ × Q₁₂ avec les sommets q = 0.
- Contrôle exact de cette décomposition (`g16_blocks.py`) :

| motif | configurations (ombres forcées) | les deux blocs morts | survivantes |
|---|---|---|---|
| (0,2,0,2) | 256 | 248 | **8** |
| (0,2,2,2) | 256 | 256 | 0 |
| (2,2,2,2) | 256 | 244 | **12** |

Les 8 survivantes de (0,2,0,2) forment une seule famille à symétrie près : ρ₀ = ρ₂ (une bijection entre les étiquettes
de 1 et celles de 3, parallèle ou croisée), et ε(1^t)·ε(ρ(1^t)) = −1, où ε(ℓ) = ± indique si τ_ℓ préserve ou échange
les signes entre les classes 0 et 2.

## 5. Ce qui reste pour g(x) ≤ 16
Il faut un ordre de plus pour les 20 configurations survivantes. On sait déjà, pour un double z (q = 2) et un sommet
y* ∈ Q₀₁ non voisin de z :
- l'unique voisin de y* dans Q₀₁ ∖ {y*} qui partage son étiquette de la classe 0 est un voisin de z ;
- il faut donc exactement un voisin commun de plus, parmi les siblings de z dans son quadrangle et les voisins de z
  dans Q₂₆ et Q₃₆.

Les cinq droites de z sont également contraintes :
- une par voisin de Q₀₁, avec un voisin dans Q₂₆ ou Q₃₆ ;
- une par voisin de Q₂₃, avec un voisin dans Q₀₆ ou Q₁₆ ;
- une qui joint les voisins de z dans Q₀₂ et Q₁₃, qui doivent donc être appariés par la bijection de Kneser φ₀₂,₁₃.

C'est la mécanique de L8 (bijections de Kneser) appliquée à la partie de type Hamming. Rien n'est encore décidé.
