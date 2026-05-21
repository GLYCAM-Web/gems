# Readme for GEMS Module batchcompute

Provides entity Batchcompute which has a SubmitJob service.

Purpose:  Manage execution of jobs that happen outside GEMS or that are likely to take a very long time to execute.  
In particular, this module manages jobs that would reasonably be expected to execute on a high-performance computing
(HPC) machine or cluster.

Notably, the intention is not that this module should run short, local jobs. 


## Workflow

1. Instantiate the Transaction.

2. If the requested Service requires a computing resource, set it.

   A computing resource might not be required, for example, if a list of Services is requested.

   1. For now, it must be in the Instance Config.

   2. One day, Batchcompute could look for Slurm, etc., on the local machine.

3. Run the Service and return.



START HERE fixing the docs



### The information needed by all computing resources 

The tasks common to the batchcompute submodules are:

- Determining which host should run a job.

- Interacting with the scheduler (or OS) on that host.

- Instructing the scheduler to run the executable.

Therefore, batchcompute needs whatever information is necessary for
completing those tasks.

The JSON request should minimally contain:

- Path to the executable to be run.
- Path to the working directory where any output should go.
- Paths to any input files.

The JSON might also include the following, though they are more likely to be
contained in settings or environment variables (in a file or otherwise).

- Host and scheduler information.
- Computational limits such as time, memory, CPUs, etc.

#### Important notes

- Neither batchcompute nor its submodules should be generating or altering
  any input or executables.
- Executables must pre-exist in place.  It is not the job of batchcompute to 
  put executables anywhere or to construct them. 
- EXCEPT: the submodules will need to build the wrapper scripts for dealing 
  with the schedulers or the OS.  
- Nonetheless: the submodules will not accept direct commands to the OS or
  the schedulers, nor any options to be given to any commands.  The sub-
  modules will build or determine all OS/scheduler interactions.  They cannot 
  be imported within JSON, etc.


### Determining the location of the GEMS that should process the request

The GEMS instance whose batchcompute submodule first receives a JSON object
might not be the one that should ultimately process the object.  For example,
the GEMS most dirctly employed by the website is probably not running on the
head node of a supercomputer.  It uses GRPC to send the request to some other 
GEMS that is running on the head node of a supercomputer.  By design, the
non-HPC GEMS instance does not know the identity or location of the HPC-GEMS.
Instead, it relies on variables that could resolve to any one of a number of
values.  Specifically, the variables are the identity of the remote host that
should be queried and the port number over which to connect.  This would allow 
us, for example, to somewhat seamlessly offload overflow jobs to a temporary 
HPC cluster in some cloud-based IaaS.  

It is necessary to have that resolution of host ID and port number happen.  At
the moment, it is ultimately handled by environment variables (which can be 
read from a file or not).  

The decision regarding which host to use typically boils down to finding a 
host that is capable of running the job and has the capacity for doing so.

#### An example of how this might be used

Let's say that the website has, at its disposal, a cluster that can handle 
most of the normal website traffic.  Let's call that host "internal-hpc". 
Normally, the host ID is, then, "internal-hpc", or, more precisely, whatever
the IP address is for "internal-hpc".  But, perhaps, occasionally, something
causes the number of requested jobs to spike.  In this case, we might want 
to spin up a temporary IaaS and offload the extra jobs there.  


### Determining the recipient submodule

Currently, the only decision ie between 'localhost' and 'slurm'.  This is
decided, also currently, by inspecting certain variables to see if they 
are defined.  If the variables are not defined, localhost is chosen.

This need not remain the method forever.  Or, perhaps, it will always be
a good way.


