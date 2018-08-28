import requests
from authentication import AUTH_TOKEN
"""
    This script is for posting testing
    ATOM-based text is shown with the status information
"""
#First, you need to input username and password to get athentication
#If not passed, you are a guest. Further query will get error information
#If passed, you can input the name/postcode of the area you want to post:
#e.g:
#Name: SYDNEY, Bluemountains, leeton
#Postcode:2000: single entry posting; 2745: 5 entries posting
#For name post, if the entry already existed, you will get a '200 OK' with the link of it
#For postcode post, if one or more of entries already existed, only the unposted area
#will be posted with '201 created' and the link of new-post entry. The entry already
#existed will not be shown in the response(their link as well).
#If the name/postcode you input is wrong, you may get '404 NOT FOUND'
#ATOM-based information is shown in some response.

try:
    # Both lower and upper letter supported
    # Both name(str) and postcode(int) supported
    addr = input("Please input the area you want to serach (name or postcode):")
except ValueError:
    print("Goodbye!")

if addr.isdigit(): #if the input is digits, it must be postcode
    postcode = addr
    URL = 'http://localhost:5000/areas'
    result = requests.post(URL, params = {'postcode':postcode}, \
                           headers = {"AUTH_TOKEN":AUTH_TOKEN})
else: #if the input is a str, it must be name
    name = addr
    URL = 'http://localhost:5000/areas'
    result = requests.post(URL, params = {'name':name}, \
                           headers = {"AUTH_TOKEN":AUTH_TOKEN})

if not result.ok:
    print(result.text)
    print("status code", result.status_code)
    quit()
else:
    print(result.text)
    print("status code", result.status_code)

