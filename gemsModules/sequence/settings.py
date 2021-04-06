#!/usr/bin/env python3
from gemsModules import common
from gemsModules.common.transaction import *
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel

## Who I am
WhoIAm='Sequence'

##Status Report
status = "Stable"
moduleStatusDetail = "Nearing ready for v1 release. Needs tests and documentation."

servicesStatus = [
    {
        "service" : "Validate",
        "status" : "Stable.",
        "statusDetail" : "Rarely used Evaluate includes Validate. Validate mayeventually be deprecated."
    },
    {
        "service" : "Evaluate",
        "status" : "Stable.",
        "statusDetail" : "Works for GLYCAM condensed sequences."
    },
    {
        "service" : "Build3DStructure",
        "status" : "Stable.",
        "statusDetail" : "Ready for tests and documentation."
    }
]

subEntities = [
    {
        "subEntity" : "Graph"
    }
]


#Validate service in focus.
#Evaluate service still needs to be developed.
#Build3DStructure can create a default structure.
#No minimization is applied yet.
#No options can be set yet."

## Module names for services that this entity/module can perform.
serviceModules = {
    'Validate' : 'validate',
    'Evaluate' : 'evaluate',
    'Build3DStructure' : 'build3Dstructure'
}


# ## from Lachele, 2021-04-01:  
# ##    I'm moving these here from io.py.  They don't
# ##    have to stay here.  I was hoping to make io.py
# ##    a little sipler.  I also have my eye on making
# ##    a lot of the io classes be generic so that they
# ##    need a lot less redefinition in the child classes.
#
# ##
# ## Services
# ##
class Services(str,Enum):
    build3dStructure = 'Build3DStructure'
    drawGlycan = 'DrawGlycan'
    evaluate = 'Evaluate'
    status = 'Status'

# ## Environment variables
# ##
class Environment(str,Enum):
    ## The entity itself
    sequenceentity   = 'GEMS_MODULES_SEQUENCE_PATH'
    ## Services for this entity, in alphabetical order
    build3DStructure = 'GEMS_MODULES_SEQUENCE_STRUCTURE_PATH'
    graph = 'GEMS_MODULES_SEQUENCE_GRAPH_PATH'
    evaluate         = 'GEMS_MODULES_SEQUENCE_STRUCTURE_PATH'

# ## Recognized input and output formats
# ##
class Formats(str,Enum):
    """All Sequenes must be in GLYCAM Condensed notation"""
    # the basic sequence as it might arrive, unspecified order, assumed condensed glycam
    sequence = 'Sequence'  

class Locations(str,Enum):
    internal='internal'  ##< All input at this time must be internal to the JSON object(s)

### This does not appear to be used anywhere.   (Lachele 2021-04-01)
class LinkageRotamerNames(str, Enum):
    phi = 'phi'
    psi = 'psi'
    omg = 'omg'
    omega = 'omega'

