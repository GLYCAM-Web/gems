# Sub-module batchcompute/slurm

The purpose of this module is to interface the Slurm Workload Manager (we say
_scheduler_).  You can learn more about Slurm here:

https://slurm.schedmd.com/

Notes:  

- This module only interfaces Slurm.  It is not the business of this module to 
  place or alter executables to be run by Slurm.
- This module should only perform actions on behalf of users.  Never should 
  any directive from a user be directly executed, including arguments to the
  various Slurm executables (e.g., `sbatch`, `squeue`, etc.).
- This module, like all other sub-modules of batchcompute, should know the 
  details regarding how to find appropriate hosts for executing jobs.  It 
  should also do the work of making calls to find a host.  However, the code 
  for making the calls, and for interpreting the responses, should live above, 
  in batchcompute.

## Input 



