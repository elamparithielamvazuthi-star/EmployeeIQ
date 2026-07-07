import streamlit as st
import sqlite3
import pandas as pd

DB_NAME = "employee.db"

def show_analytics():

    st.title("📊 Workforce Analytics")

    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql("SELECT * FROM employees", conn)

    conn.close()

    if df.empty:
        st.warning("No Employee Data Available")
        return

    st.subheader("Employee Dataset")
    st.dataframe(df, use_container_width=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Employees by Department")

        dept = df["department"].value_counts()

        st.bar_chart(dept)

    with col2:
        st.subheader("Performance")

        st.bar_chart(df.set_index("name")["performance"])

    st.markdown("---")

    st.subheader("Salary Statistics")

    st.write(df["salary"].describe())