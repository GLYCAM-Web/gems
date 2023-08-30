import json
import os
import traceback
from gemsModules.systemoperations.environment_ops import is_GEMS_test_workflow

from gemsModules.mmservice.mdaas_amber.amber import manageIncomingString

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def make_slurm_submission_script(SlurmJobInfo):
    # script.write("#!/bin/bash" + "\n")
    # script.write("#SBATCH --chdir=" + incoming_dict["workingDirectory"] + "\n")
    # script.write("#SBATCH --error=slurm_%x-%A.err" + "\n")
    # script.write("#SBATCH --get-user-env" + "\n")
    # script.write("#SBATCH --job-name=" + incoming_dict["name"] + "\n")
    # script.write("#SBATCH --nodes=1" + "\n")
    # script.write("#SBATCH --output=slurm_%x-%A.out" + "\n")
    # script.write("#SBATCH --partition=" + incoming_dict["partition"] + "\n")
    # script.write("#SBATCH --tasks-per-node=4\n\n")
    # using fstrings and building up the string before writing
    script = (
        "#!/bin/bash\n"
        f"#SBATCH --chdir={SlurmJobInfo['workingDirectory']}\n"
        f"#SBATCH --error=slurm_%x-%A.err\n"
        f"#SBATCH --get-user-env\n"
        f"#SBATCH --job-name={SlurmJobInfo['name']}\n"
        f"#SBATCH --nodes=1\n"
        f"#SBATCH --output=slurm_%x-%A.out\n"
        f"#SBATCH --partition={SlurmJobInfo['partition']}\n"
        f"#SBATCH --tasks-per-node=4\n\n"
    )

    if is_GEMS_test_workflow():
        log.debug("setting testing workflow to yes")
        script += "export MDUtilsTestRunWorkflow=Yes\n\n"
    else:
        log.debug("NOT setting testing workflow to yes")
    log.debug("The sbatchArgument is : " + SlurmJobInfo["sbatchArgument"])
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

    script.write(make_slurm_submission_script(script, incoming_dict))
