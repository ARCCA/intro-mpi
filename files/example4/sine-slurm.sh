#!/bin/bash --login
#SBATCH -n 4
#SBATCH -t 0-00:05:00
#SBATCH -J SineIntegral
#SBATCH -p compute
#SBATCH --account scw1248
#SBATCH -o sine.integral.out.%J

# Load required modules.
module purge
module load mpi4py/20181128
module list

# Create an output directory on the fast scratch filesystem, and
# run from this directory.
WDPATH=/scratch/$USER/mpi_training/sine.integral.$SLURM_JOBID
mkdir -p $WDPATH
cd $WDPATH

# Copy the python code to the run directory
cp $SLURM_SUBMIT_DIR/sine.py .

# Run a number of copies of the code equal to the number of
# MPI processes requested.
mpirun -np 4 ./sine.py
