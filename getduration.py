import requests
from places import getlatlong
import googlemaps
import json

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


def getDurationGMaps(origin, destination,api_key="AIzaSyDU10bwXHIREeYwTyNmt_vrsMHxD3iS7-I"):
    gmaps = googlemaps.Client(key=api_key)
    origin_latlong = getlatlong(origin, api_key)
    destination_latlong = getlatlong(destination, api_key)
    print(origin_latlong)
    try:
        # Request directions
        # 'mode' can be 'driving', 'walking', 'bicycling', 'transit'
        # 'departure_time' can be set to 'now' for real-time traffic
        directions_result = gmaps.directions(origin_latlong,
                                             destination_latlong,
                                             mode="driving",
                                             departure_time="now")
        if directions_result and len(directions_result) > 0:
            # Typically, the first leg of the first route is what we want
            leg = directions_result[0]['legs'][0]
            result={}
            result['distance'] = leg['distance']['value']  # Distance in meters
            result['time_taken_secs'] = leg['duration']['value']  # Duration in seconds
            return result
        else:
            print("Error: No directions found for the given points.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def getDurationGMaps_live(origin, destination,api_key="AIzaSyDU10bwXHIREeYwTyNmt_vrsMHxD3iS7-I"):
    print(api_key)
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    origin_latlong = getlatlong(origin, api_key)
    destination_latlong = getlatlong(destination, api_key)
    # Request headers
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        # Field mask specifies which fields to return in the response
        "X-Goog-FieldMask": "routes.duration,routes.staticDuration,routes.distanceMeters",
    }
    # Request body
    payload = {
        "origin": {"location": {"latLng": {"latitude": origin_latlong.split(',')[0], "longitude": origin_latlong.split(',')[1]}}},
        "destination": {"location": {"latLng": {"latitude": destination_latlong.split(',')[0], "longitude": destination_latlong.split(',')[1]}}},
        "travelMode": "DRIVE",
        # This is the key parameter for real-time traffic
        "routingPreference": "TRAFFIC_AWARE_OPTIMAL",
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        route_data = response.json()
        # Check if the API returned a valid route
        if "routes" in route_data and len(route_data["routes"]) > 0:
            route = route_data["routes"][0]
            distance_meters = route["distanceMeters"]
            # Duration in seconds, including traffic. Comes as '313s'.
            duration_with_traffic_str = route["duration"]
            duration_seconds = int(duration_with_traffic_str.replace("s", ""))
            if duration_seconds == 0:
                return None # Avoid division by zero
            result={}
            result['status'] = 'Success'
            result['origin'] = origin
            result['destination'] =destination
            result['origin_latlong']=origin_latlong
            result['destination_latlong'] =destination_latlong
            result['distance'] = distance_meters  # Distance in meters
            result['time_taken_secs'] = duration_seconds  # Duration in seconds
            result['source'] = 'Google Maps API'
            result['api_url'] = url
            print(result)
            return result
        else:
            print(f"API Error: No route found. Response: {route_data}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network request failed: {e}")
        return None
    except (KeyError, IndexError):
        print(f"Could not parse API response: {response.text}")
        return None

getDurationGMaps_live('Siddapura Junction','Marathahalli Bridge')

