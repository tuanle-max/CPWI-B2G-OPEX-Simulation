import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Strict Reproducibility
np.random.seed(42)

# 1. Input Parameters
NUM_ITERATIONS = 10000
EXPECTED_BIDS = 50000 
FEE_PER_BID_ALGO = 0.003 
ALGO_PRICE_INITIAL = 0.12 
VOLATILITY = 0.60 
FIAT_BUDGET_USD = EXPECTED_BIDS * FEE_PER_BID_ALGO * ALGO_PRICE_INITIAL

# 2. Simulation Logic (Geometric Brownian Motion)
T = 1.0
drift = 0.0
# Z is a standard normal random variable
Z = np.random.standard_normal(NUM_ITERATIONS)
S_T = ALGO_PRICE_INITIAL * np.exp((drift - 0.5 * VOLATILITY**2) * T + VOLATILITY * np.sqrt(T) * Z)

# 3. Policy Cost Calculations
# Spot Baseline Cost
cost_spot = EXPECTED_BIDS * FEE_PER_BID_ALGO * S_T

# DCA + 50% Reserve Cost (Net OPEX Accounting)
P_dca = (ALGO_PRICE_INITIAL + S_T) / 2.0
total_spent = EXPECTED_BIDS * 1.5 * FEE_PER_BID_ALGO * P_dca
reserve_tokens = EXPECTED_BIDS * 0.5 * FEE_PER_BID_ALGO
reserve_value_eoy = reserve_tokens * S_T
cost_dca_net = total_spent - reserve_value_eoy

# 4. Risk Metrics (Overrun vs. Budget)
overrun_spot = np.maximum(0, cost_spot - FIAT_BUDGET_USD)
overrun_dca = np.maximum(0, cost_dca_net - FIAT_BUDGET_USD)

# Metric 1: Probability of cost overrun > 20% of the FIAT_BUDGET_USD
threshold = 0.20 * FIAT_BUDGET_USD
prob_overrun_20_spot = np.mean(overrun_spot > threshold) * 100
prob_overrun_20_dca = np.mean(overrun_dca > threshold) * 100

# Metric 2: 95% Monetary OPEX VaR
var_95_spot = np.percentile(overrun_spot, 95)
var_95_dca = np.percentile(overrun_dca, 95)

# Metric 3: 99% Monetary OPEX VaR
var_99_spot = np.percentile(overrun_spot, 99)
var_99_dca = np.percentile(overrun_dca, 99)

# 5. Output formatting
print("### Monetary OPEX VaR Simulation Results\n")
print("| Metric | Spot Market Baseline | DCA + 50% Reserve (Net OPEX) |")
print("|--------|----------------------|------------------------------|")
print(f"| Prob of Overrun > 20% budget | {prob_overrun_20_spot:.2f}% | {prob_overrun_20_dca:.2f}% |")
print(f"| 95% Monetary OPEX VaR | ${var_95_spot:.4f} | ${var_95_dca:.4f} |")
print(f"| 99% Monetary OPEX VaR | ${var_99_spot:.4f} | ${var_99_dca:.4f} |\n")

# Generate Plot
plt.figure(figsize=(10, 6))

# Use custom colors and styling for publication-ready chart
plt.hist(overrun_spot, bins=50, alpha=0.6, label='Spot Market Baseline', color='#e63946', edgecolor='black')
plt.hist(overrun_dca, bins=50, alpha=0.6, label='DCA + 50% Reserve (Net OPEX)', color='#457b9d', edgecolor='black')

plt.title('Cost Overrun Distributions: Spot vs. DCA + 50% Reserve (Net OPEX)', fontsize=14, fontweight='bold')
plt.xlabel('Cost Overrun (USD)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.legend(loc='upper right', fontsize=11)
plt.grid(axis='y', alpha=0.4, linestyle='--')

# Save the plot
os.makedirs('results', exist_ok=True)
output_path = os.path.join('results', 'opex_var_histogram.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"Plot successfully saved to {output_path}")
