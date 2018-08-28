import requests
"""
    This script is for filtering testing
    ATOM-based text is shown with the specific collection
"""
#For this test, please follow the rule shown blew, which is strictly stick to the assignment specification
#e.g:

#Type1: http://127.0.0.1:5000/areas/filter?lgaName eq Sydney or lgaName eq Bluemountains
#Type 2: http://127.0.0.1:5000/areas/filter?lgaName eq sydney and year eq 2014

#Note: you should copy or input <THE WHOLE URL> as the input
#If entries founded, you may get '200 OK'
#If entries not founded or you input the wrong year(which should be 2012-2016),
# you may get '404 NOT FOUND' or '400 BAD REQUEST'
#ATOM-based information is shown in response is successfully founded

try:
    URL = input("Please input URL query you want to access(please follow the rule):")
except ValueError:
    print("Goodbye!")

URL2 = URL.replace(' ','+')
response = requests.get(URL2, params=None)
print("Areas Information:\n", response.text)
print("Status Code",response.status_code)