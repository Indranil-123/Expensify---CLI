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
