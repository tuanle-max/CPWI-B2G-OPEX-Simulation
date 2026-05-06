import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- 1. Input Parameters ---
NUM_ITERATIONS = 10000
EXPECTED_BIDS = 50000  # Total operations needed in the fiscal year
FEE_PER_BID_ALGO = 0.002  # Deterministic protocol fee
ALGO_PRICE_INITIAL = 0.11967973796573292  # USD price on May 06, 2026
VOLATILITY = 0.60  # Annualized volatility (60%)
FIAT_BUDGET_USD = 20.0  # Fixed B2G fiat contract budget (EXPECTED_BIDS * FEE_PER_BID_ALGO * ALGO_PRICE_INITIAL)

# For reproducibility
np.random.seed(42)

# --- 2. Simulation Logic (GBM) ---
# T = 1 year
# S_T = S_0 * exp((r - 0.5 * sigma^2) * T + sigma * sqrt(T) * Z)
# Assuming risk-free rate r = 0 for simplicity in OPEX projections
Z = np.random.standard_normal(NUM_ITERATIONS)
algo_prices_end_year = ALGO_PRICE_INITIAL * np.exp(-0.5 * VOLATILITY**2 + VOLATILITY * Z)

# --- 3. Policy Cost Calculations ---

# A. Spot Baseline Policy
# All fees paid at end-of-year price (worst-case assumption for risk modeling)
total_algo_needed = EXPECTED_BIDS * FEE_PER_BID_ALGO
costs_spot = total_algo_needed * algo_prices_end_year

# B. DCA + 50% Reserve Policy
# Logic: 
# 1. 50% of tokens bought upfront (Reserve) at ALGO_PRICE_INITIAL
# 2. 50% of tokens bought via DCA. Average price ≈ (S_0 + S_T) / 2
reserve_tokens = total_algo_needed * 0.50
dca_tokens = total_algo_needed * 0.50

upfront_reserve_cost_usd = reserve_tokens * ALGO_PRICE_INITIAL
avg_dca_price = (ALGO_PRICE_INITIAL + algo_prices_end_year) / 2
costs_dca_portion = dca_tokens * avg_dca_price

# Total Cash Outlay (Initial Accounting)
total_cash_outlay = upfront_reserve_cost_usd + costs_dca_portion

# Critical Fix: Mark-to-Market Reserve Asset
# Unused reserve tokens are assets. Since we use them for OPEX, 
# the "Net OPEX" is (Cash Outlay) - (Value of Reserve if it were sold at S_T)
# OR more simply: Net_OPEX = Upfront_Cost + DCA_Cost - End_Value_of_Reserve
reserve_asset_value_end = reserve_tokens * algo_prices_end_year
net_opex_dca_reserve = total_cash_outlay - reserve_asset_value_end

# --- 4. VaR Calculation (95% Confidence) ---
overrun_spot = costs_spot - FIAT_BUDGET_USD
overrun_dca = net_opex_dca_reserve - FIAT_BUDGET_USD

var_95_spot = np.percentile(overrun_spot, 95)
var_95_dca = np.percentile(overrun_dca, 95)

# --- 5. Output & Visualization ---
print(f"--- Monte Carlo Simulation Results ({NUM_ITERATIONS} iterations) ---")
print(f"Fiat Budget: ${FIAT_BUDGET_USD:.2f}")
print(f"Spot Baseline 95% VaR: ${var_95_spot:.2f}")
print(f"DCA + 50% Reserve 95% VaR: ${var_95_dca:.2f}")
print(f"Risk Reduction: {((var_95_spot - var_95_dca) / var_95_spot)*100:.2f}%")

plt.figure(figsize=(10, 6))
plt.hist(overrun_spot, bins=50, alpha=0.5, label='Spot Baseline Overrun', color='red')
plt.hist(overrun_dca, bins=50, alpha=0.5, label='DCA + 50% Reserve Overrun', color='blue')
plt.axvline(var_95_spot, color='darkred', linestyle='--', label=f'Spot VaR: ${var_95_spot:.2f}')
plt.axvline(var_95_dca, color='darkblue', linestyle='--', label=f'DCA VaR: ${var_95_dca:.2f}')
plt.title('OPEX Overrun Distribution: Spot vs. Hedged Policy')
plt.xlabel('Budget Overrun (USD)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)

# Save result
os.makedirs('results', exist_ok=True)
plt.savefig('results/opex_var_histogram.png')
plt.close()
