import numpy as np
import requests
import json


def send_request(request):
    # response = requests.get()
    # response_json = json.loads(response.content)
    response_json = {
        "0": {'altitude': 100, 'datetime': 1543665867, 'latitude': 40.71, 'longitude': -74.0, 'passes': 5},
        "1": {'altitude': 100, 'datetime': 1543665867, 'latitude': 40.71, 'longitude': -75.0, 'passes': 5},
        "2": {'altitude': 100, 'datetime': 1543665867, 'latitude': 40.71, 'longitude': -76.0, 'passes': 5},

        "3": {'altitude': 110, 'datetime': 1543665867, 'latitude': 41.71, 'longitude': -74.0, 'passes': 5},
        "4": {'altitude': 110, 'datetime': 1543665867, 'latitude': 41.71, 'longitude': -75.0, 'passes': 5},
        "5": {'altitude': 110, 'datetime': 1543665867, 'latitude': 41.71, 'longitude': -76.0, 'passes': 5},

        "6": {'altitude': 120, 'datetime': 1543665867, 'latitude': 42.71, 'longitude': -74.0, 'passes': 5},
        "7": {'altitude': 120, 'datetime': 1543665867, 'latitude': 42.71, 'longitude': -75.0, 'passes': 5},
        "8": {'altitude': 120, 'datetime': 1543665867, 'latitude': 42.71, 'longitude': -76.0, 'passes': 5}
    }
    return response_json


def get_positions_dict(response_json):
    positions = {
        "latitude": [],
        "longitude": [],
        "altitude": []
    }

    for position in response_json.values():
        positions['latitude'].append(position['latitude'])
        positions['longitude'].append(position['longitude'])
        positions['altitude'].append(position['altitude'])
    return positions


def generate_map(positions):
    map_array = np.array((positions['latitude'],
                          positions['longitude'],
                          positions['altitude']
                          ))
    return map_array
