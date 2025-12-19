import streamlit as st
import config
import pandas as pd

from database import (
    CategoryModel,
    TransactionModel,
    UserModel,
    BudgetModel
)

from analytics.analyzer import FinanceAnalyzer
from analytics.visualizer import FinanceVisualizer  

from views import (
    render_categories,
    render_transactions,
    render_user_profile,
    render_dashboard,
    render_budget
)

# =============================================
# 0. Page configuration
# =============================================
st.set_page_config(
    page_title="Finance Tracker",
    page_icon="🤑",
    layout="wide"
)

# =============================================
# 1. Initialize models (cached)
# =============================================
@st.cache_resource
def init_models():
    return {
        "category": CategoryModel(),
        "user": UserModel(),
        "transaction": TransactionModel(),
        "budget": BudgetModel(),
        "visualizer": FinanceVisualizer()
    }

if "models" not in st.session_state:
    st.session_state["models"] = init_models()

models = st.session_state["models"]

# =============================================
# 2. Authentication (PUBLIC APP - EMAIL LOGIN)
# =============================================
def require_login():
    if "user_email" not in st.session_state:
        st.session_state.user_email = None

    if not st.session_state.user_email:
        st.title("🔐 Login Required")
        st.caption("Please enter your email to continue")

        email = st.text_input("Email")

        if st.button("Login"):
            if not email or "@" not in email:
                st.error("Please enter a valid email")
            else:
                st.session_state.user_email = email
                st.rerun()

        st.stop()


# Enforce login
require_login()
user_email = st.session_state.user_email

# =============================================
# 3. Login / Create user in MongoDB
# =============================================
user_model: UserModel = models["user"]

try:
    mongo_user_id = user_model.login(user_email)
except Exception as e:
    st.error(f"Error during user login: {e}")
    st.stop()

# Set user_id for all models
models["category"].set_user_id(mongo_user_id)
models["transaction"].set_user_id(mongo_user_id)
models["budget"].set_user_id(mongo_user_id)

# User info object
user_data = {
    "id": mongo_user_id,
    "email": user_email
}

# Render user profile
render_user_profile(user_model, user_data)

# Init analyzer
analyzer_model = FinanceAnalyzer(models["transaction"])

# =============================================
# 4. Sidebar (User + Logout + Navigation)
# =============================================
with st.sidebar:
    st.write(f"👤 {user_email}")
    if st.button("Logout"):
        st.session_state.user_email = None
        st.rerun()

    page = st.radio(
        "Navigation",
        ["Home", "Category", "Transaction", "Budget"]
    )

# =============================================
# 5. Router
# =============================================
if page == "Home":
    st.title("Home")
    render_dashboard(
        analyzer_model=analyzer_model,
        transaction_model=models["transaction"],
        visualizer_model=models["visualizer"]
    )

elif page == "Category":
    render_categories(category_model=models["category"])

elif page == "Transaction":
    render_transactions(
        transaction_model=models["transaction"],
        category_model=models["category"]
    )

elif page == "Budget":
    render_budget(
        budget_model=models["budget"],
        category_model=models["category"],
        transaction_model=models["transaction"]
    )
