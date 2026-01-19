from pathlib import Path
import gmml
import os

from gemsModules.logging.logger import Set_Up_Logging

from gemsModules.structurefile.PDBFile.swig_api import (
    cds_PdbFile,
    PreprocessorInformation,
    PreprocessorOptions,
)

log = Set_Up_Logging(__name__)


def preprocess(
    input_pdb_path: str, options: PreprocessorOptions
) -> tuple[PreprocessorInformation, cds_PdbFile]:
    """Run the gmml.PreProcess() function on a PDB file.

    Returns the PpInfo and the cds_PdbFile objects.
    """
    pdb_file = gmml.cds_PdbFile(input_pdb_path)
    return PreprocessorInformation.try_from_swigpyobject(
        pdb_file.PreProcess(options)
    ), cds_PdbFile(pdbfile=pdb_file)


def preprocess_and_write_pdb(
    input_pdb_path: str,
    options: PreprocessorOptions,
    output_pdb_path: str = "./preprocessed.pdb",
) -> tuple[PreprocessorInformation, cds_PdbFile]:
    """Preprocess a PDB file and write it.

    Returns the ppInfo and the cds_PdbFile objects.
    """
    pp_info, pdb_file = preprocess(input_pdb_path, options)
    # check if parent path exists:
    if not Path(output_pdb_path).parent.exists():
        log.warning(
            f"Parent directory of {output_pdb_path} does not exist? PM should run before this"
        )
        
    log.debug(f"Attempting to writing a preprocessed PDB file to {output_pdb_path}...")
    pdb_file.raw.Write(output_pdb_path)
    if not os.path.exists(output_pdb_path):
        log.warning(f"GMML failed to write preprocessed PDB file to {output_pdb_path}!")

    return pp_info, pdb_file


def execute(
    input_pdb_path: str,
    output_pdb_path: str = "./preprocessed.pdb",
    options: dict = None,
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
        options = PreprocessorOptions().build()
    else:
        options = PreprocessorOptions(**options).build()

    pp_info, _ = preprocess_and_write_pdb(input_pdb_path, options, output_pdb_path)

    log.debug(f"Prepare_PDB Created {pp_info=} from {options=}.")
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
