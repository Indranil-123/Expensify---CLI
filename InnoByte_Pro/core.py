import click
import mysql.connector
from db_transactions import *
from pyfiglet import Figlet

user_global = None

Db_dict ={'id': 1}

@click.group()
@click.version_option(version='0.01', prog_name="Expensify CLI")
def main():
    header = Figlet(font='slant')
    print(header.renderText('ExpensiFy CLI'))

@main.command()
def init():
    host = input("Host :").strip()
    username = input("username :").strip()
    password = input("Passsword :").strip()

    if not all([host, username, password]):
        print("The Host, Username, Password is can't be empty")
        return

    Db_dict.update({'host':host, 'username' : username, 'password': password})

    if not Db_init(host,username,password):
        print("Something Went wrong")
    else :
        print("database initialized")

@main.command()
def Authentication():
    global user_global
    usr_username = input("Your Username").strip()
    usr_password = input("Your password").strip()

    if not all([usr_username,usr_password]):
        print("All fields are needed...")
        return

    conn , cur = sqlMount(Db_dict['host'], Db_dict['username'],Db_dict['password'], "expensify")
    if conn.is_connected():
        try:
            query = "SELECT * FROM User WHERE username = %s AND password = %s"
            cur.execute(query, (usr_username, usr_password))
            data = cur.fetchone()

            if data:
                print("thanks successfully Logged in")
                user_global = data['id']
                return True
            else:
                print("You are not valid user so you need to register")
                if(Db_User_register(Db_dict['host'], Db_dict['username'],Db_dict['password'], "expensify")):
                    print("Registration Successful")
                    Authentication()
        except Exception as e:
            print(f"Error in authentication : {e}")
        finally:
            cur.close()
            conn.close()
    else:
        print("Database connection faled Please Try again")

@main.command()
def Budget():
    usr_username = str(input("Please enter your personal username"))
    b_month = str(input("please enter month in this format YYYY-MM :"))
    budget = str(input("enter your budget :"))
    global user_global

    if not user_global:
        print("you need to log in first")
        return

    if not all([usr_username,b_month,budget]):
        print("All fields are needed...")
        return

    conn, cur = sqlMount(Db_dict['host'], Db_dict['username'], Db_dict['password'], "expensify")
    if conn.is_connected():
        try:
            q = "SELECT id FROM users WHERE username = %s"
            cur.execute(q,(usr_username))
            res = cur.fetchone()
            if res:
                user_global = res[0]
                cur.execute("""
                                 INSERT INTO budgets (user_id, month, budget)
                                 VALUES (%s, %s, %s)
                                 ON DUPLICATE KEY UPDATE budget = %s
                                """, (user_global, b_month, budget, budget))
                conn.commit()
                print("The budget is successfully")
        except mysql.connector.Error as e:
            print(f"error {e}")
        finally:
            cur.close()
            conn.close()

@main.command()
def transaction():
    global user_global

    if not user_global:
        print("You need to Login First")
        return

    amount = input("Amount :").strip()
    category = input("Category :").strip()
    type = input("Income/Expenses :")
    date = input("Date(YYY-MM-DD)").strip()

    if not all([user_global,amount,category,type,date]):
        print("all fields needed...")
        return

    conn, cur = sqlMount(Db_dict['host'], Db_dict['username'], Db_dict['password'], "expensify")
    try:
        if conn.is_connected():
            month = date[:7]
            cur.execute("""
                            SELECT budget, COALESCE(SUM(amount), 0) AS total_expenses
                            FROM budgets
                            LEFT JOIN transactions ON budgets.user_id = transactions.user_id AND MONTH(transactions.date) = MONTH(%s)
                            WHERE budgets.user_id = %s AND budgets.month = %s
                        """, (date, user_global, month))
            data = cur.fetchone()
            budget, expense = data
            if expense + amount > budget:
                print("Your amount is crossed the limit of budget")
        cur.execute("""
                         INSERT INTO transactions (user_id, amount, category, type, date)
                          VALUES (%s, %s, %s, %s, %s)
                      """, (user_global, amount, category, type, date))
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Error {e}")
    finally:
        conn.close()


@main.command()
def report():
    username = input("Username").strip()
    print("1 for yearly report")
    print("1 for monthly report")
    print("1 for category wise")
    ch = input("your Choise").strip()

    conn, cur = sqlMount(Db_dict['host'], Db_dict['username'], Db_dict['password'], "expensify")
    try:
        if ch == "1":
            month = input("Enter the month in YYYY-MM format : ").strip()
            q = """
                        SELECT 
                            category, 
                            type, 
                            SUM(amount) AS total_amount 
                        FROM transactions 
                        WHERE username = %s AND DATE_FORMAT(date, '%%Y-%%m') = %s 
                        GROUP BY category, type
                    """
            cur.execute(q, (username, month))
            res = cur.fetchall()

            if res:
                print("monthly report is :")
                for row in res:
                    print(f"Category: {row['category']}, Type: {row['type']}, Total Amount: {row['total_amount']}")
            else:
                print("No transactions have made yet")

        elif ch == "2":
            year = input("Enter the year (YYYY): ").strip()
            q = """
                        SELECT 
                            category, 
                            type, 
                            SUM(amount) AS total_amount 
                        FROM transactions 
                        WHERE username = %s AND YEAR(date) = %s 
                        GROUP BY category, type
                    """
            cur.execute(q, (username, year))
            res = cur.fetchall()

            if res:
                print("yearly result")
                for val in res:
                    print(f"Category: {val['category']}, Type: {val['type']}, Total Amount: {val['amount']}")
            else:
                print("no transtsaction")
        elif ch == "3":
            q = """
                        SELECT 
                            category, 
                            type, 
                            SUM(amount) AS total_amount 
                        FROM transactions 
                        WHERE username = %s 
                        GROUP BY category, type
                    """
            cur.execute(q, (username))
            res = cur.fetchall()

            if res:
                for row in res:
                    print(f"Category: {row['category']}, Type: {row['type']}, Total Amount: {row['total_amount']}")
            else:
                print("No transactions have made yet")
        else:
            print("invalid choice")
    except mysql.connector.Error as e:
        print(f"Error:{e}")
    finally:
        conn.close()



if __name__ == '__main__':
    main()
