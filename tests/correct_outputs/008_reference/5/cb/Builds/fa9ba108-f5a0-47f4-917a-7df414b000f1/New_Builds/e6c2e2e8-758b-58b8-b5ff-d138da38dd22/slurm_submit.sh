#!/bin/bash
#SBATCH --chdir=/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/fa9ba108-f5a0-47f4-917a-7df414b000f1/New_Builds/e6c2e2e8-758b-58b8-b5ff-d138da38dd22
#SBATCH --error=slurm_%x-%A.err
#SBATCH --get-user-env
#SBATCH --job-name=Glycan-fa9ba108-
#SBATCH --nodes=1
#SBATCH --output=slurm_%x-%A.out
#SBATCH --partition=amber
#SBATCH --tasks-per-node=4

export MDUtilsTestRunWorkflow=Yes

/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/fa9ba108-f5a0-47f4-917a-7df414b000f1/New_Builds/e6c2e2e8-758b-58b8-b5ff-d138da38dd22/Minimize.bash
