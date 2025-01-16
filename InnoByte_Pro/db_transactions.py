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

def Db_init(host, username, password):
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
            if(Db_table_init(host,username,password,db_name)):
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


def Db_table_init(host,username,password,database):
    if not all([host,username,password,database]):
        print("Database Credentials (Host,Username,Password,Database) -> needed.....")
    else:
        try:
            connection,cursor = sqlMount(host,username,password,database)
            if connection.is_connected():
                create_table_query = """
                            CREATE TABLE IF NOT EXISTS User (
                                 ID INT NOT NULL AUTO_INCREMENT,
                                 name VARCHAR(255) NOT NULL,
                                 username VARCHAR(255) UNIQUE NOT NULL,
                                 password VARCHAR(255) NOT NULL,
                                 PRIMARY KEY (ID)
                            )
                            """
                cursor.execute(create_table_query)
                connection.commit()
                return True
            else:
                print("Query Problem")
        except Error as db_error:
            print(f"Database Error: {db_error}")
            return False


def Db_User_register(host,username,password,db):
    name = str(input("Name"))
    u_username = str(input("Username"))
    u_password = str(input("Password"))
    if not all([name,u_username,u_password]):
        print("Credentials is needed")
    else:
        try:
            connection,cursor = sqlMount(host,username,password,db)
            if connection.is_connected():
                cursor.execute("SELECT * FROM User WHERE username = %s", (username,))
                if cursor.fetchone():
                    print("User already exists. Please choose a different username.")
                    return False

                cursor.execute(
                    "INSERT INTO User (name, username, password) VALUES (%s, %s, %s)",
                    (name, u_username,u_password)
                )
                connection.commit()
                print("Registration successful!")
            else:
                print("Query Problem")
        except Error as db_error:
            print(f"Database Error: {db_error}")
            return False



