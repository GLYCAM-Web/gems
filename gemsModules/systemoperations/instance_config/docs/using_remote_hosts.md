
# In the DevEnv

In order to use a remote host configured in your instance configuration, you need to ensure the remote host's GEMS is also configured correctly to identify itself and a gRPC server wrapping GEMS is running. 

## Configuring the Remote Host

```bash
'$GEMSHOME/bin/setup-instance.py' --config REMOTE_\<HOST\>_preconfig-git-ignore-me.json
```

## Starting the gRPC Server

```bash
#!/usr/bin/env bash

# Ensure The correct GEMSHOME is in your Python path.
PYTHONPATH="${GEMSHOME}:${PYTHONPATH}"

#GEMS_LOGGING_LEVEL="debug" GEMS_DEBUG_VERBOSITY=1 \
#GEMS_GRPC_SLURM_PORT=12345 \
python3 $GEMSHOME/gRPC/SLURM/gems_grpc_slurm_server.py
```

> Currently one must manually grab the GEMS_GRPC_SLURM_PORT from the REMOTE_HOST_preconfig-git-ignore-me.json.



