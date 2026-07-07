import streamlit as st
import sqlite3
import pandas as pd

DB_NAME = "employee.db"


# -----------------------------
# Add Employee
# -----------------------------
def add_employee(name, department, designation, email, salary, performance):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO employees
    (name, department, designation, email, salary, performance)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (name, department, designation, email, salary, performance))

    conn.commit()
    conn.close()


# -----------------------------
# Update Employee
# -----------------------------
def update_employee(emp_id, name, department, designation, email, salary, performance):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    UPDATE employees
    SET
        name=?,
        department=?,
        designation=?,
        email=?,
        salary=?,
        performance=?
    WHERE id=?
    """, (
        name,
        department,
        designation,
        email,
        salary,
        performance,
        emp_id
    ))

    conn.commit()
    conn.close()


# -----------------------------
# Delete Employee
# -----------------------------
def delete_employee(emp_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM employees WHERE id=?",
        (emp_id,)
    )

    conn.commit()
    conn.close()


# -----------------------------
# Employee Page
# -----------------------------
def show_employee_page():

    st.header("👥 Employee Management")

    # -----------------------------
    # Add Employee
    # -----------------------------
    st.subheader("➕ Add Employee")

    name = st.text_input("Employee Name")
    department = st.text_input("Department")
    designation = st.text_input("Designation")
    email = st.text_input("Email")
    salary = st.number_input("Salary", min_value=0)
    performance = st.slider("Performance", 0, 100, 75)

    if st.button("Add Employee"):

        if name.strip() == "":
            st.warning("Please enter employee name.")
        else:
            add_employee(
                name,
                department,
                designation,
                email,
                salary,
                performance
            )

            st.success("Employee Added Successfully!")
            st.rerun()

    st.divider()

    # -----------------------------
    # Employee Records
    # -----------------------------
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM employees", conn)

    st.subheader("📋 Employee Records")

    search = st.text_input("🔍 Search Employee")

    if search:
        df = df[
            df["name"].str.contains(search, case=False)
            | df["department"].str.contains(search, case=False)
            | df["designation"].str.contains(search, case=False)
        ]

    st.dataframe(df, use_container_width=True)

    st.divider()

    # -----------------------------
    # Update Employee
    # -----------------------------
    st.subheader("✏️ Update Employee")

    employee_id = st.number_input(
        "Employee ID",
        min_value=1,
        step=1
    )

    new_name = st.text_input("New Name")
    new_department = st.text_input("New Department")
    new_designation = st.text_input("New Designation")
    new_email = st.text_input("New Email")

    new_salary = st.number_input(
        "New Salary",
        min_value=0,
        key="update_salary"
    )

    new_performance = st.slider(
        "New Performance",
        0,
        100,
        75,
        key="update_performance"
    )

    if st.button("Update Employee"):

        update_employee(
            employee_id,
            new_name,
            new_department,
            new_designation,
            new_email,
            new_salary,
            new_performance
        )

        st.success("Employee Updated Successfully!")
        st.rerun()

    st.divider()

    # -----------------------------
    # Delete Employee
    # -----------------------------
    st.subheader("🗑️ Delete Employee")

    delete_id = st.number_input(
        "Employee ID to Delete",
        min_value=1,
        step=1,
        key="delete_id"
    )

    if st.button("Delete Employee"):

        delete_employee(delete_id)

        st.success("Employee Deleted Successfully!")
        st.rerun()

    conn.close()