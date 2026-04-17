import mysql.connector
from mysql.connector import Error

def main():
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",    
            database="stud"
        )

        cursor = conn.cursor()
        print("Connected to MySQL")

        # Create table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stud (
            id INT PRIMARY KEY AUTO_INCREMENT,
            marks INT
        )
        """)

        # Clear old data
        cursor.execute("DELETE FROM stud")

        # Insert sample data
        cursor.executemany(
            "INSERT INTO stud (marks) VALUES (%s)",
            [(80,), (75,), (90,), (60,)]
        )

        conn.commit()

        #  Drop procedure if exists
        cursor.execute("DROP PROCEDURE IF EXISTS TotalMarks")

        # Create stored procedure
        procedure_sql = """
        CREATE PROCEDURE TotalMarks (OUT param1 INT)
        BEGIN
            DECLARE a INT;
            DECLARE b INT DEFAULT 0;
            DECLARE total INT DEFAULT 0;

            DECLARE cur1 CURSOR FOR SELECT marks FROM stud;
            DECLARE CONTINUE HANDLER FOR NOT FOUND SET b = 1;

            OPEN cur1;

            read_loop: LOOP
                FETCH cur1 INTO a;
                IF b = 1 THEN
                    LEAVE read_loop;
                END IF;
                SET total = total + a;
            END LOOP;

            CLOSE cur1;

            SET param1 = total;
        END
        """

        cursor.execute(procedure_sql)
        print("Procedure created successfully")

        # ▶️ Call procedure
        cursor.callproc('TotalMarks', [0])

        for result in cursor.stored_results():
            pass  # not needed here

        # MySQL connector stores OUT values in args
        args = cursor.callproc('TotalMarks', [0])
        print("Total Marks =", args[0])

    except Error as e:
        print("Error:", e)

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Connection closed")

if __name__ == "__main__":
    main()