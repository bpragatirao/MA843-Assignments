import mysql.connector
from mysql.connector import Error

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='test'
    )

def create_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Student_Details (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            age INT,
            major VARCHAR(255)
        )
    """)

def insert_student(cursor, connection):
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    major = input("Enter major: ")

    sql = "INSERT INTO Student_Details (name, age, major) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, age, major))
    connection.commit()
    print(" Student added successfully!")

def view_students(cursor):
    cursor.execute("SELECT * FROM Student_Details")
    rows = cursor.fetchall()

    if not rows:
        print(" No records found.")
        return

    print("\n--- Student Records ---")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Major: {row[3]}")

def update_student(cursor, connection):
    name = input("Enter student name to update: ")
    new_age = int(input("Enter new age: "))
    new_major = input("Enter new major: ")

    sql = "UPDATE Student_Details SET age=%s, major=%s WHERE name=%s"
    cursor.execute(sql, (new_age, new_major, name))
    connection.commit()

    if cursor.rowcount == 0:
        print(" No matching record found.")
    else:
        print(" Record updated successfully!")

def delete_student(cursor, connection):
    name = input("Enter student name to delete: ")

    sql = "DELETE FROM Student_Details WHERE name=%s"
    cursor.execute(sql, (name,))
    connection.commit()

    if cursor.rowcount == 0:
        print(" No matching record found.")
    else:
        print(" Record deleted successfully!")

def main():
    try:
        connection = connect_db()

        if connection.is_connected():
            cursor = connection.cursor()
            print(" Connected to MySQL database")

            create_table(cursor)

            while True:
                print("\n====== STUDENT DATABASE MENU ======")
                print("1. Insert Student")
                print("2. View Students")
                print("3. Update Student")
                print("4. Delete Student")
                print("5. Exit")

                choice = input("Enter your choice (1-5): ")

                if choice == '1':
                    insert_student(cursor, connection)
                elif choice == '2':
                    view_students(cursor)
                elif choice == '3':
                    update_student(cursor, connection)
                elif choice == '4':
                    delete_student(cursor, connection)
                elif choice == '5':
                    print(" Exiting program...")
                    break
                else:
                    print(" Invalid choice. Try again.")

    except Error as e:
        print(f" Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print(" MySQL connection closed.")
main()