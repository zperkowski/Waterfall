import visualizer
import map_generator
import subprocess

if __name__ == '__main__':
    # response = map_generator.request_osm_api()
    response = map_generator.load_request_from_file("samples/poland.json")
    print(str(response))
    positions = map_generator.get_osm_positions_dict(response)
    map_array = map_generator.generate_map(positions)
    visualizer.save_animation(map_array, 'animation.mp4')
