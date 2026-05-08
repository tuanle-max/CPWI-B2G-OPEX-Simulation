import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def run_simulation(expected_bids=50000, fee_per_bid_algo=0.003, algo_price_initial=0.12, num_iterations=10000, volatility=0.9395, drift=0.0):
    # Strict Reproducibility
    np.random.seed(42)

    # 1. Input Parameters
    FIAT_BUDGET_USD = expected_bids * fee_per_bid_algo * algo_price_initial

    # 2. Simulation Logic (Geometric Brownian Motion)
    T = 1.0
    # Z is a standard normal random variable
    Z = np.random.standard_normal(num_iterations)
    S_T = algo_price_initial * np.exp((drift - 0.5 * volatility**2) * T + volatility * np.sqrt(T) * Z)

    # 3. Policy Cost Calculations
    # Spot Baseline Cost
    cost_spot = expected_bids * fee_per_bid_algo * S_T

    # DCA + 50% Reserve Cost (Net OPEX Accounting)
    P_dca = (algo_price_initial + S_T) / 2.0
    total_spent = expected_bids * 1.5 * fee_per_bid_algo * P_dca
    reserve_tokens = expected_bids * 0.5 * fee_per_bid_algo
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

    return {
        "FIAT_BUDGET_USD": FIAT_BUDGET_USD,
        "prob_overrun_20_spot": prob_overrun_20_spot,
        "prob_overrun_20_dca": prob_overrun_20_dca,
        "var_95_spot": var_95_spot,
        "var_95_dca": var_95_dca,
        "var_99_spot": var_99_spot,
        "var_99_dca": var_99_dca,
        "overrun_spot": overrun_spot,
        "overrun_dca": overrun_dca
    }

if __name__ == "__main__":
    results = run_simulation()
    
    # 5. Output formatting
    print("### Monetary OPEX VaR Simulation Results\n")
    print("| Metric | Spot Market Baseline | DCA + 50% Reserve (Net OPEX) |")
    print("|--------|----------------------|------------------------------|")
    print(f"| Prob of Overrun > 20% budget | {results['prob_overrun_20_spot']:.2f}% | {results['prob_overrun_20_dca']:.2f}% |")
    print(f"| 95% Monetary OPEX VaR | ${results['var_95_spot']:.4f} | ${results['var_95_dca']:.4f} |")
    print(f"| 99% Monetary OPEX VaR | ${results['var_99_spot']:.4f} | ${results['var_99_dca']:.4f} |\n")

    # Generate Plot
    plt.figure(figsize=(10, 6))

    # Use custom colors and styling for publication-ready chart
    plt.hist(results['overrun_spot'], bins=50, alpha=0.6, label='Spot Market Baseline', color='#e63946', edgecolor='black')
    plt.hist(results['overrun_dca'], bins=50, alpha=0.6, label='DCA + 50% Reserve (Net OPEX)', color='#457b9d', edgecolor='black')

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
