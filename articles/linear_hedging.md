<h2>Simple hedge ratio via variance minimization</h2>
Suppose that there are 2 instruments with prices $X$ and $Y$ with standard deviations $\sigma_X$ and $\sigma_Y$ and correlation $\rho$. How can one hedge 1 unit of instrument $X$ with instrument $Y$? <br><br>

In general, if $n$ different securities have <a href="https://en.wikipedia.org/wiki/Covariance_matrix">variance-covariance matrix</a> $\Omega$, then the variance of a portfolio of positions $q \in \mathbb{R}^n$ of the securities is given by the quadratic form $q^T \Omega q$. So, in this simple case with 2 securities, if we take $q$ to be of the form $q = [1, h]^T$, then the portfolio variance for a given choice of $h$ is 
$$
V(h) = \begin{bmatrix} 1 \\ h \end{bmatrix}^T    \begin{bmatrix} \sigma_X^2 & \rho \sigma_X \sigma_Y \\ \rho \sigma_X \sigma_Y & \sigma_Y^2 \end{bmatrix} \begin{bmatrix} 1 \\ h \end{bmatrix} 
= \sigma_X^2 + 2 h \rho \sigma_X \sigma_Y + h^2 \sigma_Y^2.
$$ <br><br>

So, setting the derivative $V^{\prime}(h^*) = 2 h^* \sigma_Y^2 + 2 \rho \sigma_X \sigma_Y = 0$ we can derive the hedge ratio $h^* = -\rho \frac{\sigma_X}{\sigma_Y}$.

<h2>Price and position matrix</h2>
It can often be useful when designing or managing portfolios of securities to consider linear transformations of the prices of the securities involved. For example, if one is trading an ETF $X$ against a future $Y$ that it is supposed to track, with some effective price ratio $\alpha$, then it might be useful to consider the linear combination $X - \alpha Y$ as a security in its own right. <br> <br>

Given the potential usefulness of such linear transformations of the prices of securities, it is natural to consider how we should also (linearly) transform <i>positions</i> of securities. There is in fact a unique and fairly straightforward way to transform positions given a particular (linear) transformation of prices. <br> <br>

Suppose that we have a $n$ securities, and let's represent the vector of their prices and positions as $p, q \in \mathbb{R}^n$. Assume that each of the securities has the same contract size aka point value, of 1. Given a new vector of prices $p^{\prime} \in \mathbb{R}^n$, the profit or change in the portfolio value $\pi$ is simply the dot product of the vector of price changes $p^{\prime} - p$ and the position, i.e.
$$
\pi = \sum_{i=1}^n q_i (p_i^{\prime} - p_i) =  (p^{\prime} - p) \cdot q = \Delta_p \cdot q.
$$

Now, suppose that we want to use some invertible matrix $A \in M_{n \times n}(\mathbb{R})$ to transform our vector of security prices. In our ETF vs futures example from above, we might conceivably be interested in the matrix 
$$
A = \begin{bmatrix}
1 & 0 \\
1 & -\alpha
\end{bmatrix},
$$
as the bottom row or <i>factor</i> corresponds to the ETF vs futures basis that we are interested in trading, whereas the top row corresponds to the dimension of risk we'd likely want to hedge. <br><br>

Given such a matrix $A$ for transforming our vector of instrument prices (henceforth <i>price matrix</i>), what should we use for our invertible matrix $B$ for transforming our vector of instrument positions (henceforth <i>position matrix</i>)? Our choice of matrix should preserve the PnL earned by the portfolio under any possible price changes for any possible position changes. That is, 
$$
\Delta_p \cdot q = A \Delta_p \cdot B q
$$
for any possible $\Delta_p$ and $q$. Then, <a href="https://proofwiki.org/wiki/Factor_Matrix_in_the_Inner_Product">since we can move the matrix by transposing it</a>, we can see 
$$
\Delta_p \cdot q = \Delta_p \cdot A^T B q.
$$
<br><br>

Since this must hold for <i>all</i> possible vectors $\Delta_p$ and $q$, one can see (e.g. by plugging in all pairs of unit vectors) that $A^T B = I$ and so $B = (A^{-1})^T = (A^T)^{-1}$. That is to say, the <i>unique</i> position matrix consistent with the price matrix $A$ is the inverse transpose of $A$.