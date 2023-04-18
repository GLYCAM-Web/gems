#!/bin/bash
#SBATCH --chdir=/website/userdata/sequence/cb/Builds/140b63e5-e57a-4578-8c37-6eac6607b5c0/New_Builds/6009ea31-3ded-57b9-aee3-2b65fe1071be
#SBATCH --error=slurm_%x-%A.err
#SBATCH --get-user-env
#SBATCH --job-name=Glycan-140b63e5-
#SBATCH --nodes=1
#SBATCH --output=slurm_%x-%A.out
#SBATCH --partition=amber
#SBATCH --tasks-per-node=4

export MDUtilsTestRunWorkflow=Yes

/website/userdata/sequence/cb/Builds/140b63e5-e57a-4578-8c37-6eac6607b5c0/New_Builds/6009ea31-3ded-57b9-aee3-2b65fe1071be/Minimize.bash
