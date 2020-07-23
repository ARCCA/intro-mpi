---
title: "Advanced topics in MPI"
teaching: 30
exercises: 15
questions:
- "What is the best way to read and write data to disk?"
- "Can MPI optimise commnications by itself?"
- "How can I use OpenMP and MPI together?"
objectives:
- "Use the appropriate reading and writing methods for your data."
- "Understand the topology of the problem affects communications."
- "Understand the use of hybrid coding and how it interacts."
keypoints:
- "MPI can deliver efficient disk I/O if designed"
- "Providing MPI with some knowledge of topology can make MPI do all the hard work."
- "The different ways threads can work with MPI dictates how you can use MPI and OpenMP together."
---

Having coverred simple point to point communication and collective communications, this section covers topics that are
not required but useful to know exist.

## MPI-IO

When reading and writing data to disk from a program using MPI, there are a number of approaches:

- gather/scatter all data to/from leader (MPI task 0) and write/read to disk from this one task.  Performance can be
  slow to communicate and perform a large amount of I/O from one task.
- read and write directly to disk from each MPI task but to separate files.  Not good for portability due to dependent
  on processor decomposition.
- use included MPI-IO that takes advantage of parallel filesystems performane and knowledge of where MPI task should
  read or write data.

All forms of MPI-IO require the use of `MPI_File_Open`.  `mpi4py` uses:
~~~
MPI.File.Open(comm, filename, amode)
~~~
{: .language-python}

Where `amode` is the access mode - such as `MPI.MODE_WRONLY`, `MPI.MODE_RDWR`, `MPI.MODE_CREATE`.  This can be combined
with bitwise-or `|` operator.

There are 2 types of I/O, independent and collective. **Independent I/O** is like standard Unix I/O whilst **Collective I/O** is where all MPI tasks in the communicator must be involved in the operation.   Increases the opportunity
for MPI to take advantage of optimisations such as large block I/O that is much more efficient that small block I/O.

### Independent I/O

Just like Unix like `open`, `seek`, `read/write`, `close`.  MPI has a way of allowing a single task to read and write
from a file.

- `MPI_File_seek` - seek to position
- `MPI_File_read` - read from a task.
- `MPI_File_write` - write from a task.
- `MPI_File_read_at` - seek and read from task.
- `MPI_File_write_at` - seek and read from task.
- `MPI_File_read_shared` - read using shared pointer
- `MPI_File_write_shared` - write using shared pointer

`mpi4py` have its similar versions e.g. `File.Seek` - see `help(MPI.File)`

For example to write from the leader:

~~~
from mpi4py import MPI
import numpy as np

amode = MPI.MODE_WRONLY|MPI.MODE_CREATE
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
fh = MPI.File.Open(comm, "./datafile.mpi", amode)

buffer = np.empty(10, dtype=np.int)
buffer[:] = rank

offset = comm.Get_rank() * buffer.nbytes
if rank == 0:
    fh.Write_at(offset, buffer)

fh.Close()
~~~
{: .language-python}

Useful where collective calls do not naturally fit in code or overhead of collective calls outweigh benefits (e.g. small
I/O)

### Collective non-contiguous I/O

If a file operation needs to be performed across the whole file but not contigious (e.g. gaps between data that the each
task reads).  This uses the concept of a *File view* set with `MPI_File_set_view`.  `mpi4py` uses `fh.Set_view` where
`fh` is the file handle returned from `MPI.File.Open`.

~~~
fh.Set_view(displacement, filetype=filetype)
~~~
{: .language-python}

`displacement` is the location in the file and `filetype` is a description of the data for each task.

Key functions are:
- `MPI_File_seek` - seek to position
- `MPI_File_read_all` - read across all tasks.
- `MPI_File_write_all` - write across all tasks.
- `MPI_File_read_at_all` - seek and read all tasks.
- `MPI_File_write_at_all` - seek and read all tasks.
- `MPI_File_read_ordered` - read using shared pointer
- `MPI_File_write_ordered` - write using shared pointer

The `_at_` versions of the functions are better than performing a seek and then an read or write.  See `help(MPI.File)`

For example:

~~~
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

amode = MPI.MODE_WRONLY|MPI.MODE_CREATE
fh = MPI.File.Open(comm, "./datafile.noncontig", amode)

item_count = 10

buffer = np.empty(item_count, dtype='i')
buffer[:] = rank

filetype = MPI.INT.Create_vector(item_count, 1, size)
filetype.Commit()

displacement = MPI.INT.Get_size() * rank
fh.Set_view(displacement, filetype=filetype)

fh.Write_all(buffer)
filetype.Free()
fh.Close()
~~~
{: .language-python}

### Contiguous collective I/O

Contiguous collective I/O is where all tasks are used to perform the I/O operation across the whole data.

> ## Contiguous example
>
> Write a file where each MPI task write 10 elements with value of its rank in order of rank.
>
> > ## Solution
> > 
> > This is very similar to the non-contiguous I/O but the file view is not required.
> > ~~~
> > offset = comm.Get_rank() * buffer.nbytes
> > fh.Write_at_all(offset, buffer)
> > ~~~
> > {: .language-python}
> >
> {: .solution}
{: .challenge}

See example in [mpiio.py]({{ site.baseurl }}/files/example5/mpiio.py)

### Access patterns

Access patterns can greatly impact the performance of the I/O.  It is expressed with 4 levels - level 0 to level 3.

- Level 0, each process makes one independent read request for each row in the local array.
- Level 1, similar to leve 1 but collective I/O functions are used.
- Level 2, process creates a derived filetype using non-contiguous access pattern and calls independent I/O functions.
- Level 3, similar to level 2 but each process uses collective I/O functions.

In summary MPI-IO requires some special care but worth looking at closer if you have large data access requirements in
your code.  Level 3 would give the best performance.

## Application toplogies

MPI tasks have no favoured orientation or priority, however it is possible to map tasks onto a virtual topology.  The
topologies are:
- **Cartesian**, a regular grid
- **Graph**, a more complex connected structure.

The functions used are:
- `MPI_Cart_Create` - creates a Cartesian topology from specified communicator
- `MPI_Cart_Get` - returns information about a given topology
- `MPI_Cart_Rank` - return rank from Cartesian location
- `MPI_Cart_Coords` - return coordinates for a task of a given rank
- `MPI_Cart_Shift` - discover rank of near neighbour given a shifted direction. i.e. Up, Left, etc.

In `mpi4py` to create a Cartesian toplogy:
~~~
cart = comm.Create_cart(dims=(axis, axis),
                        periods=(False, False), reorder=True)
~~~
Then the methods are applied to the `cart` object.
~~~
cart.Get_topo(...)
cart.Get_cart_rank(...)
cart.Get_coords(...)
cart.Shift(...)
~~~
{: .language-python}

See: `help(MPI.Cartcomm)`

There is an example [cartesian.py]({{ site.baseurl }}/files/example6/cartesian.py).

## Hybrid MPI and OpenMP

With Python this would be tricker (but not impossible to do).  You can instead create threads in Python with the
`multiprocessing` module.  The MPI implementation you use would need to support the threading method you want.

Basically the following can be suggested:
- When calling OpenMP (or other threads) from within an MPI task it should be perfectly safe.  MPI task is just a
  process.
- When calling MPI from within an OpenMP thread it will depend on MPI implementation and thread safety of the MPI task.

The levels of threading in MPI is described with:

`MPI_THREAD_SINGLE` - only one thread will execute MPI commands.
`MPI_THREAD_FUNNELED` - the process may be multi-threaded but only the main thread will make MPI calls.
`MPI_THREAD_SERIALIZED` - the process may be multi-threaded and multiple threads may make MPI calls, but only one at a
time.
`MPI_THREAD_MULTIPLE` - multiple threads may cal MPI, with no restrictions.

`mpi4py` calld `MPI_Init_thread` requesting `MPI_THREAD_MULTIPLE`.  The MPI implementation tries to fulfil that but can
provide a different level of threading support but closed to the requested level.

This really only becomes a concern when writing MPI with C and Fortran.


{% include links.md %}

