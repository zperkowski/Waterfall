#!/usr/bin/env python
import sys

import numpy as np
from mpi4py import MPI

from utils import filter_only_water, find_column, pour_water, find_neighbouring_tiles, chunks


# Splits work between workers and joins results to visualize them
def start(list_water_maps):
    lf_water = filter_only_water(list_water_maps[0])
    water_position = lf_water[:, 0]
    neighbouring_tiles = find_neighbouring_tiles(water_position, list_water_maps[-1])
    for tile in neighbouring_tiles:
        from_column = find_column(list_water_maps[-1], water_position[0], water_position[1])
        list_water_maps.append(pour_water(tile, from_column, list_water_maps[-1]))

    # for i in range(10):
    NUM_OF_WORKERS = 1
    comm = MPI.COMM_SELF.Spawn(sys.executable,
                               args=['worker.py'],
                               maxprocs=NUM_OF_WORKERS)
    rank = comm.Get_rank()
    size = comm.Get_size()
    print("Master " + str(rank) + "\tSending broadcast map")
    N = np.array(NUM_OF_WORKERS)
    comm.Bcast([N, MPI.INT], root=MPI.ROOT)

    water_map = list_water_maps[-1]

    comm.bcast(water_map, root=MPI.ROOT)
    wl_water = []
    wl_water = comm.gather(wl_water, root=MPI.ROOT)
    for l_water in wl_water:
        for water in l_water:
            list_water_maps.append(water)

    comm.Disconnect()

    return list_water_maps


def worker(water_map):
    # Find places where water is and split work between workers
    filtered_water_map = filter_only_water(water_map)
    split_filtered_water_map = chunks(filtered_water_map, 1)
    filtered_water_map = split_filtered_water_map[0]

    l_water = [water_map]

    # Pour water on neighbouring tiles
    for i in range(len(filtered_water_map[0])):
        water_position = filtered_water_map[:, i]
        neighbouring_tiles = find_neighbouring_tiles(water_position, water_map)
        from_column = find_column(l_water[-1], water_position[0], water_position[1])
        for tile in neighbouring_tiles:
            water_map = pour_water(tile, from_column, water_map)
            l_water.append(water_map)
    return l_water
