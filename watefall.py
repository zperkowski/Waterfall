import visualizer
import map_generator

if __name__ == '__main__':
    # URL to use google
    # request = "https://maps.googleapis.com/maps/api/elevation/json?locations="
    # URL to use OSM
    request = "https://api.open-elevation.com/api/v1/lookup?locations="
    coordinates = map_generator.build_request_string(
        map_generator.build_list_of_coordinates(54.75, 13.80, 48.65, 24.52, 0.5))
    request += coordinates
    # Key for Google API
    # api_key = map_generator.load_api_key()
    # request += api_key
    response = map_generator.send_request(request)
    print(str(response))
    positions = map_generator.get_osm_positions_dict(response)
    map_array = map_generator.generate_map(positions)
    visualizer.save_animation(map_array, 'animation.mp4')
