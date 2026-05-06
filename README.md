# Web3 B2G Infrastructure OPEX Simulation

This repository contains a standalone Python script designed to run a 10,000-iteration Monte Carlo simulation. It calculates the Monetary Value-at-Risk (VaR) of Operational Expenditure (OPEX) overruns for an Algorand-based B2G auction system.

## Mathematical Model

The simulation employs the **Geometric Brownian Motion (GBM)** model to predict end-of-year Algorand ($ALGO) prices. The formula used is:

$$S_T = S_0 \times \exp\left((0 - 0.5 \times \sigma^2) \times T + \sigma \times \sqrt{T} \times Z\right)$$

Where:
- $S_T$ = Simulated end-of-year ALGO price
- $S_0$ = Initial ALGO price
- $\sigma$ = Annualized volatility (60%)
- $T$ = Time horizon (1 year)
- $Z$ = Standard normal random variable

### Policy Comparison
1. **Spot Market Baseline**: The organization buys ALGO at the end-of-year simulated price $S_T$.
2. **DCA + 50% Reserve**: The organization purchases 50% more tokens upfront/progressively, assuming an average purchase price of $P_{dca} = (S_0 + S_T) / 2$.

## How to Run

### Prerequisites
Ensure you have Python 3.8+ installed.

### Installation
Install the exact dependencies to ensure reproducibility:
```bash
pip install -r requirements.txt
```

### Execution
Run the simulation script or the empirical validation script from the root directory:
```bash
# To run the Monte Carlo simulation
python simulation.py

# To run the empirical variance analysis
python src/empirical_variance_analysis.py
```

### Empirical Validation
The script `src/empirical_variance_analysis.py` validates the assumption that the Fiat-to-Local (USD/VND) exchange rate variance is negligible compared to the Token-to-Fiat (ALGO/USD) variance. This is a critical prerequisite for the simplified OPEX model used in the academic paper.

### Results
- `results/opex_var_histogram.png`: Distribution of cost overruns for both policies.
- `results/variance_comparison.png`: Comparison of annualized variances (ALGO vs. BNB vs. USD/VND).

