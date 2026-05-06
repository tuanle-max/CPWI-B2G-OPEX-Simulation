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
Run the simulation script from the root directory:
```bash
python simulation.py
```

### Expected Output
The script will print a markdown-formatted table with the risk metrics (Probability of >20% overrun, 95% VaR, 99% VaR) directly to your console. It will also generate a high-quality histogram comparing the cost overruns of both policies, saved as `results/opex_var_histogram.png`.
