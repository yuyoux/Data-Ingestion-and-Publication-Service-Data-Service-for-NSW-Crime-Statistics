import requests
from authentication import AUTH_TOKEN
"""
    This script is for deleting testing
    json text is shown with the specific information
"""
#First, you need to input username and password to get athentication
#If not passed, you are a guest. Further query will get error information
#If passed, you can input the name of the area you want to delete:
#e.g:
#Name: SYDNEY, Bluemountains, leeton
#You may get '200 OK' or '404 NOT FOUND' with json information for responses

try:
    # Both lower and upper letter supported
    name1 = str(input("Please input the area you want to delete (name):"))
except ValueError:
    print("Goodbye!")

name = name1.lower().replace(' ','')
URL = 'http://localhost:5000/areas/' + name
result = requests.delete(URL,headers={"Content-Type": "application/json",\
                                      "AUTH_TOKEN":AUTH_TOKEN})
if not result.ok:
    print(result.text)
    print("Status Code", result.status_code)
    quit()
else:
    print(result.text)
    print("Status Code", result.status_code)