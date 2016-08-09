###FOR FURTHER INSTRUCTIONS PLEASE REFER TO alternateresidues.py SAMPLE FILE
###SAMPLE COMMAND :
# python unknownheavyatoms.py -amino_libs "gmml/dat/lib/GLYCAM_amino_06h.lib","gmml/dat/lib/GLYCAM_aminoct_06h.lib","gmml/dat/lib/GLYCAM_aminont_06h.lib" -prep "gmml/dat/prep/Glycam_06.prep" -pdb "gmml/example/pdb/sucros.pdb"

#If you need to add other libraries for glycam and other residues there are -glycam_libs and -other_libs options available for the command.

import sys
sys.path.insert(0, '../')
import gmml

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

temp.ExtractUnknownHeavyAtoms(pdbfile, amino_libs, glycam_libs, other_libs, prep)	

###FOR GIVING THE FILES MANUALLY AND THROUGH THE COMMAND LINE USE THE FOLOWING SECTION
#amino_libs.push_back("gmml/dat/lib/GLYCAM_amino_06h.lib")
#amino_libs.push_back("gmml/dat/lib/GLYCAM_aminoct_06h.lib")
#amino_libs.push_back("gmml/dat/lib/GLYCAM_aminont_06h.lib")
#prep.push_back("gmml/dat/prep/Glycam_06.prep")
#temp.ExtractUnknownHeavyAtoms("gmml/example/pdb/sucros.pdb", amino_libs, glycam_libs, other_libs, prep)

unrecognized_heavy_atoms = temp.GetUnrecognizedHeavyAtoms()
for x in xrange(0, unrecognized_heavy_atoms.size()):
        unrecognized_heavy_atoms[x].Print()


temp.RemoveUnknownHeavyAtoms(pdbfile, unrecognized_heavy_atoms)

pdbfile.Write('unknownheavyatoms-update.pdb')


