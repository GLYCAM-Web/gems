#!/bin/bash
#SBATCH --chdir=/website/userdata/sequence/cb/Builds/f86b075b-a9cc-465e-bc7a-512004946bbc/New_Builds/structure
#SBATCH --error=slurm_%x-%A.err
#SBATCH --get-user-env
#SBATCH --job-name=Glycan-f86b075b-
#SBATCH --nodes=1
#SBATCH --output=slurm_%x-%A.out
#SBATCH --partition=amber
#SBATCH --tasks-per-node=4

export MDUtilsTestRunWorkflow=Yes

/website/userdata/sequence/cb/Builds/f86b075b-a9cc-465e-bc7a-512004946bbc/New_Builds/structure/Minimize.bash
