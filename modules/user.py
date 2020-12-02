import os
import subprocess
import sys
from modules import settings, ADConnector
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

class User:
    """
    Class representing a user in the Active Directory.
    """

    username = ''
    phone_number = ''
    ad = None

    def __init__(self, username):
        """
        Initialise an instance of the User class with a username
        and a connection to the Active Directory.

        Params:
            - username - The user represented by this class.
        """

        self.username = username
        print('User \'%s\' initialised.' % self.username)

    def handle(self):
        """
        Handle a user by disabling their account on
        all active directories, logging out their sessions
        and notifying them by phone.
        """

        windows = True
        azure = True
        numbers = []

        if settings.WINDOWS_DIR:
            self.ad = ADConnector()
            self.ad.bind()
            windows, numbers = self.disable_windows()
            self.ad.unbind()
        
        if settings.AZURE_DIR:
            azure, numbers = self.disable_azure()

        self.notify(numbers=numbers)


    def disable_windows(self):
        """
        Disable user on Windows Active Directory.
        """

        disable = self.ad.disable_user(self.username)

        if not disable:
            print('There was an issue with modifying user \'%s\' and setting their account to disabled.' % self.username)
            return False

        # Logout the user from all active sessions.
        print('Logging out user \'%s\' from all active sessions.' % self.username)
        command = 'Invoke-Command -ComputerName %s -ScriptBlock { C:/scripts/kick.ps1 %s }' % (settings.AD_HOST, self.username)
        process = subprocess.Popen(['powershell.exe', command])
        result = process.communicate()
        print('Logout of user \'%s\' complete.' % self.username)

    
        # Get user phone number and call.
        query = self.ad.query_user(self.username)

        if not query:
            print('The user \'%s\' could not be contacted as they have no phone number associated with their account.' % self.username)
            return False

        numbers = [entry.telephoneNumber for entry in query]

        return True, numbers

    def disable_azure(self):
        """
        Disable user on Azure Active Directory.
        """
        print('Disabling user \'%s\' in Azure active directory and logging them out.' % self.username)
        process = subprocess.run(r'C:\Windows\sysnative\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Unrestricted powershell/azure.ps1 -user %s' % self.username, shell=True, stdout=subprocess.PIPE)
        result = process.stdout
        numbers = result.decode('utf-8').split(',')
        numbers = [number.strip('\n').strip(' ') for number in numbers if number.strip('\n').strip(' ') != '']
        print('Logout of user \'%s\' complete.' % self.username)

        return True, numbers

    def notify(self, numbers=[]):
        """
        Notify user that their account has been disabled.
        """

        if numbers:
            number = numbers[0]
        else:
            return

        # Create Twilio client and send call request.
        print('Creating call request to user %s.' % self.username)

        try:
            client = Client(settings.TWILIO_SID, settings.TWILIO_TOKEN)
            client.calls.create(
                url='http://%s:%s/play' % (settings.ROOT_URL, settings.PORT),
                to=number,
                from_=settings.TWILIO_PHONE_NUMBER
            )

        except TwilioRestException as e:
            print('Error when contacting user \'%s\': %s' % self.username, e)

        