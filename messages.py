

#includes status messages
class messages():
    def __init__(self):
        self.notWelcomeMsg = "You are not authorized to use this bot"
        self.welcomeMsg = "Attach the contact csv file from Control Hub and will be converted into a UCM compatible file.\nAttach the Excel file to provision your Webex org"
        self.addMsg = "Upload on Unified CM or Dedicated Instance to create contacts as local users"
        self.deleteMsg = "Upload on Unified CM or Dedicated Instance to delete contacts"
        self.createContactMsg = "...Creating local users as contacts on Dedicated Instance"
        self.doneMsg = "...done"
        self.provisioningMsg = "--------- PROVISIONING STARTED ----------"
        self.provisioningDone = "--------- PROVISIONING DONE ----------"
        self.adProvisioningStart = "Starting AD provisioning"
        self.diProvisioningStart = "Starting DI provisioning"
        self.awsProvisioningStart = "Starting AWS inboxes provisioning"
        self.orgProvisioningStart = "Starting org provisioning"
        self.doneWait = "AD Provisiong done. Waiting for 6 minutes to complete user sync via Directory Connector"
        self.deleteConfig = "Starting to delete users and devices"
        self.deleteConfigDone = "Config deleted"

class messageText():
      def __init__(self, roomId, text):
          self.data = {
                        "text": text,
                        "roomId": roomId
                      }

class messageFile():
      def __init__(self, roomId, text, file, filepath, filetype):
          self.data = {
                       'roomId': roomId,
                       'text': text,
                       'files': (file, open(filepath, 'rb'), filetype)
                       }

class webexHeaders():
    def __init__(self, bearer, content):

        self.webexHeaders = {'Authorization': 'Bearer ' + str(bearer),
                    'Content-type': content}
        self.webexSimpleHeaders = {'Authorization': 'Bearer ' + bearer}

class simpleHeaders ():
    def __init__(self):
        self.headers = {'Content-type': 'application/json'}
