import json
import os
import traceback
from gemsModules.systemoperations.environment_ops import is_GEMS_test_workflow
from gemsModules.systemoperations.instance_ops import InstanceConfig
from gemsModules.systemoperations import filesystem_ops

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


# TODO: Where should this go? systemoperations seems like the spot until you consider this is an amber specific function. Tasks might be better interpreted as common library utilities for an Entity.
def get_residues_from_parm7(parm7_file) -> int:
    with open(parm7_file, "r") as f:
        for line in f:
            if "FLAG SOLVENT_POINTERS" in line:
                # Skip the next line
                next(f)
                # Read the third line after the matched line
                target_line = next(f).strip()
                return int(target_line.split()[0])
    return 0  # "FLAG SOLVENT_POINTERS" not found in file


def make_slurm_submission_script(SlurmJobDict):
    log.debug("SlurmJobDict: " + str(SlurmJobDict))
    script = (
        "#!/bin/bash\n"
        f"#SBATCH --chdir={SlurmJobDict['workingDirectory']}\n"
        f"#SBATCH --error=slurm_%x-%A.err\n"
        f"#SBATCH --get-user-env\n"
        f"#SBATCH --job-name={SlurmJobDict['name']}\n"
        f"#SBATCH --nodes={SlurmJobDict['nodes']}\n"
        f"#SBATCH --output=slurm_%x-%A.out\n"
        f"#SBATCH --partition={SlurmJobDict['partition']}\n"
        f"#SBATCH --tasks-per-node={SlurmJobDict['tasks-per-node']}\n"
        f"#SBATCH --cpus-per-task={SlurmJobDict['cpus-per-task']}\n"
        f"#SBATCH --time={SlurmJobDict['time']}\n"
    )

    if SlurmJobDict["use_gpu"]:
        script += f"#SBATCH --gres={SlurmJobDict['gres']}\n"
    script += "\n"

    if is_GEMS_test_workflow():
        log.debug("setting testing workflow to yes")
        script += "export MDUtilsTestRunWorkflow=Yes\n\n"
    else:
        log.debug("NOT setting testing workflow to yes")

    # This argument is set to the script we want slurm to execute.
    script += SlurmJobDict["sbatchArgument"] + "\n"
    log.debug("The sbatchArgument is : " + SlurmJobDict["sbatchArgument"])

    return script


def update_local_parameters_file(SlurmJobDict):
    # TODO: Fix? Hacked?
    # We need to update Local_Run_Parameters.bash as it was copied by gemsModules/mmservice/amber before we were local.
    local_param_file = os.path.join(
        SlurmJobDict["workingDirectory"], "Local_Run_Parameters.bash"
    )

    # update MPI/CUDA settings if using GPU.
    if SlurmJobDict["use_gpu"]:
        filesystem_ops.replace_bash_variable_in_file(
            local_param_file, {"useMpi": "N", "useCuda": "Y"}
        )

    # lets replace all local parameters configured from the instance config. For example, "numProcs".
    ic = InstanceConfig()
    args = ic.get_keyed_arguments("local_parameters", context=SlurmJobDict["context"])
    filesystem_ops.replace_bash_variable_in_file(local_param_file, args)


def execute(SlurmJobDict):
    path = SlurmJobDict["slurm_runscript_name"]
    amber_input_file = os.path.join(SlurmJobDict["workingDirectory"], "MdInput.parm7")

    # could be part of a "update_slurm_job" task.
    # gpu toggle must update both local params and slurm script.
    requires_gpu = False
    if "gres" in SlurmJobDict:
        requires_gpu = SlurmJobDict["gres"] is not None

    # can_use_gpu = get_residues_from_parm7(amber_input_file) > 3
    if requires_gpu:  # and can_use_gpu:
        SlurmJobDict["use_gpu"] = True
    else:
        SlurmJobDict["use_gpu"] = False
    log.debug(f"requires_gpu=%s", requires_gpu)

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
