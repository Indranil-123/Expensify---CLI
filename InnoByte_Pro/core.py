#importing the python Click Library
import click
from pyfiglet import Figlet
import mysql.connector
from db_transactions import *


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
    username = str(input("please enter your username: \n"))
    password = str(input("please enter your password: \n"))

    if len(username) == 0 or len(password) == 0 :
        print("please fill the values")
    else:
        connection,cursor = sqlMount("localhost","root","","expensify")
        if connection.is_connected():
            print(username)
            print(password)






if __name__ =='__main__':
    main()