import os
import sys
import re

# Ensure console output handles UTF-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

input_file = "ICBC2025 (12).tex"
output_file = "ICBC2025_CameraReady.tex"

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

# Define replacements using regex
replacements = [
    # 1. Fix Lỗi Typo Abstract
    (r"while blockchain execution A key design choice is that each bid isare paid", 
     "while blockchain execution costs are paid"),
    
    # 2. Sửa cấu trúc Transaction (Sec 4.2)
    (r"one outer application call and one inner transaction[.,]", 
     "two outer transactions (PaymentTxn and ApplicationCallTxn) and one inner transaction."),
    
    # 3. Sửa cơ chế Dispatch (Sec 5.1)
    (r"2\{,\}500 concurrent transaction groups", 
     "2{,}500 asynchronous transaction groups dispatched at 50 RPS"),
    (r"remained absolutely constant", 
     "remained consistent"),
    
    # 4. Cập nhật số liệu TTF thực tế mới
    (r"6\.11\\,s", r"7.49\\,s"),
    (r"10\.75\\,s", r"16.70\\,s"),
    
    # 5. Cập nhật tỷ lệ Thành công/Thất bại mới
    (r"28\.32\\%", r"13.00\\%"),
    (r"71\.68\\%", r"87.00\\%"),
    
    # 6. Làm rõ nguyên nhân thất bại khách quan
    (r"not the result of network instability or insufficient gas fees; rather, it was the intended outcome of the smart contract's deterministic validation logic", 
     "primarily the intended outcome of the smart contract's deterministic validation logic (state contention), alongside expected node-side rate limiting during the asynchronous burst"),
    
    # 7. Sửa lỗi mâu thuẫn '3 seconds' thành '7.5 seconds'
    (r"median finality of approximately three seconds", 
     "median finality of approximately 7.5 seconds"),
    
    # 8. Cập nhật Limitations Narrative (Sec 7) - FIXED PATTERN
    (r"limited to a single use\s+case, namely public asset auctions, and to a single deterministic-fee\s+instantiation on Algorand TestNet\.", 
     "limited to the observed workload on Algorand MainNet."),
    (r"does not establish long-run production performance under organic MainNet usage\.", 
     "represents a synthetic stress test rather than long-term organic usage."),
    (r"calibrated on historical\s+ALGO and BNB data", 
     "calibrated on historical ALGO price dynamics")
]

for old_pattern, new_text in replacements:
    pattern = re.compile(old_pattern, re.IGNORECASE | re.MULTILINE)
    if pattern.search(content):
        content = pattern.sub(new_text, content)
        print(f"OK: Found pattern matching '{old_pattern[:40]}...'")
    else:
        if "blockchain execution costs are paid" in content and "while blockchain execution A key design choice" in old_pattern:
             print(f"INFO: Abstract typo seems already fixed.")
             continue
        if "limited to the observed workload on Algorand MainNet." in content and "limited to a single use" in old_pattern:
             print(f"INFO: Limitations section seems already updated.")
             continue
        print(f"NOT FOUND: '{old_pattern}'")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nSuccessfully created {output_file}!")
