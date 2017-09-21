'''
This extends upon ap-info.py somewhat and adds a delete function.
The input source is a specified file with a list of APs that we'd like to
remove from the SCG controller.

With Python, checking if an item is in a list is pretty easy, so the overall
logic is along the lines of grab all the MAC addresses in the interesting zone.
Then, for each, check the AP name and compare it against the list of APs, we'd like
to delete.
If it's on the list, proceed with deletion, if not , then get the AP name from the next
MAC address on the list.

This would be much simpler if were are able to query by AP name using the API....

To do:
Needs some serious validation for :
    -File name (list of APs)
    -AP name, as per specified naming convention
    -Existing record in SCG or if there are no records found

Maybe no prompt prior to each individual deletion.
    -Instead display the list and verify that it's OK to proceed with each one.
'''


import requests
import json
import getpass
import os


session = requests.Session()
base_url = "https://wlc.ruckuscontroller.com/endpoint"
session.headers.pop('Accept-Encoding')
access = "/v1_0/session"
ap_list = "/v1_0/aps"
wap_info = "/v1_0/aps/"
wap_operational = "/v1_0/aps/"
ap_list_params = {'index': 0, 'listSize': 400, 'zoneId': 'some-uuid-for-desired-zone'}

username = input("Enter Username: ")
password = getpass.getpass("Enter Password: ")

credentials = {"username":username, "password":password}

s = session.post(base_url+access, json=credentials)

s = session.get(base_url+ap_list, params=ap_list_params)


ap_list = json.loads(s.text)

destroy = []
wap_file = input("file name:")
with open(wap_file) as f:
    for line in f:
        destroy.append(str(line).strip())
print(destroy)
print(len(destroy))

for wap in ap_list['list']:
    s = session.get(base_url+wap_info+wap['mac'])
    wap_Jinfo = json.loads(s.text)
    #print(wap_Jinfo)
    if wap['name'] in destroy:
        print("Are you sure you want to delete: ")
        print(wap['name'],",",wap['mac'], ",",wap_Jinfo['description'],",",wap_Jinfo['latitude'],",",wap_Jinfo['longitude'])
        decision = input("y/n: ")
        if decision == "y":
            s = session.delete(base_url+wap_info+wap['mac'])
            if s.status_code == 204:
                print(wap['name'], " successfuly deleted.")
            else:
                print(wap['name'], " was not successfuly deleted.")
        else:
            print(wap['name'], " was not deleted.")

s = session.delete(base_url+access)
