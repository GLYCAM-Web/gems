from gemsModules.common.code_utils import GemsStrEnum


class Complex_Allowed_File_Formats(GemsStrEnum):
    """
    The file formats that the complex meta-entity knows about and allows.
    """

    PDB = "PDB"
    mmCIF = "mmCIF"
    Mol2 = "Mol2"
    xyz = "xyz"
