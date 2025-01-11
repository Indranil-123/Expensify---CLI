#importing the python Click Library
import click
from pyfiglet import Figlet
import mysql.connector
from db_transactions import *
from getpass import getpass


Blank = " "
#Code inititaion

@click.group()
@click.version_option(version='0.01',prog_name='ExpensiFy CLI')
def main():
    """Please Initiate the CLI Program with init Command"""
    pass


#User Manual Function
@main.command()
def init():
    f = Figlet(font="slant")
    print(f.renderText("Expensify CLI"))
    print()


#Authentication Purpose
@main.command()
def Auth():
    username = input("Please enter your username: ").strip()
    password = getpass("Please enter your password: ")

    if not username or not password:
        print("Error: Username and password cannot be empty. Please try again.")
        return

    connection, cursor = sqlMount("localhost", "root", "", "expensify")
    if connection and connection.is_connected():
        try:
            print(f"Username: {username}")
            print("Authentication successful.")
        except Exception as e:
            print(f"Error during authentication: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Database connection failed. Please check your credentials and try again.")


if __name__ =='__main__':
    main()