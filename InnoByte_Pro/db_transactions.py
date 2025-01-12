import mysql.connector
from mysql.connector import Error


def sqlMount(host, user, password, database):
        try:
            # Establish the connection
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )

            if connection.is_connected():
                # Create a cursor object
                cursor = connection.cursor()
                print("Connection to MySQL database established successfully.")
                return connection, cursor

        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None, None

def Db_init(host,username,password):
    try:
        db_name = "expensify"
        if not all([host, username]):
            raise ValueError("Host, username, and password must be provided.")

        #Creating the Connection
        conn = mysql.connector.connect(
            host=host,
            user=username,
            password=password
        )

        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print(f"Database '{db_name}' created successfully.")
            return True

    except ValueError as ve:
        print(f"Input Error: {ve}")
        return False

    except Error as db_error:
        print(f"Database Error: {db_error}")
        return False

    finally:
        if 'connection' in locals() and conn.is_connected():
            conn.close()
            print("MySQL connection closed.")
