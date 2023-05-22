#!/bin/bash
#SBATCH --chdir=/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/52ef9ba3-52e6-4e00-a85e-0f16cf1ea2e4/New_Builds/e6c2e2e8-758b-58b8-b5ff-d138da38dd22
#SBATCH --error=slurm_%x-%A.err
#SBATCH --get-user-env
#SBATCH --job-name=Glycan-52ef9ba3-
#SBATCH --nodes=1
#SBATCH --output=slurm_%x-%A.out
#SBATCH --partition=amber
#SBATCH --tasks-per-node=4

export MDUtilsTestRunWorkflow=Yes

/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/52ef9ba3-52e6-4e00-a85e-0f16cf1ea2e4/New_Builds/e6c2e2e8-758b-58b8-b5ff-d138da38dd22/Minimize.bash
