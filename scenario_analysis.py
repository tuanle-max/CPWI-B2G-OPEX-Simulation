from simulation import run_simulation

scales = [50000, 500000, 5000000]

print(f"{'Scale (Bids/Year)':<20} | {'Nominal OPEX (USD)':<20} | {'99% Spot VaR (USD)':<20} | {'99% DCA VaR (USD)':<20} | {'Absolute Risk Reduction (USD)':<30}")
print("-" * 120)

for scale in scales:
    res = run_simulation(expected_bids=scale)
    
    nom_opex = res["FIAT_BUDGET_USD"]
    spot_var = res["var_99_spot"]
    dca_var = res["var_99_dca"]
    reduction = spot_var - dca_var
    
    print(f"{scale:<20} | ${nom_opex:<19.2f} | ${spot_var:<19.2f} | ${dca_var:<19.2f} | ${reduction:<29.2f}")
