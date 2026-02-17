import sqlite3

# Connect to SQLite database (or create it)
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS student (
    roll_no INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    course TEXT
)
""")

# Insert student details
n = int(input("Enter number of students: "))

for i in range(n):
    print(f"\nEnter details for student {i + 1}")
    roll_no = int(input("Roll Number: "))
    name = input("Name: ")
    age = int(input("Age: "))
    course = input("Course: ")

    cursor.execute(
        "INSERT INTO student (roll_no, name, age, course) VALUES (?, ?, ?, ?)",
        (roll_no, name, age, course)
    )

conn.commit()

# Fetch and display records
cursor.execute("SELECT * FROM student")
records = cursor.fetchall()

print("\nStudent Details (From Database)")
print("-" * 55)
print(f"{'Roll No':<10}{'Name':<15}{'Age':<10}{'Course':<20}")
print("-" * 55)

for row in records:
    print(f"{row[0]:<10}{row[1]:<15}{row[2]:<10}{row[3]:<20}")

print("-" * 55)

# Close connection
conn.close()
