import os
import json
import base64

files = [
    "README.md",
    "requirements.txt",
    "simulation.py",
    "src/empirical_variance_analysis.py",
    ".gitignore",
    "data/algo-usd.csv",
    "data/bnb-usd.csv",
    "data/usd-vnd.csv",
    "results/opex_var_histogram.txt",
    "results/variance_comparison.txt"
]

all_data = []
for f in files:
    path = os.path.join(os.getcwd(), f)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()
            all_data.append({"path": f, "content": content})

with open("scratch/full_export.json", "w", encoding="utf-8") as out:
    json.dump(all_data, out)
