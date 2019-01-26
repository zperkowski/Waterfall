import numpy as np


def find_column(map, x, y):
    return np.where((map[0] == x) * (map[1] == y))[0]


def filter_only_water(map):
    ret = map[:, np.where(map[3] > 0)]
    ret = ret.reshape(ret.shape[0], ret.shape[2])
    return ret


def find_neighbouring_tiles(water_position, water_map):
    neighbouring_tiles = []
    neighbouring_tiles.append(find_column(water_map, water_position[0] - 1, water_position[1] - 1))
    neighbouring_tiles.append(find_column(water_map, water_position[0] - 1, water_position[1] + 1))
    neighbouring_tiles.append(find_column(water_map, water_position[0] + 1, water_position[1] - 1))
    neighbouring_tiles.append(find_column(water_map, water_position[0] + 1, water_position[1] + 1))
    return neighbouring_tiles


def pour_water(to_column, from_column, divider, water_map):
    amount = (water_map[3][from_column] - water_map[2][from_column]) / divider
    water_map[3][from_column] = water_map[3][from_column] - amount
    water_map[3][to_column] = water_map[3][to_column] + amount
    return water_map


def chunks(list_to_split, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(list_to_split), n):
        yield list_to_split[i:i + n]
