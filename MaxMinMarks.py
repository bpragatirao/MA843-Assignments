import mysql.connector
from mysql.connector import Error

def main():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",          # replace with your password
            database="college_db"
        )

        cursor = conn.cursor()
        print("Connected to MySQL")

        # Create table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Student (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(50),
            Age INT
        )
        """)

        # Clear old data
        cursor.execute("DELETE FROM Student")

        # Insert sample data
        cursor.executemany("""
        INSERT INTO Student (name, Age) VALUES (%s, %s)
        """, [
            ("Alice", 20),
            ("Bob", 22),
            ("Charlie", 18),
            ("David", 25)
        ])

        conn.commit()

        # Drop procedure if exists
        cursor.execute("DROP PROCEDURE IF EXISTS MaxMinAge")

        # Create procedure (corrected version)
        procedure_sql = """
        CREATE PROCEDURE MaxMinAge(OUT maxAge INT, OUT minAge INT)
        BEGIN
            DECLARE currAge INT;
            DECLARE maxSoFar INT DEFAULT 0;
            DECLARE minSoFar INT DEFAULT 1000;
            DECLARE done INT DEFAULT 0;

            DECLARE cur CURSOR FOR
                SELECT Age FROM Student;

            DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

            OPEN cur;

            read_loop: LOOP
                FETCH cur INTO currAge;

                IF done = 1 THEN
                    LEAVE read_loop;
                END IF;

                IF currAge > maxSoFar THEN
                    SET maxSoFar = currAge;
                END IF;

                IF currAge < minSoFar THEN
                    SET minSoFar = currAge;
                END IF;

            END LOOP;

            CLOSE cur;

            SET maxAge = maxSoFar;
            SET minAge = minSoFar;
        END
        """

        cursor.execute(procedure_sql)
        print("Procedure created successfully")

        # Call procedure
        args = cursor.callproc('MaxMinAge', [0, 0])

        print("\nResults:")
        print("Maximum Age =", args[0])
        print("Minimum Age =", args[1])

    except Error as e:
        print("Error:", e)

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("\nConnection closed")

main()