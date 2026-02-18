import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(page_title="Menu QR Order", layout="centered")
st.title("🍜 Menu Gọi Món Tự Động")

# 2. ĐỊNH NGHĨA LINK SHEET (Thay link này bằng link file Sheet của bạn)
# Link này phải là link bạn copy từ trình duyệt khi đang mở file Sheet
SHEET_URL = "https://docs.google.com/spreadsheets/d/1X6GzXW0Y_P6W5fO_Y_H8n9X_Y_P6W5fO_Y_H8n9X/edit#gid=0"

# 3. KẾT NỐI VỚI GOOGLE SHEETS
conn = st.connection("gsheets", type=GSheetsConnection)

# 4. ĐỌC DỮ LIỆU MENU
try:
    # Đọc dữ liệu từ Sheet
    df = conn.read(spreadsheet=SHEET_URL)
    st.success("Kết nối dữ liệu thành công!")
    
    # Hiển thị Menu (Ví dụ đơn giản)
    st.subheader("Danh sách món ăn")
    st.dataframe(df)

except Exception as e:
    st.error(f"Lỗi kết nối: {e}")
    st.info("Hãy kiểm tra lại Secrets và quyền chia sẻ của file Sheet.")

# 5. PHẦN XỬ LÝ ORDER (Bạn có thể thêm code xử lý nút bấm của bạn ở đây)
# Khi bạn muốn ghi đơn hàng vào sheet, hãy dùng: 
# conn.update(spreadsheet=SHEET_URL, data=your_new_dataframe)
        st.session_state.cart = [] # Xóa giỏ hàng sau khi đặt



