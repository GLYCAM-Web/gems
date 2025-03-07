import os 
import subprocess
from gemsModules.systemoperations.environment_ops import get_gems_path


GEMSHOME = get_gems_path()    
GMML_PATH = os.path.join(GEMSHOME, "gmml")
DETECT_SUGARS_BIN = os.path.join(GMML_PATH, "bin", "detect_sugars")


def execute(pdb_path, workdir):
    """Run detect_sugars on a pdb file and capture stdout to generate glycan_ring_atoms.txt"""    
    
    # Run detect_sugars on ligand.pdb to generate glycan_ring_atoms.txt
    # detect_sugars ligand.pdb | tee > glycan_ring_atoms.txt (use an io buffer to both write stodout to file and return it)
    with open("glycan_ring_atoms.txt", "w") as f:
        try:
            subprocess.run([DETECT_SUGARS_BIN, pdb_path], stdout=f, cwd=workdir, check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error running detect_sugars: {e}")
        
    return os.path.join(workdir, "glycan_ring_atoms.txt")


if __name__ == "__main__":
    pdb_path = "/programs/gems/gmml/tests/tests/inputs/4mbz.pdb"
    workdir = os.getcwd()
    execute(pdb_path, workdir)