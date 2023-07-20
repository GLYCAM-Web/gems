import gmml
import os
import pydantic
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


# TODO: These probably belong elsewhere, but for now prepare_pdb is motivating their creation.
class PreprocessorOptions(pydantic.BaseModel):
    """Pydantic model for gmml.PreprocessorOptions(), which is used for gmml.PreProcess()"""

    chainNTermination: pydantic.typing.Literal["NH3+", ""] = pydantic.Field(
        default="NH3+", alias="chainNtermination_"
    )
    chainCTermination: str = pydantic.Field(default="CO2-", alias="chainCtermination_")
    gapNTermination: str = pydantic.Field(default="COCH3", alias="gapNtermination_")
    gapCTermination: str = pydantic.Field(default="NHCH3", alias="gapCtermination_")
    hisSelections: list[tuple[str, str]] = pydantic.Field(
        default_factory=list, alias="hisSelections_"
    )

    def append_his_selection(self, selection: tuple[str, str]):
        """Append a histidine selection to the hisSelections list.

        selection: tuple[str, str]
            - A tuple of the form   ("residue name" , selection type)
            - For example:          ("HIS_20_?_A_1" , "HID")
        """
        self.hisSelections.append(selection)

    def build(self) -> gmml.PreprocessorOptions:
        """Build a gmml.PreprocessorOptions object from this Pydantic model"""
        options = gmml.PreprocessorOptions()

        options.chainNtermination_ = self.chainNTermination
        options.chainCtermination_ = self.chainCTermination
        options.gapNtermination_ = self.gapNTermination
        options.gapCtermination_ = self.gapCTermination
        for selection in self.hisSelections:
            options.hisSelections_.append(selection)

        return options


class PpInfo(pydantic.BaseModel):
    """Pydantic model for gmml.PpInfo, which is returned by gmml.PreProcess()"""

    unrecognizedAtoms: list[str] = pydantic.Field(
        default_factory=list, alias="unrecognizedAtoms_"
    )
    missingHeavyAtoms: list[str] = pydantic.Field(
        default_factory=list, alias="missingHeavyAtoms_"
    )
    unrecognizedResidues: list[str] = pydantic.Field(
        default_factory=list, alias="unrecognizedResidues_"
    )
    missingResidues: list[str] = pydantic.Field(
        default_factory=list, alias="missingResidues_"
    )
    hisResidues: list[str] = pydantic.Field(default_factory=list, alias="hisResidues_")
    cysBondResidues: list[str] = pydantic.Field(
        default_factory=list, alias="cysBondResidues_"
    )
    chainTerminals: list[str] = pydantic.Field(
        default_factory=list, alias="chainTerminals_"
    )


class cds_PdbFile(pydantic.BaseModel):
    """Hacky pydantic wrapper for gmml.cds_PdbFile, which is returned by gmml.cds_PdbFile()"""

    pdbfile: pydantic.typing.Any = pydantic.Field(default_factory=object)

    def Write(self, path: str):
        """Write the PDB file to a path - manually wrapping the gmml.cds_PdbFile.Write() function as an example."""
        self.pdbfile.Write(path)

    @property
    def raw(self) -> pydantic.typing.Any:
        """Return the underlying gmml.cds_PdbFile object - unsafe."""
        return self.pdbfile


def preprocess(
    input_pdb_path: str, options: PreprocessorOptions
) -> tuple[PpInfo, cds_PdbFile]:
    """Run the gmml.PreProcess() function on a PDB file.

    Returns the PpInfo and the cds_PdbFile objects.
    """
    pdb_file = gmml.cds_PdbFile(input_pdb_path)
    return pdb_file.PreProcess(options), cds_PdbFile(pdbfile=pdb_file)


def preprocess_and_write_pdb(
    input_pdb_path: str,
    options: PreprocessorOptions,
    output_pdb_path: str = "./preprocessed.pdb",
) -> tuple[PpInfo, cds_PdbFile]:
    """Preprocess a PDB file and write it.

    Returns the ppInfo and the cds_PdbFile objects.
    """
    pp_info, pdb_file = preprocess(input_pdb_path, options)
    log.debug(f"Writing preprocessed PDB file to {output_pdb_path}...")
    pdb_file.raw.Write(output_pdb_path)
    if not os.path.exists(output_pdb_path):
        log.warning(f"GMML failed to write preprocessed PDB file to {output_pdb_path}!")

    return pp_info, pdb_file


def execute(
    input_pdb_path: str,
    output_pdb_path: str = "./preprocessed.pdb",
    options: dict = None,
) -> dict:
    """Prepare an Amber MD input file

    options: dict
        A dictionary of options to pass to the preprocessor. See the
        `PreprocessorOptions` class in the `gmml` module for details.

    >>> "Congratulations" in execute("tests/inputs/016.AmberMDPrep.4mbzEdit.pdb")
    True
    """

    # Demonstration
    if options is None:
        options = PreprocessorOptions().build()
    else:
        options = PreprocessorOptions(**options).build()

    pp_info, _ = preprocess_and_write_pdb(input_pdb_path, options, output_pdb_path)

    # Build the output dict
    output = {}
    output["unrecognizedAtoms"] = [
        {
            "atomName": {a.name_},
            "residueName": a.residue_.getName(),
            "chainId": a.residue_.getChainId(),
            "numberAndInsertionCode": a.residue_.getNumberAndInsertionCode(),
        }
        for a in pp_info.unrecognizedAtoms_
    ]
    output["missingHeavyAtoms"] = [
        {
            "atomName": {a.name_},
            "residueName": a.residue_.getName(),
            "chainId": a.residue_.getChainId(),
            "numberAndInsertionCode": a.residue_.getNumberAndInsertionCode(),
        }
        for a in pp_info.missingHeavyAtoms_
    ]
    output["unrecognizedResidues"] = [
        {
            "residueName": {r.getName()},
            "chainId": r.getChainId(),
            "numberAndInsertionCode": r.getNumberAndInsertionCode(),
        }
        for r in pp_info.unrecognizedResidues_
    ]

    output["missingResidues"] = [
        {
            "chainId": r.chainId_,
            "residueBeforeGap": r.residueBeforeGap_,
            "residueAfterGap": r.residueAfterGap_,
            "terminationBeforeGap": r.terminationBeforeGap_,
            "terminationAfterGap": r.terminationAfterGap_,
        }
        for r in pp_info.missingResidues_
    ]

    output["hisResidues"] = [
        {
            "chainId": r.getChainId(),
            "residueName": r.getName(),
            "numberAndInsertionCode": r.getNumberAndInsertionCode(),
        }
        for r in pp_info.hisResidues_
    ]

    output["cysBondResidues"] = [
        {
            "residue1": {
                "chainId": r.residue1_.getChainId(),
                "residueName": r.residue1_.getName(),
                "numberAndInsertionCode": r.residue1_.getNumberAndInsertionCode(),
            },
            "distance": r.distance_,
            "residue2": {
                "chainId": r.residue2_.getChainId(),
                "residueName": r.residue2_.getName(),
                "numberAndInsertionCode": r.residue2_.getNumberAndInsertionCode(),
            },
        }
        for r in pp_info.cysBondResidues_
    ]

    output["chainTerminals"] = [
        {
            "chainId": ct.chainId_,
            "startIndex": ct.startIndex_,
            "endIndex": ct.endIndex_,
            "nTermination": ct.nTermination_,
            "cTermination": ct.cTermination_,
        }
        for ct in pp_info.chainTerminals_
    ]

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
