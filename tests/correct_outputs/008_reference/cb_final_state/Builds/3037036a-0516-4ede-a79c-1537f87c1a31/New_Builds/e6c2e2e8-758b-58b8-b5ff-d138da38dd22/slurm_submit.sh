#!/bin/bash
#SBATCH --chdir=/website/userdata/sequence/cb/Builds/3037036a-0516-4ede-a79c-1537f87c1a31/New_Builds/e6c2e2e8-758b-58b8-b5ff-d138da38dd22
#SBATCH --error=slurm_%x-%A.err
#SBATCH --get-user-env
#SBATCH --job-name=Glycan-3037036a-
#SBATCH --nodes=1
#SBATCH --output=slurm_%x-%A.out
#SBATCH --partition=amber
#SBATCH --tasks-per-node=4

export MDUtilsTestRunWorkflow=Yes

/website/userdata/sequence/cb/Builds/3037036a-0516-4ede-a79c-1537f87c1a31/New_Builds/e6c2e2e8-758b-58b8-b5ff-d138da38dd22/Minimize.bash
