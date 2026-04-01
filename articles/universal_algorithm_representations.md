**LLMs Converge on a Universal Algorithm Representation Across Programming Languages, Natural Languages, and Modalities**

*April 2026*

Large language models appear to construct an internal representation of algorithms that is independent of the surface form in which the algorithm is expressed. A Mandarin description of the Fibonacci sequence, a Haskell implementation, and a Bash script all converge to the same region of representational space in the middle layers of Qwen3.5-27B. This post presents the experimental evidence.

<h2>Background and Motivation</h2>

Recent work on the "platonic representation hypothesis" ([Huh et al., 2024](https://arxiv.org/abs/2405.07987)) has argued that foundation models trained on different data and with different objectives converge on a shared statistical model of reality. Separately, [Ng (2024)](https://www.lesswrong.com/posts/bDukCqjfXdaasYb5o/exploring-the-similarity-of-representations-across-languages) showed that LLM representations of the same sentence in different natural languages become increasingly similar in mid-layers, suggesting a language-independent semantic core.

I wanted to push this further. If models converge on shared representations across natural languages, do they also converge across *programming* languages? And if so, does this extend across the code/prose boundary — do natural language *descriptions* of algorithms map to the same representational space as their code *implementations*?

<h2>Setup</h2>

All experiments were run on a single AMD Ryzen AI MAX 395+ with 128GB unified memory, running CachyOS with ROCm 7.2. Models were loaded in bfloat16 via HuggingFace Transformers.

The core dataset is 64 short programs: 8 algorithms (hello world, fibonacci, factorial, fizzbuzz, reverse string, insertion sort, is-prime, GCD) × 8 programming languages (Python, C, JavaScript, Rust, Haskell, Go, Lisp, Bash). Each implementation is correct, self-contained, and minimal.

For each program, I extracted mean-pooled hidden states at every layer of Qwen3.5-27B (64 transformer layers + embedding layer), then computed pairwise centered cosine similarity, grouping pairs into three categories: *same algorithm, different language*; *same language, different algorithm*; and *different on both*.

<h2>Finding 1: Mid-Layer Representations Cluster by Algorithm</h2>

In layers 10–47 (roughly 15–75% of model depth), programs implementing the same algorithm in different languages are far more similar to each other than programs in the same language implementing different algorithms.

| Region | Same Algorithm | Same Language | Gap |
|---|---|---|---|
| Mid-layers (15–75% depth) | 0.487 | 0.185 | **+0.302** |
| Late layers (82–100% depth) | 0.218 | 0.420 | −0.202 |

The pattern reverses in the final ~20% of layers: language-level features dominate the geometry, consistent with the model re-encoding surface syntax for next-token prediction.

This replicates on a second architecture — Qwen3.5-35B-A3B, a mixture-of-experts model with 3B active parameters — at the same proportional depth (~82% crossover point), with a mid-layer gap of +0.314.

The per-language-pair similarity matrix in the mid-layer band reveals expected structure: C, JavaScript, and Go cluster tightly (centered cosine 0.67–0.73), Haskell and Lisp form a separate cluster (0.54), and the two groups are distant from each other.

<h2>Finding 2: Algorithm Identity Is Never Erased</h2>

A natural question: does the late-layer reversal mean the model *loses* its algorithm representation? No. An 8-way logistic regression probe (L2-regularized, PCA-50 preprocessing) trained to predict algorithm label from hidden states achieves 100% accuracy at *every single layer*, using leave-one-language-out cross-validation (train on 7 languages, test on the held-out 8th).

The late-layer cosine reversal reflects a geometry shift — language features become the dominant axis of variation — but the algorithm subspace persists underneath and remains perfectly linearly separable through the output layer.

<h2>Finding 3: Computational Structure Is Encoded, Not Surface Form</h2>

Binary probes for structural properties of the code (same leave-one-language-out CV):

| Property | Definition | Chance | Peak Accuracy |
|---|---|---|---|
| Is recursive | fibonacci, factorial, gcd, reverse = 1 | 50% | 100% (from layer 7) |
| Has loop | fizzbuzz, sort, isprime = 1 | 62.5% | 100% (from layer 1) |
| Is functional language | haskell, lisp = 1 | 75% | 89.1% (barely above chance) |

The model robustly encodes whether code uses recursion or loops — computational structure — while language family membership (functional vs imperative) is barely detectable. The representation is organized around *what the code does*, not *what it looks like*.

<h2>Finding 4: English Descriptions Retrieve Correct Code Cross-Lingually</h2>

This is where it gets interesting. I wrote short English descriptions of each algorithm (e.g., *"Compute the nth Fibonacci number by summing the two preceding values, starting from 0 and 1"*) and extracted their hidden states at every layer. Then, for each description, I ranked all 64 code programs by centered cosine similarity and measured top-8 retrieval accuracy (chance = 12.5%).

| Layer Range | Mean Top-8 Retrieval |
|---|---|
| 0–8 (early) | 32–44% |
| 12–16 | 75–78% |
| 20–40 (mid) | **96–100%** |
| 48–56 (late) | 77–84% |
| 64 (final) | 61% |

At layers 36–40, a plain English sentence describing Fibonacci is closer in representational space to Fibonacci implementations in Python, C, Rust, Haskell, Lisp, Go, JavaScript, and Bash than to code implementing *any other algorithm* in *any language*. The model maps prose and code to the same semantic space.

<h2>Finding 5: This Extends Across Natural Languages</h2>

I repeated the cross-domain retrieval experiment with algorithm descriptions in five natural languages: English, Mandarin Chinese, French, Arabic, and Russian.

| Natural Language | Best Layer | Peak Retrieval Accuracy |
|---|---|---|
| English | 27 | 100% |
| French | 24 | 100% |
| Russian | 26 | 100% |
| Arabic | 37 | 100% |
| Mandarin | 39 | 98.4% |

A Mandarin description of Fibonacci maps to the same mid-layer region as Fibonacci implementations in 8 programming languages. All five natural languages achieve 90–100% retrieval accuracy across layers 20–40. Late-layer degradation is steeper for non-English languages (Arabic drops to 36% at layer 60 vs 80% for English), consistent with stronger English-centric surface representations in the head.

The NL-to-NL similarity analysis confirms that descriptions of the same algorithm in different natural languages cluster together in mid-layers, grouped by algorithm identity rather than by natural language.

<h2>Finding 6: The Representation Captures How, Not Just What</h2>

How fine-grained is this representation? I introduced algorithm variants — iterative Fibonacci (loop-based instead of recursive), bubble sort (instead of insertion sort), subtraction-based GCD, recursive reverse — and near-miss algorithms that are structurally similar but compute different things (sum-to-n, Collatz sequence). All in 8 programming languages, for a total of 112 programs.

Centered cosine similarity between algorithm centroids at the peak algorithm layer (layer 36):

| Variant | Nearest Original | Similarity | Gap to 2nd Nearest |
|---|---|---|---|
| reverse (recursive) | reverse | 0.801 | +0.71 |
| sort (bubble) | sort (insertion) | 0.754 | +0.55 |
| GCD (subtraction) | GCD (modulo) | 0.738 | +0.64 |
| fibonacci (iterative) | fibonacci (recursive) | 0.443 | +0.31 |

Every variant's nearest neighbor is its corresponding original algorithm. But the relative distances are revealing: bubble sort and insertion sort (similarity 0.754) are represented as more similar than iterative and recursive Fibonacci (0.443). The model distinguishes the *computational pattern* — recursion vs iteration — more than it distinguishes two algorithms that solve the same abstract task (sorting) differently.

The near-miss results are equally informative. Sum-to-n maps nearest to factorial (0.473) — both are single-argument recursive accumulations differing only in the operation (addition vs multiplication). Collatz maps to essentially nothing, floating near zero similarity to all existing clusters. The model correctly identifies it as a genuinely novel computation.

<h2>Causal Interventions: A Negative Result</h2>

Correlational evidence, no matter how strong, leaves open the question of whether the model *uses* this representation for generation. I attempted two types of causal intervention: centroid-shifting (replacing the mean activation for one algorithm's cluster with another's) and targeted DAS-style interventions (projecting onto probe-learned algorithm directions). Neither reliably redirected generation — only 2/192 attempted flips succeeded with centroid-shifting, and near-zero with probe directions.

I interpret this as follows: the algorithm representation is genuinely present (the correlational evidence is overwhelming) but the causal mechanism for algorithm-specific generation operates through distributed, token-position-dependent features rather than a single mean-pooled residual stream direction. Token-position probes show that algorithm identity is strongest at the final token positions and exhibits gradients across the sequence. Single-layer, mean-pooled interventions are too coarse to redirect the model's generation behavior.

<h2>Variance Decomposition</h2>

To quantify the geometry more precisely than cosine similarity (which saturated in some experiments), I computed $\eta^2$ (the ratio of between-group to total variance) for both algorithm and language groupings at each layer.

Algorithm $\eta^2$ dominates language $\eta^2$ by 3.5:1 at peak (layer 28). The crossover occurs at layer 53 (~83% depth), matching the cosine similarity crossover from the first experiment.

<h2>Summary</h2>

Taken together, these experiments suggest that Qwen3.5-27B (and to a substantial degree, Qwen3.5-35B-A3B) constructs a representational space in its mid-layers that encodes the *semantic content* of algorithms independent of:

1. **Programming language** (Python, C, JavaScript, Rust, Haskell, Go, Lisp, Bash)
2. **Natural language** (English, French, Russian, Arabic, Mandarin)
3. **Modality** (code vs prose)
4. **Implementation strategy** (recursive vs iterative, though these are distinguished within the space)

This space emerges around 15% of model depth, peaks around 40–55%, and gives way to surface-level features in the final 20% of layers as the model prepares for next-token prediction. The two-phase structure — semantic trunk, syntactic head — replicates across architectures (dense transformer and mixture-of-experts) at the same proportional depth.

The negative causal result is an important caveat: we can observe this representation but cannot yet manipulate it to redirect generation. Whether this reflects a fundamental limitation of linear interventions on distributed representations, or simply insufficient intervention methodology, is an open question.

<h2>Reproducibility</h2>

All code is available at [github.com/laundrevity/research](https://github.com/laundrevity/research) in the `cepa/` directory. Experiments were run on a single consumer machine (AMD Ryzen AI MAX 395+, 128GB LPDDR5X, integrated Radeon 8060S with ROCm 7.2). The full experiment suite runs in under 2 hours.

<h2>Acknowledgments</h2>

Thanks to Claude (Anthropic) for serving as research advisor throughout this project, and to the authors of the platonic representation hypothesis and Ng's cross-language work for the intellectual foundations.
