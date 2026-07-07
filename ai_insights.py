import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

DB_NAME = "employee.db"


def load_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM employees", conn)
    conn.close()
    return df


def show_ai_page():

    st.title("🤖 AI Insights")
    st.markdown("### Intelligent Workforce Insights")

    df = load_data()

    if df.empty:
        st.warning("No employee data found.")
        return

    # ===============================
    # KPI Cards
    # ===============================

    total_emp = len(df)
    avg_salary = df["salary"].mean()
    avg_perf = df["performance"].mean()

    best_perf = df.loc[df["performance"].idxmax()]
    highest_salary = df.loc[df["salary"].idxmax()]

    col1, col2 = st.columns(2)

    with col1:
        st.success(
            f"""
🏆 Best Performer

Name : {best_perf['name']}

Performance : {best_perf['performance']}%
"""
        )

    with col2:
        st.success(
            f"""
💰 Highest Salary

Name : {highest_salary['name']}

Salary : ₹{highest_salary['salary']}
"""
        )

    col3, col4 = st.columns(2)

    with col3:
        st.info(f"📈 Average Salary\n\n₹{avg_salary:,.2f}")

    with col4:
        st.info(f"⭐ Average Performance\n\n{avg_perf:.2f}%")

    st.divider()

    # ===============================
    # Low Performers
    # ===============================

    st.subheader("⚠ Employees Needing Improvement")

    low = df[df["performance"] < 50]

    if low.empty:
        st.success("All employees are performing well.")
    else:
        st.dataframe(low, use_container_width=True)

    st.divider()

    # ===============================
    # Department Performance
    # ===============================

    st.subheader("🏢 Department Performance")

    dept = (
        df.groupby("department")["performance"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        dept,
        x="department",
        y="performance",
        title="Average Performance by Department",
        color="department"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ===============================
    # Salary Distribution
    # ===============================

    st.subheader("💰 Salary Distribution")

    fig2 = px.histogram(
        df,
        x="salary",
        nbins=10,
        title="Salary Distribution"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # ===============================
    # Top Performers
    # ===============================

    st.subheader("🏆 Top Performers")

    top = df.sort_values(
        by="performance",
        ascending=False
    )

    st.dataframe(
        top[
            [
                "id",
                "name",
                "department",
                "designation",
                "performance"
            ]
        ],
        use_container_width=True
    )

    st.divider()

    # ===============================
    # AI Recommendations
    # ===============================

    st.subheader("🤖 AI Recommendations")

    if avg_perf >= 80:
        st.success(
            "Excellent overall employee performance."
        )

    elif avg_perf >= 60:
        st.info(
            "Employee performance is good. Continue monitoring."
        )

    else:
        st.warning(
            "Overall performance is low. Conduct training programs."
        )

    if len(low) > 0:
        st.warning(
            f"{len(low)} employee(s) require additional training."
        )
    else:
        st.success(
            "No employees require improvement training."
        )

    if avg_salary > 60000:
        st.info(
            "Average salary is high. Review budget planning."
        )
    else:
        st.success(
            "Salary expenditure is within the expected range."
        )

    st.divider()

    # ===============================
    # Summary
    # ===============================

    st.subheader("📋 AI Summary")

    st.write(f"👥 Total Employees : **{total_emp}**")

    st.write(f"🏢 Departments : **{df['department'].nunique()}**")

    st.write(f"📈 Average Performance : **{avg_perf:.2f}%**")

    st.write(f"💰 Average Salary : **₹{avg_salary:,.2f}**")

    st.write(f"🏆 Best Performer : **{best_perf['name']}**")

    st.write(f"💵 Highest Salary : **{highest_salary['name']}**")

    st.success("EmployeeIQ AI analysis completed successfully.")