# Communication Between GEMS Instances

GEMS instances are designed to be able to communicate with each other. 

## Rationale

It is impractical, if not impossible, to have a single computer be able to perform all the tasks needed
for all the scientific services managed by GEMS. So, GEMS is designed to be installed on two (or more) 
computers with different capabilities. For example, one GEMS might directly serve the needs of GLYCAM-Web 
while another might reside on an HPC cluster so that it can submit and analyze jobs.

The original need: 

At the time (and possibly still), Slurm, a computing resource manager and scheduler, did not have a 
mechanism for receiving job submissions from another computer.  After researching various options, such 
as SSH, gRPC was chosen for the task. GRPC allows for very fine control of the information flow, allowing 
for lighter weight, more targeted, and more secure communications.

## Mechanism

The coding mechanics of the GEMS-to-GEMS communications can be found in:

```
$GEMSHOME/gRPC/JSON/                               # Generates the gRPC client and server
$GEMSHOME/gemsModules/networkconnections/          # Uses the gRPC client 
$GEMSHOME/gemsModules/configuration/               # Manages the database of accessible GEMS instances
$GEMSHOME/gemsModules/complex/antibody/receive.py  # Sample use of forwarding requests via gRPC
```

The basic workflow is as follows:

1. Some gemsModule receives a JSON request via the local Delegator.
2. If the current host cannot complete the job, the gemsModule uses `seek_correct_host` (1) to:
    - Find a host with the needed resources
    - Forward the JSON request to the delegator at the remote host
    - Receive the returned JSON response 

See `$GEMSHOME/gemsModules/configuration` regarding the database of accessible GEMS instances.

(1) This function is in: `$GEMSHOME/gemsModules/networkconnections/seek_correct_host.py`.

