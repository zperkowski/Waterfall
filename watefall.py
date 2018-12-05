import visualizer
import map_generator

if __name__ == '__main__':
    request = "https://maps.googleapis.com/maps/api/elevation/json?locations="
    coordinates = map_generator.build_request_string(
        map_generator.build_list_of_coordinates(54.751923, 13.802965, 48.652599, 24.520693, 1))
    request += coordinates
    api_key = map_generator.load_api_key()
    request += api_key
    response = map_generator.send_request(request)
    positions = map_generator.get_positions_dict(response)
    map_array = map_generator.generate_map(positions)
    visualizer.save_animation(map_array, 'animation.mp4')
