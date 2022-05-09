import csv
import random
import string
from datetime import datetime
from credentials import credentials

#file converter from Webex to DI for contacts
path = credentials["path"]

def getKey(dict, val):
    for key, value in dict.items():
        if val == value.lower():
            return key

    return None

def csvConversion(file, personEmail):
        primaryPhone = "work_extension"
        newEmail = personEmail.replace(".", "_")
        fileName1stPart = newEmail.replace("@", "_")
        #read csv file and create a dictionary called contacts, and another dictionary called ucmItems
        with open(file, encoding='utf-8-sig') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            # the following lines create a nested dictionary named contacts:
            # {'contact1': {'Display Name': 'Coffee Machine', 'Contact UUID': '18df2635-458c-4c78-bc19-10ee7da4e99c', 'First Name': '', 'Last Name': '', 'Phone Number 1': '+14085554321', 'Phone Number 1 Type': 'work', 'Phone Number 2': '+13280669002', 'Phone Number 2 Type': 'mobile', 'Phone Number 3': '', 'Phone Number 3 Type': '', 'Phone Number 4': '', 'Phone Number 4 Type': '', 'Phone Number 5': '', 'Phone Number 5 Type': '', 'Contact Email': 'coffe@caffeineorchamomille.com', 'SIP URI': '', 'Address Street': '', 'Address City': '', 'Address State': '', 'Address Country': '', 'Address Zip': ''}, 'contact2': {'Display Name': 'Taxi Service London', 'Contact UUID': '323159b7-9440-4d31-8cb0-269ca9167e4e', 'First Name': '', 'Last Name': '', 'Phone Number 1': '+442079460096', 'Phone Number 1 Type': 'work', 'Phone Number 2': '', 'Phone Number 2 Type': '', 'Phone Number 3': '', 'Phone Number 3 Type': '', 'Phone Number 4': '', 'Phone Number 4 Type': '', 'Phone Number 5': '', 'Phone Number 5 Type': '', 'Contact Email': 'taxi@abcinc.com', 'SIP URI': '', 'Address Street': '', 'Address City': '', 'Address State': '', 'Address Country': '', 'Address Zip': ''}, 'contact3': {'Display Name': 'Taxi Service San Jose', 'Contact UUID': 'f3525b71-b0ff-4dd4-a4fe-1f260a74c6f6', 'First Name': '', 'Last Name': '', 'Phone Number 1': '+14085551234', 'Phone Number 1 Type': 'work', 'Phone Number 2': '', 'Phone Number 2 Type': '', 'Phone Number 3': '', 'Phone Number 3 Type': '', 'Phone Number 4': '', 'Phone Number 4 Type': '', 'Phone Number 5': '', 'Phone Number 5 Type': '', 'Contact Email': 'transport@abcinc.com', 'SIP URI': '', 'Address Street': '', 'Address City': '', 'Address State': '', 'Address Country': '', 'Address Zip': ''}}
            titles =[]
            contacts = {}
            contact = {}
            numbers = {}
            ucmItems = {}
            for row in csv_reader:
                if line_count == 0:
                    rowLen = len(row)
                    for i in range(rowLen):
                        titles.append(row[i])
                    print("titles are:", titles)
                    line_count += 1
                else:
                    current_contact = "contact" + str(line_count)
                    for j in range(rowLen):
                        title = titles[j]
                        contact[title] = row[j]
                    contacts[current_contact] = contact
                    contact = {} #or the dictionary will be broken
                    line_count += 1
            print(f'Processed {line_count} lines.')
            print(f"contacts from csv file are: \n {contacts}")
            totalContacts = len (contacts)
            phones = {}
            for i in range(totalContacts):
                index="contact"+str(i+1)
                # populates first and last name with display name if they are not populated
                print ("contact is:", index, contacts[index])
                displayName = contacts[index]['Display Name']
                print("Record is:", displayName, index, i)
                firstName = contacts[index]['First Name']
                lastName = contacts[index]['Last Name']
                email = contacts[index]['Contact Email']
                sipUri = contacts[index]['SIP URI']
                if lastName == "":
                    lastName = displayName
                if firstName == "":
                    firstName = displayName
                displayNameListCapital = displayName.split()
                displayNameList = [x.lower() for x in displayNameListCapital]
                userId = "_".join(displayNameList)
                userId = userId.replace("'", "")
                userId = userId + "_" + "wxc_contact"
                ucmItems [index] = {"firstName": firstName, "lastName": lastName, "displayName": displayName, "userId": userId, "email": email, "sipUri": sipUri}
                for i in range (5):
                    keyNumber = f"Phone Number {i+1}"
                    keyNumberType = f"Phone Number {i+1} Type"
                    if contacts [index][keyNumberType] != "" and contacts [index][keyNumber] != "":
                     phones[contacts [index][keyNumberType]] = contacts [index][keyNumber]
                ucmItems[index]["phones"] = phones
                numbers[index] = phones #creates a dictionary {'contact1': ['+14085554321', '+14085559002'], 'contact2': [...]}
                phones = {}
            print(f"ucmItems are: \n {ucmItems}")

        pager = ""
        home = ""
        work = ""
        work_extension = ""
        other = ""
        mobile = ""
        lines = []
        contactRecord = []
        records = []
        ucmTitle = ['FIRST NAME', 'MIDDLE NAME', 'LAST NAME', 'USER ID', 'PASSWORD', 'DISPLAY NAME', 'MANAGER USER ID', 'DEPARTMENT', 'PIN', 'DEFAULT PROFILE', 'USER LOCALE', 'TELEPHONE NUMBER', 'MOBILE NUMBER', 'HOME NUMBER', 'PAGER NUMBER', 'TITLE', 'PRIMARY EXTENSION', 'ASSOCIATED PC', 'IPCC EXTENSION', 'MAIL ID', 'PRESENCE GROUP', 'SUBSCRIBE CALLING SEARCH SPACE', 'DIGEST CREDENTIALS', 'REMOTE DESTINATION LIMIT', 'MAXIMUM WAIT TIME FOR DESK PICKUP', 'ENABLE EMCC', 'DIRECTORY URI', 'ENABLE MOBILITY', 'ENABLE MOBILE VOICE ACCESS', 'ALLOW CONTROL OF DEVICE FROM CTI', 'NAME DIALING', 'MLPP USER IDENTIFICATION NUMBER', 'MLPP PASSWORD', 'MLPP PRECEDENCE AUTHORIZATION LEVEL', 'HOME CLUSTER', 'ENABLE USER FOR UNIFIED CM IM AND PRESENCE', 'UC SERVICE PROFILE', 'INCLUDE MEETING INFORMATION IN PRESENCE', 'SELF-SERVICE USER ID', 'USER PROFILE', 'ASSIGNED PRESENCE SERVER', 'ENABLE END USER TO HOST CONFERENCE NOW', 'MEETING NUMBER', 'ATTENDEES ACCESS CODE', 'EM MAX LOGIN TIME']
        lines.append(ucmTitle)
        deleteList = []
        for iterator in range (len(ucmItems)):
            index = "contact" + str(iterator+1)
            firstName = ucmItems[index]["firstName"]
            lastName = ucmItems[index]["lastName"]
            displayName = ucmItems[index]["displayName"]
            email = ucmItems[index]["email"]
            sipUri = ucmItems[index]["sipUri"]
            userId = ucmItems[index]["userId"]
            phoneTypes = ucmItems[index]["phones"].keys()
            if "work" in phoneTypes:
                phoneNo = ucmItems[index]["phones"]["work"]
            if "mobile" in phoneTypes:
                mobile = ucmItems[index]["phones"]["mobile"]
            if "home" in phoneTypes:
                home = ucmItems[index]["phones"]["home"]
            if primaryPhone != "other" and "other" in phoneTypes:
               pager = ucmItems[index]["phones"]["other"]
            if "work" not in phoneTypes:
                if primaryPhone in phoneTypes:
                   print(f"processing line {iterator}")
                   print(phoneTypes)
                   phoneNo = ucmItems[index]["phones"][primaryPhone]
            contactRecord = [firstName, lastName, userId, displayName,phoneNo, mobile, home, pager, email, sipUri]

            lines.append([firstName, "", lastName, userId, "", displayName,"", "", "", "", "", phoneNo, mobile, home, pager, "", "", "", "", email, "", "", "", "", "", "", sipUri, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""])
            records.append(contactRecord)
            deleteList.append(userId)

            pager = ""
            home = ""
            work = ""
            work_extension = ""
            other = ""
            mobile = ""
            phoneNo = ""
        print(lines)

        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        print(dt_string)
        filenameAdd = f"{fileName1stPart}_{dt_string}_addUsers.csv"
        filenameDelete = f"{fileName1stPart}_{dt_string}_deleteUsers.txt"
        with open(f"{path}/{filenameAdd}", "w+", encoding='utf-8-sig', newline ='') as csvFile:
            write = csv.writer(csvFile)
            write.writerows(lines)
        with open(f"{path}/{filenameDelete}", "w+") as deleteFile:
            for item in deleteList:
                deleteFile.write(item + '\n')
        return filenameAdd, filenameDelete, records
