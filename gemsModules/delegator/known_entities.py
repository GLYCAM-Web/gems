#!/usr/bin/env python3
#from enum import Enum
from gemsModules.common.code_utils import GemsStrEnum

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


class Known_Entities(GemsStrEnum):
    """
    The entities that Delegator knows about.
    """

    Delegator = "Delegator"
    DeprecatedDelegator = "DeprecatedDelegator"
    MDaaS = "MDaaS"
    Status = "Status"
    BatchCompute = "BatchCompute"
    Conjugate = "Conjugate"
    #CommonServicer = "CommonServicer"
    MmService = "MmService"
    Query = "Query"
    Sequence = "Sequence"
    DrawGlycan = "DrawGlycan"
    StructureFile = "StructureFile"
    PDBFile = "PDBFile"
    Glycomimetics = "Glycomimetics"
    AntibodyDocking = "AntibodyDocking"
    GlycoProtein = "GlycoProtein"
#    GpBuilder = "GpBuilder" # for backwards compatibility


