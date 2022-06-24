#!/usr/bin/env python3
from typing import List, Any 
from pydantic import BaseModel
from gemsModules.common.loggingConfig import *
from gemsModules.sequence.geometries import *  # star is ok here bc this really does need all the defs in geometries.py
import traceback


if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


class TheResidueGeometryOptions(BaseModel):
    """Geometry options for residues"""
    ringPuckers: List[TheResidueRingPucker] = []


class TheLinkageGeometryOptions(BaseModel):
    linkageRotamerInfo: AllLinkageRotamerInfo = None

    def getRotamerData(self):
        log.info("Linkage GeometryOptions.getRotamerData was called")
        if self.linkageRotamerInfo is None:
            return None
        else:
            return self.linkageRotamerInfo

    def createRotamerData(self):
        log.info("Linkage geometry options.createRotamerDataOut was called")
        if self.linkageRotamerInfo is None:
            self.linkageRotamerInfo = AllLinkageRotamerInfo()
        self.linkageRotamerInfo.createRotamerData()

    def setLinkageRotamerInfo(self, validatedSequence: str):
        from gemsModules.sequence import evaluate
        self.linkageRotamerInfo = evaluate.getLinkageOptionsFromGmmlcbBuilder(
            validatedSequence)
        log.debug(self.linkageRotamerInfo.json())


class TheGeometryOptions(BaseModel):
    residues: TheResidueGeometryOptions = None  # Not yet handled.
    linkages: TheLinkageGeometryOptions = None

    def __init__(self, **data: Any):
        super().__init__(**data)

    def getRotamerData(self):
        log.info("GeometryOptions.getRotamerData was called")
        if self.linkages is None:
            return None
        elif self.linkages.linkageRotamerInfo is None:
            return None
        else:
            return self.linkages.linkageRotamerInfo

    def createRotamerData(self):
        log.info("Geometry options.createRotamerDataOut was called")
        if self.linkages is None:
            self.linkages = TheLinkageGeometryOptions()
        if self.linkages.linkageRotamerInfo is None:
            self.linkages.linkageRotamerInfo = AllLinkageRotamerInfo()
        self.linkages.linkageRotamerInfo.createRotamerData()

    def setLinkageRotamerInfo(self, validatedSequence: str):
        if self.linkages is None:
            self.linkages = TheLinkageGeometryOptions()
        self.linkages.setLinkageRotamerInfo(validatedSequence)
#        from gemsModules.sequence import evaluate
#        self.linkages = evaluate.getLinkageOptionsFromGmmlcbBuilder(validatedSequence)
#        log.debug(self.linkages.json())


def generateSchema():
    print(TheGeometryOptions.schema_json(indent=2))


if __name__ == "__main__":
    generateSchema()
