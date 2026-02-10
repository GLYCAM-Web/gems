#!/usr/bin/env bash

echo "Generating an Instance Config for a Remote Execution, Website, Swarm, Instance"

export EXECUTION_CONTEXT=Mixed # Can have local and remote needs
                               # Values: Service Standalone Local Remote Mixed
export WEBSITE_CONTEXT=Swarm   # This is a website running in a docker swarm
                               # Values: Standalone DevEnv Swarm None

# Declare all the arrays
declare -a Services
Services=( 
	"MD" 
	"GM" 
	"AD" 
	"GP" 
	) # One day might need CB, GF and others

declare -A PreconfigName # This is for use in the test
PreconfigName=(
	["MD"]=
	["GM"]=
	["AD"]=
	["GP"]=
	)

# For now, I am making these names be more descriptive, but will not change the names used in GEMS
declare -A SubmissionHosts       # Connection info (e.g., IP Addy) for hosts to which batch jobs are submitted (e.g., Slurm Hosts)
declare -A SubmissionHostNames   # Names for these hosts - are descriptive and need not correspond to anything, but probably should for sanity
declare -A SubmissionHostPorts   # Ports for these hosts 
declare -A RedirectionHosts      # Same as above, but for hosts to which JSON requests should be forwarded
declare -A RedirectionHostNames
declare -A RedirectionHostPorts
declare -A BatchSubmissionArgs   # Submission arguments for the service (each service will treat as default, enforced, etc., as needed)
declare -A LocalParameters       # If execution is local, provide some preferences
declare -A LocalWorkingPathHead  # The parent directory for working directories on the local machine
declare -A RemoteWorkingPathHead # The parent directory for working directories on the remote machine 
                                 # TODO - Consider if this can be known only by the remote host.
				 #        This is of use to sysadmins for mounting remote directories, but is not of use to GEMS, generally.
				 #        One exception would be the preparation of instructions to be executed remotely, but it seems that
				 #        variables could be used that are set at the remote location.

SubmissionHosts=(
	["MD"]='172.16.4.2'
	["GM"]='172.16.4.4'
	["AD"]='172.16.4.2'
	["GP"]='172.16.4.2'
	)
SubmissionHostNames=(
	["MD"]='thoreau'
	["GM"]='harper'
	["AD"]='thoreau'
	["GP"]='thoreau'
	)
SubmissionHostPorts=(
	["MD"]='42029'
	["GM"]='42029'
	["AD"]='42030'
	["GP"]='42030'
	)
    AD_JSON_PORT=42031 # UNUSED currently, but needs to be set for AD.
RedirectionHosts=(
	["MD"]=''
	["GM"]=''
	["AD"]='172.16.4.2'
	["GP"]=''
	)
RedirectionHostNames=(
	["MD"]=''
	["GM"]=''
	["AD"]='thoreau'
	["GP"]=''
	)
RedirectionHostPorts=(
	["MD"]=''
	["GM"]=''
	["AD"]='42030'
	["GP"]=''
	)
SbatchArgs=(
	["MD"]='{ "partition": "mdaas", "time": "120", "nodes": "1", "gres": "gpu:1", "tasks-per-node": "4", "cpus-per-task": "7" }'
	["GM"]='{ "partition": "gm", "time": "120", "nodes": "1", "gres": "gpu:1", "tasks-per-node": "4", "cpus-per-task": "7" }'
	["AD"]='{ "partition": "amber", "time": "120", "nodes": "1", "tasks-per-node": "4" }'
	["GP"]='{ "partition": "amber", "time": "120", "nodes": "1", "tasks-per-node": "4" }'
	)
LocalParameters=(
	["MD"]='{ "numProcs": "4" }'
	["GM"]='{ "numProcs": "4" }'
	["AD"]='{ "numProcs": "4" }'
	["GP"]='{ "numProcs": "4" }'
	)
LocalWorkingPathHead=(
	["MD"]="/website/userdata/mmservice/md"
	["GM"]="/website/userdata/complex/gm"
	["AD"]="/website/userdata/complex/ad"
	["GP"]="/website/userdata/conjugate/gp"
	)
RemoteWorkingPathHead=(
	["MD"]="/scratch2/thoreau-web/mmservice/swarmtest-md"
	["GM"]="/scratch2/harper-web/complex/swarmtest-gm"
	["AD"]="/scratch2/thoreau-web/complex/swarmtest-ad"
	["GP"]="/scratch2/thoreau-web/conjugate/swarmtest-gp"
	)


