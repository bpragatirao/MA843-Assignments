import mysql.connector
from mysql.connector import Error

def manage_student_db():
    try:
        # 1. Establish Connection
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='test'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            print("Connected to MySQL database")

            # 2. CREATE TABLE
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

            # 3. CREATE (Insert Data)
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

            # 4. READ (Select Data)
            cursor.execute("SELECT * FROM Student")
            print("\n--- Current Student Records ---")
            for row in cursor.fetchall():
                print(row)

            # 5. UPDATE (Modify Data)
            sql_update = "UPDATE Student SET age = %s WHERE name = %s"
            cursor.execute(sql_update, (23, 'Bhumi'))
            connection.commit()
            print("\nUpdated Bhumi's age to 23.")

            # 6. DELETE (Remove Data)
            sql_delete = "DELETE FROM Student WHERE name = %s"
            cursor.execute(sql_delete, ('Danish',))
            connection.commit()
            print("Deleted record for Danish.")

            # Final Read to show changes
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