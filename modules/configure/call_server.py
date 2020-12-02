import os
from colorama import Fore, init

# Current file directory details
file = os.path.realpath(__file__)
filedir = os.path.dirname(file)
parentdir = os.path.dirname(filedir)

# Initialise colors for terminal
init()

# Print out header
print(Fore.CYAN + '-' * 13 + Fore.RESET)
print('Call Server')
print(Fore.CYAN + '-' * 13 + Fore.RESET)

# Get variables
print()
print(Fore.CYAN + 'What is the root FQDN for this machine: ' + Fore.RESET, end='')
root_url = input()
print(Fore.CYAN + 'On which port should the call server run: ' + Fore.RESET, end='')
port = input()

# Write out configuration file
print()
print(Fore.CYAN + 'Writing Call Server configuration...' + Fore.RESET)
with open(parentdir + '\\settings.py', 'a+') as f:
    f.write('# CALL SERVER SETTINGS\n')
    f.write('ROOT_URL=\'%s\'\n' % root_url.rstrip('/').lstrip('http://').lstrip('https://'))
    f.write('PORT=%s\n\n' % port)
print()
print(Fore.GREEN + 'Call Server configuration successfully written!' + Fore.RESET)
print()
