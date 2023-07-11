#!/usr/bin/env python3
import sys
import os
from pathlib import Path

GemsPath = os.environ.get('GEMSHOME')
sys.path.append(GemsPath) #Required for import gmml
import gmml

USAGE="""
\nUsage: AmberMDPrep.py inputPdbFile
Exmpl: python3 bin/AmberMDPrep.py tests/inputs/016.AmberMDPrep.4mbzEdit.pdb
\n"""
if len(sys.argv) != 2:
    print(USAGE)
    sys.exit()

def main():
    pdbFileName = sys.argv[1]
    pdbFile = gmml.cds_PdbFile(pdbFileName)
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
