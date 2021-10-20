import requests
import pandas as pd
import json
import geopy.distance
import numpy as np
from time import sleep
import re
from requests_html import HTMLSession
import validators

def get_details(api_key, location, keyword, fields_list):

    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="+location+"&inputtype=textquery&locationbias=circle%3A2000%4047.6918452%2C-122.2226413&fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&key="+api_key
    #GET LOCATION DETAILS
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    loc_details = dict(json.loads(response.text))
    #-------------------------------------------------------------------------

    #GET COORDINATES AND RADIUS OF LOCATION
    coord = (loc_details['candidates'][0]['geometry']['location']['lat'],loc_details['candidates'][0]['geometry']['location']['lng'])
    ne = (loc_details['candidates'][0]['geometry']['viewport']['northeast']['lat'],loc_details['candidates'][0]['geometry']['viewport']['northeast']['lng'])
    sw = (loc_details['candidates'][0]['geometry']['viewport']['southwest']['lat'],loc_details['candidates'][0]['geometry']['viewport']['southwest']['lng'])
    radius = str(geopy.distance.distance(ne,sw).km/2*1000)
    # In[29]:


    #SEARCH FOR KEYWORD IN THE RADIUS
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+keyword+"&location="+str(coord[0])+"%2C"+str(coord[1])+"&radius="+radius+"&type=establishment&key="+api_key
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    results = list(json.loads(response.text)['results'])
    df = pd.DataFrame(results)

    #GET THE NEXT 2 PAGES OF RESULTS
    for i in range(2):
        try:
            sleep(2)
            d = dict(json.loads(response.text))
            page_token = d['next_page_token']
            headers = {}
            payload = {}
            url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken='+page_token+'&key='+api_key
            response = requests.request("GET", url, headers=headers, data=payload)
            results = list(json.loads(response.text)['results'])
            df = df.append(results,ignore_index=True)
            print('success')
        except:
            print('Less than 60 exist')

    #
    results = []
    email_flag = 0
    if 'email' in fields_list:
        fields_list.remove('email')
        email_flag = 1
        if 'website' not in fields_list:
            fields_list.append('website')
    fields_list.insert(0,'name')
    fields = '%2C'.join(fields_list)
    for place_id in df.place_id:
        try:
            payload = {}
            headers = {}
            url = "https://maps.googleapis.com/maps/api/place/details/json?place_id="+place_id+"&fields="+fields+"&key="+api_key
            response = requests.request("GET", url, headers=headers, data=payload)
            results.append(json.loads(response.text)['result'])
        except:
            pass


    df = pd.DataFrame(results)
    df['S.No'] = np.arange(len(df))+1
    first_column = df.pop('S.No')
    df.insert(0,'S.No',first_column)
    second_column = df.pop('name')
    df.insert(1, 'name', second_column)
    if 'opening_hours' in df.columns:
        df['opening_hours'] = [x['open_now'] if type(x) == dict else "-" for x in df['opening_hours']]

    EMAIL_REGEX = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\(.com|.in)"
    if email_flag:
        session = HTMLSession()
        emails = []
        for url in df.website:
            try:
                r = session.get(url)
                email = ''
                for re_match in re.finditer(EMAIL_REGEX, r.html.raw_html.decode()):
                    if re_match.group() not in email:
                        email = email + re_match.group() + "\n"
                emails.append(email)
            except:
                emails.append(' ')
        print(len(emails))
        df['email'] = emails
    df = df.rename(columns={'name':'Name','formatted_phone_number':'Phone Number','formatted_address':'Address','opening_hours':'Open Now','rating':'Rating','price_level':'Price Level','website':'Website','email':'Email'})
    return df




