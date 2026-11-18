#!/bin/env python3
# Scatter data across multiple processes. The data consists of a
# two-dimensional numpy array, which each process receiving a row.

from mpi4py import MPI # Python MPI library
import numpy as np     # To create a data array to be communicated to all processes

if __name__ == "__main__":

    # Initialise a communicator and get the rank of this process.
    try:
        comm = MPI.COMM_WORLD # Initiate communications
        rank = comm.Get_rank()
        size = comm.Get_size()
    except Exception as err:
        sys.exit("Error: %s" % err)

    # This variable defines the length of each row in the array. In a
    # real world case this would depend on the amount of data.
    allocsize = 4

    # The root process initially holds the data array. It is populated with
    # integers and shaped to match the number of processes. Note, this is
    # for convenience - in reality allocating your data amongst processes
    # can be a major challenge.
    if rank == 0:
        senddata = np.arange(
            size * allocsize, dtype='i').reshape(size, allocsize)
    else:
        senddata = None

    # Each process has an initially empty array set up to receive its share
    # of the data.
    recvdata = np.empty(allocsize, dtype='i')

    # Confirm data hold by each proces
    if rank == 0:
        print("data before scattering")

    comm.Barrier()

    print("rank = ", rank, "senddata = ", senddata, "recvdata", recvdata)

    comm.Barrier()

    # Break up the two-dimensional array amongst processes.
    comm.Scatter(senddata, recvdata, root=0)

    comm.Barrier()

    # Each process prints out the data it has received.
    if rank == 0:
        print("=====================")
        print("data after scattering")

    print ("rank = ", rank, "recvdata = ", recvdata)
