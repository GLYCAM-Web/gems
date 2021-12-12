#!/usr/bin/env python3
import sys
import os
import json
from pathlib import Path
from pydantic import BaseModel, Field, ValidationError, validator



# check out the environment
GemsPath = os.environ.get('GEMSHOME')
if GemsPath == None:
    print("""

Must set GEMSHOME environment variable

    BASH:  export GEMSHOME=/path/to/gems
    SH:    setenv GEMSHOME /path/to/gems

""")
    sys.exit(1)

# import gems/gmml stuff
sys.path.append(GemsPath)
import gmml

## Defining the Usage Statement
USAGE="""

GlycoproteinBuilder.py [ GPBINPUTFILE ] 
GPBINPUTFILE:
    Example here: .

"""

# OG StackO example, maybe a way that we can have pseudo-constructors guarantee some state for us.
# class PleaseCoorperate(BaseModel):
#     self0: str
#     next0: str
#     @classmethod
#     def custom_init(cls, page: int, total: int, size: int):
#         # Do some math here and later set the values
#         self0 = ""
#         next0 = ""
#         return cls(self0=self0, next0=next0)
# x = PleaseCoorperate.custom_init(10, 10, 10)


## OG Never tested code, just showing what it might look like:
# class TheGlycosylationSiteInput(BaseModel):
#     proteinResidueId : str = None  # E.g. ?_20 if no chain ID and residue number is 20. C_20 if chain id is C.
#     glycanInputType : str = None # "Library" if pre-build as a pdb file (not implemented for website) or "Sequence" if glycam condensed nomenclature.
#     glycanInput :  str = None # E.g. E.g. DGlcpNAcb1-4DGlcpNAcb1-OH if "Sequence".

# class GlycoproteinBuilderInputs(BaseModel): 
#     workingDirectory : str = None
#     prepFileLocation : str = None
#     substrateFileName : str = None
#     number3DStructures : str = None
#     maxThreads : str = None
#     presistCycles : str = None 
#     overlapTolerance : str = None
#     isDeterministic : str = None
#     glycositesInputVector : List[TheGlycosylationSiteInput] = [] 

#     @classmethod
#     def with_defaults():
#         workingDirectory = "Default"
#         prepFileLocation = "Default"
#         substrateFileName = "Undefined"
#         number3DStructures = "1"
#         maxThreads = "1" 
#         presistCycles = "5"
#         overlapTolerance = "0.1"
#         isDeterministic = "false"

#     @classmethod
#     def with_gmmlClass(gpbInputs):
#         workingDirectory = gpbInputs.workingDirectory_

        

## Declare and define the main function.
def main():
    
    # The gmml level builder uses an input file and a function to fill in this struct. Here I imagine we want to convert from JSON, so I'm showing how to explicitely set stuff.
    gpbInStruct = gmml.GlycoproteinBuilderInputs()
    gpbInStruct.substrateFileName_ = "gmml/tests/tests/inputs/017.1eer_eop_Asn.pdb"
    gpbInStruct.isDeterministic_ = "true" # Only good for testing, so you get the same 3D structure each time. Don't do this in live site, overlap algo is better with rng.
    gpbInStruct.prepFileLocation_ = "gmml/dat/prep/GLYCAM_06j-1_GAGS.prep" # "Default" doesn't work at gems level.
    glycositeInputA = gmml.GlycositeInput("F_24", "Sequence", "DManpa1-6[DManpa1-2DManpa1-2DManpa1-3]DManpb1-4DGlcpNAcb1-4DGlcpNAcb1-OH")
    glycositeInputB = gmml.GlycositeInput("A_40", "Sequence", "DGalpNAca1-OH")
    gpbInStruct.glycositesInputVector_.append(glycositeInputA)
    gpbInStruct.glycositesInputVector_.append(glycositeInputB)

    gpBuilder = gmml.GlycoproteinBuilder(gpbInStruct)
    gpBuilder.ResolveOverlaps()
    gpBuilder.WriteOutputFiles()
    
    sys.exit(0)

## Now we call main function.
if __name__ == "__main__":
    main()

