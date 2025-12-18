import streamlit as st
from datetime import datetime
from utils import format_currency,format_date,handler_datetime
import config
from database import TransactionModel
import pandas as pd

def render_budget(budget_model, category_model, transaction_model):

    """
    Render the Budget Dashboard
    - Each category has a budget limit
    - Track spending per category
    - Sync with transactions
    - Dashboard view with charts and summaries
    """
    st.title("💰 Budgets")

    #Dashboard
    render_budget_dashboard(
        budget_model,
        transaction_model,
        category_model
    )
    # Fetch all budgets
    budgets = budget_model.get_all_budgets()
    #category_type = category_model.get_all_category_types()
    if not budgets:
        st.warning("No budgets found. Please add a budget.")
        # --- Create New Budget ---
    with st.expander("➕ Create New Budget"):
        _render_create_budget_form(budget_model, category_model)

    st.divider()

    # --- Render each category budget card ---
    for budget in budgets:
        category = budget.get("category")
        limit_amount = budget.get("limit_amount", 0)
        month = budget.get("month") # YYYY-MM
        year = budget.get("year")

        # Calculate spent amount in month
        spent = budget_model.calculate_spent(
            transaction_model,
            category,
            month,
            year
        )

        remaining = limit_amount - spent
        exceeded = spent > limit_amount

        _render_budget_card(budget, spent, remaining, exceeded, budget_model,category_model)

# ===============================
# Create Budget Form
# ===============================
def _render_create_budget_form(budget_model,category_model):

    
    #now = datetime.now()
    col1, col2 = st.columns(2)

    with col1:
        # Month and year separately
        month = st.selectbox("Month", list(range(1, 13)))
        year = st.number_input("Year", min_value=1990, max_value=2100, value=datetime.now().year)
        
        type_ = st.selectbox("Type", ["Expense","Income"],disabled=True)
        categories = category_model.get_category_by_type(type_)
        category_names = [c["name"] for c in categories]      
        
        category = st.selectbox("Category", category_names)     

    with col2:
        limit_amount = st.number_input(
            "Budget Limit",
            min_value=1.0,
            value=100.0,
            step=5.0
        )
        created_at = st.date_input(
                                    "Created at",
                                    value=datetime.now().date()
                                )
        description = st.text_area("Description", placeholder="Optional")

    if st.button("💾 Save Budget", type="primary"):

        budget_date = datetime.combine(created_at, datetime.now().time())
        budget_id = budget_model.create_budget(
                category=category,
                type_=type_,
                limit_amount=limit_amount,
                month=month,
                year=year,
                budget_date=budget_date,
                description=description
            )
        if budget_id:
            st.success("Budget created successfully!")
            st.rerun()
        else:
            st.error("Failed to create budget.")
# ===============================
# Render Budget Card
# ===============================
def _render_budget_card(budget, spent, remaining, exceeded, budget_model,category_model):
    is_editing = st.session_state.get("edit_budget") == str(budget["_id"]) #Dạt
    budget_type = budget.get("type_")
    category = budget.get("category")
    limit_amount = budget.get("limit_amount")
    month = budget.get("month")
    year = budget.get("year")
    created_at = budget.get("date",datetime.now())
    updated_at = budget.get("updated_at",datetime.now())
    type_color = "🔴" if budget_type == "Expense" else "🟢"
   
    header = f"💰 {category} | {month}/{year} | Limit: {format_currency(limit_amount)}"

    with st.expander(header,expanded=is_editing):
        if not is_editing:

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Budget", format_currency(limit_amount))


            with col2:
                st.metric("Total Spent", format_currency(spent))

            with col3:
                st.metric("Remaining", format_currency(remaining))

            if exceeded:
                st.error(f"⚠️ Over Budget by {format_currency(abs(remaining))}")
            else:
                st.success(f"Remaining: {format_currency(remaining)}")

            st.write(f"📅**Created At:** {format_date(created_at)}")
            st.write(f"📝**Last Updated:** {format_date(updated_at)}")
            st.divider()

        # Edit and delete buttons
            col_edit, col_delete, _ = st.columns([1, 1, 3])

            with col_edit:
                if st.button(f"✏️ Edit",key=f"edit_{budget['_id']}", use_container_width=True):
                    st.session_state.edit_budget = str(budget["_id"])
                    st.rerun()

            with col_delete:
                if st.button(f"🗑️ Delete",key=f"delete_{budget['_id']}",use_container_width=True, type="primary"):
                    if budget_model.delete_budget(budget["_id"]):
                        st.success("Budget deleted successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to delete budget.")
        else: #Hàm editing budget
        
            st.subheader("✏️ Edit Budget")
            budget_id = str(budget["_id"])

            with st.form(f"edit_form_{budget_id}"):

                col1, col2 = st.columns(2)

                # Cột trái
                with col1:

                    month = st.selectbox("Month", list(range(1, 13)))
                    year = st.number_input("Year", min_value=1990, max_value=2100, value=datetime.now().year)
                    
                    type_ = st.selectbox(
                                        "Type",
                                        options=config.TRANSACTION_TYPES,
                                        key=f"type_{budget_id}",
                                        index=config.TRANSACTION_TYPES.index(budget["type"]),
                                        disabled=True
                                        )
                                         
                    categories = category_model.get_category_by_type(type_)
                    category_names = [c["name"] for c in categories]      
                    category = st.selectbox("Category", category_names) 
                           
                                      
                # Cột phải
                with col2:
                    amount_value = st.number_input(
                        "Limit amount",
                        min_value=1.0,
                        value=float(budget["limit_amount"]),
                        step=5.0
                    )           

                    date_value = st.date_input(
                        "Update date",
                        value=updated_at.date() if isinstance(updated_at, datetime) else datetime.now().date()
                    )                 
                    
                    description_value = st.text_area(
                        "Description",
                        value=budget.get("description", "")
                    )

                col_save, col_cancel, _ = st.columns([2, 2, 6])
                # Save
                with col_save:
                    update_at = datetime.combine(date_value, datetime.now().time())
                    if  st.form_submit_button("💾 Save", use_container_width=True):
                        updated = {
                            "type": type_,
                            "limit_amount": amount_value,
                            "updated_at": update_at,
                            "category": category,
                            "description": description_value,
                            "month": month,
                            "year": year
                        }

                        if budget_model.update_budget(budget["_id"], **updated):
                            st.session_state.edit_budget = None
                            st.rerun() 
                        else:
                            st.error("Failed to update budget.")

                
                
                with col_cancel:
                    # Cancel
                    if  st.form_submit_button("❌ Cancel", use_container_width=True):
                        st.session_state.edit_budget = None
                        st.rerun()   

def render_budget_dashboard(
                            budget_model,
                            transaction_model,
                            category_model
                        ):
    st.title("📊 Budget Dashboard")

    # ==========================
    # Month / Year Filter
    # ==========================
    now = datetime.now()

    col1, col2, _ = st.columns([2, 2, 6])

    with col1:
        month = st.selectbox(
            "📅 Month",
            options=list(range(1, 13)),
            index=now.month - 1
        )

    with col2:
        year = st.number_input(
            "📆 Year",
            min_value=2000,
            max_value=2100,
            value=now.year,
            step=1
        )

    summary = _build_budget_summary(
        budget_model,
        transaction_model,
        category_model,
        month,
        year
    )

    if not summary:
        st.warning("No budget data available.")
        return

    _render_summary_cards(summary)
    st.divider()
    _render_budget_chart(summary)
    st.divider()
    _render_budget_table(summary)
    st.divider()
def _build_budget_summary(
                        budget_model,
                        transaction_model,
                        category_model,
                        month,
                        year
                    ):
    categories = category_model.get_category_by_type("Expense")
    budgets = budget_model.get_all_budgets(month, year)

    budget_map = {
        b["category"]: b["limit_amount"]
        for b in budgets
    }

    summary = []

    for cate in categories:
        name = cate["name"]

        limit_amount = budget_map.get(name, 0)

        spent = transaction_model.get_total_spent_by_category(
            name,
            month,
            year
        )

        remaining = limit_amount - spent

        summary.append({
            "Category": name,
            "Budget": limit_amount,
            "Spent": spent,
            "Remaining": remaining,
            "Status": "Over" if remaining < 0 else "OK"
        })

    return summary

def _render_summary_cards(summary):
    total_budget = sum(s["Budget"] for s in summary)
    total_spent = sum(s["Spent"] for s in summary)
    total_remaining = total_budget - total_spent

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total Budget", format_currency(total_budget))
    col2.metric("💸 Total Spent", format_currency(total_spent))
    col3.metric(
        "🧾 Remaining",
        format_currency(total_remaining),
        delta=format_currency(total_remaining),
    )

def _render_budget_table(summary):
    df = pd.DataFrame(summary)

    df["Budget"] = df["Budget"].apply(format_currency)
    df["Spent"] = df["Spent"].apply(format_currency)
    df["Remaining"] = df["Remaining"].apply(format_currency)

    st.subheader("📋 Category Budget Breakdown")
    st.dataframe(df, use_container_width=True)

def _render_budget_chart(summary):
    df = pd.DataFrame(summary)

    df_chart = df.set_index("Category")[["Budget", "Spent"]]

    st.subheader("📊 Budget vs Spent")
    st.bar_chart(df_chart)
