#!/usr/bin/env python3
from typing import Dict, Any 
from pydantic import Field
from gemsModules.common.loggingConfig import *
import gemsModules.common.common_api as commonio
from gemsModules.sequence import settings
import traceback


if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


class sequenceEntity(commonio.Entity):
    """Holds information about the main object responsible for a service."""
    entityType: str = Field(
        settings.WhoIAm,
        title='Type',
        alias='type'
    )
    services: Dict[str, sequenceService] = sequenceService()
    inputs: SequenceInputs = None
    outputs: SequenceOutputs = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        log.info("Instantiating a sequenceEntity")
        log.debug("entityType: " + self.entityType)

    # ## I'm certain there is a better way to do this.  - Lachele
    def getInputSequencePayload(self):
        log.info("sequenceEntity.getInputSequencePayload was called")
        if self.inputs is None:
            return None
        elif self.inputs.sequence is None:
            return None
        elif self.inputs.sequence.payload is None:
            return None
        else:
            return self.inputs.sequence.payload

    def getBuildStrategyIDOut(self):
        if self.outputs is None:
            return None
        else:
            return self.outputs.getBuildStrategyID()

    def getBuildSequenceOut(self):
        if self.outputs is None:
            return None
        else:
            return self.outputs.getSequence()

    def getRotamerDataIn(self):
        log.info("Entity.getRotamerDataIn was called")
        if self.inputs is None:
            log.debug("inputs is None. returning None.")
            return None
        elif self.inputs.geometryOptions is None:
            log.debug("inputs.geometryOptions is None. returning None.")
            return None
        else:
            return self.inputs.geometryOptions.getRotamerData()

    def getRotamerDataOut(self):
        log.info("Entity.getRotamerDataOut was called")
        if self.outputs is None:
            return None
        else:
            return self.outputs.getRotamerData()

    def createRotamerDataOut(self):
        log.info("Entity.createRotamerDataOut was called")
        if self.outputs is None:
            self.outputs = SequenceOutputs()
        self.outputs.createRotamerData()

    # ## I'm certain there is a better way to do this.  - Lachele
    def getSequenceVariantIn(self, variant):
        log.info("sequenceEntity.getSequenceVariantIn was called")
        if self.inputs is None:
            return None
        elif self.inputs.sequenceVariants is None:
            return None
        else:
            return self.inputs.sequenceVariants[variant]

    # ## I'm certain there is a better way to do this.  - Lachele
    def getSequenceVariantOut(self, variant):
        log.debug("sequenceEntity.getSequenceVariantOut was called")
        if self.outputs is None:
            log.debug("sequenceEntity.getSequenceVariantOut found NO OUPUTS")
            return None
        elif self.outputs.sequenceEvaluationOutput is None:
            log.debug(
                "sequenceEntity.getSequenceVariantOut found NO Sequence Evaluation Output")
            return None
        else:
            log.debug(
                "sequenceEntity.getSequenceVariantOut attempting to return variant.")
            return self.outputs.sequenceEvaluationOutput.getSequenceVariant(variant)

    def validateCondensedSequence(self, validateOnly: bool = False):
        self.evaluateCondensedSequence(validateOnly=True)

    def evaluateCondensedSequence(self, validateOnly: bool = False):
        if self.inputs is None:
            thisAdditionalInfo = {'hint', 'The entity has no defined inputs.'}
            self.generateCommonParserNotice(
                noticeBrief='EmptyPayload',
                scope='SequenceEntity',
                additionalInfo=thisAdditionalInfo
            )
            raise
        if self.inputs.sequence is None:
            thisAdditionalInfo = {
                'hint': 'The entity has inputs but cannot find Sequence Payload.'}
            self.generateCommonParserNotice(
                noticeBrief='EmptyPayload',
                scope='SequenceEntityInputs',
                additionalInfo=thisAdditionalInfo
            )
            raise
        sequence = self.inputs.sequence.payload
        if sequence is None or "":
            thisAdditionalInfo = {
                'hint': 'The entity a Sequence but cannot find Sequence Payload.'}
            self.generateCommonParserNotice(
                noticeBrief='EmptyPayload',
                scope='SequenceEntityInputSequence',
                additionalInfo=thisAdditionalInfo
            )
            raise
        if self.outputs is None:
            self.outputs = SequenceOutputs()
        if self.outputs.sequenceEvaluationOutput is None:
            self.outputs.sequenceEvaluationOutput = TheSequenceEvaluationOutput()
        self.outputs.sequenceEvaluationOutput.getEvaluation(
            sequence, validateOnly)



def generateSchema():
    print(sequenceTransactionSchema.schema_json(indent=2))


if __name__ == "__main__":
    generateSchema()
