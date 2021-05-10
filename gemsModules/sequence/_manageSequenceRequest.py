#!/usr/bin/env python3
from gemsModules.common.loggingConfig import *
import traceback, os, sys

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

def manageSequenceRequest(self, defaultOnly : bool = False) :
    log.info("manageSequenceRequest was called ")
    from typing import List
    from gemsModules.sequence import structureInfo, projects, logic, build
    from gemsModules.sequence import io as sequenceio
    from gemsModules.project import projectUtilPydantic as projectUtils
    from gemsModules.common import services as commonservices
    startNewProject = False
    if self.transaction_out is None and self.transaction_in is None :
        thisAdditionalInfo={'hint':'Neither the transaction_in nor the transaction_out are populated.'}
        self.generateCommonParserNotice(
                noticeBrief = 'InvalidInput', 
                scope='TransactionWrapper.ManageSeqeunceRequest',
                additionalInfo=thisAdditionalInfo
                )
        raise "Neither the transaction_in nor the transaction_out are populated."
    if self.transaction_out is None :
        self.initialize_transaction_out_from_transaction_in() 
        startNewProject = True
    log.debug("The transaction_out is :   " )
    log.debug(self.transaction_out.json(indent=2))
    ##  If the project dir is not found, a new project is needed
    if self.transaction_out.project is None :
        startNewProject = True
    elif self.transaction_out.project.project_dir is None :
        startNewProject = True
    elif self.transaction_out.project.project_dir is  "" :
        startNewProject = True
    if startNewProject is True :
        log.debug("Starting new project in manageSequenceRequest")
        try :
            log.debug("Attempting to start a new project")
            self.transaction_out.project=projectUtils.startProject(self).copy(deep=True)
            ## This is called in startProject, is this duplicated on purpose?
            self.transaction_out.project.setProjectDir(self, noClobber=True)
        except Exception as error :
            log.error("There was a problem creating a project: " + str(error))
            log.error(traceback.format_exc())
            raise error
        log.debug("Just built a new project.  The transaction_out is :   " )
        log.debug(self.transaction_out.json(indent=2))
    project_dir = self.transaction_out.project.project_dir 
#    log.debug("self.transaction_out.project.project_dir is : >>>" + str(self.transaction_out.project.project_dir) + "<<<")
#    log.debug("startNewProject in manageSequenceRequest is : " + str(startNewProject))
    log.debug("Apparent project directory: " + str(project_dir))
    if commonservices.directoryExists(project_dir) : 
        log.debug("This directory already exists: " + str(project_dir))
    ##  Build structureInfo object
    if self.transaction_out.entity is None :
        log.error("The entity in transaction_out does not exist.")
    if self.transaction_out.entity.outputs is None :
        self.transaction_out.entity.outputs=sequenceio.SequenceOutputs()
    if self.transaction_out.entity.outputs.structureBuildInfo is None :
        self.transaction_out.entity.outputs.structureBuildInfo=sequenceio.StructureBuildInfo()
        log.debug("structureBuildInfo: " + str(self.transaction_out.entity.outputs.structureBuildInfo))
    try:
        thisStructureInfo = structureInfo.buildStructureInfoOliver(self, self.transaction_out.project.pUUID)
        self.transaction_out.entity.outputs.structureBuildInfo= thisStructureInfo
        #thisStructureInfo.buildStates[0].energy=8.8888  # to test change-making
        log.debug("structureInfo: " + thisStructureInfo.json(indent=2))
    except Exception as error:
        log.error("There was a problem building structureInfo: " + str(error))
        log.error(traceback.format_exc())
        raise error
#    log.debug("Just built a thisStructureInfo.  The transaction_out is :   " )
#    log.debug(self.transaction_out.json(indent=2))
    ##  Save some copies of structureInfo for status tracking.
    try:
        ## Determine whether to save or update.
        project_dir = self.transaction_out.project.project_dir 
        filename = project_dir + "logs/structureInfo_request.json"
        log.debug("looking for existing filename: " + filename)
        if os.path.exists(filename):
            log.debug("\n\nstructureInfo_request.json found. Updating both the request and the status file.\n\n")
            structureInfo.updateStructureInfoWithUserOptions(self, thisStructureInfo, filename)
            statusFile = project_dir + "logs/structureInfo_status.json"
            if os.path.exists(statusFile):
                structureInfo.updateStructureInfoWithUserOptions(self, thisStructureInfo, statusFile)
            else:
                ##Create new files for tracking this project.
                structureInfo.saveRequestInfo(thisStructureInfo, project_dir)
        else:
            log.debug("Failed to find structureInfo_request.json at: " + filename)
            # TODO: Maybe we need this? Unsure. Timing isn't right for testing. ~ Dan
            # structureInfo.saveRequestInfo(thisStructureInfo, project_dir)
    except Exception as error:
        log.error("There was a problem saving the request info: " + str(error))
        log.error(traceback.format_exc())
        raise error


    try:
        ## Here we need to setup project folder, create some symLinks etc, before we get into each buildState
        ## Not happy with the organization of this logic. Too much state being passed around and similar code!
        ## Smells like it should be a class and this stuff goes in the initializer. 
        thisProject = self.transaction_out.project
        this_pUUID = projectUtils.getProjectpUUID(thisProject)
        log.debug("this_pUUID is : " + this_pUUID)
        this_sequence = self.getSequenceVariantOut('indexOrdered')
        this_seqID = projectUtils.getSeqIDForSequence(this_sequence)
        buildStrategyID = "buildStrategyID1" # TODO implement getCurrentBuildStrategyID().
        projects.setupInitialSequenceFolders(this_seqID, this_pUUID, buildStrategyID)
        #Can generate the response already:
        for buildState in thisStructureInfo.individualBuildDetails:
            conformerID = buildState.structureDirectoryName
            projects.addResponse(buildState, self, conformerID, buildState.conformerLabel)
        ## Regardless if requesting default or not, I think I need to generate a default. Otherwise I get into madness
        ## with figuring out exist status and which conformerID to use in place of default. Then when a default 
        ## request does come, should it overwrite previous default for old projects?
        ## A default request is always first, this is now implemented in buildStructureInfo
        # Decide if we need to minimize or not and tell everyone if need be
        mdMinimize=True  
        # Check the outgoing transaction to see if it got set
        if self.transaction_out.mdMinimize is False :
            mdMinimize=False
        # Check the incoming transaction, too.
        if self.transaction_in is not None :
            if self.transaction_in.mdMinimize is False :
                mdMinimize=False
                if self.transaction_in.entity.inputs is not None :
                    if self.transaction_in.entity.inputs.buildOptions is not None :
                        self.transaction_in.entity.inputs.buildOptions.mdMinimize = False
        if mdMinimize is False : 
            if self.transaction_out.entity.inputs is None : 
                if self.transaction_in.entity.inputs is not None : 
                    self.transaction_out.entity.inputs = self.transaction_in.entity.inputs 
                else : 
                    self.transaction_out.entity.inputs = sequenceio.SequenceInputs() 
            if self.transaction_out.entity.inputs.buildOptions is None : 
                self.transaction_out.entity.inputs.buildOptions = sequenceio.TheBuildOptions()
            self.transaction_out.entity.inputs.buildOptions.mdMinimize = False
            if self.transaction_out.entity.outputs is None : 
                self.transaction_out.entity.outputs = sequenceio.TheSequencenOutputs()
            if self.transaction_out.entity.outputs.sequenceEvaluationOutput is None : 
                self.transaction_out.entity.outputs.sequenceEvaluationOutput = sequenceio.TheSequenceEvaluationOutput()
            if self.transaction_out.entity.outputs.sequenceEvaluationOutput.buildOptions is None : 
                self.transaction_out.entity.outputs.sequenceEvaluationOutput.buildOptions = sequenceio.TheBuildOptions()
            self.transaction_out.entity.outputs.sequenceEvaluationOutput.buildOptions.mdMinimize = False
        #
        # Do the building of the structures
        #
        #  First, see if we should use a blocking call rather than the usual non-blocking call.
        #  Doing this is generally useful only for debugging.
        #
        GEMS_FORCE_SERIAL_EXECUTION = os.environ.get('GEMS_FORCE_SERIAL_EXECUTION')
        log.debug("GEMS_FORCE_SERIAL_EXECUTION: " + str(GEMS_FORCE_SERIAL_EXECUTION))
        #
        if GEMS_FORCE_SERIAL_EXECUTION is 'True' :
            #   use a blocking method:
            build.buildEach3DStructureInStructureInfo(self)
        else :
            #   using a non-blocking method:
            p = logic.EverLastingProcess(target=build.buildEach3DStructureInStructureInfo, args=(self,), daemon=False)
            p.start()
            #
        #sequenceProjects.createDefaultSymLinkBuildsDirectory(projectDir, buildDir + conformerID)
            ##  create downloadUrl
            ##  submit to amber for minimization, 
            ##      update structureInfo_status.json again
            ##      update project again                    
            ##  append response to transaction           
    except Exception as error:
        log.error("There was a problem managing this sequence request: " + str(error))
        log.error(traceback.format_exc())
        raise error

