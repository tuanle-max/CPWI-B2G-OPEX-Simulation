# CPWI-B2G-OPEX-Simulation

Monte Carlo simulation and empirical variance analysis for Web3 B2G (Business-to-Government) infrastructure Operational Expenditure (OPEX) management.

## Project Overview

This repository contains tools to analyze and simulate the monetary risks associated with crypto-based protocol fees in B2G contracts. Specifically, it compares different treasury management policies for Algorand-based auction systems.

### Key Components

1.  **Monte Carlo Simulation (`simulation.py`)**: 
    - Calculates Monetary Value-at-Risk (VaR) for OPEX overruns.
    - Compares "Spot Market Baseline" vs. "DCA + 50% Reserve" policies.
    - Isolates Net OPEX from Reserve Assets (Mark-to-Market).

2.  **Empirical Variance Analysis (`src/empirical_variance_analysis.py`)**:
    - Validates the assumption that Fiat-to-Local (e.g., USD/VND) exchange rate variance is negligible compared to Token-to-Fiat (e.g., ALGO/USD) variance.
    - Performs variance decomposition using historical data from Jan 2024 to May 2026.

## Data

The simulation relies on historical price data located in the `data/` folder:
- `algo-usd.csv`: Historical ALGO/USD prices.
- `bnb-usd.csv`: Historical BNB/USD prices (for comparison).
- `usd-vnd.csv`: Historical USD/VND exchange rates.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Run OPEX Simulation
```bash
python simulation.py
```

### Run Empirical Variance Analysis
```bash
python src/empirical_variance_analysis.py
```

## Results

Results and visualizations are stored in the `results/` directory.

- `opex_var_histogram.png`: Distribution of OPEX costs across policies.
- `variance_comparison.png`: Comparison of annualized variances (Log Scale).

---
*Developed as part of a Q1 academic paper on Web3 B2G Infrastructure.*
