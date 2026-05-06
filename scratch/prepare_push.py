import os
import json
import base64

files_to_push = [
    "README.md",
    "requirements.txt",
    "simulation.py",
    "data/algo-usd.csv",
    "data/bnb-usd.csv",
    "data/usd-vnd.csv",
    "results/opex_var_histogram.txt",
    "results/variance_comparison.txt",
    "scratch/encode_results.py",
    "src/empirical_variance_analysis.py"
]

result = []
for file_path in files_to_push:
    full_path = os.path.join(os.getcwd(), file_path.replace("/", os.sep))
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            result.append({
                "path": file_path,
                "content": content
            })

print(json.dumps(result))
