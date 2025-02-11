
# Introduction

On considère une population $\mathcal{U}$ de taille $N$ pour laquelle on voudrait mesurer des caractères $Y \in \mathbb{R}^N$. En particulier, on désire estimer le total de ces caractères sur le total de la population $\mathcal{U}$ : $Y = \sum_{k \in \mathcal{U}} y_{k}$.

On tire pour cela un échantillon $\mathcal{s}$ de $n$ éléments appartenant à $\mathcal{U}$, avec un plan $p$ de probabilités d'inclusion simples $\pi_{k}$ pour chaque élément $k$ de $\mathcal{s}$. On dispose de $J$ variables auxiliaires $(X_{j})$ pour lesquelles ont connait les totaux $T(X_{j})$ sur $\mathcal{U}$ ainsi que les valeurs prises individuellement par chaque individu de $s$. Ces totaux, appelés marges de calage, sont regroupés dans un vecteur $T_{X} \in \mathbb{R}^{J}$. 

Le but d'un calage sur marges est de trouver des "poids de calage", $w_{k}$ pour chaque $k \in \mathcal{s}$, permettant d'extrapoler à partir des valeurs individuelles des $X_{j}$ sur $\mathcal{s}$ et des totaux $T(X_{j})$ sur $\mathcal{U}$, la somme $Y = \sum_{k \in \mathcal{U}} y_{k} = \sum_{k \in \mathcal{s}} w_{k} y_{k}$ où les $w_{k}$ sont obtenus de telle sorte à être les plus proches que possible des poids de sondage $d_{k}=\frac{1}{\pi_{k}}$.

Le calage de marges consiste ainsi à trouver les poids $\mathbf{w}=(w_{k})_{k \in \mathcal{s}}$ vérifiant :

$\arg\min_{\mathbf{w}} \sum_{k \in \mathcal{s}} d_{k}G(\frac{w_{k}}{d_{k}})$, avec $G$ une pseudo-distance.

Sous la contrainte suivante : $X_{\mathcal{s}}^{'}\mathbf{w}=T_{X}$, où $X_{\mathcal{s}}$ correspond à la matrioce dont les colonnes dont les $X_{j}$ pour les différents individus de $\mathcal{s}$ et $T_{X}$ le vecteur dont chaque élément $j$ correspond à $T(X_{j})$.

Différentes pseudo-distances ou "méthodes de calage" sont proposées:
- méthode "linéaire" : $G(r) = \frac{1}{2}(r-1)^{2}$, cette méthode conduit à une distance de type khi-deux entre les poids $d_{k}$ et $w_{k}$. Cette méthode est la plus rapide, une confergence est assurée à partir de deux itérations avec un algorithme de Newton. Elle peut conduire à des poids $w_{k}$ négatifs, et les poids ne sont pas bornés supérieurement
- méthode "raking ratio" : $G(r) = r\ln(r)-r+1$, cette méthode conduit à une distance de type entropie entre les poids $w_{k}$ et $d_{k}$. Conduit à des poids toujours positifs et non bornés supérieurement. Les poids issus de cette méthode sont généralement supérieurs à ceux de la méthode linéaire
- méthode "logit" : méthode tronquée, on choisit deux bornes inférieure et supérieure $L$ et $U$

# Margin calibration

# Penalized margin calibration

# Margin calibration on tight bounds

# References
