# About

the instance_config.json is currently used to configure the hosts that GEMs can connect to with SLURM.

## code usage
Please see `gemsModules/systemoperations/instance_config` for a Python InstanceConfig class which provides helpers for reading the instance_config.json file.

Curently, the only request routed using this feature is "RunMD" which is used to batch MD simulations through SLURM to amber MD nodes.

# instance_config.json.example


> grpc-default is ignored as a SLURM host, it's just auxilary. routes and subhosts are currently documentation only.


The below is for reference only, please use the provided `instance_config.json.example` in the $GEMSHOME root. The `instance_config.json.wip` file is a blueprint/work in progress. 

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
        "MDaaS-RunMD"
      ],
      // A DevEnv situation might still want to use thoreau for MDaaS-RunMD because it's slightly different from swarm.
      // One could create an ssh reverse tunnel and set the host to localhost, for example.
      "host": "thoreau",
      "slurmport": "50052",
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
        "Glycomimetics"
      ],
      "host": "harper",
      "slurmport": "50052"
    }
  },
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
  }
}
```
