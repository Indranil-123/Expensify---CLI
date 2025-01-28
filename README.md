
# Expensify CLI Application Documentation


## Authors

- [@Indranil Bakshi](https://github.com/Indranil-123)


## Installation

Install my-project

```bash
  install python
  
  pip install mysql.connector

  pip install pyfiglet
```
    
## Documentation

[Documentation](https://linktodocumentation)
Table of Contents
1. Installation
2. Getting Started
3. Commands
    - init
    - authenticate
    - budget
    - transaction
    - report
4. Database Schema
5. Error Handling


Installation
### Prerequisites
- Python 3.7 or above.
- MySQL server installed and running.
- Required Python libraries:
  - click
  - mysql-connector-python
  - pyfiglet

### Installation Steps
1. Clone the repository or copy the script to your local machine.
2. Install the required Python libraries:
   pip install click mysql-connector-python pyfiglet
3. Ensure the MySQL database server is running and accessible.
Getting Started
1. Initialize the CLI with the init command to set up the database connection.
2. Authenticate or register as a user to access other features.
3. Start managing your finances by setting budgets, recording transactions, and generating reports.
Commands
### init
Initializes the database connection by collecting the MySQL host, username, and password.

Usage:
expensify init

Input Prompts:
- Host
- Username
- Password

Description:
- Updates the application with the MySQL server connection details.
- Ensures the connection is valid.
Database Schema
### Database: expensify


