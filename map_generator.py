import numpy as np
import requests
import json


def load_api_key():
    with open("api_key") as api_key_file:
        line = api_key_file.readline()
    return "&key=" + line


def build_request_string(list_of_coordinates):
    return ''.join([str(lat) + """,""" + str(lng) + """|""" for lat, lng in list_of_coordinates])[:-1]


def load_request_from_file(path):
    with open(path) as file:
        response = json.load(file)
    return response


def build_list_of_coordinates(start_lat, start_lng, end_lat, end_lng, resolution):
    coordinates = []
    if start_lat < end_lat:
        resolution_lat = resolution
    else:
        resolution_lat = -resolution
    if start_lng < end_lng:
        resolution_lng = resolution
    else:
        resolution_lng = -resolution
    # Todo: Optimize
    for lat in np.arange(start_lat, end_lat, resolution_lat):
        for lng in np.arange(start_lng, end_lng, resolution_lng):
            coordinates.append((lat, lng))
    print("Created list of " + str(len(coordinates)) + " coordinates")
    return coordinates


def send_request(request):
    print("Sending request:\t" + request)
    response = requests.get(request)
    response_json = json.loads(response.content)
    return response_json


def get_osm_positions_dict(response_json):
    positions = {
        "latitude": [],
        "longitude": [],
        "elevation": []
    }

    for position in response_json['results']:
        positions['latitude'].append(position['latitude'])
        positions['longitude'].append(position['longitude'])
        positions['elevation'].append(position['elevation'])
    return positions


def get_google_positions_dict(response_json):
    positions = {
        "latitude": [],
        "longitude": [],
        "elevation": []
    }

    for position in response_json['results']:
        positions['latitude'].append(position['location']['lat'])
        positions['longitude'].append(position['location']['lng'])
        positions['elevation'].append(position['elevation'])
    return positions


def generate_map(positions):
    map_array = np.array((positions['latitude'],
                          positions['longitude'],
                          positions['elevation']
                          ))
    return map_array


def request_google_api():
    request = "https://maps.googleapis.com/maps/api/elevation/json?locations="

    coordinates = build_request_string(
        build_list_of_coordinates(54.75, 13.80, 48.65, 24.52, 0.5))
    request += coordinates

    # Key for Google API
    api_key = load_api_key()
    request += api_key
    response = send_request(request)
    return response


def request_osm_api():
    request = "https://api.open-elevation.com/api/v1/lookup?locations="

    coordinates = build_request_string(
        build_list_of_coordinates(54.75, 13.80, 48.65, 24.52, 0.5))
    request += coordinates

    # Key for Google API
    api_key = load_api_key()
    request += api_key
    response = send_request(request)
    return response
