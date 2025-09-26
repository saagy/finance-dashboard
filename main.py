import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os 
st.set_page_config(page_title="Finance App", page_icon="💸",layout="wide")


if "categories" not in st.session_state:
    st.session_state.categories = {
        "Uncategorized": [],
        }
if os.path.exists("categories.json"):
    with open("categories.json", "r") as f:
        st.session_state.categories = json.load(f)
def save_categories():
    with open("categories.json", "w") as f:
        json.dump(st.session_state.categories, f)

def categorize_transaction(df):
    df['Category'] = 'Uncategorized'
    for category, keywords in st.session_state.categories.items():
        if category == "Uncategorized" or not keywords:
            continue
        lower_keywords = [kw.lower().strip() for kw in keywords]
        for idx, row in df.iterrows():
            details = row['Details'].lower()
            if details in lower_keywords:
                df.at[idx, 'Category'] = category
    return df

def load_transactions(file):
    try:
        df = pd.read_csv(file)
        st.success("File uploaded successfully!")
        df.columns = [col.strip() for col in df.columns]  # Clean column names
        df['Amount'] = df['Amount'].str.replace(',', '').astype(float)  # Ensure Amount is float
        df['Date'] = pd.to_datetime(df['Date'], format='%d %b %Y')  # Ensure Date is datetime
        return categorize_transaction(df)
    
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

def add_keyword_to_category(category, keyword):
    keyword = keyword.strip()
    if keyword and keyword not in st.session_state.categories[category]:
        st.session_state.categories[category].append(keyword)
        save_categories()
        return True
    return False
def main():
    st.title("Finance Dashboard")
    # File uploader
    uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])
    if uploaded_file is not None:
        df = load_transactions(uploaded_file)
        if df is not None:
            debits_df = df[df["Debit/Credit"] == "Debit"].copy()
            credits_df = df[df["Debit/Credit"] == "Credit"].copy()

            st.session_state.debits_df = debits_df.copy()

            tab1, tab2 = st.tabs(["Expenses (Debits)", "Payments (Credits)"])
            with tab1:
                new_category = st.text_input("Add New Category")
                add_button = st.button("Add Category")
                if add_button and new_category:
                    if new_category not in st.session_state.categories:
                        st.session_state.categories[new_category] = []
                        save_categories()
                        #st.success(f"Category '{new_category}' added!")
                        #ToDO: Fix the rerun issue  not displaying the message
                        st.rerun()
                    else:
                        st.warning(f"Category '{new_category}' already exists.")

                st.subheader("Your Expenses")
                edited_df = st.data_editor(
                    st.session_state.debits_df[['Date', 'Details', 'Amount', 'Category']],
                    column_config={
                        'Date': st.column_config.DateColumn("Transaction Date",format = "DD/MM/YYYY"),
                        #'Details': st.column_config.TextColumn("Transaction Details"),
                        'Amount': st.column_config.NumberColumn("Amount", format="%.2f AED"),
                        'Category': st.column_config.SelectboxColumn(
                            "Category",
                            options=list(st.session_state.categories.keys()),
                            help="Select a category for the transaction"
                        )
                    },
                    hide_index=True,
                    use_container_width=True,
                    key="category editor"
                )
                save_button = st.button("Apply Changes", type="primary")
                if save_button:
                    for idx, row in edited_df.iterrows():
                        new_category = row['Category']
                        if new_category == st.session_state.debits_df.at[idx, 'Category']:
                            continue
                        details = row['Details'].strip()
                        st.session_state.debits_df.at[idx, 'Category'] = new_category
                        add_keyword_to_category(new_category, details)
                st.subheader("Expense Summary by Category")
                category_totals = st.session_state.debits_df.groupby('Category')['Amount'].sum().reset_index()
                category_totals = category_totals.sort_values('Amount', ascending=False)
                st.dataframe(category_totals,
                                column_config={
                                    'Category': st.column_config.TextColumn("Category"),
                                    'Amount': st.column_config.NumberColumn("Total Amount", format="%.2f AED")
                                },
                                use_container_width=True,
                                hide_index=True
                             )  
                fig = px.pie(
                    category_totals, names='Category',
                      values='Amount', title='Expenses by Category')
                st.plotly_chart(fig, use_container_width=True)
            with tab2:
                st.subheader("Your Payments summary")
                total_credits = credits_df['Amount'].sum()
                st.metric("Total Payments Received", f"{total_credits:,.2f} AED")
                st.write(credits_df)
main()

