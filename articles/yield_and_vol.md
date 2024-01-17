The concept of yield in finance is often considered to be substantially more elementary than implied volatility, but they are effectively different versions of the same notion. Yield and implied volatility are simply the values that you plug into a model to get a given price as output.

<h2> (Implied) Yield </h2>
Let's start with yield. Imagine that there is a future on some asset whose current value is $S$, supppose that it has time to expiry $T$. Suppose also that there is a constant growth rate $r$. Then the expected value of the asset at time $T$ is
$$
F = S \exp(rT).
$$

So, if the market price for such a future is some value $p_F$, then we can derive the market-implied yield $y$ -- or, more briefly, yield -- of this asset by simply plugging in $p_F$ for $F$ and solving the above equation, obtaining
$$
y = \frac{\ln( \frac{p_F}{S})}{T}.
$$

It is worth belaboring upon this simple example because the idea of deriving a price of a security based on a possibility of arbitrage -- or, more precisely, risk-free profit -- is fundamental to asset pricing in general and the Black-Scholes Merton model in particular. Suppose that the price $p$ of the future is less than its fair value $F = S \exp(rT)$. 

Why would this be a problem? Because then -- within the confines of this incredibly oversimplified model, granted -- one could ensure a risk-free profit. How? If $p < F$ -- e.g., the future is underpriced -- then you could buy the future and sell the spot and be guaranteed a positive payout (of $F - p$) at time $T$. Conversely, if $p > F$ then the future is overpriced and you could ensure a positive profit by selling the future and buying the underlying.

<h2>Implied Volatility</h2>
Now suppose instead that we are considering a (without loss of generality) _call_ option on an instrument with strike price $X$, time to expiry $T$, risk-free rate $r$ and underlying price $S$. The strike price is simply a feature of the instrument, but in order to obtain a price via the Black-Scholes Merton model we must also introduce a (significantly more complex) parameter, $\sigma$, which denotes the volatility or standard-deviation of the diffusion process that the asset is presumed to follow:

$$
\frac{dS_t}{S_t} = \sigma dW_t.
$$

It is easy to get lost in the details here, so either excuse some hand-waving or study stochastic calculus. Strictly speaking, the asset is presumed to follow a geometric Brownian motion, and it also can have a non-zero drift term (which, interestingly, does not affect the theoretical value of the option). But for the time being, it is sufficient to simply regard $\sigma$ as a positive value which indicates how noisy or volatile the asset is. Bitcoin, for example, has a significantly larger volatility than the S&P 500, and the S&P has a significantly larger volatility than the EURUSD exchange rate.

Under the (fairly restrictive) assumptions of the Black-Scholes Merton model -- holding fixed the values $S, X, T, r$ -- one can obtain a monotonically increasing function $f(\sigma)$ for the fair value of this call option. If the market price of the option is $p_I$, then the implied volatility of the option is simply that value of $\sigma$ for which 
$$
f(\sigma) = p_O.
$$

In other words, the implied volatiltiy is just the value of the parameter $\sigma$ which justifies the observed market price $p_O$ of the option, in precisely the same way that the yield is the value of the parameter $r$ which justifies the observed market price $p_F$ of the future.