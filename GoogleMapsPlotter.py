import requests
import json
import geopy.distance
import plotly.graph_objects as go
import math
import numpy as np


def plot_location(api_key, location):
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=' + location + "&inputtype=textquery&locationbias=circle%3A2000%4047.6918452%2C-122.2226413&fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&key=" + api_key
    # GET LOCATION DETAILS
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    loc_details = dict(json.loads(response.text))
    # -------------------------------------------------------------------------

    # GET COORDINATES AND RADIUS OF LOCATION
    coord = (loc_details['candidates'][0]['geometry']['location']['lat'],
             loc_details['candidates'][0]['geometry']['location']['lng'])
    ne = (float(loc_details['candidates'][0]['geometry']['viewport']['northeast']['lat']),
          float(loc_details['candidates'][0]['geometry']['viewport']['northeast']['lng']))
    sw = (float(loc_details['candidates'][0]['geometry']['viewport']['southwest']['lat']),
          float(loc_details['candidates'][0]['geometry']['viewport']['southwest']['lng']))
    radius = float(math.sqrt((ne[0]-sw[0])**2+(ne[1]-sw[1])**2))/2
    num_points = 100
    theta = np.arange(0, 2*math.pi, math.pi / num_points)
    x_coord = [float(coord[0]) + radius * math.cos(x) for x in theta]
    y_coord = [float(coord[1]) + radius * math.sin(x) for x in theta]


    fig = go.Figure(go.Scattermapbox(
        fill="toself",
        lon=y_coord, lat=x_coord,
        marker={'size': 5, 'color': "orange"}))
    fig.update_layout(
        autosize=True,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox={
            'style': "stamen-terrain",
            'center': {'lon': float(coord[1]), 'lat': float(coord[0])},
            'zoom': 10},
        showlegend=False)

    return fig

