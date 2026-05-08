# CPWI: Web3 B2G Infrastructure OPEX Simulation & MainNet Validation

This repository provides a comprehensive framework for simulating, validating, and testing the Operational Expenditure (OPEX) risks of a Government-to-Business (B2G) auction system built on the Algorand blockchain. It combines theoretical Monte Carlo simulations with empirical data analysis and real-world MainNet stress testing.

## 📌 Project Overview

Developing public infrastructure on a decentralized blockchain introduces financial volatility. This project quantifies the risk of cost overruns when using $ALGO for transaction fees and evaluates treasury management strategies to mitigate these risks using probabilistic modeling.

### Core Objectives:
1.  **Risk Quantification**: Using Monte Carlo simulations to calculate Monetary Value-at-Risk (VaR).
2.  **Empirical Validation**: Analyzing historical data to justify the simplified volatility model.
3.  **Real-World Stress Testing**: Deploying a smart contract to Algorand MainNet to measure actual Time-to-Finality (TTF) and Protocol Fees under load, with built-in compliance mechanics (Time Window & KYC Simulation).

---

## 🛠 Project Structure

### 1. Financial Simulation (`simulation.py`)
Predicts the probability of budget overruns over a 1-year horizon using **Geometric Brownian Motion (GBM)**.
- **Policies Compared**: Spot Market Baseline vs. **DCA + 50% Reserve** (Recommended).
- **Update**: Parameters updated after MainNet testing (Fee set to 0.003 ALGO to account for inner transactions).

### 2. Empirical Analysis (`src/empirical_variance_analysis.py`)
Validates that the variance of the Token/Fiat (ALGO/USD) pair is the dominant risk factor compared to Fiat/Local (USD/VND) exchange rate fluctuations.

### 3. MainNet Stress Test (`mainnet_stress_test/`)
A suite of tools for real-world validation on the Algorand MainNet.
- `auction_contract.py`: A PyTeal-based smart contract featuring inner transaction refunds, a 24-hour time window constraint, and a participant Opt-in requirement (KYC/Whitelist simulation).
- `deploy_mainnet.py`: Deployment automation script.
- `async_benchmark.py`: High-concurrency stress tester (50 RPS) using `asyncio`.
- `utils.py`: Account sanity checks and balance monitoring.

---

## 📊 Key Results

### Monte Carlo Simulation (10,000 Iterations)
| Metric | Spot Market Baseline | DCA + 50% Reserve |
| :--- | :--- | :--- |
| **Overrun Prob (> 20% budget)** | **27.18%** | **10.03%** |
| **95% Monetary VaR** | $22.28 | $5.57 |
| **99% Monetary VaR** | $42.66 | $10.66 |

### MainNet Stress Test Findings (App ID: `3548200231`)
- **Node**: AlgoNode MainNet.
- **Median Time-to-Finality (TTF)**: ~6.11 seconds.
- **P95 TTF**: ~10.75 seconds.
- **Protocol Fee**: Constant 0.003 ALGO per transaction group (Payment + AppCall + Inner Refund).

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Algorand account with ~15-20 ALGO (for MainNet tests).

### Installation
```bash
pip install -r requirements_mainnet.txt
```

### Configuration
1. Rename `.env.example` to `.env`.
2. Fill in your `MAINNET_MNEMONIC` and `ALGOD_ADDRESS`.

### Execution
1. **Run Simulation**: `python simulation.py`
2. **Run Empirical Analysis**: `python src/empirical_variance_analysis.py`
3. **Run MainNet Stress Test**: `python mainnet_stress_test/async_benchmark.py`

---

## 📄 Documentation
- [Simulation Summary](results/simulation_summary.md)
- [MainNet Summary Report](mainnet_summary_report.txt)
- [Updated Treasury Results](updated_treasury_results.txt)

## 🛡 Disclaimer
This project is for academic and research purposes only. Blockchain MainNet transactions involve real financial costs. Use the included Circuit Breaker mechanisms to protect your funds.
