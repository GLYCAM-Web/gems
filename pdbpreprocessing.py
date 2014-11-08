#SAMPLE COMMAND :
# python pdbpreprocessing.py -amino_libs "gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib","gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib","gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminoct12.lib" -prep "gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j-1.prep" -pdb "gmml/example/pdb/1RVZ_New.pdb"

#If you need to add other libraries for glycam and other residues there are -glycam_libs and -other_libs options available for the command. 

import gmml
import sys

temp = gmml.PdbPreprocessor()
amino_libs = gmml.string_vector()
glycam_libs = gmml.string_vector()
other_libs = gmml.string_vector()
prep = gmml.string_vector()

for i, arg in enumerate(sys.argv):	
    if arg == '-amino_libs':                       
		arguments = sys.argv[i+1].split(',')
		for argument in arguments:
			amino_libs.push_back(argument)
    elif arg == '-glycam_libs':
		arguments = sys.argv[i+1].split(',')
		for argument in arguments:
			glycam_libs.push_back(argument)
    elif arg == '-other_libs':
		arguments = sys.argv[i+1].split(',')
		for argument in arguments:
			other_libs.push_back(argument)
    elif arg == '-prep':
		arguments = sys.argv[i+1].split(',')
		for argument in arguments:
			prep.push_back(argument)
    elif arg == '-pdb':
		pdb = sys.argv[i+1]

pdbfile = gmml.PdbFile(pdb)

temp.Preprocess(pdbfile, amino_libs, glycam_libs, other_libs, prep)

###IN ORDER TO UPDATE EACH PARTS OF THE PDB FILE YOU CAN USE THE SAME CODE FROM ANY OF THE SAMPLE FILES, i.e. cysresidues.py
###UPDATING CYS RESIDUES###
#disulfide_bonds = temp.GetDisulfideBonds()
#disulfide_bonds[0].SetIsBonded(False)

###FIRST OPTION:
###THIS FUNCTIONS WILL APPLY ALL THE UPDATED INFORMATION ON THE SELECTED MODEL.
###THE DEFAULT MODEL IS THE FIRST ONE, IN ORDER TO CHANGE IT GIVE ANOTHER MODEL NUMBER AS THE 3RD ARGUMENT TO THE FOLLOWING FUNCTION i.e. temp.ApplyPreprocessingWithTheGivenModelNumber(pdbfile, amino_libs, glycam_libs, prep, 2)
temp.ApplyPreprocessingWithTheGivenModelNumber(pdbfile, amino_libs, glycam_libs, prep)
temp.Print()
###THE DEFAULT MODEL IS THE FIRST ONE, IN ORDER TO CHANGE IT GIVE ANOTHER MODEL NUMBER AS THE 3RD ARGUMENT TO THE FOLLOWING FUNCTION i.e. pdbfile.WriteWithTheGivenModelNumber('updated_pdb.txt', 2). THE GIVEN NUMBER SHOULD MATCH THE PREVIOUS MODEL NUMBER WHICH HAS BEEN GIVEN TO THE ApplyPreprocessingWithTheGivenModelNumber FUNCTION.
pdbfile.WriteWithTheGivenModelNumber('updated_pdb.txt')

###SECOND OPTION:
###THIS FUNCTIONS WILL APPLY ALL THE UPDATED INFORMATION ON ALL THE MODELS.
#temp.ApplyPreprocessing(pdbfile, amino_libs, glycam_libs, prep)
#temp.Print()
#pdbfile.Write('updated_pdb.txt')
