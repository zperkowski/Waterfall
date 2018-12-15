#!/usr/bin/env python
import numpy as np
from mpi4py import MPI

comm = MPI.Comm.Get_parent()
size = comm.Get_size()
rank = comm.Get_rank()

N = np.array(0)
print("Worker " + str(rank) + "\tWaiting for broadcast variable N: " + str(N))
comm.Bcast([N, MPI.INT], root=0)
print("Worker " + str(rank) + "\tGot broadcast variable N: " + str(N))
comm.Disconnect()
