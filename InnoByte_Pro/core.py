import click
import mysql.connector
from db_transactions import *
from pyfiglet import Figlet




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

    if not all([host, username]):
        print("The Host, Username, Password is can't be empty")
        return

    if not Db_init(host,username,password):
        print("Something Went wrong")
    else :
        print("database initialized")

@main.command()
def Authentication():
    usr_username = input("Your Username : ").strip()
    usr_password = input("Your password : ").strip()

    if not all([usr_username,usr_password]):
        print("All fields are needed...")
        return

    conn, cur = sqlMount('localhost','root','', "expensify")
    print(conn)
    if conn and conn.is_connected():
        try:

            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cur.execute(query, (usr_username, usr_password))
            data = cur.fetchone()

            if data:
                print("thanks successfully Logged in")
                user_global = data[0]
                print(f"your User id Is : {user_global} ")
                return True
            else:
                print("You are not valid user so you need to register")
                if(Db_User_register('localhost','root','', "expensify")):
                    print("Registration Successful")
                    Authentication()
        except Exception as e:
            print(f"Error in authentication : {e}")
        finally:
            cur.close()
            conn.close()
    else:
        print("Database connection failed Please Try again")

@main.command()
def Budget():
    usr_username = input("Please enter your personal username").strip()
    b_month = input("please enter month in this format YYYY-MM :").strip()
    budget = input("enter your budget :").strip()

    if not all([usr_username,b_month,budget]):
        print("All fields are needed...")
        return

    conn, cur = sqlMount('localhost','root','', "expensify")
    if conn and conn.is_connected():
        try:
            user_id = find_user_id(usr_username)
            cur.execute("""
                                             INSERT INTO budgets (user_id, month, budget)
                                             VALUES (%s, %s, %s)
                                             ON DUPLICATE KEY UPDATE budget = %s
                                            """, (user_id, b_month, budget, budget))
            conn.commit()
            print("The budget is successfully Assigned")

        except mysql.connector.Error as e:
            print(f"error {e}")
        finally:
            cur.close()
            conn.close()


@main.command()
def transaction():
    username = input("Username : ").strip()
    amount = int(input("Amount :"))
    category = input("Category :").strip()
    type = input("Income/Expenses :")
    date = input("Date(YYY-MM-DD)").strip()

    if not all([amount,category,type,date]):
        print("all fields needed...")
        return

    conn, cur = sqlMount('localhost','root','', "expensify")
    try:
        if conn.is_connected():
            user_id = find_user_id(username)
            month = date[:7]
            cur.execute("""
                            SELECT budget, COALESCE(SUM(amount), 0) AS total_expenses
                            FROM budgets
                            LEFT JOIN transactions ON budgets.user_id = transactions.user_id AND MONTH(transactions.date) = MONTH(%s)
                            WHERE budgets.user_id = %s AND budgets.month = %s
                        """, (date, user_id, month))
            data = cur.fetchone()
            budget, expense = data
            if expense + amount > budget:
                print("Your amount is crossed the limit of budget")
        cur.execute("""
                         INSERT INTO transactions (user_id, amount, category, type, date)
                          VALUES (%s, %s, %s, %s, %s)
                      """, (user_id, amount, category, type, date))
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Error {e}")
    finally:
        conn.close()


@main.command()
def report():
    username = input("Username : ").strip()
    print("1 for yearly report")
    print("1 for monthly report")
    print("1 for category wise")
    ch = input("your Choice :").strip()

    conn, cur = sqlMount('localhost','root','', "expensify")
    user_id = find_user_id(username)
    try:
        if ch == "1":
            month = input("Enter the month in YYYY-MM format : ").strip()
            q = """
                        SELECT 
                            category, 
                            type, 
                            SUM(amount) AS total_amount 
                        FROM transactions 
                        WHERE user_id = %s AND DATE_FORMAT(date, '%%Y-%%m') = %s 
                        GROUP BY category, type
                    """
            cur.execute(q, (user_id, month))
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
                        WHERE user_id = %s AND YEAR(date) = %s 
                        GROUP BY category, type
                    """
            cur.execute(q, (user_id, year))
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
                        WHERE user_id = %s 
                        GROUP BY category, type
                    """
            cur.execute(q, (user_id,))
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
