---
title: "MPI standard"
teaching: 25
exercises: 5
questions:
- "Why was MPI developed?"
- "How can I use MPI?"
- "What is the basic code required?"
objectives:
- "Understand why MPI is important"
- "Understand how MPI can be coded"
- "Use the key MPI functions to write a basic example"
keypoints:
- "MPI allowed programmers to write portable code across many different supercomputer architectures."
- "MPI is available is available in many languages."
- "MPI requires function calls to pass data around."
---

## A brief history

The idea of message passing evolved in the 1980s where supercomputers were dominated by [Cray](https://en.wikipedia.org/wiki/Cray).
Due to dependency on Cray and competition was difficult this required new approaches to supercomputing.  Message passing was born 
out of a desire to link competing technologies. Cray realised that many cheaper commodity processors could be linked together
cheaper than fewer expensive vector processors. To make sure code was portable between systems, assurances were made to make this
possible hence MPI was formed.

MPI forum was formed in 1992 with its first standard in 1994, available in C and Fortran. The easiest approach was to decompose 
data for processors to work on the same problem (but different views). This works within processors on a node and across a network
and is Limited only by *Amdahl's Law*.

MPI standard is **large**, but the good news is that many programs only use a small subset. There are many sophisticated functions
available. The design of MPI makes no assumptions on underlying hardware so work with homogenous and heterogeneuos systems, that
is to say it is hardware vendor neutral.

> ## ECMWF weather and climate model IFS
>
> A well respected weather and climate model called IFS, developed by the European Centre for Medium-range Weather
> Forecasting, [ECMWF](https://www.ecmwf.int), only required approximately 10 MPI calls.
{: .callout}

## Preliminary information

The examples are written in Python using the [**mpi4py**](http://mpi4py.readthedocs.io) module.  This should be easily
translated into other languages. The web can be used for information.

> ## Data models
>
> - **SPMD** - Single Program Multiple Data is usually the recommended approach.
>   - One program executes mutliple times.
>   - Problem divided using the same executable code.
>
> - **MPMD** - Multiple Program Multiple Data can be trickier to master.
>   - Different executables used to communicate
>   - Useful to couple different models that would contain completely different approaches such as ocean and atmosphere
>    modelling.
>   - Available in MPI version 2.0
{: .callout}

> ## Definitions
>
> - Task
>   - One running instance of program
>   - Basic unit of MPI parallel code
> - Leader
>   - The first task in the set of parallel tasks
>   - Given id of zero
> - Follower
>   - All other tasks in the program.
>   - No real difference other than usually leader can interact easily with system, such as I/O.
{: .callout}

## Hello World!

The following command executes a 3 MPI tasks.

~~~
$ mpirun -np 3 echo "hello_world"
~~~
{: .language-bash}

~~~
hello_world
hello_world
hello_world
~~~
{: .output}

![mpirun example](../fig/mpirun_example.png)

A more meaningful *hello world* program may be written as:
~~~
#!/bin/env python
#
# Hello World MPI

from mpi4py import MPI # Python MPI library
import sys

if __name__ == "__main__":
# What rank process is this?
    try:
        comm = MPI.COMM_WORLD # Initiate communications
        rank = comm.Get_rank()
        size = comm.Get_size()
        # Say hello
        print(f"Hello World from process: {rank} of {size}")
    except Exception as err:
        sys.exit("Error: %s" % err)
~~~
{: .language-python}

Then run in SLURM with:

~~~
#!/bin/bash --login
#SBATCH -p compute
#SBATCH --account=scw1148
#SBATCH --ntasks=3
#SBATCH --tasks-per-node=3
#SBATCH -o HelloPython.out
#SBATCH -t 00:05:00

# Load required modules. module purge
module load python
module load mpi
# Run 3 (mpirun knows SLURM variables) copies of the code
mpirun python3 hello_parallel.py
~~~
{: .language-bash}

## Initialisation and identification

The [MPI standard](https://www.mpi-forum.org/docs/) defines the following.

- **`MPI_init` and `MPI_init_thread`** - initialises MPI environment.  Required by MPI standard.
- **`MPI_COMM_WORLD`** - a provided communicator that allows all processors to "talk" to all others.
- **`MPI_comm_size`** - a function that returns the total number of processors in communicator.
- **`MPI_comm_rank`** - a function that returns the id of the current exectuable within the communicator.
- **`MPI_finalize`** - a function that shuts down MPI communications - the counterpart to **`MPI_init`**.

In Python these are used behind the scenes to perform similar functionality but in a Pythonic manner.  For example
at import time the `MPI_init_thread` is called. At exit `MPI_finalize` is called automatically. The `MPI_comm_rank` and
`MPI_comm_size` functions are called in the `mpi4py` communicator methods `Get_rank` and `Get_size`.

## The MPI Python module

- **mpi4py** is the top-level package.
  - provides package **MPI**
  - contains all the MPI constructs and parameters.
  - encapsulates the MPI protocol in wrapper functions to allow passing of python objects not coverred by the MPI
   standard.

> ## Install the package on Hawk
>
> Since this is a Python package, anyone should be able to download and install the package.  How would you go about
> doing this? (Hint: Look at previous [SLURM Advanced Topics](https://arcca.github.io/slurm_advanced_topics/08-packages/index.html)
> > ## Solution
> >
> > There is a dependency on MPI so you would need to load the mpi module.  The Python package will already load a
> > compiler.  Check `module list` after loading modules.
> > 
> > To install **mpi4py**:
> > ~~~
> > $ module load python
> > $ module load mpi
> > $ pip3 install --user mpi4py
> > $ python3 -c "import mpi4py"
> > ~~~
> > {: .language-bash}
> {: .solution}
{: .challenge}

## Other platforms

MPI can be installed on other platforms along with Python.

### Microsoft Windows

Microsoft Windows makes available Microsoft MPI (MS-MPI).  It is possible to download from the
[website](https://docs.microsoft.com/en-us/message-passing-interface/microsoft-mpi) the latest version
([v10.1.2](https://www.microsoft.com/en-us/download/details.aspx?id=100593) has been tested.  For the run-time
executables such as mpiexec install `msmpisetup.exe`, for compile time files such as include and library files install `msmpisdk.msi`.

You will need to install [Microsoft Visual Studio](https://visualstudio.microsoft.com).  You can then compile C++ code
using the tutorial on their
[website](https://docs.microsoft.com/en-us/archive/blogs/windowshpc/how-to-compile-and-run-a-simple-ms-mpi-program)

It is also possible to install `mpi4py` on Windows with the above files.  For example install
[Python](https://www.python.org).  Make sure you add Python to the the default PATH during installation.  It is then
possible to run using `cmd`:

~~~
$ python -m pip install --user mpi4py
~~~
{: .source}

Then with an example MPI Python file `mpihelloworld.py`

~~~
$ mpiexec python mpihelloworld.py
~~~
{: .source}

### Apple Mac

For a lot of software that is not supported by Apple can be installed with [Homebrew](https://brew.sh).

After installing Homebrew, use

~~~
$ brew install openmpi
~~~
{: .source}

This should install [Open MPI](https://www.openmpi.org) in `/usr/local`.  This can then compile C code with `mpicc` or
C++ with `mpicxx` and run with `mpirun` or `mpiexec`.

Python can also be installed with Homebrew and then `mpi4py` can be installed using:

~~~
$ python3.7 -m pip install --user mpi4py
~~~
{: .source}

### Linux

Open MPI tends to be available with many of the popular Linux distributions.  For example Ubuntu can install Open MPI
with

~~~
$ apt-get install openmpi-bin libopenmpi-dev
~~~
{: .language-bash}

There is also [MPICH](https://www.mpich.org) which is a different implementation of the MPI standard. Either package
should provide compiler wrappers `mpicc` and `mpicxx` along with runtime executables `mpirun` or `mpiexec`.

{% include links.md %}

