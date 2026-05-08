# CPWI: Monetary OPEX VaR Simulation Summary

This document summarizes the quantitative risk analysis for the Algorand B2G Auction system's Operational Expenditure (OPEX).

## 1. Simulation Parameters (Post-MainNet Update)
- **Iteration Count**: 10,000 Monte Carlo runs.
- **Protocol Fee**: 0.003 ALGO per bid (Empirical baseline from MainNet stress test).
- **Projected Annual Traffic**: 50,000 bids.
- **Initial ALGO Price**: $0.12 USD.
- **Volatility ($\sigma$)**: 60% annualized.
- **Horizon ($T$)**: 1 Year.

## 2. Quantitative Risk Metrics

| Metric | Spot Market Baseline | DCA + 50% Reserve |
| :--- | :--- | :--- |
| **Probability of Overrun > 20%** | **27.18%** | **10.03%** |
| **95% Monetary VaR (USD)** | **$22.28** | **$5.57** |
| **99% Monetary VaR (USD)** | **$42.66** | **$10.66** |

## 3. Analysis & Strategy Recommendation

The simulation highlights the high financial risk associated with the **Spot Market Baseline** policy, where ALGO is purchased only when needed. Under this policy, there is a **27.18% probability** that the actual OPEX will exceed the fixed Fiat budget by more than 20%.

In contrast, the **DCA + 50% Reserve** strategy significantly stabilizes costs:
- It reduces the 20% overrun probability by more than half (to **10.03%**).
- It drastically lowers the tail risk (99% VaR) from $42.66 down to **$10.66**.

### Recommendation:
Government agencies deploying on Algorand should adopt a **DCA + Reserve** treasury model to ensure budget predictability and mitigate the impact of native token price volatility.
