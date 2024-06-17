# About

The Instance Configuration is used to configure the hosts that GEMs can connect to over gRPC with SLURM.

A GEMS instance can discern whether it can serve a request based on the contexts and hosts in the instance_config.json file. If it is not the correct context, the request can be forwarded over gRPC to the appropriate GEMS host configured in this instance's configuration file.

## Generating an instance_config.json file

See [setup_instance.md](setup_instance.md) for more information on setting up your instance_config.json file.

### DevEnv

GRPC/bin/initialize.sh initializes the GEMS instance configuration. This script is run when the DevEnv is started. It can be run manually from the GRPC folder.

### Manually

The Development environment configures a number

Also see [using_remote_hosts.md](using_remote_hosts.md) for more information on synchronizing remote host configurations.

## coder details

Please see `$GEMSHOME/gemsModules/systemoperations/instance_config` for the InstanceConfig Python class which provides helpers for reading and updating the instance_config.json file.

Curently, the only Services which use this feature are:
- "RunMD" GEMS requests, which are executed under MDaaS-RunMD contexts. 
- "Glycomimetics" GEMS requests, which are executed under Glycomimetics contexts. 

Both of these services utilize SLURM to batch Amber MD jobs. As an external GEMS request is generally received by the grpc-delegator, the instance_config.json file is used to determine which host the request should be forwarded over gRPC to. In the DevEnv, the configuration is trivial, as each request is forwarded to gw-slurm-head. In the Swarm, the configuration is more complex, as the requests may be forwarded to the swarm's gw-slurm-head, or other SLURM-capable "cluster hosts" such as thoreau or harper.

# instance_config.json.example

> grpc-default is ignored as a SLURM host, it's just auxilary. routes and subhosts are currently documentation only.


The below is for reference only. The actual instance_config.json file is located in your $GEMSHOME directory. A working example exists in this documentation directory.

Please see [setup_instance.md](setup_instance.md) for more information on setting up your instance_config.json file.

```json
{
  "hosts": {
    "grpc-default": {
      "contexts": [
        "DevEnv"
      ],
      "host": "gw-grpc-delegator",
      "routes": [
        "swarm",
        "thoreau",
        "harper"
      ]
    },
    // named host
    "swarm": {
      "contexts": [
        "Swarm",
        "DevEnv",
        "FreeTier",
        "ShortJob",
        "Sequence-Build3DStructure"
        // If you want to run mdaas on DevEnv without thoreau access, define this: (And make sure to add a comma to the end of the line above)
        // "MDaaS-RunMD"
      ],
      // slurm addr == host:slurmport
      "host": "gw-slurm-head",
      "slurmport": "50052"
    },
    "thoreau": {
      "contexts": [
        "Swarm",
        "PaidTier",
        "MediumJob",
        "LongJob",
        // specifically, a cluster host for MDaaS-RunMD
        "MDaaS-RunMD"
      ],
      "host": "thoreau", // or the ip address
      "slurmport": "50052", // This is a gRPC-mediated port for sending GEMS requests to the SLURM host.
      // SLURM runscripts will use these arguments
      "sbatch_arguments": {
        "MDaaS-RunMD": {
          "partition": "defq",
          "time": "120",
          "nodes": "1",
          "gres": "gpu:1"
        }
      }
    },
    "harper": {
      "contexts": [
        "Swarm",
        "FreeTier",
        "PaidTier",
        "MediumJob",
        "LongJob",
        // Our cluster host for Glycomimetics
        "Glycomimetics"
      ],
      "host": "harper", // or the ip address
      "slurmport": "50052"
    }
  },
  // When no context-specific sbatch_arguments are found, use these defaults.
  "default_sbatch_arguments": {
    // default for DevEnv context
    "DevEnv": {
      "partition": "amber",
      "time": "120",
      "nodes": "4"
    },
    // When no Default for a context is found but default is requested
    "Default": {
      "partition": "amber",
      "time": "120",
      "nodes": "4"
    }
  },
  "filesystem_paths": {
    "MDaaS-RunMD": "/website/userdata/mmservice/md",
    "Glycomimetics": "/website/userdata/complex/gm"
  }
}
```
