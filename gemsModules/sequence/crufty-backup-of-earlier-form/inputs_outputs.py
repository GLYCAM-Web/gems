#!/usr/bin/env python3
from tkinter import W
from pydantic import BaseModel
from gemsModules.sequence.info_evaluation import TheSequenceEvaluationOutput
from gemsModules.sequence.info_build3D import StructureBuildInfo
from gemsModules.sequence.sequence_self import TheSequence, TheSequenceVariants
from gemsModules.sequence.options_build_3D import TheBuildOptions,TheSystemSolvationOptions
from gemsModules.sequence.options_evaluation import TheEvaluationOptions
from gemsModules.sequence.options_geometry import TheGeometryOptions
from gemsModules.sequence.options_draw import TheDrawOptions
from gemsModules.common.loggingConfig import *
import traceback


if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


# This is a Response and should be called that
class SequenceOutputs(BaseModel):
    sequenceEvaluationOutput: TheSequenceEvaluationOutput = None
    structureBuildInfo: StructureBuildInfo = None

    def getStructureBuildInfo(self):
        if self.structureBuildInfo is None:
            return None
        else:
            return self.structureBuildInfo

    def getBuildStrategyID(self):
        if self.structureBuildInfo is None:
            return None
        else:
            return self.structureBuildInfo.getBuildStrategyID()

    def getSequence(self):
        if self.structureBuildInfo is None:
            return None
        else:
            return self.structureBuildInfo.getSequence()

    def getRotamerData(self):
        log.info("evaluate.getRotamerData was called")
        if self.sequenceEvaluationOutput is None:
            return None
        else:
            return self.sequenceEvaluationOutput.getRotamerData()

    def createRotamerData(self):
        log.info("Sequence outputs.createRotamerDataOut was called")
        if self.sequenceEvaluationOutput is None:
            self.sequenceEvaluationOutput = TheSequenceEvaluationOutput()
        self.sequenceEvaluationOutput.createRotamerData()


class SequenceInputs(BaseModel):
    sequence: TheSequence = None
    sequenceVariants: TheSequenceVariants = None
    systemSolvationOptions: TheSystemSolvationOptions = None
    geometryOptions: TheGeometryOptions = None
    buildOptions: TheBuildOptions = None
    evaluationOptions: TheEvaluationOptions = None
    drawOptions: TheDrawOptions = None

def generateSchema():
    print(SequenceInputs.schema_json(indent=2))
    print(SequenceOutputs.schema_json(indent=2))

if __name__ == "__main__":
    generateSchema()
