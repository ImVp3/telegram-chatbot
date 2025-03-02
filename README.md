# 🚀 Telegram Expense Manager Bot

Đây là mã nguồn sử dụng **Langchain** và **PaddleOCR** để làm bot quản lý chi tiêu thông qua **Telegram**. Khi gửi một tin nhắn hoặc một hình ảnh giao dịch chuyển tiền, bot sẽ tự động **trích xuất thông tin** và lưu trữ vào **Google Sheets**. Ngoài ra, bot cũng có thể **phản hồi châm chọc** người dùng dựa trên nội dung tin nhắn.
Vì sử dụng LLM có khả năng hiểu ngôn ngữ khá ổn nên mình không fine-tune lại PaddleOCR mà xài bản gốc luôn dù độ chính xác với Tiếng Việt cũng không quá tốt.

## 🔥 **Tính năng**
- [x] 📩 **Nhận tin nhắn & hình ảnh giao dịch**
- [x] 🔍 **Trích xuất thông tin giao dịch tự động**
- [x] 📊 **Lưu dữ liệu vào Google Sheets**
- [x] 🤖 **Phản hồi châm chọc người dùng**
- [x] 💡 **Hỗ trợ ChatGPT (OpenAI) hoặc Gemini**
- [ ] 📈 **Lập báo cáo chi tiêu hàng tháng**
- [ ] ⚠️ **Cảnh báo chi tiêu vượt mức**
---

## 📌 **Hướng dẫn cài đặt**

### 1️⃣ **Cài đặt các thư viện cần thiết**
```sh
pip install -r requirements.txt
```

### 2️⃣ **Cấu hình biến môi trường**
Tạo một file **`.env`** để lưu trữ các key cần thiết:
```
GOOGLE_API_KEY=your_google_api_key
TELEGRAM_TOKEN=your_telegram_bot_token
OPEN_AI_KEY=your_openai_api_key   # Nếu muốn dùng ChatGPT thay vì Gemini
```

### 3️⃣ **Chạy bot**
```sh
python src/bot.py
```

---

## 🎯 **Công nghệ sử dụng**
- **Langchain** → Xử lý ngôn ngữ tự nhiên
- **PaddleOCR** → Nhận diện chữ từ hình ảnh giao dịch
- **Telegram Bot API** → Giao tiếp với người dùng
- **Google Sheets API** → Lưu trữ dữ liệu chi tiêu

---

## 🛠 **Cần hỗ trợ?**
Nếu bạn gặp vấn đề khi sử dụng hoặc có ý tưởng gì mới, hãy mở một **issue** trên GitHub hoặc liên hệ trực tiếp với tác giả. 🚀

---

# Hình ảnh Demo
<image src = "attachments/telegram.png" width= 40% />
Hình ảnh phản hồi giữa người và bot =))
<image src = "attachments/bill_ggsheet.png"/>

Còn đây là các chi tiêu được trích ra và lưu vào gg sheet