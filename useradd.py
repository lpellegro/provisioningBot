import ldap3
from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException, LDAPBindError
from credentials import credentials

#creates user in AD

ad_admin = credentials ["ad_admin"]
ad_password = credentials["ad_password"]
search_base = credentials["search_base"]
ad_ip = credentials["ad_ip"]
userpassword = credentials["user_default_password"]
def connect_ldap_server(first_name, last_name, userid, email, tel):
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
                print(f"User {userid} already exists")
                telephoneNumber = results[i]["raw_attributes"]["telephoneNumber"][0].decode('UTF-8')
                print(f"old telephone number is {telephoneNumber}")
                print(f"new telephone number is {tel}")
                if telephoneNumber != tel:
                    modifyFlag = True
                #sys.exit()
        #print(sAMAccountNames)

        cn = f'{first_name} {last_name},{search_base}'
        dn = f'{userid},{search_base}'
        attributes_change =  {
                         'sn': ('MODIFY_REPLACE', last_name),
                         'givenName': ('MODIFY_REPLACE', first_name),
                         'displayName': ('MODIFY_REPLACE', f'{first_name} {last_name}'),
                         'mail': ('MODIFY_REPLACE', email),
                         'sAMAccountName': ('MODIFY_REPLACE', userid),
                         'userPrincipalName': ('MODIFY_REPLACE', email),
                         'telephoneNumber': ('MODIFY_REPLACE', f'{tel}')
                         }
        attributes = {
                             'sn': last_name,
                             'givenName': first_name,
                             'displayName': f'{first_name} {last_name}',
                             'mail': email,
                             'sAMAccountName':userid,
                             'userPrincipalName':email,
                             'userPassword': userpassword,
                             'telephoneNumber': f'{tel}',
                             'pwdLastSet': '-1'
                         }
        if modifyFlag == True:
            print("dn is", f'sAMAccountName={dn}')
            connection.modify(f'cn={cn}', {'telephoneNumber': [('MODIFY_REPLACE', [tel])]})
            #connection.modify(f'cn={cn}', attributes_change)
        else:

            connection.add(f'cn={cn}', 'User', attributes)

            connection.modify(f'cn={cn}', {'userAccountControl': ('MODIFY_REPLACE', '544')})
        print(connection.result)

    except LDAPBindError as e:
        connection = e
        print (connection)



