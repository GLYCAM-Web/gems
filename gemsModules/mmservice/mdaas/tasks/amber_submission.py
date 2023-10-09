import json
import os

from gemsModules.systemoperations.environment_ops import is_GEMS_test_workflow
from gemsModules.mmservice.mdaas_amber.amber import manageIncomingString
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def make_input(pUUID: str, outputDirPath: str, control_script: str):
    outputDirPath = os.path.join(outputDirPath, pUUID)
    # simulationControlScriptPath = os.path.join(outputDirPath, control_script)

    amberSubmissionJson = json.dumps(
        {
            "molecularSystemType": "Solvated System",
            "molecularModelingJobType": "Roe Protocol",
            "jobID": pUUID,
            "localWorkingDirectory": outputDirPath,
            "submissionName": f"md-{pUUID}",
            "context": "MDaaS-RunMD",
            "simulationControlScriptPath": control_script,
            "simulationWorkingDirectory": outputDirPath,
            "comment": "initiated by gemsModules/mmservice/mdaas",
        }
    )
    return amberSubmissionJson


def execute(pUUID: str, outputDirPath: str, control_script: str = "Run_Protocol.bash"):
    the_input = make_input(
        pUUID=pUUID, outputDirPath=outputDirPath, control_script=control_script
    )
    log.debug("The amber submission from mdaas is:\n%s", the_input)
    manageIncomingString(the_input)
