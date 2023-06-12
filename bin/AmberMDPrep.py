#!/usr/bin/env python3
import sys
import os
from pathlib import Path

GemsPath = os.environ.get("GEMSHOME")
sys.path.append(GemsPath)  # Required for import gmml
import gmml

USAGE = """
\nUsage: AmberMDPrep.py inputPdbFile
Exmpl: python3 bin/AmberMDPrep.py tests/inputs/016.AmberMDPrep.4mbzEdit.pdb
\n"""
if len(sys.argv) != 2:
    print(USAGE)
    sys.exit()


def main():
    pdbFileName = sys.argv[1]
    pdbFile = gmml.cds_PdbFile(pdbFileName)
    options = gmml.PreprocessorOptions()

    options.chainNTermination_ = "NH3+"  # aka zwitterionic
    options.chainCTermination_ = "CO2-"  # aka zwitterionic
    options.gapNTermination_ = "COCH3"  # aka ACE
    options.gapCTermination_ = "NHCH3"  # aka NME
    options.hisSelections_.append(("HIS_20_?_A_1", "HID"))

    ppInfo = pdbFile.PreProcess(options)
    pdbFile.Write("./preprocessed.pdb")

    # Build the output string
    output = ""
    output += "Unrecognized atoms:\n"
    for unrecognized in ppInfo.unrecognizedAtoms_:
        output += f"{unrecognized.name_} | {unrecognized.residue_.getName()} | {unrecognized.residue_.getChainId()} | {unrecognized.residue_.getNumberAndInsertionCode()}\n"
    output += "\nMissing heavy atoms:\n"
    for missing in ppInfo.missingHeavyAtoms_:
        output += f"{missing.name_} | {missing.residue_.getName()} | {missing.residue_.getChainId()} | {missing.residue_.getNumberAndInsertionCode()}\n"
    output += "\nUnrecognized residues:\n"
    for unrecognized in ppInfo.unrecognizedResidues_:
        output += f"{unrecognized.getName()} | {unrecognized.getChainId()} | {unrecognized.getNumberAndInsertionCode()}\n"
    output += "\nGaps in amino acid chain:\n"
    for gap in ppInfo.missingResidues_:
        output += f"{gap.chainId_} | {gap.residueBeforeGap_} | {gap.residueAfterGap_} | {gap.terminationBeforeGap_} | {gap.terminationAfterGap_}\n"
    output += "\nHistidine Protonation:\n"
    for his in ppInfo.hisResidues_:
        output += f"{his.getName()} | {his.getChainId()} | {his.getNumberAndInsertionCode()}\n"
    output += "\nDisulphide bonds:\n"
    for cysBond in ppInfo.cysBondResidues_:
        output += f"{cysBond.residue1_.getChainId()} | {cysBond.residue1_.getName()} | {cysBond.residue1_.getNumberAndInsertionCode()} | {cysBond.distance_:.2f} | {cysBond.residue2_.getChainId()} | {cysBond.residue2_.getName()} | {cysBond.residue2_.getNumberAndInsertionCode()}\n"
    output += "\nChain terminations:\n"
    for chainT in ppInfo.chainTerminals_:
        output += f"{chainT.chainId_} | {chainT.startIndex_} | {chainT.nTermination_} | {chainT.endIndex_} | {chainT.cTermination_}\n"
    output += "\nWe made it to the end. Congratulations!\n"

    print(output)

    sys.exit(0)


## Now we call the main function.
if __name__ == "__main__":
    main()
