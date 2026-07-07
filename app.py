import streamlit as st
import sqlite3
import pandas as pd

from database import create_database
from employee import show_employee_page
from analytics import show_analytics
from reports import show_reports
from login import login
import ai_insights

# ---------------------------------
# Create Database
# ---------------------------------
create_database()

# ---------------------------------
# Login Session
# ---------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

# ---------------------------------
# Page Config
# ---------------------------------
st.set_page_config(
    page_title="EmployeeIQ AI",
    page_icon="👨‍💼",
    layout="wide"
)

# ---------------------------------
# Database
# ---------------------------------
conn = sqlite3.connect("employee.db")
df = pd.read_sql("SELECT * FROM employees", conn)

# ---------------------------------
# Sidebar
# ---------------------------------
st.sidebar.title("👨‍💼 EmployeeIQ AI")

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Employee Management",
        "Analytics",
        "AI Insights",
        "Reports"
    ]
)

# ---------------------------------
# Dashboard
# ---------------------------------
if page == "Dashboard":

    st.title("👨‍💼 EmployeeIQ AI")
    st.subheader("Intelligent Workforce Analytics Platform")

    st.success("✅ Database Connected Successfully")

    total = len(df)

    if total > 0:
        departments = df["department"].nunique()
        performance = round(df["performance"].mean())
        salary = int(df["salary"].mean())
    else:
        departments = 0
        performance = 0
        salary = 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Employees", total)
    col2.metric("Departments", departments)
    col3.metric("Performance", f"{performance}%")
    col4.metric("Average Salary", f"₹{salary}")

    st.divider()

    st.header("Welcome")

    st.write(
        "EmployeeIQ AI is an intelligent workforce analytics platform "
        "for managing employees, analyzing workforce performance, "
        "and generating AI-powered insights."
    )

    st.subheader("Features")

    st.markdown("""
    ✅ Employee Management

    ✅ Workforce Analytics

    ✅ AI Insights

    ✅ Reports

    ✅ Login Authentication

    ✅ CSV & Excel Download
    """)

# ---------------------------------
# Employee Management
# ---------------------------------
elif page == "Employee Management":

    show_employee_page()

# ---------------------------------
# Analytics
# ---------------------------------
elif page == "Analytics":

    show_analytics()

# ---------------------------------
# AI Insights
# ---------------------------------
elif page == "AI Insights":

    ai_insights.show_ai_page()

# ---------------------------------
# Reports
# ---------------------------------
elif page == "Reports":

    show_reports()

# ---------------------------------
# Close Database
# ---------------------------------
conn.close()