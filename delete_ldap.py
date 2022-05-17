import ldap3
from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException, LDAPBindError
from credentials import credentials

import sys

#configures users in AD

ad_admin = credentials ["ad_admin"]
ad_password = credentials["ad_password"]
search_base = credentials["search_base"]
ad_ip = credentials["ad_ip"]
userpassword = credentials["user_default_password"]
def delete_ldap_user(first_name, last_name, userid):
    modifyFlag = False
    try:
        search_filter = '(&(objectClass=person)(objectClass=user))'
        # Provide the hostname and port number of the openLDAP
        server_uri = f"ldap://{ad_ip}"
        server = Server(server_uri, get_info=ALL)
        # username and password can be configured during openldap setup
        connection = Connection(server,
                                user=ad_admin,
                                password=ad_password)
        bind_response = connection.bind()  # Returns True or False
        #print (bind_response)
        connection.search(search_base=search_base,
                         search_filter=search_filter,
                         search_scope=SUBTREE,
                         attributes=['cn', 'sn', 'uid', 'uidNumber', 'sAMAccountName', 'telephoneNumber'])
        results = connection.response
        #print(results)
        print(f"{len(results)} entries")
        sAMAccountNames = []
        for i in range (len(results)):
            sAMAccountName = results[i]["raw_attributes"]["sAMAccountName"][0].decode('UTF-8')

            #print(results[i]["raw_attributes"]["sAMAccountName"][0].decode('UTF-8'))
            if sAMAccountName == userid:
                cn = f'{first_name} {last_name},{search_base}'
                connection.delete(f'cn={cn}')

                print(connection.result)

    except LDAPBindError as e:
        connection = e
        print (connection)

