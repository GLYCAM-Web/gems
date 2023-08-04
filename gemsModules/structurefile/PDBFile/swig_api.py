import pydantic
import gmml

# A far cry from good:
# class SwigModel(pydantic.BaseModel):
#     # cannot be set, has to be built from the swigpyobject, is not a field to set yourself
#     swigobj: pydantic.typing.Any = pydantic.Field(default_factory=object)

#     # Note: This probably needs to be implemented in swig so the swigpyobject itself provides something compatible with BaseModel construction.
#     @staticmethod
#     def try_from_swigpyobject(spobj: pydantic.typing.Any) -> "SwigModel":
#         raise NotImplementedError(
#             "This is an abstract method, it must be implemented by the inheriting class."
#         )

#     @root_validator(pre=True)
#     def parse_swig_object(cls, values: dict):
#         # This is non trivial, because values is supposed to be a dict, but we want to pass BaseModel(SwigPyObject) (ideally **SwigPyObject.__fields__ or similar, but that's not possible.)
#         # Essentially, we need to run try_from_swigpyobject on values before they even get to the validator.
#         # This is not possible with Pydantic, as it expects values to already be formatted dict it can validate.

#         # this does not work, as the validator "coerces" values into a dict. It seems we must manually call try_from_swigpyobject on values before the validator.
#         values = cls.try_from_swigpyobject(values)

#         # Because the above cannot work, we have to do this manually.

#         return values

# # Note: All this could be done away with if we move the construction logic of BaseModel to swig - gmml's interface file.


class PreprocessorOptions(pydantic.BaseModel):  # SwigModel):
    """Pydantic model for gmml.PreprocessorOptions(), which is used for gmml.PreProcess()

    The gmml defaults are:
        chainNTermination = "NH3+"
        chainCTermination = "CO2-"
        gapNTermination = "COCH3"
        gapCTermination = "NHCH3"
    """

    chainNTermination_: str = pydantic.Field(
        default=None,
        alias="chainNtermination",
        description="The residue name of the N-terminus of the chain, defaults to NH3+.",
    )
    # TODO: Should we make these default to None to not shadow gmml?
    chainCTermination_: str = pydantic.Field(
        default=None,
        alias="chainCtermination",
        description="The residue name of the C-terminus of the chain, defaults to CO2-.",
    )
    gapNTermination_: str = pydantic.Field(
        default=None,
        alias="gapNtermination",
        description="The residue name of the N-terminus of the gap residue, defaults to COCH3.",
    )
    gapCTermination_: str = pydantic.Field(
        default=None,
        alias="gapCtermination",
        description="The residue name of the C-terminus of the gap residue, defaults to NHCH3.",
    )
    hisSelections_: list[tuple[str, str]] = pydantic.Field(
        default_factory=list,
        alias="hisSelections",
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

        # We acheck every field to make sure gmml can pass it's defaults.
        if self.chainNTermination_ is not None:
            options.chainNtermination_ = self.chainNTermination_
        if self.chainCTermination_ is not None:
            options.chainCtermination_ = self.chainCTermination_
        if self.gapNTermination_ is not None:
            options.gapNtermination_ = self.gapNTermination_
        if self.gapCTermination_ is not None:
            options.gapCtermination_ = self.gapCTermination_

        # this must be done because options.hisSelections_ is a raw swig std::Vector<Pair> wrapper. (only an iterator, not a list)
        if len(self.hisSelections_):
            for selection in self.hisSelections_:
                options.hisSelections_.append(selection)

        return options

    @staticmethod
    def try_from_swigpyobject(spobj: gmml.PreprocessorOptions) -> "PreprocessorOptions":
        """Try to create a PreprocessorOptions object from a swigpyobject.

        Note: Ideally, swig would produce the Pydantic.BaseModel compatible wrappers for us,
        these methods are an annoying work-around as Pydantic validators only support dicts of
        fields as input and we cannot transform them before the validator with Pydantic.

        This is a hacky workaround for the fact that Pydantic doesn't support swigpyobjects, and swigpyobjects are actually generic wrappers for specialized gmml classes.
        It converts a generic SwigPyOjbect wrapper to the appropriate gems BaseModel for the gmml class.

        As such, it needs custom logic for each class. Swig should probably handle this logic itself, in the future.

        - If we were to try to pass the swigpyobject.__dict__ directly to the constructor, we would not be able to find the appropriate fields from all the attributes.
        - If we were to try to use the swigpyobject directly with Pydantic, we would not be able to use the private member getters as appropriate with a validator.
            - This is because a BaseModel constructor expects a dict of fields, and without extracting the fields manually for each gmml Class wrapped by swig, we cannot create such a dict.
            - there is no way to transform the values input to a validator before the validator, meaning we cannot pass a SwigPyObject to a validator and have it work.
                - We could pass SwigPyObject.__dict__, but to process this, we'd have to know the fields of the swigpyobject, which we cannot get from the swigpyobject dynamically, demanding a custom interface like the try_from_swigpyobject methods.
                    - Doing so would end up with BaseModels that have to be constructed like such: BaseModel(**gmml.SwigPyObject.__dict__) where SwigPyObject represents any of the gmml classes wrapped by swig.
        """
        # Because PydanticModel validates on construction or coerces the input into a dict,
        # which can not be appropriate for all SwigPyObject-wrapped gmml classes, we need
        # to manually build the dict of fields to pass to the constructor instead.
        return PreprocessorOptions(
            # pydantic aliases affect the field names, so we need to use the alias names here..
            chainNTermination_=spobj.chainNtermination_,
            chainCTermination_=spobj.chainCtermination_,
            gapNTermination_=spobj.gapNtermination_,
            gapCtermination_=spobj.gapCtermination_,
            hisSelections_=spobj.hisSelections_,
        )
        # If we could get the validator to apply try_from_swigpyobject to the values before the validator, we could just pass the swigpyobject.__dict__ to the constructor - if all gmml interfaces were unified.
        # However, because they aren't we still need to manually build python dicts for each gmml class wrapped by swig to access the class's public members and attributes appropriately.
        # return {
        #     "chainNTermination_": spobj.chainNtermination_,
        #     "chainCTermination_": spobj.chainCtermination_,
        #     "gapNTermination_": spobj.gapNtermination_,
        #     "gapCtermination_": spobj.gapCtermination_,
        #     "hisSelections_": spobj.hisSelections_,
        # }


class ResidueId(pydantic.BaseModel):
    residueName: str = pydantic.Field(alias="residueName_")
    sequenceNumber: str = pydantic.Field(alias="sequenceNumber_")
    insertionCode: str = pydantic.Field(alias="insertionCode_")
    chainId: str = pydantic.Field(alias="chainId_")
    alternativeLocation: str = pydantic.Field(alias="alternativeLocation_")

    @staticmethod
    def try_from_swigpyobject(spobj: gmml.ResidueId) -> "ResidueId":
        """Try to create a ResidueId object from a swigpyobject.

        This is a hacky workaround for the fact that Pydantic doesn't support swigpyobjects and swigpyobjects are actually generic wrappers for specialized gmml classes.
        """
        return ResidueId(
            # Again, we can't just use the swig object, instead we're using the private member getters.
            # Because of the diverse ways the actual gmml code works, and the lack of unified swig interface, we can not generalize this static method for preparsing a validator's input.
            # (On top of the fact pydantic doesn't let us do that. If SwigPyObject provided __fields__ this might be different)
            residueName_=spobj.getName(),
            sequenceNumber_=spobj.getNumber(),
            insertionCode_=spobj.getInsertionCode(),
            chainId_=spobj.getChainId(),
            alternativeLocation_=spobj.getAlternativeLocation(),
        )


class AtomInfo(pydantic.BaseModel):
    name: str = pydantic.Field(alias="name_")
    # Note, the original test output expects residue to be unpacked at top level as dict entries with differentfield namesfrom gmml.ResidueId (combined numberAndInsertionCode - for instance)
    residue: ResidueId = pydantic.Field(alias="residue_")

    @staticmethod
    def try_from_swigpyobject(spobj: gmml.AtomInfo) -> "AtomInfo":
        """Try to create an AtomInfo object from a swigpyobject.

        This is a hacky workaround for the fact that Pydantic doesn't support swigpyobjects and swigpyobjects are actually generic wrappers for specialized gmml classes.
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

        This is a hacky workaround for the fact that Pydantic doesn't support swigpyobjects and swigpyobjects are actually generic wrappers for specialized gmml classes.
        """

        return GapInAminoAcidChain(
            # **spobj.__dict__ - This does not work .__dict__ != __fields__, we need custom logic for each spobj because they are generic,
            # but instead wrap specialized gmml classes with different interfaces.
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

        This is a hacky workaround for the fact that Pydantic doesn't support swigpyobjects and swigpyobjects are actually generic wrappers for specialized gmml classes.
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

        This is a hacky workaround for the fact that Pydantic doesn't support swigpyobjects and swigpyobjects are actually generic wrappers for specialized gmml classes.
        """
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


class PreprocessorInformation(pydantic.BaseModel):
    """Pydantic model for gmml.PpInfo, which is returned by gmml.PreProcess()

    Note:
    ---
    The original AmberMDPrep test structures the data differently, for instance we now produce:
       { "atomName": name, "residue": residue } where residue=Residue()
    As opposed to:
       { "atomName": name, "residueName": residueName, "chainId": chainId, "numberAndInsertionCode": numberAndInsertionCode }
    where we extract the fields from the gmml Residue object directly without try_from_swigpyobject.
    """

    unrecognizedAtoms_: list[AtomInfo] = pydantic.Field(
        default_factory=list, alias="unrecognizedAtoms"
    )
    missingHeavyAtoms_: list[AtomInfo] = pydantic.Field(
        default_factory=list, alias="missingHeavyAtoms"
    )
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
    def try_from_swigpyobject(
        spobj: gmml.PreprocessorInformation,
    ) -> "PreprocessorInformation":
        """Try to create a PpInfo object from a swigpyobject.

        This is a hacky workaround for the fact that Pydantic doesn't support swigpyobjects.
        """
        # Because SwigPyObj is not a dict-class or compatible type as expected of most PyObjects, we cannot use the ** operator
        # swig probably could wrap it for us.
        return PreprocessorInformation(
            # Because spobj.field's are Swig Vectors, we cannot treat them as lists w/o the constructor.
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
