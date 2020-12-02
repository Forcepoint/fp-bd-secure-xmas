import datetime
import os
import sys
from modules import settings

parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'libs')
sys.path.append(vendor_dir)

import pyodbc


class reg(object):
    def __init__(self, cursor, row):
        for (attr, val) in zip((d[0] for d in cursor.description), row):
            setattr(self, attr, val)

class DBConnector:
    """
    Class representing a connection to the Database.
    """

    current_partition = ''

    def __init__(self):
        """
        Initialise instance of the class.
        """
        self.current_partition = self.get_latest_partition()

    def table_fields_by_name(self, sql):
        """
        Retrieve table fields using field name.
        """

        rows = []
        cursor = self.execute_sql(sql)
        for row in list(cursor):
            rows.append(reg(cursor, row))
        return rows


    def get_latest_partition(self):
        """
        Retrieve latest partition.
        By default the DB is split into 90 day partitions.
        """

        get_partitions = 'SELECT MAX([PARTITION_INDEX]) FROM [wbsn-data-security].[dbo].[PA_EVENT_PARTITION_CATALOG]'
        partition = self.execute_sql(get_partitions).fetchall()[0][0]
        return partition


    def get_events(self, date):
        """
        Retrieve events from Database.
        """

        events_query = 'SELECT * FROM [wbsn-data-security].[dbo].[PA_EVENTS_%s] WHERE [INSERT_DATE] > \'%s\' ORDER BY [INSERT_DATE]' % (self.current_partition, date)
        return self.execute_sql(events_query).fetchall()


    def execute_sql(self, sql_statement):
        """
        Execute SQL on the database.
        """

        connection_string = 'Driver={SQL Server};Server=%s;Port=%s;Database=wbsn-data-security;Trusted_Connection=%s;UID=%s;PWD=%s;' % (settings.DB_HOST, settings.DB_PORT, 'yes' if settings.DB_TRUSTED else 'no', settings.DB_USER, settings.DB_PASSWORD)
        conn = pyodbc.connect(connection_string)

        cursor = conn.cursor()
        return cursor.execute(sql_statement)

    def execute_policy_events(self, row):
        """
        Retrieve policy events from Database.
        """

        return self.execute_sql(
            'SELECT * FROM [wbsn-data-security].[dbo].[PA_EVENT_POLICIES_%s] where EVENT_ID = %s' % (self.partition, row))

    def query_events(self, row):
        """
        Retrieve events from Database.
        """

        pa_events_query = 'SELECT * FROM [wbsn-data-security].[dbo].[PA_EVENTS_%s] where ID = %s'
        return self.table_fields_by_name(pa_events_query % (self.partition, row))

    def query_users(self, source_id):
        """
        Retrieve users from Database.
        """

        users_query = 'SELECT * FROM [wbsn-data-security].[dbo].[PA_MNG_USERS] where ID = %s'
        return self.table_fields_by_name(users_query % source_id)

    def get_event_details(self, date='1970-01-01 0:00:00.000'):
        """
        Retrieve required details for event.
        Utilised by user handler.
        """

        events = []
        self.partition = self.get_latest_partition()
        db_event_list = self.get_events(date)

        for row in db_event_list:
            policy_events = self.execute_policy_events(row[0])
            for policy in policy_events:
                source = self.query_events(row[0])[0]
                user = self.query_users(source.SOURCE_ID)[0]
                event = {
                    'source_id': source.SOURCE_ID,
                    'insert_date': source.INSERT_DATE,
                    'event_id': policy.EVENT_ID,
                    'full_name': user.FULL_NAME,
                    'login_name': user.LOGIN_NAME,
                    'email': user.EMAIL,
                    'severity': policy.SEVERITY,

                }
                events.append(event)

        return events