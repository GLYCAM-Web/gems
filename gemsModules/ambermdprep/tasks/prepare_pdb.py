import gmml


def execute(input_pdb_path: str, output_pdb_path: str = "./preprocessed.pdb") -> str:
    """Prepare an Amber MD input file

    >>> "Congratulations" in execute("tests/inputs/016.AmberMDPrep.4mbzEdit.pdb")
    True
    """

    # Replace with JSON input from delegator.
    pdbFile = gmml.cds_PdbFile(input_pdb_path)

    options = gmml.PreprocessorOptions()
    # The defaults are fine, but we can change them if we want:
    # options.chainNTermination_ = "NH3+"  # aka zwitterionic
    # options.chainCTermination_ = "CO2-"  # aka zwitterionic
    # options.gapNTermination_ = "COCH3"  # aka ACE
    # options.gapCTermination_ = "NHCH3"  # aka NME
    # options.hisSelections_.append(("HIS_20_?_A_1", "HID"))

    ppInfo = pdbFile.PreProcess(options)
    pdbFile.Write(output_pdb_path)

    # Build the output string
    output = ""
    output += "Unrecognized atoms:\n"
    for unrecognized in ppInfo.unrecognizedAtoms_:
        output += f"{unrecognized.name_}  |  {unrecognized.residue_.getName()}  |  {unrecognized.residue_.getChainId()}  |  {unrecognized.residue_.getNumberAndInsertionCode()}\n"
    output += "Missing heavy atoms:\n"
    for missing in ppInfo.missingHeavyAtoms_:
        output += f"{missing.name_}  |  {missing.residue_.getName()}  |  {missing.residue_.getChainId()}  |  {missing.residue_.getNumberAndInsertionCode()}\n"
    output += "Unrecognized residues:\n"
    for unrecognized in ppInfo.unrecognizedResidues_:
        output += f"{unrecognized.getName()}  |  {unrecognized.getChainId()}  |  {unrecognized.getNumberAndInsertionCode()}\n"
    output += "Gaps in amino acid chain:\n"
    for gap in ppInfo.missingResidues_:
        output += f"{gap.chainId_}  |  {gap.residueBeforeGap_}  |  {gap.residueAfterGap_}  |  {gap.terminationBeforeGap_}  |  {gap.terminationAfterGap_}\n"
    output += "Histidine Protonation:\n"
    for his in ppInfo.hisResidues_:
        output += f"{his.getName()}  |  {his.getChainId()}  |  {his.getNumberAndInsertionCode()}\n"
    output += "Disulphide bonds:\n"
    for cysBond in ppInfo.cysBondResidues_:
        output += f"{cysBond.residue1_.getChainId()}  |  {cysBond.residue1_.getName()}  |  {cysBond.residue1_.getNumberAndInsertionCode()}  |  {cysBond.distance_:.2f}  |  {cysBond.residue2_.getChainId()}  |  {cysBond.residue2_.getName()}  |  {cysBond.residue2_.getNumberAndInsertionCode()}\n"
    output += "Chain terminations:\n"
    for chainT in ppInfo.chainTerminals_:
        output += f"{chainT.chainId_}  |  {chainT.startIndex_}  |  {chainT.nTermination_}  |  {chainT.endIndex_}  |  {chainT.cTermination_}\n"
    output += "We made it to the end. Congratulations!\n"

    return output


if __name__ == "__main__":
    import doctest

    results = doctest.testmod()
    if results.failed == 0:
        print(
            f"Congratulations! All {results.attempted} tests passed! "
            "Now removing the test output file..."
        )
        import os

        os.remove("./preprocessed.pdb")
