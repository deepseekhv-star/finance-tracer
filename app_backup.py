import streamlit as st
import config
import pandas as pd
#from database.category_models import CategoryModel 
#Hoac
from database import CategoryModel 


# initialize models
@st.cache_resource
def init_models():
    """Initialize and cached models"""
    return CategoryModel()


category_model = init_models()

# Page configuration
st.set_page_config(
    page_title = "Category Manager",
    layout = "wide"
)

# =============================================
# MAIN APP
# =============================================


# App tile
st.title(config.APP_NAME)



#Add categories
#st.header("Add categories")
#type_col, name_col, submit_col = st.columns(3)

#with type_col:
#    type_cate = st.selectbox("Select type:",config.TRANSACTION_TYPES)
#    st.text(type_cate)

#with name_col:
#    if type_cate == "Expense":
#        name_cate = st.selectbox("Select categrories:",config.DEFAULT_CATEGORIES_EXPENSE)
#        st.text(name_cate)
#    else:
#        name_cate = st.selectbox("Select categrories:",config.DEFAULT_CATEGORIES_INCOME)
#        st.text(name_cate)
#with submit_col:
#    submit = st.button("Submit")

#if submit:
#    added_cate = category_model.add_category(type = type_cate,category_name = name_cate)
#    st.write(added_cate)
 
#st.divider()

# Overall
st.header("Categories Overall")

col1, col2, col3 = st.columns(3)

with col1:
    st.text("Total Categories")
    total = category_model.get_total()
    st.text(f"{len(total)}")

with col2:
    st.text("Expense Categories")
    expense = category_model.get_category_by_type(type = "Expense")
    st.text(f"{len(expense)}")

with col3:
    st.text("Income Categories")
    income = category_model.get_category_by_type(type = "Income")
    st.text(f"{len(income)}")

st.divider()

### Add new category

st.header("➕ Add new category")

with st.form("add_category_form"):
    col1, col2, col3 = st.columns([3, 3, 1])

    with col1:
        # category_type = st.selectbox("Type", ['Expense', 'Income'])
        category_type = st.selectbox("Type", config.TRANSACTION_TYPES)

    with col2:
        category_name = st.text_input("Category Name",
                                      placeholder = "e.g, Groceries, Rent, KPI bonus")
        
    with col3:
        st.write("")
        st.write("")
        submited = st.form_submit_button("▶", use_container_width=True)

    if submited:
        if not category_type:
            st.error("Please choose Category Type")
        if not category_name:
            st.error("Please enter a Category Name")
        else:
            # print(f"Category type: {category_type}")
            # print(f"Category name: {category_name}")
            new_category = category_model.add_category(type = category_type,
                                                    category_name=category_name)

            if new_category:
                st.success(f"Category added {category_name} successfully !")
                st.rerun() # Refresh the page to load data
            else:
                st.error("Failed to add new category")

st.divider()


#Read category
#st.header("➕ Read category")
#st.subheader("Category detail")
#with st.form("Press button to read data"):

## TODO: make categories detail
#    tab1, tab2, tab3 = st.tabs(["**Expense**","**Income**","**All**"])
#    Filter = st.form_submit_button("▶", use_container_width=True)
#    with tab1:
#        expense_lst = category_model.get_category_by_type(type = "Expense")
#        st.subheader("Category detail by json")
#        st.json(expense_lst) #Kiểu json
#        st.subheader("Category detail by frame")
#        st.dataframe(expense_lst)#Kiểu data frame

#    with tab2:    
#        income_lst = category_model.get_category_by_type(type = "Income")
#        st.subheader("Category detail by json")
#        st.json(income_lst)#Kiểu json
#        st.subheader("Category detail by frame")
#        st.dataframe(income_lst)#Kiểu data frame

#    with tab3:  
#        df1 = category_model.get_total()  
#        df2 = category_model.get_total_dataframe()
#        st.subheader("Category detail by json")
#        st.json(df1)#Kiểu json
#        st.subheader("Category detail by frame")
#        st.dataframe(df2)#Kiểu data frame        

st.header("➕ Read category")
st.subheader("Category detail")
#with st.form("Press button to read data"):
# TODO: make categories detail
tab1, tab2 = st.tabs(["**Expense**","**Income**"])

with tab1:
    expense_lst=category_model.get_category_by_type(type="Expense")

    if expense_lst:
        st.write(f"Total:{len(expense_lst)} categories")
        st.write("")

        cols = st.columns(3)

        for idx,item in enumerate(expense_lst):
            col_idx = idx %3 

            with cols[col_idx]:
                with st.container():
                    subcol_a, subcol_b = st.columns([4,1])

                    with subcol_a:
                        st.write(f"{item.get("name")}")
                        st.caption(f"{item.get("created_at").strftime("%d-%m-%Y")}")

                    with subcol_b:
                        delete_button = st.button("Delete",key = f"del_exp_{item["_id"]}")  
                        if delete_button:
                            result = category_model.delete_category(type=item.get("type"),category_name=item.get("name"))
                            if result:
                                st.success(f"Delate {item.get("name")} done")
                                st.rerun()
                            else:
                                st.error(f"Delete {item.get("name")} failed")    
                    
with tab2:
    income_lst=category_model.get_category_by_type(type="Income")

    if income_lst:
        st.write(f"Total:{len(income_lst)} categories")
        st.write("")

        cols = st.columns(3)

        for idx,item in enumerate(income_lst):
            col_idx = idx %3 

            with cols[col_idx]:
                with st.container():
                    subcol_a, subcol_b = st.columns([4,1])

                    with subcol_a:
                        st.write(f"{item.get("name")}")
                        st.caption(f"{item.get("created_at").strftime("%d-%m-%Y")}")

                    with subcol_b:
                        delete_button = st.button("Delete",key = f"del_exp_{item["_id"]}") 
                        if delete_button:
                            result = category_model.delete_category(type=item.get("type"),category_name=item.get("name"))
                            if result:
                                st.success(f"Delate {item.get("name")} done")
                                st.rerun()
                            else:
                                st.error(f"Delete {item.get("name")} failed")

    