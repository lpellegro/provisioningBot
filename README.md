This bot provisions users and devices in:
- Active Directory
- Email Server (Amazon Workmail)
- Webex organization
- Dedicated Instance/Unified CM

This bot uses ngrok to setup a public url. This url is then used to create a webhook in Webex. ngrok starts automatically and webhooks are automatically created.
You don't need that your server has a public IP. This bot can also be run in your laptop.

Add the bot to a space and send it a file. The bot will provision users and devices accordingly to the file's specified settings.

Step-by-step Installation:
1. Login to developer.webex.com with admin credentials
2. Click on your user on the top right-hand side of the web page
3. Select "My Webex Apps"
4. Create a Bot
   1. Copy the Bot access token, the Bot ID, the Bot username (email)
5. Create an Integration for OAuth
   1. Copy the Client ID, Client Secret, OAuth Authorization URL, Integration ID, Redirect URI
6. Fill in the "credentials.py" file
7. Install ngrok
8. Create a virtual environment in your server or your local machine
9. Install the following packages:
   1. pip install requests 
   2. pip install flask 
   3. pip install requests_toolbelt 
   4. pip install webexteamsbot 
   5. pip install zeep 
   6. pip install lxml 
   7. pip install boto3 
   8. pip install zeep 
   9. pip install openpyxl 
   10. pip install ldap3
10. Run the bot by launching "start_here.py" file
11. Go to your Webex app, click to the "+" button near the search window and then "Send a direct message"
12. Look for your newly created Bot through its email (Bot username) and add it to your Webex list
13. Send a provisioning file to the bot with the following commands:
    1. add
    2. delete


*** XLSX FILE SPECS FOLLOWING ***