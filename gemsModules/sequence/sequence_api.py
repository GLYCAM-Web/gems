#!/usr/bin/env python3
from typing import  Any 
from gemsModules.common.loggingConfig import *
import gemsModules.common.common_api as commonio
import gemsModules.project.project_api as projectio
import traceback


if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


class sequenceTransactionSchema(commonio.TransactionSchema):
    """
    Holds info about the Transaction JSON object used in the Sequence entity.
    """
    # ... means a value is required in Pydantic.
    entity: sequenceEntity = ...
    project: projectio.CbProject = None

    def __init__(self, **data: Any):
        super().__init__(**data)

    class Config:
        title = 'gensModulesSequenceTransaction'

    # ## I'm certain there is a better way to do this.  - Lachele
    def getInputSequencePayload(self):
        log.info("sequenceTransactionSchema.getInputSequencePayload was called")
        if self.entity is None:
            return None
        else:
            return self.entity.getInputSequencePayload()

    def getRotamerDataIn(self):
        log.info("Transaction.getRotamerDataIn was called")
        if self.entity is None:
            return None
        else:
            return self.entity.getRotamerDataIn()

    def getRotamerDataOut(self):
        log.info("Transaction.getRotamerDataOut was called")
        if self.entity is None:
            return None
        else:
            return self.entity.getRotamerDataOut()

    def createRotamerDataOut(self):
        log.info("Transaction.createRotamerDataOut was called")
        if self.entity is None:
            self.entity = sequenceEntity()
        self.entity.createRotamerDataOut()

    def getBuildStrategyIDOut(self):
        if self.entity is None:
            return None
        else:
            return self.entity.getBuildStrategyIDOut()

    def getBuildSequenceOut(self):
        if self.entity is None:
            return None
        else:
            return self.entity.getSequence()

    # ## I'm certain there is a better way to do this.  - Lachele
    def getSequenceVariantIn(self, variant):
        log.info("sequenceTransactionSchema.getSequenceVariantIn was called")
        if self.entity is None:
            return None
        else:
            return self.entity.getSequenceVariantIn(variant)

    # ## I'm certain there is a better way to do this.  - Lachele
    def getSequenceVariantOut(self, variant):
        log.info("sequenceTransactionSchema.getSequenceVariantOut was called")
        if self.entity is None:
            return None
        else:
            return self.entity.getSequenceVariantOut(variant)

    def evaluateCondensedSequence(self):
        if self.entity is None:
            thisAdditionalInfo = {
                'hint': 'The transaction has no defined entity.'}
            self.generateCommonParserNotice(
                noticeBrief='GemsError',
                scope='SequenceTransaction',
                additionalInfo=thisAdditionalInfo
            )
            return
#            raise error
        self.entity.evaluateCondensedSequence()


class Transaction(commonio.Transaction):
    transaction_in: sequenceTransactionSchema
    transaction_out: sequenceTransactionSchema

    def populate_transaction_in(self):
        log.info("sequence - Transaction.populate_transaction_in was called")
        self.transaction_in = sequenceTransactionSchema(**self.request_dict)
        log.debug("The transaction_in is: ")
        log.debug(self.transaction_in.json(indent=2))

    def initialize_transaction_out_from_transaction_in(self):
        log.info("initialize_transaction_out_from_transaction_in was called")
        self.transaction_out = self.transaction_in.copy(deep=True)
        log.debug("The transaction_out is: ")
        log.debug(self.transaction_out.json(indent=2))

#    def doDefaultService(self):
#        from gemsModules.sequence.receive import doDefaultService
#        doDefaultService(self)

    def getRotamerDataIn(self):
        log.info("Transaction-Wrapper.getRotamerDataIn was called")
        if self.transaction_in is None:
            return None
        else:
            return self.transaction_in.getRotamerDataIn()

    def getRotamerDataOut(self):
        log.info("Transaction-Wrapper.getRotamerDataOut was called")
        if self.transaction_out is None:
            return None
        else:
            return self.transaction_out.getRotamerDataOut()

    def createRotamerDataOut(self):
        log.info("Transaction-Wrapper.createRotamerDataOut was called")
        if self.transaction_out is None:
            self.transaction_out = sequenceTransactionSchema()
        return self.transaction_out.createRotamerDataOut()

    # ## I'm certain there is a better way to do this.  - Lachele
    def getInputSequencePayload(self):
        log.info("sequence - Transaction.getInputSequencePayload was called")
        if self.transaction_in is None:
            return None
        else:
            return self.transaction_in.getInputSequencePayload()

    # These project-based ones should really depend more on project
    def getPuuIDOut(self):
        if self.transaction_out is None:
            return None
        if self.transaction_out.project is None:
            return None
        if self.transaction_out.project.pUUID is None:
            return None
        else:
            return self.transaction_out.project.pUUID

    def getProjectDirOut(self):
        if self.transaction_out is None:
            return None
        if self.transaction_out.project is None:
            return None
        if self.transaction_out.project.project_dir is None:
            return None
        else:
            return self.transaction_out.project.project_dir

    def getIsEvaluationSetNoBuild(self):
        if all(v is not None for v in [
            self.transaction_out,
            self.transaction_out.entity,
            self.transaction_out.entity.outputs,
            self.transaction_out.entity.outputs.sequenceEvaluationOutput,
            self.transaction_out.entity.outputs.sequenceEvaluationOutput.evaluationOptions
        ]):
            return self.transaction_out.entity.outputs.evaluationOptions.noBuild
        else:
            return False  # the default value if not set otherwise

    def setIsEvaluationSetNoBuild(self, value):
        if all(v is not None for v in [
            self.transaction_out,
            self.transaction_out.entity,
            self.transaction_out.entity.outputs,
            self.transaction_out.entity.outputs.sequenceEvaluationOutput,
            self.transaction_out.entity.outputs.sequenceEvaluationOutput.evaluationOptions
        ]):
            self.transaction_out.entity.outputs.evaluationOptions.noBuild = value
        else:
            self.generateCommonParserNotice(
                noticeBrief='GemsError',
                additionalInfo={"hint": "cannot set noBuild option"})

    def getIsEvaluationForBuild(self):
        if all(v is not None for v in [
            self.transaction_out,
            self.transaction_out.entity,
            self.transaction_out.entity.outputs,
            self.transaction_out.entity.outputs.sequenceEvaluationOutput,
            self.transaction_out.entity.outputs.sequenceEvaluationOutput.evaluationOptions
        ]):
            return self.transaction_out.entity.outputs.sequenceEvaluationOutput.evaluationOptions.evaluateForBuild
        else:
            return False  # the default value if not set otherwise

    def setIsEvaluationForBuild(self, value):
        if all(v is not None for v in [
            self.transaction_out,
            self.transaction_out.entity,
            self.transaction_out.entity.outputs,
            self.transaction_out.entity.outputs.sequenceEvaluationOutput,
            self.transaction_out.entity.outputs.sequenceEvaluationOutput.evaluationOptions
        ]):
            self.transaction_out.entity.outputs.sequenceEvaluationOutput.evaluationOptions.evaluateForBuild = value
        else:
            self.generateCommonParserNotice(
                noticeBrief='GemsError',
                additionalInfo={"hint": "cannot set evaluateForBuild option"})

    def getNumberStructuresHardLimitIn(self):
        if all(v is not None for v in [
            self.transaction_in,
            self.transaction_in.entity,
            self.transaction_in.entity.inputs,
            self.transaction_in.entity.inputs.buildOptions
        ]):
            return self.transaction_in.entity.inputs.buildOptions.numberStructuresHardLimit
        else:
            return None

    def setNumberStructuresHardLimitOut(self, value):
        if all(v is not None for v in [
            self.transaction_out,
            self.transaction_out.entity,
            self.transaction_out.entity.outputs,
            self.transaction_out.entity.outputs.sequenceEvaluationOutput,
            self.transaction_out.entity.outputs.sequenceEvaluationOutput.buildOptions
        ]):
            self.transaction_out.entity.outputs.sequenceEvaluationOutput.buildOptions.numberStructuresHardLimit = value
        else:
            self.generateCommonParserNotice(
                noticeBrief='GemsError',
                additionalInfo={"hint": "cannot set limit for number of structures"})
            return None
    # TODO - write all these if-not-None-return recursions to look like the ones above.

    def getSeqIdOut(self):
        if self.transaction_out is None:
            return None
        if self.transaction_out.entity is None:
            return None
        if self.transaction_out.entity.outputs is None:
            return None
        if self.transaction_out.entity.outputs.structureBuildInfo is None:
            return None
        if self.transaction_out.entity.outputs.structureBuildInfo.seqID is None:
            return None
        else:
            return self.transaction_out.entity.outputs.structureBuildInfo.seqID

    def getStructureBuildInfoOut(self):
        if self.transaction_out is None:
            return None
        if self.transaction_out.entity is None:
            return None
        if self.transaction_out.entity.outputs is None:
            return None
        if self.transaction_out.entity.outputs.structureBuildInfo is None:
            return None
        else:
            return self.transaction_out.entity.outputs.structureBuildInfo

    def getIndividualBuildDetailsOut(self):
        if self.transaction_out is None:
            return None
        if self.transaction_out.entity is None:
            return None
        if self.transaction_out.entity.outputs is None:
            return None
        if self.transaction_out.entity.outputs.structureBuildInfo is None:
            return None
        if self.transaction_out.entity.outputs.structureBuildInfo.individualBuildDetails is None:
            return None
        if self.transaction_out.entity.outputs.structureBuildInfo.individualBuildDetails is []:
            return None
        else:
            return self.transaction_out.entity.outputs.structureBuildInfo.individualBuildDetails

    def getBuildStrategyIDOut(self):
        if self.transaction_out is None:
            return None
        else:
            return self.transaction_out.getBuildStrategyIDOut()

    def getBuildSequenceOut(self):
        if self.transaction_out is None:
            return None
        else:
            return self.transaction_out.getSequence()

    # ## I'm certain there is a better way to do this.  - Lachele
    def getSequenceVariantIn(self, variant):
        log.info("sequence - Transaction.getSequenceVariantIn was called")
        if self.transaction_in is None:
            return None
        else:
            return self.transaction_in.getSequenceVariantIn(variant)

    # ## I'm certain there is a better way to do this.  - Lachele
    def getSequenceVariantOut(self, variant):
        log.info("sequence - Transaction.getSequenceVariantOut was called")
        if self.transaction_out is None:
            return None
        else:
            return self.transaction_out.getSequenceVariantOut(variant)

    def evaluateCondensedSequence(self):
        if self.transaction_out is None and self.transaction_in is None:
            thisAdditionalInfo = {
                'hint': 'Neither the transaction_in nor the transaction_out are populated.'}
            self.generateCommonParserNotice(
                noticeBrief='NoInputPayloadDefined',
                scope='TransactionWrapper.EvaluateCondensedSequence',
                additionalInfo=thisAdditionalInfo
            )
            return
#            raise error
        if self.transaction_out is None:
            self.initialize_transaction_out_from_transaction_in()
        self.transaction_out.evaluateCondensedSequence()

# In file _manageSequenceBuild3DStructureRequest.py:
#    def manageSequenceBuild3DStructureRequest(self, defaultOnly : bool = False)
    from gemsModules.sequence._manageSequenceBuild3DStructureRequest import manageSequenceBuild3DStructureRequest

    def build_outgoing_string(self):
        if self.transaction_out.prettyPrint is True:
            self.outgoing_string = self.transaction_out.json(indent=2)
        else:
            self.outgoing_string = self.transaction_out.json()


def generateSchema():
    print(sequenceTransactionSchema.schema_json(indent=2))


inputJSON = '{ "entity": { "type": "Sequence", "services":  { "Build": { "type": "Build3DStructure" } } , "inputs":  { "Sequence": { "payload": "DManpa1-OH" } } } }'


def troubleshoot():
    thisTransaction = Transaction(inputJSON)
    print(thisTransaction.incoming_string)
    print(thisTransaction.request_dict)
    thisTransaction.populate_transaction_in()
    print(thisTransaction.transaction_in)


if __name__ == "__main__":
    generateSchema()
    troubleshoot()
