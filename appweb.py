import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="Menu QR Order", layout="centered")
st.title("🍜 Menu Gọi Món Tự Động")

# 2. LINK GOOGLE SHEETS (Dán link file của bạn vào giữa dấu "")
SHEET_URL = "https://docs.google.com/spreadsheets/d/1X6GzXW0Y_P6W5fO_Y_H8n9X_Y_P6W5fO_Y_H8n9X/edit#gid=0"

# 3. KẾT NỐI DỮ LIỆU
conn = st.connection("gsheets", type=GSheetsConnection)

# Khởi tạo giỏ hàng nếu chưa có
if 'cart' not in st.session_state:
    st.session_state.cart = []

# 4. ĐỌC DỮ LIỆU MENU
try:
    df = conn.read(spreadsheet=SHEET_URL)
    st.subheader("Danh mục món ăn")
    
    # Hiển thị món ăn dạng danh sách đơn giản
    for index, row in df.iterrows():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{row['Mon']}** - {row['Gia']:,}đ")
        with col2:
            if st.button(f"Thêm", key=f"add_{index}"):
                st.session_state.cart.append({"Mon": row['Mon'], "Gia": row['Gia']})
                st.toast(f"Đã thêm {row['Mon']}")

except Exception as e:
    st.error(f"Chưa kết nối được với Sheets: {e}")

# 5. GIỎ HÀNG VÀ GỬI ĐƠN
st.divider()
st.subheader("🛒 Giỏ hàng của bạn")

if st.session_state.cart:
    cart_df = pd.DataFrame(st.session_state.cart)
    st.table(cart_df)
    total = cart_df['Gia'].sum()
    st.write(f"### Tổng cộng: {total:,}đ")

    if st.button("🚀 GỬI ĐƠN HÀNG"):
        try:
            # Ghi dữ liệu vào sheet (Cần file Sheet có các cột tương ứng)
            # conn.update(spreadsheet=SHEET_URL, data=cart_df)
            st.success("Đơn hàng đã được gửi thành công!")
            st.session_state.cart = [] # Xóa giỏ hàng sau khi đặt (Dòng này không được thụt lề sai)
            st.rerun()
        except Exception as ex:
            st.error(f"Lỗi khi gửi đơn: {ex}")
else:
    st.info("Giỏ hàng đang trống.")

