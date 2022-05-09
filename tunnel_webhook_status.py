import requests
import subprocess
from credentials import credentials


#list active webhooks on machine. Useful but not used
ngrokUrl = "http://127.0.0.1:4040/api/"
ngrokBaseUrl = "http://127.0.0.1:4040"

def ngrokStart(localPort):
   cmd = f'/Applications/ngrok http {localPort}'
   # start ngrok process
   print(f'starting ngrok, command: {cmd}')
   subprocess.Popen(cmd.split())


def tunnelList():
   try:
      response = requests.get(ngrokUrl + "tunnels")
      resp = response.json()
      print("ngrok tunnels:", resp)
      tunnels = resp["tunnels"]
      l = len(tunnels)
      for i in range(l):
         print(tunnels[i]["public_url"])
      return tunnels
   except:
      tunnels = "ngrokStart"
      return tunnels


def tunnelKill(tunnels):
   l = len(tunnels)
   print("tunnels are", tunnels)
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
tunnels = tunnelList()
# check the status of the webhooks
bearer = credentials["bearer"]
webexHeaders = {'Authorization': 'Bearer ' + str(bearer),
                'Content-type': 'application/json'}
header = {'Authorization': 'Bearer ' + bearer}
webexUrl = "https://webexapis.com/v1/"
webhookUrl = f"{webexUrl}webhooks"
response = requests.get(webhookUrl, headers=webexHeaders)
resp = response.json()
print("Webex tunnels", resp)
items = resp["items"]
webhookNo = len(items)

for i in range (webhookNo):
   targetUrl = items[i]["targetUrl"]
   print(targetUrl)

   clear = input("do you want to delete ngrok webhooks?")
   if clear.lower().startswith("y"):
      for i in range (webhookNo):
         if "ngrok" in targetUrl:
            webhookId = items[i]["id"]
            deleteUrl = f"{webhookUrl}/{webhookId}"
            print(deleteUrl)
            response = requests.delete(webhookUrl, headers=header)

            headers = {
               'Authorization': bearer
            }
            payload ={}
            response = requests.request("DELETE", deleteUrl, headers=header, data=payload)

            print(response.text)

            print(response)


            tunnelKill(tunnels)



