import gmml
import os
from typing import Optional

from gemsModules.logging.logger import Set_Up_Logging

from gemsModules.structurefile.PDBFile.swig_api import (
    cds_PdbFile,
    PreprocessorInformation,
    PreprocessorOptions,
)

log = Set_Up_Logging(__name__)


# N.B. execute is not validated by pydantic currently
def execute(
    input_pdb_path: str,
    output_pdb_path: str = "./preprocessed.pdb",
    options: Optional[PreprocessorOptions] = None,
) -> PreprocessorInformation:
    """Prepare an Amber MD input file

    options: dict
        A dictionary of options to pass to the preprocessor. See the
        `PreprocessorOptions` class in the `gmml` module for details.

    >>> "Congratulations" in execute("tests/inputs/016.AmberMDPrep.4mbzEdit.pdb")
    True
    """

    # Use all gmml defaults
    if options is None:
        options = PreprocessorOptions()
    else:
        log.debug(f"PPP: {options}")
        options = PreprocessorOptions(**options)

    pdb_file = cds_PdbFile(path=input_pdb_path)
    pp_info = pdb_file.PreProcess(options)

    log.debug(f"Attempting to writing a preprocessed PDB file to {output_pdb_path}...")
    pdb_file.Write(output_pdb_path)
    if not os.path.exists(output_pdb_path):
        log.warning(f"GMML failed to write preprocessed PDB file to {output_pdb_path}!")

    log.debug(f"Prepare_PDB Created pp_info from {options=}.")
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
