#!/bin/env python3
from mpi4py import MPI
import numpy as np

amode = MPI.MODE_WRONLY|MPI.MODE_CREATE
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
filename="./datafile.collective.mpi"
fh = MPI.File.Open(comm, filename, amode)

item_count = 10

buffer = np.empty(item_count, dtype='i')
buffer[:] = rank

print(f"{rank} : {buffer}")

offset = comm.Get_rank() * buffer.nbytes
fh.Write_at_all(offset, buffer)
fh.Close()

# read file back just for confirmation
if rank == 0:
    data = np.fromfile(filename, dtype=np.intc)
    print(data)
