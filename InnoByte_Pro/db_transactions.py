import mysql.connector
from mysql.connector import Error


def sqlMount(host, user, password, database):
        try:
            # Establish the connection
            conn= mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )

            if conn.is_connected():
                # Create a cursor object
                cursor = conn.cursor()
                print("Connection to MySQL database established successfully.")
                return conn, cursor

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
    if not all([host,username,database]):
        print("Database Credentials (Host,Username,Password,Database) -> needed.....")

    else:
        try:
            connection,cursor = sqlMount(host,username,password,database)
            if connection.is_connected():
                cursor.execute("""
                           CREATE TABLE `expensify`.`users` 
                           (`id` INT NOT NULL AUTO_INCREMENT , `username` VARCHAR(255) NOT NULL ,
                            `password` VARCHAR(255) NOT NULL , 
                            PRIMARY KEY (`id`)) ENGINE = InnoDB;
                        """)
                cursor.execute("""
                            CREATE TABLE IF NOT EXISTS transactions (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    user_id INT NOT NULL,
                                    amount DECIMAL(10, 2) NOT NULL,
                                    category VARCHAR(255) NOT NULL,
                                    type ENUM('income', 'expense') NOT NULL,
                                    date DATE NOT NULL,
                                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
                        """)
                cursor.execute("""
                            CREATE TABLE IF NOT EXISTS budgets (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                user_id INT NOT NULL,
                                month YEAR(4) NOT NULL,
                                budget DECIMAL(10, 2) NOT NULL,
                                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                                UNIQUE (user_id, month)
                            )
                        """)
                connection.commit()
                return True
            else:
                print("Query Problem")
        except Error as error:
            print(f"Database Error: {error}")
            return False


def Db_User_register(host,username,password,db):
    u_username = str(input("Username"))
    u_password = str(input("Password"))
    if not all([u_username, u_password]):
        print("Credentials is needed")
    else:
        try:
            connection,cursor = sqlMount(host,username,password,db)
            if connection.is_connected():
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                if cursor.fetchone():
                    print("User already exists. Please choose a different username.")
                    return False

                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s)",
                    (u_username,u_password)
                )
                connection.commit()
                print("Registration successful!")
            else:
                print("Query Problem")
        except Error as db_error:
            print(f"Database Error: {db_error}")
            return False


def find_user_id(username):
    conn, cur = sqlMount('localhost','root','', "expensify")

    if conn and conn.is_connected():
        try :
            q = "SELECT id FROM users WHERE username = %s"
            cur.execute(q, (username))
            data = cur.fetchone()
            if data:
                user_id = data[0]
                return user_id
        except mysql.connector.Error as e:
            print(f"Error for Finding User Id Error : {e}")






