# CPWI B2G OPEX Simulation - MainNet Stress Test

Thư mục này chứa các kịch bản và cấu hình để thực hiện stress test và triển khai thực tế trên Algorand MainNet.

## Hướng dẫn An toàn (Security Warning & Best Practices)

**KHÔNG BAO GIỜ COMMIT TỆP `.env` LÊN GITHUB!** 
Tệp `.gitignore` đã được cấu hình để bỏ qua `.env`, nhưng hãy luôn cẩn thận. Tuyệt đối không để lộ `MAINNET_MNEMONIC`.

### 1. Khởi tạo ví MainNet mới
- **Bắt buộc**: Tạo một ví MainNet mới hoàn toàn chỉ dành riêng cho mục đích stress test (sử dụng Pera Wallet, Defly Wallet, hoặc thuật toán tạo ví của SDK).
- Không sử dụng ví cá nhân đang lưu trữ tài sản lớn.

### 2. Cấp vốn cho ví (Funding)
- Chỉ nạp **vừa đủ** số lượng ALGO cần thiết cho bài test.
- Với các bài test này, khuyến cáo nạp khoảng **15-20 ALGO** là đủ để:
  - Chi trả phí giao dịch (thường là 0.001 ALGO mỗi giao dịch).
  - Đáp ứng yêu cầu số dư tối thiểu (Minimum Balance Requirement - MBR) khi tạo Smart Contract hoặc Opt-in tài sản.

### 3. Thiết lập biến môi trường
- Sao chép tệp mẫu để tạo tệp `.env` thực tế của bạn:
  ```bash
  cp .env.example .env
  ```
- Mở tệp `.env` và điền đầy đủ thông tin:
  - `MAINNET_MNEMONIC`: Cụm 25 từ khóa bí mật của ví test.
  - `PURESTAKE_API_TOKEN`: API Token truy cập node MainNet (như PureStake, AlgoNode, hoặc Nodely).
  - `APP_ID`: ID của Smart Contract (bạn sẽ có ID này sau khi chạy script deploy).
