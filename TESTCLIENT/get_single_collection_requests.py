import requests
"""
    This script is for get-single-collection testing
    ATOM-based text is shown with the specific collection
"""
#Input the name you want to search
#e.g:
#Name: SYDNEY, Bluemountains, leeton
#You may get '200 OK' with ATOM information for responses if founded
#or '404 NOT FOUND' if the entry does not existed

try:
    # Both lower and upper letter supported
    name = str(input("Please input the area you want to serach (name):"))
except ValueError:
    print("Goodbye!")

URL = 'http://localhost:5000/areas/' + name
response = requests.get(URL, params=None)
print("Areas Information:\n", response.text)
print("Status Code",response.status_code)