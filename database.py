import sqlite3

DB_NAME = "employee.db"


# -----------------------------
# Database Connection
# -----------------------------
def get_connection():
    return sqlite3.connect(DB_NAME)


# -----------------------------
# Create Database
# -----------------------------
def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Employees Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department TEXT,
        designation TEXT,
        email TEXT,
        salary REAL,
        performance INTEGER
    )
    """)

    # Attendance Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        employee_name TEXT,
        date TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# Add Employee
# -----------------------------
def add_employee(name, department, designation, email, salary, performance):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO employees
    (name, department, designation, email, salary, performance)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (name, department, designation, email, salary, performance))

    conn.commit()
    conn.close()


# -----------------------------
# View Employees
# -----------------------------
def get_all_employees():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees")

    rows = cursor.fetchall()

    conn.close()

    return rows


# -----------------------------
# Search Employee
# -----------------------------
def search_employee(keyword):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM employees
    WHERE
        name LIKE ?
        OR department LIKE ?
        OR designation LIKE ?
    """,
    (
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    rows = cursor.fetchall()

    conn.close()

    return rows


# -----------------------------
# Update Employee
# -----------------------------
def update_employee(
    emp_id,
    name,
    department,
    designation,
    email,
    salary,
    performance
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE employees
    SET
        name=?,
        department=?,
        designation=?,
        email=?,
        salary=?,
        performance=?
    WHERE id=?
    """,
    (
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
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM employees WHERE id=?",
        (emp_id,)
    )

    conn.commit()
    conn.close()