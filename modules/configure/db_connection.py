import os
import pyodbc
from colorama import Fore, init

# Current file directory details
file = os.path.realpath(__file__)
filedir = os.path.dirname(file)
parentdir = os.path.dirname(filedir)

# Initialise colors for terminal
init()

# Print out header
print(Fore.CYAN + '-' * 18 + Fore.RESET)
print('Database Connection')
print(Fore.CYAN + '-' * 18 + Fore.RESET)

windows_auth = False

while True:
    print()
    try:
        # Check whether the SQLServer is using trusted connections.
        print(Fore.CYAN + 'Is your database configured to use Windows authentication (y/n)? ' + Fore.RESET, end='')
        response = input() 
        valid_inputs = {
            'y': True,
            'Y': True,
            'n': False,
            'N': False
        }
        windows_auth = valid_inputs[response]
    except KeyError:
        print(Fore.RED + 'That wasn\'t a valid response. Please try again.' + Fore.RESET)
        continue

    print()
    print(Fore.CYAN + 'What is the host address of the database? ' + Fore.RESET, end='')
    db_host = input()
    print(Fore.CYAN + 'What port is the database running on? ' + Fore.RESET, end='')
    db_port = input()
    db_user = ''
    db_password = ''

    if not windows_auth:
        print(Fore.CYAN + 'What is the username used to login and read from the database? ' + Fore.RESET, end='')
        db_user = input()
        print(Fore.CYAN + 'What password is used for logging in? ' + Fore.RESET, end='')
        db_password = input()

    connection_string = 'Driver={SQL Server};Server=%s;Port=%s;Database=wbsn-data-security;Trusted_Connection=%s;UID=%s;PWD=%s;' % (db_host, db_port, 'yes' if windows_auth else 'no', db_user, db_password)

    try:
        conn = pyodbc.connect(connection_string, timeout=10)
        cursor = conn.cursor()
    except pyodbc.OperationalError:
        print()
        print(Fore.RED + 'There was an issue connecting to the database. Please try again.' + Fore.RESET)
        continue

    break

print()
print(Fore.CYAN + 'Writing DB Scanner settings configuration...' + Fore.RESET)
with open(parentdir + '\\settings.py', 'a+') as f:
    f.write('# DATABASE SETTINGS\n')
    f.write('DB_TRUSTED=%s\n' % windows_auth)
    f.write('DB_HOST=\'%s\'\n' % db_host)
    f.write('DB_PORT=%s\n' % db_port)
    f.write('DB_USER=\'%s\'\n' % db_user)
    f.write('DB_PASSWORD=\'%s\'\n\n' % db_password)
print()
print(Fore.GREEN + 'DB Scanner configuration successfully written!' + Fore.RESET)
print()