#!/bin/bash
#SBATCH --chdir=/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/eb59785d-23ae-4e6c-bf83-0ddb4880335f/New_Builds/ce32017d-6663-5ecc-b282-9e9812986d1c
#SBATCH --error=slurm_%x-%A.err
#SBATCH --get-user-env
#SBATCH --job-name=Glycan-eb59785d-
#SBATCH --nodes=1
#SBATCH --output=slurm_%x-%A.out
#SBATCH --partition=amber
#SBATCH --tasks-per-node=4

export MDUtilsTestRunWorkflow=Yes

/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/eb59785d-23ae-4e6c-bf83-0ddb4880335f/New_Builds/ce32017d-6663-5ecc-b282-9e9812986d1c/Minimize.bash
