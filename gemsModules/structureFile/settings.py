#!/usr/bin/env python3
from gemsModules import common
from gemsModules.common.transaction import *
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel
## Who I am
WhoIAm='StructureFile'

##Status Report
status = "Dev"
moduleStatusDetail = "PDB Pre-processing for Amber currently in development. Writing evaluate service."

servicesStatus = [
    {
        "service" : "Evaluate",
        "status" : "In development.",
        "statusDetail" : "In development. Currently fails to return a valid response. Queued for after Schema service."
    },
    {
        "service" : "PreprocessPdbForAmber",
        "status" : "In development.",
        "statusDetail" : "In development."
    }
]

serviceModules = {
    'Evaluate' : 'evaluate',
    'PreprocessPdbForAmber' : 'preprocessPdbForAmber'
}

# ## Services
# ##
class Services(str,Enum):
    evaluate = 'Evaluate'
    status = 'Status'
    preprocessPdbForAmber = 'PreprocessPdbForAmber'

## Is this the best place for these?
amino_libs = "gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib",
glycam_libs = "gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib",
other_libs = "gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminoct12.lib" 
prep_file = "gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j-1.prep"

