'''
A basic script for interacting with the Ruckus SCG 200 and getting some info on
an access point by AP name.

This is a bit tricky as at the time this was written, it wasn't possible to
do this by AP name using the API.
The work around implemented here first gets a list of MAC addresses for APs in
the desired zone, then performs another lookup by MAC address and compares
the AP name value against the one we're interested in for a match.

While, this feature is avaialble through the web portal, the interface really
sucks when you have more than 200 items in there. 
'''

import requests
import json
import getpass

session = requests.Session()

# Base URL to post requests to
base_url = "https://wlc.ruckuscontroller.com/endpoint"

#For some reason with v1.0 this field can be problematic, so pop it!
session.headers.pop('Accept-Encoding')

#Various endpoints that will be used:

#Authentication endpoint
access = "/v1_0/session"

#We'll grab a list of MAC addresses in the interesting zone from here
ap_list = "/v1_0/aps"

#This endpoint will give us more info on the AP from the provided MAC address.
wap_info = "/v1_0/aps/"

#Things we'll need to grab the initial list of APs.
ap_list_params = {'index': 0, 'listSize': 400, 'zoneId': 'some-uuid-for-desired-zone'}

#Getting the creds, and using Python 3.0's getpass function.
#The beautiful thing about the getpass function is that it doesn't echo your
#password to the terminal!
#Saves a lot of work on writing a function to do that for you!

username = input("Username: ")
password = getpass.getpass("Password: ")

credentials = {"username":username, "password":password}

#Authenticating:
s = session.post(base_url+access, json=credentials)

#Grabbing a list of APs fromt the specified zone.
s = session.get(base_url+ap_list, params=ap_list_params)
ap_list = json.loads(s.text)


#The bulk of the work:
for wap in ap_list['list']:
    s = session.get(base_url+wap_info+wap['mac'])
    wap_Jinfo = json.loads(s.text)
    if wap['name'] == "122171":
        print(wap['name'],",",wap['mac'], ",",wap_Jinfo['description'],",",wap_Jinfo['latitude'],",",wap_Jinfo['longitude'])

#Close the session.
s = session.delete(base_url+access)
