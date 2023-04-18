#!/bin/bash
#SBATCH --chdir=/website/userdata/sequence/cb/Builds/7eae9c9d-974c-48c1-83ec-1e5b8c94b869/New_Builds/c408f40d-28e0-5e8d-86a3-221b74da42f7
#SBATCH --error=slurm_%x-%A.err
#SBATCH --get-user-env
#SBATCH --job-name=Glycan-7eae9c9d-
#SBATCH --nodes=1
#SBATCH --output=slurm_%x-%A.out
#SBATCH --partition=amber
#SBATCH --tasks-per-node=4

export MDUtilsTestRunWorkflow=Yes

/website/userdata/sequence/cb/Builds/7eae9c9d-974c-48c1-83ec-1e5b8c94b869/New_Builds/c408f40d-28e0-5e8d-86a3-221b74da42f7/Minimize.bash
