import requests
import json


def load_key(key_file):
    with open(key_file) as f:
        api_key = "".join(f.readlines())
    return api_key

url = "https://developer.woot.com"
payload = {"x-api-key" : "API key goes here"}

r = requests.get(url+"/feed/home", headers={"x-api-key": load_key("./api_key")})

json_object = r.json()

for item in json_object['Items']:
    if "HOME/Bedding" in item['Categories'] and item['IsSoldOut'] == False:
        print(item)