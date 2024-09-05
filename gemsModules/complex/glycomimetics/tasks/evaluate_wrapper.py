import subprocess
import os

from ..services.common_api import Modification_Position


# Do not use GM_Utils validation - the webtool has fixes.
# TODO: Use the Instance Config to get the Glycomimetics Webtool path
#EVALUATE_EXE="/programs/glycomimeticsWebtool/internal/glycomimetics/validation/main.exe"
EVALUATE_EXE = "$GEMSHOME/External/GM_Utils/external_programs/validation/main.exe"
EVALUATE_EXE = os.path.expandvars(EVALUATE_EXE)
EVALUATE_WRAPPER = os.path.join(os.path.dirname(__file__), "evaluate_wrapper.sh")


def execute(parent_dir, pdb_filename: str, evaluate_exe: str = EVALUATE_EXE):
    os.chdir(parent_dir)
    result = subprocess.run([EVALUATE_WRAPPER, parent_dir, pdb_filename, evaluate_exe])
    if result.returncode != 0:
        raise RuntimeError(f"Error running Evaluation step, return code: {result.returncode}")
    
    # Position Modifications
    with open(os.path.join(parent_dir, "available_atoms.txt")) as f:
        available_atoms = f.read().splitlines()
    
    for line in available_atoms:
        mp = line.split('-')
        yield Modification_Position(
            Residue_Identifier=mp[0],
            Residue_Name=mp[1],
            Chain_Identifier=mp[2],
            Attachment_Atom=mp[3],
            Replaced_Atom=mp[4]
        )
        
