import os
import sys
import re

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

input_file = "ICBC2025_CameraReady.tex"
output_file = "ICBC2025_Final_v2.tex"

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

replacements = [
    # 1. Xóa lặp ý
    (r"submitting 2\{,\}500 asynchronous transaction groups dispatched at 50 RPS at a sustained target rate of 50 requests per second \(RPS\)", 
     "submitting 2{,}500 asynchronous transaction groups at a sustained target rate of 50 requests per second (RPS)"),
    
    # 2. Sửa Fee Claim
    (r"the execution cost remained consistent at 0\.003 ALGO", 
     "the deployed transaction-group design enforced a fixed configured fee budget of 0.003 ALGO per bid, and no higher fee was required during the benchmark"),
    
    # 3. Sửa Failure Interpretation
    (r"primarily the intended outcome of the smart contract's deterministic validation logic \(state contention\), alongside expected node-side rate limiting during the asynchronous burst", 
     "primarily due to state contention during high-frequency bidding, with additional node-side rate limiting observed under the public API endpoint workload"),
    
    # 4. Sửa Treasury Proxy: Trong Section 5.2, thêm câu.
    # We will find the start of Section 5.2 and add the sentence after the section header or somewhere appropriate.
    # Or just replace the section header and add the sentence right after.
    (r"(\\subsection\{Treasury Analysis & DCA Simulation\}|\\subsection\{.*Treasury.*\})", 
     r"\1\n\nThe treasury evaluation utilizes a stylized DCA proxy under annual-horizon budgeting to assess relative risk reduction.")
]

for old_pattern, new_text in replacements:
    pattern = re.compile(old_pattern, re.IGNORECASE | re.MULTILINE)
    if pattern.search(content):
        content = pattern.sub(new_text, content)
        print(f"OK: Found pattern matching '{old_pattern[:40]}...'")
    else:
        print(f"NOT FOUND: '{old_pattern}'")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nSuccessfully created {output_file}!")
