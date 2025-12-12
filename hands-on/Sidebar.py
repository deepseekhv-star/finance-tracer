import streamlit as st

with st.sidebar:
    st.header("User Info")
    username = st.text_input("Tên đăng nhập")
    password = st.text_input("Mật khẩu", type="password")

    st.header("Cài đặt hiển thị")
    dark_mode = st.checkbox("Dark mode")




st.sidebar.title("📌 Menu")
page = st.sidebar.radio(
    "Chọn trang:",
    ["🏠 Home", "📂 Categories", "➕ Add Category"]
)

if page == "🏠 Home":
    st.title("Home Page")

elif page == "📂 Categories":
    st.title("Danh sách Categories")

elif page == "➕ Add Category":
    st.title("Thêm Category mới")