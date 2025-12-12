import streamlit as st

st.set_page_config(page_title="Máy tính", page_icon="🧮")

st.title("🧮 Máy tính giao diện nút bấm")

# --- STATE ---
if "display" not in st.session_state:
    st.session_state.display = ""

# --- BUTTON FUNCTION ---
def press(btn):
    if btn == "C":
        st.session_state.display = ""
    elif btn == "=":
        try:
            st.session_state.display = str(eval(st.session_state.display))
        except:
            st.session_state.display = "Lỗi!"
    else:
        st.session_state.display += btn

# --- DISPLAY ---
st.text_input("Màn hình", st.session_state.display, disabled=True)

# --- BUTTON LAYOUT ---
buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "C", "+"],
    ["="]
]

# Hiển thị nút theo dạng grid
for row in buttons:
    cols = st.columns(len(row))
    for i, btn in enumerate(row):
        if cols[i].button(btn):
            press(btn)