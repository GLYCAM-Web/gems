#SAMPLE COMMAND :
# python pdbpreprocessing.py -libs "gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib","gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib","gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminoct12.lib" -pdb "gmml/example/pdb/1RVZ_New.pdb"

import gmml
import sys

temp = gmml.PdbPreprocessor()
libs = gmml.string_vector()
prep = gmml.string_vector()

for i, arg in enumerate(sys.argv):	
    if arg == '-libs':                       
		arguments = sys.argv[i+1].split(',')
		for argument in arguments:
			libs.push_back(argument)
    elif arg == '-prep':
		arguments = sys.argv[i+1].split(',')
		for argument in arguments:
			prep.push_back(argument)
    elif arg == '-pdb':
		pdb = sys.argv[i+1]

temp.Preprocess(pdb, libs, prep)

pdbfile = gmml.PdbFile(pdb)

###IN ORDER TO UPDATE EACH PARTS OF THE PDB FILE YOU CAN USE THE SAME CODE FROM ANY OF THE SAMPLE FILES, i.e. cysresidues.py
###UPDATING CYS RESIDUES###
disulfide_bonds = temp.GetDisulfideBonds()
disulfide_bonds[0].SetIsBonded(False)

###THIS FUNCTIONS WILL APPLY ALL THE UPDATED INFORMATION
temp.ApplyPreprocessing(pdbfile, libs)
pdbfile.Write('updated_pdb.txt')
