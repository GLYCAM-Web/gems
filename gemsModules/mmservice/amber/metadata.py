#!/usr/bin/env python3
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from typing import ForwardRef
from pydantic import BaseModel, Field
from pydantic.schema import schema
from gemsModules.common.loggingConfig import *
import traceback

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

class AmberInstalltionData(BaseModel):
    """Description of a the AMBER installation itself."""
    amberHome: str = Field(
            None,
            description='Full path for the AMBER installation directory.'
            )
    version: str = Field(
            None,
            description='Versioning info - usually either a release number + patches or a git hash.'
            )
    hasSander: bool = Field(
            None,
            description='Brief title, status or name for this notice or notice type.'
            )


class SampleEnum(str,Enum):
    """
    Information specific to the AMBER installation itself.

    That is, this is where to encode AMBERHOME, the presence of MPI versions
    of files, versioning information, etc.  

    """
    evaluate = 'Evaluate'
    defaultService = 'DefaultService'
    marco = 'Marco'


	"amber

AMBERHOME='/programs/amber16'  # default prefix for a structure file
MD_ENERGY_LOC_TEXT='FINAL RESULTS'  # text in the MDOUT file just before final energy
MD_GP_DONE_TEXT='wallclock'  # text in the MDOUT file that signifies successful completion
MD_GP_FINAL_TIME_TEXT='Total Time'
MD_SOL_DONE_TEXT='Total wall time'  # text in the MDOUT file that signifies successful completion
MD_SOL_ELAPSED_LOC_TEXT='Average timings for all steps'
MD_SOL_ELAPSED_TEXT='Elapsed(s) ='
MD_SOL_ELAPSED_TAIL_TEXT='Per Step(ms)'
MD_SOL_TIME_REMAINING_TXT='Estimated time remaining:'
MD_SOL_FINAL_TIME_TEXT='Total wall time'
prefSTRUCTURE='mol'  # default prefix for a structure file

##
## File Extensions - the part after the final period (.)
##
# General extensions
extPDB='pdb'  # all varieties of PDB-style file
extOFF='off'  # OFF files
extMMCIF='mmcif'  # mm-cif files
extTEXT='txt'  # A plain-text file, usually ASCII
extRUNLOG='runlog'  # log for the GLYCAM-Web process

# AMBER-related extensions
extPARM='parm7'  # AMBER parameter-topology file
extINPCRD='rst7'  # AMBER input-coordinate file
extMINCRD='mincrd'
extHEATCRD='heatcrd'
extEQUICRD='equicrd'
extMDCRD='mdcrd'  # AMBER coordinate trajectory
extMDVEL='mdvel'  # AMBER velocity trajectory
extMDCRDBOX='crdbox'  # AMBER coordinate trajectory with periodic boundary

extLEAPIN='leapin'
extMININ='minin'
extHEATIN='heatin'
extEQUIIN='equiin'
extMDIN='mdin'  # AMBER molecular dynamics input file

extMINOUT='minout'
extHEATOUT='heatout'
extEQUIOUT='equiout'
extMDOUT='mdout'  # AMBER molecular dynamics output file

extMDCRDREF='rst7'  # AMBER molecular dynamics reference coordinate file
extMDRST='rst7'  # AMBER molecular dynamics reference coordinate file

extMININFO='mininfo'
extHEATINFO='heatinfo'
extEQUIINFO='equiinfo'
extMDINFO='mdinfo'  # AMBER molecular dynamics simulation information file

extMINLOG='minlog'
extHEATLOG='heatlog'
extEQUILOG='equilog'
extMDLOG='mdlog'  # AMBER molecular dynamics simulation log file
# Docking-related extensions
# Grafting-related extensions

##
## Modifiers - separated by underscores
##
modAMBER='AMBER'  # non-AMBER files formatted for use with AMBER utilities
modION='Ion'  # a structure containing a charged molecule with counter-ions
modSOLV='Sol' # a solvated structure
modNOH='noh'  # a structure file from which hydrogens have been removed

##
## Global Names - do not change with project
##
SMAP_Actual='Structure_Mapping_Table.txt' # maps rotamers to directory names, 
                                          # Official version, touched only by wev server.
SMAP='Shadow_Mapping_Table.txt'  # copy of SMAP_Actual, used by submission scripts
FFINFO='Force_Field_Info.txt' # lists force fields used to generate structures
GVIZ='Graphviz_SNFG_script.dot' # file used to make the SNFG image
RMAP='Residue_Mapping_Table.txt' # Maps input PDB residues to output residues
SNFG_SVG='SNFG.svg' # SVG file of the SNFG image
SNFG_PNG='SNFG.png' # PNG file of the SNFG image
SUB_OSM_PREF='Run' # Submission script prefix, OS-modeling
}
