#!/usr/bin/env python
import sys

import numpy as np
from mpi4py import MPI

from utils import filter_only_water, find_column, pour_water, find_neighbouring_tiles


# Splits work between workers and joins results to visualize them
def start(list_water_maps):
    lf_water = filter_only_water(list_water_maps[0])
    water_position = lf_water[:, 0]
    neighbouring_tiles = find_neighbouring_tiles(water_position, list_water_maps[-1])
    for tile in neighbouring_tiles:
        from_column = find_column(list_water_maps[-1], water_position[0], water_position[1])
        list_water_maps.append(pour_water(tile, from_column, len(neighbouring_tiles), list_water_maps[-1]))

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

    water_map = filter_only_water(list_water_maps[-1])

    comm.bcast(water_map, root=MPI.ROOT)
    new_map = comm.gather(water_map, root=MPI.ROOT)
    print('master:', new_map)
    list_water_maps.append(new_map)

    comm.Disconnect()

    return list_water_maps
