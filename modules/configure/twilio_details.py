import os
from colorama import Fore, init
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# Current file directory details
file = os.path.realpath(__file__)
filedir = os.path.dirname(file)
parentdir = os.path.dirname(filedir)

# Initialise colors for terminal
init()

# Print out header
print(Fore.CYAN + '-' * 18 + Fore.RESET)
print('Twilio Details')
print(Fore.CYAN + '-' * 18 + Fore.RESET)

print()
print('Now we shall setup your Twilio account details. These are found online when logged into Twilio.')  
while True:
    print()
    print(Fore.CYAN + 'What is your Twilio SID? ' + Fore.RESET, end='')
    twilio_sid = input()
    print(Fore.CYAN + 'What is your Twilio token? ' + Fore.RESET, end='')
    twilio_token = input()
    print(Fore.CYAN + 'What is the source phone number for calls? ' + Fore.RESET, end='')
    twilio_phone_number = input()
    print()
    print(Fore.CYAN + 'Would you like to validate these details by calling your phone (y/n)? ' + Fore.RESET, end='')
    validated = input()
    if validated == 'Y' or validated == 'y':
        print(Fore.CYAN + 'What phone number would you like to call (ensure it includes the country code)? ' + Fore.RESET, end='')
        number = input()
    
        client = Client(twilio_sid, twilio_token)
        client.calls.create(
            url='http://demo.twilio.com/docs/voice.xml',
            to=number,
            from_=twilio_phone_number
        )

        print(Fore.CYAN + 'Did you receive a phone call? ' + Fore.RESET, end='')
        received = input()
        if received != 'y' and received != 'Y':
            print(Fore.RED + 'There was an issue with the call. Please try again.' + Fore.RESET)
            continue
        break
    break

# Write out configuration file
print()
print(Fore.CYAN + 'Writing Call Server configuration...' + Fore.RESET)
with open(parentdir + '\\settings.py', 'a+') as f:
    f.write('# TWILIO SETTINGS\n')
    f.write('TWILIO_PHONE_NUMBER=\'%s\'\n' % twilio_phone_number)
    f.write('TWILIO_SID=\'%s\'\n' % twilio_sid)
    f.write('TWILIO_TOKEN=\'%s\'\n\n' % twilio_token)
print()
print(Fore.GREEN + 'Call Server configuration successfully written!' + Fore.RESET)
print()