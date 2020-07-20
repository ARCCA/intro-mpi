---
title: "MPI point to point communication"
teaching: 0
exercises: 0
questions:
- "How do I send a message?"
objectives:
- "Understand how to send a message"
keypoints:
- "Sending messages to another processor is like sending a letter."
---

## Reminder

> ## `MPI_init` and `MPI_init_thread`
> - Initialises MPI environment inside code.
> - Strictly speaking code before this is called has undefined behaviour.
> - Function automatically called by `mpi4py` library.
> - Capture the error messages from this function.
{: .solution}
> ## `MPI_COMM_WORLD`
> - MPI communicator representing a method to talk to all processors.
> - The `mpi4py` library represents this in a class instance.
> - Having different communicators is quite advanced.
> - This is most common communicator to use.
{: .solution}
> ## `MPI_comm_size`
> - Function that returns the size of the communicator.
> - The `mpi4py` library represents this in a class method **Get_size()**
> - Stops having to read number of processors from elsewhere.
> - For `MPI_COMM_WORLD` it should return the number of processors.
> - Allows for dynamic allocation of resources without recompiling or relying on hard-coded arrays.
{: .solution}
> ## `MPI_comm_rank`
> - An identifier within the communicator between `0` and `MPI_comm_size-1`
> - The `mpi4py` library represents this in a class method **Get_rank()**
> - Can be confusing in Fortran as arrays are usually indexed from 1.
> - Used as part of the address when communicating messages.
{: .solution}
> ## `MPI_finalize`
> - Tells the MPI layer we have finished.
> - Any MPI calls after this will be an error.
> - Does not stop the program.
> - Usually called near (or at) the end.
> - The `mpi4py` library calls this automatically when exiting.
> - Alternatively `MPI_abort` can be used
>   - Aborts task in communicator
>   - One processor may cause the abort.
>   - Should only be used for unrecoverable error.
{: .solution}

{% include links.md %}

