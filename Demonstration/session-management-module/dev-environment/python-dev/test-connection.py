import mysql.connector

host = "session-management-db-service"
user = "session-manager"
password = "uitcisco"
database = "SessionManagementDB"

try:
    
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    if connection.is_connected():
        print("Connect successed")

except mysql.connector.Error as err:
    print(f"Connect failed: {err}")

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("closed")
