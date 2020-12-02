import json
import os
import subprocess
from colorama import init, Fore
from ldap3 import Connection, Server, NONE, NTLM

# Current file directory details
file = os.path.realpath(__file__)
filedir = os.path.dirname(file)
parentdir = os.path.dirname(filedir)

# Initialise colors for terminal
init()

# Print out header
print(Fore.CYAN + '-' * 16 + Fore.RESET)
print('Active Directory')
print(Fore.CYAN + '-' * 16 + Fore.RESET)

valid_inputs = {
    'y': True,
    'Y': True,
    'n': False,
    'N': False
}

# Check which directories the user wishes to install.
while True:
    print()
    print(Fore.CYAN + 'Would you like to connect to a windows active directory (y/n)? ' + Fore.RESET, end='')
    windows_dir = input()
    if windows_dir not in valid_inputs:
        print(Fore.RED + 'Please enter a valid value of \'y\' or \'n\'.' + Fore.RESET)
        continue

    print(Fore.CYAN + 'Would you like to connect to an azure active directory (y/n)? ' + Fore.RESET, end='')
    azure_dir = input()
    if azure_dir not in valid_inputs:
        print(Fore.RED + 'Please enter a valid value of \'y\' or \'n\'.' + Fore.RESET)
        continue

    if not valid_inputs[windows_dir] and not valid_inputs[azure_dir]:
        print(Fore.RED + 'Please configure at least one active directory.' + Fore.RESET)
        continue

    break     

# Get active directory host and verify it's pingable.
while True and valid_inputs[windows_dir]:
    print()
    print(Fore.CYAN + 'What is the host address of your windows active directory? ' + Fore.RESET, end='')
    ad_host = input()
    p = subprocess.Popen('ping.exe -n 1 %s' % ad_host, stdout=subprocess.PIPE)
    p.wait()
    if p.poll() == 0:
        print(Fore.GREEN + 'That host address was successfully reached. Moving on.' + Fore.RESET)
        break
    else:
        print(Fore.RED + 'There was an error with the host address provided. It was unreachable.' + Fore.RESET)
print()

# Check how the user wishes to connect
while True and valid_inputs[windows_dir]:
    print(Fore.CYAN + 'Would you like to use SSL when connecting to windows active directory (y/n)? ' + Fore.RESET, end='')
    ssl = input()
    if ssl not in valid_inputs:
        print(Fore.RED + 'Please enter a valid value of \'y\' or \'n\'.' + Fore.RESET)
        continue
    ad_use_ssl = valid_inputs[ssl]
    break


# Get required details for logging into Active Directory
while True and valid_inputs[windows_dir]:
    print(Fore.CYAN + 'What is the domain of your windows active directory e.g random.domain.com? ' + Fore.RESET, end='')
    ad_domain = input()
    print()
    print(Fore.CYAN + 'Username: ' + Fore.RESET, end='')
    ad_username = input()
    print(Fore.CYAN + 'Password: ' + Fore.RESET, end='')
    ad_password = input()

    try:
        server = Server(
            ad_host, 
            get_info=NONE,
            connect_timeout=5
        )
        connection = Connection(
            server, 
            user=r'%s\%s' % (ad_domain.split('.')[0], ad_username),
            password=ad_password,
            authentication=NTLM,
        )
        connection.bind()
    except:
        print(Fore.RED + 'There was an issue with the active directory details provided. Please try again.' + Fore.RESET)
        continue
    print(Fore.GREEN + 'The windows active directory settings have been validated. Moving on.' + Fore.RESET)
    break

# Get azure active directory details 
while True and valid_inputs[azure_dir]:
    print(Fore.CYAN + 'What is the global administrator email address used to login to Azure Portal? ' + Fore.RESET, end='')
    azure_email = input()
    print(Fore.CYAN + 'What is the password for the global administrator account? ' + Fore.RESET, end='')
    azure_password = input()
    print(Fore.CYAN + 'What is Tenant ID found on the Azure Active Directory page? ' + Fore.RESET, end='')
    tenant_id = input()

    data = {
        'azure_email': azure_email,
        'azure_password': azure_password,
        'tenant_id': tenant_id
    }

    with open('powershell/config.json', 'w+', encoding='utf-8') as config:
        json.dump(data, config, ensure_ascii=False, indent=2)
    break

# Write out configuration file
print()

with open(parentdir + '\\settings.py', 'a+') as f:
    f.write('# ACTIVE DIRECTORY SETTINGS\n')
    f.write('WINDOWS_DIR=%s\n' % valid_inputs[windows_dir])
    f.write('AZURE_DIR=%s\n' % valid_inputs[azure_dir])

if valid_inputs[windows_dir]:
    print(Fore.CYAN + 'Writing active directory configuration...' + Fore.RESET)
    with open(parentdir + '\\settings.py', 'a+') as f:
        f.write('AD_HOST=\'%s\'\n' % ad_host)
        f.write('AD_DOMAIN=\'%s\'\n' % ad_domain)
        f.write('AD_USERNAME=\'%s\'\n' % ad_username)
        f.write('AD_PASSWORD=\'%s\'\n' % ad_password)
        f.write('AD_USE_SSL=%s\n' % ad_use_ssl)
        f.write('AD_DISABLE=514\n\n')
print()
print(Fore.GREEN + 'Active directory configuration successfully written!' + Fore.RESET)
print()