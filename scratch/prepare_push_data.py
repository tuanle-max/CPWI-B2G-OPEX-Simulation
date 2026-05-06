import os
import json

files_to_push = [
    "data/algo-usd.csv",
    "data/bnb-usd.csv",
    "data/usd-vnd.csv",
    "results/opex_var_histogram.txt",
    "results/variance_comparison.txt"
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
