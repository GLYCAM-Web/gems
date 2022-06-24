#!/usr/bin/env python3
from typing import List, Any 
from pydantic import BaseModel, Field
from gemsModules.common.loggingConfig import *
import traceback


if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


class TheResidueRingPucker(BaseModel):
    puckerClassificationSystem: str = Field(
        'BFMP',
        description="The system used to identify the ring pucker (shape)."
    )


class TheRotamerDihedralInfo(BaseModel):
    dihedralName: str = None  # phi, psi etc.
    dihedralValues: List[str] = []  # gg, -g, tg, etc


class SingleLinkageRotamerData(BaseModel):
    indexOrderedLabel: str = None
    linkageLabel: str = None
    linkageName: str = None
    firstResidueNumber: str = None
    secondResidueNumber: str = None
    dihedralsWithOptions: List[str] = []
    possibleRotamers: List[TheRotamerDihedralInfo] = []
    likelyRotamers: List[TheRotamerDihedralInfo] = []
    selectedRotamers: List[TheRotamerDihedralInfo] = []


class AllLinkageRotamerInfo(BaseModel):
    """Geometry options for linkages"""
    singleLinkageRotamerDataList: List[SingleLinkageRotamerData] = []
    totalLikelyRotamers: int = 0
    totalPossibleRotamers: int = 0
    totalSelectedRotamers: int = 0

    def __init__(self, **data: Any):
        super().__init__(**data)

        if self.singleLinkageRotamerDataList != []:
            from gemsModules.sequence import structureInfo
            if self.totalSelectedRotamers == 0:
                self.totalSelectedRotamers = structureInfo.countNumberOfShapes(
                    self, 'Selected')
            if self.totalPossibleRotamers == 0:
                self.totalPossibleRotamers = structureInfo.countNumberOfShapes(
                    self, 'Possible')
            if self.totalLikelyRotamers == 0:
                self.totalLikelyRotamers = structureInfo.countNumberOfShapes(
                    self, 'Likely')


def generateSchema():
    print(AllLinkageRotamerInfo.schema_json(indent=2))


if __name__ == "__main__":
    generateSchema()
