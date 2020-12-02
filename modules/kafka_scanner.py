import json
from confluent_kafka import Consumer, KafkaError
from modules import settings, User

class KafkaScanner:
    """
    Class representing a kafka scanner.
    This polls for new messages on the kafka bus and
    upon receiving them handles the user.
    """

    ad = None
    consumer = None

    def __init__(self, ad=None):
        """
        Initialise an instance of the KafkaScanner. 

        Params:
            - ad - The Active Directory Connector to be user.
        """
        self.ad = ad
        self.consumer = Consumer(settings.KAFKA_SETTINGS)
        self.consumer.subscribe(['ENTITY_RISK_LEVEL'])
        print('Kafka Scanner initialised.')

    def scan_for_message(self):
        """
        Method for running a kafka bus scan.
        Polls for new messages and upon receiving one,
        if the user risk level is 4/5 it handles the 
        user.
        """

        while True:
            msg = self.consumer.poll(0.1)
            if msg is None:
                continue
            elif not msg.error():
                message = json.loads(msg.value().decode('utf8'))
                print('Received message: {0}'.format(message))
                if message['risk_level'] >= 4:
                    user = User(message['user_id'].replace(' ', '.'))
                    user.handle()
            elif msg.error().code() == KafkaError._PARTITION_EOF:
                print('End of partition reached {0}/{1}'
                        .format(msg.topic(), msg.partition()))
            else:
                print('Error occured: {0}'.format(msg.error().str()))
        