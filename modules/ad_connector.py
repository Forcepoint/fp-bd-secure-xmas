import ssl
from modules import settings
from ldap3 import ALL, Connection, NTLM, Tls, Server, MODIFY_ADD, MODIFY_REPLACE, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES

class ADConnector:
    """
    Class representing the Active Directory connection.
    """

    connection = None

    def bind(self):
        """
        Open a connection to the active directory server.
        Previous sessions are always closed beforehand.
        """

        if settings.AD_USE_SSL:
            self.bind_ssl()
        else:
            self.bind_open()

    def bind_open():
        """
        Open a connection to the windows active
        directory server. This is not secure.
        """

        try:
            # Connect to Active Directory Server via NTLM
            server = Server(
                settings.AD_HOST, 
                get_info=ALL
            )
            self.connection = Connection(
                server, 
                user=r'%s\%s' % (settings.AD_DOMAIN.split('.')[0], settings.AD_USERNAME),
                password=settings.AD_PASSWORD,
                authentication=NTLM
            )
            if not self.connection.bind():
                raise Exception
            print('Connected to Active Directory.')
                
        except Exception:
            print('There was an exception when connecting to the windows active directory.')

    def bind_ssl(self):
        """
        Open a secure connection to the windows active
        directory server. All previous sessions are closed
        before hand.
        """
        try:
            # Connect to Active Directory Server via SSL
            tls =  Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1_2)
            server = Server(
                settings.AD_HOST, 
                use_ssl=True,
                tls=tls
            )
            self.connection = Connection(
                server, 
                user=r'%s\%s' % (settings.AD_DOMAIN.split('.')[0], settings.AD_USERNAME),
                password=settings.AD_PASSWORD,
            )
            if not self.connection.bind():
                raise Exception
            print('Connected to Windows Active Directory.')
        except:
            print('There was an exception when connecting to the windows active directory.')

    def disable_user(self, username):
        """
        Disable a user account in the active directory based on
        the provided username parameter.
        """

        print('Updating user %s\'s account and setting it to disabled.' % username)
        domain = ','.join(['dc=' + dc for dc in settings.AD_DOMAIN.split('.')])
        username = username.replace('.', ' ')
        query = 'cn=%s,cn=Users,%s' % (username, domain) 
        result = self.connection.modify(
            query, 
            {'userAccountControl': [
                    MODIFY_REPLACE, 
                    [settings.AD_DISABLE]
                ]
            }
        )

        return result

    def query_user(self, username):
        """
        Query a user in the active directory based on
        the provided username parameter.
        """

        print('Retrieving user %s\'s phone number.' % username)
        domain = ','.join(['dc=' + dc for dc in settings.AD_DOMAIN.split('.')])
        user = username.replace(' ', '.')
        self.connection.search(
            domain, 
            '(&(objectClass=user)(sAMAccountName=%s))' % username, 
            attributes=['telephoneNumber']
        )

        return self.connection.entries

    def unbind(self):
        """
        Close the current active directory connection.
        """

        self.connection.unbind()