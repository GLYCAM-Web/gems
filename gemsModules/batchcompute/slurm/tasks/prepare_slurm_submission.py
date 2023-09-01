#!/usr/bin/env python3

from gemsModules.mmservice.mdaas.tasks import create_slurm_submission

from gemsModules.networkconnections.grpc import slurm_grpc_submit, RpcError

from gemsModules.systemoperations.instance_ops import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


def create_contextual_slurm_submission_script(
    context, slurm_runscript_path, thisSlurmJobInfo
):
    ic = InstanceConfig()
    args = ic.get_sbatch_args(context=context)

    # TODO: One day, different slurm submission will need to be made.
    # TODO: Update job info keys so that we can just dict unpack/update. RN this is a compatibility patch.
    thisSlurmJobInfo["workingDirectory"] = args["chdir"]
    thisSlurmJobInfo["name"] = args["job-name"]
    thisSlurmJobInfo["nodes"] = args["nodes"]
    thisSlurmJobInfo["time"] = args["time"]
    thisSlurmJobInfo["partition"] = args["partition"]
    thisSlurmJobInfo["sbatchArgument"] = args["sbatchArgument"]
    thisSlurmJobInfo["tasks-per-node"] = args["tasks-per-node"]
    if hasattr(args, "gres"):
        thisSlurmJobInfo["gres"] = args["gres"]
    else:
        thisSlurmJobInfo["gres"] = None
    log.debug(f"Filled SLURM Job info with sbatch_arguments from: %s", args)

    create_slurm_submission.execute(slurm_runscript_path, thisSlurmJobInfo)


def seek_correct_host(jsonObjectString, context):
    """Using gRPC."""
    addresses = InstanceConfig().get_possible_hosts_for_context(
        context, with_slurmport=True
    )
    # just using first host for now, we could try slurm_grpc_submit, and if it fails, go down the list
    host, port = addresses[0].split(":")

    failed = False
    tried = []
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

    if response is None:
        log.error("Got none response")

    return response
