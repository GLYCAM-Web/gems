import gmml
import os
import pydantic
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


# TODO: These probably belong elsewhere, but for now prepare_pdb is motivating their creation.
class PreprocessorOptions(pydantic.BaseModel):
    """Pydantic model for gmml.PreprocessorOptions(), which is used for gmml.PreProcess()

    The gmml defaults are:
        chainNTermination = "NH3+"
        chainCTermination = "CO2-"
        gapNTermination = "COCH3"
        gapCTermination = "NHCH3"
    """

    chainNTermination: pydantic.typing.Literal["NH3+", ""] = pydantic.Field(
        default=None,
        alias="chainNtermination_",
        description="The residue name of the N-terminus of the chain, defaults to NH3+.",
    )
    # TODO: Should we make these default to None to not shadow gmml?
    chainCTermination: str = pydantic.Field(
        default=None,
        alias="chainCtermination_",
        description="The residue name of the C-terminus of the chain, defaults to CO2-.",
    )
    gapNTermination: str = pydantic.Field(
        default=None,
        alias="gapNtermination_",
        description="The residue name of the N-terminus of the gap residue, defaults to COCH3.",
    )
    gapCTermination: str = pydantic.Field(
        default=None,
        alias="gapCtermination_",
        description="The residue name of the C-terminus of the gap residue, defaults to NHCH3.",
    )
    hisSelections: list[tuple[str, str]] = pydantic.Field(
        default_factory=list,
        alias="hisSelections_",
        description="A list of histidine selections to use in preprocessing.",
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


class ResidueId(pydantic.BaseModel):
    residueName: str = pydantic.Field(alias="residueName_")
    sequenceNumber: str = pydantic.Field(alias="sequenceNumber_")
    insertionCode: str = pydantic.Field(alias="insertionCode_")
    chainId: str = pydantic.Field(alias="chainId_")
    alternativeLocation: str = pydantic.Field(alias="alternativeLocation_")

    # Can we make pydantic call this for us? Should we really be validating every entry of PpInfo?
    @staticmethod
    def try_from_swigpyobject(spobj: gmml.ResidueId) -> "ResidueId":
        """Try to create a ResidueId object from a swigpyobject."""
        return ResidueId(
            # Again, we can't just use the swig object, instead we're using the private member getters.
            residueName_=spobj.getName(),
            sequenceNumber_=spobj.getNumber(),
            insertionCode_=spobj.getInsertionCode(),
            chainId_=spobj.getChainId(),
            alternativeLocation_=spobj.getAlternativeLocation(),
        )


class AtomInfo(pydantic.BaseModel):
    name: str = pydantic.Field(alias="name_")
    # Note, the original test output expects residue to be unpacked at top level as dict entries with different field names from gmml.ResidueId (numberAndInsertionCode - for instance)
    residue: ResidueId = pydantic.Field(alias="residue_")

    @staticmethod
    def try_from_swigpyobject(spobj: gmml.AtomInfo) -> "AtomInfo":
        """Try to create an AtomInfo object from a swigpyobject.

        This is a hacky workaround for the fact that Pydantic doesn't support swigpyobjects.
        """
        return AtomInfo(
            name_=spobj.name_, residue_=ResidueId.try_from_swigpyobject(spobj.residue_)
        )


class GapInAminoAcidChain(pydantic.BaseModel):
    chainId: str = pydantic.Field(alias="chainId_")
    # should these be ResidueIds?
    residueBeforeGap: str = pydantic.Field(alias="residueBeforeGap_")
    residueAfterGap: str = pydantic.Field(alias="residueAfterGap_")
    terminationBeforeGap: str = pydantic.Field(alias="terminationBeforeGap_")
    terminationAfterGap: str = pydantic.Field(alias="terminationAfterGap_")

    @staticmethod
    def try_from_swigpyobject(spobj: gmml.GapInAminoAcidChain) -> "GapInAminoAcidChain":
        """Try to create a GapInAminoAcidChain object from a swigpyobject.

        This is a hacky workaround for the fact that Pydantic doesn't support swigpyobjects.
        """

        return GapInAminoAcidChain(
            chainId_=spobj.chainId_,
            # These are strings in gmml, but need to be residues, probably. Lets ignore for now
            # residueBeforeGap_=ResidueId.try_from_swigpyobject(spobj.residueBeforeGap_),
            # residueAfterGap_=ResidueId.try_from_swigpyobject(spobj.residueAfterGap_),
            residueBeforeGap_=spobj.residueBeforeGap_,
            residueAfterGap_=spobj.residueAfterGap_,
            # These probably shoudl be some sort of Id as well instead of strings.
            terminationBeforeGap_=spobj.terminationBeforeGap_,
            terminationAfterGap_=spobj.terminationAfterGap_,
        )


class DisulphideBond(pydantic.BaseModel):
    residue1: ResidueId = pydantic.Field(alias="residue1_")
    distance: float = pydantic.Field(alias="distance_")
    residue2: ResidueId = pydantic.Field(alias="residue2_")

    @staticmethod
    def try_from_swigpyobject(spobj: gmml.DisulphideBond) -> "DisulphideBond":
        """Try to create a DisulphideBond object from a swigpyobject.

        This is a hacky workaround for the fact that Pydantic doesn't support swigpyobjects.
        """
        return DisulphideBond(
            residue1_=ResidueId.try_from_swigpyobject(spobj.residue1_),
            distance_=spobj.distance_,
            residue2_=ResidueId.try_from_swigpyobject(spobj.residue2_),
        )


class ChainTerminal(pydantic.BaseModel):
    chainId: str = pydantic.Field(alias="chainId_")
    startIndex: int = pydantic.Field(alias="startIndex_")
    endIndex: int = pydantic.Field(alias="endIndex_")
    nTermination: str = pydantic.Field(alias="nTermination_")
    cTermination: str = pydantic.Field(alias="cTermination_")

    @staticmethod
    def try_from_swigpyobject(spobj: gmml.ChainTerminal) -> "ChainTerminal":
        """Try to create a ChainTerminal object from a swigpyobject.

        This is a hacky workaround for the fact that Pydantic doesn't support swigpyobjects.
        """
        log.debug(
            f" Attempting to create ChainTerminal from {spobj}:\nspobj.chainId_={spobj.chainId_}\nspobj.startIndex_={spobj.startIndex_}\nspobj.endIndex_={spobj.endIndex_}\nspobj.nTermination_={spobj.nTermination_}\nspobj.cTermination_={spobj.cTermination_}"
        )

        return ChainTerminal(
            # No private getters, just access the members directly, remember, we cannot use dict unpacking on swigpyobjects.
            chainId_=spobj.chainId_,
            startIndex_=spobj.startIndex_,
            endIndex_=spobj.endIndex_,
            nTermination_=spobj.nTermination_,
            cTermination_=spobj.cTermination_,
        )


class NonNaturalProteinResidue(pydantic.BaseModel):
    residue: ResidueId = pydantic.Field(alias="residue_")

    @staticmethod
    def try_from_swigpyobject(
        spobj: gmml.NonNaturalProteinResidue,
    ) -> "NonNaturalProteinResidue":
        """Try to create a NonNaturalProteinResidue object from a swigpyobject.

        This is a hacky workaround for the fact that Pydantic doesn't support swigpyobjects.
        """
        return NonNaturalProteinResidue(
            residue_=ResidueId.try_from_swigpyobject(spobj.residue_)
        )


class PpInfo(pydantic.BaseModel):
    """Pydantic model for gmml.PpInfo, which is returned by gmml.PreProcess()"""

    unrecognizedAtoms_: list[AtomInfo] = pydantic.Field(
        default_factory=list, alias="unrecognizedAtoms"
    )
    missingHeavyAtoms_: list[AtomInfo] = pydantic.Field(
        default_factory=list, alias="missingHeavyAtoms"
    )
    # Note, the original test structures the fields differently, as w/ AtomInfo comment.
    unrecognizedResidues_: list[ResidueId] = pydantic.Field(
        default_factory=list, alias="unrecognizedResidues"
    )
    missingResidues_: list[GapInAminoAcidChain] = pydantic.Field(
        default_factory=list, alias="missingResidues"
    )
    hisResidues_: list[ResidueId] = pydantic.Field(
        default_factory=list, alias="hisResidues"
    )
    cysBondResidues_: list[DisulphideBond] = pydantic.Field(
        default_factory=list, alias="cysBondResidues"
    )
    chainTerminals_: list[ChainTerminal] = pydantic.Field(
        default_factory=list, alias="chainTerminals"
    )

    @staticmethod
    def try_from_swigpyobject(spobj: gmml.PreprocessorInformation) -> "PpInfo":
        """Try to create a PpInfo object from a swigpyobject.

        This is a hacky workaround for the fact that Pydantic doesn't support swigpyobjects.
        """
        # Because SwigPyObj is not a dict-class or compatible type as expected of most PyObjects, we cannot use the ** operator
        # swig probably could wrap it for us.
        return PpInfo(
            # Because spobj.field_'s are Swig Vectors, we cannot treat them as lists w/o the constructor.
            # This seems costly, swig should be able to do this, probably.
            unrecognizedAtoms=[
                AtomInfo.try_from_swigpyobject(ai) for ai in spobj.unrecognizedAtoms_
            ],
            missingHeavyAtoms=[
                AtomInfo.try_from_swigpyobject(ai) for ai in spobj.missingHeavyAtoms_
            ],
            unrecognizedResidues=[
                ResidueId.try_from_swigpyobject(ri)
                for ri in spobj.unrecognizedResidues_
                if ri != ""
            ],
            missingResidues=[
                GapInAminoAcidChain.try_from_swigpyobject(gi)
                for gi in spobj.missingResidues_
            ],
            hisResidues=[
                ResidueId.try_from_swigpyobject(hi)
                for hi in spobj.hisResidues_
                if hi != ""
            ],
            cysBondResidues=[
                DisulphideBond.try_from_swigpyobject(cb)
                for cb in spobj.cysBondResidues_
            ],
            chainTerminals=[
                ChainTerminal.try_from_swigpyobject(ct) for ct in spobj.chainTerminals_
            ],
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
    return PpInfo.try_from_swigpyobject(pdb_file.PreProcess(options)), cds_PdbFile(
        pdbfile=pdb_file
    )


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
) -> PpInfo:
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

    # The nice thing about below, is we don't validate the PpInfo contents, as Gems probably shouldn't have the scientific knowledge to validate it.
    # Build the output dict
    # output = {}
    # output["unrecognizedAtoms"] = [
    #     {
    #         "atomName": {a.name_},
    #         "residueName": a.residue_.getName(),
    #         "chainId": a.residue_.getChainId(),
    #         "numberAndInsertionCode": a.residue_.getNumberAndInsertionCode(),
    #     }
    #     # It seems we can do this because these swig objects are iterable, not because they're lists.
    #     for a in pp_info.unrecognizedAtoms_
    # ]
    # output["missingHeavyAtoms"] = [
    #     {
    #         "atomName": {a.name_},
    #         "residueName": a.residue_.getName(),
    #         "chainId": a.residue_.getChainId(),
    #         "numberAndInsertionCode": a.residue_.getNumberAndInsertionCode(),
    #     }
    #     for a in pp_info.missingHeavyAtoms_
    # ]r
    # output["unrecognizedResidues"] = [
    #     {
    #         "residueName": {r.getName()},
    #         "chainId": r.getChainId(),
    #         "numberAndInsertionCode": r.getNumberAndInsertionCode(),
    #     }
    #     for r in pp_info.unrecognizedResidues_
    # ]

    # output["missingResidues"] = [
    #     {
    #         "chainId": r.chainId_,
    #         "residueBeforeGap": r.residueBeforeGap_,
    #         "residueAfterGap": r.residueAfterGap_,
    #         "terminationBeforeGap": r.terminationBeforeGap_,
    #         "terminationAfterGap": r.terminationAfterGap_,
    #     }
    #     for r in pp_info.missingResidues_
    # ]

    # output["hisResidues"] = [
    #     {
    #         "chainId": r.getChainId(),
    #         "residueName": r.getName(),
    #         "numberAndInsertionCode": r.getNumberAndInsertionCode(),
    #     }
    #     for r in pp_info.hisResidues_
    # ]

    # output["cysBondResidues"] = [
    #     {
    #         "residue1": {
    #             "chainId": r.residue1_.getChainId(),
    #             "residueName": r.residue1_.getName(),
    #             "numberAndInsertionCode": r.residue1_.getNumberAndInsertionCode(),
    #         },
    #         "distance": r.distance_,
    #         "residue2": {
    #             "chainId": r.residue2_.getChainId(),
    #             "residueName": r.residue2_.getName(),
    #             "numberAndInsertionCode": r.residue2_.getNumberAndInsertionCode(),
    #         },
    #     }
    #     for r in pp_info.cysBondResidues_
    # ]

    # We can ignore the fact that GapInAminoAcidChain's C++ definition is a string, need info from the residue id if we were to build this up using ResidueID or respect GapInAminoAcidChain's C++ definition.
    # output["chainTerminals"] = [
    #     {
    #         "chainId": ct.chainId_,
    #         "startIndex": ct.startIndex_,
    #         "endIndex": ct.endIndex_,
    #         "nTermination": ct.nTermination_,
    #         "cTermination": ct.cTermination_,
    #     }
    #     for ct in pp_info.chainTerminals_
    # ]

    log.debug(f"pp_info: {pp_info}")
    return pp_info


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
