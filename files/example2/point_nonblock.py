#!/bin/env python3
# Example of non-blocking point-to-point MPI communication. Pairs of processes
# will send and receive data to and from each other in the form of
# pickled python dictionaries.

from mpi4py import MPI # Python MPI library

if __name__ == "__main__":

    # Initialise a communicator and get the rank of this process.
    try:
        comm = MPI.COMM_WORLD # Initiate communications
        rank = comm.Get_rank()
        size = comm.Get_size()
    except Exception as err:
        sys.exit("Error: %s" % err)

    # Create a python dictionary containing the rank and world size which we
    # will send via MPI point-to-point communication methods.
    send_data = {'rank': rank, 'world': size}

    # Even numbered processes send data to process rank + 1, whilst odd
    # numbered processes send data to process rank - 1.
    if rank % 2 == 0:
        # Determine rank of process to exchange data with and set communication
        # tags.
        exch_rank = (rank + 1)
        sendtag = rank
        recvtag = 100 + exch_rank
    else:
        exch_rank = (rank - 1)
        sendtag = 100 + rank
        recvtag = exch_rank

    # all processes send their data, no need to pair with requests
    sendreq = comm.isend(send_data, dest=exch_rank, tag=sendtag)

    # Further processing could occur here while the MPI libraries perform
    # the communication...

    # all processes request data
    recvreq = comm.irecv(source=exch_rank, tag=recvtag)

    # we can continue doing some more work
    # we don't have confirmation of having received the data yet...

    # Only at this point do we wait until communication has been verified
    # to be complete. Note, it's only at this point can we be sure that
    # the recv_data variable contains any data.
    sendreq.wait()
    recv_data = recvreq.wait()

    # Print out the data sent and received by this process.
    print ("Rank:",rank," sent:",send_data,"received:",recv_data)
