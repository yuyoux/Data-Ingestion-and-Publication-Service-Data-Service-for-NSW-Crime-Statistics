import requests
"""
    This script is for get-all-available collections testing.
    ATOM-based text is shown with existing entries.
"""
#Just run this script, you will get all existed entries with '200 OK'
#ATOM-based information is shown in response as well

response = requests.get("http://localhost:5000/areas", params=None)
print("Areas Information:\n", response.text)
print("Status Code",response.status_code)