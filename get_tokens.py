import requests
from flask import Flask, request
import datetime
from datetime import datetime, timedelta
import webbrowser
import json
from os.path import exists
import glob
from credentials import credentials
from card import card

#gets the access and refresh tokens

oauth_authorization_url = credentials["oauth_authorization_url"]

app = Flask(__name__)

class Storage():
    access_token = None
    at_expires_in = None
    refresh_token = None
    rt_expires_in = None
    release_date = None

class Org():
      filename = None

Store = Storage()
org = Org()

@app.route('/', methods=['GET', 'POST'])
def hook():
    if request.method == 'GET':
        if "code" in request.args:
            # state = request.args.get("state")  # Captures value of the state.
            code = request.args.get("code")  # Captures value of the code.
            print("OAuth code:", code)
            get_tokens('authorization_code', code)
            shutdown_func = request.environ.get('werkzeug.server.shutdown')
            if shutdown_func is None:
                raise RuntimeError('Not running werkzeug')
            shutdown_func()
            return "Access granted, shutting down..."


def get_tokens(token_type, token):
    client_id = credentials["client_id"]
    client_secret = credentials["client_secret"]
    redirect_uri = credentials["redirect_uri"]
    url = "https://webexapis.com/v1/access_token"
    payload = {
        "grant_type": token_type,
        "client_id": client_id,
        "client_secret": client_secret
    }

    if token_type == "authorization_code":
        payload["code"] = token
        payload["redirect_uri"] = redirect_uri

    if token_type == "refresh_token":
        payload["refresh_token"] = token

    print('from get_tokens this is the payload: ', payload)

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.request("POST", url, headers=headers, data=payload)
    while response.status_code == 401:
        print("We got 401")
        new_response = requests.request("POST", url, headers=headers, data=payload)
        print('from get_tokens this is the response: ', new_response)
        response = new_response

    response = response.json()
    print('from get_tokens this is the response: ', response)
    now = datetime.now()
    access_token = response['access_token']
    at_exp = response['expires_in']
    #calculate the date and time of expiration based on the delta time expressed in seconds
    at_expiration = now + timedelta(0, at_exp)
    refresh_token = response['refresh_token']
    rt_exp = response['refresh_token_expires_in']
    #calculate the date and time of expiration based on the delta time expressed in seconds
    rt_expiration = now + timedelta(0, rt_exp)
    Store.access_token = access_token
    Store.refresh_token = refresh_token
    Store.at_expires_in = str(at_expiration) #expiration in time and date
    Store.rt_expires_in = str(rt_expiration)
    Store.at_exp = at_exp #expiration in seconds
    Store.rt_exp = rt_exp
    Store.at_release_date = str(datetime.now())
    token_details = vars(Store)
    print(f"token details are {token_details} and type is {type(token_details)}")
    expiry_date = token_details['at_expires_in']
    print(f"expiry date for access token is {expiry_date} and variable type is {type(expiry_date)}")
    response = requests.get("https://webexapis.com/v1/organizations", headers = {'Authorization': 'Bearer ' + access_token})
    response = response.json()
    friendly_name_sc = response["items"][0]["displayName"].lower()
    friendly_name = ''.join(filter(str.isalnum, friendly_name_sc))
    print(friendly_name)
    write_file(token_details, friendly_name)
    return

def get_my_access_token(roomId):
    data = read_file("")
    if data != {}:
       at_expires_in = data['at_expires_in']
       rt_expires_in = data['rt_expires_in']
       print(at_expires_in, type(at_expires_in))
       at_expiry_time = datetime.fromisoformat(at_expires_in)
       rt_expiry_time = datetime.fromisoformat(rt_expires_in)
       now = datetime.now()
       access_token = data['access_token']
       if at_expiry_time > now:
          bearer = access_token
          print(bearer)
       else:
          print('outdated access token is: ', access_token)
          if rt_expiry_time > now:
             refresh_token = data['refresh_token']
             get_tokens("refresh_token", refresh_token)
          else:
             start()
    else:
        start(roomId)

    new_data = read_file(org.filename)
    access_token = new_data['access_token']
    return access_token

def read_file (filename): #args: the file name
    file_dict = {}
    friendly_dict = {}
    i = 1
    for file in glob.glob("*_token.txt"):
        file_dict[str(i)] = file
        friendly_dict[(i)] = file.split("_")[0]
        i = i + 1
    if filename == "":
       print(file_dict)
       if int(i) == 2:
           filename = file_dict["1"]
           print ("filename friendly name is: ", filename)
           answer = "y" #input (f"Do you want to connect to {friendly_dict[1]}?")
           if answer.lower().startswith("n") == True:
              filename = ""

       if int(i) > 2:
         print("Which org do you want to connect to? \nPress any key to select another org ")
         for key, value in friendly_dict.items():
           print(key, ") ", value)
         answer = str(input("\nEnter value here: "))
         print("type of answer is: ", type(answer))
         #print(answer)
         if answer in file_dict:
            filename = file_dict[answer]
            print(filename)


    data = {}
    if filename != None and filename != "" and exists(filename) == True:
          with open (filename, 'r') as local_file:
              values = local_file.read()
              print(values)
              data = json.loads(values)
              org.filename = filename
    print("filename data is: ", data)
    print("filename is :", filename)
    return data

def write_file (token_details, friendly_name):  #args: the content of the file
    filename = friendly_name + "_token.txt"
    org.filename = filename
    with open (filename, 'w') as local_file:
        local_file.write(json.dumps((token_details)))


def start(roomId):
     webexUrl = "https://webexapis.com/v1/"
     bearer = credentials["bearer"]
     webexHeaders = {'Authorization': 'Bearer ' + str(bearer),
                     'Content-type': 'application/json'}
     authCard = card()
     print(authCard)
     text = f"Please authenticate\n{oauth_authorization_url}"
     payload = json.dumps({
         "roomId": roomId,
         "text": text,
         "attachments": [
                          {
                            "contentType": "application/vnd.microsoft.card.adaptive",
                            "content": authCard
                          }
                        ]
                          })
     response = requests.post(f"{webexUrl}messages", headers=webexHeaders, data=payload)
     print(response.text)
     app.run('0.0.0.0', port=5062)

if __name__ == '__main__':
    get_my_access_token()




