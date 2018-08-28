import requests
"""
    This script is for token-accessing
"""
#modify the username and password to get token
#only admin can get the token, others are all labeled as guests
#username: admin password:admin --> admin (access to GET,POST,DELETE)
#other inputs -->guests (access to GET)

global AUTH_TOKEN

#Interactive version
username=str(input("For authentication, input your username frist:"))
password=str(input("Input your password then:"))

#An un-interactive version - default as admin
#username = 'admin' #You can change this part, if you want to be a guest
#password = 'admin' #You can change this part, if you want to be a guest

URL = 'http://localhost:5000/auth'
response = requests.get(URL, params={'username':username,'password':password})
if response.ok:
    AUTH_TOKEN = response.text
else:
    AUTH_TOKEN = ''
    print("Authentication failed, You're a guest.")