#!/bin/env python3
from mpi4py import MPI
import numpy as np

amode = MPI.MODE_WRONLY|MPI.MODE_CREATE
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
fh = MPI.File.Open(comm, "./datafile.independent.mpi", amode)

buffer = np.empty(10, dtype=np.int)
buffer[:] = rank

print(f"{rank} : {buffer}")

offset = comm.Get_rank() * buffer.nbytes
if rank == 0:
    fh.Write_at(offset, buffer)

fh.Close()
