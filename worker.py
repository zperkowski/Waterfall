#!/usr/bin/env python
import numpy as np
from mpi4py import MPI

from utils import filter_only_water, chunks, find_neighbouring_tiles, find_column, pour_water

comm = MPI.Comm.Get_parent()
size = comm.Get_size()
rank = comm.Get_rank()
print("Worker: " + str(rank))

# Get information how many workers are spawned
N = np.array(0)
comm.Bcast([N, MPI.INT], root=0)

# Each worker gets whole map
water_map = np.zeros(1)
water_map = comm.bcast(water_map, root=0)

# Find places where water is and split work between workers
filtered_water_map = filter_only_water(water_map)
split_filtered_water_map = chunks(filtered_water_map, N)
filtered_water_map = split_filtered_water_map[rank]

l_water = [water_map]

# Pour water on neighbouring tiles
for i in range(len(filtered_water_map[0])):
    water_position = filtered_water_map[:, i]
    neighbouring_tiles = find_neighbouring_tiles(water_position, water_map)
    from_column = find_column(l_water[-1], water_position[0], water_position[1])
    for tile in neighbouring_tiles:
        water_map = pour_water(tile, from_column, water_map)
        l_water.append(water_map)

# Workers send modified map back to master
comm.gather(l_water, root=0)

comm.Disconnect()
