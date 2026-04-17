import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='test'
        )
        if conn.is_connected():
            print("Connected to MySQL")
            return conn
    except Error as e:
        print("Error:", e)
        return None


def create_tables(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        dept_id INT PRIMARY KEY,
        dept_name VARCHAR(50)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INT PRIMARY KEY,
        name VARCHAR(50),
        dept_id INT,
        FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        course_id INT PRIMARY KEY,
        course_name VARCHAR(50),
        dept_id INT,
        FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
    )
    """)


def insert_data(cursor):
    cursor.execute("DELETE FROM students")
    cursor.execute("DELETE FROM departments")
    cursor.execute("DELETE FROM courses")

    departments = [
        (1, "Computer Science"),
        (2, "Mechanical"),
        (3, "Electrical")
    ]

    students = [
        (101, "Alice", 1),
        (102, "Bob", 2),
        (103, "Charlie", None),
        (104, "David", 1)
    ]

    courses = [
        (201, "Data Structures", 1),
        (202, "Thermodynamics", 2),
        (203, "Circuits", 3)
    ]

    cursor.executemany("INSERT INTO departments VALUES (%s, %s)", departments)
    cursor.executemany("INSERT INTO students VALUES (%s, %s, %s)", students)
    cursor.executemany("INSERT INTO courses VALUES (%s, %s, %s)", courses)


def run_query(cursor, title, query):
    print("\n" + "="*50)
    print(title)
    print("="*50)

    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        print(row)


def main():
    conn = connect_db()
    if conn is None:
        return

    cursor = conn.cursor()

    try:
        create_tables(cursor)
        insert_data(cursor)
        conn.commit()

        # INNER JOIN
        run_query(cursor, "INNER JOIN",
        """
        SELECT s.name, d.dept_name
        FROM students s
        INNER JOIN departments d
        ON s.dept_id = d.dept_id
        """)

        # LEFT JOIN
        run_query(cursor, "LEFT JOIN",
        """
        SELECT s.name, d.dept_name
        FROM students s
        LEFT JOIN departments d
        ON s.dept_id = d.dept_id
        """)

        # RIGHT JOIN
        run_query(cursor, "RIGHT JOIN",
        """
        SELECT s.name, d.dept_name
        FROM students s
        RIGHT JOIN departments d
        ON s.dept_id = d.dept_id
        """)

        # FULL OUTER JOIN (MySQL workaround)
        run_query(cursor, "FULL OUTER JOIN (via UNION)",
        """
        SELECT s.name, d.dept_name
        FROM students s
        LEFT JOIN departments d
        ON s.dept_id = d.dept_id

        UNION

        SELECT s.name, d.dept_name
        FROM students s
        RIGHT JOIN departments d
        ON s.dept_id = d.dept_id
        """)

        # CROSS JOIN
        run_query(cursor, "CROSS JOIN",
        """
        SELECT s.name, d.dept_name
        FROM students s
        CROSS JOIN departments d
        """)

        # MULTIPLE JOIN
        run_query(cursor, "MULTIPLE JOIN",
        """
        SELECT s.name, d.dept_name, c.course_name
        FROM students s
        INNER JOIN departments d
            ON s.dept_id = d.dept_id
        INNER JOIN courses c
            ON d.dept_id = c.dept_id
        """)

    except Error as e:
        print("Error during execution:", e)

    finally:
        cursor.close()
        conn.close()
        print("\nConnection closed.")


main()