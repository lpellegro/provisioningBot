
import subprocess
import shutil
import requests
import json
from flask import Flask, request, Response, render_template, jsonify, session
from file_generator import csvConversion
from requests_toolbelt.multipart.encoder import MultipartEncoder
from provisioning import provisioning
from credentials import credentials
from contacts import provision_ucm
from messages import messages, messageText, messageFile, webexHeaders, simpleHeaders
from webexteamsbot import TeamsBot
from delete_config import deleteConfig
import time
import sys

#initial file to be launched

path = credentials["path"]
ngrokUrl = "http://127.0.0.1:4040/api/"
ngrokBaseUrl = "http://127.0.0.1:4040"
bearer = credentials["bearer"]
webexUrl = credentials["webexUrl"]
webhookExists = False
botPersonId = credentials["botPersonId"]
msg = messages()
tunnelCounter = 0
simpleHead = simpleHeaders()
headers = simpleHead.headers
webexHead = webexHeaders(bearer, "application/json")


def ngrokStart(localPort):
    cmd = f'{credentials["ngrokDir"]}ngrok http {localPort}'
    # start ngrok process
    print(f'starting ngrok, command: {cmd}')
    subprocess.Popen(cmd.split())
    tunnels = tunnelList()
    print("tunnels are", tunnels)
    while tunnels == "ngrokStart":
        tunnelCounter = 1;
        print("waiting ngrok tunnel")
        time.sleep(2)
        tunnels = tunnelList()
        if tunnelCounter > 30:
            sys.exit()

def tunnelList():
    print("in tunnellist now")
    try:
        response = requests.get(ngrokUrl + "tunnels")
        resp = response.json()
        print(resp)
        tunnels = resp["tunnels"]
        print("ngrok tunnels are", tunnels)
        # print(tunnels)
        return tunnels
    except:
        tunnels = "ngrokStart"
        return tunnels

def tunnelStart():
    tunnels = tunnelList()
    tunnelCounter = 0
    while tunnels == []:
        body = {
            "addr": localPort,
            "proto": "http",
            "name": "web"
        }
        data = json.dumps(body)
        startUrl = f"{ngrokUrl}tunnels"
        print(startUrl)
        response = requests.post(startUrl, headers=headers, data=data)
        resp = response.json()
        print(resp)
        if "error_code" in resp.keys():
            tunnels = []
            time.sleep(2)
            tunnelCounter += 1
            if tunnelCounter > 30:
                sys.exit()
        else:
            tunnels = tunnelList()
    tunnelUrl = []
    if len(tunnels) == 0:
        exit()
    for j in range(len(tunnels)):
        tunnelUrl.append(tunnels[j]["public_url"])
    return tunnelUrl

def tunnelKill(tunnels):
    l = len(tunnels)
    for i in range(l):
        name = tunnels[i]["name"]
        uri = tunnels[i]["uri"]
        print(uri)
        deleteUrl = f"{ngrokBaseUrl}{uri}"
        print("deleteUrl is:", deleteUrl)
        try:
            response = requests.delete(deleteUrl)
            resp = response.json()
            print(resp)
        except:
            pass

class incomingMessage():
    def __init__(self, request):
        self.contactflag = False
        self.provisioningflag = False
        req = request.json
        if "personId" in req["data"]:
            self.personId = req["data"]["personId"]
            if req["data"]["personId"] != botPersonId and "roomId" in req["data"]:
                self.roomId = req["data"]["roomId"]
                print("room ID is:", self.roomId)
                self.personId = req["data"]["personId"]
                self.personEmail = req["data"]["personEmail"]
                self.messageId = req["data"]["id"]
                print("message ID is:", self.messageId)
                print("person ID is:", self.personId)
                print("person email is: ", self.personEmail)
                if req["resource"] == "memberships" and req["event"] == "created":
                    if "cisco.com" in self.personEmail or "ent-pa.com" in self.personEmail or "cloudentpa.com" in self.personEmail:
                        msgText = messageText(self.roomId, msg.welcomeMsg)
                    else:
                        msgText = messageText(self.roomId, msg.notWelcomeMsg)
                    body = json.dumps(msgText.data)
                    response = requests.post(f"{webexUrl}messages", headers=webexHead.webexHeaders, data=body)
                    print(response.text)

            if "files" in req["data"] and self.personId != botPersonId and "cisco.com" in self.personEmail or "ent-pa.com" in self.personEmail or "cloudentpa.com" in self.personEmail:
                filepath = req["data"]["files"][0]
                print("file path is:", filepath)

                print(f"Sending request to: {webexUrl}contents/{self.messageId}")
                fileinfo = requests.head(filepath, headers=webexHead.webexSimpleHeaders)
                print(fileinfo.headers)
                if "Content-Disposition" in fileinfo.headers:
                    rawFilename = fileinfo.headers["Content-Disposition"]
                    print(rawFilename)

                    filename = rawFilename.split("filename=")[1]
                    filename = filename.replace("\"", "")
                    print(filename)
                    fileNewName = f"{self.messageId}{filename}"
                    if len(filename.split(".xls")) > 1: #this sintax doesn't work: ".xlsx" in str(filename):
                        self.provisioningflag = True
                        print("Excel file", filename)
                        teststring = filename.split(".xlsx")
                        print(teststring)
                    if ".csv" in str(filename):
                        self.contactflag = True
                        print("csv file", filename)
                print(f"contactflag is {self.contactflag} provisioningflag is {self.provisioningflag}")
                getResponse = requests.get(filepath, headers=webexHead.webexSimpleHeaders)
                print(getResponse)
                self.file = f"{path}/{fileNewName}"
                open(self.file, 'wb').write(getResponse.content)

tunnelCounter = 0
localPort = 6000
tunnels = tunnelList()
if tunnels == "ngrokStart":
   ngrokStart(localPort)
print("tunnels are:", tunnels)

while tunnels == []:
        tunnelUrl = tunnelStart()
        print("tunnelUrl is", tunnelUrl)
        tunnels = tunnelList()
        time.sleep(2)
        tunnelCounter += 1
        if tunnelCounter > 30:
            sys.exit()

tunnelUrl = tunnelStart()

# tunnelUrl = tunnels[0]["public_url"]
webhookUrl = f"{webexUrl}webhooks"
response = requests.get(webhookUrl, headers=webexHead.webexHeaders)
resp = response.json()
print("webhook list in Webex", resp)
items = resp["items"]
webhookNo = len(items)
for i in range(webhookNo):
    if items[i]["targetUrl"] in tunnelUrl:
        # webhook already exists
        print(f"webhook {items[i]['targetUrl']} already exists")
        webhookExists = True
        break
if webhookExists == False:
    webhookName = tunnelUrl[0].split("//")[-1]
    body = json.dumps({"name": webhookName,
                       "targetUrl": tunnelUrl[0],
                       "resource": "all",
                       "event": "all"
                       })

bot_email = credentials["botEmail"]
teams_token = credentials["bearer"]
bot_url = tunnelUrl[0]
bot_app_name = ("testBot")

# Create a Bot Object
bot = TeamsBot(
    bot_app_name,
    teams_bot_token=teams_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
    webhook_resource="all",
    webhook_event="all",
)
print("sending request to: ", bot_url)

# A simple command that returns a basic string that will be sent as a reply
def add_config(incoming_msg):

    print (request.data)
    dataCapture = incomingMessage (request)
    file = dataCapture.file
    personEmail = dataCapture.personEmail
    contactflag = dataCapture.contactflag
    provisioningflag = dataCapture.provisioningflag
    roomId = dataCapture.roomId
    if contactflag == True:
        usersAdd, usersDelete, records = csvConversion(file, personEmail)
        print(usersAdd)
        msgAdd = msg.addMsg
        msgDelete = msg.deleteMsg
        addFilepath = f"{path}/{usersAdd}"
        fileType = 'text/plain'
        deleteFilepath = f"{path}/{usersDelete}"
        msgAddFile = messageFile(roomId, msgAdd, usersAdd, addFilepath, fileType)
        msgDeleteFile = messageFile(roomId, msgDelete, usersDelete, deleteFilepath, fileType)

        dataAdd = msgAddFile.data
        dataDelete = msgDeleteFile.data
        url = f"{webexUrl}messages"
        mAdd = MultipartEncoder(fields=dataAdd)
        mDelete = MultipartEncoder(fields=dataDelete)
        webexSendAddFile = webexHeaders(bearer, mAdd.content_type).webexHeaders
        webexSendDeleteFile = webexHeaders(bearer, mDelete.content_type).webexHeaders
        r = requests.post(url, data=mAdd,
                          headers=webexSendAddFile)
        print(r.json())
        r = requests.post(url, data=mDelete,
                          headers=webexSendDeleteFile)
        print(r.json())
        msgText = messageText(roomId, msg.createContactMsg)

        body = json.dumps(msgText.data)
        response = requests.post(f"{webexUrl}messages", headers=webexHead.webexHeaders, data=body)
        print(response.text)

        provision_ucm(records)

        msgText = messageText(roomId, msg.doneMsg)

        data = msgText.data
        body = json.dumps(data)
        response = requests.post(f"{webexUrl}messages", headers=webexHead.webexHeaders, data=body)
        print(response.text)

    if provisioningflag == True:
        msgText = messageText(roomId, msg.provisioningMsg)
        data = msgText.data
        body = json.dumps(data)
        response = requests.post(f"{webexUrl}messages", headers=webexHead.webexHeaders, data=body)
        print(response.text)
        provisioning(file, roomId)
        msgText = messageText(roomId, msg.provisioningDone)
        data = msgText.data
        body = json.dumps(data)
        response = requests.post(f"{webexUrl}messages", headers=webexHead.webexHeaders, data=body)
        print(response.text)
    return ""

def delete_config(incoming_message):
    dataCapture = incomingMessage(request)
    file = dataCapture.file
    roomId = dataCapture.roomId
    msgText = messageText(roomId, msg.deleteConfig)
    data = msgText.data
    body = json.dumps(data)
    response = requests.post(f"{webexUrl}messages", headers=webexHead.webexHeaders, data=body)
    print(response.text)
    deleteConfig(file, roomId)
    msgText = messageText(roomId, msg.deleteConfigDone)
    data = msgText.data
    body = json.dumps(data)
    response = requests.post(f"{webexUrl}messages", headers=webexHead.webexHeaders, data=body)
    print(response.text)
    return ""

def check_memberships(api, incoming_msg):
    wl_dom = credentials["wl_dom"]

    if wl_dom and incoming_msg["event"] != "deleted":
        pemail = incoming_msg["data"]["personEmail"]
        pid = incoming_msg["data"]["personId"]
        pdom = pemail.split("@")[1]
        #plist = json.loads(wl_dom)
        print(pemail, pdom, wl_dom)
        if pdom in wl_dom or pemail == bot_email:
            # membership check succeeded
            return ""
        else:
            # membership check failed
            print("membership failed. deleting " + incoming_msg["data"]["id"])
            api.memberships.delete(incoming_msg["data"]["id"])
            api.messages.create(toPersonId=pid, markdown="You were automatically removed from the space because "
                                        "it is restricted to employees.")
            return "'" + pemail + "' was automatically removed from this space; it is restricted to only " \
                                    "internal users."

    return ""



# Add new commands to the box.
bot.add_command("add", "*", add_config)
bot.add_command("delete", "*", delete_config)
bot.add_command('memberships', '*', check_memberships)


if __name__ == "__main__":
    # Run Bot

    bot.run(host="0.0.0.0", port=6000)
