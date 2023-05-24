#!/usr/bin/env python3
import sys
import os
#import json
from pathlib import Path

# check out the environment
GemsPath = os.environ.get('GEMSHOME')
# import gems/gmml stuff
sys.path.append(GemsPath) # is this required for import gmml??
import gmml

## Defining the Usage Statement
USAGE="""

AmberMDPrep.py [ OPTIONS ] [ SEQUENCE ]

OPTIONS:
    -v, --verbose           Will be verbose on what is happening. (For Debugging)
    -h, --help              Show this help message and exit.
    -w, --write             Write out a default config file(JSON) and exit.
    -c CONFIG_FILE          CONFIG_FILE is the path to the config file(JSON) used.
    
CONFIG_FILE:
    
SEQUENCE:

"""
## Declare and define the main function.
def main():
    pdbFile = gmml.cds_PdbFile("tests/inputs/016.AmberMDPrep.4mbzEdit.pdb")
    options = gmml.PreprocessorOptions() # Default values are good, but here I show how you change them:
    options.chainNTermination_ = "NH3+" # aka zwitterionic
    options.chainCTermination_ = "CO2-" # aka zwitterionic
    options.gapNTermination_ = "COCH3" # aka ACE
    options.gapCTermination_ = "NHCH3" # aka NME
    # Not sure how to set hisSelections_ in Python:
    # std::vector<std::pair<std::string,std::string>> hisSelections_; // e.g. pair: residue id like this <"HIS_20_?_A_1", "HID">
    #gmml.PreprocessorInformation 
    ppInfo = pdbFile.PreProcess(options);
    pdbFile.Write("./preprocessed.pdb")
    # Just showing what's in the ppInfo and how to access it
    print( "Unrecognized atoms:")
    for unrecognized in ppInfo.unrecognizedAtoms_:
        print( unrecognized.name_ , " | " , unrecognized.residue_.getName() , " | " , unrecognized.residue_.getChainId() , " | " , unrecognized.residue_.getNumberAndInsertionCode() )
    print( "Missing heavy atoms:")
    for missing in ppInfo.missingHeavyAtoms_:
        print( missing.name_ , " | " , missing.residue_.getName() , " | " , missing.residue_.getChainId() , " | " , missing.residue_.getNumberAndInsertionCode() )
    print( "Unrecognized residues:")
    for unrecognized in ppInfo.unrecognizedResidues_:
        print( unrecognized.getName() , " | " , unrecognized.getChainId() , " | " , unrecognized.getNumberAndInsertionCode() )
    print( "Gaps in amino acid chain:")
    for gap in ppInfo.missingResidues_:
        print( gap.chainId_ , " | " , gap.residueBeforeGap_ , " | " , gap.residueAfterGap_ , " | " , gap.terminationBeforeGap_ , " | " , gap.terminationAfterGap_ )
    print( "Histidine Protonation:")
    for his in ppInfo.hisResidues_:
        print( his.getName() , " | " , his.getChainId() , " | " , his.getNumberAndInsertionCode() )
    print( "Disulphide bonds:")
    for cysBond in ppInfo.cysBondResidues_:
        print( cysBond.residue1_.getChainId() , " | " ,  cysBond.residue1_.getName() , " | " ,  cysBond.residue1_.getNumberAndInsertionCode() , " | " ,  "{:.2f}".format(cysBond.distance_) , " | " , cysBond.residue2_.getChainId() , " | " ,  cysBond.residue2_.getName() , " | " ,  cysBond.residue2_.getNumberAndInsertionCode() )
    print( "Chain terminations:")
    for chainT in ppInfo.chainTerminals_:   
        print( chainT.chainId_ , " | " , chainT.startIndex_ , " | " , chainT.nTermination_ ,  " | " , chainT.endIndex_ , " | " , chainT.cTermination_ )
    print("We made it to the end. Congratulations!")
    ## We made it! :)
    sys.exit(0)

## Now we call main function.
if __name__ == "__main__":
    main()
