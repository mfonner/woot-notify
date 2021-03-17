import requests
import json


url = "https://developer.woot.com"
payload = {"x-api-key" : "API key goes here"}

r = requests.get(url+"/feed/home", headers={"x-api-key":"API key goes here"})

json_object = r.json()

for item in json_object['Items']:
    if "HOME/Bedding" in item['Categories'] and item['IsSoldOut'] == False:
        print(item)