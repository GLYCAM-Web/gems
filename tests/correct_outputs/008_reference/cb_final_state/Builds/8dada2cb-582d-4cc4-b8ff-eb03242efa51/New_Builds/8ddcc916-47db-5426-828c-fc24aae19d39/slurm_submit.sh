#!/bin/bash
#SBATCH --chdir=/website/userdata/sequence/cb/Builds/8dada2cb-582d-4cc4-b8ff-eb03242efa51/New_Builds/8ddcc916-47db-5426-828c-fc24aae19d39
#SBATCH --error=slurm_%x-%A.err
#SBATCH --get-user-env
#SBATCH --job-name=Glycan-8dada2cb-
#SBATCH --nodes=1
#SBATCH --output=slurm_%x-%A.out
#SBATCH --partition=amber
#SBATCH --tasks-per-node=4

export MDUtilsTestRunWorkflow=Yes

/website/userdata/sequence/cb/Builds/8dada2cb-582d-4cc4-b8ff-eb03242efa51/New_Builds/8ddcc916-47db-5426-828c-fc24aae19d39/Minimize.bash
