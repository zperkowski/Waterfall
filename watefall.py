import visualizer
import map_generator

if __name__ == '__main__':
    request = "https://maps.googleapis.com/maps/api/elevation/json?locations=39.7391536,-104.9847034&key=AIzaSyA-wBCunmhKpOK28OT-VC4X9Wd0UflrlZo"
    response = map_generator.send_request(request)
    positions = map_generator.get_positions_dict(response)
    map_array = map_generator.generate_map(positions)
    visualizer.save_animation(map_array, 'animation.mp4')
