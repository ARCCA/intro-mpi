#!/bin/bash --login
#SBATCH -J SineIntegral
#SBATCH -o sine.integral.out.%j
#SBATCH -n 4
#SBATCH -t 0-00:05:00
#SBATCH -p dev
#SBATCH --account scwfXXXXX_j_doe_X # check your accounts with the command `myaccounts`

# if run on a training session add your reservation code as
# #SBATCH --reservation=training

set -euo pipefail

# Load required modules.
module purge
module load mpi4py/4.1.0-gompi-2025a
module load SciPy-bundle/2025.06-gfbf-2025a
module list

# use scratch directory associated with account in current job
# see output of `myprojects` for a full list of your projects
# and replace if you prefer another
MYPROJECT=`echo ${SLURM_JOB_ACCOUNT} | cut -d'_' -f1 | awk '{ print toupper($0) }'`
# Create an output directory on the fast scratch filesystem, and
# run from this directory.
SCRATCH=/scratch/${MYPROJECT}/${USER}/mpi_training/${SLURM_JOB_ID}
# check if we can actually create our SCRATCH directory
mkdir -p ${SCRATCH} || (echo "error, cannot create ${SCRATCH} directory" && exit 1)

cd ${SCRATCH}

# Copy the python code to the run directory
cp ${SLURM_SUBMIT_DIR}/sine.py .

# Run a number of copies of the code equal to the number of
# MPI processes requested.
mpirun -np ${SLURM_NTASKS} python3 sine.py

# clean up scratch (only reached if everything above succeeded)
cd "${SLURM_SUBMIT_DIR}"
rm -rf -- "${SCRATCH:?}"
