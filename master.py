#!/usr/bin/env python
import sys
import time

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
        list_water_maps.append(pour_water(tile, from_column, list_water_maps[-1])[0])

    # for i in range(10):
    NUM_OF_WORKERS = 3
    mpi_info = MPI.Info.Create()
    start_time = time.time()
    mpi_info.Set("add-hostfile", "hostfile")
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
    changed_tiles_each_worker = []
    changed_tiles_each_worker = comm.gather(changed_tiles_each_worker, root=MPI.ROOT)

    # Get first map and modify based on other workers modifications
    for w in range(0, NUM_OF_WORKERS):
        changed_tiles = changed_tiles_each_worker[w]
        for key in changed_tiles.keys():
            wl_water[0][-1][3][key] += changed_tiles[key]

    list_water_maps.append(wl_water[0][-1])
    elapsed_time = time.time() - start_time
    comm.Disconnect()

    print(time.strftime("%H:%M:%S:%MS", time.gmtime(elapsed_time)))

    return list_water_maps

