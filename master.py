#!/usr/bin/env python
import sys

import numpy as np
from mpi4py import MPI

comm = MPI.COMM_SELF.Spawn(sys.executable,
                           args=['worker.py'],
                           maxprocs=4)
rank = comm.Get_rank()
print("Master " + str(rank) + "\tSending broadcast map")
N = np.array(100)
comm.Bcast([N, MPI.INT], root=MPI.ROOT)
comm.Disconnect()
