# About

the instance_config.json is currently used to configure the hosts that GEMs can connect to with SLURM.

## code usage
Please see `gemsModules/systemoperations/instance_ops.py` for a Python InstanceConfig class which provides helpers for reading the instance_config.json file.

Curently, the only request routed using this feature is "RunMD" which is used to batch MD simulations through SLURM to amber MD nodes.

# instance_config.json.example

For now, grpc-default is ignored as a SLURM host, and routes are documentation only.
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
    "swarm": {
      "contexts": [
        "Swarm",
        "DevEnv",
        "FreeTier",
        "ShortJob",
        "Sequence-Build3DStructure"
        // If you want to run mdaas on DevEnv without thoreau access, define this:
        // "MDaaS-RunMD"
      ],
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
      "host": "thoreau",
      "slurmport": "50052",
      "sbatch_arguments": {
        "MDaaS-RunMD": {
          "partition": "defq",
          "time": "120",
          "job-name": "md-{{pUUID}}",
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
    "DevEnv": {
      "partition": "defq",
      "time": "120",
      "job-name": "none-{{pUUID}}",
      "nodes": "4"
    },
    "Default": {
      "partition": "defq",
      "time": "120",
      "job-name": "none-{{pUUID}}{{time}}",
      "nodes": "4"
    }
  }
}
```