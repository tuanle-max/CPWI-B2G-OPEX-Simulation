import os

input_file = "ICBC2026_Final_Scaled.tex"

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

# Danh sách thay thế chính xác 100% (Raw strings để xử lý an toàn ký tự \$ và \% của LaTeX)
replacements = {
    # 1. Cập nhật giải thích về Volatility Input
    r"\sigma_{\text{ALGO}}=0.60": r"\sigma_{\text{ALGO}}=0.94 (derived from the empirical variance of 0.88)",
    
    # 2. Cập nhật Xác suất Overrun > 20%
    r"27.18\%": r"25.23\%",
    r"10.03\%": r"13.75\%",
    
    # 3. Cập nhật 95% Monetary OPEX VaR (Quy mô 50k)
    r"\$22.29": r"\$36.18",
    r"\$5.57": r"\$9.05",
    
    # 4. Cập nhật 99% VaR & Absolute Risk Reduction - Quy mô Small (50k)
    r"\$42.66": r"\$84.84",
    r"\$10.66": r"\$21.21",
    r"\$31.99": r"\$63.63",
    
    # 5. Cập nhật 99% VaR & Absolute Risk Reduction - Quy mô Regional (500k)
    r"\$426.59": r"\$848.45",
    r"\$106.65": r"\$212.11",
    r"\$319.94": r"\$636.34",
    
    # 6. Cập nhật 99% VaR & Absolute Risk Reduction - Quy mô National (5M)
    r"\$4,265.91": r"\$8,484.47",
    r"\$1,066.48": r"\$2,121.12",
    r"\$3,199.43": r"\$6,363.35"
}

# Thực hiện quét và thay thế
for old_text, new_text in replacements.items():
    if old_text in content:
        content = content.replace(old_text, new_text)
        print(f"DONE: {old_text} -> {new_text}")
    else:
        print(f"WARNING: Khong tim thay chuoi '{old_text}' trong file.")

with open(input_file, "w", encoding="utf-8") as f:
    f.write(content)

print("\nHoan tat! Da dong bo so lieu VaR moi len toan bo file LaTeX.")
