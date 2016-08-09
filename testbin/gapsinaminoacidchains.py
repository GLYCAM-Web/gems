###FOR FURTHER INSTRUCTIONS PLEASE REFER TO alternateresidues.py SAMPLE FILE
#SAMPLE COMMAND :
# python gapsinaminoacidchains.py -amino_libs "gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib","gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib","gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminoct12.lib" -pdb "gmml/example/pdb/1Z7E.pdb"

import sys
sys.path.insert(0, '../')
import gmml

temp = gmml.PdbPreprocessor()
amino_libs = gmml.string_vector()


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

temp.ExtractGapsInAminoAcidChains(pdbfile)

missing_residues = temp.GetMissingResidues()
for x in xrange(0, missing_residues.size()):
        missing_residues[x].Print()


###UPDATING GAPS IN AMINO ACID CHAINS###
#MODIFYING n_termination and c_termination ATTRIBUTES OF THE CHAIN TERMINATIONS VECTOR:
#POSSIBLE n_termination OPTIONS: gmml.COCH3, gmml.NH3
#POSSIBLE c_termination OPTIONS: gmml.NH2, gmml.NHCH3, gmml.CO2
missing_residues[0].SetSelectedNTermination(gmml.NH3)
missing_residues[0].SetSelectedCTermination(gmml.NH2)

temp.UpdateGapsInAminoAcidChains(pdbfile, amino_libs, missing_residues)

pdbfile.Write('gapsinaminoacidchains-update.pdb')

