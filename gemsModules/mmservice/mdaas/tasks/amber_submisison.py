import os
from gemsModules.mmservice.mdaas_amber.amber import manageIncomingString



def make_input(pUUID : str, outputDirPath : str, control_script : str):
    simulationControlScriptPath=os.path.join(outputDirPath,control_script)
    amberSubmissionJson = '{ \
    "molecularSystemType":"Solvated System", \
    "molecularModelingJobType":"Roe Protocol", \
    "jobID":"' + pUUID + '", \
    "localWorkingDirectory":"' + outputDirPath + '", \
    "simulationControlScriptPath":"' + simulationControlScriptPath + '", \
    "comment":"initiated by gemsModules/mmservice/mdaas"\
    }'
    return amberSubmissionJson


def execute(pUUID : str, outputDirPath: str, control_script : str = "Run_Protocol.bash"):
    the_input=make_input(pUUID=pUUID, outputDirPath=outputDirPath, control_script=control_script)
    log.debug("The amber submission from mdaas is: ")
    log.debug(the_input)
    manageIncomingString(the_input)



def testme():
    this_input=make_input(pUUID="1234567890", outputDirPath="this_is_a_path", control_script="this_is_a_script")
    print(this_input)



if __name__== "__main__":
    project=testme()

