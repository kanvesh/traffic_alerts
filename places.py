import requests
import json


stored_places = json.load(open('places_with_latlong.json','r'))

url = "https://api.olamaps.io/places/v1/geocode"


def latlong2string(latlong):
    return str(latlong['lat'])+","+str(latlong['lng'])


def getlatlong(address, api_key):
    if address in stored_places:
        latlong = stored_places[address]['location']
        return latlong2string(latlong)
    else:
        params = {
            "address": address,
            "api_key": api_key
            }
        response = requests.get(url, params=params)
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            #print(data)
            latlong = data['geocodingResults'][0]['geometry']['location']
            return latlong2string(latlong)
        else:
            print(f"Request failed with status code {response.status_code}")
    return None

