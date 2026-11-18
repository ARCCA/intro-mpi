from mpi4py import MPI
import numpy as np

amode = MPI.MODE_WRONLY|MPI.MODE_CREATE
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
filename="./datafile.noncontig.mpi"
fh = MPI.File.Open(comm, filename, amode)
size = comm.Get_size()

item_count = 10

buffer = np.empty(item_count, dtype='i')
buffer[:] = rank

filetype = MPI.INT.Create_vector(count=item_count, blocklength=1, stride=size)
filetype.Commit()
displacement = MPI.INT.Get_size() * rank
fh.Set_view(displacement, filetype=filetype)

fh.Write_all(buffer)
filetype.Free()
fh.Close()

# read file back just for confirmation
if rank == 0:
    data = np.fromfile(filename, dtype=np.intc)
    print(data)
