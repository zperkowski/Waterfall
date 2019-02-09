import numpy as np
import visualizer
import map_generator
from master import start
from utils import find_column


def generate_initial_waterfall(x, y, amount, map):
    # Find initial water position
    list_of_water_states = []
    initial_state = map[:, :]
    position = find_column(initial_state, x, y)

    # Add new dimension for water level
    initial_state = np.vstack([initial_state, np.zeros(len(initial_state[0]))])
    initial_state[3, position] = amount

    list_of_water_states.append(initial_state)
    return list_of_water_states


if __name__ == '__main__':
    # mpirun -hostfile hostfile -np 1 python watefall.py
    # response = map_generator.request_osm_api()
    response = map_generator.load_request_from_file("samples/poland_s.json")
    print(str(response))
    positions = map_generator.get_osm_positions_dict(response)
    map_array = map_generator.generate_map(positions)

    l_water = generate_initial_waterfall(48.0, 18.0, 1000, map_array)

    l_water = start(l_water)

    visualizer.save_animation(map_array, l_water, 'animation.mp4')
