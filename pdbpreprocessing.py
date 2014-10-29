#SAMPLE COMMAND :
# python pdbpreprocessing.py -libs "gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib","gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib","gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminoct12.lib" -prep "gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j-1.prep" -pdb "gmml/example/pdb/1RVZ_New.pdb"

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

pdbfile = gmml.PdbFile(pdb)

temp.Preprocess(pdbfile, libs, prep)

###IN ORDER TO UPDATE EACH PARTS OF THE PDB FILE YOU CAN USE THE SAME CODE FROM ANY OF THE SAMPLE FILES, i.e. cysresidues.py
###UPDATING CYS RESIDUES###
#disulfide_bonds = temp.GetDisulfideBonds()
#disulfide_bonds[0].SetIsBonded(False)

###FIRST OPTION:
###THIS FUNCTIONS WILL APPLY ALL THE UPDATED INFORMATION ON THE SELECTED MODEL.
###THE DEFAULT MODEL IS THE FIRST ONE, IN ORDER TO CHANGE IT GIVE ANOTHER MODEL NUMBER AS THE 3RD ARGUMENT TO THE FOLLOWING FUNCTION i.e. temp.ApplyPreprocessingWithTheGivenModelNumber(pdbfile, libs, 2)
temp.ApplyPreprocessingWithTheGivenModelNumber(pdbfile, libs)
temp.Print()
###THE DEFAULT MODEL IS THE FIRST ONE, IN ORDER TO CHANGE IT GIVE ANOTHER MODEL NUMBER AS THE 3RD ARGUMENT TO THE FOLLOWING FUNCTION i.e. pdbfile.WriteWithTheGivenModelNumber('updated_pdb.txt', 2). THE GIVEN NUMBER SHOULD MATCH THE PREVIOUS MODEL NUMBER WHICH HAS BEEN GIVEN TO THE ApplyPreprocessingWithTheGivenModelNumber FUNCTION.
pdbfile.WriteWithTheGivenModelNumber('updated_pdb.txt')

###SECOND OPTION:
###THIS FUNCTIONS WILL APPLY ALL THE UPDATED INFORMATION ON ALL THE MODELS.
#temp.ApplyPreprocessing(pdbfile, libs)
#temp.Print()
#pdbfile.Write('updated_pdb.txt')
