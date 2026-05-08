import os

input_file = "ICBC2026_Final.tex"
output_file = "ICBC2026_Final_Scaled.tex"

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Đổi tên Mục 5.2 hiện tại để thể hiện nó chỉ là baseline quy mô nhỏ
old_heading = r"\subsection{Treasury Risk Analysis}"
new_heading = r"\subsection{Technical Proof-of-Concept: Small-Scale Baseline}"
content = content.replace(old_heading, new_heading)

# 2. Nội dung tiếng Anh học thuật cho Mục 5.3 mới (Sử dụng số liệu chính xác tuyệt đối)
section_5_3 = r"""
\subsection{Economic Scalability and Industrial Thresholds}
While the 50,000-bid baseline successfully demonstrates the relative risk reduction of the DCA policy, its nominal OPEX (\$18.00) is too small to justify the administrative overhead of a complex treasury operation. To evaluate the practical business value of the CPWI architecture for large-scale Auction Organizers (AOs), we conducted a scenario analysis scaling the operational volume to regional (500,000 bids) and national (5,000,000 bids) levels.

\begin{table}[hbt!]
\centering
\caption{Treasury OPEX Risk Analysis Across Operational Scales (Base Price: \$0.12, Fee: 0.003 ALGO)}
\label{tab:scenario_analysis}
\resizebox{\columnwidth}{!}{%
\begin{tabular}{|l|c|c|c|c|}
\hline
\textbf{Scale (Bids/Year)} & \textbf{Nominal OPEX} & \textbf{99\% Spot VaR} & \textbf{99\% DCA VaR} & \textbf{Absolute Risk Reduction} \\ \hline
Small (50,000) & \$18.00 & \$42.66 & \$10.66 & \$31.99 \\ \hline
Regional (500,000) & \$180.00 & \$426.59 & \$106.65 & \$319.94 \\ \hline
National (5,000,000) & \$1,800.00 & \$4,265.91 & \$1,066.48 & \$3,199.43 \\ \hline
\end{tabular}%
}
\end{table}

As shown in Table \ref{tab:scenario_analysis}, while the relative overrun probability remains invariant due to the proportional nature of geometric Brownian motion, the absolute monetary value protected by the treasury policy scales significantly. At a national scale of 5 million bids per year, the baseline OPEX increases to \$1,800.00. Under severe market stress (99\% VaR), an unhedged spot-purchasing strategy exposes the AO to potential losses exceeding \$4,265.91. Implementing the DCA and 50\% reserve policy compresses this extreme tail risk to \$1,066.48, yielding an absolute risk reduction of \$3,199.43. 

Furthermore, if the protocol fee structure incorporates additional on-chain compliance operations (e.g., ASA minting, final asset transfers, or document hashing), this baseline OPEX---and the corresponding absolute savings---would multiply. These results confirm that while fee determinism is a technical prerequisite, the CPWI treasury model delivers its primary industrial value in high-volume, national-scale deployments where absolute financial exposure is substantial enough to warrant treasury management.
"""

# 3. Tìm chính xác vị trí chèn: Ngay trước Section 6
target_section = r"\section{Operational Implications for Auction Organizers}"
if target_section in content:
    content = content.replace(target_section, section_5_3 + "\n\n" + target_section)
    print("SUCCESS: Da tim thay vi tri va chen thanh cong Muc 5.3!")
else:
    print("ERROR: Khong tim thay heading Section 6 de chen.")

# 4. Ghi ra file mới
with open(output_file, "w", encoding="utf-8") as f:
    f.write(content)

print(f"DONE: Da luu tep hoan thien tai: {output_file}")
