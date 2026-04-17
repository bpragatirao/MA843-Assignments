import mysql.connector
from mysql.connector import Error

def main():
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",              # replace with your password
            database="college_db"
        )

        cursor = conn.cursor()
        print("Connected to MySQL")

        # Create table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employee (
            eid INT PRIMARY KEY AUTO_INCREMENT,
            efn VARCHAR(14),
            eln VARCHAR(16),
            birthdate DATE
        )
        """)

        # Clear old data
        cursor.execute("DELETE FROM employee")

        # Insert sample data
        cursor.executemany("""
        INSERT INTO employee (efn, eln, birthdate)
        VALUES (%s, %s, %s)
        """, [
            ("Alice", "Smith", "2000-04-16"),
            ("Bob", "John", "1999-12-10"),
            ("Charlie", "Brown", "2001-04-16"),
            ("David", "Lee", "1998-07-22")
        ])

        conn.commit()

        # Drop procedure if exists
        cursor.execute("DROP PROCEDURE IF EXISTS Birthmonthdate")

        # Create procedure
        procedure_sql = """
        CREATE PROCEDURE Birthmonthdate()
        BEGIN
            DECLARE done INT DEFAULT FALSE;
            DECLARE id INT;
            DECLARE fn VARCHAR(14);
            DECLARE ln VARCHAR(16);
            DECLARE bdate DATE;

            DECLARE mycursor CURSOR FOR
            SELECT eid, efn, eln, birthdate FROM employee
            WHERE MONTH(birthdate)=MONTH(CURRENT_DATE)
            AND DAY(birthdate)=DAY(CURRENT_DATE);

            DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

            OPEN mycursor;

            fetch_loop: LOOP
                FETCH mycursor INTO id, fn, ln, bdate;

                IF done THEN
                    LEAVE fetch_loop;
                END IF;

                SELECT id, fn, ln, bdate;
            END LOOP;

            CLOSE mycursor;
        END
        """

        cursor.execute(procedure_sql)
        print("Procedure created successfully")

        # ▶️ Call procedure
        cursor.callproc('Birthmonthdate')

        print("\nEmployees with birthday today:\n")

        # Fetch results from stored procedure
        for result in cursor.stored_results():
            rows = result.fetchall()
            for row in rows:
                print(row)

    except Error as e:
        print("Error:", e)

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("\nConnection closed")

main()