#!/bin/bash
#SBATCH --chdir=/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/83e38ccd-af2f-4402-a5bc-7c1629a85d1b/New_Builds/b90a4d30-822c-5aba-ae5a-10a9ddb1a227
#SBATCH --error=slurm_%x-%A.err
#SBATCH --get-user-env
#SBATCH --job-name=Glycan-83e38ccd-
#SBATCH --nodes=1
#SBATCH --output=slurm_%x-%A.out
#SBATCH --partition=amber
#SBATCH --tasks-per-node=4

export MDUtilsTestRunWorkflow=Yes

/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/83e38ccd-af2f-4402-a5bc-7c1629a85d1b/New_Builds/b90a4d30-822c-5aba-ae5a-10a9ddb1a227/Minimize.bash
