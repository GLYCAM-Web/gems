import json
import os

from gemsModules.systemoperations.environment_ops import is_GEMS_test_workflow
from gemsModules.logging.logger import Set_Up_Logging

from ...amber_receive import manageIncomingString


log = Set_Up_Logging(__name__)


def make_input(pUUID: str, projectDir: str, sbatch = False):
    # TODO: update with correct AntibodyDocking configuration
    amberSubmissionJson = json.dumps(
        {
            "molecularSystemType": "Solvated System",
            "molecularModelingJobType": "",
            "jobID": pUUID,
            "localWorkingDirectory": str(projectDir),
            "submissionName": f"ad-{pUUID}",
            "context": "AntibodyDocking",
            "simulationWorkingDirectory": str(projectDir),
            "dontSbatch": not sbatch,
            "comment": "initiated by gemsModules/complex/AntibodyDocking",
        }
##  The following are not set or used anywhere in the code. Tagging for deletion.
#            "simulationControlScriptPath": "\n".join(control_lines),
#            "simulationControlScriptArguments": " ".join(control_args) if control_args else None,
##  This def is not needed if they are removed.
#   def make_input(pUUID: str, projectDir: str, control_lines: str, control_args: list = None, sbatch = False):
    )
    return amberSubmissionJson


# TODO: AD control script
##  This def is not needed.
#   def execute(pUUID: str, projectDir: str, control_lines: list[str], control_args: list = None, sbatch = False):
def execute(pUUID: str, projectDir: str, sbatch = False):
    the_input = make_input(
        pUUID=pUUID, projectDir=projectDir, sbatch=sbatch
    )
    log.debug("The remote submission for AntibodyDocking is:\n%s", the_input)

    # TODO: Delegate this instead of directly calling manageIncomingString.
    manageIncomingString(the_input)
