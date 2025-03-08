import json
import os

from gemsModules.systemoperations.environment_ops import is_GEMS_test_workflow
from gemsModules.logging.logger import Set_Up_Logging

from ...amber_receive import manageIncomingString


log = Set_Up_Logging(__name__)


def make_input(pUUID: str, projectDir: str, control_lines: str, control_args: list = None, sbatch = False):
    # TODO: update with correct AntibodyDocking configuration
    amberSubmissionJson = json.dumps(
        {
            "molecularSystemType": "Solvated System",
            "molecularModelingJobType": "",
            "jobID": pUUID,
            "localWorkingDirectory": str(projectDir),
            "submissionName": f"ad-{pUUID}",
            "context": "AntibodyDocking",
            "simulationControlScriptPath": "\n".join(control_lines),
            "simulationControlScriptArguments": " ".join(control_args) if control_args else None,
            "simulationWorkingDirectory": str(projectDir),
            "dontSbatch": not sbatch,
            "comment": "initiated by gemsModules/complex/AntibodyDocking",
        }
    )
    return amberSubmissionJson


# TODO: AD control script
def execute(pUUID: str, projectDir: str, control_lines: list[str], control_args: list = None, sbatch = False):
    the_input = make_input(
        pUUID=pUUID, projectDir=projectDir, control_lines=control_lines, control_args=control_args, sbatch=sbatch
    )
    log.debug("The remote submission for AntibodyDocking is:\n%s", the_input)

    # TODO: Delegate this instead of directly calling manageIncomingString.
    manageIncomingString(the_input)
