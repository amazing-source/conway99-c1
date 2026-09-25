# 98 — Bilan de la nuit du 24 au 25/09 (session autonome de 8 h)

*À lire en premier au réveil. Tout est poussé sur GitHub. Détails : notes/94 (littérature), 95 (L7, L8), 96 (Akiyama),
97 (k).*

## Résultats nouveaux, vérifiés
| | énoncé | statut |
|---|---|---|
| **L7** | un point de Hamming n'est pas le point fixe d'une involution (le point fixe de la branche C2 est tordu) | **preuve à la main** (auparavant SAT seul) |
| **L9'** | τ_a(c) ≠ c̄ et τ_{c̄}(a) = ā ⇒ une grille G_{[c],m} (m ∉ {[a],[c]}) manque en x | preuve à la main (tirée d'un noyau UNSAT de 7 contraintes) |
| L10 | g(x) ≠ 19 | seconde preuve humaine via L9' (la première, via L12, existait déjà) |
| **L20** | pour toute étiquette a : k ≥ 11 − 2e(τ_a) (e = cycles pairs du graphe de classes de τ_a) | preuve à la main + calcul exhaustif sur les 10 395 τ_a |
| **L20 bis** | k ≠ 6, donc **k ≥ 8** | preuve à la main |
| **L20 ter** | k ≠ 8, donc **k ≥ 10**, c'est-à-dire rank₇(A − 3I) ≥ 25 | calcul exact petit (énumération sur F₇, 32 instances UNSAT par propagation) |
| formule | k = rank₇(H + 4I + 3S + P' + 5J), matrice 84 × 84 en n'importe quel sommet | preuve à la main, vérifiée exactement |
| conséquences | k = 6 ⟹ P = 0 ; P ≥ 1 ⟹ k ≥ 8 ; une étiquette non tordue ⟹ k ≥ 12 | preuve à la main |

Rappel : k = rank₇(A − 3I) − 15 est l'invariant 7-adique global de L4/L19, pair, ≤ 30. La nuit l'a encadré :
**10 ≤ k ≤ 30**, et c'est le premier lien démontré entre k et la torsion locale. **Aucun de ces résultats ne résout le
problème.**

### Preuve de L7 en quatre lignes
1. Si σ_x ∈ Aut, les bijections φ entre carrés disjoints de Γ₂(x) respectent les diagonales, avec des décalages
   δ ∈ F₂.
2. Le fait C (μ = 2 entre carrés partageant une classe) force exactement 3 des 6 paires R à avoir
   δ(ij,R) + δ(ik,R) = 1.
3. On somme sur les 105 triplets : chaque δ apparaît 12 fois, donc 0 ≡ 105 ≡ 1.
4. Contradiction.

### Preuve de k ≥ 8 en cinq lignes
1. Si k = 6, chaque étoile est de type (2,2,2), de rang 5 = k − 1.
2. Ses lignes engendrent alors un hyperplan non dégénéré de l'espace des lignes (dimension 6).
3. Donc chaque vecteur du noyau du bloc d'étoile est une relation entre lignes complètes, en particulier
   ligne({a,ℓ₁}) = ligne({a,ℓ₃}).
4. La colonne {ℓ₁,q} impose alors H − H' ≡ 4 ou 5 (mod 7) avec H, H' ∈ {0,1}.
5. Contradiction.

## Littérature (textes intégraux, et deux crédits à rendre)
- **L1 était connu** : Makhnev (1988), Mat. Zametki 44(5), théorème 2 (crédité partout).
- **Le principe des bornes de p-rang par sous-graphe induit** (base de L19 bis et L20) est dans le mémoire de van Eijl
  (1991, dirigé par Brouwer), §3.3. Ce qui est nouveau, c'est l'application à 99 (étoiles, formule 11 − 2e, k ≥ 10).
- Lus en entier : Wilbrink 1984 (ordre 11), Wilbrink–Brouwer 1983 (57), Reimbayev (19 ; hexagones), Cesarz–Woldar 2025,
  Ishida 2026 (identité trace-rang, travaillée pour 99 : rien de neuf pour C2 avec un point fixe), Shpectorov–Zhao 2025
  (85,14,3,2), Brouwer–Van Maldeghem 2022, Brouwer–Neumaier 1988, Kivva 2021, et d'autres. **Pour C1, la littérature
  ne contient rien d'autre que Makhnev 1988.**
- **Akiyama (arXiv:2609.08319, 8 sept. 2026)** : non-existence de srg(266,45,0,9), jusque-là ouvert, par réseaux entiers
  et séries thêta, formalisée en Lean. C'est la seule méthode globale nouvelle rencontrée. Pour 99, la meilleure cible
  est le **réseau des droites** (231 vecteurs de norme 4, rang 44, constante de repère impaire 21), voir notes/96. Non
  exécuté : plusieurs jours de travail.

## Audits
- **L16 (P ≤ 1151) refait entièrement à la main : correct.**
- Fichiers parasites supprimés, journaux de calcul ajoutés.

## Échecs et limites (honnêtes)
- **L8** (point de Hamming sans symétrie) : pas de preuve humaine. Structure partielle obtenue : règle de transport ;
  aucun triangle de Kneser n'a une seule arête non isométrique ; image « code de Golay factice », où la cohérence est
  impossible par 10/3. Le squelette des parties linéaires ne tranche pas en 20 min.
- **L11** : noyau UNSAT minimal de 112 équations, trop gros pour la main.
- Test « tous les τ de type (2,2,2) » : tué au plafond de 4 Go (pour le PC du labo).
- Deux étoiles couplées : rang observé ≥ 14, ce qui donnerait k ≥ 12 si c'était prouvé ; non prouvé.
- Aucune borne supérieure sur la torsion, ni sur k : le verrou principal reste entier.

## Pour la session C2
L7 a maintenant une preuve à la main de quelques lignes (notes/95), qui dispense de certifier le SAT. L'obstruction est
une parité sur la matrice d'orbites modulo 2 ; l'équation modulo 2 nue est toujours soluble, donc pas de raccourci
pour C2 dans le cas tordu.
