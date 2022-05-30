#!/usr/bin/env python3
from gemsModules.common.loggingConfig import loggers, createLogger
import traceback
import os
import sys

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


def manageSequenceBuild3DStructureRequest(self, defaultOnly: bool = False):
    log.info("manageSequenceBuild3DStructureRequest was called ")
    from typing import List
    from gemsModules.sequence import structureInfo, projects, logic, build
    from gemsModules.sequence import jsoninterface as sequenceio
    from gemsModules.project import projectUtilPydantic as projectUtils
    from gemsModules.project.jsoninterface import CbProject
    #
    # Do some sanity checks
    if self.transaction_out is None or self.transaction_in is None or self.transaction_out.project is None:
        thisAdditionalInfo = {
            'hint': 'The incoming transaction was not initialized properly.'}
        self.generateCommonParserNotice(
            noticeBrief='GemsError',
            scope='TransactionWrapper.ManageSeqeunceRequest',
            additionalInfo=thisAdditionalInfo
        )
        raise

    # Build the structureInfo object
    if self.transaction_out.entity is None :
        log.error("The entity in transaction_out does not exist.")
    if self.transaction_out.entity.outputs is None:
        self.transaction_out.entity.outputs = sequenceio.SequenceOutputs()
    if self.transaction_out.entity.outputs.structureBuildInfo is None:
        self.transaction_out.entity.outputs.structureBuildInfo = sequenceio.StructureBuildInfo()
        log.debug("structureBuildInfo: " +
                  str(self.transaction_out.entity.outputs.structureBuildInfo))
    try:
        thisStructureInfo = structureInfo.buildStructureInfoOliver(self)
        self.transaction_out.entity.outputs.structureBuildInfo = thisStructureInfo
        # thisStructureInfo.buildStates[0].energy=8.8888  # to test change-making
        log.debug("structureInfo: " + thisStructureInfo.json(indent=2))
    except Exception as error:
        log.error("There was a problem building structureInfo: " + str(error))
        log.error(traceback.format_exc())
        raise error
#    log.debug("Just built a thisStructureInfo.  The transaction_out is :   " )
#    log.debug(self.transaction_out.json(indent=2))
    # Save some copies of structureInfo for status tracking.
    try:
        # Determine whether to save or update.
        project_dir = self.transaction_out.project.project_dir
        filename = os.path.join(project_dir, "logs",
                                "structureInfo_request.json")
        log.debug("Checking for existing filename: " + filename)
        if os.path.exists(filename):
            log.debug(
                "\n\nstructureInfo_request.json found. Updating both the request and the status file.\n\n")
            structureInfo.updateStructureInfoWithUserOptions(
                self, thisStructureInfo, filename)
            statusFile = os.path.join(
                project_dir, "logs", "structureInfo_status.json")
            if os.path.exists(statusFile):
                structureInfo.updateStructureInfoWithUserOptions(
                    self, thisStructureInfo, statusFile)
            else:
                # Create new files for tracking this project.
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
        # Here we need to setup project folder, create some symLinks etc, before we get into each buildState
        # Not happy with the organization of this logic. Too much state being passed around and similar code!
        # Smells like it should be a class and this stuff goes in the initializer.
        thisProject = self.transaction_out.project
        this_pUUID = projectUtils.getProjectpUUID(thisProject)
        log.debug("this_pUUID is : " + this_pUUID)
        this_sequence = self.getSequenceVariantOut('indexOrdered')
        this_seqID = projectUtils.getSeqIdForSequence(this_sequence)
        thisProject.sequence_id = this_seqID
        thisProject.setSeqId(this_seqID)
        # TODO implement getCurrentBuildStrategyID().
        buildStrategyID = "buildStrategyID1"
        servicePath = thisProject.service_dir
        thisProject.sequence_path = os.path.join(
            thisProject.service_dir,
            'Sequences',
            thisProject.sequence_id)
        projects.setupInitialSequenceFolders(
            servicePath, this_seqID, this_pUUID, buildStrategyID)
        # Can generate the response already:
        for buildState in thisStructureInfo.individualBuildDetails:
            conformerID = buildState.structureDirectoryName
            projects.addResponse(
                buildState, self, conformerID, buildState.conformerLabel)
        # Regardless if requesting default or not, I think I need to generate a default. Otherwise I get into madness
        # with figuring out exist status and which conformerID to use in place of default. Then when a default
        # request does come, should it overwrite previous default for old projects?
        # A default request is always first, this is now implemented in buildStructureInfo
        # Decide if we need to minimize or not and tell everyone if need be
        mdMinimize = True
        # Check the outgoing transaction to see if it got set
        if self.transaction_out.mdMinimize is False:
            mdMinimize = False
        # Check the incoming transaction, too.
        if self.transaction_in is not None:
            if self.transaction_in.mdMinimize is False:
                mdMinimize = False
                if self.transaction_in.entity.inputs is not None:
                    if self.transaction_in.entity.inputs.buildOptions is not None:
                        self.transaction_in.entity.inputs.buildOptions.mdMinimize = False
        if mdMinimize is False:
            if self.transaction_out.entity.inputs is None:
                if self.transaction_in.entity.inputs is not None:
                    self.transaction_out.entity.inputs = self.transaction_in.entity.inputs
                else:
                    self.transaction_out.entity.inputs = sequenceio.SequenceInputs()
            if self.transaction_out.entity.inputs.buildOptions is None:
                self.transaction_out.entity.inputs.buildOptions = sequenceio.TheBuildOptions()
            self.transaction_out.entity.inputs.buildOptions.mdMinimize = False
            if self.transaction_out.entity.outputs is None:
                self.transaction_out.entity.outputs = sequenceio.TheSequencenOutputs()
            if self.transaction_out.entity.outputs.sequenceEvaluationOutput is None:
                self.transaction_out.entity.outputs.sequenceEvaluationOutput = sequenceio.TheSequenceEvaluationOutput()
            if self.transaction_out.entity.outputs.sequenceEvaluationOutput.buildOptions is None:
                self.transaction_out.entity.outputs.sequenceEvaluationOutput.buildOptions = sequenceio.TheBuildOptions()
            self.transaction_out.entity.outputs.sequenceEvaluationOutput.buildOptions.mdMinimize = False
        #
        # Do the building of the structures
        #
        #  First, see if we should use a blocking call rather than the usual non-blocking call.
        #  Doing this is generally useful only for debugging.
        GEMS_FORCE_SERIAL_EXECUTION = os.environ.get(
            'GEMS_FORCE_SERIAL_EXECUTION')
        log.debug("GEMS_FORCE_SERIAL_EXECUTION: " +
                  str(GEMS_FORCE_SERIAL_EXECUTION))
        # Now start the build process
        from gemsModules.sequence.build import buildEach3DStructureInStructureInfo
        if GEMS_FORCE_SERIAL_EXECUTION == 'True':
            buildEach3DStructureInStructureInfo(self)
        else:
            from gemsModules.common import logic as commonlogic
            def buildArgs() : # This merely simplifies the multiprocessing.Process call below
                buildEach3DStructureInStructureInfo(self)
            import multiprocessing
            detachedBuild=multiprocessing.Process(target=commonlogic.spawnDaemon, args=(buildArgs,))
            detachedBuild.daemon=False
            detachedBuild.start()

    except Exception as error:
        log.error(
            "There was a problem managing this sequence request: " + str(error))
        log.error(traceback.format_exc())
        raise error
