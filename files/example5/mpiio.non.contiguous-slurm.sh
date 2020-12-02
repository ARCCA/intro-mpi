#!/bin/bash --login
#SBATCH -n 4
#SBATCH -t 0-00:05:00
#SBATCH -J Non.Contiguous
#SBATCH --account scwXXXX
#SBATCH -p compute
#SBATCH -o mpiio.non.contiguous.out.%j

# if run on a training session add your reservation code as
# #SBATCH --reservation=training

# Load required modules.
module purge
module load python
module load mpi
module list

# Create an output directory on the fast scratch filesystem, and
# run from this directory.
WDPATH=/scratch/$USER/mpi_training/mpiio.non.contiguous.$SLURM_JOBID
mkdir -p $WDPATH
cd $WDPATH

# Copy the python code to the run directory
cp $SLURM_SUBMIT_DIR/mpiio.non.contiguous.py .

# Run a number of copies of the code equal to the number of
# MPI processes requested.
mpirun -np 4 python3 mpiio.non.contiguous.py
