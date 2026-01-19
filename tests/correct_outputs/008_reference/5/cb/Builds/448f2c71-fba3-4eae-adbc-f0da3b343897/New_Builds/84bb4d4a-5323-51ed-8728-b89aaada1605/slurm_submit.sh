#!/bin/bash
#SBATCH --chdir=/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/448f2c71-fba3-4eae-adbc-f0da3b343897/New_Builds/84bb4d4a-5323-51ed-8728-b89aaada1605
#SBATCH --error=slurm_%x-%A.err
#SBATCH --get-user-env
#SBATCH --job-name=Glycan-448f2c71-
#SBATCH --nodes=1
#SBATCH --output=slurm_%x-%A.out
#SBATCH --partition=amber
#SBATCH --tasks-per-node=4

export MDUtilsTestRunWorkflow=Yes

/website/TESTS/git-ignore-me/pre-push/sequence/cb/Builds/448f2c71-fba3-4eae-adbc-f0da3b343897/New_Builds/84bb4d4a-5323-51ed-8728-b89aaada1605/Minimize.bash
