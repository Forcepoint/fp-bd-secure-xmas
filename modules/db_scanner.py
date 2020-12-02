import datetime
import json
import time
from modules import DBConnector, settings, User

class DBScanner:
    """
    Class representing a database scanner.
    This polls for new events in the database.
    """

    ad = None
    db = None

    def __init__(self, ad=None):
        """
        Initialise an instance of the KafkaScanner. 

        Params:
            - ad - The Active Directory Connector to be user.
        """
        self.ad = ad
        self.db = DBConnector()
        print('DB Scanner initialised.')

    def scan_for_events(self):
        """
        Method for scanning database for new
        events on an interval.
        """

        # Load current date and time in correct format
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        while True:

            # Read latest datetime from file. If not present, write.
            try:
                with open('datetime.json', 'r+') as file:
                    data = json.load(file)
                    current_datetime = data['current_datetime']
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                with open('datetime.json', 'w+') as file:
                    file.write(json.dumps({'current_datetime': current_datetime}))

            # Get and handle events.
            events = self.db.get_event_details(current_datetime)
            for event in events:

                if not event['severity'] == 1:
                    continue

                username = None
                login_name = event['login_name']
                email = event['email']

                user_to_handle = ''
                if username:
                    user_to_handle = username.split('\\')[1] if '\\' in username else username
                elif login_name:
                    user_to_handle = login_name.split('\\')[1] if '\\' in login_name else login_name
                elif email:
                    user_to_handle = email.split('@')[0]
                else:
                    print('No username could be sourced from this event \'%s\'.' % event['event_id'])
                    continue

                with open('datetime.json', 'w+') as file:
                    file.write(json.dumps({'current_datetime': event['insert_date'].strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}))
                    
                user = User(user_to_handle)
                user.handle()

            time.sleep(10)
        