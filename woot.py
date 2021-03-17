import requests
import json


#TODO: Return results only matching search criteria i.e. mattress
#TODO: Email those results to user
#TODO: Args?


def load_key(key_file):
    with open(key_file) as f:
        api_key = "".join(f.readlines())
    return api_key


url = "https://developer.woot.com"
feed_name = "/feed/home"

r = requests.get(url+feed_name, headers={"x-api-key": load_key("./api_key")})
json_object = r.json()

for item in json_object['Items']:
    if "HOME/Bedding" in item['Categories'] and item['IsSoldOut'] == False:
        print(item)