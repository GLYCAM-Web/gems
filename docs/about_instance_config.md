# About

the instance_config.json is currently used to configure the hosts that GEMs can connect to with SLURM.

## code usage
Please see `gemsModules/systemoperations/instance_ops.py` for a Python InstanceConfig class which provides helpers for reading the instance_config.json file.

Curently, the only request routed using this feature is "RunMD" which is used to batch MD simulations through SLURM to amber MD nodes.

# instance_config.json.example

For now, grpc-default is ignored as a SLURM host, and routes are documentation only.
```json
{
  "hosts": [
    {
      "name": "grpc-default",
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
    {
      "name": "swarm",
      "contexts": [
        "Swarm",
        "DevEnv",
        "FreeTier",
        "ShortJob",
        // Currently, if one tries to run RunMD, it will only run on thoreau. If you want to run on slurm-head, because for instance you do not have access to thoreau, you must define it here.  
        // "MDaaS-RunMD",
        "Sequence-Build3DStructure"
      ],
      "host": "gw-slurm-head",
      "slurmport": "50052"
    },
    {
      "name": "thoreau",
      "contexts": [
        "Swarm",
        "PaidTier",
        "MediumJob",
        "LongJob",
        "MDaaS-RunMD"
      ],
      "host": "thoreau",
      "slurmport": "50052"
    },
    {
      "name": "harper",
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
  ]
}```