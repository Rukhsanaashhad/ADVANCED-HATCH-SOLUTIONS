import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from io import BytesIO

DB_FILE = "jadeed_expenses_db.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_db():
    with open(DB_FILE, "w") as f:
        json.dump(st.session_state.db, f, indent=4)

# Initialize
if "db" not in st.session_state:
    st.session_state.db = load_db()
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

db = st.session_state.db

# ============= LOGIN / SIGNUP =============
if not st.session_state.logged_in:
    st.title("ADVANCED HATCH SOLUTIONS")
    st.markdown("### Expense Management System")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        with st.form("login"):
            user = st.text_input("Username")
            pwd = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                if user in db and db[user]["password"] == pwd:
                    st.session_state.logged_in = True
                    st.session_state.username = user
                    st.success(f"Welcome {user}!")
                    st.rerun()
                else:
                    st.error("Wrong credentials")

    with tab2:
        with st.form("signup"):
            new_user = st.text_input("New Username")
            new_pwd = st.text_input("New Password", type="password")
            confirm = st.text_input("Confirm Password", type="password")
            if st.form_submit_button("Create Account"):
                if new_user in db:
                    st.error("Username already taken!")
                elif new_pwd != confirm:
                    st.error("Passwords don't match!")
                else:
                    db[new_user] = {"password": new_pwd, "expenses": {}}
                    save_db()
                    st.success("Account created! Now login.")
                    st.rerun()

else:
    user = st.session_state.username
    st.sidebar.success(f"Logged in: **{user}**")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()

    st.title("ADVANCED HATCH SOLUTIONS")
    st.markdown("### Monthly Expense Manager")

    # All headings (zero se start)
    headings = [
        "LEAPORD/M&P COURIER",
        "ENTERTAINMENT",
        "PRINTING & STATIONARY",
        "NEWSPAPER BILL",
        "DIESEL FOR GENERATOR",
        "TRANSPORTATION EXPENSE",
        "BUILDING REPAIR",
        "AGRICULTURE",
        "ELECTRIC BILL",
        "UTILITTY BILL",
        "CROCKERY ITEM PURCHASE",
        "WATER TANKER",
        "REPAIR MAINTANCE",
        "FUEL VEHICLE",
        "FUEL VEHICLE KIU 61898",
        "GENERATOR ITEM PURCHASE AND REP",
        "MACHINERY REPAIR",   
        "GENERAL ITEM",
        "A.C REPAIR",
        "MISC EXPENSES",
        "ELECTRICAL ITEM PURCHASE REPAIR",
        "MEDICINE FOR CHICKS",
        "MEDICAL BILL OF WORKER",        
        "TOOL TAX ON ROUTE",
        "PHONE EXPENSE ON ROUTE",
        "HATCHERY SALARY",
        
    ]

    user_data = db[user]["expenses"]
    current_month = datetime.now().strftime("%B %Y")

    
    saved_months = list(user_data.keys())
    all_months = sorted(set([current_month] + saved_months), 
                        key=lambda x: datetime.strptime(x, "%B %Y") if " " in x else datetime.now(), 
                        reverse=True)

    if "selected_month" not in st.session_state:
        st.session_state.selected_month = current_month

    selected_month = st.selectbox("Select Month", options=all_months, 
                                  index=all_months.index(st.session_state.selected_month))

    if selected_month != st.session_state.selected_month:
        st.session_state.selected_month = selected_month
        st.rerun()

    
    if selected_month not in user_data:
        user_data[selected_month] = {heading: 0 for heading in headings}
        save_db()

    expenses = user_data[selected_month]
    total = 0

    st.subheader(f"Editing: **{selected_month}**")

    for heading in headings:
        with st.expander(f"**{heading}**"):
            new_amt = st.number_input(
                "Amount (PKR)",
                min_value=0,
                value=int(expenses.get(heading, 0)),
                step=100,
                key=f"{user}_{selected_month}_{heading}"
            )
            expenses[heading] = int(new_amt)
            total += int(new_amt)

    # Buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("SAVE DATA", type="primary"):
            save_db()
            st.success("Saved!")
            st.balloons()

    with col2:
        new_month = st.text_input("New Month (e.g. January 2026)")
        if st.button("Add New Month"):
            if new_month and new_month not in user_data:
                user_data[new_month] = {h: 0 for h in headings}
                save_db()
                st.success(f"{new_month} added!")
                st.rerun()

    with col3:
        if st.button("Export to Excel"):
            df = pd.DataFrame([{"PARTICULAR": h, "AMOUNT": expenses[h]} for h in headings])
            df.loc[len(df)] = {"PARTICULAR": "TOTAL", "AMOUNT": total}
            output = BytesIO()
            df.to_excel(output, index=False, engine='openpyxl')
            output.seek(0)
            st.download_button("Download Excel", data=output, 
                               file_name=f"Jadeed_{selected_month}.xlsx")

    st.markdown("---")
    st.success(f"### GRAND TOTAL ({selected_month}): **{total:,} PKR**") 
    st.info("Sab zero se start | Tum khud daalo | Har cheez save rahegi")

    st.caption("Developed by Muhammad Ashhad Khan 🤖")
