import json
import os
import traceback
from gemsModules.systemoperations.environment_ops import is_GEMS_test_workflow
from gemsModules.systemoperations.instance_ops import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


# This might be generalized, but for now it expects to only be triggered by MDaaS as a task of mdaas.
def make_slurm_submission_script(SlurmJobInfo):
    script = (
        "#!/bin/bash\n"
        f"#SBATCH --chdir={SlurmJobInfo['workingDirectory']}\n"
        f"#SBATCH --error=slurm_%x-%A.err\n"
        f"#SBATCH --get-user-env\n"
        f"#SBATCH --job-name={SlurmJobInfo['name']}\n"
        f"#SBATCH --nodes={SlurmJobInfo['nodes']}\n"
        f"#SBATCH --output=slurm_%x-%A.out\n"
        f"#SBATCH --partition={SlurmJobInfo['partition']}\n"
        f"#SBATCH --tasks-per-node={SlurmJobInfo['tasks-per-node']}\n\n"
    )

    if SlurmJobInfo["gres"] is not None:
        script += f"#SBATCH --gres={SlurmJobInfo['gres']}\n"

    if is_GEMS_test_workflow():
        log.debug("setting testing workflow to yes")
        script += "export MDUtilsTestRunWorkflow=Yes\n\n"
    else:
        log.debug("NOT setting testing workflow to yes")
    log.debug("The sbatchArgument is : " + SlurmJobInfo["sbatchArgument"])

    # This argument is set to the script we want slurm to execute.
    script += f"{SlurmJobInfo['sbatchArgument']}\n"

    return script


def execute(path, thisSlurmJobInfo):
    try:
        script = open(path, "w")
    except Exception as error:
        log.error("Cannnot write slurm run script. Aborting")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc())
        raise error
        # sys.exit(1)

    incoming_dict = thisSlurmJobInfo.incoming_dict

    script.write(make_slurm_submission_script(incoming_dict))
    log.debug("Wrote slurm submission script to: " + path)
