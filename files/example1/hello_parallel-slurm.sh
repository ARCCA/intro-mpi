#!/bin/bash --login
#SBATCH -n 12
#SBATCH -t 0-00:05:00
#SBATCH -J HelloParallel
#SBATCH -p compute
#SBATCH --account scwXXXX
#SBATCH -o hello_parallel.out.%j

# if run on a training session add your reservation code as
# #SBATCH --reservation=training

# Load required modules.
module purge
module load python
module load mpi
module list

# Create an output directory on the fast scratch filesystem, and
# run from this directory.
WDPATH=/scratch/$USER/mpi_training/hello_parallel.$SLURM_JOBID
mkdir -p $WDPATH
cd $WDPATH

# Copy the python code to the run directory
cp $SLURM_SUBMIT_DIR/hello_parallel.py .

# Run a number of copies of the code equal to the number of
# MPI processes requested.
mpirun -np 12 python3 hello_parallel.py
