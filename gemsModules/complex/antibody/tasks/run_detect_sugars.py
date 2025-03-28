import os 
import subprocess
import gmml
import io 

from gemsModules.systemoperations.environment_ops import get_gems_path

GEMSHOME = get_gems_path()    
#GMML_PATH = os.path.join(GEMSHOME, "gmml")
DETECT_SUGARS_BIN = os.path.join(GEMSHOME, "bin", "detect_sugars.exe")

# Note: Does not agree with detectSugars.cc
# def detect_sugars(pdb_file):
#     aminolibs=gmml.string_vector()
#     aminolibs.push_back(GEMSHOME+"/gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib")

#     #print("aminolibs is >>>"+aminolibs+"<<<.")
#     #print(aminolibs)
#     #sys.exit(0)

#     het = gmml.string_vector()
#     het.push_back(pdb_file)
#     temp = gmml.Assembly(het, gmml.PDB)
#     empty = gmml.string_vector()
#     temp.BuildStructureByDistance(10)

#     # capture the c++ stdout to buffer using context manager
#     # temp.ExtractSugars(aminolibs, False, True) # always prints to stdio, we do not want this
#     # we must redirect and capture stdout ourselves
#     with io.StringIO() as buffer:
#         temp.ExtractSugars(aminolibs, False, True)
#         extracted = buffer.getvalue()
#     return extracted
    

def execute(pdb_path, workdir):
    """Run detect_sugars on a pdb file and capture stdout to generate glycan_ring_atoms.txt"""    
    
    ring_atoms_path = os.path.join(workdir, "glycan_ring_atoms.txt")
    # Run detect_sugars on ligand.pdb to generate glycan_ring_atoms.txt
    with open(ring_atoms_path, "w") as f:
        try:
            subprocess.run([DETECT_SUGARS_BIN, pdb_path], stdout=f, cwd=workdir, check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error running detect_sugars: {e}")
        # try:
        #     extracted = detect_sugars(pdb_path)
        #     f.write(extracted)
        # except Exception as e:
        #     raise Exception(f"Error running detect_sugars: {e}")
        
    return ring_atoms_path 


if __name__ == "__main__":
    print(DETECT_SUGARS_BIN)
    pdb_path = "/programs/gems/tests/inputs/DManpa1-8DNeup5Acb2-4DFrufa2-OH_structure.pdb"
    workdir = os.getcwd()
    execute(pdb_path, workdir)