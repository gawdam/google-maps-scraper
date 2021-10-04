import requests
import pandas as pd
import json
import numpy as np
from time import sleep

def APIcheck(api_key):
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=" + "Delhi" + "&inputtype=textquery&locationbias=circle%3A2000%4047.6918452%2C-122.2226413&fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&key=" + api_key

    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    message = json.loads(response.text)
    if 'error_message' in message.keys():
        return False
    return True