import os
import json

files_to_push = [
    "simulation.py",
    "src/empirical_variance_analysis.py",
    "mainnet_stress_test/auction_contract.py",
    "mainnet_stress_test/async_benchmark.py",
    "mainnet_stress_test/deploy_mainnet.py",
    "mainnet_stress_test/utils.py",
    "README.md",
    "results/simulation_summary.md",
    "updated_treasury_results.txt",
    "requirements.txt",
    "requirements_mainnet.txt",
    ".gitignore"
]

payload = []
for f in files_to_push:
    if os.path.exists(f):
        with open(f, "r", encoding="utf-8") as file:
            payload.append({
                "path": f,
                "content": file.read()
            })

print(json.dumps(payload))
