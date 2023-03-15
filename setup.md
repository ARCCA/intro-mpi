---
layout: page
title: Setup
permalink: /setup/
---

There are several pieces of software you will wish to install before the workshop.
Though installation help will be provided at the workshop,
we recommend that these tools are installed (or at least downloaded) beforehand.

## SSH

All students should have an SSH client installed.
SSH is a tool that allows us to connect to and use a remote computer as our own.
Please follow the directions below to install an SSH client for your system.

**Windows**

Install MobaXterm from [http://mobaxterm.mobatek.net](http://mobaxterm.mobatek.net).
You will want to get the Home edition (Installer edition).

**macOS**

Although macOS comes with SSH pre-installed,
you will likely want to install [XQuartz](http://www.xquartz.org) to enable graphical support.
Note that you must restart your computer to complete the installation.

**Linux**

Linux users do not need to install anything, you should be set!

## File Transfer

A cross-platform tool FileZilla can be installed from [https://filezilla-project.org](https://filezilla-project.org).
This will allow easy file transfer to and from the remote systems.

## MPI

If not using Hawk see below for platform instructions.

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
$ python -m venv venv
$ venv\Scripts\activate.bat
$ python -m pip install mpi4py
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
$ python3.7 -m venv venv
$ . venv/bin/activate
$ python3.7 -m pip install -U pip
$ python3.7 -m pip install mpi4py
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

Then install mpi4py

~~~
$ python3 -m venv venv
$ . venv/bin/activate
$ python3 -m pip install -U pip
$ python3 -m pip install mpi4py
~~~
{: .source}

{% include links.md %}
