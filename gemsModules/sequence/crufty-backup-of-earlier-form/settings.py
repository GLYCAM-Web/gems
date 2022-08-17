#!/usr/bin/env python3
from gemsModules import common
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from enum import Enum

from pydantic import BaseModel

from gemsModules.common.utils import GemsStrEnum

# Who I am
WhoIAm = 'Sequence'

# Status Report
status = "Stable"
moduleStatusDetail = "Nearing ready for v1 release. Needs tests and documentation."

servicesStatus = [
    {
        "service": "Validate",
        "status": "Stable.",
        "statusDetail": "Rarely used Evaluate includes Validate. Validate mayeventually be deprecated."
    },
    {
        "service": "Evaluate",
        "status": "Stable.",
        "statusDetail": "Works for GLYCAM condensed sequences."
    },
    {
        "service": "Build3DStructure",
        "status": "Stable.",
        "statusDetail": "Ready for tests and documentation."
    }
]


# Module names for services that this entity/module can perform.
class subEntities(GemsStrEnum) :
    Graph = 'graph'

class AvailableServices(GemsStrEnum):
    build3dStructure = 'Build3DStructure'
    drawGlycan = 'DrawGlycan'
    evaluate = 'Evaluate'
    status = 'Status'


class Environment(GemsStrEnum):
    # The entity itself
    sequenceentity = 'GEMS_MODULES_SEQUENCE_PATH'
    # Services for this entity, in alphabetical order
    build3DStructure = 'GEMS_MODULES_SEQUENCE_STRUCTURE_PATH'
    graph = 'GEMS_MODULES_SEQUENCE_GRAPH_PATH'
    evaluate = 'GEMS_MODULES_SEQUENCE_STRUCTURE_PATH'

# ## Recognized input and output formats
# ##


class Formats(GemsStrEnum):
    """All Sequenes must be in GLYCAM Condensed notation"""
    # the basic sequence as it might arrive, unspecified order, assumed condensed glycam
    sequence = 'Sequence'


class Locations(GemsStrEnum):
    # < All input at this time must be internal to the JSON object(s)
    internal = 'internal'
