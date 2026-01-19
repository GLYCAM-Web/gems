#!/bin/bash
#SBATCH --chdir=/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/dbf3c342-4894-4517-861f-9fcfbd45dedb/New_Builds/6009ea31-3ded-57b9-aee3-2b65fe1071be
#SBATCH --error=slurm_%x-%A.err
#SBATCH --get-user-env
#SBATCH --job-name=Glycan-dbf3c342-
#SBATCH --nodes=1
#SBATCH --output=slurm_%x-%A.out
#SBATCH --partition=amber
#SBATCH --tasks-per-node=4

export MDUtilsTestRunWorkflow=Yes

/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/dbf3c342-4894-4517-861f-9fcfbd45dedb/New_Builds/6009ea31-3ded-57b9-aee3-2b65fe1071be/Minimize.bash
