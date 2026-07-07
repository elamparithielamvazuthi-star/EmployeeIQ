import streamlit as st
import sqlite3
import pandas as pd

DB_NAME = "employee.db"

def show_reports():

    st.title("📄 Reports")

    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM employees", conn)

    st.subheader("Employee Report")

    st.dataframe(df, use_container_width=True)

    st.divider()

    st.subheader("Summary")

    st.write("Total Employees :", len(df))
    st.write("Departments :", df["department"].nunique())

    if len(df) > 0:
        st.write("Average Salary :", round(df["salary"].mean(), 2))
        st.write("Average Performance :", round(df["performance"].mean(), 2))

    st.divider()

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download CSV",
        csv,
        file_name="employee_report.csv",
        mime="text/csv"
    )

    excel_file = "employee_report.xlsx"

    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)

    with open(excel_file, "rb") as f:
        st.download_button(
            "⬇ Download Excel",
            f,
            file_name="employee_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    conn.close()