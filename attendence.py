import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

DB_NAME = "employee.db"


def show_attendance_page():

    st.title("📅 Attendance Management")

    conn = sqlite3.connect(DB_NAME)

    employees = pd.read_sql(
        "SELECT id, name FROM employees",
        conn
    )

    if employees.empty:
        st.warning("No employees found.")
        conn.close()
        return

    st.subheader("Mark Attendance")

    employee = st.selectbox(
        "Select Employee",
        employees["name"]
    )

    employee_id = int(
        employees.loc[
            employees["name"] == employee,
            "id"
        ].values[0]
    )

    attendance_date = st.date_input(
        "Date",
        value=date.today()
    )

    status = st.selectbox(
        "Status",
        [
            "Present",
            "Absent",
            "Leave"
        ]
    )

    if st.button("Mark Attendance"):

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO attendance
        (employee_id, employee_name, date, status)
        VALUES (?, ?, ?, ?)
        """,
        (
            employee_id,
            employee,
            str(attendance_date),
            status
        ))

        conn.commit()

        st.success("Attendance Marked Successfully!")

        st.rerun()

    st.divider()

    st.subheader("Attendance Records")

    attendance = pd.read_sql(
        "SELECT * FROM attendance ORDER BY date DESC",
        conn
    )

    st.dataframe(
        attendance,
        use_container_width=True
    )

    st.divider()

    st.subheader("Today's Summary")

    today = str(date.today())

    today_df = attendance[
        attendance["date"] == today
    ]

    col1, col2, col3 = st.columns(3)

    present = len(
        today_df[
            today_df["status"] == "Present"
        ]
    )

    absent = len(
        today_df[
            today_df["status"] == "Absent"
        ]
    )

    leave = len(
        today_df[
            today_df["status"] == "Leave"
        ]
    )

    col1.metric("Present", present)
    col2.metric("Absent", absent)
    col3.metric("Leave", leave)

    conn.close()