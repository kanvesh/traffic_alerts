import requests
from places import getlatlong
from math import ceil

# Define the endpoint and parameters

def getDuration(origin, destination, api_key, api_service='Ola'):
    origin_latlong = getlatlong(origin, api_key)
    destination_latlong = getlatlong(destination, api_key)

    if api_service=='Ola':
        url = "https://api.olamaps.io/routing/v1/directions"

    params = {
        "origin": origin_latlong,
        "destination": destination_latlong,
        "api_key": api_key
    }
    # Make the POST request
    response = requests.post(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        result={}
        result['status'] = data['status']
        result['origin'] = origin
        result['destination'] =destination
        result['origin_latlong']=data['routes'][0]['legs'][0]['start_address']
        result['destination_latlong'] =data['routes'][0]['legs'][0]['end_address'] 
        result['distance'] = data['routes'][0]['legs'][0]['distance'] 
        result['time_taken_secs'] = data['routes'][0]['legs'][0]['duration']
        result['source'] = data['source_from']
        result['api_url'] = url
        return result
    else:
        print(f"Request failed with status code {response.status_code}")
        return None
