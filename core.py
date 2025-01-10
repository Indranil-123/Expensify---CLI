#importing the python Click Library
import click
from pyfiglet import Figlet

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
    print("""Hello User I hope All things is Good Welcome To The Expensify for Initiating the Program first You Should
       Authenticate yourself and Connect the DataBase Along with for More Info You can visit the Help Section by --help
    """)


#Authentication Purpose
@main.command()
@click.argument('username')
@click.argument('password')
@click.option('--login')
def Auth(username,password,login):
    if login == True:
        pass
    else:
        usr_name = str(username)
        usr_pass = str(password)
        click.secho(f"You are entering the Username : {usr_name} And you are entering the password:{usr_pass}")


@main.command()
def Add():
    print("hello")


@main.command()
def Track():
    print("hello")

@main.command()
def Save():
    print()




if __name__ =='__main__':
    main()