
# Introduction

We consider a population $\mathcal{U}$ of size $N$ for which we want to measure characteristics $Y \in \mathbb{R}^N$. In particular, we aim to estimate the total of these characteristics across the entire population $\mathcal{U}$: $Y = \sum_{k \in \mathcal{U}} y_{k}$.

To achieve this, we draw a sample $\mathcal{s}$ of $n$ elements belonging to $\mathcal{U}$, with a sampling design $p$ that assigns simple inclusion probabilities $\pi_{k}$ to each element $k$ in $\mathcal{s}$. We have $J$ auxiliary variables $(X_{j})$ for which we know the totals $T(X_{j})$ over $\mathcal{U}$ as well as the individual values for each member of $\mathcal{s}$. These totals, called calibration margins, are grouped into a vector $T_{X} \in \mathbb{R}^{J}$.

The goal of margin calibration is to find "calibration weights" $w_{k}$ for each $k \in \mathcal{s}$, allowing us to extrapolate, based on the individual values of $X_{j}$ in $\mathcal{s}$ and the totals $T(X_{j})$ in $\mathcal{U}$, the sum $Y = \sum_{k \in \mathcal{U}} y_{k} = \sum_{k \in \mathcal{s}} w_{k} y_{k}$, where the weights $w_{k}$ are determined to be as close as possible to the sampling weights $d_{k}=\frac{1}{\pi_{k}}$.

Margin calibration thus consists of finding the weights $\mathbf{w}=(w_{k})_{k \in \mathcal{s}}$ that satisfy:

$\arg\min_{\mathbf{w}} \sum_{k \in \mathcal{s}} d_{k}G(\frac{w_{k}}{d_{k}})$, with $G$ being a pseudo-distance.

Under the following constraint: $X_{\mathcal{s}}^{'}\mathbf{w}=T_{X}$, where $X_{\mathcal{s}}$ corresponds to the matrix whose columns are the $X_{j}$ for the different individuals in $\mathcal{s}$, and $T_{X}$ is the vector where each element $j$ corresponds to $T(X_{j})$.

# Pseudo-distance functions

Different pseudo-distances or "calibration methods" are proposed:

- **"*Linear*" method**: $G(r) = \frac{1}{2}(r-1)^{2}$, this method leads to a chi-square-type distance between the weights $d_{k}$ and $w_{k}$. This method is the fastest, with convergence guaranteed after two iterations using a Newton algorithm. It can lead to negative weights $w_{k}$, and the weights are not upper-bounded.

- **"*Raking ratio*" method**: $G(r) = r\ln(r)-r+1$, this method leads to an entropy-type distance between the weights $w_{k}$ and $d_{k}$. It results in weights that are always positive and not upper-bounded. The weights from this method are generally higher than those from the linear method.

- **"*Logit*" method**: A truncated method, where two bounds, lower $L$ and upper $U$, are chosen such that $L < 1 < U$. The form of the pseudo-distance is then as follows:  
  $G(r) = [(r-L)\ln(\frac{r-L}{1-L})+(U-r)\ln(\frac{U-r}{U-1})]\frac{1}{A}$, if $L < r < U$, with $A = \frac{U-L}{(1-L)(U-1)}$.  
  This method ensures that the ratios $\frac{w_{k}}{d_{k}}$ always remain within the intervals $]L, U[$. However, the values of $L$ and $U$ cannot be chosen arbitrarily. Generally, $L$ must be less than an upper bound $L_{max}$ (less than 1) and $U$ must be greater than a lower bound $U_{min}$ (greater than 1). These values depend on the data and the calibration margins: the more the sample differs from the general population, the further these values are from 1.

- **"*Truncated linear*" method**: A truncated version of the *linear* pseudo-distance that ensures non-negative weights with reasonable magnitudes. The method is given by:  
  $G(r) = \frac{1}{2}(r-1)^{2}$ with $L \leq r \leq U$ where $L < 1 < U$, and the presence of bounds $L_{max}$ and $U_{min}$.

The *logit* and *truncated linear* methods are the most commonly used, as they allow obtaining weights with reasonable magnitudes, including negative weights as is the case with the *linear* method.

# Penalized margin calibration

Introducing regularization facilitates the convergence of the estimation program, thereby increasing the number of control variables while maintaining a narrow distribution of calibration factors. Let $\hat{T_{Xw}}$ be the estimator of the sums of auxiliary variables weighted by the weights $w$, i.e., $\hat{T_{Xw}}=(\sum_{k\in\mathcal{s}}w_{k}x_{jk})$. We also define a cost vector $\mathbf{C}$ whose size corresponds to the number of margins, and whose j-th value corresponds to the cost associated with the j-th margin. The penalized calibration problem is then formulated as:

$\arg\min_{\mathbf{w}}\sum_{k\in\mathcal{s}}d_{k}G(\frac{w_{k}}{d_{k}})+\lambda(\hat{T_{Xw}}-T_{X})^{'}\text{Diag}(C)(\hat{T_{Xw}}-T_{X})$.

The parameter $\lambda$ ranges between 0 and $+\infty$ and represents the relative importance in the program of the distance to the initial weights and the emphasis on the margins of the adjusted estimates. The same pseudo-distances can be used for penalized calibration, especially when the distance term is predominant ($\lambda\to0$). However, when the cost term is predominant ($\lambda\to+\infty$), it is not necessary to introduce a pseudo-distance with bounds (e.g., *logit*, *truncated linear*), as the margin constraints are satisfied first, which moves the calibration factors away from 1.

An exact calibration on a given margin can be achieved by assigning a higher cost to this margin than to the other margins, for example, an infinite cost.

# Margin calibration on tight bounds

$\arg\min_{g}(\max_{k\in\mathcal{s}}g_{k}-\min_{k\in\mathcal{s}}g_{k})$ sous la contrainte : $\tilde{X_{s}}^{'}g=T_{X}; g \geq 0$

# References

- Sautory, O. (2018), Les méthodes de calage. Working paper.
- Rebecq, A. (2016), Icarus : un package R pour le calage sur marges et ses variantes. Working paper. http://paperssondages16.sfds.asso.fr/submission_54.pdf
- Rebecq, A. (2023), icarus. GitHub. https://github.com/haroine/icarus

