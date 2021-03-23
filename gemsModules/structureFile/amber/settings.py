#!/usr/bin/env python3
from gemsModules import common
from gemsModules.common.transaction import *
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel

## Who I am
WhoIAm='Amber'

##Status Report
status = "In development"
moduleStatusDetail = "Module framework exists. Building logic for PDB Preprocessing."

servicesStatus = [
    {
        "service" : "PreprocessPDB",
        "status" : "In development",
        "statusDetail" : "Creating the logic used to preprocess PDB files."
    }
]


descriptions = {
	"histidineProtonation" : "Here is the description for the purpose behind the Histidine Protonation data.",
	"disulfideBonds" : "Here is the description for the purpose behind the Disulfide Bonds data",
	"unrecognizedResidues" : "Here is the description for the purpose behind the Unrecognized Residue data",
	"chainTerminations" : "Here is the description for the purpose behind the Chain Terminations data",
	"replacedHydrogens" : "Here is the description for the purpose behind the Replaced Hydrogens data",
	"unrecognizedHeavyAtoms" : "Here is the description for the purpose behind the Unrecognized Heavy Atoms data",
	"missingResidues" : "Here is the description for the purpose behind the Missing Residues data"
}

