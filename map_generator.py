import numpy as np
import requests
import json


def send_request(request):
    response = requests.get(request)
    response_json = json.loads(response.content)
    print(response_json)
    return response_json


def get_positions_dict(response_json):
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
