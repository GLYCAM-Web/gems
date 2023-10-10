import json
import os
import traceback
from gemsModules.systemoperations.environment_ops import is_GEMS_test_workflow
from gemsModules.systemoperations.instance_ops import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


# This might be generalized, but for now it expects to only be triggered by MDaaS as a task of mdaas.
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
        f"#SBATCH --tasks-per-node={SlurmJobDict['tasks-per-node']}\n\n"
    )

    if SlurmJobDict["gres"] is not None:
        script += f"#SBATCH --gres={SlurmJobDict['gres']}\n"

    if is_GEMS_test_workflow():
        log.debug("setting testing workflow to yes")
        script += "export MDUtilsTestRunWorkflow=Yes\n\n"
    else:
        log.debug("NOT setting testing workflow to yes")
    log.debug("The sbatchArgument is : " + SlurmJobDict["sbatchArgument"])

    # This argument is set to the script we want slurm to execute.
    script += SlurmJobDict["sbatchArgument"] + "\n"

    return script


def execute(SlurmJobDict):
    path = SlurmJobDict["slurm_runscript_name"]
    try:
        with open(path, "w") as script:
            script.write(make_slurm_submission_script(SlurmJobDict))
            log.debug("Wrote slurm submission script to: " + path)
        # TODO: Fix? Hacked?
        # Also update Local_Run_Parameters.bash as it was copied by gemsModules/mmservice/amber before we were local.
        local_param_file = os.path.join(
            SlurmJobDict["workingDirectory"], "Local_Run_Parameters.bash"
        )
        if SlurmJobDict["gres"] is not None:
            # the job is meant for gpu
            # replace `useMPI='Y'` with `useMPI='N'` and useCUDA='N' with useCUDA='Y'
            with open(local_param_file, "r") as f:
                content = f.read()
                content = content.replace("useMPI='Y'", "useMPI='N'")
                content = content.replace("useCUDA='N'", "useCUDA='Y'")
            with open(local_param_file, "w") as f:
                f.write(content)

    except Exception as error:
        log.error("Cannnot write slurm run script. Aborting")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc())
        raise error
