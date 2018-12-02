import visualizer
import map_generator

if __name__ == '__main__':
    request = ""
    response = map_generator.send_request(request)
    positions = map_generator.get_positions_dict(response)
    map_array = map_generator.generate_map(positions)
    visualizer.save_animation(map_array, 'animation.mp4')
