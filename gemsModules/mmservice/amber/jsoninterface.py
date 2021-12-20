#!/usr/bin/env python3
import  os, sys, subprocess, warnings
import json, re
from pathlib import Path
from datetime import datetime
#from gemsModules.common.services import *  # prefer to use common.logic
import gemsModules.common.logic as commonLogic
from pydantic import BaseModel, Field, ValidationError, validator
from pydantic.schema import schema
from gemsModules.common.loggingConfig import *
import traceback

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

##  @brief Information relevant to AMBER projects
#   @detail The data needed to ensure the right scripts are applied.
class amberProject(BaseModel):

    protocolSource : str = Field(
        'MD_Utils',
        title = 'Protocol Source',
        description = 'The name of the source for this protocol.'
        )
    protocolSourceLocation : str = Field(
        None,
        title = 'Protocol Source Location',
        description = 'The path to the source for this protocol.'
        )
    protocolSourceOrigin : str = Field(
        "https://github.com/GLYCAM-Web/MD_Utils.git",
        title = 'Protocol Source Location',
        description = 'The path to the source for this protocol.'
        )
    protocolSourceVersion : str = Field(
        None,
        title = 'Protocol Source Version',
        description = 'Version designation for the source for this protocol.'
        )
    protocolSourceBranch : str = Field(
        None,
        title = 'Protocol Source Branch',
        description = 'Git repository branch for the source for this protocol.'
        )
    protocolSourceHash : str = Field(
        None,
        title = 'Protocol Source Hash',
        description = 'Git repository hash for the source for this protocol.'
        )
    protocolDirectory : str = Field(
        None,
        title = 'Protocol Directory',
        description = 'The directory containing the files require to execute this protocol.'
        )
    protocolRequiredInputFiles : List[str] = Field(
        None,
        title = "Required Input Files",
        description = "List of input files required for this protocol"
        )
    protocolControlScriptName : str = Field(
        None,
        title = "Control Script Name",
        description = "Name of the control script for this protocol - Name ONLY, not path."
        )
    molecularSystemType : str = Field(
        'Glycan',
        title = 'Molecular System Type',
        description = 'The type of molecular system being modeled.'
        )
    molecularModelingJobType : str = Field(
        'Prep_and_Minimization',
        title = 'Molecular Modeling Job Type',
        description = 'The type of molecular modeling to perform.'
        )
    jobID : str = Field(
        "amberJob",
        title = "The Job's ID",
        description = "Generally, this is the pUUID.  Must be valid as a directory name."
        )
    localWorkingDirectory : str = Field(
        None,
        title = "Working Directory",
        description = "The directory where the files should be placed now."
        )
    simulationWorkingDirectory : str = Field(
        None,
        title = "Working Directory",
        description = "The directory on the machine/cluster where the modeling job will occur."
        )
    simulationControlScriptPath : str = Field(
        None,
        title = "Control Script Path",
        description = "The full path to the control script for this protocol"
        )
    thisProjectLog : str = Field(
        None,
        title = "GEMS AMBER Project Log",
        description = "The log for the GEMS portion of generating an AMBER job."
        )
    thisProjectJson : str = Field(
        None,
        title = "GEMS-AMBER Project JSON object",
        description = "The full JSON object that generated this GEMS-AMBER project."
        )
    submissionName : str = Field(
        None,
        title = "GEMS-AMBER Project JSON object",
        description = "The full JSON object that generated this GEMS-AMBER project."
        )
    comment : str = Field(
        None,
        title = "Comment",
        description = "Free-form comment string."
        )

    def initialize(self):
        log.info("mmservice/amber/io.py amberProject initialize was called")
        try : 
            gemshome : str = getGemsHome()
        except :
            log.error("Could not get GEMSHOME")
            raise
        if self.protocolSourceLocation is None : 
            self.protocolSourceLocation = gemshome + '/External/MD_Utils'
        log.debug("self.protocolSourceLocation is : " + self.protocolSourceLocation)
        log.debug("AANNNNNDDDD.... I get to here.....")
        try : 
            log.debug("0th - localWorkingDirectory is : " + self.localWorkingDirectory)
        except :
            log.debug("could not write the localWorkingDirectory")
            raise
        if self.localWorkingDirectory is None : 
            self.localWorkingDirectory = gemshome + "/UserSpace/amberJob"
        log.debug("1st - localWorkingDirectory is : " + self.localWorkingDirectory)
        if self.thisProjectLog is None : 
            self.thisProjectLog = gemshome + "/UserSpace/amberJob/gemsAmberProject.log"
        if self.thisProjectJson is None : 
            self.thisProjectJson = gemshome + "/UserSpace/amberJob/gemsAmberProject.json"

        # Check that the protocolSourceLocation is a directory.
        if os.path.isdir(self.protocolSourceLocation) == False :
            raise FileNotFoundError(self.protocolSourceLocation)

        # Ensure that the localWorkingDirectory exists.
        # Later we will check for required input files.
        if not Path(self.localWorkingDirectory).is_dir() :
            raise FileNotFoundError(self.localWorkingDirectory)

        # Check that the protocolSourceLocation is probably a git repo
        if os.path.isdir(self.protocolSourceLocation + '/.git') == False :
            warnings.warn(self.protocolSourceLocation + ' is not a git repo')

        # If it appears to be one, grab the branch and hash
        else :
            command = "cd " + self.protocolSourceLocation + " && git branch | sed -n -e 's/^\* \(.*\)/\\1/p'"
            p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            self.protocolSourceBranch=output.decode().rstrip()
            command = "cd " + self.protocolSourceLocation + " && git rev-parse HEAD"
            p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            self.protocolSourceHash = output.decode().rstrip()

        # If protocolDirectory does not already exist, generate the path name.
        # Note : These utilities assume that the protocols are in specific 
        # directory paths relative to protocolSourceLocation.  
        if self.protocolDirectory == None :
            self.protocolDirectory = self.protocolSourceLocation + \
                '/protocols/' + \
                self.molecularSystemType + \
                '/' + self.molecularModelingJobType
        if not Path(self.protocolDirectory).is_dir() :
            raise FileNotFoundError(self.protocolDirectory)

        # Read README.md to get the list of required input files
        pattern1 = "Required input:  "
        pattern2 = "Control script:  "
        try :
            file = open(self.protocolDirectory + "/README.md", "r") 
        except OSError :
            log.error("Cannot open file for reading:  " + self.protocolDirectory + "/README.md") 
            raise 
        for line in file:
            if re.search(pattern1, line):
                self.protocolRequiredInputFiles=line.strip(pattern1).rstrip().split(' ')
            if re.search(pattern2, line):
                self.protocolControlScriptName=line.strip(pattern2).rstrip()

        # Check that the required input files are present in the localWorkingDirectory
        for infile in  self.protocolRequiredInputFiles :
            if not Path(self.localWorkingDirectory + "/" + infile).is_file() :
                raise FileNotFoundError("Required Input File:  " + self.localWorkingDirectory + "/" + infile)

        # Check that the control script is present in the protocolDirectory or the full path
        if not Path(self.protocolDirectory + "/" + self.protocolControlScriptName).is_file() :
            raise FileNotFoundError("Control script:  " + self.protocolDirectory + "/" + self.protocolControlScriptName)


        # Lachele:  TODO - make this neater as I'm sure Python can do
        # Set the jobname to be displayed by queueing systems
        if self.submissionName is None :
            lmax1=9
            lmax2=9
            if len(self.molecularSystemType) > lmax1 :
                len1 = lmax1
            else :
                len1 =  len(self.molecularSystemType)
            if len(self.jobID) > lmax2 :
                len2 = lmax2
            else :
                len2 =  len(self.jobID)
            self.submissionName = self.molecularSystemType[0:len1] + '-' + self.jobID[0:len2]


        # Open the log file and ensure it can be written
        self.thisProjectLog = self.localWorkingDirectory +  "/gemsAmberProject.log"
        log.debug("2nd - localWorkingDirectory is : " + self.localWorkingDirectory)
        try : 
            file = open(self.thisProjectLog, "w") 
        except OSError :
            log.error("Cannot open file for writing:  " + self.thisProjectLog) 
            raise 
        file.write("GEMS AMBER project : " + self.jobID + "\ninitialized on " + datetime.now().strftime("%c") + "\n")
        file.close()

        # If the simulationWorkingDirectory is not specified, guess its name and issue a warning.
        log.debug("1st - simulationWorkingDirectory is : " + self.localWorkingDirectory)
        if self.simulationWorkingDirectory is None :
            self.simulationWorkingDirectory = self.localWorkingDirectory
            with open(self.thisProjectLog, "a") as f:
                f.write("WARNING:  setting the simulation WD equal to the local WD\n")
        log.debug("2nd - simulationWorkingDirectory is : " + self.localWorkingDirectory)
        # Set the name of the control script in the simulation environment, if not already set
        if self.simulationControlScriptPath is None : 
            self.simulationControlScriptPath = self.simulationWorkingDirectory + "/" + self.protocolControlScriptName
        log.debug("3rd - localWorkingDirectory is : " + self.localWorkingDirectory)


        # Dump this object to a file in localWorkingDirectory
        self.thisProjectJson = self.localWorkingDirectory +  "/gemsAmberProject.json"
        try : 
            file = open(self.thisProjectJson, "w") 
        except OSError :
            log.error("Cannot open file for writing:  " + self.thisProjectJson) 
            raise 
        file.write(self.json(indent=2) + "\n")
        file.close()
        with open(self.thisProjectLog, "a") as f:
            f.write("The JSON object file has been written to the localWorkingDirectory\n")


    @validator('protocolSourceLocation')
    def directory_must_exist(cls, v):
        if os.path.isdir(v) == False :
            raise FileNotFoundError(self.protocolSourceLocation)
        return v.title()

    def copy_protocol_files(self) :
        import glob
        import shutil
        dest_dir = self.localWorkingDirectory
        try :
            for file in glob.glob(self.protocolDirectory + '/*'):
                log.debug(file)
                shutil.copy(file, dest_dir)
        except :
            log.error("Unable to copy files from protocolDirectory to localWorkingDirectory")
            raise
        try : 
            file = open(self.thisProjectLog, "a") 
        except OSError :
            log.error("Cannot open file for writing:  " + self.thisProjectLog) 
            raise 
        file.write("The project files have been copied from the protocolDirectory to the localWorkingDirectory\n")
        file.close()



def troubleshoot() :

    print("Testing the amberProject!")
    try :
        amber_project = amberProject ()
        amber_project.initialize()
    except ValidationError as e :
        print(e)
    print("The protocols are here:  " + amber_project.protocolSourceLocation)
    print("The name of the protocol set is:  " + amber_project.protocolSource)
    print("Here is the git branch:  " + amber_project.protocolSourceBranch)
    print("Here is the git hash:  " + amber_project.protocolSourceHash)
    print("The molecular system type is:  " + amber_project.molecularSystemType)
    print("The molecular modeling job type is:  " + amber_project.molecularModelingJobType)
    print("Required Inputs:  " + str(amber_project.protocolRequiredInputFiles))
    print("Control Script:  " + amber_project.protocolControlScriptName)

    amber_project.copy_protocol_files()


def generateSchema():
    import json
    print(amberProject.schema_json(indent=2))

if __name__ == "__main__":
  generateSchema()
  # Uncomment the next line to get some troubleshooting output on the command line
  #troubleshoot()

