from pathlib import Path

from gemsModules.logging.logger import Set_Up_Logging

from ..services.common_api import Modification_Position

log = Set_Up_Logging(__name__)


def execute(position: Modification_Position, project_dir: Path): # , libraries: list, charge: int):
    """ Constructs and writes the input file for the Glycomimetics service.
    
    Ex.
    
    ```
    ComplexPdb:cocomplex.pdbqt
    OpenValence:3_C4_O4_H4-/programs/glycomimetic/library/test1-pdbqt  
    naturalCharge:-1
    ```
    """
    if position is None:
        raise RuntimeError("No valid Position selected.")
    
    # TODO: Libraries from API
    # Something like this maybe? libraries_str = "-".join([f"/programs/glycomimetic/library/{lib}" for lib in position.Moiety_Library_Names])
    libraries_str = "/programs/glycomimetic/library/test1-pdbqt"
    # TODO: Charge from... Ask Yao/Oliver 
    charge_str = "-1"
    
    # Glycomimetics input file format is two lines:
    complex_str = "ComplexPdb:cocomplex.pdbqt"
    open_valence = f"OpenValence:{position.Residue_Identifier}_{position.Attachment_Atom}_{position.Replaced_Atom}_H4-{libraries_str}"
    natural_charge = f"naturalCharge:{charge_str}"
    
    # warn if the input file already exists
    if (project_dir / "input.txt").exists():
        log.warning(f"Warning: {project_dir}/input.txt already exists. Overwriting.")
            
    with open(Path(project_dir) / "input.txt", "w") as f:
        f.write(f"{complex_str}\n{open_valence}\n{natural_charge}\n")