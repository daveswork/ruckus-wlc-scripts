Here are a few sample scripts I hacked together while tinkering with the
Ruckus SCG 200 API.


Full documentation for the API itself is here:


http://docs.ruckuswireless.com/scg-200/scg-public-api-reference-guide-3-0.html


While most tasks can be done through the portal, past 200 or so APs, it becomes painful
to look at, and the page refreshes get annoying.


- ap-info.py : This gets us some information on an AP by AP name

- delete-ap.py : Extends upon lessons learned from ap-info.py and adds a delete function. 
