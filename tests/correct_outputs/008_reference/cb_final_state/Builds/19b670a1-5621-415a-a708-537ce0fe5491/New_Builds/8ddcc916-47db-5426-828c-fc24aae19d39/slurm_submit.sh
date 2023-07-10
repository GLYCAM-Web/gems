#!/bin/bash
#SBATCH --chdir=/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/19b670a1-5621-415a-a708-537ce0fe5491/New_Builds/8ddcc916-47db-5426-828c-fc24aae19d39
#SBATCH --error=slurm_%x-%A.err
#SBATCH --get-user-env
#SBATCH --job-name=Glycan-19b670a1-
#SBATCH --nodes=1
#SBATCH --output=slurm_%x-%A.out
#SBATCH --partition=amber
#SBATCH --tasks-per-node=4

export MDUtilsTestRunWorkflow=Yes

/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/19b670a1-5621-415a-a708-537ce0fe5491/New_Builds/8ddcc916-47db-5426-828c-fc24aae19d39/Minimize.bash
