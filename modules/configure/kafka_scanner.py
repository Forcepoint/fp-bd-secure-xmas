import os
from colorama import Fore, init
from confluent_kafka import Consumer

# Current file directory details
file = os.path.realpath(__file__)
filedir = os.path.dirname(file)
parentdir = os.path.dirname(filedir)

# Initialise colors for terminal
init()

# Print out header
print(Fore.CYAN + '-' * 13 + Fore.RESET)
print('Kafka Scanner')
print(Fore.CYAN + '-' * 13 + Fore.RESET)

# Validate kafka bus settings
while True:
    print()
    print('At this point you should have already placed the SSL certs in the relevant folder on this machine.')
    print()
    print(Fore.CYAN + 'Please enter the host address of the kafka server: ' + Fore.RESET, end='')
    kafka_server=input()
    print(Fore.CYAN + 'Please enter the ssl cert password: ' + Fore.RESET, end='')
    kafka_ssl_password=input()
    print(Fore.CYAN + 'Please provide a unique name for your scanner: ' + Fore.RESET, end='')
    kafka_scanner_name=input()
    print()
    kafka_settings = {
        'bootstrap.servers': kafka_server,
        'group.id': 'kafka_scanner_clients',
        'client.id': 'kafka_scanner_client_%s' % kafka_scanner_name,
        'enable.auto.commit': True,
        'session.timeout.ms': 6000,
        'security.protocol': 'SSL',
        'ssl.ca.location': '/Certs/client-ca.cer',
        'ssl.certificate.location': '/Certs/client.cer',
        'ssl.key.location': '/Certs/client.key',
        'ssl.key.password': kafka_ssl_password,
        'auto.offset.reset': 'smallest'
    }
    try:
        consumer = Consumer(kafka_settings)
        consumer.subscribe(['ENTITY_RISK_LEVEL'])
    except:
        print(Fore.RED + 'There was an issue with your kafka consumer settings. Please ensure the SSL certs are in the correct directory and your settings are correct.')
        continue
    print(Fore.GREEN + 'Your kafka settings were successful. Moving on.')
    break

# Write out configuration file
print()
print(Fore.CYAN + 'Writing Kafka Scanner settings configuration...' + Fore.RESET)
with open(parentdir + '\\settings.py', 'a+') as f:
    f.write('# KAFKA SETTINGS\n')
    f.write('KAFKA_SETTINGS={\n')
    for k, v in kafka_settings.items():
        f.write('\t\'%s\': \'%s\',\n' % (k, v))
    f.write('}\n\n')
print()
print(Fore.GREEN + 'Kafka Scanner configuration successfully written!' + Fore.RESET)
print()