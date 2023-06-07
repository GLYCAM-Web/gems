#!/bin/bash
#SBATCH --chdir=/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/9bf8a5f6-9aa8-441b-b424-01a315798799/New_Builds/6009ea31-3ded-57b9-aee3-2b65fe1071be
#SBATCH --error=slurm_%x-%A.err
#SBATCH --get-user-env
#SBATCH --job-name=Glycan-9bf8a5f6-
#SBATCH --nodes=1
#SBATCH --output=slurm_%x-%A.out
#SBATCH --partition=amber
#SBATCH --tasks-per-node=4

export MDUtilsTestRunWorkflow=Yes

/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/9bf8a5f6-9aa8-441b-b424-01a315798799/New_Builds/6009ea31-3ded-57b9-aee3-2b65fe1071be/Minimize.bash
