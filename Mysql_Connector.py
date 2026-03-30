import mysql.connector
print("Student Database")

try:
    # Establishing the connection
    connection = mysql.connector.connect(
        host="localhost",      # Server address (e.g., 127.0.0.1)
        user="root",  # MySQL username (default is often 'root')
        password="", # Your MySQL password
        database="test"  # The specific database to use
    )

    if connection.is_connected():
        print("Successfully connected to the database")

except mysql.connector.Error as err:
    print(f"Error: {err}")



# try:
#     connection = mysql.connector.connect(
#         host='localhost',
#         user='root',      # Default XAMPP user
#         password='',      # Default XAMPP password is empty
#         database='test'   # A default database that comes with XAMPP
#     )
#     if connection.is_connected():
#         print("Connected to XAMPP MySQL database!")
# except Exception as e:
#     print(f"Error: {e}")