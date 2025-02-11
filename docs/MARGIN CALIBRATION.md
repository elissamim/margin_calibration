
# Introduction

On considère une population $\mathcal{U}$ de taille $N$ pour laquelle on voudrait mesurer des caractères $Y \in \mathbb{R}^N$. En particulier, on désire estimer le total de ces caractères sur le total de la population $\mathcal{U}$ : $Y = \sum_{k \in \mathcal{U}} y_{k}$.

On tire pour cela un échantillon $\mathcal{s}$ de $n$ éléments appartenant à $\mathcal{U}$, avec un plan $p$ de probabilités d'inclusion simples $\pi_{k}$ pour chaque élément $k$ de $\mathcal{s}$. On dispose de $J$ variables auxiliaires $(X_{j})$ pour lesquelles ont connait les totaux $T(X_{j})$ sur $\mathcal{U}$ ainsi que les valeurs prises individuellement par chaque individu de $s$. Ces totaux, appelés marges de calage, sont regroupés dans un vecteur $T_{X} \in \mathbb{R}^{J}$. 

Le but d'un calage sur marges est de trouver des "poids de calage", $w_{k}$ pour chaque $k \in \mathcal{s}$, permettant d'extrapoler à partir des valeurs individuelles des $X_{j}$ sur $\mathcal{s}$ et des totaux $T(X_{j})$ sur $\mathcal{U}$, la somme $Y = \sum_{k \in \mathcal{U}} y_{k} = \sum_{k \in \mathcal{s}} w_{k} y_{k}$ où les $w_{k}$ sont obtenus de telle sorte à être les plus proches que possible des poids de sondage $d_{k}=\frac{1}{\pi_{k}}$.

Le calage de marges consiste ainsi à trouver les poids $\mathbf{w}=(w_{k})_{k \in \mathcal{s}}$ vérifiant :
$\arg\min_{\mathbf{w}} \sum_{k \in \mathcal{s}} f_k(w_k) $.



# Margin calibration

# Penalized margin calibration

# Margin calibration on tight bounds

# Pseudo-distance functions

# References
