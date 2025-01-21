# Importing necessary libraries
import click
from pyfiglet import Figlet
import mysql.connector
from db_transactions import *
from getpass import getpass
import wmi

# Constants
APP_VERSION = '0.01'
APP_NAME = 'ExpensiFy CLI'
DEFAULT_FONT = 'slant'

Db_dict = {'id':1}


# Helper Functions
def display_banner():
    """Displays the application banner."""
    banner = Figlet(font=DEFAULT_FONT)
    print(banner.renderText(APP_NAME))


def check_server_status(process_name="xampp-control.exe"):
    try:
        f = wmi.WMI()
        for process in f.Win32_Process():
            if process.Name.lower() == process_name.lower():
                return True
        return False
    except Exception as e:
        print(f"Error checking server status: {e}")
        return False


def validate_inputs(**kwargs):
    for field, value in kwargs.items():
        if not value:
            print(f"Error: {field.capitalize()} is required.")
            return False
    return True


# CLI Group Initialization
@click.group()
@click.version_option(version=APP_VERSION, prog_name=APP_NAME)
def main():
    """Welcome to Expensify CLI. Use the appropriate commands to get started."""
    pass


# Init Command
@main.command()
def init():
    """Initializes the Expensify CLI."""
    display_banner()
    print("Initializing, please wait...")

    if not check_server_status():
        print("Error: Your server application is not running. Please start it and try again.")
        return

    host = input("Host: ").strip()
    username = input("Username: ").strip()
    password = getpass("Password: ").strip()

    Db_dict.update([('host',host),('username',username),('password',password)])

    if not validate_inputs(host=host, username=username):
        return
    #check the connectivity
    if not Db_init(host, username, password):
        print("Error: Something went wrong. Please try again.")
    else:
        print("Database initialized successfully!")


# Auth Command
@main.command()
def auth():
    """Authenticates the username and Password"""
    username = input("Please enter your username: ").strip()
    password = getpass("Please enter your password: ")

    # Validate inputs
    if not validate_inputs(username=username, password=password):
        return

    # Connect to the database
    connection, cursor = sqlMount(Db_dict['host'], Db_dict['username'],Db_dict['password'], "expensify")
    if connection and connection.is_connected():
        try:
            query = f"SELECT * FROM User WHERE username = {username} AND password = {password}"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                print("Thanks You are Successfully Logged in")
                return True
            else:
                print("You are not a valid User so You need to Register First")
                if(Db_User_register(Db_dict['host'], Db_dict['username'],Db_dict['password'], "expensify")):
                    print("Registration Successful")
                    auth()
        except Exception as e:
            print(f"Error during authentication: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Error: Database connection failed. Please check your credentials and try again.")


@main.command()
def Budget():
    username = str(input("Please enter your personal username"))
    month = str(input("please enter month in this format YYYY-MM :"))
    budget = str(input("enter your budget :"))

    if not validate_inputs(username=username, month=month,budget=budget):
        return

    connection, cursor = sqlMount(Db_dict['host'], Db_dict['username'], Db_dict['password'], "expensify")

    if connection and connection.is_connected():
        try:
            cursor.execute("""
                        INSERT INTO budgets (user_id, month, budget)
                        VALUES (%s, %s, %s)
                        ON DUPLICATE KEY UPDATE budget = %s
                    """, (user_id, month, budget, budget))
            connection.commit()
            print("The Budget is successfully added")
        except mysql.connector.Error as e:
            print(f"Error during authentication: {e}")
        finally:
            cursor.close()
            connection.close()

main.command()
def transaction():
    user_id = input("user_id :").strip()
    amount = input("Amount :").strip()
    category = input("Category :").strip()
    type = input("Income/Expenses :")
    date = input("Date(YYY-MM-DD)").strip()

    if not validate_inputs(amount,category,type,date):
        return

    connection , cursor = sqlMount(Db_dict['host'], Db_dict['username'], Db_dict['password'], "expensify")

    try :
        if connection and connection.is_connected():
            month = date[0:7]
            cursor.execute("""
                            SELECT budget, COALESCE(SUM(amount), 0) AS total_expenses
                            FROM budgets
                            LEFT JOIN transactions ON budgets.user_id = transactions.user_id AND MONTH(transactions.date) = MONTH(%s)
                            WHERE budgets.user_id = %s AND budgets.month = %s
                        """, (date, user_id, month))
            data = cursor.fetchone()
            budget, expense = data;
            if expense + amount > budget:
                print("Your Amount is crossed the limits of budget")

        cursor.execute("""
                         INSERT INTO transactions (user_id, amount, category, type, date)
                          VALUES (%s, %s, %s, %s, %s)
                      """, (user_id, amount, category, type, date))

        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error during authentication: {err}")
    finally:
        connection.close()



# Entry Point
if __name__ == '__main__':
    main()
