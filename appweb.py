import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Cấu hình trang web
st.set_page_config(page_title="Menu QR Order", page_icon="🍜")
st.title("🍜 Menu Gọi Món Tự Động")

# 2. Kết nối Google Sheets (Thay link của bạn vào đây)
url = "https://docs.google.com/spreadsheets/d/1tgGWynu2yGgA3EyG5gx43qURdhduVDLYr-J7q1RqRO0/edit#gid=0"

conn = st.connection("gsheets", type=GSheetsConnection)


# 3. Danh sách món ăn
menu = {
    "Phở Bò": 50000,
    "Bún Chả": 45000,
    "Cà Phê": 25000,
    "Trà Chanh": 15000
}

# 4. Lấy số bàn từ URL (Ví dụ: myweb.com/?table=5)
query_params = st.query_params
table_number = query_params.get("table", "Chưa xác định")
st.subheader(f"📍 Bàn số: {table_number}")

# 5. Giao diện chọn món
st.write("---")
selected_items = []
total_price = 0

for item, price in menu.items():
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(f"**{item}** - {price:,}đ")
    with col2:
        if st.button(f"Thêm", key=item):
            selected_items.append(item)
            # Lưu tạm vào session_state (bộ nhớ tạm của trình duyệt)
            if 'cart' not in st.session_state:
                st.session_state.cart = []
            st.session_state.cart.append({"Mon": item, "Gia": price})

# 6. Giỏ hàng và Gửi đơn
if 'cart' in st.session_state and len(st.session_state.cart) > 0:
    st.write("---")
    st.subheader("🛒 Giỏ hàng của bạn")
    df_cart = pd.DataFrame(st.session_state.cart)
    st.table(df_cart)
    total = df_cart["Gia"].sum()
    st.write(f"### Tổng cộng: {total:,}đ")

    if st.button("🚀 GỬI ĐƠN HÀNG"):
        # Chuẩn bị dữ liệu lưu vào Google Sheets
        new_order = pd.DataFrame([{
            "Thoi_gian": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Ban": table_number,
            "Mon_an": ", ".join(df_cart["Mon"].tolist()),
            "Tong_tien": total
        }])
        
        # Gửi dữ liệu đi
        existing_data = conn.read(spreadsheet=url)
        updated_df = pd.concat([existing_data, new_order], ignore_index=True)
        conn.update(spreadsheet=url, data=updated_df)
        
        st.success("Đơn hàng đã được gửi! Chúc bạn ngon miệng.")
        st.session_state.cart = [] # Xóa giỏ hàng sau khi đặt





