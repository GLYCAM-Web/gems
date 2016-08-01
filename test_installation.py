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

if sys.argv[1] == '--help':  
	print("""
Available options:
	-amino_libs : amino acid library file(s) (e.g. gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib)
	-glycam_libs: glycam library file(s)
	-other_libs : other kinds of library files
	-prep       : prep file(s) (e.g. gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j-1.prep)
	-pdb        : pdb file (e.g. gmml/example/pdb/1RVZ_New.pdb)
	-cnf        : configuration file as an argument. 

	Sample file format:
		amino_libs
		gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib
		gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib
		glycam_libs
		other_libs
		prep
		gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j-1.prep
		pdb
		gmml/example/pdb/1RVZ_New.pdb
""")
	sys.exit()
elif sys.argv[1] == '-cnf':      
	with open(sys.argv[2], 'r') as my_file:
	    conf_file = my_file.readlines()
	for i in range(0, len(conf_file)):
		conf_file[i] = conf_file[i].strip()
	i = 0
	if conf_file[i] == 'amino_libs':
		i = i+1
		while conf_file[i] != 'glycam_libs':
			amino_libs.push_back(conf_file[i])
			i = i+1	
		i = i+1
		while conf_file[i] != 'other_libs':
			glycam_libs.push_back(conf_file[i])
			i = i+1	
		i = i+1
		while conf_file[i] != 'prep':
			other_libs.push_back(conf_file[i])
			i = i+1	
		i = i+1
		while conf_file[i] != 'pdb':
			prep.push_back(conf_file[i])
			i = i+1	
		i = i+1
		pdb = conf_file[i]
	else:
		print('invalid configuration file format')
else:
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
###THE DEFAULT MODEL IS THE FIRST ONE, IN ORDER TO CHANGE IT GIVE ANOTHER MODEL NUMBER AS THE 5th ARGUMENT TO THE FOLLOWING FUNCTION i.e. temp.ApplyPreprocessingWithTheGivenModelNumber(pdbfile, amino_libs, 	glycam_libs, prep, 2)
temp.ApplyPreprocessingWithTheGivenModelNumber(pdbfile, amino_libs, glycam_libs, prep)
temp.Print()
seq_map = pdbfile.GetSequenceNumberMapping()
print(seq_map.size())
for x in seq_map:
	print(x, seq_map[x])
###THE DEFAULT MODEL IS THE FIRST ONE, IN ORDER TO CHANGE IT GIVE ANOTHER MODEL NUMBER AS THE 2ND ARGUMENT TO THE FOLLOWING FUNCTION i.e. pdbfile.WriteWithTheGivenModelNumber('updated_pdb.txt', 2). THE 		GIVEN NUMBER SHOULD MATCH THE PREVIOUS MODEL NUMBER WHICH HAS BEEN GIVEN TO THE ApplyPreprocessingWithTheGivenModelNumber FUNCTION.
pdbfile.WriteWithTheGivenModelNumber('updated_pdb.txt')

###SECOND OPTION:
###THIS FUNCTIONS WILL APPLY ALL THE UPDATED INFORMATION ON ALL THE MODELS.
#temp.ApplyPreprocessing(pdbfile, amino_libs, glycam_libs, prep)
#temp.Print()
#pdbfile.Write('updated_pdb.txt')
