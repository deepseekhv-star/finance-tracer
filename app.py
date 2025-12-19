import streamlit as st
import config
import pandas as pd
#from database.category_models import CategoryModel 
#Hoac
from database import (
    CategoryModel,
    TransactionModel,
    UserModel,
    BudgetModel
)

from analytics.analyzer import FinanceAnalyzer
from analytics.visualizer import FinanceVisualizer  

# import view module
from views import (
    render_categories,
    render_transactions,
    render_user_profile,
    render_dashboard,
    render_budget
)

# initialize models
@st.cache_resource
def init_models():
    """Initialize and cached models"""
    return {
        "category":CategoryModel(),
        "user":UserModel(),
        "transaction":TransactionModel(),
        "budget":BudgetModel(),
        "visualizer":FinanceVisualizer()
    }

#initialize session per user
if "models" not in st.session_state:
    #initialize models
    st.session_state['models'] = init_models()
# initialize models
models = st.session_state['models']

# Page configuration
st.set_page_config(
    page_title = "Finance Tracker",
    page_icon = "🤑",
    layout = "wide"
)

# =============================================
# 1. Authen User
# =============================================
# def login_screen():
#     with st.container():
#         st.header("This app is private")
#         st.subheader("Please login to continue")
#         st.button("Please with Google", on_click = st.login)

# if not st.user.is_logged_in:
#     login_screen()
# else:
#     # Get mongo_user
#     user_model:UserModel = models['user']
#     try:
#         mongo_user_id = user_model.login(st.user.email)

#     except Exception as e:
#         st.error(f"Error during user login: {e}")
#         st.stop()   

#     # set user_id for models
#     # currently we have category and transaction models
#     # you can optimize this by doing it in the model init function
#     models['category'].set_user_id(mongo_user_id)
#     models['transaction'].set_user_id(mongo_user_id)
#     models['budget'].set_user_id(mongo_user_id)

   

#     user = st.user.to_dict()
#     user.update({
#         "id":mongo_user_id    
#     })

  
#     render_user_profile(user_model, user)

#     # init analyzer
#     # because trasaction_model has set user_id already in line 71
#     analyzer_model = FinanceAnalyzer(models['transaction'])


# =============================================
# 1. Authentication (Streamlit Cloud - New API)
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
# 2. Navigation
# =============================================

page = st.sidebar.radio(
    "Navigation",
    ["Home", "Category", "Transaction", "Budget"]
)

# =============================================
# 3. Router
# =============================================
if page == "Home":
    st.title("Home")
    render_dashboard(analyzer_model=analyzer_model,
                     transaction_model=models['transaction'],
                     visualizer_model=models['visualizer'])

elif page == "Category":
    # get category_model from models
    category_model = models['category']


    # display category views
    render_categories(category_model=category_model)
elif page == "Transaction":
    # get category_model and transaction from models
    category_model = models['category']
    transaction_model = models['transaction']

    # display transaction views
    render_transactions(transaction_model=transaction_model, category_model=category_model)
    # display transaction views
elif page == "Budget":
    render_budget(
        budget_model=models['budget'],
        category_model=models['category'],
        transaction_model=models['transaction']
    )
