#!/usr/bin/env python3
from gemsModules.common.logic import getGemsHome
from gemsModules.common.loggingConfig import *
from os.path import join

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


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

try:
    gemsHome = getGemsHome()
    log.debug("gemsHome: " + gemsHome)
except Exception as error:
    log.error("There was a problem getting GEMSHOME.")
    raise error

try:
	## Is this the best place for these?
	AMINO_LIBS = os.path.join(gemsHome, "gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib")
	PREP_FILE = os.path.join(gemsHome, "gmml/dat/prep/GLYCAM_06j-1_GAGS_KDN.prep")
	GLYCAM_LIBS = os.path.join(gemsHome, "gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib")
	OTHER_LIBS = os.path.join(gemsHome, "gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminoct12.lib")
except Exception as error:
    log.error("There was a problem setting the default gmml resources: " + str(error))
    raise error