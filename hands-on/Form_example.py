import streamlit as st
from datetime import date, time, datetime

st.set_page_config(page_title="Form nhập liệu", page_icon="📝")

st.title("📝 Form nhập liệu đầy đủ")

# --- FORM ---
with st.form("my_form", clear_on_submit=False):
    st.subheader("Thông tin chung")

    # text input
    ten = st.text_input("Họ và tên")

    # number
    tuoi = st.number_input("Tuổi", min_value=0, max_value=120, step=1)

    # date
    ngay = st.date_input("Ngày thực hiện", value=date.today())

    # time
    gio = st.time_input("Giờ thực hiện", value=time(12, 0))

    # dropdown
    loai_congviec = st.selectbox(
        "Loại công việc",
        ["Báo cáo", "Họp", "Nghiên cứu", "Khác"]
    )

    # checkbox
    xacnhan = st.checkbox("Xác nhận thông tin là chính xác")

    # submit button
    submitted = st.form_submit_button("📌 Gửi")

# --- PROCESS RESULT ---
if submitted:
    if not xacnhan:
        st.warning("Bạn cần tick xác nhận trước khi gửi!")
    else:
        dt = datetime.combine(ngay, gio)

        st.success("Dữ liệu đã ghi nhận!")
        st.write("### 📄 Thông tin đã nhập:")
        st.write(f"**Họ tên:** {ten}")
        st.write(f"**Tuổi:** {tuoi}")
        st.write(f"**Loại công việc:** {loai_congviec}")
        st.write(f"**Ngày giờ:** {dt}")