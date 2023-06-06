#!/bin/bash
#SBATCH --chdir=/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/cfde2aec-1760-4f29-855f-231114efdb5b/New_Builds/b90a4d30-822c-5aba-ae5a-10a9ddb1a227
#SBATCH --error=slurm_%x-%A.err
#SBATCH --get-user-env
#SBATCH --job-name=Glycan-cfde2aec-
#SBATCH --nodes=1
#SBATCH --output=slurm_%x-%A.out
#SBATCH --partition=amber
#SBATCH --tasks-per-node=4

export MDUtilsTestRunWorkflow=Yes

/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/cfde2aec-1760-4f29-855f-231114efdb5b/New_Builds/b90a4d30-822c-5aba-ae5a-10a9ddb1a227/Minimize.bash
