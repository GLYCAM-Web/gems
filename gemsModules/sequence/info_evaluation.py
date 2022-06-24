#!/usr/bin/env python3
from typing import Any 
from pydantic import BaseModel, Field
from gemsModules.common.loggingConfig import *
from gemsModules.sequence.sequence_self import TheSequenceVariants
from gemsModules.sequence.options_build_3D import TheBuildOptions
from gemsModules.sequence.options_draw import TheDrawOptions
import traceback


if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

class TheEvaluationOptions(BaseModel):
    """Options for sequence evaluations"""
    validateOnly: bool = False  # Stop after setting sequenceIsValid and return answer
    # Is this an evaluation as part of an explicit build request?
    evaluateForBuild: bool = False
    noBuild: bool = False  # Just do a full evaluation ; don't do the default example build


class TheSequenceEvaluationOutput(BaseModel):
    # Determine if the sequence has proper syntax, etc.
    sequenceIsValid: bool = False
    sequenceVariants: TheSequenceVariants = None
    evaluationOptions: TheEvaluationOptions = Field(
        None,
        description="Options for evaluating the sequence."
    )
    buildOptions: TheBuildOptions = Field(
        None,
        description="Options for building the 3D Structure of the sequence."
    )
    drawOptions: TheDrawOptions = Field(
        None,
        description="Options for drawing a 2D Structure of the sequence."
    )

    def __init__(self, **data: Any):
        super().__init__(**data)

    def getRotamerData(self):
        log.info("sequenceEvaluationOutput.getRotamerData was called")
        if self.buildOptions is None:
            return None
        else:
            return self.buildOptions.getRotamerData()

    def createRotamerData(self):
        log.info("Sequence evaluation data.createRotamerDataOut was called")
        if self.buildOptions is None:
            self.buildOptions = TheBuildOptions()
        self.buildOptions.createRotamerData()

    def getEvaluation(self, sequence: str, validateOnly):
        log.info("Getting the Evaluation for SequenceEvaluationOutput.")

        log.debug("sequence: " + repr(sequence))
        log.debug("validateOnly: " + repr(validateOnly))

        from gemsModules.sequence import evaluate

        if self.evaluationOptions is None:
            self.evaluationOptions = TheEvaluationOptions()

        self.evaluationOptions.validateOnly = validateOnly
        self.sequenceIsValid = evaluate.checkIsSequenceSane(sequence)
        log.debug("self.sequenceIsValid: " + str(self.sequenceIsValid))

        if self.sequenceIsValid:
            self.sequenceVariants = TheSequenceVariants()
            self.sequenceVariants = evaluate.getSequenceVariants(sequence)
            log.debug("Just got sequence variants.  They are:")
            log.debug(str(self.sequenceVariants))
###
# I think these are no longer needed.
###
            #log.debug("indexOrdered: " + str(self.sequenceVariants['indexOrdered']))
            #reducingSuffix = self.sequenceVariants['indexOrdered'][-7:]
            log.debug("indexOrdered: " +
                      str(self.sequenceVariants.indexOrdered))
            reducingSuffix = self.sequenceVariants.indexOrdered[-7:]
            log.debug("reducingSuffix: " + reducingSuffix)
            log.debug("# of '-': " + str(reducingSuffix.count('-')))
#            if 2 == reducingSuffix.count('-'):
#                lastIndex = self.sequenceVariants['indexOrdered'].rfind('-')
#                log.debug("lastIndex of '-': " + str(lastIndex))
#                self.sequenceVariants['indexOrdered'] = self.sequenceVariants['indexOrdered'][:lastIndex - 2] + self.sequenceVariants['indexOrdered'][lastIndex:]
#                log.debug("indexOrdered: " + self.sequenceVariants['indexOrdered'])
            # DGlcpNAcb1-1-OH

        if self.sequenceIsValid and not self.evaluationOptions.validateOnly:
            self.buildOptions = TheBuildOptions()
            self.buildOptions.setGeometryOptions(sequence)

       # self.defaultStructure
        # drawOptions to be developed later.

    # ## I'm certain there is a better way to do this.  - Lachele
    def getSequenceVariant(self, variant):
        log.debug("TheSequenceEvaluationOutput.getSequenceVariant was called")
        # if not 'Evaluate' in  self.responses.Keys() :
        if self.sequenceVariants is None:
            return None
        else:
            theVariant = getattr(self.sequenceVariants, variant)
            return theVariant



def generateSchema():
    print(TheEvaluationOptions.schema_json(indent=2))

if __name__ == "__main__":
    generateSchema()