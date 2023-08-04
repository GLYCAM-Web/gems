This document contains information relevant to the development of the MDaaS entity.

## Overview
At the coarsest view, MDaaS does these things:

1. Runs a molecular dynamics (MD) simulation based on user input and then returns the simulation results.
2. Queries the status of the MD simulation.

The following image gives a view with a little more detail.  In this image, we assume that the MD is performed by Amber and that the workload management is handled by Slurm.

![[GEMS - MDaaS Developer Overview.png]]

The MDaaS entity has two main functions, as indicated above:  run MD simulations and evaluate MD simulations.  Each of these functions is shown here as a process involving multiple components.  Some of the components call other entities (other modules, in the image). The truth is that MDaaS doesn't do very much itself. 

Soon, we will need a separate evaluation ("Evaluate Amber Input Files") that can be run without starting a simulation.  This is useful, for example, if you need to estimate for a user how much time/money/storage/etc. will be required for a job.  For now, we are not going to do that.  But, we will need to.

### The Workflows

Running MD:
1. MDaaS sets up the working directory (or, probably, calls another module to set it up). 
	1. It dumps a copy of the JSON request.
	2. It copies in the user's input files.
	3. It leaves log info.
2. MDaaS then calls the MD engine module (mmservice/amber in this case) to finish setting up the simulation
3. The MD engine (Amber) does these things:
	1. Evaluates the input files supplied by the user. Evaluations might include:
		1. Are they correctly-formatted files?
		2. Are they appropriate to the type of simulation being requested?
		3. What is the size of the system (atoms, residues, molecules, bonds, etc.)?
		4. Writes evaluation info to the working directory.
	2. Sets up the working directory for a simulation.
		1. Copies in protocol files.
		2. Edits configurations and/or protocol files if needed.
	3. Logs status information to the working directory.
	4. Returns status information to the caller.
4. MDaaS then calls the workload manager (batchcompute/slurm in this case) to submit the job to a cluster.
5. The workload manager (Slurm) does these things:
	1. Generates any input files that are needed.
	2. If it is not inside a GEMS instance that is running on a computer/container with Slurm installed, it gets gRPC to find a remote server with Slurm.
		1. In the future, the decision about which remote server to use might be complex.  We will need to decide where the responsibility for that decision should reside.
	3. Submits the job:
		1. Locally, if it is on the correct Slurm server.
		2. Via gRPC if it is not.
	4. Logs status information to the working directory.
	5. Returns status information to the caller.
		1. Notably, this information should contain the jobID, the name of the cluster, the path to the working directory (may not be the same as the path used by the caller), and anything else that is needed upstream.  
6. MDaaS writes logs to the working directory.
7. MDaaS returns info to the user.

Evaluating MD:
1. MDaaS checks the working directory to see if its logs contain all the info it needs.
	1. If it has the info it needs, it returns that info.
	2. Generally, this means that the job has completed and MDaaS needs only return info contained in files in the working dir.
2. If that is not true, then MDaaS calls the Amber module (MD engine) to query the working directory.
	1. Amber can tell if a job is still running or has finished and the status (success, failure, other).
	2. Often, it can also tell how much time is left for the job if it is still running.
	3. It can always tell how much of the job has been completed so far.
	4. Amber returns the info.
3. Any time a job in still running or has not yet run, MDaaS should call Slurm (workload manager) for info.
	1. MDaaS will need a jobID and the identity of the cluster where the job was submitted.
	2. The Slurm module can tell:
		1. How many jobs are in queue ahead, if any.
			1. If all the jobs in queue ahead of the queried job are on time limits, it can also guess a maximum wait time for the current job.  
			2. Otherwise, reporting a time-until-job-runs is nontrivial. 
		2. Whether there are any issues with the job (no usable nodes available, etc.)
		3. How long the job has been running.
	3. If Slurm reports that a job has finished, but Amber reports that it is still running, then an error has occurred.  This sort of error probably needs a human to look at it right now.

