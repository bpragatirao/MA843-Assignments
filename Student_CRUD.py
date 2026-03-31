import mysql.connector
from mysql.connector import Error

def manage_student_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='test'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            print("Connected to MySQL database")

            cursor.execute("DROP TABLE IF EXISTS Student")
            cursor.execute("""
                CREATE TABLE Student (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    age INT,
                    major VARCHAR(255)
                )
            """)
            print("Table 'Student' created successfully.")

            sql_insert = "INSERT INTO Student (name, age, major) VALUES (%s, %s, %s)"
            students = [
                ('Arnav', 20, 'Data Science'),
                ('Bhumi', 22, 'Scientific Computing'),
                ('Charol', 21, 'Physics'),
                ('Danish', 24, 'Biology'),
                ('Eva', 22, 'Mathematics')
            ]
            cursor.executemany(sql_insert, students)
            connection.commit()
            print(f"{cursor.rowcount} records inserted.")

            cursor.execute("SELECT * FROM Student")
            print("\n--- Current Student Records ---")
            for row in cursor.fetchall():
                print(row)

            sql_update = "UPDATE Student SET age = %s WHERE name = %s"
            cursor.execute(sql_update, (23, 'Bhumi'))
            connection.commit()
            print("\nUpdated Bhumi's age to 23.")

            sql_delete = "DELETE FROM Student WHERE name = %s"
            cursor.execute(sql_delete, ('Danish',))
            connection.commit()
            print("Deleted record for Danish.")

            cursor.execute("SELECT * FROM Student")
            print("\n--- Final Student Records ---")
            for row in cursor.fetchall():
                print(row)

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("\nMySQL connection is closed.")

manage_student_db()