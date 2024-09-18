""" This file is used by the batchcompute/slurm module to generate an entity-appropriate submission script. """
import json
import os
import traceback
from gemsModules.systemoperations.environment_ops import is_GEMS_test_workflow
from gemsModules.systemoperations.instance_config import InstanceConfig
from gemsModules.systemoperations import filesystem_ops
# from .calculate_time_est_from_parm7 import parse_amber_parm7_pointers

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)

# In the case of complex/glycomimetics, this merely wraps the main control script.
def make_slurm_submission_script(SlurmJobDict):
    log.debug("SlurmJobDict: " + str(SlurmJobDict))
    script = (
        "#!/bin/bash\n"
        f"#SBATCH --chdir={SlurmJobDict['workingDirectory']}\n"
        f"#SBATCH --error=slurm_%x-%A.err\n"
        f"#SBATCH --output=slurm_%x-%A.out\n"
        f"#SBATCH --get-user-env\n"
        f"#SBATCH --job-name={SlurmJobDict['name']}\n"
        f"#SBATCH --nodes={SlurmJobDict['nodes']}\n"
        f"#SBATCH --partition={SlurmJobDict['partition']}\n"
        f"#SBATCH --time={SlurmJobDict['time']}\n"
    )

    # Not setting these may be desirable, so they are optional entries in the instance_config.
    if "tasks-per-node" in SlurmJobDict:
        script += f"#SBATCH --tasks-per-node={SlurmJobDict['tasks-per-node']}\n"
    if "cpus-per-task" in SlurmJobDict:
        script += f"#SBATCH --cpus-per-task={SlurmJobDict['cpus-per-task']}\n"

    if SlurmJobDict["use_gpu"]:
        script += f"#SBATCH --gres={SlurmJobDict['gres']}\n"

    script += "\n"

    if is_GEMS_test_workflow():
        # TODO: New env flag; should we be using MDUtils for Glycomimetics?
        script += "export MDUtilsTestRunWorkflow=Yes\n\n"

    # This argument is set to the script we want slurm to execute.
    script += SlurmJobDict["sbatchArgument"] + f" {SlurmJobDict['mainScriptArguments']}\n"
    log.debug("Our slurm submission script is:\n" + script + "\n")

    return script


def update_local_parameters_file(SlurmJobDict):
    # TODO: Fix? Hacked?
    # We need to update Local_Run_Parameters.bash as it was copied by gemsModules/mmservice/amber before we were local.
    local_param_file = os.path.join(
        SlurmJobDict["workingDirectory"], "Local_Run_Parameters.bash"
    )
    if not os.path.exists(local_param_file):
        log.info("Local_Run_Parameters.bash does not exist. Skipping update.")
        return

    # update MPI/CUDA settings if using GPU.
    if SlurmJobDict["use_gpu"]:
        filesystem_ops.replace_bash_variable_in_file(
            local_param_file, {"useMpi": "N", "useCuda": "Y"}
        )

    # lets replace all local parameters configured from the instance config. For example, "numProcs".
    ic = InstanceConfig()
    args = ic.get_keyed_arguments("local_parameters", context=SlurmJobDict["context"])
    filesystem_ops.replace_bash_variable_in_file(local_param_file, args)


def update_slurm_job(SlurmJobDict):
    # amber_input_file = os.path.join(SlurmJobDict["workingDirectory"], "MdInput.parm7")

    # could be part of a "update_slurm_job" task.
    # gpu toggle must update both local params and slurm script.
    wants_gpu = False
    if "gres" in SlurmJobDict:
        wants_gpu = SlurmJobDict["gres"] is not None

    # Note: This was part of a CPU selection fix to handle Amber's small box problem on GPU.
    # with open(amber_input_file, r) as f:
    #     will_use_gpu = parse_amber_parm7_pointers(f) > 3

    if wants_gpu:  # and will_use_gpu:
        SlurmJobDict["use_gpu"] = True
    else:
        SlurmJobDict["use_gpu"] = False
    log.debug(f"wants_gpu=%s", wants_gpu)


def execute(SlurmJobDict):
    path = SlurmJobDict["slurm_runscript_name"]

    update_slurm_job(SlurmJobDict)
    update_local_parameters_file(SlurmJobDict)

    script = make_slurm_submission_script(SlurmJobDict)

    try:
        with open(path, "w") as f:
            f.write(script)
            log.debug("Wrote slurm submission script to: " + path)
    except Exception as error:
        log.error("Cannnot write slurm run script. Aborting")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc())
        raise error
