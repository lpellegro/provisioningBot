from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from requests import Session
from requests.auth import HTTPBasicAuth
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from lxml import etree
from credentials import credentials


#convert contacts from Webex into contacts for DI/UCM and configures them as local users
def provision_ucm(contactRecords):
    disable_warnings(InsecureRequestWarning)
    user = credentials["username"]
    secret = credentials["password"]
    host = credentials["host"]
    wsdl = credentials['wsdl']

    location = 'https://{host}:8443/axl/'.format(host=host)
    binding = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"

    # Create a custom session to disable Certificate verification.
    # In production you shouldn't do this,
    # but for testing it saves having to have the certificate in the trusted store.
    session = Session()
    session.verify = False
    session.auth = HTTPBasicAuth(user, secret)

    transport = Transport(cache=SqliteCache(), session=session, timeout=20)
    history = HistoryPlugin()
    client = Client(wsdl=wsdl, transport=transport, plugins=[history])
    service = client.create_service(binding, location)

    def show_history():
        for item in [history.last_sent, history.last_received]:
            print(etree.tostring(item["envelope"], encoding="unicode", pretty_print=True))
    usercreateflag = False
    usermodifyflag = False
    usercreate = ""
    totalContacts = len (contactRecords)
    for i in range (totalContacts):
        try:
            resp = service.listUser(
                searchCriteria={
                    'userid': contactRecords[i][2]
                },
                returnedTags={
                    'userid': True,
                    'telephoneNumber': True,
                    'mailid': True,
                    'directoryUri': True
                }

            )
            print(resp, '\n')
            if resp["return"] == None:
               usercreateflag = True
            else:
               usermodifyflag = True

        except Exception as err:
            print(f'\nZeep error: listUser: {err}')
            #sys.exit(1)
            print('\nlistUser response:\n')

        #contactRecord = [firstName, lastName, userId, displayName,phoneNo, mobile, home, pager, email, sipUri]

        user = {
            'firstName': contactRecords[i][0],
            'lastName': contactRecords[i][1],
            'userid': contactRecords[i][2],
            # 'password': 'cisco',
            'displayName': contactRecords[i][3],
            'telephoneNumber': contactRecords[i][4],
            'mobileNumber': contactRecords[i][5],
            'homeNumber': contactRecords[i][6],
            'pagerNumber': contactRecords[i][7],
            'mailid': contactRecords[i][8],
            'directoryUri': contactRecords[i][9],
            'presenceGroupName': 'Standard Presence group'

        }

        if usercreateflag == True:

            try:
                resp = service.addUser(user)

            except Fault as err:
                print(f'Zeep error: addUser: {err}')
                print('err.message is:', err.message)
                if "duplicate" in err.message:
                    print ("duplicate user")
                    pass
                #sys.exit(1)


        if usermodifyflag == True:
          try:
            resp = service.updateUser(

                   userid = contactRecords[i][2],
                   firstName = contactRecords[i][0],
                   lastName = contactRecords[i][1],
                   displayName = contactRecords[i][3],
                   telephoneNumber = contactRecords[i][4],
                   mobileNumber = contactRecords[i][5],
                   homeNumber = contactRecords[i][6],
                   pagerNumber = contactRecords[i][7],
                   mailid = contactRecords[i][8],
                   directoryUri = contactRecords[i][9],
                   presenceGroupName = 'Standard Presence group'


            )

            print(resp, '\n')
          except Exception as err:
            print(f'\nZeep error: updateUser: {err}')
            #sys.exit(1)
            print('\nupdateUser response:\n')

            if "duplicate" in err.message:
                print ("duplicate in err")
                pass




