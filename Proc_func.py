import mysql.connector
from mysql.connector import Error

def manage_mysql_routines():
    try:
        # Establish connection
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='test'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # --- CALLING A STORED PROCEDURE ---
            # Scenario: A procedure 'get_employee_details' that takes an ID
            emp_id = 101
            print(f"Calling procedure for Employee ID: {emp_id}")
            
            # .callproc(name, params_tuple)
            cursor.callproc('get_employee_details', (emp_id,))

            # Procedures can return multiple result sets
            for result in cursor.stored_results():
                row = result.fetchone()
                print(f"Procedure Output: {row}")

            # --- CALLING A FUNCTION ---
            # Scenario: A function 'calculate_bonus' that returns a value
            # Functions are treated like standard SQL queries
            query = "SELECT calculate_bonus(%s) AS bonus"
            cursor.execute(query, (emp_id,))
            
            bonus = cursor.fetchone()
            print(f"Function Output (Bonus): {bonus[0]}")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

manage_mysql_routines()