#!/usr/bin/env python3

from gemsModules.mmservice.mdaas.tasks import create_slurm_submission

from gemsModules.networkconnections.grpc import slurm_grpc_submit, RpcError

from gemsModules.systemoperations.instance_ops import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


# TODO: This is deeply coupled with systemoperations.instance_ops.InstanceConfig / instance_config.json
def create_contextual_slurm_submission_script(
    context, slurm_runscript_path, SlurmJobInfo
):
    ic = InstanceConfig()
    ic_args = ic.get_sbatch_arguments(context=context)

    thisSlurmJobInfo = SlurmJobInfo.incoming_dict

    # TODO: One day, different slurm submission will need to be made.
    # TODO: Update job info keys so that we can just dict unpack/update. RN this is a compatibility patch.
    thisSlurmJobInfo["nodes"] = ic_args["nodes"]
    thisSlurmJobInfo["time"] = ic_args["time"]
    thisSlurmJobInfo["partition"] = ic_args["partition"]
    # Default is okay for now:
    # thisSlurmJobInfo["sbatchArgument"] = ic_args["sbatchArgument"]

    if hasattr(ic_args, "tasks-per_node"):
        thisSlurmJobInfo["tasks-per-node"] = ic_args["tasks-per-node"]
    else:
        thisSlurmJobInfo["tasks-per-node"] = "1"

    if hasattr(ic_args, "gres"):
        thisSlurmJobInfo["gres"] = ic_args["gres"]
    else:
        thisSlurmJobInfo["gres"] = None
    log.debug(f"Filled SLURM Job info with sbatch_arguments from: %s", ic_args)

    create_slurm_submission.execute(slurm_runscript_path, SlurmJobInfo)


def seek_correct_host(jsonObjectString, context):
    """Using gRPC."""
    addresses = InstanceConfig().get_possible_hosts_for_context(
        context, with_slurmport=True
    )

    failed = False
    tried = []
    response = None
    while len(addresses):
        h, p = addresses.pop().split(":")
        try:
            response = slurm_grpc_submit(jsonObjectString, host=h, port=p)
            failed = False
            break
        except RpcError:
            failed = True
            log.warning(
                "Failed to submit to %s:%s. Trying next host in list.",
                h,
                p,
                exc_info=True,
            )
        finally:
            tried.append(h)

    if failed:
        # maybe should be error?
        log.warning(
            "All attempts to make a SLURM submission over gRPC failed. servers tried: %s",
            tried,
        )

    return response
