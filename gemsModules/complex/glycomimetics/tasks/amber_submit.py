import json
import os

from gemsModules.systemoperations.environment_ops import is_GEMS_test_workflow
from gemsModules.logging.logger import Set_Up_Logging

from ...amber_receive import manageIncomingString


log = Set_Up_Logging(__name__)


def make_input(pUUID: str, projectDir: str, control_script: str, control_args: list = None):
    # TODO: update with correct glycomimetics configuration
    amberSubmissionJson = json.dumps(
        {
            "molecularSystemType": "Solvated System",
            "molecularModelingJobType": "Roe Protocol",
            "jobID": pUUID,
            "localWorkingDirectory": projectDir,
            "submissionName": f"gm-{pUUID}",
            "context": "Glycomimetics",
            "simulationControlScriptPath": control_script,
            "simulationControlScriptArguments": control_args,
            "simulationWorkingDirectory": projectDir,
            "comment": "initiated by gemsModules/complex/glycomimetics",
        }
    )
    return amberSubmissionJson


def execute(pUUID: str, projectDir: str, control_script: str = "scripts/00.RUN_ALL.sh", control_args: list = None):
    the_input = make_input(
        pUUID=pUUID, projectDir=projectDir, control_script=control_script, control_args=control_args
    )
    log.debug("The amber submission from glycomimetics is:\n%s", the_input)

    # TODO: Delegate this instead of directly calling manageIncomingString.
    manageIncomingString(the_input)
