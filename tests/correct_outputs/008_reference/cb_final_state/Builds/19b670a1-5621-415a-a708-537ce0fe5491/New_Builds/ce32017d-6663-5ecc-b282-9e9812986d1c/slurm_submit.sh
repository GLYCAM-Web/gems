#!/bin/bash
#SBATCH --chdir=/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/19b670a1-5621-415a-a708-537ce0fe5491/New_Builds/ce32017d-6663-5ecc-b282-9e9812986d1c
#SBATCH --error=slurm_%x-%A.err
#SBATCH --get-user-env
#SBATCH --job-name=Glycan-19b670a1-
#SBATCH --nodes=1
#SBATCH --output=slurm_%x-%A.out
#SBATCH --partition=amber
#SBATCH --tasks-per-node=4

export MDUtilsTestRunWorkflow=Yes

/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/19b670a1-5621-415a-a708-537ce0fe5491/New_Builds/ce32017d-6663-5ecc-b282-9e9812986d1c/Minimize.bash
