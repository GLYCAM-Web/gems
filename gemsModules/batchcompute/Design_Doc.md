# Design Documentation for the Batch Compute gemsModule

Name variants:
- batchcompute    - Directory name for the gemsModule
- Batchcompute    - Entity name, app name
- Batch Compute   - Easy-read Entity name for documents
- `Batch_Compute` - Easy-read Entity name for documents where a single 'word' is desirable
- bc              - Service ID, name of output tree root directory
- BC              - Internal use within instances managed by Configuration
                    Also used as an abbreviation in documents

This Entity has no child Entities and no parent Entity.

---

## Purpose and Goals

Batch Compute manages the submission of computational jobs to a high performance computing (HPC) cluster. 

It will generate input files appropriate to a given scheduler (e.g., Slurm, PBS, LoadLeveler), submit the 
job, report submission status, and report on the status of the submission. If the localhost is not able to
accept job submissions, BC will attempt to find an acceptable host.

---

## Available Services

Default (implied) Service: SubmitJob

- `Validate`
- `Report_Host_Capabilities`
- `Evaluate`
- `Manage_Submission_Files`
- `Submit_Job`
- `Status`

See below for Service details.

---

## Relation to Other gemsModules

- `Common`: Standard child.
- `Configuration`: 
  - Relies on Configuration to read the instance config (IC) for cluster information.
  - Provides Configuration with additional data to include in the IC.
- `Project`: Standard sibling.
- `NetworkConnections`: 
  - Helps BC interrogate and connect to possible computing hosts.
- `SystemOperations`: Standard client.
- `Deprecated`: Should have no relationship at all.
- `Other`:
  - BC should provide HPC services to all other gemsModules who require it.
  - Of note: the other gemsModules should send JSON objects via Delegator.
    - The other modules should not access BC internals directly.
    - BC should only receive requests directly from Delegator and should respond in kind.
  - Handling by the client Entities:
    - Each request to BC should be handled as a `Service_Request`, storing the JSON object inside.
    - Similarly, the response from BC should be stored in a paired `Service_Response`.

---

## Relation to the gRPC modules

This module should use an abstracted method such as `networkconnections/seek_correct_host` rather than
interface gRPC directly. Doing this means that if the method of GEMS-to-GEMS communication needs to
change in the future, this module will not need to be altered.

### Deprecation of the Slurm module in gRPC

The older versions of Batch Compute used the `gRPC/SLURM` module which is being deprecated. As code is u
pdated, it should be moved away from that module and onto the `gRPC/JSON` module.

That is:

- `JSON`:
  - Batch Compute should become a client of this module.
- `SLURM`:
  - This modules is being deprecated.
  - It can be used as inspiration, but the JSON module should have all that is needed.

---

## Scheduler Support

Currently, Slurm is the only supported scheduler. Support is limited to the types of clusters typically
accessed by GLYCAM-Web (glycam.org). However, the structure of the module should allow for relatively 
simple addition of other schedulers.

Where scheduler information might change significantly from version to version, the file `instance_api.py`
should contain the relevant information. 

For example, versions of Slurm that were available during the earliest days of GPUs being used for complex
calculations did not natively handle GPUs as resources. On those clusters, the _generic resource_, or _gres_,
was used instead. Some of these clusters are still in use. For various reasons, even the modern Slurm clusters
might make use of the gres feature. So, it is necessary to know whether GPUs should be requested as gpu assets
or as gres assets.

---

## Services

----

### Validate

Ensures that the JSON object is properly formed and that the contents are actionable.

#### Inputs

A JSON object.

#### Resources from Other Modules

Dependence on other modules is not expected here, though possibly NetworkConnections or SystemOperations
might be useful, depending on the location of the division between Validate and Evaluate.

#### Outputs

The output should contain a list of Services for which the inputs are sufficient.

When used internally, it should be able to report if the JSON is valid for the requested Service.

----

### Report Host Capabilities

Reports the HPC capabilities of a given host. Defaults to localhost.

#### Inputs

The name of a host, if something other than localhost is desired. The host must be in the IC.

#### Resources from Other Modules

Relies on Configuration to inspect the IC.

#### Outputs

The HPC capabilities advertised in the IC. The format can mirror the IC.

It might be desirable to separate out the Pydantic definitions of the capabilities so that the classes can
be sourced by other modules without importing all of Configuration.

Consider moving any classes that are truly common into Common or Project.

----

### Evaluate

Evaluates whether the Services can use the inputs.

#### Inputs

A json object.

#### Resources from Other Modules

This service is likely to rely on: 
- Configuration
- Network Connections
- System Operations

#### Outputs

A list of Services for which the JSON object is complete. 

When used internally, it should be able to determine if the JSON is sufficient for the requestd Service.

----

### Manage Submission Files

Generates submisison files for the relevant host. 

Future feature: Evaluates existing submission files.

#### Delegated JSON Inputs

Must have:

- The name of the executable that the scheduler should run on the compute node.

Recommended:
- The name of the working directory.
- Resource information:
  - The type of resource needed: nodes, threads, cores, gpus, memory, time
    - For most resources, these should have a scope.
      - For example. nodes per job, cores per node, cores per job, etc.
    - The time limit typically applies on a per-job basis.
  - The amount of the resource needed. Entering "-1" or "Max" indicates as many as possible
- Name for easy identification of jobs.
- The partition to use.
- User name for running the jobs.

Also available:
- Should the user's environment be sourced?
- Name prefixes for the scheduler's output and error files.


#### Resources from Other Modules

Instance Config:
  - The scheduler type.
  - Whether 'cpu' means thread or core.
  - Partitions.
  - Available resources per partition.
  - Default max time (for reporting to users)

#### Outputs

Artifacts produced:
- Location of the files produced 
- Name(s) of the file(s) generated
- Name(s) of any Heredoc files to be generated (even if these names contain variables)

For reporting Artifacts, use of a Resource is preferred, but can just be a string. Use of a Resource
includes useful metadata about the Artifact.

----

### Submit Job

Submits a job to a cluser.

#### Environment

- The code must be able to execute the script in the correct location, typically the cluster's headnode.

#### Inputs

- Path to submission script

#### Resources from Other Modules

If the standard submission executable is not to be used, that info should be in the IC.

That is, if the submission executable for the Slurm cluster is not 'sbatch', then the code needs to know
what its name is.

#### Outputs

The JSON output should return information about the job submmission.

Must contain:
- The job id

----

### Status

Reports the status of a submitted job.

#### Inputs

Job ID number.

#### Resources from Other Modules

None expected unless the standard query executable is not to be used.

#### Outputs

Job status, including:
- Waiting, Running, Completing, Finished
- Other information as appopriate:
  - Waiting:
    - Number of jobs ahead in queue
      - Number waiting
      - Number running 
      - Number completing
    - If possible, a time estimate before the job starts
      - This is probably only possible if the partition/queue has a strict time limit per job.
  - Running
    - Time running so far
    - If there is a time limit, time remaining
    - Note: Job-specific time estimates need to be handled by the Status Service of the client Entity
  - Completing
    - If possible, an estimate of the time usually required for job clean-up, etc.
  - Finished
    - Date/time when the job completed

---

## Current Support

It is not feasible to write this Entity for all possible scenarios. We will add capabilities as they
are needed.

- Scheduler: Only Slurm is supported.
- Restrictions:
  - For now, task and job will have the same meaning.
    - Thus, this should not be specified or should equal '1': #SBATCH --tasks-per-node
    - For now, the MPI manager or the run script will manage tasks per job.
- Scheduler options:
  - Working directory (#SBATCH --chdir) 
    - Setting this is strongly recommended
    - default: current working directory (can be undefined or unpredictable)
  - Cores per task/job / Threads per task/job
    - This will combine:
      - #SBATCH --cpus-per-task
      - With info about the meaning of cpu from the IC: `BatchComputingResources.cpu_hardware_equivalent`
    - It might also use other info in BatchComputingResources for reserving 'maximum' amounts of resources.
    - The IC should suggest a default and a maximum
  - GPUs per task/job
    - If the IC indicates that gres should be used, then it will be used
      - #SBATCH --gres
      - #SBATCH --gpus-per-task (check this name bc from memory)
    - The IC should suggest a default and a maximum
  - Nodes per job (#SBATCH --nodes)
    - The IC should suggest a default and a maximum
  - Time limit (cannot exceed limit in the IC) (#SBATCH --time)
    - default: IC time limit for the partition
  - Prefix for scheduler error and output. 
    - It will apply to: 
      - #SBATCH --error
      - #SBATCH --output
    - Default - use whatever Slurm sets (do not set one in the file).
  - Source the user's environment? (#SBATCH --get-user-env)
    - default: use this so that the env is sourced
  - Job Name (#SBATCH --job-name)
    - default: Slurm's default
  - Partition (aka Queue) (#SBATCH --partition)
    - default: Slurm's default
  - UID for submission (#SBATCH --uid)
    - default: Slurm's default
