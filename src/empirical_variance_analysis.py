import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Data Loading & Cleaning function
def load_and_clean(file_path):
    df = pd.read_csv(file_path)
    # Ensure columns are named 'Date' and 'Price'. 
    # If CSV has extra whitespace in headers
    df.columns = df.columns.str.strip()
    
    # If standard names aren't present, assume the first two are Date and Price
    if 'Date' not in df.columns or 'Price' not in df.columns:
        df.columns = ['Date', 'Price'] + list(df.columns[2:])
        
    df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
    df = df.sort_values('Date').reset_index(drop=True)
    
    # Clean Price: remove commas, convert to float
    df['Price'] = df['Price'].astype(str).str.replace(',', '', regex=False).astype(float)
        
    # Calculate daily log returns
    df['Log_Return'] = np.log(df['Price'] / df['Price'].shift(1))
    df = df.dropna(subset=['Log_Return'])
    
    return df

def main():
    # Load data
    algo_df = load_and_clean('data/algo-usd.csv')
    bnb_df = load_and_clean('data/bnb-usd.csv')
    usdvnd_df = load_and_clean('data/usd-vnd.csv')

    # Filter timeframe: Jan 01, 2024 to May 05, 2026
    start_date = pd.to_datetime('2024-01-01')
    end_date = pd.to_datetime('2026-05-05')

    algo_df = algo_df[(algo_df['Date'] >= start_date) & (algo_df['Date'] <= end_date)]
    bnb_df = bnb_df[(bnb_df['Date'] >= start_date) & (bnb_df['Date'] <= end_date)]
    usdvnd_df = usdvnd_df[(usdvnd_df['Date'] >= start_date) & (usdvnd_df['Date'] <= end_date)]

    # Calculate Annualized Variance
    var_algo = algo_df['Log_Return'].var() * 365
    var_bnb = bnb_df['Log_Return'].var() * 365
    var_usdvnd = usdvnd_df['Log_Return'].var() * 365

    # Variance Decomposition
    contrib_algo = (var_usdvnd / (var_algo + var_usdvnd)) * 100
    contrib_bnb = (var_usdvnd / (var_bnb + var_usdvnd)) * 100

    # Console Output
    print("### Empirical Variance Analysis (Annualized)\n")
    print("| Asset Pair | Annualized Variance |")
    print("|------------|---------------------|")
    print(f"| ALGO/USD   | {var_algo:.6f}            |")
    print(f"| BNB/USD    | {var_bnb:.6f}            |")
    print(f"| USD/VND    | {var_usdvnd:.6f}            |")
    print("\n### Variance Decomposition")
    print(f"- USD/VND contribution to ALGO OPEX variance: {contrib_algo:.4f}%")
    print(f"- USD/VND contribution to BNB OPEX variance: {contrib_bnb:.4f}%\n")

    # Academic Conclusion
    is_negligible = contrib_algo < 1.0 and contrib_bnb < 1.0
    conclusion = (f"The empirical analysis confirms that the USD/VND exchange rate variance contribution is "
                  f"{'statistically negligible (< 1%)' if is_negligible else 'NOT statistically negligible (> 1%)'}, "
                  f"thus {'justifying' if is_negligible else 'challenging'} the assumption "
                  r"\mathbb{V}[\mathcal{E}_{F/L}] \approx 0 in the OPEX model.")
    print(conclusion)

    # Visualization
    labels = ['ALGO/USD', 'BNB/USD', 'USD/VND']
    variances = [var_algo, var_bnb, var_usdvnd]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, variances, color=['#e63946', '#f4a261', '#2a9d8f'], edgecolor='black')
    
    # Log scale for Y-axis because crypto variance is orders of magnitude larger
    plt.yscale('log')
    plt.title('Annualized Variance Comparison (Log Scale)', fontsize=14, fontweight='bold')
    plt.ylabel('Annualized Variance (Log Scale)', fontsize=12)

    # Data labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval * 1.5, f'{yval:.6f}', 
                 ha='center', va='bottom', fontsize=11, fontweight='bold')

    plt.ylim(top=max(variances) * 10)
    plt.grid(axis='y', alpha=0.4, linestyle='--')

    os.makedirs('results', exist_ok=True)
    plt.savefig('results/variance_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    main()
